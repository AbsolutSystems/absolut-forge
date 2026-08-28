# Phase 2: Review Fingerprint and Harness Handoffs

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-5-ship.md`

## Shared Context
Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-5-ship/implementation-context.md`

## Context Contract

### Requires (from previous phases)
- `references/artifact-contracts.md` canonical Ship fingerprint and lifecycle contract from Phase 1.
- `docs/adr/2026-08-28-ship-post-review-closeout.md` accepted post-review freshness and transaction decisions.
- Existing `skills/review/SKILL.md` and Review metadata from Phase 4.

### Provides (for later phases)
- `skills/review/SKILL.md` Review output fields for exact safe path manifest, canonical source fingerprint, and Ship handoff.
- `references/harness-command-contract.md`, `references/claude-tools.md`, and `references/codex-tools.md` native Ship invocation and local-closeout mappings.
- `skills/review/agents/openai.yaml` unchanged explicit-only Review metadata compatible with the new handoff.

## Read Scope
- `references/artifact-contracts.md`
- `references/harness-command-contract.md`
- `references/claude-tools.md`
- `references/codex-tools.md`
- `skills/review/SKILL.md`
- `skills/review/agents/openai.yaml`
- `docs/product-vision.md`
- `docs/adr/2026-08-28-independent-review-and-bounded-fix-loop.md`
- `docs/adr/2026-08-28-ship-post-review-closeout.md`

## Write Scope
- `skills/review/SKILL.md`
- `skills/review/agents/openai.yaml`
- `references/harness-command-contract.md`
- `references/claude-tools.md`
- `references/codex-tools.md`

## Objective
Extend the existing independent Review handoff with the durable source-state
manifest and fingerprint consumed by Ship. Add native Claude and Codex handoffs
without changing Review's one-reviewer ownership, finding taxonomy, or explicit
activation behavior.

## Tasks

### Task 1: Add the reviewed-scope manifest and fingerprint handoff to Review
**Status:** completed
**Traces to:** AC-3, AC-6, AC-7, AC-9, AC-10, AC-11, AC-13, AC-15
**Test-first:** no (host-agnostic Markdown skill contract)
**Produces:** `skills/review/SKILL.md` Review instructions that record the Ship-reviewed path manifest and canonical SHA-256 fingerprint
**Consumes:** Phase 1 canonical Ship contract and existing Review lifecycle

**Modify:**
- `skills/review/SKILL.md`

**Description:**
Teach Review to persist the exact safe source scope it assessed so Ship can
recompute freshness instead of trusting prose or a generated snapshot. Keep the
reviewer read-only and preserve the current append-only finding and bounded
re-review behavior.

**Requirements:**
- In the Review artifact context, require a sorted reviewed-path manifest covering committed, staged, unstaged, and feature-owned untracked files while excluding `review.md`, process artifacts, and unrelated dirty files.
- Specify the exact `path-hex NUL state NUL mode NUL content-sha256 LF` encoding, Git content-byte hashing, deletion sentinels, and SHA-256 value that Review records for Ship.
- Require the manifest/fingerprint to be captured after the final review assessment and before setting Review `Complete`; missing or unsafe scope remains an input blocker.
- Preserve the one fresh read-only reviewer, untrusted-content redaction, no source/lifecycle mutation by the reviewer, and no automatic triada or extra review gate.
- Add the final native Ship handoff with both Brief and Review paths while retaining the existing Build handoff for open blockers.

**Tests:**
- `test_review_fingerprint_handoff_AC3_AC6_AC7_AC10_AC11_AC13` checks the manifest fields, canonical encoding, final-pass placement, and stale-scope handoff.
- `test_review_scope_redaction_AC9_AC15` checks safe-scope exclusions and untrusted-input boundaries remain intact.

**Implementation decisions / remarks:**
- Review now records the canonical raw-byte manifest and SHA-256 only after the final assessment and before `Complete`; unsafe or stale scope remains an input blocker.

### Task 2: Add native Ship mappings without changing Review activation
**Status:** completed
**Traces to:** AC-1, AC-7, AC-8, AC-9, AC-12, AC-15
**Test-first:** no (harness mapping and explicit-only metadata)
**Produces:** Native Claude/Codex Ship handoff forms and explicit-only Review metadata in the declared harness references
**Consumes:** Ship artifact contract from Phase 1 and Review fingerprint handoff from Task 1

**Modify:**
- `references/harness-command-contract.md`
- `references/claude-tools.md`
- `references/codex-tools.md`
- `skills/review/agents/openai.yaml`

**Description:**
Document how Review hands the matching Brief and Review paths to Ship in each
supported harness and how Codex maps the explicit-only metadata. Do not add a
new activation path, registry, hook, or remote operation.

**Requirements:**
- Add standalone Claude `/absolutforge:ship {brief} {review}` and Codex `$absolutforge ship {brief} {review}` examples using canonical repository-relative paths.
- State that Ship is explicit-only, local-only, and receives the Review fingerprint; rejected or stale Review input routes back to Review without mutation.
- Preserve Review's `allow_implicit_invocation: false`, existing `$review` metadata, one-reviewer fallback semantics, and active-model independence.
- Document local commit and PR-description preparation as output only, with no push, remote PR, merge, deployment, or history rewrite.

**Tests:**
- `test_harness_ship_handoffs_AC1_AC7_AC8_AC9_AC12_AC15` checks native commands, artifact paths, local-only boundaries, and explicit metadata.

**Implementation decisions / remarks:**
- Claude and Codex references provide standalone repository-relative Ship handoffs; Review Codex metadata remains unchanged with explicit-only activation.

## Phase Verification
Run:
- `python3 -m unittest tests.test_review_contract`
- `git diff --check`

## Completion Criteria
- Both tasks are completed and only the declared Write Scope changed.
- Review records the exact fingerprint handoff without changing its finding taxonomy or ownership.
- Claude/Codex commands are standalone, repository-relative, and explicit-only.
- Focused tests and diff hygiene pass.
- `implementation-context.md` records the Review-to-Ship handoff fields.

## Implementation Decisions / Remarks
- Added the final Review-to-Ship source-state handoff while preserving one fresh read-only reviewer, current finding taxonomy, and the existing Build return for blockers.
- Ship mappings state explicit-only local closeout and output-only local commit/PR description preparation, with no remote side effects.
- Verification: `python3 -m unittest tests.test_review_contract` -> pass (5 tests).
- Verification: `git diff --check` -> pass.
