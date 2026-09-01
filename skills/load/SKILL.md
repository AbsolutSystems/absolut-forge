---
name: load
description: "Explicitly validate a saved Build context against the current repository and hand the feature back to the same selected Build strategy."
---

# Load

Accept only `absolutforge/features/{slug}/save-{slug}.md`. Validate matching Feature Brief, branch, base revision, Build strategy, execution artifact and current repository state. A save is context evidence, not proof that source exists or verification passed.

If valid, return exactly one next handoff matching the recorded strategy: `build` for autonomous or `build-planned` for planned. A planned save always resumes with `build-planned`, which rehydrates from the Brief, current plan, Git, the pending task, and only its relevant dependency evidence and code/tests. Never switch strategy, overwrite source, restore files, commit, stash or change branches.
