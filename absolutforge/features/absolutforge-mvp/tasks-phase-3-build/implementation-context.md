# Implementation Context: Phase 3 — Build

## Purpose
Short handoff for phase workers. Add only durable facts needed by later phases.

## Completed Phases
- Phase 1 — Canonical Build Contracts and Harness References (commit `6158228`; phase verification passed).
- Phase 2 — Autonomous Build Skill (commit `9b19c92`; focused verification passed).

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
- Phase 3 must update the deterministic active-skill allowlist for the new `build` skill before full-suite integration verification.

## Verification History
- Planning validation: 35 existing tests passed; plan QA enrichment and review-plan both PASS.
