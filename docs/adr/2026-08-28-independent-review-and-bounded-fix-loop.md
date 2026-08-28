# ADR: Independent review with a bounded blocker fix loop

## Date
2026-08-28

## Status
Accepted

## Context

AbsolutForge needs a quality gate after autonomous Build without reproducing
AbsolutPowers' multi-agent review ceremony. The reviewer must inspect the
complete current feature change, remain independent of the implementation
context, and still provide a durable path back to Build when a concrete defect
blocks safe delivery.

## Decision

Use one generic read-only reviewer in a fresh context. The primary `review`
skill passes the Feature Brief path, review path, and Build's `base_commit`; the
reviewer extracts the current change itself from the current worktree, including
feature-owned untracked files. The primary context owns `review.md`, lifecycle
transitions, and finding normalization; Build exclusively owns implementation
fixes and their verification. Review-process artifacts and unrelated dirty
changes are excluded from the reviewed scope.

Findings use only `BLOCKING` and `FOLLOW-UP`. Blockers return the Brief to
`Building` for a bounded Build fix and targeted re-review. Follow-ups do not
block ship and default to `accepted` for preservation in the Feature Record.
The same blocker may be attempted twice; a repeated failure or material scope
expansion escalates to the human/debug path. Review uses the active harness'
configured model and does not inherit Build's model recommendation. If fresh
dispatch is unavailable, the inline result is explicitly advisory/non-isolated.

## Considered alternatives

- **Inline-only review:** rejected because it weakens independence; retained as
  an explicitly labelled fallback when fresh dispatch is unavailable.
- **Automatic triada or named review registry:** rejected for token cost,
  host coupling, and unnecessary ceremony.
- **Pre-generated diff package:** rejected because it can be stale; the reviewer
  must inspect the current repository from `base_commit`.
- **Block ship on follow-ups:** rejected because it recreates mandatory task
  work and slows the delivery path.

## Consequences

- Review is independent and cross-harness while remaining one bounded gate.
- `review.md` must preserve append-only re-review history and stable finding IDs.
- The primary context needs safe diff/status extraction and explicit filtering of
  process artifacts and unrelated dirty changes.
- Accepted follow-ups remain visible and actionable without delaying ship.
- Inline fallback can be advisory rather than fully isolated; this limitation is
  visible instead of silently omitted.

## Related

- Product behavior: `docs/product-vision.md#review-contract`
- Product vision: `docs/product-vision.md` (`Review contract`)
