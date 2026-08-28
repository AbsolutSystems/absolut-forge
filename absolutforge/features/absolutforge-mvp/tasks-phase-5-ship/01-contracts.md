# Phase 1: Canonical Ship Contracts and Transaction ADR

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-5-ship.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-5-ship/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- `references/artifact-contracts.md` Review, Feature Brief, Build Evidence, and Execution Map contracts.
- `absolutforge/features/absolutforge-mvp/planning-phase-5-ship.md` accepted scope and AC-1 through AC-15.
- `docs/product-vision.md` accepted Ship lifecycle and no-remote boundary.

### Provides (for later phases)
- `references/artifact-contracts.md` canonical Ship lifecycle, Feature Record, Executive Summary, fingerprint, approval, memory, archive, transaction journal, and recovery rules.
- `docs/adr/2026-08-28-ship-post-review-closeout.md` accepted rationale for post-review rendering and local transactional closeout.

## Read Scope
- `docs/product-vision.md`
- `absolutforge/features/absolutforge-mvp/planning-main.md`
- `absolutforge/features/absolutforge-mvp/planning-phase-5-ship.md`
- `references/artifact-contracts.md`
- `references/project-memory.md`
- `references/harness-command-contract.md`
- `docs/adr/2026-08-28-independent-review-and-bounded-fix-loop.md`
- `docs/adr/2026-08-28-outcome-oriented-build-and-checkpoints.md`
- `docs/adr/2026-08-28-single-delivery-unit-no-partial-deployment.md`

## Write Scope
- `references/artifact-contracts.md`
- `docs/adr/2026-08-28-ship-post-review-closeout.md`

## Objective
Make Ship's inputs, outputs, freshness guard, human gate, memory routing, and
local closeout transaction precise enough that later skill and harness work does
not invent lifecycle or recovery rules. Preserve the accepted Review ownership
and the complete Feature Brief as the only delivery unit.

## Tasks

### Task 1: Extend the canonical Ship artifact and transaction contract
**Status:** completed
**Traces to:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15
**Test-first:** no (canonical Markdown schema and lifecycle documentation)
**Produces:** `references/artifact-contracts.md` Ship contract with post-review fingerprint, Feature Record, Executive Summary, approval, memory, archive, journal, and recovery sections
**Consumes:** Existing Feature Brief, Build Evidence, Execution Map, Review, and project-memory contracts

**Modify:**
- `references/artifact-contracts.md`

**Description:**
Replace the minimal Ship description with the canonical contract for validating
Review-complete input and consolidating active artifacts. Define deterministic
source scope/fingerprint bytes, path-safe HTML rules, exact closeout ordering,
per-item memory approval, and recovery semantics without adding another review
or deployment stage.

**Requirements:**
- Define Ship preconditions for matching repository-relative Brief/Review paths, Brief `In Review`, Review `Complete`, no open `BLOCKING`, valid final evidence, and the original `base_commit`/safe current-worktree scope.
- Define Feature Record headings and Executive Summary fields, including immutable intent, as-built outcome, deviations, verification, review findings, ADR links, durable knowledge, follow-ups, recommended review order, and no source excerpts.
- Define the canonical sorted fingerprint manifest as `path-hex NUL state NUL mode NUL content-sha256 LF`, including raw path bytes, Git modes, deleted sentinels, Git content bytes, scope union, and SHA-256 comparison before render and mutation.
- Define one human preview approval with per-item memory decisions, archive/deletion/staging/commit ordering, normalized archive-relative HTML links, escaping/redaction, and no remote side effects.
- Define the transaction journal at `.ship-txn/{txid}/journal.json`, OS advisory lock, operation statuses, normal/failure state graph, commit intent/ref guard, conflict-safe rollback, interrupted-commit finalization, and terminal `rolled-back` behavior.

**Tests:**
- `test_ship_contract_schema_AC1_AC2_AC3_AC4_AC5_AC6_AC7_AC8_AC9_AC10_AC11_AC12_AC13_AC14_AC15` checks every canonical heading and lifecycle token after Phase 4 adds the contract scanner.
- `test_ship_contract_fingerprint_AC3_AC10_AC11` checks the manifest grammar, deletion sentinels, scope union, and stale-state refusal requirements.
- `test_ship_contract_transaction_AC7_AC8_AC12_AC13_AC15` checks approval, memory routing, journal/recovery, rollback conflicts, and no-remote boundaries.

**Implementation decisions / remarks:**
- Added the canonical preconditions, raw-byte manifest/fingerprint algorithm,
  approval-bound preview, local transaction order, HTML link policy, and
  journal/recovery protocol.

### Task 2: Align the accepted closeout ADR with the canonical contract
**Status:** completed
**Traces to:** AC-3, AC-5, AC-7, AC-8, AC-10, AC-11, AC-12, AC-13, AC-15
**Test-first:** no (architecture decision record)
**Produces:** `docs/adr/2026-08-28-ship-post-review-closeout.md` aligned with the exact Ship transaction and freshness contract
**Consumes:** Ship contract from Task 1

**Modify:**
- `docs/adr/2026-08-28-ship-post-review-closeout.md`

**Description:**
Update the accepted ADR so it records the final implementation-level decisions
without duplicating the complete artifact schema. The ADR must agree with the
canonical contract on ordering, fingerprints, link handling, recovery, and
expected-parent local commit behavior.

**Requirements:**
- State that Review's safe source scope and canonical fingerprint are the only freshness baseline and list exact path-byte, mode, hash, and deletion rules.
- Record the post-review render point, path-only self-contained HTML, approval gate, per-item memory decisions, and archive-relative link policy.
- Record OS advisory locking, journal path/state graph, per-operation output verification, commit intent, atomic expected-parent ref update, and interrupted-commit finalization.
- Record conflict-safe rollback, terminal `rolled-back` cleanup, local-only side effects, and explicit exclusion of push, PR, merge, deployment, and history rewrite.

**Tests:**
- `test_ship_adr_alignment_AC3_AC5_AC7_AC8_AC10_AC11_AC12_AC13_AC15` compares required decision markers in the ADR with the canonical contract.

**Implementation decisions / remarks:**
- Aligned the ADR's freshness baseline, raw-path ordering, and path-only HTML
  policy with the canonical contract.

## Phase Verification
Run:
- `python3 -m unittest tests.test_review_contract`
- `git diff --check`

## Completion Criteria
- Both tasks are completed and only the declared Write Scope changed.
- The canonical contract contains no unresolved placeholder or contradictory status.
- Focused tests and diff hygiene pass.
- `implementation-context.md` records the Ship schema, fingerprint, and transaction facts needed by later phases.

## Implementation Decisions / Remarks
- Ship remains a local closeout: Review owns source scope/fingerprint and Ship
  validates it before render and transaction mutation.
