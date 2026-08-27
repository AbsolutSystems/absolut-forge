# Implementation Context: Phase 2 — Discuss and optional consultation

## Purpose
Concise durable handoff between Phase 2 workers. Add only facts needed by later phases.

## Completed Phases
- None yet.

## Created / Changed API
- None yet.

## Decisions Made
- `consult` is explicit-only and optional; the normal workflow remains `discuss -> build`.
- Ready intent changes only through accepted amendments; consultation creates no durable report.

## Test Utilities / Fixtures
- Existing standard-library unittest conventions live in `tests/test_foundation.py`.

## Constraints For Next Phases
- Skills must remain in the shared `skills/` tree and link canonical contracts rather than copy full schemas.
- No hooks, MCP, apps, registered agents, Pi/Grok integrations, plugin activation, or dependency installation.

## Verification History
- None yet.
