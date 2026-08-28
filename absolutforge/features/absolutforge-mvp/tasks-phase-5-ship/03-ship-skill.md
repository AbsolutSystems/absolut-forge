# Phase 3: Ship Skill and Codex Metadata

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-5-ship.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-5-ship/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- `references/artifact-contracts.md` canonical Ship input, output, fingerprint, approval, memory, and recovery rules.
- `references/harness-command-contract.md`, `references/claude-tools.md`, and `references/codex-tools.md` native handoffs from Phase 2.
- `skills/review/SKILL.md` Review fingerprint and final handoff from Phase 2.
- `docs/adr/2026-08-28-ship-post-review-closeout.md` accepted transaction decisions.

### Provides (for later phases)
- `skills/ship/SKILL.md` explicit-only host-agnostic Ship orchestrator implementing validation, post-review rendering, approval, memory, archive, recovery, and local commit boundaries.
- `skills/ship/agents/openai.yaml` explicit Codex metadata with implicit invocation disabled.

## Read Scope
- `references/artifact-contracts.md`
- `references/project-memory.md`
- `references/harness-command-contract.md`
- `references/claude-tools.md`
- `references/codex-tools.md`
- `skills/review/SKILL.md`
- `docs/product-vision.md`
- `docs/adr/2026-08-28-ship-post-review-closeout.md`
- `skills/discuss/SKILL.md`
- `skills/build/SKILL.md`

## Write Scope
- `skills/ship/SKILL.md`
- `skills/ship/agents/openai.yaml`

## Objective
Implement the Ship skill as the lightweight final closeout stage. It must read
the final Brief, Review, Build Evidence, map, ADRs, and memory candidates;
render a trustworthy Feature Record and Executive Summary; then execute one
approved, journaled local transaction without introducing another quality gate.

## Tasks

### Task 1: Implement explicit-only Ship closeout orchestration
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (host-agnostic Markdown skill contract)
**Produces:** `skills/ship/SKILL.md` explicit-only Ship workflow with validation, rendering, approval, transaction recovery, and local commit handoff
**Consumes:** Phase 1 canonical Ship contract and Phase 2 Review/harness handoffs

**Create:**
- `skills/ship/SKILL.md`

**Description:**
Write the single shared Ship prompt that owns closeout validation and all
lifecycle mutations while keeping source evidence and generated content
untrusted. The prompt must make the post-review freshness guard, human preview,
memory routing, archive cleanup, transaction journal, and no-remote boundary
executable without a second review or task ceremony.

**Requirements:**
- Validate explicit canonical Brief/Review paths, Brief `In Review`, Review `Complete`, no open `BLOCKING`, final evidence, matching `base_commit`, safe scope, archive collisions, and unrelated dirty/index state before mutation.
- Recompute the Review manifest/fingerprint before render, after approval, and immediately before freezing the commit tree; render the Feature Record and self-contained HTML only from the final state, with required fields, escaped untrusted text, redacted secrets, archive-relative local links, and no source excerpts. Recompute again after commit and route any drift back to Review before closeout.
- Validate the commit subject against `^(feat|fix|refactor|docs|test|chore|perf)(\([a-z0-9][a-z0-9-]*\))?!?: [^\r\n]+$` (one-line subject, no secret or untrusted control text) before it enters the preview and again before commit; reject anything outside this grammar.
- Present one complete preview and approval including exact artifacts/deletions, per-memory candidate choices and destinations, commit message, PR description, and staged paths; reject the preview without mutation and preserve rejected candidates.
- Execute the journaled transaction in the documented order using operation hashes, OS advisory lock, transaction-private index, immutable commit tree, expected-parent ref update, conditional index reconciliation, interrupted-commit finalization, conflict-safe rollback, and terminal `rolled-back` recovery. The journal records `preview_digest`, manifest/fingerprint, approved path set, original bytes/modes/existence, pre-transaction index, promotion decisions, commit message/`commit_intent`, and per-operation output hashes/paths; resume verifies every completed output before continuing.
- Generate archive-relative links exactly as `../../../{repo-relative-path}` from the archive; normalize and reject traversal/escape, missing prospective frozen-tree targets, external/protocol-relative/file/javascript/data/absolute URLs, and render deleted targets as text.
- Emit native Review/Ship handoffs and closeout output with commit ID while explicitly refusing push, PR creation, merge, deployment, history rewrite, prompt-injection authorization, or unrelated scope absorption.

**Tests:**
- `test_ship_skill_validation_AC1_AC2_AC3_AC7_AC9_AC10_AC11` checks preconditions, fingerprint freshness, preview binding, and collision/dirty-input refusal.
- `test_ship_skill_rendering_AC2_AC4_AC5_AC6_AC14_AC15` checks Feature Record fields, self-contained HTML, local links, escaping, redaction, and transient map consolidation.
- `test_ship_skill_transaction_AC7_AC8_AC10_AC11_AC12_AC13` checks approval ordering, per-memory choices, complete journal fields and output hashes, commit intent/finalization, rollback conflicts, lock handling, final fingerprint/post-commit drift, and index/ref safety.
- `test_ship_skill_no_remote_AC8_AC15` checks that no remote side effect is authorized and native handoffs remain explicit-only.

**Implementation decisions / remarks:**
- Links the canonical Ship contract and makes the validation, three fingerprint
  checks, exact preview, journaled local transaction, recovery, and no-remote
  boundaries executable in one host-agnostic prompt.

### Task 2: Add explicit Codex Ship metadata
**Status:** completed
**Traces to:** AC-1, AC-7, AC-8, AC-9, AC-15
**Test-first:** no (Codex metadata configuration)
**Produces:** `skills/ship/agents/openai.yaml` explicit-only `$ship` metadata
**Consumes:** `skills/ship/SKILL.md` from Task 1

**Create:**
- `skills/ship/agents/openai.yaml`

**Description:**
Add the Codex metadata required to expose Ship as an explicit skill while
keeping implicit activation disabled. Match the existing Review/Build metadata
shape and do not add a hook, named agent registry, or remote permission.

**Requirements:**
- Set `interface.display_name`, `interface.short_description`, and a default prompt that invokes `$ship` with the final Brief and Review paths.
- Set `policy.allow_implicit_invocation: false` and expose no capabilities beyond the explicit skill.
- Keep metadata valid YAML and consistent with the host-agnostic `skills/ship/SKILL.md` name.

**Tests:**
- `test_ship_codex_metadata_AC1_AC7_AC8_AC9_AC15` checks the `$ship` prompt, explicit-only policy, and valid metadata keys.

**Implementation decisions / remarks:**
- Uses the established metadata shape with a `$ship` default prompt and
  `allow_implicit_invocation: false`.

## Phase Verification
Run:
- `python3 -m unittest tests.test_review_contract`
- `git diff --check`

## Completion Criteria
- Both tasks are completed and only the declared Write Scope changed.
- Ship is explicit-only, host-agnostic, and implements every canonical transaction boundary.
- Codex metadata is valid and cannot implicitly activate Ship.
- Focused tests and diff hygiene pass.
- `implementation-context.md` records the new skill and metadata paths.

## Implementation Decisions / Remarks
- Ship stays a local closeout stage: no second review gate, no automatic remote
  integration, and no archive mutation before explicit fingerprint-bound approval.
