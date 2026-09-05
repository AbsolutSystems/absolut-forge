# Implementation Plan: Token-Efficient Runtime Contract

## Status
Executing

## Context
- Feature Brief: `absolutforge/features/token-efficient-runtime/feature-brief.md`
- Feature branch: `feature/0.7-token-efficient-runtime`
- Base revision: `f47dfbc45563b5fce6b8de49cd005f40b7b655fb`
- Plan revision: 1
- Build strategy: planned
- Planned methodology: standard

## Strategy
Define canonical runtime and compatibility semantics first. Then update skill entrypoints and host/distribution surfaces independently. Develop a small standard-library context projection/benchmark harness alongside canonical work; integrate contract and lifecycle checks after entrypoints land. Use current 0.6 task fields for this build. The orchestrator owns shared architecture and lifecycle changes; bounded standard tasks may be delegated. No live model benchmarks or Review invocation are included.

## Coverage
- EO-001: T-001, T-002, T-005
- EO-002: T-001, T-002, T-004, T-005
- EO-003: T-001, T-002, T-003, T-004, T-005
- EO-004: T-001, T-002, T-005
- EO-005: T-001, T-002, T-003, T-005
- EO-006: T-001, T-002, T-003, T-005
- EO-007: T-001, T-002, T-005 and final verification
- EO-008: T-004, T-005 and final verification

## Task graph

### T-001 — Canonical contracts and runtime projections
- Status: complete
- Capability: high
- Goal: establish four compact runtime projections, frontier/capsule schemas, compatible task fields, IDs, compact autonomous checkpoints and preserved final gates.
- Depends on: none
- Change surface: `runtime/*.md`; `references/artifact-contracts.md`; `references/planned-build-contract.md`; `references/planned-delegated-contract.md`; `references/model-routing.md`; `references/verification-doctrine.md`; `docs/adr/2026-09-05-token-efficient-runtime.md`
- Invariants: INV-001 through INV-005; legacy delegated stays fixed-owner via build-planned; tdd unchanged; final evidence schema unchanged.
- Test obligations: documentation-only exemption for task-local automation; inspect escalation, schema ownership, normal versus legacy resume, unchanged final evidence and test charter. Automated cross-contract proof belongs to T-005.
- Verification: `rtk git diff --check`; targeted canonical/runtime comparison.
- Completion evidence: canonical contracts plus four runtime projections and ADR updated; documentation-only exemption with direct comparison of lifecycle, legacy routing, unchanged final schema and doctrine test charter; `rtk git diff --check` pass. Runtime uses targeted escalation; legacy delegated retains fixed ownership. Checkpoint: commit introducing this completed entry.

### T-002 — Skill entrypoints and lifecycle routing
- Status: pending
- Capability: standard
- Goal: compact Build/Review entrypoints and coherent Discuss/Save/Load/Ship routing; remove separate delegated skill.
- Depends on: T-001
- Change surface: `skills/` except `skills/README.md`
- Invariants: INV-001 through INV-005; two new-start builders; no implicit Review; preserve explicit acceptance and path-only commit; binding guidance is not discarded.
- Test obligations: documentation-only exemption; inspect normal start/resume, legacy delegated/tdd, final gate and Review restrictions. T-005 covers cross-workflow checks.
- Verification: `rtk git diff --check`; targeted skill routing inspection.
- Completion evidence: pending

### T-003 — Host dispatch, distribution and user documentation
- Status: pending
- Capability: standard
- Goal: bounded host capsules, legacy executor routing and 0.7 public distribution with only two Build commands.
- Depends on: T-001
- Change surface: `references/codex-tools.md`; `references/claude-tools.md`; `references/opencode-tools.md`; `references/pi-tools.md`; `references/harness-command-contract.md`; `.opencode/command/`; `.codex-plugin/plugin.json`; `.claude-plugin/`; `.agents/plugins/marketplace.json`; `package.json`; `README.md`; `skills/README.md`; `CHANGELOG.md`; `docs/product-vision.md`; `agents/delegated-executor.md`
- Invariants: INV-001 through INV-005; retain required legacy executor descriptor; model identities only host deployment mechanics; no publishing/reinstalling.
- Test obligations: documentation/configuration-only exemption; validate changed JSON and inspect host-specific invocation/legacy profile consistency. T-005 covers distribution regression checks.
- Verification: changed JSON parses; `rtk git diff --check`.
- Completion evidence: pending

### T-004 — Reproducible context projection and benchmark harness
- Status: in-progress
- Capability: standard
- Goal: small read-only standard-library tool and tests proving bounded section extraction for new/legacy task capsules and frontier resume; benchmark three synthetic sizes against pinned 0.6 without claiming live savings.
- Depends on: none
- Change surface: `tools/context_package.py`; `tests/test_context_package.py`; `docs/runtime-benchmark.md`
- Invariants: INV-001, INV-002, INV-005; never execute artifact commands or mutate feature files; reject missing/ambiguous required data; no tokenizer/API dependency; preserve material invariant text.
- Test obligations: new and legacy task shapes; direct dependency fallback; long-history bounded package; missing/stale frontier refusal; invalid IDs/ambiguous input; no plan-wide worker payload; deterministic benchmark estimates distinct from measurements.
- Verification: `rtk python3 -m unittest discover -s tests -p test_context_package.py -v`.
- Completion evidence: pending

### T-005 — Cross-contract and delivery regression proof
- Status: pending
- Capability: high
- Goal: verify distributed workflow contracts, preserved lifecycle gates, runtime escalation and feature primary path across the integrated change.
- Depends on: T-001, T-002, T-003, T-004
- Change surface: `tests/test_runtime_contract.py`
- Invariants: INV-001 through INV-005; verify observable workflow artifacts and dispatch semantics, not incidental wording or snapshots.
- Test obligations: links/distribution; two builder surfaces; legacy resume and tdd handling; compact entrypoints; exact unchanged final evidence field set; review isolation/write limits; startup-to-frontier-to-capsule-to-final-review context scenario; pinned benchmark baseline.
- Verification: `rtk python3 -m unittest discover -s tests -p test_runtime_contract.py -v`.
- Completion evidence: pending

## Final verification
- Run `rtk python3 -m unittest discover -s tests -v` once for the final attempt; integration/context scenario is included in that suite.
- Run the documented synthetic benchmark for all three sizes and report estimates, not live measurements.
- Validate distribution JSON and local links; optionally use available Claude plugin validator.
- Inspect `f47dfbc45563b5fce6b8de49cd005f40b7b655fb..HEAD`, accepted outcome coverage, unchanged accepted intent, removal of advertised delegated starts, legacy ownership routing and final delivery-gate preservation.
- Whole-feature path is the local context workflow exercised with representative feature artifacts plus distributed instruction checks; paid live multi-model execution is explicitly outside scope.

## Plan changes
None yet.
