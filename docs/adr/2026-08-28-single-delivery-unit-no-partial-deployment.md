# ADR-005: One Delivery Unit With No Partial Deployment

- **Status:** Accepted
- **Date:** 2026-08-28
- **Decision owners:** AbsolutForge maintainers
- **Scope:** AbsolutForge MVP build, review, and release boundary

## Context

An Execution Map may split a feature into dependent outcomes so that a model
can implement and resume safely. Those outcomes can be incomplete, reordered,
or revised within the accepted Brief. Treating them as independently shippable
would expose unfinished behavior and make a checkpoint look like a product
release. Expensive integration checks are also too costly to repeat after every
internal outcome.

## Decision

The complete Feature Brief is the only delivery unit. Execution Map sections and
local checkpoint commits are internal implementation and recovery boundaries;
they are never QA or production deployment units. `build` performs no
deployment, including after final verification. It runs focused checks after
outcomes and broader/expensive integration checks once all outcomes are
complete, then hands the whole feature to `review`.

QA or production deployment happens only through the external release process
after review, `ship`, and the human-controlled merge/release decision. A map may
be marked complete only when every outcome and final verification are complete;
that status means review-ready, not deployed. `ship` folds useful map facts into
the Feature Record and removes the transient map without squashing or rewriting
checkpoint history.

## Alternatives considered

1. **Deploy each internal section to QA or production.** Rejected because a
   section may be intentionally incomplete or depend on later outcomes.
2. **Run expensive integration checks after every checkpoint.** Rejected as
   unnecessarily slow and token/cost heavy; focused checks protect local seams,
   while the full suite protects the final delivery unit.
3. **Let `build` deploy the completed feature.** Rejected because deployment is
   an external, environment-specific release decision outside implementation.

## Consequences

### Benefits

- No partial feature can be mistaken for a releasable product state.
- Expensive checks are paid once at the correct whole-feature boundary.
- Review sees one complete diff from `base_commit` through the final commit.
- Internal decomposition remains flexible without changing product lifecycle.

### Costs and constraints

- A feature cannot be released until all mapped outcomes are complete.
- The build workflow must clearly distinguish internal map status from release
  status and must never emit deployment commands.
- Release automation or a human must own QA/production deployment after ship.

## Related decisions and requirements

- [AbsolutForge Product Vision](../product-vision.md), especially Build and
  the one-feature delivery contract.
- [Product Vision](../product-vision.md#build-contract).
- [Delivery Artifact Contracts](../../references/artifact-contracts.md).
- [ADR-004: Outcome-Oriented Build With Durable Checkpoints](2026-08-28-outcome-oriented-build-and-checkpoints.md).
