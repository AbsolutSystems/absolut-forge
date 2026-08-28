# Implementation Context: Phase 3 — Build

## Purpose
Short handoff for phase workers. Add only durable facts needed by later phases.

## Completed Phases
- Phase 1 — Canonical Build Contracts and Harness References (commits `6158228..ddd084f`; review clean, phase verification passed).
- Phase 2 — Autonomous Build Skill (commits `df9260f..9b19c92`; review clean, focused verification passed).
- Phase 3 — Build contract tests and product documentation (commits `7325efd..f48ff85`; review clean, full verification passed).

## Created / Changed API
- `references/artifact-contracts.md` now owns the Execution Map and append-only Build Evidence contracts, including `base_commit`, checkpoints, failure boundaries, scout/documentation, compaction, and no-deployment rules.
- `references/harness-command-contract.md` defines complete native build/review paths, durable resume, and whole-feature `base_commit..HEAD` review handoff.
- `references/codex-tools.md` maps Build to Luna `xhigh`, bounded redacted read-only Sol diagnostics, and capability-detected compaction after durable persistence.
- `skills/build/SKILL.md` implements explicit-only, host-agnostic Build and requires whole-feature verification before native review.
- `skills/build/agents/openai.yaml` exposes `$build` with `policy.allow_implicit_invocation: false` and no deployment capability.

## Decisions Made
- ADR-004 defines outcome-oriented execution, checkpoints, and boundary-first escalation.
- ADR-005 defines the whole Feature Brief as the only delivery unit; build never deploys.

## Test Utilities / Fixtures
- Existing tests are deterministic `unittest` contract scanners; no model calls.

## Constraints For Next Phases
- Preserve canonical schemas in `references/`; do not duplicate them in skill prose.
- Keep build explicit-only and compatible with both Claude Code and Codex.
- Phase 3 updated the deterministic active-skill allowlist for the new `build` skill; the full-suite integration verification passed.

## Verification History
- Planning validation: 35 existing tests passed; plan QA enrichment and review-plan both PASS.
- Phase 3: `python3 -m unittest discover -s tests -t . -p 'test_*.py'` — 46 tests passed; `git diff --check` — passed.

## Phase 3 Handoff
- Contract entry point: `tests/test_build_contract.py` (static checks for AC-1 through AC-15).
- Foundation integration: `tests/test_foundation.py` includes the explicit-only `build` skill.
- Product references: `README.md`, `CLAUDE.md`, `docs/product-vision.md`, and `skills/README.md` describe the implemented Build workflow and link canonical contracts/ADRs.
