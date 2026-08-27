# Phase 4: Integrate documentation and foundation validation

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
- Canonical consultation contracts and ADR from Phase 1.
- Implemented `skills/discuss/SKILL.md`, `skills/discuss/agents/openai.yaml`, and passing discuss contract tests from Phase 2.
- Implemented `skills/consult/SKILL.md`, `skills/consult/agents/openai.yaml`, and passing consult contract tests from Phase 3.

### Provides (for later phases)
- Repository entry points and Product Vision documenting seven MVP skills and optional consultation.
- Foundation discovery tests aligned with active `discuss` and `consult` skills.
- Recorded integrated Phase 2 verification commands and results.

## Read Scope

- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`
- `skills/discuss/SKILL.md`
- `skills/discuss/agents/openai.yaml`
- `skills/consult/SKILL.md`
- `skills/consult/agents/openai.yaml`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `docs/adr/2026-08-27-optional-cross-model-brief-consultation.md`
- `tests/test_foundation.py`
- `tests/test_discuss_contract.py`
- `tests/test_consult_contract.py`

## Write Scope

- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `skills/README.md`
- `tests/test_foundation.py`
- `absolutforge/features/absolutforge-mvp/planning-main.md`
- `absolutforge/features/absolutforge-mvp/planning-phase-2-discuss.md`
- `absolutforge/features/absolutforge-mvp/tasks-phase-2-discuss/implementation-context.md`

## Objective

Expose the implemented skills through consistent repository documentation and
replace foundation assertions that intentionally forbade runnable skills in
Phase 1. Verify shared-tree discovery, explicit activation, canonical links,
optional consultation, and the absence of global or classic-pipeline behavior.

## Tasks

### Task 1: Update product and repository documentation
**Status:** pending
**Traces to:** AC-1, AC-4, AC-5, AC-6, AC-15
**Test-first:** no (documentation synchronization)
**Produces:** documented seven-skill inventory and optional-consultation workflow
**Consumes:** explicit-only host-agnostic `skills/discuss/SKILL.md` and explicit-only host-agnostic `skills/consult/SKILL.md`

**Requirements:**

- Update `README.md` and `docs/product-vision.md` to list `consult` as a seventh explicit-only optional skill while preserving `discuss -> build -> review -> ship` as the normal core workflow.
- Document adaptive Draft persistence, readiness-frontier discovery, one acceptance gate, and the Claude↔Codex consultation use case without copying complete skill bodies or artifact templates.
- Update `CLAUDE.md` binding constraints so `consult` cannot become implicit, mandatory, artifact-producing, or able to rewrite Ready intent.
- Update `skills/README.md` from reserved Phase 1 language to the current implemented/planned inventory and single-source rule.
- Link the optional-consultation ADR and canonical references from the relevant Product Vision section.

**Tests:**

- `test_product_docs_describe_discuss_AC1_AC4` contains `[AC-1] [AC-4]` and verifies the adaptive flow and one acceptance gate.
- `test_product_docs_describe_optional_consult_AC5_AC6` contains `[AC-5] [AC-6]` and verifies optional second-model consultation.
- `test_product_docs_keep_explicit_core_AC15` contains `[AC-15]` and verifies the normal flow remains direct.

### Task 2: Update shared-tree foundation validation
**Status:** pending
**Traces to:** AC-12, AC-13, AC-15
**Test-first:** yes
**Produces:** Phase 2-compatible `tests.test_foundation.FoundationContractTests`
**Consumes:** documented seven-skill inventory and optional-consultation workflow from Task 1

**Requirements:**

- Replace the Phase 1 assertion that no `SKILL.md` exists with exact discovery of `skills/discuss/SKILL.md` and `skills/consult/SKILL.md`, while continuing to reject host-specific skill trees.
- Preserve assertions that no hooks, MCP servers, apps, registered agents, Pi, or Grok integrations exist.
- Assert both skill files link canonical artifact/handoff owners, their frontmatter names match their directories, Claude disables model invocation, and both Codex policies disable implicit invocation.
- Add document assertions for explicit-only activation, untrusted-content/secret boundaries, and optional consultation without duplicating focused contract tests.

**Tests:**

- `test_shared_skill_tree_AC2` continues to pass with exactly the two implemented skills.
- `test_active_skills_are_explicit_and_safe_AC12_AC13_AC15` contains `[AC-12] [AC-13] [AC-15]`.
- `python3 -m unittest tests.test_foundation` exits zero.

### Task 3: Run integrated Phase 2 verification
**Status:** pending
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (verification execution)
**Produces:** integrated Phase 2 verification evidence in `implementation-context.md`
**Consumes:** `tests.test_foundation.FoundationContractTests` from Task 2

**Requirements:**

- Run the complete standard-library unittest suite and require exact `AC-1` through `AC-15` tokens to be present and all tests to pass.
- Parse every tracked/untracked JSON descriptor and run strict Claude plugin validation.
- Preflight PyYAML and run the canonical Codex validator only when available; otherwise record the non-mutating skip without installing dependencies.
- Verify `AGENTS.md` remains the symlink mirror of `CLAUDE.md`, both new skills have valid frontmatter, and no forbidden hook/global integration was introduced.
- Record exact results and skipped checks in `implementation-context.md`; do not install or activate a plugin.

**Tests:**

- `python3 -m unittest discover -s tests -t . -p 'test_*.py'` exits zero.
- Discuss references pass for `test_complete_brief_without_task_recipe_AC1` `[AC-1]`, `test_evidence_inference_and_user_decisions_AC2` `[AC-2]`, `test_readiness_frontier_AC3` `[AC-3]`, `test_single_acceptance_and_build_handoff_AC4` `[AC-4]`, `test_adaptive_draft_persistence_AC7` `[AC-7]`, `test_resume_rechecks_stale_evidence_AC8` `[AC-8]`, and `test_invalid_path_and_slug_collision_AC9` `[AC-9]`.
- Consult references pass for `test_material_finding_batch_AC5` `[AC-5]`, `test_explicit_approval_mutation_AC6` `[AC-6]`, `test_building_and_review_states_stop_AC10` `[AC-10]`, `test_no_findings_and_deduplication_AC11` `[AC-11]`, `test_untrusted_content_and_secret_redaction_AC12_AC13` `[AC-12] [AC-13]`, `test_ready_changes_use_amendments_AC14` `[AC-14]`, and `test_optional_explicit_only_AC15` `[AC-15]`.
- JSON and strict Claude validators exit zero; Codex validator passes or has the documented PyYAML skip.

## Phase Verification

Run:

- `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`
- `claude plugin validate --strict .`
- `test -L AGENTS.md && test "$(readlink AGENTS.md)" = "CLAUDE.md"`
- `for f in skills/discuss/SKILL.md skills/consult/SKILL.md; do test "$(head -n 1 "$f")" = "---"; done`

## Completion Criteria

- All three tasks are completed.
- All changes remain inside Write Scope.
- Documentation and tests agree on seven MVP skills and optional consultation.
- All 15 ACs have deterministic token-bearing coverage.
- Integrated validation passes or records only the planned PyYAML skip.
- Context Contract provides are fulfilled and recorded in `implementation-context.md`.

## Implementation Decisions / Remarks
- To be completed after phase completion.
