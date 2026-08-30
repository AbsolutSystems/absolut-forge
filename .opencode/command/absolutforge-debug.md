---
description: Diagnose one concrete failure and fix it only when explicitly requested.
---

Use the AbsolutForge `debug` skill.

Arguments: the failure description, error output, or failing command.

Supplied arguments: $ARGUMENTS

Read the `debug` skill and follow its contract exactly, including every precondition, artifact schema, and safety boundary it links. If a required argument is missing, ask for it instead of guessing.

Diagnose from evidence first. Edit source only on explicit fix intent.
