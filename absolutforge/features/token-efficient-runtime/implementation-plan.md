# Implementation Plan: Token-Efficient Runtime Contract

## Status
Executing

## Context
- Feature Brief: `absolutforge/features/token-efficient-runtime/feature-brief.md`
- Feature branch: `feature/0.7-token-efficient-runtime`
- Base revision: `f47dfbc45563b5fce6b8de49cd005f40b7b655fb`
- Plan revision: 3
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

## Active frontier
- Plan revision: 3
- Next task: none
- Ready tasks: none
- Blocked tasks: none

### Relevant dependency facts
- T-001: `runtime/` projects canonical references; new starts use standard planned, legacy delegated resumes through build-planned retaining fixed ownership. Final evidence schema is unchanged.

### Active invariants
- INV-001: accepted intent and selected methodology remain authoritative.
- INV-002: preserve recovery from artifacts and Git without conversation.
- INV-003: preserve risk-based gates, final evidence and independent Review.
- INV-004: workers own bounded source surfaces; orchestrator owns checkpoints.
- INV-005: shared behavior and schema ownership remain canonical; host mechanics stay local.

### Pending final-verification obligations
- Context workflow: canonical artifact -> frontier resume -> task capsule -> complete final gate -> diff-first Review.
- Full unittest suite, synthetic benchmark, distribution checks and full implementation diff.

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
- Status: complete
- Capability: standard
- Goal: compact Build/Review entrypoints and coherent Discuss/Save/Load/Ship routing; remove separate delegated skill.
- Depends on: T-001
- Change surface: `skills/` except `skills/README.md`
- Invariants: INV-001 through INV-005; two new-start builders; no implicit Review; preserve explicit acceptance and path-only commit; binding guidance is not discarded.
- Test obligations: documentation-only exemption; inspect normal start/resume, legacy delegated/tdd, final gate and Review restrictions. T-005 covers cross-workflow checks.
- Verification: `rtk git diff --check`; targeted skill routing inspection.
- Completion evidence: compact runtime-linked Build/Review entrypoints; Discuss EO/INV IDs and two choices; Save/Load/Debug legacy routing; delegated skill and UI metadata removed (recoverable in Git). Orchestrator checked start/compile/final canonical triggers, acceptance commit and targeted Load behavior; worker corrected omitted triggers before acceptance. Seven changed skill descriptors passed isolated uv/pyyaml quick_validate; `rtk git diff --check` pass. Documentation-only exemption. Checkpoint: commit introducing this completed entry.

### T-003 — Host dispatch, distribution and user documentation
- Status: complete
- Capability: standard
- Goal: bounded host capsules, legacy executor routing and 0.7 public distribution with only two Build commands.
- Depends on: T-001
- Change surface: `references/codex-tools.md`; `references/claude-tools.md`; `references/opencode-tools.md`; `references/pi-tools.md`; `references/harness-command-contract.md`; `.opencode/command/`; `.codex-plugin/plugin.json`; `.claude-plugin/`; `.agents/plugins/marketplace.json`; `package.json`; `README.md`; `skills/README.md`; `CHANGELOG.md`; `docs/product-vision.md`; `agents/delegated-executor.md`
- Invariants: INV-001 through INV-005; retain required legacy executor descriptor; model identities only host deployment mechanics; no publishing/reinstalling.
- Test obligations: documentation/configuration-only exemption; validate changed JSON and inspect host-specific invocation/legacy profile consistency. T-005 covers distribution regression checks.
- Verification: changed JSON parses; `rtk git diff --check`.
- Completion evidence: all four host mappings and handoff routing use compact packages and legacy resume; removed delegated opencode command (Git-recoverable), retained legacy executor descriptor; manifests/docs now 0.7.0. Worker parsed five JSON descriptors; orchestrator inspected host docs and corrected residual Pi preload/capsule wording before acceptance. `rtk git diff --check` and nine focused runtime-contract tests pass. Documentation/configuration-only exemption. Checkpoint: commit introducing this completed entry.

### T-004 — Reproducible context projection and benchmark harness
- Status: complete
- Capability: high
- Goal: small read-only standard-library tool and tests proving bounded section extraction for new/legacy task capsules and frontier resume; benchmark three synthetic sizes against pinned 0.6 without claiming live savings.
- Depends on: none
- Change surface: `tools/context_package.py`; `tests/test_context_package.py`; `docs/runtime-benchmark.md`
- Invariants: INV-001, INV-002, INV-005; never execute artifact commands or mutate feature files; reject missing/ambiguous required data; no tokenizer/API dependency; preserve material invariant text.
- Test obligations: new and legacy task shapes; direct dependency fallback; long-history bounded package; missing/stale frontier refusal; invalid IDs/ambiguous input; no plan-wide worker payload; deterministic benchmark estimates distinct from measurements.
- Verification: `rtk python3 -m unittest discover -s tests -p test_context_package.py -v`.
- Completion evidence: read-only CLI resume/capsule and pinned artifact-derived benchmark, documented commands/limitations; 16 focused tests pass for canonical/legacy shapes, no-ID intent, amendments, duplicate/unknown IDs, active/global constraints, per-dependency evidence, unchanged input bytes, 300-task history isolation and measured string lengths. Worker result was corrected and escalated under PC-002; orchestrator finished ambiguity/intent projection and equal-evidence benchmark packaging. Actual feature-plan resume/capsule exercised locally. `rtk git diff --check` pass. New fact: helper is optional and fails closed on unsupported ambiguity; Git durability/semantic sufficiency remain orchestrator checks. Checkpoint: commit introducing this completed entry.

### T-005 — Cross-contract and delivery regression proof
- Status: complete
- Capability: high
- Goal: verify distributed workflow contracts, preserved lifecycle gates, runtime escalation and feature primary path across the integrated change.
- Depends on: T-001
- Change surface: `tests/test_runtime_contract.py`
- Invariants: INV-001 through INV-005; verify observable workflow artifacts and dispatch semantics, not incidental wording or snapshots.
- Test obligations: links/distribution; two builder surfaces; legacy resume and tdd handling; compact entrypoints; exact unchanged final evidence field set; review isolation/write limits; startup-to-frontier-to-capsule-to-final-review context scenario; pinned benchmark baseline.
- Verification: `rtk python3 -m unittest discover -s tests -p test_runtime_contract.py -v`.
- Completion evidence: ten focused tests pass: separate-process resume-to-capsule with immutable inputs and no completed history; missing frontier refusal; linked runtime packaging; two build command surfaces; exact baseline final evidence template and doctrine charter preserved; legacy ownership/tdd restrictions unchanged; Review boundary and PC-001 section regression; host startup packages; 0.7 JSON distribution. This proves local artifact/context behavior and instruction contracts, not live model adherence. Checkpoint: commit introducing this completed entry.

### T-006 — Preserve canonical section boundaries for targeted readers
- Status: complete
- Capability: low
- Goal: keep Review severity/write rules within the Review section when adding runtime escalation documentation.
- Depends on: T-001
- Change surface: `references/artifact-contracts.md`
- Invariants: INV-003, INV-005; wording and final schema unchanged; sequential corrective ownership after T-001 completion.
- Test obligations: documentation-only exemption; inspect section boundary and confirm Review contains its severity/write rules. T-005 regression checks cover the integrated contract.
- Verification: `rtk git diff --check`; targeted Review section inspection.
- Completion evidence: moved runtime escalation to its own end section, preserving Review severity/write boundary in its canonical section; documentation-only exemption, targeted inspection and `rtk git diff --check` pass. No schema or behavior change. Checkpoint: commit introducing this completed entry.

## Final verification
- Run `rtk python3 -m unittest discover -s tests -v` once for the final attempt; integration/context scenario is included in that suite.
- Run the documented synthetic benchmark for all three sizes and report estimates, not live measurements.
- Validate distribution JSON and local links; optionally use available Claude plugin validator.
- Inspect `f47dfbc45563b5fce6b8de49cd005f40b7b655fb..HEAD`, accepted outcome coverage, unchanged accepted intent, removal of advertised delegated starts, legacy ownership routing and final delivery-gate preservation.
- Whole-feature path is the local context workflow exercised with representative feature artifacts plus distributed instruction checks; paid live multi-model execution is explicitly outside scope.

## Plan changes

### PC-001 — 2026-09-05
- Evidence: `references/artifact-contracts.md` inserted Runtime projections heading before Review severity/write rules; targeted section reads would omit those Review rules. T-005 tests depend on already-set canonical contracts and can be authored while independent entrypoint edits finish.
- Reason: preserve targeted canonical loading; allow bounded test authoring independently of distribution completion, keeping integration acceptance at final verification.
- Preserved completed tasks: T-001
- Revised pending tasks: T-005 may be authored after T-001; completion validation uses integrated T-002/T-003 results and final verification covers T-004.
- Removed pending tasks: none
- Added tasks: T-006, sequential bounded canonical-section correction after T-001.
- Dependency changes: T-005 depends on T-001; T-006 depends on T-001. Final verification still requires every task complete.
- Plan revision: 1 -> 2
- Validation: outcomes covered; dependencies acyclic; correction ownership sequential; test obligations complete; no intent expansion.

### PC-002 — 2026-09-05
- Evidence: T-004 worker correction still accepts duplicate Brief IDs, can omit applicable active invariants, and lacks long-history regression proof; benchmark compares unequal contract/source packages.
- Reason: intent-preserving projection and faithful measurement require shared-contract judgment beyond the initial bounded parser estimate. Orchestrator takes over correction under standard methodology.
- Preserved completed tasks: T-001, T-002, T-003, T-006
- Revised pending tasks: T-004 capability standard -> high; retain its existing write surface and obligations, add explicit ambiguity/global-invariant and equal-package benchmark checks.
- Removed pending tasks: none
- Added tasks: none
- Dependency changes: none
- Plan revision: 2 -> 3
- Validation: outcomes covered; dependencies acyclic; write surfaces unchanged; test obligations complete; no intent expansion.
