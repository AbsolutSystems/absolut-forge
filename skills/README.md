# AbsolutForge skills

This directory is the single host-agnostic source tree for the six planned
AbsolutForge skills:

- `discuss` — clarify intent and produce an accepted Feature Brief.
- `build` — implement the accepted change and verify the result.
- `review` — run one independent review of the completed change.
- `ship` — prepare the durable delivery record and local closeout.
- `debug` — investigate concrete failures and, when requested, fix them.
- `tech-debt` — audit technical debt and produce a remediation backlog.

Phase 1 reserves this layout only. It intentionally contains no `SKILL.md`
definitions, so no incomplete skill can be discovered or invoked.

Future harness integrations must stay thin and may add an optional
`references/{harness}-tools.md` mapping. The shared skill tree remains the
single source of truth: create zero host-specific skill forks.
