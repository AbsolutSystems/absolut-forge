# Phase 4: Contract Tests and Product Documentation

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-4-review.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- `skills/review/SKILL.md` and `skills/review/agents/openai.yaml` from Phases 2–3.
- Canonical Review and handoff references from Phases 1–2.
- Existing helpers and allowlists in `tests/test_foundation.py`.

### Provides (for later phases)
- `tests/test_review_contract.py` deterministic AC-tokenized Review coverage.
- Foundation tests that discover four explicit-only skills and validate Review metadata.
- Product and contributor docs consistently describing Review as implemented.

## Read Scope
- `tests/test_foundation.py`
- `tests/test_build_contract.py`
- `tests/test_discuss_contract.py`
- `tests/test_consult_contract.py`
- `skills/review/SKILL.md`
- `skills/review/agents/openai.yaml`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `references/claude-tools.md`
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`

## Write Scope
- `tests/test_review_contract.py`
- `tests/test_build_contract.py`
- `tests/test_foundation.py`
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`

## Objective
Make the Review stage mechanically verifiable and visible in product
documentation without duplicating canonical schemas. Keep tests static,
deterministic, non-mutating, and independent of model availability.

## Tasks

### Task 1: Add deterministic Review contract tests and foundation integration
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (the deterministic contract suite is the deliverable)
**Produces:** `tests/test_review_contract.py` plus four-skill/fourth-metadata assertions in `tests/test_foundation.py`
**Consumes:** All Phase 1–3 contracts, skill, and metadata

**Create:**
- `tests/test_review_contract.py`

**Modify:**
- `tests/test_build_contract.py`
- `tests/test_foundation.py`

**Description:**
Create a static conformance suite following the existing test helpers and
extend foundation discovery for the new skill. Assertions must inspect text and
metadata only; they must never invoke a model, mutate plugin configuration, or
run the Review workflow.

**Requirements:**
- Assert explicit-only frontmatter/metadata, canonical links, fresh dispatch/fallback, no Build Recommendation inheritance, and untrusted-content/redaction rules with AC-bearing test names/docstrings.
- Assert Brief/review lifecycle, base-commit/current-worktree boundaries, feature-owned untracked inclusion, process-artifact exclusion, and unrelated-dirty handling.
- Assert stable finding IDs, required evidence fields, allowed classifications/resolutions, append-only targeted re-review, follow-up defaults, two-attempt escalation, and narrow verification.
- Update foundation expected skill paths/directories and loop over `review` metadata without weakening existing manifest or capability assertions; keep the existing Build handoff assertion compatible with Review's current-worktree extension.
- Keep every `AC-1` through `AC-15` literal visible in test names or docstrings and use precise failure messages.

**Tests:**
- `test_review_contract.py` methods `test_lifecycle_AC1_AC6_AC7_AC8_AC9`, `test_diff_scope_AC2_AC10_AC11`, `test_findings_AC4_AC5_AC12_AC13_AC14`, and `test_security_AC3_AC15` cover the full Review contract.
- Full foundation suite confirms the fourth skill is explicit-only and has `$review` metadata.

**Implementation decisions / remarks:**
- Added static Review conformance coverage for lifecycle validation, current-worktree scope, stable finding history, bounded blocker handling, explicit-only dispatch, untrusted-content handling, and redaction.
- Kept the existing Build contract test aligned with the current-worktree review boundary while preserving the canonical Build handoff assertions.
- Extended foundation discovery and metadata checks to the four explicit-only MVP skills.

### Task 2: Update product and contributor documentation
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-5, AC-6, AC-7, AC-8, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (documentation update)
**Produces:** Review-implemented lifecycle descriptions in `README.md`, `CLAUDE.md`, `docs/product-vision.md`, and `skills/README.md`
**Consumes:** `skills/review/SKILL.md` and canonical Review/handoff contracts

**Modify:**
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`

**Description:**
Replace planned/stub wording with the implemented Review stage while preserving
the separate Ship stage and the product's low-ceremony boundary. Link canonical
schemas rather than copying them, and make the review/fix handoff understandable
to a human PR reviewer.

**Requirements:**
- Mark Review as implemented while preserving `discuss -> build -> review -> ship` and the Phase 5 Ship dependency.
- Describe one fresh evidence-based reviewer, only `BLOCKING`/`FOLLOW-UP`, stable history, accepted follow-ups, bounded Build return, and no automatic triada.
- Describe current-worktree/base-commit extraction, feature-scoped TODO/hack checks, narrow verification, active-model ownership, and inline advisory fallback.
- Preserve explicit-only activation, no deployment/push/PR/merge/history rewrite, untrusted repository/secret-redaction, and AbsolutPowers isolation language.
- Link the new ADR and canonical references without adding an alternate Review schema.

**Tests:**
- Documentation assertions in `test_product_docs_review_AC1_AC2_AC3_AC5_AC6_AC7_AC8_AC10_AC11_AC12_AC13_AC14_AC15` verify the product-facing boundary.

**Implementation decisions / remarks:**
- Marked Review as implemented across README, CLAUDE.md, product vision, and skills index while preserving Ship as the separate closeout stage.
- Documentation links the canonical artifact and harness contracts and describes the one-reviewer, BLOCKING/FOLLOW-UP, bounded-fix-loop, untrusted-content, and no-deploy/push/PR boundaries without duplicating schemas.

## Phase Verification
Run:
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- `git diff --check`

## Completion Criteria
- All task tests and the full static suite pass.
- Foundation allowlists and metadata checks cover exactly four skills.
- Documentation describes Review as implemented without moving Ship or introducing duplicate schemas.
- Changes remain within Write Scope and durable handoff facts are recorded.

## Implementation Decisions / Remarks
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'` -> 56 tests passed.
- `git diff --check` -> clean.
