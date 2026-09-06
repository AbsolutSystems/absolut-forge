# ADR: Feature-family planning before accepted Briefs

**Date:** 2026-09-06  
**Status:** Accepted

## Context

AbsolutForge previously required `discuss` to converge every product idea into
one Feature Brief. `build` could decompose a large accepted Brief, but that
decomposition concerns implementation. It could not prevent a broad product
idea from freezing several delivery outcomes, rollout boundaries, and uncertain
later behavior into one Ready intent baseline.

## Decision

`discuss` has two valid outcomes. A bounded request produces one accepted Ready
Feature Brief as before. When repository and product evidence shows multiple
independently valuable, cancellation-safe outcomes, material learning between
outcomes, or distinct rollout, migration, security, or operational boundaries,
Discuss recommends a Feature Plan route and requires explicit human agreement.

The planning route creates one canonical `feature-plan.md` and stable `P{NN}`
Phase Seeds. The plan owns coarse end-to-end behavior, behavior custody, shared
invariants, dependencies, uncertainties, phase ordering, and coherent stop
states. It is accepted as `Planned` in one path-scoped local commit containing
exactly the plan and its seeds.

A Phase Seed is later passed to `discuss`. That run validates current evidence
and lineage, excludes later-phase scope, and produces an ordinary self-contained
Feature Brief at the path declared by the seed. Applicable plan behavior and
invariants are copied into the Brief rather than inherited dynamically. Only an
explicitly accepted Ready Brief can enter `build`; Build refuses Feature Plans
and Phase Seeds before mutation.

Material planning changes use explicitly accepted, append-only reconciliation
records and may replace only unexpanded seeds. Ready Briefs remain immutable and
use their existing amendment contract independently.

## Consequences

- Product-delivery phasing is separate from Build strategy and implementation
  task planning.
- Later phases can stay intentionally coarse until earlier delivery produces
  evidence.
- A family creates more artifacts and acceptance checkpoints, but each Build
  receives a smaller and more truthful intent boundary.
- Stable phase IDs survive reordering; sequence numbers are not phase identity.
- One indivisible transaction, migration, security boundary, compatibility
  window, or rollback unit is not split merely to reduce phase size.

## Rejected alternatives

- Let Build split one mega-Brief: implementation begins after speculative
  product intent has already been accepted.
- Split by document length or file count: these do not establish independent
  user value or safe delivery boundaries.
- Make the Feature Plan itself buildable: this would create a second intent
  authority and bypass per-phase acceptance.
- Fully specify all phases at planning time: this recreates the mega-Brief as
  several files and prevents evidence-driven refinement.
