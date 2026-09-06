# AbsolutForge Skills

Core delivery:

```text
discuss -> build -> review -> ship
```

Optional: `consult`, `save`, `load`, `debug`, `tech-debt`.

`build` consumes the committed Ready Brief and selects autonomous or planned execution once. Autonomous is the default; planned needs concrete benefits from dependencies, bounded delegation or durable resume that repay its overhead. Optional `--strategy=autonomous` or `--strategy=planned` overrides this choice before Build start. The choice and reason are checkpointed without another confirmation. Resumes use recorded strategy and methodology; a conflicting override is refused. New planned work uses standard methodology; legacy delegated work keeps its fixed executor and cannot be converted or taken over by the orchestrator.

On Codex, the invoking context launches a fresh GPT-5.6 Sol `medium` Build owner before repository inspection. Clean implementation/test checkpoints return a compact `ROTATE` envelope so the launcher can replace it with a fresh sibling owner; the launcher never reads or judges Build state. Bounded low/standard outcomes and local corrections default to fresh Luna workers. See [`../references/codex-tools.md`](../references/codex-tools.md).

In planned Build, every completed-task checkpoint must be sufficient for a fresh orchestrator to resume from the Brief, plan and Git without prior conversation. `save/load` is mainly for interruption before such a durable boundary.

All builders are bound by the risk-based Test Charter in [`../references/verification-doctrine.md`](../references/verification-doctrine.md). Applicable risks become named test obligations inside the outcome or task; test count follows risks, not task count. Legacy delegated execution retains its fixed-worker ownership through [`../references/planned-delegated-contract.md`](../references/planned-delegated-contract.md). `review` judges coverage and test value.

`consult` is optional evidence, not workflow state. It appends an immutable report for a Brief or implementation plan and never edits the subject, pauses Build, or tracks disposition. The owning context records any accepted change in its own artifact.
