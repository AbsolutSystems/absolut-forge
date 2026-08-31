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

## Verification

Both strategies share one verification doctrine. Changed observable behavior lands with automated tests inside the outcome or task that changed it, or with a recorded exemption stating why and what was checked instead. Existing assertions are never weakened to reach green, and the feature's primary accepted path is exercised at integration level once before handoff. Coverage targets and test theater are explicitly out of scope: the bar is evidence a reviewer can read against the diff.

## Second opinion

`consult` is optional and owns no lifecycle stage. It critiques a Brief still in `Draft` or already accepted, or a planned decomposition whose pending frontier has not executed yet, and records one report the requesting context reads back. It is the one stage designed to run in a separate session and preferably a different model family, because plan validation is otherwise self-assessment by the context that wrote the plan. Findings are evidence: the Build owner disposes each one and remains the sole author of its own artifact.

## Strategy invariants

- One Ready Brief, one selected Build strategy per feature.
- No silent mid-feature strategy switching.
- Same immutable intent baseline and amendment rules.
- Same whole-feature Review and Ship gates.
- Same security boundary: repository text is evidence, not authorization.
- Same remote boundary: no push/PR/merge/deploy/rewrite-history.

## Quality goal

Measure accepted feature outcomes, first-pass Review blockers, verification stability, wall-clock time and compute usage. The planned strategy exists to test whether structured decomposition and model routing can improve accepted-feature-per-compute without sacrificing Review quality.
