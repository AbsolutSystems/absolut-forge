# Phase 4: Contract Tests and Product Documentation

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-5-ship.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-5-ship/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- `references/artifact-contracts.md` complete Ship contract from Phase 1.
- `skills/review/SKILL.md` and harness references with fingerprint handoff from Phase 2.
- `skills/ship/SKILL.md` and `skills/ship/agents/openai.yaml` from Phase 3.
- `docs/product-vision.md`, `README.md`, `CLAUDE.md`, and `skills/README.md` current Phase 4 documentation patterns.

### Provides (for later phases)
- `tests/test_ship_contract.py` deterministic coverage of Ship contracts, safety, rendering, recovery, and no-remote behavior.
- `tests/test_review_contract.py` compatibility coverage for the Review-to-Ship fingerprint handoff.
- `tests/test_foundation.py` discovery/metadata coverage for the fifth skill and Ship integration.
- `README.md`, `CLAUDE.md`, `docs/product-vision.md`, `skills/README.md`, and `.gitignore` documentation/configuration reflecting implemented Ship behavior.

## Read Scope
- `absolutforge/features/absolutforge-mvp/planning-phase-5-ship.md`
- `references/artifact-contracts.md`
- `references/project-memory.md`
- `references/harness-command-contract.md`
- `skills/review/SKILL.md`
- `skills/review/agents/openai.yaml`
- `skills/ship/SKILL.md`
- `skills/ship/agents/openai.yaml`
- `tests/test_review_contract.py`
- `tests/test_foundation.py`
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`

## Write Scope
- `tests/test_review_contract.py`
- `tests/test_ship_contract.py`
- `tests/test_foundation.py`
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`
- `.gitignore`

## Objective
Make the fifth skill discoverable and prove the complete Ship contract with
deterministic repository tests. Update product and harness documentation so a
fresh session understands the final post-review closeout without resurrecting
the AbsolutPowers ceremony or adding remote side effects.

## Tasks

### Task 1: Add deterministic Review and Ship contract coverage
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** yes
**Produces:** Contract test suite covering Ship and the Review fingerprint handoff
**Consumes:** Completed Review/Ship contracts and skills from Phases 1–3

**Create:**
- `tests/test_ship_contract.py`

**Modify:**
- `tests/test_review_contract.py`
- `tests/test_foundation.py`

**Description:**
Extend the existing text-contract test style to make every Ship acceptance
criterion grep-verifiable. Tests must stay deterministic: inspect Markdown,
YAML, JSON, and pure fixture data only; never invoke a model, mutate a real
repository, activate a plugin, or contact a remote service.

**Requirements:**
- Add Review assertions for the exact path manifest/fingerprint fields and Ship handoff while preserving existing Review AC coverage.
- Add Ship tests for preconditions, Feature Record/HTML fields, archive-relative safe links, normalized traversal/escape rejection, prospective frozen-tree target existence, every unsafe URL scheme, escaped/redacted untrusted content, preview approval, memory decisions, and Execution Map consolidation.
- Add pure fingerprint fixtures covering canonical ordering, raw path bytes, present/deleted entries, Git modes/content hashes, scope drift, and final freshness refusal.
- Add transaction fixtures covering complete journal fields, per-operation output hashes/paths, journal state transitions, operation hashes, lock metadata/stale ownership, final fingerprint immediately before tree freeze, post-commit drift, commit intent/interrupted finalization, expected-parent ref, conditional index restoration, rollback conflicts, and no-remote commands. Assert the exact commit-subject regex `^(feat|fix|refactor|docs|test|chore|perf)(\([a-z0-9][a-z0-9-]*\))?!?: [^\r\n]+$` with accepted and rejected fixtures (shown as the canonical regex, not a doubly escaped string literal).
- Update foundation discovery and metadata assertions for `skills/ship/SKILL.md`, `skills/ship/agents/openai.yaml`, and the `.ship-txn/` ignore rule; include literal `AC-1` through `AC-15` in test names/docstrings.

**Tests:**
- `test_ship_validation_AC1_AC2_AC3_AC7_AC9_AC10_AC11` covers eligibility, preview binding, freshness, collisions, and dirty-scope refusal.
- `test_ship_feature_record_AC2_AC4_AC14` covers immutable intent, outcomes, deviations, verification, review, ADRs, memory, follow-ups, and map consolidation.
- `test_ship_executive_summary_AC5_AC6_AC15` covers self-contained HTML, local links, no excerpts, escaping, and redaction.
- `test_ship_transaction_recovery_AC7_AC8_AC10_AC11_AC12_AC13` covers approval, memory choices, journaling, commit finalization, lock/index/ref safety, and conflict-safe rollback.
- `test_ship_disallows_remote_effects_AC8_AC15` covers explicit-only local closeout and forbidden push/PR/deploy actions.

**Implementation decisions / remarks:**
- Added deterministic text-contract coverage for the Review fingerprint
  handoff, Ship lifecycle, rendering safety, local-only boundaries, and pure
  fingerprint/journal/commit-subject fixtures.

### Task 2: Update product documentation for implemented Ship
**Status:** completed
**Traces to:** AC-1, AC-2, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (product documentation and ignore configuration)
**Produces:** Product, repository, skill-index, and ignore documentation that describes the implemented Ship closeout
**Consumes:** Ship contract tests and skill paths from Task 1

**Modify:**
- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`
- `.gitignore`

**Description:**
Replace the planned-status language with the implemented Ship behavior while
keeping canonical schemas in `references/artifact-contracts.md`. Document the
human Executive Summary purpose, post-review freshness, explicit approval,
memory routing, local transaction/recovery, and no-remote boundaries.

**Requirements:**
- Mark Ship implemented in README, CLAUDE, product vision, and skills index; list its explicit native Claude/Codex command and artifact outputs.
- Describe Feature Record and Executive Summary contents, final post-review generation, path-only review order, and no code excerpts or external assets.
- Describe one approval gate, per-item memory promotion, archive cleanup, journal/recovery, local commit, and no push/PR/merge/deploy/history rewrite.
- Preserve the separate Phase 6 `debug`/`tech-debt` scope, no SessionStart hook, explicit-only core, and non-overlapping AbsolutPowers guidance.
- Add `.ship-txn/` to `.gitignore` without ignoring archive outputs or active feature artifacts.

**Tests:**
- `test_product_docs_ship_AC1_AC2_AC4_AC5_AC6_AC7_AC8_AC9_AC10_AC12_AC13_AC14_AC15` checks product docs expose the implemented closeout without duplicate schema.

**Implementation decisions / remarks:**
- Marked Ship as implemented across product and skill documentation, including
  native commands, transactional recovery, and no-remote boundaries.

## Phase Verification
Run:
- `python3 -m unittest tests.test_review_contract tests.test_foundation tests.test_ship_contract`
- `git diff --check`

## Completion Criteria
- Both tasks are completed and only the declared Write Scope changed.
- Every AC-1 through AC-15 has a token-bearing deterministic test and the focused suite passes.
- Documentation reflects implemented Ship behavior and preserves Phase 6 boundaries.
- `.ship-txn/` is ignored while durable archives remain tracked.
- `implementation-context.md` records test and documentation coverage.

## Implementation Decisions / Remarks
- Focused deterministic tests cover every AC token through `AC-15`; canonical
  schemas remain linked rather than duplicated in product documentation.
