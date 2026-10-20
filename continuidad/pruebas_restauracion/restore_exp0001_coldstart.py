#!/usr/bin/env python3
"""EXP-0001: recuperación en frío desde la API de GitHub (biblioteca estándar).

No requiere credenciales para repositorios públicos. Para repositorios privados:
export GITHUB_TOKEN=...  (nunca poner el token en archivos ni argumentos).
Ejecución: python continuidad/pruebas_restauracion/restore_exp0001_coldstart.py /ruta/DESTINO_NUEVO
El destino NO debe existir. El script no modifica Drive, GitHub ni otros archivos.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

REPOSITORY = "antonioalarcon/kosmotic-inter-ia-capacidades"
SOURCE_REF = "exp/exp-0001-manifest-20261016"
PREFIX = "experiments/federacion-documental/EXP-0001"
MANIFEST_PATH = PREFIX + "/manifest.json"
ARTIFACT_PATH = PREFIX + "/replica/EXP-0001.md"
EXPECTED_SHA256 = "04ec94bd1df74a3d5309668011f1b0c014dc97c6adf068d03b4690e12d7014d4"
EXPECTED_SIZE = 920
TEST_ID = "EXP-0001-COLDSTART-20261019"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def github_fetch(path: str) -> bytes:
    """Descarga el contenido REAL por HTTPS de GitHub, no de un fixture."""
    url = ("https://api.github.com/repos/" + REPOSITORY + "/contents/"
           + quote(path, safe="/") + "?ref=" + quote(SOURCE_REF, safe=""))
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "KosmoTIC-Inter-IA-EXP0001-ColdStart",
               "X-GitHub-Api-Version": "2022-11-28",
               "Cache-Control": "no-cache"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("encoding") != "base64" or not isinstance(payload.get("content"), str):
        raise ValueError("GitHub no devolvió contenido Base64 verificable")
    return base64.b64decode("".join(payload["content"].split()), validate=True)


def restore(destination: Path, fetcher=github_fetch, clock=None) -> dict:
    """Falla de forma cerrada: valida manifiesto y bytes antes de escribir."""
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError("El destino ya existe; no se permite sobrescribir: " + str(destination))
    if destination.parent.resolve() == destination.resolve():
        raise ValueError("Destino inválido")
    manifest_bytes = fetcher(MANIFEST_PATH)
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    if (manifest.get("gid") != "KOS-IIA-EXP-0001"
            or manifest.get("vid") != "V0.1"
            or manifest.get("sha256") != EXPECTED_SHA256
            or manifest.get("size_bytes") != EXPECTED_SIZE):
        raise ValueError("Manifiesto no coincide con los valores fijados")
    artifact = fetcher(ARTIFACT_PATH)
    if len(artifact) != EXPECTED_SIZE or sha256(artifact) != EXPECTED_SHA256:
        raise ValueError("Integridad fallida: longitud o SHA-256 de la réplica")
    if artifact.startswith(b"\xef\xbb\xbf") or b"\r" in artifact or not artifact.endswith(b"\n"):
        raise ValueError("Formato inválido: BOM, CR o falta LF final")
    destination.mkdir(parents=True, exist_ok=False)
    restored = destination / "EXP-0001.md"
    with restored.open("xb") as handle:
        handle.write(artifact)
    recovered = restored.read_bytes()
    if recovered != artifact or sha256(recovered) != EXPECTED_SHA256:
        raise ValueError("Lectura posterior de restauración no coincide")
    timestamp = clock() if clock else datetime.now(timezone.utc).isoformat()
    certificate = {
        "test_id": TEST_ID,
        "timestamp_utc": timestamp,
        "result": "PASS",
        "scope": "recuperacion_documental_en_directorio_nuevo",
        "fetch_method": "GitHub Contents API" if fetcher is github_fetch else "TEST_FIXTURE",
        "repository": REPOSITORY,
        "source_ref": SOURCE_REF,
        "manifest_path": MANIFEST_PATH,
        "artifact_path": ARTIFACT_PATH,
        "size_bytes": len(recovered),
        "sha256_expected": EXPECTED_SHA256,
        "sha256_restored": sha256(recovered),
        "binary_identical": recovered == artifact,
        "no_overwrite": True,
        "human_approval": "PENDIENTE",
        "federated_homologation": "PENDIENTE",
        "limitations": [
            "No acredita recuperación integral ante caída de proveedor",
            "No acredita disponibilidad sin red",
            "La réplica existe en rama no fusionada; no hay sincronización automática",
            "La aprobación humana y la prueba federada siguen pendientes"
        ],
    }
    with (destination / "certificado.json").open("x", encoding="utf-8") as handle:
        json.dump(certificate, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return certificate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="Directorio de destino inexistente")
    args = parser.parse_args()
    try:
        result = restore(args.destination)
    except (OSError, ValueError, HTTPError, URLError, json.JSONDecodeError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
