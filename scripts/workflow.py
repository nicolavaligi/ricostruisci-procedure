#!/usr/bin/env python3
"""Genera specifiche funzionali e confronta evidenze locali di due workflow."""
import argparse
import json
from pathlib import Path

from render_procedura import inline, render


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def observed_checks(document):
    render(document)
    checks = {}
    seen = set()
    flows = [document["passi"], *(variant["passi"] for variant in document.get("varianti", []))]
    for flow in flows:
        for step in flow:
            identifier = step.get("id")
            if step["stato"] == "osservato" or identifier is not None:
                if not isinstance(identifier, str) or not identifier or identifier != identifier.strip():
                    raise ValueError("Ogni passo osservato deve avere un ID stabile")
                if identifier in seen:
                    raise ValueError(f"ID duplicato: {identifier}")
                seen.add(identifier)
            if step["stato"] == "osservato":
                checks[identifier] = " ".join(step["esito"].split())
    return checks


def compare(reference, candidate):
    expected = observed_checks(reference)
    actual = observed_checks(candidate)
    if not expected:
        raise ValueError("Il riferimento deve contenere almeno un esito osservato")
    lines = ["# Confronto degli esiti osservati", ""]
    missing = changed = 0
    for identifier, outcome in expected.items():
        label = inline(identifier)
        if identifier not in actual:
            missing += 1
            lines.append(f"- **Da verificare** · {label} · atteso {inline(outcome)}")
        elif actual[identifier] != outcome:
            changed += 1
            lines.append(f"- **Differente** · {label} · atteso {inline(outcome)} · rilevato "
                         f"{inline(actual[identifier])}")
        else:
            lines.append(f"- **Conforme** · {label} · {inline(outcome)}")
    for identifier in sorted(actual.keys() - expected.keys()):
        lines.append(f"- **Aggiuntivo** · {inline(identifier)} · {inline(actual[identifier])}")
    lines.extend(["", f"Conformi {len(expected) - missing - changed}/{len(expected)} · "
                  f"Differenti {changed} · Da verificare {missing}"])
    return "\n".join(lines), bool(missing or changed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    spec = commands.add_parser("specifica", help="Genera una specifica Markdown")
    spec.add_argument("reference", type=Path)
    check = commands.add_parser("confronta", help="Confronta gli esiti osservati per ID")
    check.add_argument("reference", type=Path)
    check.add_argument("candidate", type=Path)
    args = parser.parse_args()
    try:
        reference = read_json(args.reference)
        if args.command == "specifica":
            print(render(reference))
            return 0
        report, differences = compare(reference, read_json(args.candidate))
        print(report)
        return int(differences)
    except (KeyError, ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
