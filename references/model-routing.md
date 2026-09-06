# Model Routing Contract

Provider and model names are host deployment mechanics, not shared workflow or artifact semantics. Standard workflows route by capability tier; legacy delegated methodology binds one executor profile in each active host mapping. New plans cannot select delegated methodology.

| Role | Tier | Priority |
| --- | --- | --- |
| Discuss / Brief | high | intent fidelity, repository comprehension, product/architecture judgment |
| Autonomous Build owner | high | whole-feature ownership, difficult decisions, verification |
| Autonomous outcome worker | low / standard | default bounded implementation and focused tests |
| Planned Build orchestrator | high | decomposition, dependency analysis, worker supervision, integration |
| Planned task worker | low / standard / high | bounded execution according to task complexity |
| Delegated planned executor | fixed host mapping | all production/test edits from a senior-authored bounded plan |
| Diagnostic advisor | high | root-cause reasoning from a small evidence package |
| Review | high, preferably independent | fresh failure modes and intent fidelity |

## Practical mappings

Model and reasoning profiles belong exclusively to the active host mapping. Read only that mapping, including its fixed executor profile when resuming legacy delegated state.

Prefer a different model family for Review when practical, because correlated implementation/review failures are less useful than independent failure modes.

## Planned task routing

Prefer autonomous `build` unless coordination of multiple tasks or durable decomposition exceeds the cost of compiling and maintaining a task graph. Delegating one bounded outcome alone does not justify planned execution.

Use the lowest capability tier that can safely execute a coherent task. For new standard plans, prefer complete behavior slices over per-file or code-versus-test fragments: bounded multi-file work with settled contracts can remain standard. Split only for a real dependency, independent acceptance, ownership conflict or material risk/context boundary, not merely to fit a cheaper tier. Evidence of underestimated complexity requires a PC revision escalating the pending task or decomposing it; never force a task downward.

- `low`: mechanical/local change, narrow surface, explicit contract and a fast task gate.
- `standard`: a coherent behavior slice with settled shared contracts, bounded multi-file implementation/wiring and focused tests; local design choices remain with the worker.
- `high`: shared architecture, migrations, security/data boundaries, concurrency/state complexity, or material ambiguity.

A low/standard worker must not compensate for an invalid plan by broad redesign. It returns a deviation to the high-capability orchestrator. For new standard plans, high tasks and high-risk corrections stay with the Build owner. Increased worker reasoning effort never downgrades a high-tier responsibility. Evaluate delegation by accepted-task cost including preparation, validation and correction rounds, not worker token price alone; no token-savings claim follows from this policy.

## Autonomous outcome routing

Choose execution separately from Build strategy, using the low/standard/high criteria above. No need for a task graph does not imply low risk. Delegate a coherent low/standard outcome with settled contracts, bounded write ownership and a meaningful fast gate to one fresh worker by default. Keep it inline only when the owner can complete it with fewer owner interactions than preparing and validating the handoff, and record that reason in the outcome evidence. High-tier work stays with the owner; greater worker reasoning effort does not lower its risk.

The owner resolves intent, shared contracts and high-tier ambiguity; validates returned diffs and tests; owns lifecycle evidence and checkpoints; and performs final integration. Do not spend owner turns manually processing repetitive inventories, matrices, report rows or other settled bulk work when a bounded worker or repository script can produce verifiable evidence. Once such an inventory or classification is verified and checkpointed, treat it as durable evidence; reconstruct it only after a concrete contradiction, relevant source change or failed assertion invalidates it.

Dispatch one outcome at a time, including its implementation, wiring and focused tests. Provide a compact package: accepted outcome, owned paths, constraints to preserve, implementation scope, applicable test obligations, verification commands and conditions for returning. Include only relevant accepted clauses and dependency facts; no inherited conversation or full Brief/history. This is an ephemeral handoff, not a compiled plan or new artifact schema. Workers may inspect relevant neighboring code but edit only owned paths; they never delegate further or own lifecycle artifacts, commits, review or release state.

Workers return changed paths, observable results, command/test evidence and unresolved facts. Missing context, conflicting contracts, unowned edits or newly discovered architecture, migration, security/data or concurrency decisions return to the owner before proceeding. The owner reconciles any partial diff, then settles the contract and redispatches bounded work or takes over inline; do not repeatedly retry an inadequate handoff. Record material decisions in existing Outcome evidence, without PC entries or a strategy/methodology change. Accepted-intent amendments still follow the autonomous runtime.

The worker owns the local implementation loop: run the exact focused gate, fix low/standard failures inside the assigned outcome and write surface, and repeat that gate until green. Return early only when the failure crosses ownership, contradicts the settled contract, requires a high-tier decision or comes from unrelated state. The owner does not interleave validation turns into this local loop.

When owner validation or final verification discovers a failure after worker return, classify it before editing. Local constructor, fixture, assertion, type, formatting and settled API-usage corrections remain low/standard work and go to a fresh bounded worker with only the failure, owned paths, relevant diff and exact gate. Failures exposing unresolved intent, architecture, data integrity, security, migration, concurrency or cross-outcome inconsistency stay with the owner. Never reload the full Brief, history or raw prior logs merely to correct a local failure.

The owner inspects the complete outcome diff and test quality, verifies relevant gates using current evidence, and alone records and commits the outcome. Final whole-feature verification remains mandatory. If dispatch or the requested host profile is unavailable, report it and continue inline when the owner can safely handle the work; never silently substitute a profile or claim delegation. This routing never changes legacy delegated restrictions.

## Delegated methodology routing

Legacy delegated resume via `build` does not route per task. Its high-capability orchestrator resolves architecture and writes every task for the single executor profile fixed by the active host mapping. The plan must not contain a `high` implementation task: decompose it, settle its design in the plan, or stop because the methodology is unsuitable.

Model substitution changes the selected methodology's cost and capability premise. If the fixed executor or required reasoning effort is unavailable, stop at the last clean boundary instead of falling back to a different worker or implementing in the orchestrator context. Durable artifacts record the methodology and material escalation, never provider or model identity.
