# Phase 99: Final Verification

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-4-review.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- All Phase 1–4 `Context Contract -> Provides` entries are fulfilled.
- `tests/test_review_contract.py` contains token-bearing tests for AC-1 through AC-15.

### Provides (for later phases)
- Verified Phase 4 Review skill, canonical contracts, harness mappings, metadata,
  tests, and documentation ready for the product-level review closure.

## Read Scope
- `absolutforge/features/absolutforge-mvp/tasks-phase-4-review.md`
- All Phase 1–4 files referenced above
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `references/claude-tools.md`
- `skills/review/SKILL.md`

## Write Scope
- `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/99-final-verification.md`

## Objective
Run complete deterministic validation against the integrated Phase 4 change and
record exact results. This verifies repository contracts only; it does not invoke
a model, activate a plugin, deploy, push, create a PR, merge, or rewrite history.

## Tasks

### Task 1: Run integrated Phase 4 verification
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (final verification only)
**Produces:** Verified Phase 4 repository state and exact command results recorded in this file
**Consumes:** All completed Phase 1–4 artifacts and `implementation-context.md`

**Requirements:**
- Run `python3 -m unittest discover -s tests -t . -p 'test_*.py'` and record exit code and test count.
- Run `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done` and `git diff --check`.
- Run `claude plugin validate --strict .` when Claude CLI exists; otherwise record `not applicable — claude CLI unavailable`.
- Grep test sources for every literal `AC-1` through `AC-15`; missing tokens fail verification.
- Record commands, results, skipped checks, and any plugin validator limitation; do not mark complete while a required command fails.

**Tests:**
- AC token scan confirms `AC-1`, `AC-2`, `AC-3`, `AC-4`, `AC-5`, `AC-6`, `AC-7`, `AC-8`, `AC-9`, `AC-10`, `AC-11`, `AC-12`, `AC-13`, `AC-14`, and `AC-15` are present in test sources.

**Implementation decisions / remarks:**
- `rtk test python3 -m unittest discover -s tests -t . -p 'test_*.py'` -> pass; 56 tests.
- `rtk git diff --check` -> pass; no whitespace errors.
- `rtk claude plugin validate --strict .` -> pass; marketplace manifest validated.
- Recursive JSON parse -> pass; 4 JSON files validated.
- AC token scan -> pass; every literal `AC-1` through `AC-15` is present in test sources.
- No required checks skipped.

## Phase Verification
Run:
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`
- `git diff --check`

## Completion Criteria
- All implementation phases and task statuses are completed.
- Full suite, JSON validation, diff hygiene, applicable plugin validation, and AC token scan pass or are explicitly marked not applicable.
- This file contains exact evidence and the orchestrator has read it.

## Implementation Decisions / Remarks
- Integrated Phase 4 verification is complete and all required deterministic
  checks passed. No model activation, deployment, push, PR, merge, or history
  rewrite was performed.
