#!/usr/bin/env python3
"""Converte evidenze curate da un operatore in una procedura Markdown."""
import argparse
import json
import re
from pathlib import Path


def inline(value):
    if not isinstance(value, str) or not value.split():
        raise ValueError("Attesa una stringa non vuota")
    return re.sub(r'([\\`*_{}\[\]()<>#+!|~&])', r'\\\1', " ".join(value.split()))


def items(value):
    if not isinstance(value, list):
        raise ValueError("Atteso un elenco")
    return value


def render_steps(value, sources):
    steps = items(value)
    if not steps:
        raise ValueError("Serve almeno un passo")
    lines = []
    for index, step in enumerate(steps, 1):
        if not isinstance(step, dict):
            raise ValueError(f"Passo {index}: atteso un oggetto")
        status = step["stato"]
        if status not in ("osservato", "inferito", "da verificare"):
            raise ValueError(f"Passo {index}: stato sconosciuto")
        references = items(step["fonti"])
        if status != "da verificare" and not references:
            raise ValueError(f"Passo {index}: manca una fonte")
        for reference in references:
            if not isinstance(reference, str) or reference not in sources:
                raise ValueError(f"Passo {index}: riferimento a una fonte sconosciuta")
        labels = ", ".join(inline(reference) for reference in references)
        evidence = f" · Fonti {labels}" if labels else ""
        lines.append(f"{index}. **{inline(step['azione'])}** — {inline(step['esito'])} "
                     f"({status}{evidence})")
    return lines


def render(data):
    if not isinstance(data, dict):
        raise ValueError("Atteso un oggetto JSON")
    sources = data["fonti"]
    if not isinstance(sources, dict):
        raise ValueError("fonti deve essere un oggetto")
    source_lines = [f"- {inline(key)} — {inline(value)}" for key, value in sources.items()]
    lines = [f"# {inline(data['titolo'])}", "", inline(data["contesto"]), ""]
    lines.extend(["## Prerequisiti", ""])
    lines.extend(f"- {inline(entry)}" for entry in items(data["prerequisiti"]))
    lines.extend(["", "## Procedura", "", *render_steps(data["passi"], sources)])
    variants = items(data.get("varianti", []))
    if variants:
        lines.extend(["", "## Varianti", ""])
    for variant in variants:
        if not isinstance(variant, dict):
            raise ValueError("Variante: atteso un oggetto")
        lines.extend([
            f"### {inline(variant['condizione'])}", "",
            *render_steps(variant["passi"], sources), "",
        ])
    if variants:
        lines.pop()
    if source_lines:
        lines.extend(["", "## Fonti", "", *source_lines])
    pending = items(data["punti_aperti"])
    if pending:
        lines.extend(["", "## Punti aperti", ""])
        lines.extend(f"- {inline(entry)}" for entry in pending)
    lines.extend(["", "## Verifica", "", inline(data["verifica"])])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="File JSON delle osservazioni")
    args = parser.parse_args()
    try:
        report = render(json.loads(args.input.read_text(encoding="utf-8")))
    except (KeyError, ValueError, OSError) as error:
        parser.error(str(error))
    print(report)


if __name__ == "__main__":
    main()
