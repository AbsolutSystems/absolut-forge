# Phase 1: Canonical Recommendation Contract and Harness Mapping

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
- `references/codex-tools.md`

## Context Contract

### Requires (from existing product)
- Existing Feature Brief, Amendment, Execution Map, and Build Evidence schemas.
- Existing native Claude/Codex build handoff and Codex Luna/Sol routing.

### Provides (for later phases)
- Canonical optional `## Build Recommendation` schema, field vocabulary, model mapping, and placement outside the immutable intent baseline.
- Native handoff and Codex guidance for preserving advisory recommendation, fallback, and override evidence.

## Read Scope
- `absolutforge/features/build-model-recommendation/planning-build-model-recommendation.md`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `docs/adr/2026-08-27-explicit-activation-without-hooks.md`
- `docs/adr/2026-08-27-host-agnostic-skill-tree.md`

## Write Scope
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`

## Objective
Define one cross-harness artifact contract for a durable, advisory Build model
recommendation without turning execution metadata into immutable product intent.

## Tasks

### Task 1: Add the canonical Build Recommendation schema
**Status:** pending
**Traces to:** AC-1, AC-2, AC-3, AC-5, AC-6, AC-7, AC-8, AC-11
**Test-first:** no (canonical Markdown contract)
**Produces:** `references/artifact-contracts.md` `## Build Recommendation contract` with placement, fields, allowed values, mapping, fallback, and override semantics
**Consumes:** Existing Feature Brief and Build Evidence contracts in `references/artifact-contracts.md`

**Modify:**
- `references/artifact-contracts.md`

**Description:**
Add the optional section after `## Expected outcomes` and before `## Open
questions`. Define `Complexity`, `Execution shape`, `Claude model`, `Codex
model`, `Rationale`, `Confidence`, and `Override` fields. State that the
section is execution metadata, not part of the immutable baseline, and that
older Briefs may omit it.

**Requirements:**
- Define exactly two valid profiles: `simple/single` → Sonnet and `gpt-5.6-luna`; `complex/phased` → Opus and `gpt-5.6-terra`.
- Require concise evidence-based rationale and confidence while forbidding line/file-count-only classification.
- Specify that absent or malformed recommendations do not invalidate a Brief and that Build records fallback without changing intent.
- Specify that an explicit user/model override is allowed with a reason and is not a product amendment or deployment authorization.

**Tests:**
- Phase 3 `test_build_recommendation_schema` with display tokens `[AC-1] [AC-2] [AC-3] [AC-5] [AC-6] [AC-7] [AC-8] [AC-11]` scans the canonical headings, values, baseline boundary, fallback, and override wording.

**Implementation decisions / remarks:**
- To be completed after task completion.

### Task 2: Extend native handoff and Codex routing
**Status:** pending
**Traces to:** AC-1, AC-4, AC-5, AC-6, AC-7, AC-8, AC-11
**Test-first:** no (harness documentation)
**Produces:** Recommendation-preserving Claude/Codex handoff and Codex model-tier/fallback mapping in canonical references
**Consumes:** `## Build Recommendation contract` from Task 1

**Modify:**
- `references/harness-command-contract.md`
- `references/codex-tools.md`

**Description:**
Document that the recommendation travels with the Brief into Build, remains
advisory, and is reflected in Build Evidence when followed, overridden, or
unavailable. Keep actual model availability and user choice authoritative.

**Requirements:**
- Map Claude `sonnet`/`opus` and Codex `gpt-5.6-luna`/`gpt-5.6-terra` consistently with the canonical profiles.
- State that handoff does not trigger automatic model switching or provider configuration.
- State that fallback/override reasons are durable evidence and that the complete Feature Brief remains the sole delivery unit.

**Tests:**
- Phase 3 `test_model_recommendation_handoff` with display tokens `[AC-1] [AC-4] [AC-5] [AC-6] [AC-7] [AC-8] [AC-11]` checks both references and native command examples.

**Implementation decisions / remarks:**
- To be completed after task completion.

## Phase Verification
Run:
- `git diff --check`

## Completion Criteria
- Both tasks are completed within Write Scope.
- Canonical fields and model mappings are internally consistent.
- Handoff and Codex references consume the canonical contract without duplicating a conflicting schema.
- Phase verification passes.

## Implementation Decisions / Remarks
- To be completed after phase completion.
