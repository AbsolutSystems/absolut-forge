# AbsolutForge

AbsolutForge is an intent-driven development workflow for strong coding models.
It gives the model a precise product goal, durable context, and room to execute
autonomously, while concentrating quality control on verification and one final,
independent review.

> Status: private pilot foundation. The `discuss`, optional `consult`, and
> `build` skills are implemented; review and closeout stages remain in phased
> delivery and validation is non-mutating.

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
- **review** performs one independent review with `BLOCKING` and `FOLLOW-UP`
  findings.
- **ship** creates the final Feature Record, a human-facing Executive Summary
  HTML, promotes approved project memory, and prepares the local commit and PR
  description.

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

## Current planning

The accepted product contracts are captured in
[`docs/product-vision.md`](docs/product-vision.md). New contributors and coding
agents should read that document before interpreting the phase roadmap.

The MVP roadmap and phase stubs live in
[`absolutforge/features/absolutforge-mvp/`](absolutforge/features/absolutforge-mvp/).
