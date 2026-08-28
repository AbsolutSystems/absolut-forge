# ADR-004: Outcome-Oriented Build With Durable Checkpoints

- **Status:** Accepted
- **Date:** 2026-08-28
- **Decision owners:** AbsolutForge maintainers
- **Scope:** AbsolutForge MVP `build` workflow

## Context

The accepted Feature Brief should give a capable implementation model enough
intent and constraints to make local engineering decisions. A second detailed
task recipe, mandatory worker delegation, and repeated review ceremonies would
recreate the token-heavy process AbsolutForge is intended to replace. At the
same time, a long feature needs durable resume state and a reviewable Git
anchor when work crosses sessions or context compaction.

## Decision

Make `build` outcome-oriented and autonomous. The primary model owns the
implementation, verification, and local plan. It creates an Execution Map only
when there are dependent outcomes, meaningful uncertainty, or a likely need for
durable resume. The map tracks map-level and section-level status, but sections
are internal implementation boundaries rather than approval or delivery gates.

Every build records `base_commit` and the initial worktree state. Small cohesive
work keeps changes for `ship`; larger mapped work may create a local checkpoint
commit after each coherent, verified outcome. Checkpoint IDs are recorded in the
map and Build Evidence, and review uses `base_commit..HEAD`. `build` never
pushes, merges, rewrites history, or deploys.

The default Codex route uses `gpt-5.6-luna` with `xhigh` reasoning. If Luna is
genuinely stuck, it may ask a bounded, read-only `gpt-5.6-sol` advisor for
diagnosis. The advisor never edits or commits; the main model remains
responsible for decisions and verification. Delegation is otherwise optional.
After a major verified milestone, the active harness may request native context
compaction. Durable artifacts remain authoritative when compaction is
unavailable or opaque.

Failure escalation is boundary-first, not based on a fixed number of attempted
hypotheses. A failure is a non-passing verification result that blocks an
accepted outcome; the same failure is the same observable check/runtime symptom
and violated invariant, even when proposed causes differ. Before a second repair
attempt, the model runs a Failure Boundary Check. It may continue only when the
failure is causally mapped to the current outcome, the invariant is clear, and
the edit remains within the accepted change surface. It escalates before another
speculative edit when causal mapping or invariant clarity is absent, the edit
would cross an unapproved module/scope boundary, or it touches a public
contract, security/data boundary, migration, shared architecture, or conflicting
binding evidence. The wording is an observable guardrail; it does not require
the model to recognize an abstract uncertainty label. An unapproved material
scope expansion is a stop condition, not an accidental outcome.

## Alternatives considered

1. **No commits until `ship`.** Rejected for larger mapped work because resume
   and phase-level review would lose useful traceability.
2. **Commit every implementation step.** Rejected as noisy and ceremony-heavy;
   checkpoints are limited to coherent verified outcomes.
3. **Mandatory coding subagents and review gates.** Rejected because they add
   token cost without improving every capable model's result.
4. **Always-on Sol advisor or compaction.** Rejected because both add cost and
   harness coupling; each is capability- and need-driven.
5. **Session-only progress state.** Rejected because cross-session and
   cross-harness resume must work from repository artifacts alone.

## Consequences

### Benefits

- A capable model can reason locally without a second task ceremony.
- Long work remains resumable and reviewable through map state, evidence, and
  Git anchors.
- Advisor and compaction cost is paid only when capability or context pressure
  justifies it.
- The same artifact contract works across supported harnesses.

### Costs and constraints

- The model must maintain accurate map status and append-only Build Evidence.
- Checkpoint commits require clean scope separation from pre-existing dirty
  worktree changes.
- Harness integrations must detect native compaction and generic advisor
  dispatch rather than assuming either primitive exists.

## Related decisions and requirements

- [AbsolutForge Product Vision](../product-vision.md), especially Build and
  cross-harness resume.
- [Phase 3 planning](../../absolutforge/features/absolutforge-mvp/planning-phase-3-build.md).
- [Delivery Artifact Contracts](../../references/artifact-contracts.md).
- [Codex primitive mapping](../../references/codex-tools.md).
- [ADR-001: One Host-Agnostic Skill Tree](2026-08-27-host-agnostic-skill-tree.md).
