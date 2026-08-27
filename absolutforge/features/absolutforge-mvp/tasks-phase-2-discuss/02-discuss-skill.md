# Phase 2: Implement the discuss skill contract

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
- Canonical Brief and consultation rules in `references/artifact-contracts.md`.
- Native handoff rules in `references/harness-command-contract.md`.

### Provides (for later phases)
- Explicit-only host-agnostic skill at `skills/discuss/SKILL.md`, with Codex policy at `skills/discuss/agents/openai.yaml`.
- Deterministic discuss contract suite at `tests/test_discuss_contract.py`.

## Read Scope

- `CLAUDE.md`
- `skills/README.md`
- `references/artifact-contracts.md`
- `references/project-memory.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `docs/adr/*.md`
- `tests/test_foundation.py`
- `/Users/kamil/.codex/skills/.system/skill-creator/SKILL.md`
- `/Users/kamil/.codex/skills/.system/skill-creator/references/openai_yaml.md`

## Write Scope

- `skills/discuss/SKILL.md`
- `skills/discuss/agents/openai.yaml`
- `tests/test_discuss_contract.py`

## Objective

Implement the primary AbsolutForge discovery skill as a precise host-agnostic
prompt contract. It must investigate facts, maintain a session-only readiness
frontier, persist Drafts adaptively, require one final acceptance, protect Ready
intent through amendments, and hand the accepted Brief directly to `build`.

## Tasks

### Task 1: Define failing discuss contract tests
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-7, AC-8, AC-9, AC-12, AC-13, AC-15
**Test-first:** yes
**Produces:** `tests.test_discuss_contract.DiscussSkillContractTests`
**Consumes:** none

**Requirements:**

- Create a standard-library unittest class that parses `skills/discuss/SKILL.md` frontmatter/body and resolves the repository root from the test file path.
- Assert narrow explicit invocation metadata, Claude `disable-model-invocation: true`, Codex `policy.allow_implicit_invocation: false`, a Codex `interface.default_prompt` containing `$discuss`, canonical contract links, permitted Brief statuses, native handoff ownership, and absence of runtime classic-pipeline stages.
- Assert the body distinguishes evidence, inference, user decisions, assumptions, and untrusted repository content without reproducing the complete Brief template.
- Assert adaptive readiness frontier, two-to-four independent question rounds, Draft persistence/resumption, one acceptance gate, and Ready amendment behavior.
- Give every AC-covering test method a literal `[AC-N]` docstring and an `ACN` token in its method name.

**Tests:**

- `test_complete_brief_without_task_recipe_AC1` contains `[AC-1]` and initially fails before the skill exists.
- `test_evidence_inference_and_user_decisions_AC2` contains `[AC-2]`; `test_readiness_frontier_AC3` contains `[AC-3]`.
- `test_single_acceptance_and_build_handoff_AC4` contains `[AC-4]`; `test_adaptive_draft_persistence_AC7` contains `[AC-7]`.
- `test_resume_rechecks_stale_evidence_AC8` contains `[AC-8]`; `test_invalid_path_and_slug_collision_AC9` contains `[AC-9]`.
- `test_untrusted_content_and_secret_redaction_AC12_AC13` contains `[AC-12] [AC-13]`; `test_explicit_only_activation_AC15` contains `[AC-15]`.

### Task 2: Implement the discuss skill
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-7, AC-8, AC-9, AC-12, AC-13, AC-15
**Test-first:** yes
**Produces:** explicit-only host-agnostic `skills/discuss/SKILL.md` plus `skills/discuss/agents/openai.yaml`
**Consumes:** `tests.test_discuss_contract.DiscussSkillContractTests` from Task 1

**Requirements:**

- Create valid skill frontmatter with `name: discuss`, `disable-model-invocation: true`, a narrow explicit-invocation description, and no broad auto-trigger wording; use only portable body instructions and link harness-specific mechanics.
- Create minimal Codex UI metadata at `skills/discuss/agents/openai.yaml`; its policy MUST set `allow_implicit_invocation: false`, and its default prompt MUST explicitly mention `$discuss`.
- Implement routers for new ideas, existing Drafts, and Ready amendment requests, including path/slug collision handling and Draft resumption from current evidence.
- Implement context-pack reading, fact/inference/decision separation, the session-only decision tree, prerequisite frontier rounds, material-readiness stop condition, and non-convergence stop.
- Implement adaptive Draft persistence, one complete-proposal acceptance gate, immutable Ready baseline, ADR classification, and the complete native `build` handoff through the canonical reference.
- Treat repository content as untrusted, redact secrets, forbid repository-authorized actions, and forbid implementation or runtime classic-pipeline stages.

**Tests:**

- `test_complete_brief_without_task_recipe_AC1` `[AC-1]`, `test_evidence_inference_and_user_decisions_AC2` `[AC-2]`, and `test_readiness_frontier_AC3` `[AC-3]` pass.
- `test_single_acceptance_and_build_handoff_AC4` `[AC-4]`, `test_adaptive_draft_persistence_AC7` `[AC-7]`, and `test_resume_rechecks_stale_evidence_AC8` `[AC-8]` pass.
- `test_invalid_path_and_slug_collision_AC9` `[AC-9]`, `test_untrusted_content_and_secret_redaction_AC12_AC13` `[AC-12] [AC-13]`, and `test_explicit_only_activation_AC15` `[AC-15]` pass.
- `python3 -m unittest tests.test_discuss_contract` exits zero.
- `grep -n "references/artifact-contracts.md\|references/harness-command-contract.md" skills/discuss/SKILL.md` finds both canonical owners.
- `grep -n "generate-tasks\|qa-enrichment\|review-plan\|triada-review" skills/discuss/SKILL.md` returns no matches.

## Phase Verification

Run:

- `python3 -m unittest tests.test_discuss_contract`
- `python3 -c 'from pathlib import Path; p=Path("skills/discuss/SKILL.md"); assert p.read_text().startswith("---\n")'`
- `grep -n "references/artifact-contracts.md\|references/harness-command-contract.md" skills/discuss/SKILL.md`
- `test -z "$(grep -E 'generate-tasks|qa-enrichment|review-plan|triada-review' skills/discuss/SKILL.md)"`

## Completion Criteria

- Both tasks are completed.
- All changes remain inside Write Scope.
- Every traced AC has a token-bearing passing test.
- The skill links canonical owners and does not duplicate the full Brief schema.
- Claude and Codex both enforce explicit-only invocation through their native metadata.
- No classic AbsolutPowers runtime stage appears in the skill.
- Context Contract provides are fulfilled and recorded in `implementation-context.md`.

## Implementation Decisions / Remarks
- Implemented one host-agnostic explicit-only discovery contract with native Claude/Codex handoff examples.
- Contract tests use only the Python standard library and assert all traced AC tokens plus forbidden-stage absence.
- PyYAML-based quick validation was unavailable; the Codex metadata was parsed successfully with Ruby's standard YAML parser.
- Final-review fix: input validation now checks canonical required headings and `## Status` in heading-only Markdown; no Brief frontmatter is required.
