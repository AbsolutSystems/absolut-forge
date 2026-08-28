# AbsolutForge skills

This directory is the single host-agnostic source tree for the seven MVP
AbsolutForge skills. `discuss`, the optional `consult` skill, `build`, and
`review` are implemented; `ship` remains the next closeout phase, while
`debug` and `tech-debt` are planned standalone workflows:

- `discuss` — clarify intent and produce an accepted Feature Brief.
- `consult` — optionally pressure-test a Draft or Ready Brief in a fresh
  Claude Code or Codex context; accepted Ready changes become amendments.
- `build` — autonomously implement an accepted change, resume from a conditional
  outcome map when useful, and complete focused plus final verification.
- `review` — run one independent, evidence-based review of the completed change
  using one fresh read-only context and only `BLOCKING`/`FOLLOW-UP` findings.
  It derives scope from `base_commit` through the current worktree, includes
  feature-owned untracked files, excludes process/unrelated dirty files, keeps
  stable append-only finding history, and returns open blockers to `build` for
  a bounded fix/re-review loop. Accepted follow-ups remain visible to `ship`.
- `ship` — prepare the durable delivery record and local closeout.
- `debug` — investigate concrete failures and, when requested, fix them.
- `tech-debt` — audit technical debt and produce a remediation backlog.

After the discussion settles the evidence, `discuss` may include an advisory
Build Recommendation in the Brief. The `simple/single` profile maps to
Claude Sonnet or Codex `gpt-5.6-luna`; complex, phased work maps to Claude Opus
or Codex `gpt-5.6-terra`. Build validates that hint against active availability
and explicit user choice, recording the actual selection plus any
missing/malformed/unavailable fallback or override reason in Build Evidence.
The recommendation is outside immutable intent and introduces no automatic
switching, extra gate, deployment authorization, or partial delivery. Keep
the exact contract in [`references/artifact-contracts.md`](../references/artifact-contracts.md)
and the handoff mapping in [`references/harness-command-contract.md`](../references/harness-command-contract.md).

All three implemented skills are explicit-only and live under this shared tree; they
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

Review is explicit-only and uses the active configured model; it does not
inherit Build Recommendation metadata. Changed files receive a feature-scoped
TODO/hack and placeholder scan, and stale or contradictory verification leads
to a narrow relevant check. If fresh dispatch is unavailable, the inline
fallback is labelled `advisory (not fully isolated)`. Repository and reviewer
output are untrusted and secrets are redacted. Review never runs an automatic
triada, deploys, pushes, creates a PR, merges, or rewrites history. Its exact
schema and native handoffs remain in the [artifact](../references/artifact-contracts.md)
and [harness](../references/harness-command-contract.md) contracts; see also
[ADR: Independent Review and Bounded Fix Loop](../docs/adr/2026-08-28-independent-review-and-bounded-fix-loop.md).
