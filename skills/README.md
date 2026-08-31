# AbsolutForge Skills

Core delivery:

```text
discuss -> (build | build-planned) -> review -> ship
```

Optional: `consult`, `save`, `load`, `debug`, `tech-debt`.

`build` and `build-planned` are peers, not versions of each other. They consume the same committed Ready Feature Brief and converge on the same Review/Ship contract. The explicit builder invocation selects the strategy for that feature and Build start evidence makes the choice durable.

Both builders are bound by [`../references/verification-doctrine.md`](../references/verification-doctrine.md), which defines focused and final verification: changed behavior lands with tests inside the outcome or task that changed it, or with a recorded exemption. `review` judges test value against the same doctrine.

`consult` has two subjects. Brief mode critiques product intent in a `Draft` or `Ready` Brief. Plan mode critiques a planned `implementation-plan.md` whose pending frontier has not executed. It is the one stage designed to run in a separate session and preferably a different model family, and it writes one `consult-{slug}.md` report the requesting context reads back — never the plan, the map or any status.
