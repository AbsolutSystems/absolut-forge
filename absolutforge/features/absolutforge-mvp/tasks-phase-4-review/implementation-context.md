# Implementation Context: Phase 4 — Review

## Purpose
Short handoff for phase workers. Keep only durable facts needed by later phases.

## Completed Phases
- Phase 1: canonical Review schema and accepted independent-review ADR.
- Phase 2: native Claude/Codex handoffs, fresh generic reviewer mappings, and
  explicit-only Codex Review metadata.
- Phase 3: explicit-only shared Review orchestration in `skills/review/SKILL.md`.
- Phase 4: deterministic Review contract tests, four-skill foundation coverage,
  and product/contributor documentation updates.

## Created / Changed API
- Review contract now defines stable `F-NNN` IDs, append-only pass history,
  `open|fixed|accepted|deferred` resolutions, and current-worktree scope.
- Native Review accepts repository-relative Brief/review paths, derives the
  change from `base_commit` through the current worktree, and returns blockers
  through the native Build form only.
- The primary Review context validates canonical inputs and owns `review.md` /
  lifecycle writes; one fresh generic reviewer is read-only and must inspect
  `base_commit` through the current worktree itself. The fallback is explicitly
  `advisory (not fully isolated)`.

## Decisions Made
- One generic fresh reviewer; no automatic triada or named reviewer registry.
- Findings are only `BLOCKING` or `FOLLOW-UP`; follow-ups default to accepted.
- Review stays on the active configured model and never inherits Build
  Recommendation metadata. Invalid/malicious reviewer output is rejected;
  reviewers never own source or lifecycle mutation.

## Test Utilities / Fixtures
- Existing static `unittest` helpers in `tests/test_foundation.py` and phase tests.

## Constraints For Next Phases
- Review compares `base_commit` to the current worktree and redacts secrets.
- Review artifacts/process files and unrelated dirty changes stay outside scope.
- Phase 2 creates `skills/review/agents/openai.yaml`; Phase 4 must extend the
  foundation skill-directory allowlist before `tests.test_foundation` can pass.
- The primary Review context owns artifact normalization and lifecycle changes;
  Claude `Agent`/Codex `spawn_agent` reviewers are fresh, generic, and read-only.
- Review uses the active configured model and never inherits Build Recommendation.
- The new Review skill handles invalid base revisions and inseparable unrelated
  dirty worktree state as input blockers, scans changed files for introduced
  TODOs/hacks, requests narrow verification when evidence is stale, and
  escalates after two failed attempts per blocker or material scope expansion.
- Phase 4 verification: full static suite passed (56 tests); `git diff --check`
  passed. Review contract test was kept static and model-independent.

## Verification History
- Phase 1: `python3 -m unittest tests.test_foundation` (13 passed); diff check clean.
- Phase 2: `python3 -m unittest tests.test_discuss_contract
  tests.test_consult_contract` (24 passed); phase-specific static contract
  assertions passed; `git diff --check` passed. The earlier foundation suite
  exposed its later-owned skill-directory allowlist gap for Phase 4 to resolve.
- Phase 3: `tests/test_review_contract.py` was not yet present (Phase 4 owns
  it), so targeted static contract validation passed; `git diff --check`
  passed.
