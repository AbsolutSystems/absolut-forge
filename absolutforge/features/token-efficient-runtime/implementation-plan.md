# Implementation Plan: Token-Efficient Runtime Contract

## Status
Complete

## Context
- Feature Brief: `absolutforge/features/token-efficient-runtime/feature-brief.md`
- Feature branch: `feature/0.7-token-efficient-runtime`
- Base revision: `f47dfbc45563b5fce6b8de49cd005f40b7b655fb`
- Plan revision: 5
- Build strategy: planned
- Planned methodology: standard

## Strategy
Define canonical runtime and compatibility semantics first. Then update skill entrypoints and host/distribution surfaces independently. Develop a small standard-library context projection/benchmark harness alongside canonical work; integrate contract and lifecycle checks after entrypoints land. Use current 0.6 task fields for this build. The orchestrator owns shared architecture and lifecycle changes; bounded standard tasks may be delegated. No live model benchmarks or Review invocation are included.

## Coverage
- EO-001: T-001, T-002, T-005
- EO-002: T-001, T-002, T-004, T-005
- EO-003: T-001, T-002, T-003, T-004, T-005, T-007
- EO-004: T-001, T-002, T-005, T-007
- EO-005: T-001, T-002, T-003, T-005
- EO-006: T-001, T-002, T-003, T-005
- EO-007: T-001, T-002, T-005 and final verification
- EO-008: T-004, T-005 and final verification
- A-001: T-008, T-009, T-010, T-011 and final verification

## Active frontier
- Plan revision: 5
- Next task: none
- Ready tasks: none
- Blocked tasks: none

### Relevant dependency facts
- None; all tasks checkpointed and final verification passed.

### Active invariants
- INV-001: accepted intent and selected methodology remain authoritative.
- INV-002: preserve recovery from artifacts and Git without conversation.
- INV-003: preserve risk-based gates, final evidence and independent Review.
- INV-004: workers own bounded source surfaces; orchestrator owns checkpoints.
- INV-005: shared behavior and schema ownership remain canonical; host mechanics stay local.

### Pending final-verification obligations
- None; authoritative 64-test suite, generated-runtime freshness check, projection failure fixtures and complete 0.11 candidate diff/accepted coverage review passed. Paired live comparison remains deliberately post-release under A-001 and is not claimed as implementation evidence.

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

### T-007 — Resolve modern Covers against accepted legacy outcomes
- Status: complete
- Capability: standard
- Covers: EO-003, EO-004
- Depends on: T-004
- Change surface: `tools/context_package.py`; `tests/test_context_package.py`
- Preserves: INV-001 through INV-005; read-only inputs, existing EO-ID and legacy Goal compatibility, bounded context and accepted-only intent.
- Implementation intent: resolve modern Covers references to unambiguous accepted outcome headings/text; refuse unknown or ambiguous references rather than emitting unaccepted prose.
- Test obligations: preserve full accepted clause for modern tasks with no-ID Briefs by heading/text; reject unknown and ambiguous references; preserve EO-ID and legacy Goal consumers and input immutability.
- Return boundary: return if correction requires changing public task contracts, unrelated parser behavior or expanding the write surface.
- Verification: `rtk python3 -m unittest discover -s tests -p test_context_package.py -v`; `rtk git diff --check`.
- Completion evidence: `tools/context_package.py` resolves modern Covers to full accepted heading/text clauses, including comma-containing headings, or valid EO IDs; unknown/ambiguous and mixed ID-plus-invented references refuse dispatch. `tests/test_context_package.py` adds heading/text preservation and unknown/mixed/ambiguous refusal regressions. Fresh bounded standard worker implemented only the two owned files; orchestrator independently inspected the diff, unchanged legacy consumers and semantic assertions. Focused `rtk python3 -m unittest discover -s tests -p test_context_package.py -v` passed all 18 tests; `rtk git diff --check` passed. Review F-001 correction is ready for final verification and independent re-review. Checkpoint: this checkpoint.

### T-008 — Value-triggered rotation and boundary economics
- Status: complete
- Capability: standard
- Covers: A-001; EO-002, EO-003, EO-007
- Depends on: T-007
- Change surface: `references/codex-tools.md`; `references/planned-build-contract.md`; `runtime/common.md`; `runtime/planned.md`; `runtime/autonomous.md`; `tests/test_runtime_contract.py`
- Preserves: INV-001 through INV-005; every checkpoint remains durable; explicit later Build invocations retain fresh ownership; final independence remains conditional and enforceable.
- Implementation intent: replace checkpoint-only rotation with explicit value triggers and require a concrete economic reason for adjacent plan boundaries.
- Test obligations: prove ordinary checkpoints do not rotate; lock every retained trigger, clean resume policy and boundary question.
- Risk controls: none
- Return boundary: return if a change weakens checkpoint recoverability, final verification or host isolation claims.
- Verification: `rtk python3 -m unittest discover -s tests -p test_runtime_contract.py -v`; `rtk git diff --check`.
- Completion evidence: Codex mapping and shared runtimes retain recoverable checkpoints while enumerating context pressure, changed decision frame, independent high-risk/final phase, unsafe compaction and later-invocation triggers. Planned compilation challenges boundaries without merging unrelated outcomes. Runtime contract coverage passes in the 64-test suite.

### T-009 — Deterministic owner and final packages
- Status: complete
- Capability: high
- Covers: A-001; EO-002, EO-005, EO-007
- Depends on: T-008
- Change surface: `tools/artifact_state.py`; `tools/build_projection.py`; `tools/context_package.py`; `tests/test_build_projection.py`; `tests/test_context_package.py`; `docs/runtime-benchmark.md`
- Preserves: INV-001 through INV-005; projections are read-only derived caches; existing resume/capsule API and legacy compatibility remain unchanged.
- Implementation intent: share Markdown/Git parsing and expose fail-closed owner/final JSON with lifecycle, frontier, coverage, ownership, freshness and blocker checks.
- Test obligations: deterministic durable-state output; dirty, unowned, stale and blocking refusal; complete diff pointer without diff duplication; existing capsule regressions green.
- Risk controls: parsing never executes artifact commands or mutates state; semantic exceptions remain explicit; ambiguous or contradictory data refuses output.
- Return boundary: return if a fact cannot be reconstructed from artifacts and Git or would require a new authoritative schema.
- Verification: `rtk python3 -m unittest discover -s tests -p 'test_*projection.py' -v`; existing context tests; full suite.
- Completion evidence: reusable parser primitives extracted without changing resume/capsule behavior. Owner/final commands derive the required state, validate plan schemas/coverage/write ownership/cleanliness/evidence ancestry/open blockers and emit PASS plus semantic exceptions. Four failure modes and successful final navigation are covered; all prior capsule tests remain green.

### T-010 — Generated effective Codex runtime
- Status: complete
- Capability: standard
- Covers: A-001; EO-001, EO-003, EO-007
- Depends on: T-009
- Change surface: `tools/compile_runtime.py`; `runtime/generated/`; `references/codex-tools.md`; `tests/test_build_projection.py`; `tests/test_runtime_contract.py`
- Preserves: INV-001, INV-003, INV-005; canonical source wins; generated files contain no unique normative rules; artifact schemas and full diff remain links.
- Implementation intent: deterministically compile planned Building and final states with source hashes, rule coverage and repaired package-relative links.
- Test obligations: byte-deterministic output; canonical mutation changes output; stale check; all local links resolve; lifecycle/worker/final gates remain present.
- Risk controls: none
- Return boundary: return rather than expanding to autonomous or other hosts before the later paired comparison.
- Verification: `rtk python3 tools/compile_runtime.py --check`; full runtime/link tests.
- Completion evidence: two non-authoritative generated Codex planned projections are reproducible from four named canonical sources, include SHA-256 provenance and rule IDs, and pass mutation/staleness plus repository-wide link checks.

### T-011 — 0.11 candidate policy and release surfaces
- Status: complete
- Capability: standard
- Covers: A-001; EO-003, EO-006, EO-008
- Depends on: T-010
- Change surface: `references/codex-tools.md`; `README.md`; `CHANGELOG.md`; `package.json`; `.claude-plugin/plugin.json`; `.codex-plugin/plugin.json`; `docs/0.10-token-efficiency-implementation-plan.md`; `docs/runtime-benchmark.md`; `tests/test_runtime_contract.py`
- Preserves: INV-001 through INV-005; host-specific model names remain in Codex mapping; no unmeasured efficiency claim; 0.10.1 remains the paired baseline.
- Implementation intent: ship 0.11.0 candidate with Luna high for standard work and record the explicit empirical-gate deferral.
- Test obligations: lock exact Codex tier mapping and all distribution versions; retain legacy delegated Luna high behavior; document comparison limitation.
- Risk controls: none
- Return boundary: do not claim a winning policy or remove 0.10.1 comparison evidence before controlled paired runs.
- Verification: distribution JSON parsing and full runtime-contract suite.
- Completion evidence: manifests and public docs identify 0.11.0; standard Codex mapping is Luna high and explicitly experimental; changelog and amendment record the narrow validation override and no-claim boundary. Full suite passes 64 tests.

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

### PC-003 — 2026-09-05
- Evidence: Review F-001 reproduces unresolved modern Covers for a no-ID Brief and successful projection of invented intent in `tools/context_package.py`.
- Reason: reopen the completed plan for the bounded accepted-intent compatibility correction requested by Review.
- Preserved completed tasks: T-001 through T-006
- Revised pending tasks: none
- Removed pending tasks: none
- Added tasks: T-007 — resolve accepted legacy outcomes and reject unknown/ambiguous references.
- Dependency changes: T-007 depends on completed T-004; sequential reuse of its two-file write surface.
- Plan revision: 3 -> 4
- Validation: outcomes covered; dependencies acyclic; write surfaces valid and sequential; test obligations complete; no intent expansion.

### PC-004 — 2026-09-10
- Evidence: accepted A-001 explicitly authorizes implementing the maintainer WP-2 through WP-5 candidate before paired empirical validation, while retaining correctness and lifecycle gates.
- Reason: create both 0.10.1 and 0.11.0 implementations before measuring them comparatively, as directed by the maintainer.
- Preserved completed tasks: T-001 through T-007
- Revised pending tasks: none
- Removed pending tasks: none
- Added tasks: T-008 through T-011 — value-triggered rotation, deterministic packages, generated planned runtime, experimental Luna high mapping and 0.11.0 release surfaces.
- Dependency changes: sequential T-008 -> T-009 -> T-010 -> T-011 to keep shared runtime/tool/version surfaces coherent.
- Plan revision: 4 -> 5
- Validation: A-001 and EO coverage complete; dependencies acyclic; shared write surfaces sequential; empirical gates alone deferred; correctness, lifecycle, freshness, ownership and generation gates retained.
