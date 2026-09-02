# AbsolutForge Skills

Core delivery:

```text
discuss -> (build | build-planned | build-planned-tdd*) -> review -> ship
```

`*` `build-planned-tdd` is an experimental methodology of the planned strategy, not a third first-class strategy.

Optional: `consult`, `save`, `load`, `debug`, `tech-debt`.

`build` and planned Build consume the same committed Ready Feature Brief and converge on the same Review/Ship contract. Prefer autonomous `build`; use `build-planned` when durable decomposition, meaningful bounded delegation, fresh-context rotation, or cross-session resume justifies its overhead. Experimental `build-planned-tdd` selects the same planned strategy with strict RED-GREEN-REFACTOR task execution. Invocation selects durable strategy and methodology state for that feature.

In planned Build, every completed-task checkpoint must be sufficient for a fresh orchestrator to resume from the Brief, plan and Git without prior conversation. `save/load` is mainly for interruption before such a durable boundary.

All builders are bound by the risk-based Test Charter in [`../references/verification-doctrine.md`](../references/verification-doctrine.md). Applicable risks become named test obligations inside the outcome or task; test count follows risks, not task count. TDD adds chronology through [`../references/planned-tdd-contract.md`](../references/planned-tdd-contract.md), without replacing the charter. `review` judges coverage and test value.

`consult` is optional evidence, not workflow state. It appends an immutable report for a Brief or implementation plan and never edits the subject, pauses Build, or tracks disposition. The owning context records any accepted change in its own artifact.
