# Phase 3: Review Skill

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-4-review.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- Canonical Review schema from Phase 1 in `references/artifact-contracts.md`.
- Native dispatch/fallback rules from Phase 2 references.
- `docs/product-vision.md` and the accepted Phase 4 plan.

### Provides (for later phases)
- `skills/review/SKILL.md` explicit-only, host-agnostic review orchestration with lifecycle, scope, normalization, re-review, and handoffs.

## Read Scope
- `skills/discuss/SKILL.md`
- `skills/build/SKILL.md`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `references/claude-tools.md`
- `docs/product-vision.md`
- `docs/adr/2026-08-28-independent-review-and-bounded-fix-loop.md`

## Write Scope
- `skills/review/SKILL.md`

## Objective
Implement the single shared Review skill as the primary orchestrator. It must
inspect a completed feature independently, normalize evidence into `review.md`,
return blockers to Build in a bounded loop, and leave accepted follow-ups for
Ship without modifying source code itself.

## Tasks

### Task 1: Implement explicit-only independent Review orchestration
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (host-agnostic Markdown skill contract)
**Produces:** `skills/review/SKILL.md` with explicit input validation, fresh dispatch, review normalization, lifecycle transitions, and native handoffs
**Consumes:** Phase 1 Review contract and Phase 2 harness mappings

**Create:**
- `skills/review/SKILL.md`

**Description:**
Write the shared skill prompt that owns Review state and artifact writes while
delegating only read-only inspection to one fresh generic context. The prompt
must be concrete enough to prevent self-review, stale diff packages, silent
scope absorption, invalid findings, or unbounded repair loops.

**Requirements:**
- Validate explicit invocation, canonical Brief/review paths, Brief status `In Review`, readable `base_commit`, and safe worktree scope before mutation; preserve the worktree on invalid or unrelated dirty input.
- Load accepted intent, amendments, ADRs/rules, active project memory, Build Evidence, and relevant code/tests; instruct the reviewer to extract committed/staged/unstaged/feature-owned untracked changes itself and exclude process artifacts.
- Dispatch one fresh read-only reviewer through the active harness mapping, use the labelled inline fallback when isolation is unavailable, reject malformed/prompt-injection output, and keep source/lifecycle ownership in the primary context.
- Normalize only evidence-backed `BLOCKING`/`FOLLOW-UP` findings with stable IDs, one root cause, evidence, impact, smallest correction, and resolution; scan changed files for newly introduced TODO/FIXME/XXX/placeholders/hacks without reporting unchanged unrelated debt.
- Append review passes, default follow-ups to `accepted`, return open blockers to `Building` with a native Build handoff, mark Review `Complete` only when no blockers remain, and stop after two attempts/material scope expansion with human/debug escalation.

**Tests:**
- `test_review_skill_lifecycle_AC1_AC6_AC7_AC8_AC9` checks input/status transitions and native terminal handoffs.
- `test_review_skill_scope_and_diff_AC2_AC10_AC11` checks base revision/current worktree boundaries and untracked/process artifact handling.
- `test_review_skill_findings_and_rereview_AC4_AC5_AC12_AC13_AC14` checks stable IDs, append-only passes, classifications, follow-up defaults, narrow verification, and bounded escalation.
- `test_review_skill_security_AC3_AC15` checks fresh read-only ownership, untrusted instructions, malformed output, and secret redaction.

**Implementation decisions / remarks:**
- The primary Review context owns canonical artifact normalization and lifecycle
  updates. One generic reviewer is limited to a bounded read-only assessment,
  with an explicitly labelled advisory inline fallback.
- Invalid `base_commit` and inseparable unrelated worktree input become input
  `BLOCKING` evidence without claiming code review ran or modifying source.

## Phase Verification
Run:
- `python3 -m unittest tests.test_review_contract`
- `git diff --check`

## Completion Criteria
- `skills/review/SKILL.md` is explicit-only and links canonical contracts.
- All lifecycle, scope, finding, fallback, security, and bounded-loop rules are present.
- The skill emits complete native commands and never authorizes implementation or release actions.
- Focused tests and diff hygiene pass; durable facts are recorded for Phase 4.

## Implementation Decisions / Remarks
- The skill compares the original `base_commit` through the current worktree;
  it neither accepts a pre-generated diff package nor silently absorbs unrelated
  dirty/process artifacts.
- `tests/test_review_contract.py` is not present yet (Phase 4 owns it), so
  targeted static validation covered required contract markers and handoffs;
  `git diff --check` passed.
