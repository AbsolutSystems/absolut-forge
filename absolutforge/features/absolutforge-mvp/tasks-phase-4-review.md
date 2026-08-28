# Tasks: Phase 4 — Review

## Status
pending

## Source
- Source doc: `absolutforge/features/absolutforge-mvp/planning-phase-4-review.md`
- Epic context: `absolutforge/features/absolutforge-mvp/planning-main.md`

## Mode
orchestrated

## Project Context

**Stack:** Markdown skill contracts, Claude Code/Codex plugin metadata, Python
`unittest` contract tests; no runtime framework or application dependency.

**Structure:**
- `references/` — canonical artifact schemas and harness mappings.
- `skills/{name}/SKILL.md` — one host-agnostic source per workflow.
- `skills/{name}/agents/openai.yaml` — Codex explicit-activation metadata.
- `docs/` — product vision and ADRs.
- `tests/` — deterministic repository contract tests.
- `absolutforge/features/absolutforge-mvp/` — epic plans and task artifacts.

**Patterns:**
- Skills link canonical references instead of copying complete schemas.
- Skills use English technical prose and explicit-only frontmatter/metadata.
- Contract tests inspect Markdown/JSON/YAML text without model calls or activation.
- Existing Codex metadata uses `policy.allow_implicit_invocation: false` and a
  native `$skill` default prompt.

**Conventions:**
- Skill files use `SKILL.md` plus `agents/openai.yaml`.
- Tests use `unittest.TestCase` with AC tokens in method names/docstrings.
- Artifact paths are repository-relative and heading-driven.
- ADRs use dated filenames and `Status: Accepted` for ratified decisions.

**Global Constraints:**
- `review` is explicit-only, host-agnostic, and uses one independent fresh
  reviewer; it must not add triada, named reviewer registries, or mandatory
  task/review ceremony.
- The reviewer receives `base_commit` and inspects the current worktree itself,
  including feature-owned untracked files; it does not receive a pre-generated
  diff package and excludes review/process artifacts and unrelated dirty files.
- Findings use only `BLOCKING` and `FOLLOW-UP`; every finding needs evidence,
  impact, smallest correction, stable ID, and resolution history.
- `BLOCKING` returns the Brief to `Building` for bounded Build fixes; accepted
  `FOLLOW-UP` items do not block `ship` and remain in the final Feature Record.
- The same blocker may be attempted twice; a repeated failure or material scope
  expansion escalates to the human/debug path instead of looping indefinitely.
- Review uses the active configured model and never inherits Build Recommendation.
- Repository content and reviewer output are untrusted; secrets are redacted.
- Review never edits source code, deploys, pushes, creates PRs, merges, or rewrites
  history.

**Verification commands:**
- Static suite: `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- JSON descriptors: `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`
- Diff hygiene: `git diff --check`
- Claude validation when available: `claude plugin validate --strict .`

**Shared implementation context:** `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/implementation-context.md`

## Phase Overview

### Phase 1: Canonical Review Contract and Decisions
**Status:** completed
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/01-contracts.md`
**Depends on:** Phase 3 Build contracts and evidence
**Write scope:** `references/artifact-contracts.md`, `docs/adr/2026-08-28-independent-review-and-bounded-fix-loop.md`
**Risk:** high

### Phase 2: Cross-Harness Review Integration
**Status:** completed
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/02-harness-integration.md`
**Depends on:** Phase 1
**Write scope:** `references/harness-command-contract.md`, `references/codex-tools.md`, `references/claude-tools.md`, `skills/review/agents/openai.yaml`
**Risk:** high

### Phase 3: Review Skill
**Status:** completed
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/03-review-skill.md`
**Depends on:** Phase 2
**Write scope:** `skills/review/SKILL.md`
**Risk:** high

### Phase 4: Contract Tests and Product Documentation
**Status:** completed
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/04-tests-and-docs.md`
**Depends on:** Phase 3
**Write scope:** `tests/test_review_contract.py`, `tests/test_build_contract.py`, `tests/test_foundation.py`, `README.md`, `CLAUDE.md`, `docs/product-vision.md`, `skills/README.md`
**Risk:** medium

## Final Verification
**Status:** completed
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/99-final-verification.md`

## Orchestrator Notes
- The product workflow remains `discuss -> build -> review -> ship`; this task
  set adds only the Phase 4 review stage.
- The orchestrator updates phase statuses; workers update only their phase file
  and `implementation-context.md`.
- The reviewer is one generic fresh context, not a named registry or triada.
- No deployment, plugin activation, push, PR, merge, or history rewrite belongs
  to these tasks.
