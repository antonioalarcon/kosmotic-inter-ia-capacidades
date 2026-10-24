#!/usr/bin/env python3
"""Genera una vista de consulta temporal desde un KKO. Nunca publica ni modifica docs/."""

import argparse
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KKO = "knowledge/agentes/KKO-IA-AGENTES-001.md"
DEFAULT_OUTPUT = "dist/preview/kosmowiki/agentes-ia.md"
SECTIONS = (
    ("Definición", "Qué es"),
    ("Explicación para cualquier persona", "En palabras sencillas"),
    ("Funcionamiento básico", "Cómo funciona"),
    ("Límites y riesgos", "Límites y riesgos"),
    ("Relación con KosmoTIC", "Gobernanza y relaciones"),
    ("Fuentes de referencia", "Fuentes"),
)


def load_kko(path, allow_draft=False):
    raw = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.S)
    if not match:
        raise ValueError("El KKO no tiene frontmatter YAML válido")
    meta = yaml.safe_load(match.group(1))
    if not isinstance(meta, dict) or not all(meta.get(k) for k in ("id", "version", "title")):
        raise ValueError("Faltan id, version o title en el KKO")
    status = meta.get("status")
    if status != "validated" and not (allow_draft and status == "draft"):
        raise ValueError("Solo se generan vistas de KKO validados; para pruebas de borradores use --allow-draft")
    body = raw[match.end():]
    headers = list(re.finditer(r"(?m)^## (.+?)\s*$", body))
    sections = {}
    for i, header in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(body)
        sections[header.group(1).strip()] = body[header.end():end].strip()
    missing = [name for name, _ in SECTIONS if not sections.get(name)]
    if missing:
        raise ValueError("Faltan secciones canónicas: " + ", ".join(missing))
    return meta, sections


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kko", default=DEFAULT_KKO, help="Ruta del KKO dentro de knowledge/")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Salida temporal dentro de dist/preview/")
    parser.add_argument("--allow-draft", action="store_true", help="Permitir KKO en draft solo para una vista temporal de revisión")
    args = parser.parse_args()
    source = (ROOT / args.kko).resolve()
    target = (ROOT / args.output).resolve()
    if not source.is_relative_to((ROOT / "knowledge").resolve()):
        parser.error("El KKO debe estar en knowledge/")
    if not target.is_relative_to((ROOT / "dist/preview").resolve()):
        parser.error("La salida debe permanecer en dist/preview/; nunca en docs/ o web/")
    meta, sections = load_kko(source, allow_draft=args.allow_draft)
    rel_source = source.relative_to(ROOT).as_posix()
    parts = [
        "---",
        f"id: {json.dumps('KOS-PREVIEW-' + str(meta['id']), ensure_ascii=False)}",
        f"source_kko: {json.dumps(str(meta['id']), ensure_ascii=False)}",
        f"source_version: {json.dumps(str(meta['version']))}",
        f"source_path: {json.dumps(rel_source)}",
        "representation: kosmowiki",
        "status: draft",
        "generated: true",
        "publication_approved: false",
        "---",
        "",
        f"# {meta['title']} · vista KosmoWiki (borrador)",
        "",
        "> Vista generada automáticamente para revisión humana. No es una publicación aprobada ni sustituye al KKO canónico.",
    ]
    for canonical, heading in SECTIONS:
        parts.extend(["", f"## {heading}", "", sections[canonical]])
    parts.extend(["", f"**Fuente canónica:** `{rel_source}` · versión `{meta['version']}`.", ""])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(parts), encoding="utf-8")
    print(f"OK: {source.relative_to(ROOT)} -> {target.relative_to(ROOT)} (solo borrador)")


if __name__ == "__main__":
    main()
