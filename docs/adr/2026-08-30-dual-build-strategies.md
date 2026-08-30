# ADR: Two first-class Build strategies

**Accepted:** 2026-08-30

## Decision

Keep one AbsolutForge plugin and one `discuss -> review -> ship` lifecycle, but expose two explicit implementation skills after a Ready Brief: `build` and `build-planned`.

`build` preserves the autonomous outcome-oriented model. `build-planned` keeps a high-capability orchestrator as feature owner, creates a durable implementation task graph, delegates bounded tasks by semantic capability tier when useful, validates each result, replans on evidence, and performs whole-feature integration verification.

Record the chosen strategy in Build start evidence. Resume and Review blocker handoffs return to the same strategy. Do not silently convert in-progress state between strategies.

## Rationale

The two modes optimize different workloads while preserving one intent contract and one quality gate. Keeping both in one plugin enables per-feature choice and direct measurement without duplicating discovery, review, ship or project-memory semantics.
