---
name: load
description: "Explicitly validate a saved Build context against the current repository and hand the feature back to the same selected Build strategy."
---

# Load

Accept only `absolutforge/features/{slug}/save-{slug}.md`. Validate matching Feature Brief, branch, base revision, Build strategy, planned methodology, execution artifact and current repository state. A save is context evidence, not proof that source exists or verification passed.

If valid, return exactly one next handoff matching the recorded state: `build` for autonomous or `build-planned` for planned standard and legacy delegated state. A legacy planned save without methodology means `standard`. Before delegated resume, `build-planned` loads its fixed-executor restrictions; never convert methodology. Legacy `tdd` state has no current matching builder; direct it to a compatible older release or explicit abandonment and restart rather than converting it. The planned builder rehydrates from the Brief, plan header plus Active Frontier, current task, Git, and relevant code/tests; read direct-dependency evidence only when its facts are insufficient. It reconstructs and persists a missing or stale frontier canonically while preserving completed definitions and evidence. Never switch strategy or methodology, overwrite source, restore files, commit, stash or change branches.
