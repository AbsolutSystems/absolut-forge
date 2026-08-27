# ADR-003: Optional Cross-Model Brief Consultation

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** AbsolutForge maintainers
- **Scope:** AbsolutForge MVP `consult` workflow for Claude Code and Codex

## Context

An accepted Feature Brief is the durable boundary between interactive discovery
and implementation. A developer may want a fresh second opinion from another
harness after discussion, but adding another mandatory stage would recreate the
ceremony and coupling that AbsolutForge is intended to avoid. Consultation must
also preserve product ownership and the immutable intent of a `Ready` Brief.

## Decision

Provide `consult` as an optional, explicit-only workflow for an existing `Draft`
or `Ready` Brief. It returns one bounded batch of material findings, each with
evidence, impact, and a precise proposed Brief change. No Brief mutation occurs
until the human explicitly accepts individual findings or the complete batch.

Accepted findings merge into a `Draft`; accepted material changes to a `Ready`
Brief are recorded as accepted amendments, leaving its original baseline
unchanged. A Brief created in Claude may be consulted in Codex, and a Brief
created in Codex may be consulted in Claude. The Brief does not record model
identity. `Building` and `In Review` Briefs are not mutated; material intent
changes return to `discuss` and its amendment flow. No material issue returns
`no material findings` and creates no consultation artifact.

The normal workflow remains `discuss -> build -> review -> ship`; consultation
is never a gate between `discuss` and `build`.

## Alternatives considered

1. **Make consultation mandatory before build.** Rejected: it adds a new gate,
   slows the normal path, and makes a second model a process requirement.
2. **Invoke consultation automatically from `discuss`.** Rejected: invocation
   must remain visible and human-controlled, and the original use case is a
   fresh session in another harness.
3. **Embed consultation inside `discuss`.** Rejected: it couples discovery to
   a particular multi-model session and prevents a later cross-harness check.
4. **Write a persistent consultation report.** Rejected: accepted findings
   belong in the Brief and rejected findings have no downstream consumer; a
   report would create artifact and lifecycle noise.

## Consequences

### Benefits

- Developers can request a fresh cross-model check without changing the default
  delivery path.
- Explicit approval preserves human control over Draft edits and Ready intent.
- One Brief remains the interoperability boundary across Claude Code and Codex.
- Deduplication and the no-findings outcome avoid consultation artifact noise.

### Costs and constraints

- Consultation is an additional explicit command and does not promise a model
  comparison score or persistent audit trail.
- Skills must follow the canonical artifact and native handoff contracts rather
  than inventing consultation-specific schemas.
- Material changes discovered after build starts must use `discuss` and the
  established amendment flow.

## Related decisions and requirements

- [AbsolutForge Product Vision](../product-vision.md), especially the `discuss`
  contract, immutable intent, and core workflow.
- [Phase 2 planning](../../absolutforge/features/absolutforge-mvp/planning-phase-2-discuss.md).
- [Delivery Artifact Contracts](../../references/artifact-contracts.md),
  especially the Feature Brief and Amendment contracts.
- [Native Harness Command and Handoff Contract](../../references/harness-command-contract.md).
- [ADR-001: One Host-Agnostic Skill Tree](2026-08-27-host-agnostic-skill-tree.md).
- [ADR-002: Explicit Activation Without SessionStart Hooks](2026-08-27-explicit-activation-without-hooks.md).
