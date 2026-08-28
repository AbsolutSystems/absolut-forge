# Implementation Context: Phase 3 — Build

## Purpose
Short handoff for phase workers. Add only durable facts needed by later phases.

## Completed Phases
- None yet.

## Created / Changed API
- None yet.

## Decisions Made
- ADR-004 defines outcome-oriented execution, checkpoints, and boundary-first escalation.
- ADR-005 defines the whole Feature Brief as the only delivery unit; build never deploys.

## Test Utilities / Fixtures
- Existing tests are deterministic `unittest` contract scanners; no model calls.

## Constraints For Next Phases
- Preserve canonical schemas in `references/`; do not duplicate them in skill prose.
- Keep build explicit-only and compatible with both Claude Code and Codex.

## Verification History
- Planning validation: 35 existing tests passed; plan QA enrichment and review-plan both PASS.

