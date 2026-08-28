# Phase 2: Discuss and Build Integration

## Status
pending

## Parent
`absolutforge/features/build-model-recommendation/tasks-build-model-recommendation.md`

## Shared Context
Read before starting:
- `absolutforge/features/build-model-recommendation/planning-build-model-recommendation.md`
- `absolutforge/features/build-model-recommendation/tasks-build-model-recommendation/implementation-context.md`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `skills/discuss/SKILL.md`
- `skills/build/SKILL.md`

## Context Contract

### Requires (from Phase 1)
- Canonical Build Recommendation contract and model mapping.
- Native handoff and Codex fallback/override semantics.

### Provides (for later phases)
- `discuss` final proposal behavior that produces one advisory profile from settled evidence.
- `build` behavior that consumes, validates, overrides, and records the recommendation without rewriting intent.

## Read Scope
- `absolutforge/features/build-model-recommendation/planning-build-model-recommendation.md`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `skills/discuss/SKILL.md`
- `skills/build/SKILL.md`
- `tests/test_discuss_contract.py`
- `tests/test_build_contract.py`

## Write Scope
- `skills/discuss/SKILL.md`
- `skills/build/SKILL.md`

## Objective
Wire the recommendation into the two runtime skill contracts while preserving
explicit activation, autonomous Build ownership, and the existing lifecycle.

## Tasks

### Task 1: Produce the recommendation from Discuss
**Status:** pending
**Traces to:** AC-1, AC-2, AC-3, AC-9, AC-10, AC-11
**Test-first:** no (host-agnostic Markdown skill contract)
**Produces:** `skills/discuss/SKILL.md` final Brief proposal instructions for `## Build Recommendation`
**Consumes:** Canonical recommendation schema from Phase 1

**Modify:**
- `skills/discuss/SKILL.md`

**Description:**
Extend the final proposal step so `discuss` emits one optional Build
Recommendation with complexity, execution shape, both harness model names,
rationale, confidence, and explicit override wording. The profile must derive
from outcome coupling, uncertainty, and risk evidence in the settled frontier.

**Requirements:**
- Recommend `simple/single` with Sonnet/Luna only for one cohesive low-risk outcome.
- Recommend `complex/phased` with Opus/Terra for dependent outcomes, material uncertainty, public/security/data/migration boundaries, shared architecture, or durable phased execution.
- Explicitly prohibit classification based only on line count or file count and keep the recommendation outside immutable intent.
- Preserve one acceptance gate, explicit-only activation, and the native build handoff.

**Tests:**
- Phase 3 `test_build_recommendation_output` with display tokens `[AC-1] [AC-2] [AC-3] [AC-9] [AC-10] [AC-11]` checks recommendation fields, profile rules, evidence basis, and safety boundaries.

**Implementation decisions / remarks:**
- To be completed after task completion.

### Task 2: Consume the recommendation in Build
**Status:** pending
**Traces to:** AC-4, AC-5, AC-6, AC-7, AC-8, AC-11
**Test-first:** no (host-agnostic Markdown skill contract)
**Produces:** `skills/build/SKILL.md` advisory recommendation consumption, fallback, override, and Build Evidence rules
**Consumes:** Canonical recommendation and handoff contracts from Phase 1

**Modify:**
- `skills/build/SKILL.md`

**Description:**
Add a context-loading step that reads the optional recommendation and treats it
as an execution hint. Build must keep the active harness/model authoritative,
record actual profile/fallback/override evidence, and leave accepted intent
unchanged.

**Requirements:**
- Use the recommended profile when available and compatible, without invoking or switching models automatically.
- For missing, malformed, or unavailable recommendations, use the configured default and record the reason in Build Evidence.
- For an explicit override, record the chosen profile and reason; do not require a product amendment or review gate.
- If later evidence raises risk, preserve the Brief and apply existing amendment and Failure Boundary rules rather than silently rewriting metadata.
- Preserve no-deployment, no-partial-delivery, secret-redaction, and explicit-only boundaries.

**Tests:**
- Phase 3 `test_build_recommendation_consumption` with display tokens `[AC-4] [AC-5] [AC-6] [AC-7] [AC-8] [AC-11]` checks advisory use, fallback, override, intent preservation, and delivery boundaries.

**Implementation decisions / remarks:**
- To be completed after task completion.

## Phase Verification
Run:
- `git diff --check`

## Completion Criteria
- Both skill contracts link the canonical recommendation schema.
- Discuss and Build semantics agree on profile values and advisory behavior.
- Existing explicit-only and no-deployment wording remains intact.
- Phase verification passes.

## Implementation Decisions / Remarks
- To be completed after phase completion.
