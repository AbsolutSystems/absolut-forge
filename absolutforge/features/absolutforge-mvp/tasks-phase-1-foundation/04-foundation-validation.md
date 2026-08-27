# Phase 4: Add deterministic foundation validation

## Status
pending

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation.md`

## Shared Context

Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation/implementation-context.md`
- `absolutforge/features/absolutforge-mvp/planning-phase-1-foundation.md`

## Context Contract

### Requires (from previous phases)
- Complete descriptors and layout from Phase 1.
- Canonical references and ADRs from Phase 2.
- Updated repository context and documentation from Phase 3.

### Provides (for later phases)
- Deterministic foundation conformance suite in `tests/test_foundation.py`.
- Recorded JSON, unit-test, Claude-validation, and conditional Codex-validator results.

## Read Scope

- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`
- `skills/**`
- `agents/**`
- `references/**`
- `docs/**`
- `README.md`
- `CLAUDE.md`
- `AGENTS.md`

## Write Scope

- `tests/test_foundation.py`
- Any Phase 1 foundation file when a failing validator demonstrates a defect
- `absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation/implementation-context.md`

## Objective

Create and run a deterministic conformance suite for every Phase 1 acceptance criterion. Validate both plugin descriptors without installing or enabling either workflow and record a transparent fallback if the optional Codex canonical validator cannot run because PyYAML is unavailable.

## Tasks

### Task 1: Create the foundation conformance suite
**Status:** pending
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12
**Test-first:** no (conformance tests assert completed declarative scaffold)
**Produces:** `tests.test_foundation.FoundationContractTests`
**Consumes:** all Phase 1 descriptors, contracts, ADRs, and documentation

**Requirements:**

- Use only Python standard library modules and resolve the repository root from the test file path.
- Create explicit test methods named `test_manifest_identity_AC1`, `test_shared_skill_tree_AC2`, `test_context_entrypoints_AC3`, `test_non_mutating_validation_AC4`, `test_private_metadata_optional_AC5`, `test_marketplace_root_AC6`, `test_no_discoverable_stubs_AC7`, `test_manifest_drift_rejected_AC8`, `test_no_implicit_capabilities_AC9_AC10_AC11`, and `test_concurrent_workflow_warning_AC12`; give each method a docstring containing its literal `[AC-N]` token or tokens.
- Parse every JSON descriptor and assert exact name, version, author, marketplace policy, and root source values.
- Reject hooks, MCP/apps, host-specific skill trees, runnable skills, registered agents, and missing context/ADR links.
- Confirm AGENTS is a symlink to CLAUDE and all validation commands documented for Phase 1 are non-mutating.

**Tests:**

- Every named test method has a docstring embedding its traced literal `[AC-N]` token.
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'` exits zero.

### Task 2: Run canonical and harness validation
**Status:** pending
**Traces to:** AC-4, AC-8, AC-11
**Test-first:** no (verification execution)
**Produces:** recorded validation results in implementation context
**Consumes:** `tests.test_foundation.FoundationContractTests` from Task 1

**Requirements:**

- Parse every tracked and untracked repository JSON file with `python3 -m json.tool`.
- Run the complete Python foundation suite and fix only demonstrated Phase 1 defects.
- Run `claude plugin validate --strict .` and record its exit status.
- Preflight `python3 -c 'import yaml'`; if successful, run the canonical plugin-creator validator, otherwise record `skipped: PyYAML unavailable` without installing a dependency.
- Do not run any plugin marketplace add, plugin add, enable, disable, install, or remove command.

**Tests:**

- `test_non_mutating_validation_AC4` with `[AC-4]` evidence remains green after the documented command set.
- `test_manifest_drift_rejected_AC8` with `[AC-8]` evidence remains green for the final descriptors.
- `test_no_implicit_capabilities_AC9_AC10_AC11` with `[AC-11]` evidence remains green after strict validation.

## Phase Verification

Run:

- `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- `claude plugin validate --strict .`
- `python3 -c 'import yaml'`
- When the import succeeds: `python3 /Users/kamil/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .`

## Completion Criteria

- Both tasks are completed.
- All changes remain inside Write Scope or are explicit validator-driven fixes to Phase 1 files.
- Deterministic tests and strict Claude validation pass.
- The canonical Codex validator passes or its PyYAML skip is explicitly recorded.
- No install or activation command ran.
- Context Contract provides are fulfilled and recorded in `implementation-context.md`.

## Implementation Decisions / Remarks
- To be completed after phase completion.
