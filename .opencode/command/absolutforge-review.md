---
description: Run one independent read-only whole-feature review.
---

Use the AbsolutForge `review` skill.

Arguments: the Feature Brief path, then the review artifact path.

Supplied arguments: $ARGUMENTS

Read the `review` skill and follow its contract exactly, including every precondition, artifact schema, and safety boundary it links. If a required argument is missing, ask for it instead of guessing.

Use one fresh read-only subagent when available; otherwise label the result `advisory (not fully isolated)`.
