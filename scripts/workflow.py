#!/usr/bin/env python3
"""Generate functional specifications and compare local workflow observations."""
import argparse
import json
from pathlib import Path

from render_procedure import inline, render


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def observed_checks(document):
    render(document)
    checks = {}
    seen = set()
    flows = [document["steps"], *(variant["steps"] for variant in document.get("variants", []))]
    for flow in flows:
        for step in flow:
            identifier = step.get("id")
            if step["status"] == "observed" or identifier is not None:
                if not isinstance(identifier, str) or not identifier or identifier != identifier.strip():
                    raise ValueError("Every observed step must have a stable ID")
                if identifier in seen:
                    raise ValueError(f"Duplicate ID: {identifier}")
                seen.add(identifier)
            if step["status"] == "observed":
                checks[identifier] = " ".join(step["outcome"].split())
    return checks


def compare(reference, candidate):
    expected = observed_checks(reference)
    actual = observed_checks(candidate)
    if not expected:
        raise ValueError("The baseline must contain at least one observed outcome")
    lines = ["# Observed outcome comparison", ""]
    missing = changed = 0
    for identifier, outcome in expected.items():
        label = inline(identifier)
        if identifier not in actual:
            missing += 1
            lines.append(f"- **Unverified** · {label} · expected {inline(outcome)}")
        elif actual[identifier] != outcome:
            changed += 1
            lines.append(f"- **Different** · {label} · expected {inline(outcome)} · actual "
                         f"{inline(actual[identifier])}")
        else:
            lines.append(f"- **Match** · {label} · {inline(outcome)}")
    for identifier in sorted(actual.keys() - expected.keys()):
        lines.append(f"- **Additional** · {inline(identifier)} · {inline(actual[identifier])}")
    lines.extend(["", f"Matches {len(expected) - missing - changed}/{len(expected)} · "
                  f"Differences {changed} · Unverified {missing}"])
    return "\n".join(lines), bool(missing or changed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    spec = commands.add_parser("spec", help="Generate a Markdown specification")
    spec.add_argument("reference", type=Path)
    check = commands.add_parser("compare", help="Compare observed outcomes by ID")
    check.add_argument("reference", type=Path)
    check.add_argument("candidate", type=Path)
    args = parser.parse_args()
    try:
        reference = read_json(args.reference)
        if args.command == "spec":
            print(render(reference))
            return 0
        report, differences = compare(reference, read_json(args.candidate))
        print(report)
        return int(differences)
    except (KeyError, ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
