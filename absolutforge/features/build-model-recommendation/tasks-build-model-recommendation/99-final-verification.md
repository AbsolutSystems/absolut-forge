# Final Verification: Build model recommendation

## Status
pending

## Parent
`absolutforge/features/build-model-recommendation/tasks-build-model-recommendation.md`

## Shared Context
Read before starting:
- `absolutforge/features/build-model-recommendation/planning-build-model-recommendation.md`
- `absolutforge/features/build-model-recommendation/tasks-build-model-recommendation/implementation-context.md`
- All completed Phase 1–3 task files

## Context Contract

### Requires (from Phase 1–3)
- Canonical schema, skill integration, tests, and documentation are complete.

### Provides (for review)
- Verified recommendation contract and cross-harness behavior ready for branch review.

## Read Scope
- `absolutforge/features/build-model-recommendation/tasks-build-model-recommendation.md`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `skills/discuss/SKILL.md`
- `skills/build/SKILL.md`
- `tests/test_discuss_contract.py`
- `tests/test_build_contract.py`

## Write Scope
- `absolutforge/features/build-model-recommendation/tasks-build-model-recommendation/99-final-verification.md`

## Objective
Run integrated deterministic verification and record exact results before branch review.

## Task 1: Run integrated verification
**Status:** pending
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11
**Test-first:** no (final verification only)
**Produces:** Recorded verification evidence in this file
**Consumes:** All completed Phase 1–3 artifacts

**Requirements:**
- Run `python3 -m unittest discover -s tests -t . -p 'test_*.py'` and record exit code and test count.
- Parse every tracked or untracked non-ignored JSON descriptor with `python3 -m json.tool` and record the result.
- Run `git diff --check`.
- When available, run `claude plugin validate --strict .`; otherwise record `not applicable — claude CLI unavailable`.
- Scan test sources for literal `AC-1` through `AC-11`; any missing token fails verification.

**Tests:**
- Full suite passes, JSON descriptors parse, diff check passes, Claude validation passes or is explicitly not applicable, and literal `[AC-1]` `[AC-2]` `[AC-3]` `[AC-4]` `[AC-5]` `[AC-6]` `[AC-7]` `[AC-8]` `[AC-9]` `[AC-10]` `[AC-11]` tokens are present in test names/docstrings.

## Phase Verification
Run:
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`
- `git diff --check`

## Completion Criteria
- All required commands pass or an unavailable optional command is recorded as not applicable.
- Every AC-1 through AC-11 is present in test sources.
- Exact outputs and skipped checks are recorded below.

## Implementation Decisions / Remarks
- Commands executed: to be completed after verification.
- Results: to be completed after verification.
- Skipped checks: to be completed after verification.
