# Phase 3: Wire repository context and product documentation

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation.md`

## Shared Context

Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation/implementation-context.md`
- `references/artifact-contracts.md`
- `references/project-memory.md`
- `references/harness-command-contract.md`

## Context Contract

### Requires (from previous phases)
- Canonical references and accepted ADRs produced by Phase 2.

### Provides (for later phases)
- Fresh-session read order and binding constraints in `CLAUDE.md`/`AGENTS.md`.
- Public product overview and private-pilot validation/install boundary in `README.md`.
- Product Vision linked to canonical references without duplicated exact templates.
- Seeded project-memory source of truth.

## Read Scope

- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `absolutforge/features/absolutforge-mvp/planning-main.md`
- `absolutforge/features/absolutforge-mvp/planning-phase-1-foundation.md`
- `references/**`
- `docs/adr/**`

## Write Scope

- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `absolutforge/project-memory.md`
- `absolutforge/features/absolutforge-mvp/planning-main.md`
- `absolutforge/features/absolutforge-mvp/planning-phase-1-foundation.md`

## Objective

Make every fresh Claude or Codex session find the same product truth and operational contracts without loading a global workflow. Remove duplicate exact schemas from Product Vision while preserving the accepted product semantics and provide clear private-pilot validation and isolation guidance.

## Tasks

### Task 1: Refactor Product Vision to canonical references
**Status:** completed
**Traces to:** AC-3
**Test-first:** no (documentation source-of-truth refactor)
**Produces:** Product Vision with stable semantic contracts and canonical reference links
**Consumes:** artifact and memory contracts from Phase 2

**Requirements:**

- Replace exact artifact and memory templates with concise semantic invariants plus direct canonical reference paths.
- Preserve every accepted workflow behavior, stopping condition, review exclusion, and ship boundary from the current Product Vision.
- Link both Phase 1 ADRs from the relevant architectural decisions.
- Keep known implementation-level questions explicitly deferred.

**Tests:**

- `test_context_entrypoints_AC3` with `[AC-3]` evidence will require the canonical links.
- Manual diff review confirms no accepted behavioral invariant was removed.

### Task 2: Complete repository entry points and memory seed
**Status:** completed
**Traces to:** AC-3, AC-4, AC-12
**Test-first:** no (repository documentation and empty memory seed)
**Produces:** README validation guide, fresh-session bootstrap, and `absolutforge/project-memory.md`
**Consumes:** Product Vision links from Task 1 and harness contracts from Phase 2

**Requirements:**

- Update README with architecture, private-pilot status, non-mutating validation commands, and explicit note that activation is deferred.
- Update CLAUDE development context to require Product Vision, epic main, phase plan, canonical references, and relevant ADRs in that order.
- Seed project memory with its path, allowed statuses, an empty-state marker, and a link to the canonical memory contract.
- Document that AbsolutPowers must be disabled before any later AbsolutForge activation.
- Preserve `AGENTS.md` as the symlink mirror of `CLAUDE.md`.

**Tests:**

- `test_context_entrypoints_AC3` with `[AC-3]` evidence will verify all entry points.
- `test_non_mutating_validation_AC4` with `[AC-4]` evidence will verify documented commands do not install or enable.
- `test_concurrent_workflow_warning_AC12` with `[AC-12]` evidence will verify the isolation warning.

## Phase Verification

Run:

- `test -L AGENTS.md`
- `test "$(readlink AGENTS.md)" = "CLAUDE.md"`
- `grep -n "references/artifact-contracts.md\|references/project-memory.md\|references/harness-command-contract.md" README.md CLAUDE.md docs/product-vision.md`
- `grep -n "AbsolutPowers" README.md CLAUDE.md references/codex-tools.md`

## Completion Criteria

- Both tasks are completed.
- All changes remain inside Write Scope.
- A fresh session has an unambiguous read order.
- Product Vision retains semantic authority while exact schemas have canonical reference owners.
- Context Contract provides are fulfilled and recorded in `implementation-context.md`.

## Implementation Decisions / Remarks
- Product Vision retains behavioral contracts and links exact artifact and memory
  schemas to their canonical references.
- README and CLAUDE.md now document the same fresh-session read order, private-
  pilot non-mutating validation boundary, and AbsolutPowers isolation rule.
- Seeded `absolutforge/project-memory.md` as an empty canonical store with
  allowed statuses and an explicit-approval promotion boundary.
