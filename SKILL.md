---
name: retroengine-pro
description: Reconstruct and compare functional website and app workflows using authorized observations, recordings, manuals, or source code. Use for documenting, reproducing, or migrating an existing procedure.
---

Read the [working prompt](references/prompt.md) and apply it to the scenario. Start with the supplied sources. Use authorized tools when you need to observe the workflow. For desktop apps without direct access, use recordings, screenshots, or manuals. Record the user role, the version when known, and the last state you verified directly.

Consult the [analysis methods](references/methods.md) when comparing runtime behavior with static evidence, checking an export, or reconstructing a data schema. Stop before external changes that lack authorization and record the last observable state.

Use the following JSON format for a reproducible Markdown report. Give each source a short identifier and a precise locator.

```json
{
  "title": "Export orders",
  "context": "Demo, operator account",
  "prerequisites": ["One test order"],
  "sources": {"V1": "Demo recording, 00:12"},
  "steps": [
    {"id": "export.format", "action": "Open Export", "outcome": "The menu includes CSV", "status": "observed", "sources": ["V1"]}
  ],
  "variants": [
    {
      "condition": "The order list is empty",
      "steps": [
        {"action": "Open Export", "outcome": "Check whether CSV is available", "status": "unverified", "sources": []}
      ]
    }
  ],
  "open_questions": ["Check which roles can export"],
  "verification": "Reviewed the demo recording"
}
```

The `variants` field is optional. Steps use `observed`, `inferred`, or `unverified`. An observed or inferred step needs at least one source. Run `python3 scripts/workflow.py spec observations.json` from the repository root and check the result against the evidence.

For comparison, give every observed step a unique `id` across the main workflow and variants. Record the new implementation separately with the same IDs and its own evidence. Run `python3 scripts/workflow.py compare baseline.json candidate.json`. Keep outcome wording consistent because the comparison is textual.
