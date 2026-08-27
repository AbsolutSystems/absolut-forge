# Tasks: Phase 1 — Product foundation

## Status
in-progress

## Source

- Source doc: `absolutforge/features/absolutforge-mvp/planning-phase-1-foundation.md`
- Epic context: `absolutforge/features/absolutforge-mvp/planning-main.md`

## Mode
orchestrated

## Project Context

**Stack:** Markdown contracts, JSON plugin manifests, Python 3 `unittest`, local Claude Code and Codex CLIs.

**Global Constraints:**

- Keep one host-agnostic `skills/{name}/SKILL.md` tree for every current and future harness.
- Create no hooks, MCP servers, apps, host-specific skill copies, or discoverable incomplete `SKILL.md` files.
- Plugin identifier is `absolutforge`, pilot version is `0.1.0`, and author is `Absolut Systems`.
- The repository root is the plugin root; repo-local marketplace entries use `source.path: "."`.
- Do not install or enable AbsolutForge during this phase while AbsolutPowers remains enabled.
- Exact operational schemas have one canonical reference owner; Product Vision keeps semantics and links rather than duplicate templates.

**Verification commands:**

- JSON: `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`
- Tests: `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- Claude manifest: `claude plugin validate --strict .`
- Codex manifest, when PyYAML is available: `python3 /Users/kamil/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .`

**Shared implementation context:** `absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation/implementation-context.md`

## Phase Overview

### Phase 1: Create manifests and extensible repository layout
**Status:** completed
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation/01-manifests-and-layout.md`
**Depends on:** none
**Write scope:** `.codex-plugin/**`, `.claude-plugin/**`, `.agents/plugins/**`, `skills/README.md`, `agents/README.md`, `.gitignore`
**Risk:** low

### Phase 2: Establish canonical contracts and ADRs
**Status:** in-progress
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation/02-contracts-and-adrs.md`
**Depends on:** Phase 1
**Write scope:** `references/**`, `docs/adr/**`
**Risk:** low

### Phase 3: Wire repository context and product documentation
**Status:** pending
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation/03-context-and-documentation.md`
**Depends on:** Phase 2
**Write scope:** `README.md`, `CLAUDE.md`, `docs/product-vision.md`, `absolutforge/project-memory.md`, `absolutforge/features/absolutforge-mvp/planning-main.md`, `absolutforge/features/absolutforge-mvp/planning-phase-1-foundation.md`
**Risk:** low

### Phase 4: Add deterministic foundation validation
**Status:** pending
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation/04-foundation-validation.md`
**Depends on:** Phases 1-3
**Write scope:** `tests/**`, foundation files when a validator exposes a defect
**Risk:** low

## Final Verification
**Status:** pending
**File:** `absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation/99-final-verification.md`

## Orchestrator Notes

- The orchestrator owns statuses in this file.
- Workers own only their phase file, their declared Write Scope, and `implementation-context.md`.
- Do not mark a phase completed until focused verification and phase review pass.
- Do not install or enable either plugin as part of verification.
