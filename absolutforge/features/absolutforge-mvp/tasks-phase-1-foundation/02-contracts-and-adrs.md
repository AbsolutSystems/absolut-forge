# Phase 2: Establish canonical contracts and ADRs

## Status
pending

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation.md`

## Shared Context

Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation/implementation-context.md`
- `docs/product-vision.md`

## Context Contract

### Requires (from previous phases)
- Root `skills/` and `agents/` layout produced by Phase 1.

### Provides (for later phases)
- Canonical artifact schemas in `references/artifact-contracts.md`.
- Canonical memory routing and promotion schema in `references/project-memory.md`.
- Native harness handoff rules and Codex primitive mapping.
- Accepted ADRs for the single skill tree and hook-free explicit activation.

## Read Scope

- `docs/product-vision.md`
- `CLAUDE.md`
- `README.md`
- `/Users/kamil/Projekty/absolut-ai-skills/references/harness-command-contract.md`
- `/Users/kamil/Projekty/absolut-ai-skills/references/project-memory.md`
- `/Users/kamil/Projekty/absolut-ai-skills/references/codex-tools.md`

## Write Scope

- `references/artifact-contracts.md`
- `references/project-memory.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `docs/adr/2026-08-27-host-agnostic-skill-tree.md`
- `docs/adr/2026-08-27-explicit-activation-without-hooks.md`

## Objective

Create the exact shared contracts later skills will consume and record the two architectural decisions that make future harness additions cheap without reintroducing global workflow injection.

## Tasks

### Task 1: Extract canonical delivery artifact contracts
**Status:** pending
**Traces to:** AC-3, AC-7
**Test-first:** no (normative Markdown schemas)
**Produces:** canonical Feature Brief, amendment, Execution Map, review, Feature Record, and Executive Summary contracts
**Consumes:** none (`docs/product-vision.md` is binding read-only source context, not an earlier task output)

**Requirements:**

- Define exact active and archived paths, status values, ownership, and lifecycle transitions.
- Include complete templates for Feature Brief, amendment, Execution Map, review findings, and Feature Record.
- Specify that accepted intent is immutable and that transient maps are not archived.
- Specify the human-facing Executive Summary content and self-contained requirement without choosing a rendering implementation.

**Tests:**

- `test_context_entrypoints_AC3` with `[AC-3]` evidence will require the canonical artifact reference.
- `test_no_discoverable_stubs_AC7` with `[AC-7]` evidence will distinguish documentation examples from runnable skills.

### Task 2: Define memory and harness handoff contracts
**Status:** pending
**Traces to:** AC-2, AC-3, AC-12
**Test-first:** no (normative Markdown contracts)
**Produces:** canonical project-memory routing, native command contract, and Codex tool mapping
**Consumes:** plugin namespace and shared-tree decision from Phase 1

**Requirements:**

- Define global versus package-local memory routing, active/superseded states, candidate capture, and explicit promotion approval.
- Define native explicit commands for Claude `/absolutforge:{skill}` and Codex `$absolutforge {skill}` with complete path/argument handoffs.
- Document Codex generic fresh-agent dispatch versus inline fallback without defining a required review agent.
- Document local plugin enable/disable facts and the prohibition on concurrent AbsolutPowers/AbsolutForge activation without changing user configuration.

**Tests:**

- `test_shared_skill_tree_AC2` with `[AC-2]` evidence will require harness mappings to point at shared skills.
- `test_context_entrypoints_AC3` with `[AC-3]` evidence will require both contracts.
- `test_concurrent_workflow_warning_AC12` with `[AC-12]` evidence will require the isolation warning and disable guidance.

### Task 3: Record cross-harness and activation ADRs
**Status:** pending
**Traces to:** AC-2, AC-9, AC-10, AC-11
**Test-first:** no (architecture decision records)
**Produces:** two accepted ADRs linked to the product vision and Phase 1 plan
**Consumes:** contracts from Tasks 1-2

**Requirements:**

- Record the decision, alternatives, consequences, and future-harness procedure for one host-agnostic skill tree.
- Record explicit-only core activation, the narrowly auto-triggered `debug`, and absence of SessionStart hooks.
- State that Pi/Grok require new thin integrations and optional tool references, with zero existing skill edits.
- Link each ADR to Product Vision and the Phase 1 planning document.

**Tests:**

- `test_shared_skill_tree_AC2` with `[AC-2]` evidence will require the cross-harness ADR.
- `test_no_implicit_capabilities_AC9_AC10_AC11` with `[AC-9] [AC-10] [AC-11]` evidence will require the activation ADR.

## Phase Verification

Run:

- `test -s references/artifact-contracts.md`
- `test -s references/project-memory.md`
- `test -s references/harness-command-contract.md`
- `test -s references/codex-tools.md`
- `test -s docs/adr/2026-08-27-host-agnostic-skill-tree.md`
- `test -s docs/adr/2026-08-27-explicit-activation-without-hooks.md`

## Completion Criteria

- All three tasks are completed.
- All changes remain inside Write Scope.
- Exact schemas have one declared canonical owner.
- Both ADRs have accepted status, alternatives, consequences, and related links.
- Context Contract provides are fulfilled and recorded in `implementation-context.md`.

## Implementation Decisions / Remarks
- To be completed after phase completion.
