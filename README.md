# AbsolutForge

AbsolutForge is an intent-driven development workflow for strong coding models.
It gives the model a precise product goal, durable context, and room to execute
autonomously, while concentrating quality control on verification and one final,
independent review.

> Status: private pilot foundation. The workflow skills are not implemented yet;
> local manifests and documentation are being validated without activation.

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
- **build** implements autonomously, creates an Execution Map only when useful,
  and runs focused plus final verification.
- **review** performs one independent review with `BLOCKING` and `FOLLOW-UP`
  findings.
- **ship** creates the final Feature Record, a human-facing Executive Summary
  HTML, promotes approved project memory, and prepares the local commit and PR
  description.

Two standalone workflows complement the core:

- **debug** investigates root cause and, when fixing, creates a compact Fix Brief.
- **tech-debt** produces a static, evidence-based remediation backlog.

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
