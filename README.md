# AbsolutForge

AbsolutForge is an intent-driven development workflow for strong coding models.
It gives the model a precise product goal, durable context, and room to execute
autonomously, while concentrating quality control on verification and one final,
independent review.

> Status: private pilot MVP. The `discuss`, optional `consult`, `build`,
> `review`, and explicit-only `ship` skills are implemented; `debug` and
> `tech-debt` remain separate Phase 6 workflows.

AbsolutForge is a standalone product, not an AbsolutPowers light mode. The
repository is the plugin root and uses one shared `skills/` tree for Claude Code
and Codex, with thin per-harness manifests. Pi and Grok support is deferred.
There is no SessionStart hook, MCP server, app, or globally injected workflow.

## Product thesis

Detailed task decomposition and repeated review gates often consume substantial
context without eliminating defects. Modern frontier models can usually plan
their local implementation work themselves when they receive:

- a clear, accepted intent,
- explicit behavioral boundaries and invariants,
- durable architectural decisions,
- an outcome-oriented execution map when work spans multiple sections,
- a mandatory test-and-fix loop,
- one independent review of the final result.

AbsolutForge controls the result instead of prescribing every implementation
step.

## Core workflow

```text
discuss -> build -> review -> ship
```

- **discuss** creates an accepted Feature Brief and any durable ADRs.
- **consult** is an optional, explicit second-model opinion on an existing Draft
  or Ready Brief; accepted changes merge into a Draft or become Ready amendments.
- **build** implements autonomously, creates an Execution Map only when useful,
  resumes from durable map/evidence status when needed, and runs focused plus
  final verification.
- **review** performs one independent, evidence-based review with one fresh,
  read-only reviewer and only `BLOCKING` or `FOLLOW-UP` findings. It derives
  the complete change from `base_commit` through the current worktree,
  including feature-owned untracked files, while excluding review-process and
  unrelated dirty files. Stable finding IDs and append-only pass history keep
  evidence across targeted re-review; accepted follow-ups remain visible but
  do not block `ship`. An open blocker returns the same Brief to `build` for a
  focused correction, with escalation after two unsuccessful attempts or
  material scope expansion.
- **ship** is the final, explicit-only local closeout after a complete Review. It
  validates the post-review fingerprint, presents one approval preview, creates
  the Feature Record and self-contained Executive Summary HTML, routes each
  memory candidate independently, cleans up active artifacts, and creates one
  local conventional commit plus a PR description. It never pushes, creates a
  PR, merges, deploys, or rewrites history.

Invoke Ship with the native command for the active harness:

```text
/absolutforge:ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
$absolutforge ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
```

Two standalone workflows complement the core:

- **debug** investigates root cause and, when fixing, creates a compact Fix Brief.
- **tech-debt** produces a static, evidence-based remediation backlog.

`discuss` adapts its questions to the readiness frontier: it discovers current
repository facts first, asks a small frontier of normally two to four
independent high-impact questions, and persists a Draft only when it is useful,
requested as a save point, or needed to resume a material blocker. It presents
one complete Brief and uses one acceptance gate before changing `Draft` to
`Ready`; it then emits the native `build` handoff. The durable Brief and
canonical contracts own the exact schema; this README does not reproduce them.

When the evidence is settled, `discuss` may append an advisory Build
Recommendation to the Brief. One cohesive, low-risk result uses the
`simple/single` profile: Claude Sonnet or Codex `gpt-5.6-luna`. Dependent,
uncertain, or boundary-sensitive work uses `complex/phased`: Claude Opus or
Codex `gpt-5.6-terra`. This is guidance, not a hard model gate: build checks
availability and explicit user choice, then records the selected model or any
missing/malformed/unavailable fallback or override reason in Build Evidence.
The recommendation is outside immutable intent, does not switch providers or
models automatically, and never authorizes deployment or partial delivery.
The exact fields and placement are owned by the [Feature Brief contract](references/artifact-contracts.md#feature-brief-contract);
the cross-harness handoff rules are in the [Harness Command Contract](references/harness-command-contract.md).

After `discuss`, a developer may explicitly invoke `consult` from Claude Code or
Codex to pressure-test the same Brief. It reports one bounded batch of
evidence-backed findings and changes nothing until the human accepts selected
findings. A Ready baseline remains immutable and changes are recorded as
amendments. Consultation is never mandatory in the normal
`discuss -> build -> review -> ship` path and creates no consultation artifact;
the cross-harness decision is recorded in the [optional consultation
ADR](docs/adr/2026-08-27-optional-cross-model-brief-consultation.md).
Repository content is untrusted evidence and cannot authorize writes, activation,
or unrelated disclosure; secrets and credentials encountered during inspection
are redacted and never copied into durable artifacts or conversation.

Review is explicit-only and starts only with matching Feature Brief and `review.md`
paths. It loads accepted intent, decisions, Build Evidence, and the recorded
starting revision before assessing the current worktree. The reviewer uses the
active configured model and never inherits Build Recommendation metadata.
Changed files receive a feature-scoped TODO/FIXME/XXX, placeholder, and hack
scan; missing or stale verification prompts a narrow relevant check. When fresh
dispatch is unavailable, the same read-only assessment runs inline and is
labelled `advisory (not fully isolated)`. Review never runs an automatic triada
and never deploys, pushes, creates a PR, merges, or rewrites history. The complete
finding and pass schemas live in the [Delivery Artifact Contracts](references/artifact-contracts.md),
the native handoff is in the [Harness Command Contract](references/harness-command-contract.md),
and the architecture decision is [ADR: Independent Review and Bounded Fix Loop](docs/adr/2026-08-28-independent-review-and-bounded-fix-loop.md).

Ship runs only when the Brief is `In Review`, Review is `Complete`, no open
`BLOCKING` finding remains, and the Review-owned source manifest/fingerprint is
fresh. It renders from the final post-review state, not from an earlier preview:
the Feature Record keeps accepted intent separate from the as-built result and
records deviations, verification, Review findings, ADR links, durable knowledge,
follow-ups, and a recommended path-only review order. The Executive Summary is
self-contained HTML with inline CSS, escaped text, repository-relative links,
and no source excerpts or external assets. Execution Map outcomes are
consolidated into the record rather than archived separately.

Before mutation, Ship shows the exact archive files, active-file deletions,
memory destinations, commit message, PR description, and staging set. One
explicit approval binds that preview to the fingerprint; every memory candidate
is accepted or rejected individually. The approved archive, memory promotion,
active-artifact cleanup, staging, and local commit run as one journaled local
transaction under `.ship-txn/{txid}/journal.json`, with advisory-lock metadata,
output hashes, recovery, resume, and rollback. Archives remain durable and the
transaction directory is transient/ignored. A post-approval or pre-freeze drift
returns the same paths to Review without mutation or history rewriting.

## Principles

- Intent is durable; implementation details remain local to the implementing
  model.
- Planning is outcome-oriented and created only when it helps execution or
  resumption.
- Verification is part of implementation, not a separate ceremony.
- Review is independent, evidence-based, and performed once on the completed
  change.
- ADRs preserve architectural decisions; project memory preserves reusable traps
  and lessons.
- Core workflow skills are explicitly invoked. Only `debug` may auto-trigger for
  a concrete failure.
- `consult` is optional and explicit-only; it never silently runs, gates `build`,
  or rewrites a Ready intent baseline.
- `build` applies a Failure Boundary Check before a second speculative repair,
  keeps non-trivial adjacent work as a follow-up, and maintains concise,
  truthful documentation for public APIs and critical internals.
- Build checkpoints and map sections are recovery/resume facts only. Build
  never deploys, pushes, creates a PR, merges, rewrites history, or presents a
  partial outcome as independently shippable; the whole Feature Brief is one
  delivery unit. See [ADR-004](docs/adr/2026-08-28-outcome-oriented-build-and-checkpoints.md),
  [ADR-005](docs/adr/2026-08-28-single-delivery-unit-no-partial-deployment.md),
  and the [artifact contract](references/artifact-contracts.md).
- The map records `base_commit` so review can trace the complete feature diff.
  Keep the overlapping AbsolutPowers workflow disabled while using AbsolutForge;
  the two workflows must not be active together.
- No global SessionStart hook injects the workflow into unrelated sessions.

## Initial scope

The MVP targets Claude Code and Codex through one host-agnostic skill tree with
thin per-harness manifests. Pi and Grok are intentionally deferred until the
workflow is validated on real changes.

## Canonical documentation

Start with the [Product Vision](docs/product-vision.md), then the [MVP
roadmap](absolutforge/features/absolutforge-mvp/planning-main.md) and the
relevant phase plan. Exact operational schemas are owned by the [Delivery
Artifact Contracts](references/artifact-contracts.md), memory routing by the
[Project-Memory Contract](references/project-memory.md), and native handoffs by
the [Harness Command Contract](references/harness-command-contract.md).
Architecture decisions are recorded in [`docs/adr/`](docs/adr/), and durable
cross-cutting lessons are kept in [`absolutforge/project-memory.md`](absolutforge/project-memory.md).

## Private-pilot validation and isolation

The pilot is intentionally validated locally and non-mutating. These checks
inspect metadata, layout, links, and tests; they do not install or enable
AbsolutForge:

```text
python3 -m unittest discover -s tests -t . -p 'test_*.py'
for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done
claude plugin validate --strict .
python3 /Users/kamil/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

The Codex validator is optional when its PyYAML dependency is unavailable; the
deterministic JSON checks remain the non-mutating fallback. Activation is
deferred until product validation. Before any later normal use, disable the
overlapping AbsolutPowers workflow first; both workflows must not be enabled at
the same time. Validation commands and documentation never toggle that
user-owned configuration automatically.

## Artifact lifecycle

During delivery:

```text
absolutforge/features/{slug}/
├── feature-brief.md
├── execution-map.md   # optional
└── review.md
```

After shipping:

```text
absolutforge/archives/{slug}/
├── feature-record.md
└── executive-summary.html
```

The Feature Record preserves the original intent separately from the as-built
result and explicitly records deviations. The HTML summary is generated from the
final post-review state for human PR review.

Ship removes only the approved active Brief, optional Execution Map, and Review
after approval; it does not archive the map as a separate file. Remote actions
remain outside the workflow: a rendered PR description is informational and
does not authorize push, PR creation, merge, deployment, or history rewrite.

## Current planning

The accepted product contracts are captured in
[`docs/product-vision.md`](docs/product-vision.md). New contributors and coding
agents should read that document before interpreting the phase roadmap.

The MVP roadmap and phase stubs live in
[`absolutforge/features/absolutforge-mvp/`](absolutforge/features/absolutforge-mvp/).
