# Implementation Context: Phase 5 — Ship

## Purpose
Short handoff for phase workers. Keep this file concise. Add only facts that future phases need.

## Completed Phases
- Phases 1–3 provide the canonical Ship contract, Review freshness handoff, and
  explicit-only Ship skill.
- Phase 4 adds deterministic Review/Ship contract coverage and implemented
  product/skill documentation.

## Created / Changed API
- `references/artifact-contracts.md` now defines Ship preconditions, Review-owned
  source manifest/fingerprint validation, archive outputs, and recovery contract.
- `skills/review/SKILL.md` records the final reviewed-path manifest and canonical SHA-256 fingerprint for Ship freshness validation.
- Claude and Codex harness references provide explicit-only, local Review-to-Ship handoffs with matching Brief and Review paths.
- `skills/ship/SKILL.md` implements the explicit-only local Ship closeout and
  `skills/ship/agents/openai.yaml` exposes it to Codex without implicit activation.

## Decisions Made
- ADR `2026-08-28-ship-post-review-closeout.md` binds post-review rendering to
  the Review fingerprint and local transactional closeout.

## Test Utilities / Fixtures
- Existing tests are text-contract checks using `unittest.TestCase`; no model or repository mutation is required.
- `tests/test_ship_contract.py` uses pure raw-byte fingerprint and journal
  fixtures; run its focused suite with Review and foundation coverage.

## Constraints For Next Phases
- Preserve explicit-only activation, no remote side effects, and the exact artifact contracts.
- Review must record the canonical raw-byte manifest and SHA-256 fingerprint;
  Ship validates it before rendering, after approval, and before freezing commit state.
- Ship's transaction journal is `.ship-txn/{txid}/journal.json`; only approved
  memory items and paths participate, with explicit recovery on failure.

## Verification History
- Phase 1 implementation completed after planning and task-review gates passed.
- `python3 -m unittest tests.test_review_contract` and `git diff --check` passed for Phase 1; source changes are committed as `ee9cf67`.
- Phase 3: `python3 -m unittest tests.test_review_contract` and `git diff --check` passed.
- Phase 4: `python3 -m unittest tests.test_review_contract tests.test_foundation tests.test_ship_contract` and `git diff --check` passed.
