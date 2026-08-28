# AbsolutForge skills

This directory is the single host-agnostic source tree for the nine implemented
MVP AbsolutForge skills:

- `discuss` — clarify intent and produce an accepted Feature Brief.
- `consult` — optionally pressure-test a Draft or Ready Brief in a fresh
  Claude Code or Codex context; accepted Ready changes become amendments.
- `build` — autonomously implement an accepted change, resume from a conditional
  outcome map when useful, and complete focused plus final verification.
- `save` — capture concise, durable Build context before pausing work or
  switching branches; it never preserves source changes by itself.
- `load` — validate a Build Save against the current branch, then hand the
  restored context back to `build`.
- `review` — run one independent, evidence-based review of the completed change
  using one fresh read-only context and only `BLOCKING`/`FOLLOW-UP` findings.
  It derives exactly the committed `base_commit..HEAD` range, rejects uncommitted
  source changes, keeps stable append-only finding history, and returns open
  blockers to `build` for a bounded fix/re-review loop. Accepted follow-ups
  remain visible to `ship`.
- `ship` — explicitly close a final Review into a Feature Record and
  self-contained Executive Summary HTML, then make one approved local commit.
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

All nine skills live under this shared tree and link the canonical artifact and
handoff contracts instead of copying schemas. Core skills, `consult`, and
`save`, `load`, and `tech-debt` are explicit-only. Only `debug` may auto-trigger, and only for a
concrete failure; auto-triggering authorizes diagnosis rather than a source
change. `consult` is optional, produces no durable consultation artifact, and
never gates the normal `discuss -> build -> review -> ship` flow.

Build uses a Failure Boundary Check before a second speculative repair, escalates
material scope changes for an amendment, and applies a narrow scout rule. It may
request a bounded redacted read-only Sol diagnosis, but never deploys, pushes,
creates PRs, merges, rewrites history, or treats a map section as independently
shippable. Public and critical internal documentation remains concise and
truthful; stale or misleading docs are corrected or removed.

While a Brief is `Building`, `save` writes
`absolutforge/features/{slug}/save-{slug}.md` with actual progress, the next
action, and open items. The developer commits that file with WIP source (or
stashes both) before a branch switch. `load` validates the matching branch and
base revision, reads the current repository state, and hands back to `build`; it
does not restore source or write changes.

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

Ship runs only after a complete final Review with a recorded reviewed branch
revision. If code changes after Review, commit it and invoke Review again before
Ship. Invoke it as
`/absolutforge:ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md`
in Claude Code or
`$absolutforge ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md`
in Codex. It presents one explicit approval preview, routes each memory
candidate independently, archives the Feature Record and path-only Executive
Summary, cleans approved active artifacts, and creates one approved local commit.
It does not push, create a PR, merge, deploy, or rewrite history. The canonical
Ship schema remains in
[`references/artifact-contracts.md`](../references/artifact-contracts.md) and
the commands in
[`references/harness-command-contract.md`](../references/harness-command-contract.md).
