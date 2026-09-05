# ADR: Token-efficient runtime projections

**Date:** 2026-09-05
**Status:** Accepted through the token-efficient-runtime Ready Brief.

Canonical references retain complete lifecycle, schema and verification rules. Four runtime documents project normal execution and name escalation triggers. Planned execution resumes from a validated Active Frontier and dispatches compact Task Capsules. Final verification deliberately reads full coverage and diff. Review starts with intent, final evidence, diff and tests; execution history needs a concrete question. This changes loading policy, not risk-based tests or final delivery gates.

New work has exactly two entrypoints: build and build-planned. Planned tasks use the lowest safe capability with high-capability orchestrator implementation when justified. Existing delegated builds resume via build-planned with original fixed-executor ownership, serial dispatch and no substitution. The separate delegated skill is removed. This supersedes the new-start surface of the 2026-09-04 fixed-executor ADR while preserving its legacy guarantees. Legacy tdd eligibility is unchanged.

Durable recovery uses artifacts and checkpointed Git history; Ship consolidation remains unchanged. New briefs use stable outcome/material-invariant IDs. Legacy artifacts remain readable, and missing/stale frontiers are reconstructed before dispatch without rewriting completed history.

Benchmark acceptance requires reproducible context/resume checks and three synthetic sizes against pinned 0.6. Live paid comparisons are deferred; static estimates must not be described as measured model savings.
