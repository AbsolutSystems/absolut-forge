---
description: Implement an accepted Feature Brief using automatic or explicit strategy selection.
---

Use the AbsolutForge `build` skill.

Arguments: the canonical Feature Brief path, optionally followed by `--strategy=autonomous` or `--strategy=planned`.

Supplied arguments: $ARGUMENTS

Read the `build` skill and follow its contract exactly, including every precondition, artifact schema, and safety boundary it links. If a required argument is missing, ask for it instead of guessing.

At Ready, select and record a strategy and reason under the shared Build contract. At Building, resume the recorded strategy and methodology; a conflicting override is refused before mutation.
