---
name: load
description: "Explicitly validate a saved Build context against the current repository and hand the feature back to the same selected Build strategy."
---

# Load

Accept only `absolutforge/features/{slug}/save-{slug}.md`. Validate matching Feature Brief, branch, base revision, Build strategy, planned methodology, execution artifact and current repository state. A save is context evidence, not proof that source exists or verification passed.

If valid, return exactly one next handoff matching the recorded state: `build` for autonomous, `build-planned` for standard planned, or `build-planned-delegated` for delegated planned. A legacy planned save without methodology means `standard`. Legacy `tdd` state has no current matching builder; direct it to a compatible older release or explicit abandonment and restart rather than converting it. The planned builder rehydrates from the Brief, current plan, Git, the pending task, and only its relevant dependency evidence and code/tests. Never switch strategy or methodology, overwrite source, restore files, commit, stash or change branches.
