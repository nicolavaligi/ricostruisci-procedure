#!/usr/bin/env python3
"""Render structured workflow evidence as a Markdown procedure."""
import argparse
import json
import re
from pathlib import Path


def inline(value):
    if not isinstance(value, str) or not value.split():
        raise ValueError("Expected a non-empty string")
    return re.sub(r'([\\`*_{}\[\]()<>#+!|~&])', r'\\\1', " ".join(value.split()))


def items(value):
    if not isinstance(value, list):
        raise ValueError("Expected a list")
    return value


def render_steps(value, sources):
    steps = items(value)
    if not steps:
        raise ValueError("At least one step is required")
    lines = []
    for index, step in enumerate(steps, 1):
        if not isinstance(step, dict):
            raise ValueError(f"Step {index}: expected an object")
        status = step["status"]
        if status not in ("observed", "inferred", "unverified"):
            raise ValueError(f"Step {index}: unknown status")
        references = items(step["sources"])
        if status != "unverified" and not references:
            raise ValueError(f"Step {index}: an evidence reference is required")
        for reference in references:
            if not isinstance(reference, str) or reference not in sources:
                raise ValueError(f"Step {index}: unknown evidence reference")
        labels = ", ".join(inline(reference) for reference in references)
        evidence = f" · Sources {labels}" if labels else ""
        lines.append(f"{index}. **{inline(step['action'])}** — {inline(step['outcome'])} "
                     f"({status}{evidence})")
    return lines


def render(data):
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object")
    sources = data["sources"]
    if not isinstance(sources, dict):
        raise ValueError("sources must be an object")
    source_lines = [f"- {inline(key)} — {inline(value)}" for key, value in sources.items()]
    lines = [f"# {inline(data['title'])}", "", inline(data["context"]), ""]
    lines.extend(["## Prerequisites", ""])
    lines.extend(f"- {inline(entry)}" for entry in items(data["prerequisites"]))
    lines.extend(["", "## Procedure", "", *render_steps(data["steps"], sources)])
    variants = items(data.get("variants", []))
    if variants:
        lines.extend(["", "## Variants", ""])
    for variant in variants:
        if not isinstance(variant, dict):
            raise ValueError("Variant: expected an object")
        lines.extend([
            f"### {inline(variant['condition'])}", "",
            *render_steps(variant["steps"], sources), "",
        ])
    if variants:
        lines.pop()
    if source_lines:
        lines.extend(["", "## Sources", "", *source_lines])
    pending = items(data["open_questions"])
    if pending:
        lines.extend(["", "## Open questions", ""])
        lines.extend(f"- {inline(entry)}" for entry in pending)
    lines.extend(["", "## Verification", "", inline(data["verification"])])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Workflow observations JSON file")
    args = parser.parse_args()
    try:
        report = render(json.loads(args.input.read_text(encoding="utf-8")))
    except (KeyError, ValueError, OSError) as error:
        parser.error(str(error))
    print(report)


if __name__ == "__main__":
    main()
