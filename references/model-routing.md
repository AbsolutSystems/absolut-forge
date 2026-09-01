# Model Routing Contract

Model names are deployment guidance, not workflow semantics. Core skills route by capability tier.

| Role | Tier | Priority |
| --- | --- | --- |
| Discuss / Brief | high | intent fidelity, repository comprehension, product/architecture judgment |
| Autonomous Build | high | whole-feature ownership, implementation, verification |
| Planned Build orchestrator | high | decomposition, dependency analysis, worker supervision, integration |
| Planned task worker | low / standard / high | bounded execution according to task complexity |
| Diagnostic advisor | high | root-cause reasoning from a small evidence package |
| Review | high, preferably independent | fresh failure modes and intent fidelity |

## Practical mappings

These examples are non-binding and may be updated without changing workflow contracts.

- OpenAI/Codex: high -> Sol high; standard -> Terra medium; low -> Luna high.
- Claude: high -> Opus; standard -> Sonnet; low -> the cheapest reliable coding worker available in the active plan.

Prefer a different model family for Review when practical, because correlated implementation/review failures are less useful than independent failure modes.

## Planned task routing

Prefer autonomous `build` unless the expected delegation or durable decomposition benefit exceeds the cost of compiling and maintaining a task graph.

Start from the task's declared capability.

- `low`: mechanical/local change, narrow surface, explicit contract and focused verification.
- `standard`: ordinary multi-file coordination with local design choices.
- `high`: shared architecture, migrations, security/data boundaries, concurrency/state complexity, or material ambiguity.

A low/standard worker must not compensate for an invalid plan by broad redesign. It returns a deviation to the high-capability orchestrator. A high task may be executed directly by the orchestrator instead of delegated.
