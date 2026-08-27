# AbsolutForge

AbsolutForge is an intent-driven development workflow for strong coding models.
It gives the model a precise product goal, durable context, and room to execute
autonomously, while concentrating quality control on verification and one final,
independent review.

> Status: design and planning. The plugin is not implemented yet.

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
