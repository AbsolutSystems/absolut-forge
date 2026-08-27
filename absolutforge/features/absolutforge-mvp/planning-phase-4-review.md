# Phase 4: Review (epic: AbsolutForge MVP)

## Parent context

> Start by reading `absolutforge/features/absolutforge-mvp/planning-main.md`.

- Epic planning: `absolutforge/features/absolutforge-mvp/planning-main.md`
- Dependencies: Phase 3 final diff and Build Evidence

## Status
To plan — 2026-08-27

## Phase goal

Deliver one independent, evidence-based review of the completed change, using a
fresh context and the simple classifications `BLOCKING` and `FOLLOW-UP`.

## Scope

### In scope

- Review against Feature Brief intent, scope, ADRs, diff, and verification.
- Correctness, edge cases, security, data integrity, test value, regressions,
  compatibility, scope creep, and diff garbage.
- A concise persistent `review.md`.
- Focused return to `build` for blocking fixes and targeted re-review.

### Out of scope

- Plan review, task review, phase review, or automatic triada.
- Style findings handled by deterministic tooling.
- Implementing fixes inside the reviewer context.

### Deliberately not doing

- Reporting unrelated existing debt as a current-change blocker.
- Reopening the entire review taxonomy during every re-review.

## Assumptions and decisions

### Assumptions

- One fresh reviewer provides materially better independence than self-review by
  the implementing context.

### Decisions requiring confirmation

- TODO — define how each harness obtains a fresh review context without making
  multi-agent dispatch mandatory everywhere.

## Selected solution
TODO — to plan in a separate phase session.

### Rationale
TODO

### Alternatives considered
TODO

## Implementation plan
TODO — to plan in a separate phase session.

## Files to modify or create
TODO

## Edge cases and risks
TODO

## Acceptance Criteria
TODO — define during phase planning without an automatic QA-enrichment gate.

## Open questions

- What is the precise terminal state when only accepted `FOLLOW-UP` findings
  remain?

## Discussion notes

- A high-risk specialist audit may be invoked manually but is not part of the
  standard workflow.

