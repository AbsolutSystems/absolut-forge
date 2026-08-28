# ADR: Simple post-review closeout

## Date

2026-08-28

## Status

Accepted

## Context

AbsolutForge needs a local closeout step that turns a reviewed feature into
durable documentation and one local commit. Developers work on a branch and
Review is the quality checkpoint. A complicated freshness or recovery mechanism
would add ceremony without improving the normal workflow.

## Decision

Each feature starts on a clean local branch. Build records that branch's current
commit as `base_commit` and leaves implementation committed before Review.
Review assesses exactly `base_commit..HEAD` and records the reviewed `HEAD`.
Ship requires a `Complete` Review with no open blockers and the same current
branch revision.

There is no separate source-content calculation, lock, transaction journal,
private index, or rollback protocol. If code changes after Review, the developer
commits it and invokes Review again before Ship.

After explicit approval, Ship promotes accepted memory, writes the archive,
removes the active feature artifacts, stages its own closeout changes, and creates one
local commit. On failure it stops and reports the actual worktree state; it does
not overwrite an existing archive or absorb unrelated staged work. It never
pushes, creates a pull request, merges, deploys, or rewrites history.

## Considered alternatives

- **Separate source identity and transaction recovery:** rejected as
  disproportionate to ordinary Git branch review.
- **Reviewing a dirty worktree:** rejected because it makes the reviewed boundary
  ambiguous.
- **Remote-first closeout:** rejected because remote side effects remain an
  explicit human action outside the MVP.

## Consequences

- The normal path remains: build, review, then one local closeout commit.
- A source edit after Review requires a commit and a new Review invocation.
- Ship stays auditable through the committed review range, preview, and approval.

## Related

- Product behavior: `docs/product-vision.md#ship-contract`
- Artifact schemas: `references/artifact-contracts.md`
