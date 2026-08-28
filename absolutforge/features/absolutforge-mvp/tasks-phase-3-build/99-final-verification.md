# Phase 99: Final Verification

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-3-build.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-3-build/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- All Phase 1–3 `Context Contract -> Provides` entries are fulfilled.
- `tests/test_build_contract.py` exists and contains token-bearing tests for AC-1 through AC-15.

### Provides (for later phases)
- Verified Phase 3 Build skill, contracts, tests, manifests, and documentation ready for the independent Phase 4 review.

## Read Scope
- `absolutforge/features/absolutforge-mvp/tasks-phase-3-build.md`
- All Phase 1–3 files referenced above
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`

## Write Scope
- `absolutforge/features/absolutforge-mvp/tasks-phase-3-build/99-final-verification.md`

## Objective
Run the complete deterministic validation suite against the integrated Phase 3
change, record exact results, and confirm that every Acceptance Criterion token is
represented in tests. This task verifies repository contracts only; it does not
install/enable the plugin, invoke a model, deploy, push, create a PR, merge, or
rewrite history.

## Tasks

### Task 1: Run integrated Phase 3 verification
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (final verification only)
**Produces:** Verified Phase 3 repository state and recorded command results in this file
**Consumes:** All completed Phase 1–3 artifacts and `implementation-context.md`

**Requirements:**
- Run `python3 -m unittest discover -s tests -t . -p 'test_*.py'` and record the exit code and test count.
- Run `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done` and record whether every descriptor parses; run `git diff --check`.
- Run `claude plugin validate --strict .` when the Claude CLI exists; otherwise record `not applicable — claude CLI unavailable` without claiming validation.
- Grep test sources for every literal AC token `AC-1` through `AC-15`; a missing token fails this task.
- Record skipped checks and exact results under `Implementation decisions / remarks`; do not mark complete while any required command fails.

**Tests:**
- `test_build_contract.py` token scan: `AC-1`, `AC-2`, `AC-3`, `AC-4`, `AC-5`, `AC-6`, `AC-7`, `AC-8`, `AC-9`, `AC-10`, `AC-11`, `AC-12`, `AC-13`, `AC-14`, `AC-15` all present.

**Implementation decisions / remarks:**
- Commands executed: to be completed after verification.
- Results: to be completed after verification.
- Skipped checks: to be completed after verification.

## Phase Verification
Run:
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`
- `git diff --check`

## Completion Criteria
- Task 1 is completed only after all required commands pass or explicitly applicable checks are recorded as not applicable.
- Every AC token `AC-1` through `AC-15` is found in test sources.
- This file contains exact command results and skipped-check explanations.
- The orchestrator marks Final Verification completed only after reading this evidence.

## Implementation Decisions / Remarks
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'` — exit 0; 46 tests passed.
- `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done` — exit 0; all JSON descriptors parsed.
- `git diff --check` — exit 0; no whitespace errors.
- AC token scan over `tests/` — exit 0; every literal `AC-1` through `AC-15` is present.
- `claude plugin validate --strict .` — exit 0; Claude CLI available and validation passed.
- Verification is static and non-mutating; no plugin activation, model invocation, deployment, push, PR, merge, or history rewrite was performed.
