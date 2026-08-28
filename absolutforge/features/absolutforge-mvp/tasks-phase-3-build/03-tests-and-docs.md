# Phase 3: Contract Tests and Product Documentation

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-3-build.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-3-build/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- `skills/build/SKILL.md` and `skills/build/agents/openai.yaml` from Phase 2.
- Canonical Build contracts in `references/artifact-contracts.md`, `references/harness-command-contract.md`, and `references/codex-tools.md` from Phase 1.
- Existing test helpers and manifest assertions in `tests/test_foundation.py`, `tests/test_discuss_contract.py`, and `tests/test_consult_contract.py`.

### Provides (for later phases)
- `tests/test_build_contract.py` deterministic AC-tokenized conformance coverage for the complete Build contract.
- Product docs consistently describe Build as implemented, outcome-oriented, resumable, failure-boundary-aware, documentation-conscious, and non-deploying.

## Read Scope
- `tests/test_foundation.py`
- `tests/test_discuss_contract.py`
- `tests/test_consult_contract.py`
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`
- `skills/build/SKILL.md`
- `references/artifact-contracts.md`

## Write Scope
- `tests/test_build_contract.py`
- `tests/test_foundation.py`
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`

## Objective
Make the new Build contract mechanically verifiable and visible in product
documentation without duplicating canonical schemas. Tests must remain static,
deterministic, and non-mutating; documentation must preserve the distinction
between AbsolutForge's runtime workflow and the repository's implementation task
process.

## Tasks

### Task 1: Add deterministic Build contract tests
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (the deterministic contract suite is the task deliverable)
**Produces:** `tests/test_build_contract.py` with static `unittest` coverage for every Build AC and explicit-only metadata
**Consumes:** `skills/build/SKILL.md`, `skills/build/agents/openai.yaml`, and canonical references from previous phases

**Create:**
- `tests/test_build_contract.py`

**Description:**
Create a repository-level conformance suite following existing test helpers. The
tests inspect Markdown/JSON/YAML text and documented command blocks only; they do
not invoke a model, change plugin configuration, deploy, or execute application
code.

**Requirements:**
- Assert canonical input/lifecycle/map/resume/base-commit/checkpoint and final review handoff behavior with test names/docstrings containing `[AC-1]` through `[AC-6]`.
- Assert concise truthful documentation, final verification, no partial deployment, and scout/failure-boundary behavior with token-bearing tests `[AC-7]` through `[AC-13]`.
- Assert optional bounded read-only Sol advisor escalation and conflict handling with an `[AC-14]` test; assert untrusted-content handling, secret redaction, explicit-only activation, and absence of deployment/implicit capabilities with an `[AC-15]` test.
- Reuse `Path`, frontmatter, YAML-text, JSON, and documented-code-block helpers where applicable; fail with precise messages when a contract phrase or forbidden capability is missing.
- Keep the suite non-mutating and make every AC token grep-visible in a test name or docstring.

**Tests:**
- The task's own test methods are the verification: `test_ready_lifecycle` display `[AC-1]`; `test_map_threshold_and_resume` displays `[AC-2]` and `[AC-4]`; `test_autonomous_verification` displays `[AC-3]` and `[AC-8]`; `test_failure_boundary` displays `[AC-5]`, `[AC-6]`, `[AC-10]`, and `[AC-13]`; `test_scout_rule` displays `[AC-11]` and `[AC-12]`; `test_documentation_rule` displays `[AC-7]`; `test_invalid_input` displays `[AC-9]`; `test_advisor_escalation` displays `[AC-14]`; `test_untrusted_and_redaction` displays `[AC-15]`.

**Implementation decisions / remarks:**
- Added a static, whitespace-normalized `unittest` scanner with literal `[AC-1]` through `[AC-15]` tokens; it checks the Build skill, manifests, canonical contracts, and product-doc boundary without model calls.
- Extended the foundation active-skill allowlist to include `build`, keeping the full deterministic suite aligned with the new explicit-only skill.

### Task 2: Update product and contributor documentation for Build
**Status:** completed
**Traces to:** AC-1, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-13, AC-14, AC-15
**Test-first:** no (documentation update)
**Produces:** consistent Build lifecycle descriptions in `README.md`, `CLAUDE.md`, `docs/product-vision.md`, and `skills/README.md`
**Consumes:** `skills/build/SKILL.md` and the canonical Build contracts from Tasks in Phases 1–2

**Modify:**
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`

**Description:**
Replace the planned/stub wording with the implemented Build contract while
keeping canonical schemas linked rather than duplicated. Explain outcome maps,
durable resume, boundary-first escalation, concise documentation maintenance, and
the whole-feature/no-deployment boundary; preserve the separate product identity
and AbsolutPowers isolation.

**Requirements:**
- Mark Build as implemented in status/current-state sections and preserve the core `discuss -> build -> review -> ship` lifecycle.
- Describe the conditional Execution Map, `base_commit`/checkpoint traceability, focused-versus-final verification, and cross-harness resume without introducing detailed task decomposition.
- Describe Failure Boundary Check semantics, optional read-only Sol escalation, scout/documentation rules, and amendment escalation in plain language.
- State that Build never deploys, pushes, creates PRs, merges, rewrites history, or presents internal outcomes as independently shippable.
- Link ADR-004/ADR-005 and canonical references; retain untrusted-input and secret-redaction guidance.

**Tests:**
- Contract tests: `test_product_docs_contract` with display names `[AC-1]`, `[AC-3]`, `[AC-4]`, `[AC-5]`, `[AC-6]`, `[AC-7]`, `[AC-8]`, `[AC-13]`, `[AC-14]`, `[AC-15]`; scout and invalid-input requirements remain asserted by the complete contract suite with display names `[AC-9]`, `[AC-10]`, `[AC-11]`, `[AC-12]`.

**Implementation decisions / remarks:**
- Marked Build implemented in contributor/product indexes and documented conditional maps, durable resume, Failure Boundary Check, scout/documentation rules, optional redacted Sol advice, no partial deployment, and AbsolutPowers isolation.

## Phase Verification
Run:
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- `git diff --check`

## Completion Criteria
- All phase tasks are completed.
- All changes remain within Write Scope.
- Phase verification commands pass.
- `implementation-context.md` records test entry points and documentation links useful to final verification.
- All `Context Contract -> Provides` items are fulfilled.

## Implementation Decisions / Remarks
- Phase verification passed: `python3 -m unittest discover -s tests -t . -p 'test_*.py'` (46 tests) and `git diff --check`.
