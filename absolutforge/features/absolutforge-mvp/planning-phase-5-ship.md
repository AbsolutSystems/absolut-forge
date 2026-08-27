# Phase 5: Ship (epic: AbsolutForge MVP)

## Parent context

> Start by reading `absolutforge/features/absolutforge-mvp/planning-main.md`.

- Epic planning: `absolutforge/features/absolutforge-mvp/planning-main.md`
- Dependencies: Phase 4 review with no open `BLOCKING` findings

## Status
To plan — 2026-08-27

## Phase goal

Deliver final closeout that preserves original intent and the as-built result,
generates a human-facing Executive Summary HTML from the post-review state,
promotes approved memory, archives active artifacts, and prepares the local
commit plus PR description.

## Scope

### In scope

- Brief-to-diff consistency and deviation reporting.
- Consolidated `feature-record.md` with immutable original intent.
- Self-contained `executive-summary.html` optimized for human PR review.
- Proposed project-memory or package-local Gotchas promotion with human approval.
- Active artifact cleanup, local commit, and copyable PR description.

### Out of scope

- Generating HTML before review fixes are complete.
- Automatic push, PR creation, merge, or history rewriting.
- Archiving unrelated reports or another feature's artifacts.

### Deliberately not doing

- Keeping the transient Execution Map in the final archive.
- Rewriting original intent to make implementation deviations disappear.

## Assumptions and decisions

### Assumptions

- The final diff is the source of truth for what was built; the Brief is the
  source of truth for why it was requested.

### Decisions requiring confirmation

- TODO — finalize the self-contained HTML rendering approach and preview gate.

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

- Should the Executive Summary embed selected code excerpts or link only to the
  recommended review order?

## Discussion notes

- The HTML is for humans; Markdown plus diff remain the inputs for model review.

