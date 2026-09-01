# AbsolutForge Skills

Core delivery:

```text
discuss -> (build | build-planned) -> review -> ship
```

Optional: `consult`, `save`, `load`, `debug`, `tech-debt`.

`build` and `build-planned` consume the same committed Ready Feature Brief and converge on the same Review/Ship contract. Prefer autonomous `build`; use `build-planned` when durable decomposition, meaningful bounded delegation, fresh-context rotation, or cross-session resume justifies its overhead. Invocation selects a durable strategy for that feature.

In planned Build, every completed-task checkpoint must be sufficient for a fresh orchestrator to resume from the Brief, plan and Git without prior conversation. `save/load` is mainly for interruption before such a durable boundary.

Both builders are bound by the risk-based Test Charter in [`../references/verification-doctrine.md`](../references/verification-doctrine.md). Applicable risks become named test obligations inside the outcome or task; test count follows risks, not task count. `review` judges coverage of those obligations.

`consult` is optional evidence, not workflow state. It appends an immutable report for a Brief or implementation plan and never edits the subject, pauses Build, or tracks disposition. The owning context records any accepted change in its own artifact.
