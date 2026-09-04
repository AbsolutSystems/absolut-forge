# AbsolutForge Skills

Core delivery:

```text
discuss -> (build | build-planned | build-planned-delegated*) -> review -> ship
```

`*` `build-planned-delegated` is a fixed-executor methodology of the planned strategy, not a third first-class strategy.

Optional: `consult`, `save`, `load`, `debug`, `tech-debt`.

`build` and planned Build consume the same committed Ready Feature Brief and converge on the same Review/Ship contract. Prefer autonomous `build`; use `build-planned` when durable decomposition, flexible capability routing, fresh-context rotation, or cross-session resume justifies its overhead. `build-planned-delegated` selects the same planned strategy but requires a high-capability orchestrator to compile every task for one fixed host-mapped executor, which owns all source and test edits. Invocation selects durable strategy and methodology state for that feature.

In planned Build, every completed-task checkpoint must be sufficient for a fresh orchestrator to resume from the Brief, plan and Git without prior conversation. `save/load` is mainly for interruption before such a durable boundary.

All builders are bound by the risk-based Test Charter in [`../references/verification-doctrine.md`](../references/verification-doctrine.md). Applicable risks become named test obligations inside the outcome or task; test count follows risks, not task count. Delegated execution adds its fixed-worker ownership and planner-to-executor contract through [`../references/planned-delegated-contract.md`](../references/planned-delegated-contract.md). `review` judges coverage and test value.

`consult` is optional evidence, not workflow state. It appends an immutable report for a Brief or implementation plan and never edits the subject, pauses Build, or tracks disposition. The owning context records any accepted change in its own artifact.
