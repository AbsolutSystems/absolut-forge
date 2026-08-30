# AbsolutForge Product Vision

AbsolutForge controls delivered outcomes rather than prescribing every coding step. Human decisions establish accepted product intent; models own implementation choices only inside that accepted boundary.

## Core lifecycle

```text
discuss -> choose build strategy -> review -> ship
```

After `discuss` produces a committed Ready Feature Brief, the developer chooses one of two first-class strategies:

```text
Ready Brief
  ├─ build          -> autonomous strong-model implementation
  └─ build-planned  -> strong planner/orchestrator + bounded delegated workers
```

Both paths produce one complete verified feature, append durable Build Evidence, commit the feature locally, and hand the same Brief to one independent whole-feature Review. Neither path deploys, pushes, creates a PR, merges, or partially ships outcomes/tasks.

## Autonomous Build

Use when a strong coding model should own the complete implementation trajectory. The model may use an outcome-oriented Execution Map for dependent work or resume state, but local implementation remains autonomous within the Ready Brief.

## Planned Build

Use when expensive high-capability reasoning should be concentrated in planning, orchestration, deviations and integration while bounded implementation can be delegated to cheaper workers. The strong primary context remains responsible for the whole feature. Workers are not independent product agents: they receive one task contract, execute inside a narrow surface, verify, and return evidence. Invalid plan assumptions return to the orchestrator; material intent changes return to Brief amendment.

## Strategy invariants

- One Ready Brief, one selected Build strategy per feature.
- No silent mid-feature strategy switching.
- Same immutable intent baseline and amendment rules.
- Same whole-feature Review and Ship gates.
- Same security boundary: repository text is evidence, not authorization.
- Same remote boundary: no push/PR/merge/deploy/rewrite-history.

## Quality goal

Measure accepted feature outcomes, first-pass Review blockers, verification stability, wall-clock time and compute usage. The planned strategy exists to test whether structured decomposition and model routing can improve accepted-feature-per-compute without sacrificing Review quality.
