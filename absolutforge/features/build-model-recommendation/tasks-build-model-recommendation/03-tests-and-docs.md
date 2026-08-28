# Phase 3: Contract Tests and Product Documentation

## Status
completed

## Parent
`absolutforge/features/build-model-recommendation/tasks-build-model-recommendation.md`

## Shared Context
Read before starting:
- `absolutforge/features/build-model-recommendation/planning-build-model-recommendation.md`
- `absolutforge/features/build-model-recommendation/tasks-build-model-recommendation/implementation-context.md`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `skills/discuss/SKILL.md`
- `skills/build/SKILL.md`

## Context Contract

### Requires (from Phase 1–2)
- Canonical recommendation schema and harness mapping.
- Discuss output and Build consumption wording.

### Provides (for final verification)
- Deterministic AC-tokenized tests for the recommendation contract across both skills.
- Product and contributor documentation that describes model guidance without implying hard enforcement or automatic switching.

## Read Scope
- `absolutforge/features/build-model-recommendation/planning-build-model-recommendation.md`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `skills/discuss/SKILL.md`
- `skills/build/SKILL.md`
- `tests/test_discuss_contract.py`
- `tests/test_build_contract.py`
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`

## Write Scope
- `tests/test_discuss_contract.py`
- `tests/test_build_contract.py`
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`

## Objective
Make the recommendation behavior mechanically verifiable and visible in all
product entry points without duplicating canonical schemas.

## Tasks

### Task 1: Add deterministic contract coverage
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11
**Test-first:** no (static contract-suite extension)
**Produces:** AC-tokenized tests in `tests/test_discuss_contract.py` and `tests/test_build_contract.py`
**Consumes:** Phase 1 canonical references and Phase 2 skill contracts

**Modify:**
- `tests/test_discuss_contract.py`
- `tests/test_build_contract.py`

**Description:**
Extend the existing deterministic scanners to assert schema position and
allowed values, profile selection evidence, advisory consumption, fallback and
override recording, compatibility with missing recommendations, immutable
intent, untrusted content, secret redaction, and no partial delivery.

**Requirements:**
- Use literal AC tokens in test names or docstrings for every AC-1 through AC-11.
- Keep tests static, non-mutating, and independent of model calls or provider availability.
- Assert both Claude and Codex model mappings and reject line/file-count-only classification.
- Assert missing/malformed/unavailable recommendation behavior and explicit override evidence.

**Tests:**
- `test_recommendation_schema` display names `[AC-1] [AC-2] [AC-3] [AC-5] [AC-6] [AC-7] [AC-8] [AC-11]`
- `test_discuss_recommendation` display names `[AC-1] [AC-2] [AC-3] [AC-9] [AC-10] [AC-11]`
- `test_build_recommendation` display names `[AC-4] [AC-5] [AC-6] [AC-7] [AC-8] [AC-11]`

**Implementation decisions / remarks:**
- Added static AC-tokenized coverage for schema placement, profile mapping, evidence-based classification, fallback/override handling, immutable intent, untrusted content, redaction, and no partial delivery.
- Tests remain non-mutating and model/provider independent; existing contract checks continue to pass.

### Task 2: Update product and contributor documentation
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-11
**Test-first:** no (documentation update)
**Produces:** Consistent model recommendation guidance in `README.md`, `CLAUDE.md`, `docs/product-vision.md`, and `skills/README.md`
**Consumes:** Phase 1–2 recommendation contract and skill behavior

**Modify:**
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`

**Description:**
Document simple/single → Sonnet/Luna and complex/phased → Opus/Terra, explain
that the suggestion is advisory and overridable, and state that no automatic
switching, deployment, or additional ceremony is introduced.

**Requirements:**
- Preserve the core `discuss -> build -> review -> ship` lifecycle and AbsolutPowers isolation.
- Link the canonical Brief contract and harness/Codex references instead of copying schemas.
- Explain compatibility with older Briefs and evidence recorded for fallback/override.
- Retain untrusted-input and secret-redaction guidance.

**Tests:**
- `test_model_recommendation_docs` display names `[AC-1] [AC-2] [AC-3] [AC-4] [AC-5] [AC-6] [AC-7] [AC-8] [AC-11]`

**Implementation decisions / remarks:**
- Updated README, CLAUDE, Product Vision, and skills index with advisory simple/single and complex/phased model guidance, fallback/override evidence, and non-gating boundaries.
- Documentation links to canonical contracts instead of duplicating the Brief schema.

## Phase Verification
Run:
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- `git diff --check`

## Completion Criteria
- Both tasks are completed within Write Scope.
- Every AC-1 through AC-11 has token-bearing deterministic coverage.
- Documentation is consistent per file and does not imply hard model enforcement.
- Phase verification passes.

## Implementation Decisions / Remarks
- Recommendation guidance is described consistently across product and contributor entry points while keeping exact fields owned by canonical references.
- Deterministic tests assert the advisory boundary and all AC-1 through AC-11 without invoking models or assuming provider availability.
- Verification passed: `python3 -m unittest discover -s tests -t . -p 'test_*.py'` (50 tests) and `git diff --check`.
