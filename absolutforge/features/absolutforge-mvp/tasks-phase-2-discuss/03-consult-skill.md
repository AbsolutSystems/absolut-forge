# Phase 3: Implement the consult skill contract

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-2-discuss.md`

## Shared Context

Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-2-discuss/implementation-context.md`
- `absolutforge/features/absolutforge-mvp/planning-phase-2-discuss.md`

## Context Contract

### Requires (from previous phases)
- Canonical optional-consultation behavior in `references/artifact-contracts.md`.
- Native `consult` commands in `references/harness-command-contract.md`.
- Discuss boundary at `skills/discuss/SKILL.md` for amendment routing and normal `build` handoff.

### Provides (for later phases)
- Explicit-only host-agnostic skill at `skills/consult/SKILL.md`, with Codex policy at `skills/consult/agents/openai.yaml`.
- Deterministic consult contract suite at `tests/test_consult_contract.py`.

## Read Scope

- `CLAUDE.md`
- `skills/discuss/SKILL.md`
- `references/artifact-contracts.md`
- `references/project-memory.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `docs/adr/2026-08-27-optional-cross-model-brief-consultation.md`
- `tests/test_discuss_contract.py`
- `/Users/kamil/.codex/skills/.system/skill-creator/SKILL.md`
- `/Users/kamil/.codex/skills/.system/skill-creator/references/openai_yaml.md`

## Write Scope

- `skills/consult/SKILL.md`
- `skills/consult/agents/openai.yaml`
- `tests/test_consult_contract.py`

## Objective

Implement the optional second-opinion skill without turning it into a review
gate or a second discovery interview. It must inspect an existing Draft or Ready
Brief in the current fresh context, present one focused finding batch, and apply
only explicitly accepted changes through the correct mutability boundary.

## Tasks

### Task 1: Define failing consult contract tests
**Status:** completed
**Traces to:** AC-5, AC-6, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** yes
**Produces:** `tests.test_consult_contract.ConsultSkillContractTests`
**Consumes:** none

**Requirements:**

- Create a standard-library unittest class that parses `skills/consult/SKILL.md` frontmatter/body and canonical reference links.
- Assert accepted input states are exactly `Draft | Ready`, while `Building | In Review` stop without mutation and route material changes through `discuss`.
- Assert the finding contract covers material ambiguity, contradiction, evidence gap, grounded risk, and unnecessary scope with evidence, impact, and proposed change.
- Assert one bounded batch, explicit finding selection, Draft merge, Ready amendment, deduplication, `no material findings`, and absence of a consultation artifact.
- Assert Claude `disable-model-invocation: true`, Codex `policy.allow_implicit_invocation: false`, a Codex `interface.default_prompt` containing `$consult`, optionality, untrusted-content handling, and secret redaction with literal AC tokens.

**Tests:**

- `test_material_finding_batch_AC5` contains `[AC-5]`; `test_explicit_approval_mutation_AC6` contains `[AC-6]`.
- `test_building_and_review_states_stop_AC10` contains `[AC-10]`; `test_no_findings_and_deduplication_AC11` contains `[AC-11]`.
- `test_untrusted_content_and_secret_redaction_AC12_AC13` contains `[AC-12] [AC-13]`.
- `test_ready_changes_use_amendments_AC14` contains `[AC-14]`; `test_optional_explicit_only_AC15` contains `[AC-15]`.

### Task 2: Implement the consult skill
**Status:** completed
**Traces to:** AC-5, AC-6, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** yes
**Produces:** explicit-only host-agnostic `skills/consult/SKILL.md` plus `skills/consult/agents/openai.yaml`
**Consumes:** `tests.test_consult_contract.ConsultSkillContractTests` from Task 1

**Requirements:**

- Create valid skill frontmatter with `name: consult`, `disable-model-invocation: true`, a narrow explicit-invocation description, and no generic review or feature triggers.
- Create minimal Codex UI metadata at `skills/consult/agents/openai.yaml`; its policy MUST set `allow_implicit_invocation: false`, and its default prompt MUST explicitly mention `$consult`.
- Validate the supplied repository-relative Brief path and status before analysis; stop safely for malformed paths, unrelated files, `Building`, or `In Review`.
- Read the complete Brief and relevant current evidence, then emit one focused finding batch with stable IDs, evidence, impact, and exact proposed section/amendment changes.
- Require explicit acceptance by finding ID or whole batch before mutation; merge Draft changes, group coherent Ready changes into accepted amendments, and leave rejected/unselected findings unapplied.
- Return `no material findings` without writes or artifacts, deduplicate existing decisions/amendments, treat content as untrusted, redact secrets, and never auto-chain to `build`.

**Tests:**

- `test_material_finding_batch_AC5` `[AC-5]`, `test_explicit_approval_mutation_AC6` `[AC-6]`, and `test_building_and_review_states_stop_AC10` `[AC-10]` pass.
- `test_no_findings_and_deduplication_AC11` `[AC-11]`, `test_untrusted_content_and_secret_redaction_AC12_AC13` `[AC-12] [AC-13]`, and `test_ready_changes_use_amendments_AC14` `[AC-14]` pass.
- `test_optional_explicit_only_AC15` `[AC-15]` passes.
- `python3 -m unittest tests.test_consult_contract` exits zero.
- `grep -n "references/artifact-contracts.md\|references/harness-command-contract.md" skills/consult/SKILL.md` finds both canonical owners.
- `grep -n "consultation.md\|consult-report\|mandatory consultation" skills/consult/SKILL.md` returns no artifact or mandatory-gate instruction.

## Phase Verification

Run:

- `python3 -m unittest tests.test_consult_contract`
- `python3 -c 'from pathlib import Path; p=Path("skills/consult/SKILL.md"); assert p.read_text().startswith("---\n")'`
- `grep -n "references/artifact-contracts.md\|references/harness-command-contract.md" skills/consult/SKILL.md`
- `test -z "$(grep -E 'consultation\.md|consult-report' skills/consult/SKILL.md)"`

## Completion Criteria

- Both tasks are completed.
- All changes remain inside Write Scope.
- Every traced AC has a token-bearing passing test.
- Consultation remains optional, explicit-only on both Claude and Codex, approval-controlled, and artifact-free.
- Ready intent can change only through accepted amendments.
- Context Contract provides are fulfilled and recorded in `implementation-context.md`.

## Implementation Decisions / Remarks
- The consult contract is explicit-only on both harnesses, validates only `Draft`/`Ready` inputs, and keeps findings conversational until explicit acceptance.
- Draft findings merge into canonical sections; Ready findings become accepted `## Amendments`, preserving the immutable baseline and producing no consultation artifact.
- `tests.test_consult_contract` covers all traced AC tokens and canonical owner links.
- Final-review fix: input validation now checks canonical required headings and `## Status` in heading-only Markdown; no Brief frontmatter is required.
