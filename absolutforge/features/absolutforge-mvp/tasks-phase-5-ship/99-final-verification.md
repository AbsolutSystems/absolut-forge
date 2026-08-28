# Phase 99: Final Verification

## Status
pending

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-5-ship.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-5-ship/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- All Phase 1–4 `Context Contract -> Provides` entries are fulfilled.
- `tests/test_ship_contract.py` and `tests/test_review_contract.py` contain token-bearing tests for AC-1 through AC-15.
- `tests/test_foundation.py` discovers the fifth Ship skill and its explicit-only Codex metadata.

### Provides (for later phases)
- Verified Phase 5 Ship skill, Review fingerprint handoff, canonical contracts, harness mappings, tests, and product documentation ready for branch-level Review.

## Read Scope
- `absolutforge/features/absolutforge-mvp/tasks-phase-5-ship.md`
- All Phase 1–4 files referenced in its Phase Overview
- `references/artifact-contracts.md`
- `references/project-memory.md`
- `references/harness-command-contract.md`
- `references/claude-tools.md`
- `references/codex-tools.md`
- `skills/review/SKILL.md`
- `skills/ship/SKILL.md`
- `tests/test_ship_contract.py`

## Write Scope
- `absolutforge/features/absolutforge-mvp/tasks-phase-5-ship/99-final-verification.md`

## Objective
Run complete deterministic validation against the integrated Phase 5 change and
record exact results. This verifies repository contracts only; it does not invoke
a model, activate a plugin, mutate a real feature archive, deploy, push, create a
PR, merge, or rewrite history.

## Tasks

### Task 1: Run integrated Phase 5 verification
**Status:** pending
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (final verification only)
**Produces:** Verified Phase 5 repository state and exact command results recorded in this file
**Consumes:** All completed Phase 1–4 artifacts and `implementation-context.md`

**Requirements:**
- Run `python3 -m unittest discover -s tests -t . -p 'test_*.py'` and record exit code and test count. The focused `python3 -m unittest tests.test_foundation tests.test_review_contract tests.test_ship_contract` modules must also pass, providing the exact Ship/Review frontmatter and Codex metadata validation.
- Run `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`, `git diff --check`, and validate all Ship/review skill frontmatter and Codex metadata.
- Run `claude plugin validate --strict .` when the Claude CLI exists; otherwise record `not applicable — claude CLI unavailable`.
- Assert every literal `AC-1` through `AC-15` independently (not one alternation): `python3 - <<'PY'\nfrom pathlib import Path\nsources = '\\n'.join(p.read_text(encoding='utf-8') for p in Path('tests').rglob('test_*.py'))\nfor i in range(1, 16):\n    token = f'AC-{i}'\n    assert token in sources, token\nPY`; missing tokens fail verification.
- Record commands, results, skipped checks, and any validator limitation; do not mark complete while a required verification command fails.

**Tests:**
- Command assertion `python3 - <<'PY' ... for i in range(1, 16): assert f'AC-{i}' in sources ... PY` named `ac_token_scan_AC1_AC2_AC3_AC4_AC5_AC6_AC7_AC8_AC9_AC10_AC11_AC12_AC13_AC14_AC15` independently confirms every traced acceptance token is present in deterministic test sources.

**Implementation decisions / remarks:**
- Commands executed: [to be completed after verification]
- Results: [to be completed after verification]
- Skipped checks: [to be completed after verification or `none`]

## Phase Verification
Run:
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`
- `git diff --check`

## Completion Criteria
- All implementation phases and task statuses are completed.
- Full suite, JSON/frontmatter/metadata validation, diff hygiene, applicable
  plugin validation, and AC token scan pass or are explicitly marked not applicable.
- This file contains exact evidence and the orchestrator has read it.

## Implementation Decisions / Remarks
- [to be completed after phase completion]
