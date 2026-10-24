"""Prueba de vida N+1 con paquete sintético, sin conexión a servicios.

Uso: python -m cdt.restore_probe /ruta/destino
Crear paquete en un medio, copiarlo manualmente a otro medio independiente
y ejecutar 'verify' allí: python -m cdt.restore_probe verify /ruta/destino
"""
import hashlib
import json
import sys
from pathlib import Path

from .engine import inspect_records

SAMPLE = [{"id": "A1", "name": " Ana "}, {"id": "a1", "name": ""}, {"id": "B2", "name": "Luis"}]
SCHEMA = {"required": ["id", "name"], "unique_key": "id"}


def _encoded(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def create(destination):
    folder = Path(destination)
    folder.mkdir(parents=True, exist_ok=True)
    if any(folder.iterdir()):
        raise FileExistsError("Destino no vacío: se prohíbe sobrescribir")
    payload = {
        "schema.json": _encoded(SCHEMA),
        "synthetic_data.json": _encoded(SAMPLE),
        "quality_report.json": _encoded(inspect_records(SAMPLE, tuple(SCHEMA["required"]), SCHEMA["unique_key"])),
    }
    for name, data in payload.items():
        (folder / name).write_bytes(data)
    manifest = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    (folder / "sha256.json").write_bytes(_encoded(manifest))
    return manifest


def verify(destination):
    folder = Path(destination)
    manifest = json.loads((folder / "sha256.json").read_text(encoding="utf-8"))
    if set(manifest) != {"schema.json", "synthetic_data.json", "quality_report.json"}:
        raise ValueError("Manifiesto inválido")
    for name, digest in manifest.items():
        if hashlib.sha256((folder / name).read_bytes()).hexdigest() != digest:
            raise ValueError("Fallo de integridad: " + name)
    data = json.loads((folder / "synthetic_data.json").read_text(encoding="utf-8"))
    schema = json.loads((folder / "schema.json").read_text(encoding="utf-8"))
    report = inspect_records(data, tuple(schema["required"]), schema["unique_key"])
    if _encoded(report) != (folder / "quality_report.json").read_bytes():
        raise ValueError("Informe no reproducible")
    return True


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(json.dumps(create(sys.argv[1]), indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == "verify":
        print("RESTORE_OK" if verify(sys.argv[2]) else "RESTORE_FAILED")
    else:
        raise SystemExit("Uso: python -m cdt.restore_probe [verify] DESTINO")
