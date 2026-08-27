# Phase 1: Extend canonical contracts and record consultation ADR

## Status
pending

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-2-discuss.md`

## Shared Context

Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-2-discuss/implementation-context.md`
- `absolutforge/features/absolutforge-mvp/planning-phase-2-discuss.md`

## Context Contract

### Requires (from previous phases)
- Phase 1 foundation contract at `references/artifact-contracts.md`.
- Phase 1 native command contract at `references/harness-command-contract.md`.

### Provides (for later phases)
- Canonical optional-consultation behavior in `references/artifact-contracts.md` for `Draft`, `Ready`, no-findings, and no-artifact outcomes.
- Native Claude and Codex `consult` invocation in `references/harness-command-contract.md`.
- Accepted ADR `docs/adr/2026-08-27-optional-cross-model-brief-consultation.md`.

## Read Scope

- `docs/product-vision.md`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `docs/adr/2026-08-27-host-agnostic-skill-tree.md`
- `docs/adr/2026-08-27-explicit-activation-without-hooks.md`
- `absolutforge/features/absolutforge-mvp/planning-phase-2-discuss.md`

## Write Scope

- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `docs/adr/2026-08-27-optional-cross-model-brief-consultation.md`

## Objective

Extend the canonical contracts before either skill is written so both skill
bodies consume one stable consultation and command boundary. Record why a fresh
second opinion is optional, human-controlled, and represented directly in a
Draft or amendment instead of a new persistent report.

## Tasks

### Task 1: Extend consultation and native handoff contracts
**Status:** pending
**Traces to:** none (canonical contract infrastructure consumed by behavior tasks)
**Test-first:** no (normative Markdown contract update)
**Produces:** canonical `consult` behavior and native invocation contracts
**Consumes:** none

**Requirements:**

- Add an optional-consultation section to `references/artifact-contracts.md` covering accepted inputs `Draft | Ready`, focused finding shape, explicit approval, Draft merge, Ready amendment, `no material findings`, deduplication, and no consultation artifact.
- State that `Building | In Review` inputs are not mutated and material intent changes return to `discuss` for amendments.
- Add complete `/absolutforge:consult absolutforge/features/{slug}/feature-brief.md` and `$absolutforge consult absolutforge/features/{slug}/feature-brief.md` command forms to `references/harness-command-contract.md`.
- Preserve `discuss -> build -> review -> ship` as the normal workflow and label `consult` optional and explicit-only.

**Tests:**

- Contract inspection confirms both native command forms and the exact Brief path.
- Contract inspection confirms no persistent consultation artifact or mandatory gate is introduced.

### Task 2: Record the optional cross-model consultation ADR
**Status:** pending
**Traces to:** none (architecture record for the accepted workflow decision)
**Test-first:** no (architecture documentation)
**Produces:** accepted ADR `docs/adr/2026-08-27-optional-cross-model-brief-consultation.md`
**Consumes:** canonical `consult` behavior and native invocation contracts from Task 1

**Requirements:**

- Record context, decision, alternatives, consequences, and related links using the established ADR structure.
- State that consultation may run in Claude after Codex or in Codex after Claude without recording model identity in the Brief.
- Reject mandatory consultation, automatic invocation, embedding consultation inside `discuss`, and a persistent consultation report.
- Preserve explicit human approval and immutable Ready intent as hard consequences.

**Tests:**

- ADR inspection confirms `Accepted` status and links to Product Vision, Phase 2 planning, artifact contracts, and handoff contracts.
- ADR inspection confirms optionality and human-controlled mutation.

## Phase Verification

Run:

- `grep -n "consult" references/artifact-contracts.md references/harness-command-contract.md docs/adr/2026-08-27-optional-cross-model-brief-consultation.md`
- `grep -n "Draft\|Ready\|Building\|In Review\|no material findings" references/artifact-contracts.md`
- `grep -n "/absolutforge:consult\|\$absolutforge consult" references/harness-command-contract.md`

## Completion Criteria

- Both tasks are completed.
- All changes remain inside Write Scope.
- Consultation behavior has one canonical owner and both native commands are complete.
- The ADR is accepted and records every material rejected alternative.
- Context Contract provides are fulfilled and recorded in `implementation-context.md`.

## Implementation Decisions / Remarks
- To be completed after phase completion.
