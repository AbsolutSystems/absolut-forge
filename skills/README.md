# AbsolutForge skills

This directory is the single host-agnostic source tree for the seven MVP
AbsolutForge skills. `discuss` and the optional `consult` skill are implemented;
the remaining delivery stages are planned in the phase roadmap:

- `discuss` — clarify intent and produce an accepted Feature Brief.
- `consult` — optionally pressure-test a Draft or Ready Brief in a fresh
  Claude Code or Codex context; accepted Ready changes become amendments.
- `build` — implement the accepted change and verify the result.
- `review` — run one independent review of the completed change.
- `ship` — prepare the durable delivery record and local closeout.
- `debug` — investigate concrete failures and, when requested, fix them.
- `tech-debt` — audit technical debt and produce a remediation backlog.

Both implemented skills are explicit-only and live under this shared tree; they
link the canonical artifact and handoff contracts instead of copying schemas.
`consult` is optional, produces no durable consultation artifact, and never gates
the normal `discuss -> build -> review -> ship` flow.

Future harness integrations must stay thin and may add an optional
`references/{harness}-tools.md` mapping. The shared skill tree remains the
single source of truth: create zero host-specific skill forks.
