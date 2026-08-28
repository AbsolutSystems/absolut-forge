# AbsolutForge skills

This directory is the single host-agnostic source tree for the seven MVP
AbsolutForge skills. `discuss`, the optional `consult` skill, and `build` are
implemented; the remaining delivery stages are planned in the phase roadmap:

- `discuss` — clarify intent and produce an accepted Feature Brief.
- `consult` — optionally pressure-test a Draft or Ready Brief in a fresh
  Claude Code or Codex context; accepted Ready changes become amendments.
- `build` — autonomously implement an accepted change, resume from a conditional
  outcome map when useful, and complete focused plus final verification.
- `review` — run one independent review of the completed change.
- `ship` — prepare the durable delivery record and local closeout.
- `debug` — investigate concrete failures and, when requested, fix them.
- `tech-debt` — audit technical debt and produce a remediation backlog.

Both implemented skills are explicit-only and live under this shared tree; they
link the canonical artifact and handoff contracts instead of copying schemas.
`consult` is optional, produces no durable consultation artifact, and never gates
the normal `discuss -> build -> review -> ship` flow.

Build uses a Failure Boundary Check before a second speculative repair, escalates
material scope changes for an amendment, and applies a narrow scout rule. It may
request a bounded redacted read-only Sol diagnosis, but never deploys, pushes,
creates PRs, merges, rewrites history, or treats a map section as independently
shippable. Public and critical internal documentation remains concise and
truthful; stale or misleading docs are corrected or removed.

The exact Execution Map, Build Evidence, lifecycle, status, resume, and
secret-redaction rules remain in the [canonical artifact contract](../references/artifact-contracts.md);
see also [ADR-004](../docs/adr/2026-08-28-outcome-oriented-build-and-checkpoints.md)
and [ADR-005](../docs/adr/2026-08-28-single-delivery-unit-no-partial-deployment.md).

Future harness integrations must stay thin and may add an optional
`references/{harness}-tools.md` mapping. The shared skill tree remains the
single source of truth: create zero host-specific skill forks.
