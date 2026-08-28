# Phase 1: Canonical Build Contracts and Harness References

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-3-build.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-3-build/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- `references/artifact-contracts.md` Feature Brief, Amendment, Review, and Feature Record contracts from Phase 1/2.
- `references/harness-command-contract.md` explicit Claude/Codex command and artifact handoff rules.
- `docs/adr/2026-08-28-outcome-oriented-build-and-checkpoints.md` and `docs/adr/2026-08-28-single-delivery-unit-no-partial-deployment.md` accepted decisions.

### Provides (for later phases)
- `references/artifact-contracts.md` sections `## Execution Map contract`, `## Build Evidence contract`, and lifecycle rules for `Building`/`In Review`, map statuses, checkpoints, Failure Boundary Check, scout dispositions, documentation maintenance, and no-deployment.
- `references/harness-command-contract.md` native `$absolutforge build` and `$absolutforge review` handoff forms with complete paths.
- `references/codex-tools.md` explicit Luna/Sol routing, bounded read-only advisor dispatch, and capability-detected compaction guidance.

## Read Scope
- `docs/product-vision.md`
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `docs/adr/2026-08-28-outcome-oriented-build-and-checkpoints.md`
- `docs/adr/2026-08-28-single-delivery-unit-no-partial-deployment.md`

## Write Scope
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `absolutforge/features/absolutforge-mvp/planning-main.md` (orchestrator-only epic lifecycle status)

## Objective
Extend the canonical contracts so a later build skill can implement the accepted
outcome-oriented lifecycle without inventing schemas. Preserve the existing
Feature Brief and Review contracts, add only build-specific fields/rules, and
make model escalation and compaction harness mechanics explicit in Codex mapping.

## Tasks

### Task 1: Extend the canonical Build artifact and lifecycle contract
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (canonical Markdown schema and lifecycle documentation)
**Produces:** `references/artifact-contracts.md` headings `## Execution Map contract` and `## Build Evidence contract` with map/section statuses, base revision, checkpoint, scout, compaction, documentation, failure-boundary, and no-deployment rules
**Consumes:** Existing Feature Brief and Amendment contracts in `references/artifact-contracts.md`

**Modify:**
- `references/artifact-contracts.md`

**Description:**
Add the exact build lifecycle and durable fields required by the accepted Phase 3
design while keeping the Brief baseline immutable. The contract must distinguish
internal map completion from review-ready/release status and make `ship`'s later
map removal and Feature Record consolidation explicit.

**Requirements:**
- Define map-level `pending | in-progress | complete` and section-level statuses, with `complete` meaning verified/review-ready rather than deployed.
- Define `base_commit`, initial worktree state, optional local checkpoint records, append-only Build Evidence, and review diff range `base_commit..HEAD`.
- Define failure as a non-passing verification result blocking an accepted outcome; specify same-failure identity, the pre-second-attempt Failure Boundary Check, observable escalation signals, and unapproved material scope expansion as a stop condition.
- Define concise public/critical-internal documentation maintenance, trivial scout fixes, non-trivial scope approval, optional compaction handoff, secret redaction, and the invariant that build never deploys/pushes/merges/creates PRs/rewrites history.

**Tests:**
- Contract scanner planned in Phase 3: `test_artifact_schema` with display names `[AC-1]` through `[AC-15]`, one literal token per assertion.

**Implementation decisions / remarks:**
- Extended the canonical map and added append-only Build Evidence without changing the immutable Brief baseline or Review/Record schemas.

### Task 2: Extend native build/review handoff contract
**Status:** completed
**Traces to:** AC-1, AC-4, AC-6, AC-8, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (native command and path documentation)
**Produces:** `references/harness-command-contract.md` native `$absolutforge build` and `$absolutforge review` forms with complete paths
**Consumes:** Build lifecycle and artifact statuses from Task 1

**Modify:**
- `references/harness-command-contract.md`

**Description:**
Document the native handoff into and out of Build for Claude Code and Codex.
Ensure every command is copy-pasteable, repository-relative, and consistent with
the canonical lifecycle; do not add activation or deployment behavior.

**Requirements:**
- Add concrete Claude and Codex build/review examples using `absolutforge/features/{slug}/feature-brief.md` and the matching review artifact.
- State that Build may resume from durable map/evidence and that review receives the complete feature diff, not an internal section.
- State that handoff rendering never installs, enables, disables, deploys, pushes, creates PRs, merges, or rewrites history.

**Tests:**
- Contract scanner: `test_native_build_handoff` with display names `[AC-1]`, `[AC-4]`, `[AC-6]`, `[AC-8]`, `[AC-12]`, `[AC-13]`, `[AC-14]`, `[AC-15]`.

**Implementation decisions / remarks:**
- Added generic, complete native build/review paths and made resume, whole-diff review, and non-mutating handoff boundaries explicit.

### Task 3: Document Codex routing and capability-detected escalation
**Status:** completed
**Traces to:** AC-5, AC-7, AC-10, AC-13, AC-14, AC-15
**Test-first:** no (harness integration reference)
**Produces:** `references/codex-tools.md` Luna/Sol routing, bounded advisor dispatch, optional compaction, and no-deployment mechanics
**Consumes:** Failure Boundary Check and compaction rules from Task 1

**Modify:**
- `references/codex-tools.md`

**Description:**
Describe how the host-agnostic Build skill maps its optional capabilities onto
Codex primitives. Keep Sol advisory read-only and capability-driven; preserve the
fresh-context review mapping without creating a mandatory subagent ceremony.

**Requirements:**
- Specify primary `gpt-5.6-luna` with `xhigh` for Build and bounded read-only `gpt-5.6-sol` diagnostics only after observable Failure Boundary Check signals.
- Specify advisor input redaction, no repository edits/commits by the advisor, and main-context ownership of fixes and verification.
- Specify that native compaction is requested only after durable milestone persistence when supported; otherwise map/evidence support resume without hidden state.

**Tests:**
- Contract scanner: `test_codex_escalation_and_compaction` with display names `[AC-5]`, `[AC-7]`, `[AC-10]`, `[AC-13]`, `[AC-14]`, `[AC-15]`.

**Implementation decisions / remarks:**
- Kept Sol optional and diagnostic-only; durable artifacts remain the resume authority when native compaction is unavailable.

## Phase Verification
Run:
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
- `git diff --check`

## Verification History
- `python3 -m unittest discover -s tests -t . -p 'test_*.py'` — PASS (35 tests).
- `git diff --check` — PASS.

## Completion Criteria
- All phase tasks are completed.
- All changes remain within Write Scope.
- Phase verification commands pass.
- `implementation-context.md` records the canonical headings and routing facts needed by Phase 2.
- All `Context Contract -> Provides` items are present and internally consistent.

## Implementation Decisions / Remarks
- Canonical contracts now separate verified internal progress from whole-feature review readiness and preserve no-deployment boundaries.
