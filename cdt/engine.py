"""CDT v1.0: inspección no destructiva sobre registros en memoria.

No accede a archivos, redes ni servicios. No persiste ni modifica originales.
"""
from collections import Counter
from copy import deepcopy
from typing import Any


def _canonical(value: Any) -> str:
    return str(value).strip().casefold() if value is not None else ""


def inspect_records(records: list[dict], required: tuple[str, ...] = (),
                    unique_key: str | None = None) -> dict:
    """Informe de calidad sin incluir datos personales ni valores originales."""
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise TypeError("records debe ser una lista de diccionarios")
    columns = sorted(set().union(*(r.keys() for r in records))) if records else []
    missing = {
        col: sum(r.get(col) is None or
                 (isinstance(r.get(col), str) and not r[col].strip())
                 for r in records)
        for col in columns
    }
    for col in required:
        if col not in missing:
            missing[col] = len(records)
    keys = [_canonical(row.get(unique_key)) for row in records] if unique_key else []
    valid_keys = [k for k in keys if k]
    duplicates = sum(n - 1 for n in Counter(valid_keys).values() if n > 1)
    return {
        "version": "KOS-IIA-CDT-20261009-V1.0",
        "rows": len(records),
        "columns": columns,
        "missing_by_column": missing,
        "duplicate_keys": duplicates,
        "missing_unique_keys": len(keys) - len(valid_keys) if unique_key else None,
        "required_columns": list(required),
        "read_only": True,
    }


def normalize_records(records: list[dict], fields: tuple[str, ...]) -> list[dict]:
    """Devuelve copia normalizada; no cambia los registros recibidos.

    La normalización de espacios es explícita y restringida a campos indicados.
    No se eliminan duplicados ni se imputan valores.
    """
    result = deepcopy(records)
    for row in result:
        for field in fields:
            if isinstance(row.get(field), str):
                row[field] = row[field].strip()
    return result
