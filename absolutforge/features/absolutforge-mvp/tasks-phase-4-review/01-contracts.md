# Phase 1: Canonical Review Contract and Decisions

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-4-review.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- `references/artifact-contracts.md` Feature Brief, Build Evidence, and existing Review contract.
- `absolutforge/features/absolutforge-mvp/planning-phase-4-review.md` accepted scope and AC.
- `docs/product-vision.md` accepted review and ship lifecycle.

### Provides (for later phases)
- `references/artifact-contracts.md` canonical Review schema with stable finding IDs, append-only passes, valid resolutions, current-worktree boundaries, and bounded fix-loop semantics.
- `docs/adr/2026-08-28-independent-review-and-bounded-fix-loop.md` accepted rationale and consequences for one fresh reviewer.

## Read Scope
- `docs/product-vision.md`
- `absolutforge/features/absolutforge-mvp/planning-main.md`
- `absolutforge/features/absolutforge-mvp/planning-phase-4-review.md`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `docs/adr/2026-08-28-outcome-oriented-build-and-checkpoints.md`
- `docs/adr/2026-08-28-single-delivery-unit-no-partial-deployment.md`

## Write Scope
- `references/artifact-contracts.md`
- `docs/adr/2026-08-28-independent-review-and-bounded-fix-loop.md`

## Objective
Make the Review artifact and lifecycle precise enough that later skill and
harness work can implement them without inventing schema or status rules. Keep
the existing Build and Ship contracts intact while adding only Phase 4 semantics.

## Tasks

### Task 1: Extend the canonical Review artifact and bounded lifecycle
**Status:** completed
**Traces to:** AC-1, AC-2, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (canonical Markdown schema and lifecycle documentation)
**Produces:** `references/artifact-contracts.md` Review contract with `## Review contract`, stable `F-NNN` finding IDs, pass history, valid resolutions, worktree scope, and terminal outcome rules
**Consumes:** Existing Feature Brief, Build Evidence, and Review headings in `references/artifact-contracts.md`

**Modify:**
- `references/artifact-contracts.md`

**Description:**
Replace the minimal Review template with a canonical, append-only contract that
preserves original evidence across targeted re-reviews. Define the exact input
boundary, classification threshold, lifecycle transitions, follow-up disposition,
and bounded retry behavior without adding a task or triada stage.

**Requirements:**
- Define Review context fields for the Brief, linked decisions/rules, `base_commit` versus current worktree, and verification evidence; state that the reviewer extracts the change itself.
- Define stable finding IDs, one-root-cause findings, required Evidence/Impact/Smallest sensible correction/Resolution fields, `BLOCKING` and `FOLLOW-UP` only, and resolutions `open`, `fixed`, `accepted`, or `deferred`.
- Define append-only review passes and targeted re-review ordering: prior blocker IDs first, then a short regression scan; preserve follow-up history and default follow-ups to `accepted`.
- Define status transitions: `In Review` with open blockers returns the Brief to `Building`; no open blockers changes Review to `Complete` and permits `ship`; the same blocker gets at most two fix attempts.
- Define inclusion of feature-owned untracked files, exclusion of review/process artifacts and unrelated dirty changes, narrow verification on missing/contradictory evidence, and redaction/untrusted-content boundaries.

**Tests:**
- Contract scanner assertions named `test_review_schema_AC1_AC2_AC4_AC5_AC6_AC7_AC8_AC9_AC10_AC11_AC12_AC13_AC14_AC15` verify every required heading and literal status/classification token.

**Implementation decisions / remarks:**
- Extended the canonical schema with base revision/current-worktree scope,
  stable `F-NNN` findings, append-only pass history, explicit resolutions, and
  bounded blocker/follow-up lifecycle. Preserved Build and Ship ownership.

## Phase Verification
Run:
- `python3 -m unittest tests.test_foundation`
- `git diff --check`

## Completion Criteria
- Task 1 is completed and only its Write Scope changed.
- Review schema contains no unresolved placeholder or contradictory status.
- Verification commands pass.
- `implementation-context.md` records the canonical finding/resolution facts for later phases.

## Implementation Decisions / Remarks
- Phase verification passed: `python3 -m unittest tests.test_foundation` (13
  tests) and `git diff --check`.
