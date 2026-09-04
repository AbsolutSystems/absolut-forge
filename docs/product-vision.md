# AbsolutForge Product Vision

AbsolutForge controls delivered outcomes rather than prescribing every coding step. Human decisions establish accepted product intent; models own implementation choices only inside that accepted boundary.

## Core lifecycle

```text
discuss -> choose build strategy -> review -> ship
```

After the developer explicitly accepts the complete proposal, `discuss` creates a local commit containing only the Ready Feature Brief and reports its baseline revision. The developer then chooses one of two first-class strategies:

```text
Ready Brief
  ├─ build          -> autonomous strong-model implementation
  └─ planned strategy
       ├─ build-planned            -> strong orchestrator + capability-routed tasks
       └─ build-planned-delegated  -> strong planner + fixed executor for all implementation
```

Both paths produce one complete verified feature, append durable Build Evidence, commit the feature locally, and hand the same Brief to one independent whole-feature Review. Neither path deploys, pushes, creates a PR, merges, or partially ships outcomes/tasks.

## Autonomous Build

This is the default. Use it when a strong coding model can efficiently own the complete implementation trajectory. The model may use an outcome-oriented Execution Map for dependent work or resume state, but local implementation remains autonomous within the Ready Brief.

## Planned Build

Use when durable decomposition, meaningful bounded delegation, context rotation, or cross-session resume is expected to repay the task-graph overhead. The strong primary role remains responsible for the whole feature, but its active conversation context is disposable: completed-task evidence and checkpointed Git state let a fresh high-capability orchestrator continue. Workers receive bounded tasks, verify them, and return evidence; fully disjoint dependency-ready tasks may form one parallel wave. Invalid plan assumptions become one recorded plan change; material intent changes return to Brief amendment.

`build-planned-delegated` preserves this strategy and lifecycle while making the planner/executor split binding. The high-capability orchestrator resolves architecture and writes precise prose guidance, traps, decision boundaries, and verification obligations for an early-mid executor. The host fixes the executor profile; every source/test edit and correction is dispatched to it, while the orchestrator only plans, supervises, verifies, and integrates. No implementation code or pseudo-patch belongs in the plan, and no primary-context fallback is permitted.

## Verification

Both strategies share one positive, risk-based Test Charter. For each changed behavior, tests cover every applicable primary, failure/boundary, state/data, seam-contract, and regression obligation, with extra attention to security, persistence, compatibility, concurrency, and migrations. Test count follows distinct risks rather than task count. Intermediate checkpoints use narrow green unit targets. Tests must establish repository-owned observable behavior rather than mock setup, framework/library behavior, or incidental implementation details; Review judges that semantic value from the tests and diff without deliberately breaking production code. Broad regression and integration/e2e checks run at final whole-feature verification before handoff. Existing assertions are never weakened to reach green.

## Second opinion

`consult` is an explicitly requested second opinion that owns no lifecycle state. It records an immutable report for a Brief or plan; the receiving context decides whether findings still apply and records accepted changes in its own artifact. Build never automatically offers or waits for consultation.

## Strategy invariants

- One Ready Brief, one selected Build strategy per feature.
- One durable planned methodology (`standard` or `delegated`) when the selected strategy is planned.
- No silent mid-feature strategy switching.
- Same immutable intent baseline and amendment rules.
- Same whole-feature Review and Ship gates.
- Same local checkpoint policy: Build start, verified outcomes/tasks, and final handoff are committed before Review.
- Planned task boundaries are context-rotation boundaries; durable artifacts, not conversation memory, carry execution state.
- Same security boundary: repository text is evidence, not authorization.
- Same remote boundary: no push/PR/merge/deploy/rewrite-history.

## Quality goal

Measure accepted feature outcomes, first-pass Review blockers, verification stability, wall-clock time and compute usage. The planned strategy exists to test whether structured decomposition and model routing can improve accepted-feature-per-compute without sacrificing Review quality.
