#!/usr/bin/env python3
"""Inter-IA V4-001: dos procesos Python, transporte por archivos JSON, sin APIs de IA."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

EXPECTED_SHA = '04ec94bd1df74a3d5309668011f1b0c014dc97c6adf068d03b4690e12d7014d4'
EXPECTED_SIZE = 920
ARTIFACT = Path('experiments/federacion-documental/EXP-0001/replica/EXP-0001.md')

def utc():
    return datetime.now(timezone.utc).isoformat()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def worker(task_path, response_path, artifact_path):
    task = json.loads(task_path.read_text(encoding='utf-8'))
    if set(task) != {'task_id', 'artifact_id', 'expected_sha256', 'scenario'} or task['artifact_id'] != 'KOS-IIA-EXP-0001':
        raise ValueError('Tarea inválida')
    if task['scenario'] == 'invalid_response':
        response_path.write_text('{"task_id":', encoding='utf-8')
        return
    raw = artifact_path.read_bytes()
    if task['scenario'] == 'corrupt':
        raw += b'\nCORRUPTION-INJECTED\n'
    if task['scenario'] not in ('normal', 'corrupt'):
        raise ValueError('Escenario desconocido')
    calculated = digest(raw)
    write_json(response_path, {'task_id': task['task_id'], 'status': 'COMPLETED',
                               'computed_sha256': calculated, 'expected_sha256': task['expected_sha256'],
                               'size_bytes': len(raw), 'integrity_valid': calculated == task['expected_sha256'],
                               'timestamp_utc': utc()})

def validate_response(path, task_id):
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return False, 'INVALID_JSON: ' + type(exc).__name__, None
    required = {'task_id', 'status', 'computed_sha256', 'expected_sha256', 'size_bytes', 'integrity_valid', 'timestamp_utc'}
    if not isinstance(data, dict) or set(data) != required or data['task_id'] != task_id or data['status'] != 'COMPLETED':
        return False, 'INVALID_SCHEMA_OR_TASK', data
    if not isinstance(data['computed_sha256'], str) or len(data['computed_sha256']) != 64 or not isinstance(data['size_bytes'], int) or type(data['integrity_valid']) is not bool:
        return False, 'INVALID_TYPES', data
    if data['expected_sha256'] != EXPECTED_SHA or data['integrity_valid'] != (data['computed_sha256'] == EXPECTED_SHA):
        return False, 'INCONSISTENT_RESPONSE', data
    return True, 'VALID_RESPONSE', data

def run(output, artifact):
    original = artifact.read_bytes()
    if len(original) != EXPECTED_SIZE or digest(original) != EXPECTED_SHA:
        raise ValueError('La fuente primaria local no coincide con EXP-0001 oficial')
    output.mkdir(parents=True, exist_ok=True)
    results = []
    start_all = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='inter-ia-v4-001-') as temp:
        exchange = Path(temp)
        for name, mode in [('A', 'normal'), ('B', 'corrupt'), ('C', 'invalid_response')]:
            task_id = 'V4-001-' + name
            task_path = exchange / ('task_' + name + '.json')
            response_path = exchange / ('response_' + name + '.json')
            write_json(task_path, {'task_id': task_id, 'artifact_id': 'KOS-IIA-EXP-0001',
                                   'expected_sha256': EXPECTED_SHA, 'scenario': mode})
            start = time.perf_counter()
            completed = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker',
                                        '--task', str(task_path), '--response', str(response_path),
                                        '--artifact', str(artifact.resolve())], capture_output=True, text=True, timeout=15)
            valid, reason, response = validate_response(response_path, task_id)
            if name == 'A':
                passed = completed.returncode == 0 and valid and response['integrity_valid'] is True and response['size_bytes'] == EXPECTED_SIZE
            elif name == 'B':
                passed = completed.returncode == 0 and valid and response['integrity_valid'] is False and response['computed_sha256'] != EXPECTED_SHA
            else:
                passed = completed.returncode == 0 and not valid and reason.startswith('INVALID_JSON')
            results.append({'scenario': name, 'mode': mode, 'result': 'PASS' if passed else 'FAIL',
                            'worker_exit_code': completed.returncode, 'response_valid': valid,
                            'validation_reason': reason, 'computed_sha256': response.get('computed_sha256') if isinstance(response, dict) else None,
                            'elapsed_ms': round((time.perf_counter()-start)*1000, 2), 'worker_stderr': completed.stderr[:300]})
            write_json(output / ('task_' + name + '.json'), json.loads(task_path.read_text(encoding='utf-8')))
            (output / ('response_' + name + '.json')).write_bytes(response_path.read_bytes())
    overall = 'PASS' if all(x['result'] == 'PASS' for x in results) else 'FAIL'
    cert = {'experiment': 'V4-001', 'timestamp_utc': utc(), 'result': overall,
            'scope': 'dos procesos Python locales con intercambio JSON por directorio temporal',
            'artifact': str(ARTIFACT), 'artifact_size_bytes': len(original), 'artifact_sha256': digest(original),
            'tests': results, 'duration_ms': round((time.perf_counter()-start_all)*1000, 2),
            'manual_message_transfers_during_run': 0,
            'human_approval': 'PENDIENTE', 'production_interoperability': 'NO_DEMOSTRADA',
            'limitations': ['No utiliza modelos de IA ni demuestra independencia cognitiva',
                            'No demuestra comunicación entre ChatGPT y Gemini',
                            'No implementa A2A oficial ni transporte remoto',
                            'No prueba continuidad integral N+1']}
    write_json(output / 'certificado.json', cert)
    print(json.dumps(cert, ensure_ascii=False, indent=2))
    return 0 if overall == 'PASS' else 1

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--worker', action='store_true')
    p.add_argument('--task', type=Path)
    p.add_argument('--response', type=Path)
    p.add_argument('--artifact', type=Path, default=ARTIFACT)
    p.add_argument('--output', type=Path, default=Path('v4-001-evidencia'))
    a = p.parse_args()
    if a.worker:
        if not a.task or not a.response:
            p.error('Worker requiere --task y --response')
        worker(a.task, a.response, a.artifact)
        return 0
    return run(a.output, a.artifact)

if __name__ == '__main__':
    sys.exit(main())
