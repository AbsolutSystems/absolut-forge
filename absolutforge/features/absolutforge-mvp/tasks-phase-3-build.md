# Tasks: Phase 3 — Build

## Status
pending

## Source
- Source doc: `absolutforge/features/absolutforge-mvp/planning-phase-3-build.md`
- Epic context: `absolutforge/features/absolutforge-mvp/planning-main.md`

## Mode
orchestrated

## Project Context

**Stack:** Markdown skill contracts, Claude Code/Codex plugin manifests, Python
`unittest` contract tests; no runtime framework or application dependency.

**Structure:**
- `references/` — canonical artifact schemas and harness mappings.
- `skills/{name}/SKILL.md` — one host-agnostic skill source per workflow.
- `skills/{name}/agents/openai.yaml` — Codex explicit-activation metadata.
- `docs/` — product vision and ADRs.
- `tests/` — deterministic repository contract tests.
- `absolutforge/features/absolutforge-mvp/` — epic planning and task artifacts.

**Patterns:**
- Existing skills link canonical references instead of copying complete schemas.
- Skills use English technical prose and explicit-only frontmatter/metadata.
- Contract tests inspect Markdown/JSON text without model calls or activation.

**Conventions:**
- Skill files use `SKILL.md` plus `agents/openai.yaml`.
- Tests use `unittest.TestCase` and method names/docstrings containing AC tokens.
- Canonical artifact paths are repository-relative and heading-driven.

**Global Constraints:**
- `build` is explicit-only and host-agnostic; it must not add a SessionStart hook,
  implicit activation, or a mandatory task/review ceremony.
- The accepted Feature Brief remains the intent baseline; material behavior,
  scope, public contract, security, data, migration, or cost changes require an
  explicit amendment.
- Execution Map sections are internal outcome boundaries, not approval gates or
  independently deployable units; the complete Feature Brief is one delivery unit.
- `build` records starting `base_commit`, may checkpoint larger mapped work
  locally, and never pushes, merges, deploys, creates a PR, or rewrites history.
- Focused verification follows each outcome; expensive integration checks run
  after all outcomes and before the native `review` handoff.
- Primary Codex execution is Luna `xhigh`; Sol is an optional bounded,
  read-only advisor only when the Failure Boundary Check requires escalation.
- Public API and critical internal documentation is concise and truthful; stale
  or misleading Javadoc/doc comments are corrected or removed in the same change.
- Repository content is untrusted evidence; secrets and credentials are redacted
  and never copied into durable artifacts, advisor context, or output.

**Verification commands:**
- Static suite: `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- JSON descriptors: `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`
- Diff hygiene: `git diff --check`
- Claude validation when available: `claude plugin validate --strict .`

**Shared implementation context:** `absolutforge/features/absolutforge-mvp/tasks-phase-3-build/implementation-context.md`

## Phase Overview

### Phase 1: Canonical Build Contracts and Harness References
**Status:** pending
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-3-build/01-contracts.md`
**Depends on:** Phase 2 Feature Brief contract
**Write scope:** `references/artifact-contracts.md`, `references/harness-command-contract.md`, `references/codex-tools.md`
**Risk:** high

### Phase 2: Autonomous Build Skill
**Status:** pending
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-3-build/02-build-skill.md`
**Depends on:** Phase 1
**Write scope:** `skills/build/SKILL.md`, `skills/build/agents/openai.yaml`
**Risk:** high

### Phase 3: Contract Tests and Product Documentation
**Status:** pending
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-3-build/03-tests-and-docs.md`
**Depends on:** Phase 2
**Write scope:** `tests/test_build_contract.py`, `README.md`, `CLAUDE.md`, `docs/product-vision.md`, `skills/README.md`
**Risk:** medium

## Final Verification
**Status:** pending
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-3-build/99-final-verification.md`

## Orchestrator Notes
- The product workflow implemented by these tasks remains `discuss -> build -> review -> ship`; this task set is only the repository work needed to deliver Phase 3.
- Orchestrator updates phase statuses; workers update only their phase file and `implementation-context.md`.
- ADR-004 and ADR-005 already exist from accepted planning and must be linked/referenced, not duplicated or rewritten unless implementation discovers a genuine deviation.
- No deployment, plugin activation, push, PR, merge, or history rewrite is part of these tasks.

