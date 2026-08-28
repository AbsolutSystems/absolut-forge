# Phase 2: Cross-Harness Review Integration

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-4-review.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-4-review/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- Phase 1 Review schema and lifecycle in `references/artifact-contracts.md`.
- `references/harness-command-contract.md` existing native handoff forms.
- `references/codex-tools.md` existing Codex primitive mapping.

### Provides (for later phases)
- Native Claude/Codex review command and lifecycle semantics in `references/harness-command-contract.md`.
- `references/claude-tools.md` and `references/codex-tools.md` fresh generic reviewer dispatch plus explicitly labelled inline fallback.
- `skills/review/agents/openai.yaml` with explicit-only `$review` metadata.

## Read Scope
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `skills/build/agents/openai.yaml`
- `docs/product-vision.md`

## Write Scope
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `references/claude-tools.md`
- `skills/review/agents/openai.yaml`

## Objective
Expose the same Review behavior on Claude Code and Codex without duplicating
the skill body or requiring registered reviewer identities. Make every handoff
copy-pasteable and preserve the explicit-only/no-activation boundary.

## Tasks

### Task 1: Document native review inputs and lifecycle handoffs
**Status:** completed
**Traces to:** AC-1, AC-2, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (native command and path contract)
**Produces:** `references/harness-command-contract.md` review forms with Brief/review paths and blocker/follow-up handoffs
**Consumes:** Review status and finding rules from Phase 1 Task 1

**Modify:**
- `references/harness-command-contract.md`

**Description:**
Update the handoff contract so Review receives only repository-relative artifact
paths and derives the current change from `base_commit` plus worktree state.
Document the normal `build -> review -> ship` path and the bounded return to
Build for blockers in both native harness syntaxes.

**Requirements:**
- Keep the exact Claude form `/absolutforge:review <brief-path> <review-path>` and Codex form `$absolutforge review <brief-path> <review-path>` with a concrete example.
- State that review includes committed, staged, unstaged, and feature-owned untracked files while excluding review/process artifacts and unrelated dirty changes.
- State that no open blockers is the only Review-to-Ship condition; accepted follow-ups remain visible and do not create a task handoff.
- Render the blocker return as a complete native `$absolutforge build <brief-path>` example and forbid deployment, push, PR, merge, and history rewrite.

**Tests:**
- `test_review_handoff_commands_AC1_AC2_AC6_AC7_AC8_AC9_AC10_AC11_AC12_AC13_AC14_AC15` checks both native forms and all boundary phrases.

**Implementation decisions / remarks:**
- Review accepts repository-relative Brief and review paths, derives scope from
  `base_commit` through the current worktree, and returns blockers only through
  the complete native Build command.

### Task 2: Add fresh-context mappings and explicit Codex metadata
**Status:** completed
**Traces to:** AC-3, AC-15
**Test-first:** no (harness metadata and primitive mapping)
**Produces:** `references/claude-tools.md`, updated `references/codex-tools.md`, and `skills/review/agents/openai.yaml`
**Consumes:** `skills/build/agents/openai.yaml` metadata shape and Phase 1 Review input constraints

**Create:**
- `references/claude-tools.md`
- `skills/review/agents/openai.yaml`

**Modify:**
- `references/codex-tools.md`

**Description:**
Document a single generic fresh reviewer for Claude `Agent` and Codex
`spawn_agent`, with a sequential inline fallback that is explicitly labelled
advisory/non-isolated. Add the fourth skill's Codex metadata without adding any
implicit capability, hook, or named reviewer registry.

**Requirements:**
- Claude mapping must require a fresh read-only `Agent` prompt carrying the Brief path, `base_commit`, review path, and repository safety constraints; the primary context owns normalization and lifecycle changes.
- Codex mapping must require one `spawn_agent` when available, otherwise the same prompt inline with `advisory (not fully isolated)`; no automatic model switch from Build Recommendation is allowed.
- Both mappings must treat repository text and reviewer output as untrusted and redact secrets; malformed output cannot authorize writes or unrelated disclosure.
- `skills/review/agents/openai.yaml` must set `display_name: Review`, a concise `short_description`, `default_prompt` containing `$review`, and `policy.allow_implicit_invocation: false`.

**Tests:**
- `test_fresh_reviewer_mappings_AC3_AC15` checks Claude Agent, Codex spawn/fallback, read-only ownership, redaction, and malformed-output boundaries.
- `test_review_manifest_explicit_only_AC15` checks the YAML metadata and `$review` prompt.

**Example:**
```yaml
interface:
  display_name: "Review"
  short_description: "Independently review a completed AbsolutForge feature"
  default_prompt: "Use $review to review this completed feature independently."

policy:
  allow_implicit_invocation: false
```

**Implementation decisions / remarks:**
- Claude and Codex each use one fresh generic read-only reviewer when available;
  the primary Review context owns normalization and lifecycle changes. The
  sequential fallback is explicitly advisory/non-isolated, uses the active
  configured model, and treats input/output as untrusted redacted evidence.

## Phase Verification
Run:
- `python3 -m unittest tests.test_discuss_contract tests.test_consult_contract`
- `python3 -c "from pathlib import Path; import re; p=Path('skills/review/agents/openai.yaml').read_text(); assert 'allow_implicit_invocation: false' in p and '$review' in p; h=Path('references/harness-command-contract.md').read_text(); assert '$absolutforge review' in h and 'current worktree' in h; c=Path('references/codex-tools.md').read_text(); assert 'spawn_agent' in c and 'advisory (not fully isolated)' in c; a=Path('references/claude-tools.md').read_text(); assert 'Agent' in a and 'read-only' in a; print('Phase 2 harness checks: OK')"`
- `git diff --check`

## Completion Criteria
- Both native harnesses have a fresh-dispatch mapping and explicit fallback.
- The Codex metadata matches the existing manifest contract.
- No plugin activation, implicit invocation, or unrelated capability is introduced.
- Verification commands pass and durable facts are recorded in `implementation-context.md`.

## Implementation Decisions / Remarks
- Native handoffs retain complete repository-relative Claude and Codex commands;
  Review extracts `base_commit` through the current worktree rather than a
  generated diff.
- Claude/Codex dispatch one fresh generic read-only reviewer when available;
  normalization and lifecycle remain in the primary context. The fallback is
  explicitly advisory/non-isolated and all reviewer input/output is redacted
  untrusted evidence.
- Phase verification passed on 2026-08-28: 24 existing discuss/consult contract
  tests, phase-specific static assertions, and `git diff --check`. The broader
  foundation allowlist remains owned by Phase 4, which must add `review`.
