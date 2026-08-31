---
description: Pressure-test a Feature Brief or a not-yet-executed planned implementation plan, recorded as a consultation report.
---

Use the AbsolutForge `consult` skill.

Arguments: first the subject path — the canonical Feature Brief for Brief mode, or the canonical `implementation-plan.md` for Plan mode — then any further paths to read as additional context.

Supplied arguments: $ARGUMENTS

Read the `consult` skill and follow its contract exactly, including every precondition, artifact schema, and safety boundary it links. If a required argument is missing, ask for it instead of guessing.

Write one finding batch to `absolutforge/features/{slug}/consult-{slug}.md` and report it here. Change no other file: in Brief mode only after explicit human approval of specific finding IDs, in Plan mode never.
