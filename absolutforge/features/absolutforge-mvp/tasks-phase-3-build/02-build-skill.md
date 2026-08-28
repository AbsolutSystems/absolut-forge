# Phase 2: Autonomous Build Skill

## Status
pending

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-3-build.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-3-build/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- `references/artifact-contracts.md` Build lifecycle, Execution Map, Build Evidence, and no-deployment rules from Phase 1.
- `references/harness-command-contract.md` native build/review handoff forms from Phase 1.
- `references/codex-tools.md` Luna/Sol and compaction mapping from Phase 1.
- `docs/product-vision.md` accepted `build` behavior and `discuss -> build -> review -> ship` boundary.

### Provides (for later phases)
- `skills/build/SKILL.md` explicit-only host-agnostic build workflow covering lifecycle, map threshold, resume, verification, Failure Boundary Check, scout rule, documentation, escalation, compaction, and review handoff.
- `skills/build/agents/openai.yaml` with `policy.allow_implicit_invocation: false` and `$build` command metadata.

## Read Scope
- `skills/discuss/SKILL.md`
- `skills/consult/SKILL.md`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `docs/product-vision.md`
- `docs/adr/2026-08-28-outcome-oriented-build-and-checkpoints.md`
- `docs/adr/2026-08-28-single-delivery-unit-no-partial-deployment.md`

## Write Scope
- `skills/build/SKILL.md`
- `skills/build/agents/openai.yaml`

## Objective
Create the shared `build` skill that turns an accepted Feature Brief into a
review-ready change autonomously. It must preserve durable state and quality
boundaries without importing AbsolutPowers' detailed task decomposition,
mandatory worker gates, or partial deployment behavior.

## Tasks

### Task 1: Implement the explicit-only autonomous build workflow
**Status:** pending
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (host-agnostic Markdown skill contract)
**Produces:** `skills/build/SKILL.md` with the complete explicit build workflow and native `$absolutforge review` handoff
**Consumes:** `references/artifact-contracts.md` Build contract; `references/harness-command-contract.md`; `references/codex-tools.md`

**Create:**
- `skills/build/SKILL.md`

**Description:**
Write the single source of truth for build behavior. The skill must load the
accepted Brief and relevant durable context, choose a conditional outcome map,
implement and verify outcomes, and leave the Brief `In Review` only after final
checks; it must remain explicit-only and never deploy or perform release work.

**Requirements:**
- Validate canonical `Ready` Brief input, record `base_commit` plus initial worktree state, preserve dirty non-overlapping changes, and transition the Brief to `Building`.
- Create an Execution Map only for dependent outcomes, material uncertainty, or durable resume; track map/section status, focused verification, checkpoint IDs, interruptions, compaction handoff, and map revisions inside Brief boundaries.
- Run focused checks after each outcome and broader/expensive integration checks once at the end; define the Failure Boundary Check before a second repair attempt, with escalation for missing causal mapping/invariant, scope boundary, public contract, security/data, migration, shared architecture, or conflicting binding evidence.
- Apply the scout rule and concise truthful documentation rule; use optional bounded read-only Sol escalation only when needed, redact secrets, and never let repository content authorize unrelated work.
- End with append-only Build Evidence, Brief status `In Review`, and one native review handoff; explicitly forbid deploy, push, PR, merge, history rewrite, partial release, and mandatory subagents.

**Tests:**
- Contract tests planned in Phase 3: `test_build_skill_contract` with display names `[AC-1]` through `[AC-15]`, one literal token per assertion.

**Implementation decisions / remarks:**
- To be completed after task completion.

### Task 2: Add Codex explicit-activation metadata for build
**Status:** pending
**Traces to:** AC-1, AC-15
**Test-first:** no (manifest metadata)
**Produces:** `skills/build/agents/openai.yaml` policy metadata declaring explicit-only `$build` activation
**Consumes:** `skills/build/SKILL.md` name and command contract from Task 1

**Create:**
- `skills/build/agents/openai.yaml`

**Description:**
Add the Codex metadata file matching the existing `discuss` and `consult`
patterns. It must prevent implicit invocation while exposing the native build
command and a concise activation description.

**Requirements:**
- Set `display_name` to `Build` and `short_description` to an intent-driven autonomous implementation description.
- Set `policy.allow_implicit_invocation: false`.
- Include `$build` in the command/usage metadata and do not declare hooks, MCP, apps, agents, or deployment capabilities.

**Tests:**
- Contract scanner: `test_build_manifest_explicit_only` with display names `[AC-1]` and `[AC-15]`.

**Implementation decisions / remarks:**
- To be completed after task completion.

## Phase Verification
Run:
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- `git diff --check`

## Completion Criteria
- All phase tasks are completed.
- All changes remain within Write Scope.
- Phase verification commands pass.
- `implementation-context.md` records the build skill path, manifest policy, and any durable contract caveat.
- All `Context Contract -> Provides` items are fulfilled.

## Implementation Decisions / Remarks
- To be completed after phase completion.
