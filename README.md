# retroengine_pro

A Codex skill and Python CLI for documenting website and app workflows and comparing observed outcomes across implementations.

1. **Study** the workflow using authorized screenshots, recordings, manuals, or source code. Record actions, outcomes, and evidence in JSON.
2. **Specify** the workflow in Markdown and use it as a brief for your own implementation. [Evidence schema](SKILL.md)
3. **Verify** the implementation using the same scenarios. Record fresh evidence in a second JSON file and reuse the step IDs.

## Quick start

Use Python 3.9 or later. From the repository root:

```bash
python3 scripts/workflow.py spec examples/orders.json > specification.md
python3 scripts/workflow.py compare examples/orders.json examples/orders.json
```

The second command compares the fictional example with itself and reports two matches. To try a mismatch, copy the JSON, change an `outcome`, and use the copy as the second argument.

The CLI compares observed outcomes by `id` after normalizing whitespace. Use consistent wording in both files. An observed outcome that differs or has no comparable observation returns exit code 1. Extra candidate observations are informational. Invalid input returns exit code 2.

The CLI reads local JSON and writes reports to standard output. Evidence collection and implementation happen separately. The [working prompt](references/prompt.md) guides those steps with Codex.

Earlier versions used Italian command names and JSON fields. Use [the current schema](SKILL.md) when migrating an existing evidence file.
