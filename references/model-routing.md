# Model Routing Contract

Provider and model names are host deployment mechanics, not shared workflow or artifact semantics. Standard workflows route by capability tier; legacy delegated methodology binds one executor profile in each active host mapping. New plans cannot select delegated methodology.

| Role | Tier | Priority |
| --- | --- | --- |
| Discuss / Brief | high | intent fidelity, repository comprehension, product/architecture judgment |
| Autonomous Build | high | whole-feature ownership, implementation, verification |
| Planned Build orchestrator | high | decomposition, dependency analysis, worker supervision, integration |
| Planned task worker | low / standard / high | bounded execution according to task complexity |
| Delegated planned executor | fixed host mapping | all production/test edits from a senior-authored bounded plan |
| Diagnostic advisor | high | root-cause reasoning from a small evidence package |
| Review | high, preferably independent | fresh failure modes and intent fidelity |

## Practical mappings

Model and reasoning profiles belong exclusively to the active host mapping. Read only that mapping, including its fixed executor profile when resuming legacy delegated state.

Prefer a different model family for Review when practical, because correlated implementation/review failures are less useful than independent failure modes.

## Planned task routing

Prefer autonomous `build` unless the expected delegation or durable decomposition benefit exceeds the cost of compiling and maintaining a task graph.

Use the lowest capability tier that can safely execute the task. Start from its declared capability and bias decomposition toward safe low/standard work without hiding complexity. Evidence of underestimated complexity requires a PC revision escalating the pending task or decomposing it; never force a task downward.

- `low`: mechanical/local change, narrow surface, explicit contract and a fast task gate.
- `standard`: ordinary multi-file coordination with local design choices.
- `high`: shared architecture, migrations, security/data boundaries, concurrency/state complexity, or material ambiguity.

A low/standard worker must not compensate for an invalid plan by broad redesign. It returns a deviation to the high-capability orchestrator. A high task may be executed directly by the orchestrator instead of delegated.

## Delegated methodology routing

Legacy delegated resume via `build-planned` does not route per task. Its high-capability orchestrator resolves architecture and writes every task for the single executor profile fixed by the active host mapping. The plan must not contain a `high` implementation task: decompose it, settle its design in the plan, or stop because the methodology is unsuitable.

Model substitution changes the selected methodology's cost and capability premise. If the fixed executor or required reasoning effort is unavailable, stop at the last clean boundary instead of falling back to a different worker or implementing in the orchestrator context. Durable artifacts record the methodology and material escalation, never provider or model identity.
