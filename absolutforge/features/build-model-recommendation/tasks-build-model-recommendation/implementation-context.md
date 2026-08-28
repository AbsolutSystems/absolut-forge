# Implementation Context: Build model recommendation

## Purpose
Short handoff for the phase workers; canonical schemas remain in `references/`.

## Completed Phases
- Phase 1: canonical recommendation contract and harness mapping completed.

## Created / Changed API
- Implemented: optional `## Build Recommendation` after `## Expected outcomes`, outside immutable intent baseline.
- Implemented mapping: `simple/single` → Sonnet + `gpt-5.6-luna`; `complex/phased` → Opus + `gpt-5.6-terra`.

## Decisions Made
- Recommendation is advisory, overridable, and recorded with fallback/override reason in Build Evidence; no automatic model switching.
- Older Briefs without the section remain valid and use configured Build defaults.

## Test Utilities / Fixtures
- Existing static scanners: `tests/test_discuss_contract.py` and `tests/test_build_contract.py`.

## Constraints For Next Phases
- Preserve explicit-only activation, immutable intent, no partial delivery, untrusted-content handling, and secret redaction.
- Keep model recommendation outside product intent and avoid line/file-count-only classification.

## Verification History
- Phase 1: `git diff --check` passed.
