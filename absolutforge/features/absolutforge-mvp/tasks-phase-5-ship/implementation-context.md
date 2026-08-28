# Implementation Context: Phase 5 — Ship

## Purpose
Short handoff for phase workers. Keep this file concise. Add only facts that future phases need.

## Completed Phases
- None yet.

## Created / Changed API
- `references/artifact-contracts.md` now defines Ship preconditions, Review-owned
  source manifest/fingerprint validation, archive outputs, and recovery contract.

## Decisions Made
- ADR `2026-08-28-ship-post-review-closeout.md` binds post-review rendering to
  the Review fingerprint and local transactional closeout.

## Test Utilities / Fixtures
- Existing tests are text-contract checks using `unittest.TestCase`; no model or repository mutation is required.

## Constraints For Next Phases
- Preserve explicit-only activation, no remote side effects, and the exact artifact contracts.
- Review must record the canonical raw-byte manifest and SHA-256 fingerprint;
  Ship validates it before rendering, after approval, and before freezing commit state.
- Ship's transaction journal is `.ship-txn/{txid}/journal.json`; only approved
  memory items and paths participate, with explicit recovery on failure.

## Verification History
- Phase 1 implementation completed after planning and task-review gates passed.
- `python3 -m unittest tests.test_review_contract` and `git diff --check` passed for Phase 1; source changes are committed as `ee9cf67`.
