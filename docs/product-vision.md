# AbsolutForge Product Vision

AbsolutForge controls delivered outcomes rather than prescribing every coding step. Human decisions establish accepted product intent; models own implementation choices only inside that accepted boundary.

## Core lifecycle

```text
discuss -> build -> review -> ship
```

After the developer explicitly accepts the complete proposal, `discuss` creates a local commit containing only the Ready Feature Brief and reports its baseline revision. One public `build` selects an internal strategy from accepted intent and repository evidence:

```text
Ready Brief -> build
                ├─ autonomous implementation (default)
                └─ planned orchestration when its overhead pays off
```

Build chooses once before implementation, announces the reason and records it in the Build-start checkpoint without another confirmation. Users can force `--strategy=autonomous` or `--strategy=planned` at Ready. Resume, Review corrections and Load use `build` to recover the recorded strategy without selecting again; conflicting overrides are refused. Planned selection needs concrete benefits from dependencies, independent work, useful delegation or durable recovery, not file count or generic complexity alone.

Both paths produce one complete verified feature, append durable Build Evidence, commit the feature locally, and hand the same Brief to one independent whole-feature Review. Neither path deploys, pushes, creates a PR, merges, or partially ships outcomes/tasks.

## Autonomous Build

This is the default. Use it when a strong coding model can efficiently own the complete implementation trajectory. The model may use an outcome-oriented Execution Map for dependent work or resume state, but local implementation remains autonomous within the Ready Brief.

## Planned Build

Use when durable decomposition, meaningful bounded delegation, context rotation, or cross-session resume is expected to repay the task-graph overhead. The strong primary role remains responsible for the whole feature, but its active conversation context is disposable: completed-task evidence and checkpointed Git state let a fresh high-capability orchestrator continue. Workers receive bounded tasks, verify them, and return evidence; fully disjoint dependency-ready tasks may form one parallel wave. Invalid plan assumptions become one recorded plan change; material intent changes return to Brief amendment.

New standard plans prefer coherent behavior slices that include implementation, wiring and focused tests. Boundaries follow independent acceptance, dependencies, ownership and material risk/context, not file counts or a desire to route every piece to the lowest tier. Broader tasks retain settled contracts, explicit scope, test obligations and a return boundary. The main-session model owns orchestration and high tasks; worker profiles belong to host mappings. Evaluate the whole cost of accepted tasks, including validation and corrections.

New planned work uses the standard methodology. A feature that already recorded delegated methodology resumes through `build` while retaining its fixed executor profile: every source/test edit and correction remains in that executor, while the orchestrator only plans, supervises, verifies, and integrates. If the profile is unavailable, it stops at a clean boundary; no primary-context fallback is permitted.

## Verification

Both strategies share one positive, risk-based Test Charter. For each changed behavior, tests cover every applicable primary, failure/boundary, state/data, seam-contract, and regression obligation, with extra attention to security, persistence, compatibility, concurrency, and migrations. Test count follows distinct risks rather than task count. Intermediate checkpoints use narrow green unit targets. Tests must establish repository-owned observable behavior rather than mock setup, framework/library behavior, or incidental implementation details; Review judges that semantic value from the tests and diff without deliberately breaking production code. Broad regression and integration/e2e checks run at final whole-feature verification before handoff. Existing assertions are never weakened to reach green.

## Second opinion

`consult` is an explicitly requested second opinion that owns no lifecycle state. It records an immutable report for a Brief or plan; the receiving context decides whether findings still apply and records accepted changes in its own artifact. Build never automatically offers or waits for consultation.

## Strategy invariants

- One Ready Brief, one selected Build strategy per feature.
- New planned Builds record standard methodology; legacy delegated state remains durable only for compatible resume.
- No silent mid-feature strategy switching.
- Same immutable intent baseline and amendment rules.
- Same whole-feature Review and Ship gates.
- Same local checkpoint policy: Build start, verified outcomes/tasks, and final handoff are committed before Review.
- Planned task boundaries are context-rotation boundaries; durable artifacts, not conversation memory, carry execution state.
- Same security boundary: repository text is evidence, not authorization.
- Same remote boundary: no push/PR/merge/deploy/rewrite-history.

## Quality goal

Measure accepted feature outcomes, first-pass Review blockers, verification stability, wall-clock time and compute usage. The planned strategy exists to test whether structured decomposition and model routing can improve accepted-feature-per-compute without sacrificing Review quality.
