# Model Routing Contract

Provider and model names are host deployment mechanics, not shared workflow or artifact semantics. Standard workflows separate operational ownership and high-capability decision support from bounded execution: the Build owner resolves intent, decisions and risk controls using the active host's required advice, while fresh workers own every production-code and test edit. Capability tier always changes preparation and validation intensity and may select a different worker profile when the active host mapping differentiates tiers; it never changes that ownership boundary. Legacy delegated methodology still binds one fixed executor profile in each active host mapping; new plans cannot select delegated methodology.

| Role | Tier | Priority |
| --- | --- | --- |
| Discuss / Brief | high | intent fidelity, repository comprehension, product/architecture judgment |
| Autonomous Build owner | host-mapped owner with high-capability decision support | whole-feature ownership, difficult decisions, verification |
| Autonomous outcome worker | low / standard / high | all bounded implementation and focused tests after owner compilation |
| Planned Build orchestrator | host-mapped owner with high-capability decision support | decomposition, dependency analysis, worker supervision, integration |
| Planned task worker | low / standard / high | all bounded implementation according to execution risk |
| Delegated planned executor | fixed host mapping | all production/test edits from a senior-authored bounded plan |
| Decision / diagnostic advisor | high | bounded planning, risk analysis and root-cause reasoning from primary evidence |
| Review | high, preferably independent | fresh failure modes and intent fidelity |

## Practical mappings

Model and reasoning profiles belong exclusively to the active host mapping. Read only that mapping, including its fixed executor profile when resuming legacy delegated state.

Prefer a different model family for Review when practical, because correlated implementation/review failures are less useful than independent failure modes.

## Decision advice

A host may retain a high-capability owner or map operational ownership to a lower-cost profile with mandatory high-capability advice. Use the active host mapping to determine which owners must consult and the exact advisor profile. Advice supplies evidence; the owner retains lifecycle, scope, decision recording and acceptance responsibility.

For owners requiring advice, consult before dependent implementation or acceptance when:

- a decision or claimed guarantee concerns authorization/security, data integrity, migration strategy, public-contract compatibility, concurrency/state transitions, or a large blast radius;
- architecture, cross-task dependencies, conflicting requirements/evidence or material ambiguity remain unresolved;
- two attempts have failed to resolve the same blocker, even if the owner considers the next retry routine.

Assess the behavior being changed or prescribed, not the file extension: an operational runbook for role updates or a migration can trigger advice despite being documentation-only. Planning for settled bounded work, inventories, routine gates, lifecycle updates and commits do not trigger consultation on their own. The owner may also ask one bounded question voluntarily; confidence alone never waives a mandatory trigger.

Consult once per coherent decision, with accepted clauses and primary evidence accessible to the advisor. Preserve the decision, assumptions, affected boundary and proof obligations in existing Outcome evidence or plan/PC records. Reuse that decision across unchanged dependent tasks; reconsult when relevant evidence invalidates an assumption, introduces a new boundary or leaves the required decision unresolved. Historical decisions without sufficient evidence must be checked before dependent work resumes; do not rewrite completed history. After two failed attempts, obtain diagnosis and a changed decision, decomposition or proof plan before another attempt, rather than issuing a substantially identical third capsule.

A short owner summary is navigation, not the advisor's sole evidence. The advisor may inspect relevant source, tests and the diff read-only and must state unresolved facts. Required advice must complete before dependent work proceeds; unavailable advice follows the host's stop rule. Material intent changes still require accepted amendments. This is internal Build decision support, not invocation of the optional public `consult` stage, and never replaces independent Review.

## Planned task routing

Prefer autonomous `build` unless coordination of multiple tasks or durable decomposition exceeds the cost of compiling and maintaining a task graph. Delegating one bounded outcome alone does not justify planned execution.

Use the lowest capability tier that accurately describes the execution risk of a coherent task. For new standard plans, prefer complete behavior slices over per-file or code-versus-test fragments: bounded multi-file work with settled contracts can remain standard. Split only for a real dependency, independent acceptance, ownership conflict or material risk/context boundary, not merely to fit a cheaper tier. Evidence of underestimated complexity requires a PC revision escalating the pending task or decomposing it; never force a task downward.

- `low`: mechanical/local change, narrow surface, explicit contract and a fast task gate.
- `standard`: a coherent behavior slice with settled shared contracts, bounded multi-file implementation/wiring and focused tests; local design choices remain with the worker.
- `high`: execution crosses a migration, security/data boundary, concurrency/state transition, large blast radius or another boundary that needs stronger containment and intermediate proof.

Classify unresolved judgment separately from execution risk. Architecture, migration strategy, security/data policy, concurrency semantics, public contracts and material ambiguity are owner decisions, not implementation tasks. The owner investigates and records those decisions before dispatch. The resulting implementation may still be `high` when executing the settled design crosses a risky boundary; it remains worker-owned and carries explicit assumptions, containment, rollback when applicable, intermediate proof obligations and return conditions. If owner acceptance is required between two implementation phases, split them at that real dependency boundary instead of pausing one task. Do not manufacture decision-only work, prewrite most of the patch in the handoff, or downgrade execution risk after settling the design.

A worker must not compensate for an invalid plan by broad redesign. It returns a deviation to the owner. The owner then repairs the decision or task contract and dispatches a fresh bounded worker; after two failed attempts at the same blocker, it must re-open the underlying decision or decomposition instead of issuing a substantially identical capsule. The Build owner never edits production code or tests under standard methodology. Evaluate execution by accepted-task cost including preparation, validation and correction rounds, not worker token price alone; no token-savings claim follows from this policy.

## Autonomous outcome routing

Choose capability separately from Build strategy, using the execution-risk criteria and decision boundary above. No need for a task graph does not imply low risk. The owner compiles every coherent outcome into a bounded package with settled contracts, write ownership and meaningful gates, then dispatches one fresh worker for all production-code and test edits. A mixed outcome is not wholly `high` merely because the owner must first settle a difficult decision; classify the resulting execution on its own risk. A genuinely high execution remains worker-owned and receives the stronger controls required below.

The owner resolves intent, shared contracts and high-tier ambiguity; validates returned diffs and tests; owns lifecycle evidence and checkpoints; and performs final integration. Do not spend owner turns manually processing repetitive inventories, matrices, report rows or other settled bulk work when a bounded worker or repository script can produce verifiable evidence. Once such an inventory or classification is verified and checkpointed, treat it as durable evidence; reconstruct it only after a concrete contradiction, relevant source change or failed assertion invalidates it.

Dispatch one outcome at a time, including its implementation, wiring and focused tests. Provide a compact package: accepted outcome, owned paths, constraints to preserve, implementation scope, applicable test obligations, verification commands and conditions for returning. For high execution risk also include the settled decision, assumptions, containment, rollback when applicable and intermediate proof obligations. Include only relevant accepted clauses and dependency facts; no inherited conversation or full Brief/history. This is an ephemeral just-in-time compilation, not a planned artifact or new schema. Workers may inspect relevant neighboring code but edit only owned paths; they never delegate further or own lifecycle artifacts, commits, review or release state.

Workers return changed paths, observable results, command/test evidence and unresolved facts. Missing context, conflicting contracts, unowned edits or newly discovered architecture, migration, security/data or concurrency decisions return to the owner before proceeding. The owner reconciles any partial diff, settles the contract and redispatches bounded work; it never takes over production-code or test edits. Do not repeatedly retry an inadequate handoff. Record material decisions in existing Outcome evidence, without PC entries or a strategy/methodology change. Accepted-intent amendments still follow the autonomous runtime.

The worker owns the local implementation loop: run the exact focused gate, fix failures inside the assigned outcome and write surface, and repeat that gate until green. For high execution risk, run and report every intermediate proof obligation before returning. Return early when the failure crosses ownership, contradicts the settled contract, exposes an unresolved owner decision or comes from unrelated state.

When owner validation or final verification discovers a failure after worker return, classify it before dispatch. Local constructor, fixture, assertion, type, formatting and settled API-usage corrections retain their tier and go to a fresh bounded worker with only the failure, owned paths, relevant diff and exact gate. Failures exposing unresolved intent, architecture, data integrity, security, migration, concurrency or cross-outcome inconsistency first return to the owner for a corrected decision and package, then to a fresh worker for any production-code or test edit. Never reload the full Brief, history or raw prior logs merely to correct a local failure.

The owner inspects the complete outcome diff and test quality, verifies relevant gates using current evidence, and alone records and commits the outcome. Final whole-feature verification remains mandatory. If dispatch or the requested host profile is unavailable, report it and stop at the last clean boundary; never substitute a profile, implement inline or claim delegation. Existing partial worker state is reconciled without overwriting it. This routing never changes legacy delegated restrictions.

## Delegated methodology routing

Legacy delegated resume via `build` does not route per task. Its high-capability orchestrator resolves architecture and writes every task for the single executor profile fixed by the active host mapping. The plan must not contain a `high` implementation task: decompose it, settle its design in the plan, or stop because the methodology is unsuitable.

Model substitution changes the selected methodology's cost and capability premise. If the fixed executor or required reasoning effort is unavailable, stop at the last clean boundary instead of falling back to a different worker or implementing in the orchestrator context. Durable artifacts record the methodology and material escalation, never provider or model identity.
