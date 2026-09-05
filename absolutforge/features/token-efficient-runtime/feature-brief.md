# Feature: AbsolutForge 0.7 — Token-Efficient Runtime Contract

## Status
Building

## Change type
Feature

## Problem and goal

Reduce runtime input context while preserving accepted-intent fidelity, resumability, verification quality, independent Review, checkpoint durability, and deterministic lifecycle behavior. Durable repository state must remain sufficient for recovery; active context should scale with the current execution frontier rather than completed feature history. This is a workflow-contract and distribution change, not implementation of an application feature.

## Users

Maintainers and users of AbsolutForge on Codex, Claude Code, opencode, and Pi; high-capability builders/orchestrators, bounded workers, and independent reviewers.

## Current state and evidence

- `skills/build-planned/SKILL.md` unconditionally loads the planned, artifact, verification, routing, and harness contracts plus the active host mapping.
- `references/planned-build-contract.md`, Context rotation, requires rehydration from the complete Brief and current plan. It already establishes durable ownership, compact completion evidence, bounded workers, and immutable completed tasks.
- `skills/review/SKILL.md` requires the selected execution artifact, including a completed plan for planned Build, despite treating it as supporting evidence.
- `references/model-routing.md` already supports low/standard/high task routing and direct orchestrator execution for standard planned Build. Fixed-executor methodology prohibits that escape hatch.
- `references/codex-tools.md` already asks for a minimum worker package; its delegated profile explicitly requires a fresh worker without inherited conversation. The change must make compact context consistent across ordinary planned execution and all hosts.
- `references/artifact-contracts.md` defines two strategies and standard/delegated methodologies, immutable Ready intent, acceptance/start/task/handoff commits, complete final evidence, Save/Load and Review routing, and Ship consolidation/removal of transient artifacts.
- `AGENTS.md` requires shared behavioral ownership, host-specific mechanics in host mappings, and canonical artifact schemas rather than duplicated templates.
- The inspected worktree started clean on `main`. Discuss created `feature/0.7-token-efficient-runtime` for this Draft and its eventual acceptance baseline.

## Expected behavior

New builds expose `build` and `build-planned`; remove the separately selectable `build-planned-delegated` skill and its new-start lifecycle branch. Planned Build chooses the lowest safe capability tier and permits high-capability orchestrator implementation when justified. Existing 0.6 delegated builds resume through a legacy path inside `build-planned`, preserving their recorded fixed-executor and ownership rules without conversion to standard methodology.

The four runtime projections are `runtime/common.md`, `runtime/autonomous.md`, `runtime/planned.md`, and `runtime/review.md`. Canonical references win on disagreement. Each projection identifies concrete escalation triggers and reference sections; normal task execution does not preload full canonical documents. Approximate size targets are 400–700, 700–1100, 900–1400, and 700–1100 tokens respectively; these are engineering targets, not reasons to omit required rules.

Planned compilation reads the canonical planning contract and verification doctrine and produces the smallest useful DAG, accepted-outcome coverage, bounded write surfaces, concrete tests, capability tiers, fast gates, and final integration obligations. A normal clean resume reads the runtime, accepted Brief intent/amendments, plan header and Active Frontier, current task, sufficient direct-dependency facts, and relevant code/tests. Missing historical facts trigger targeted reads. Whole completed history and the base-to-HEAD diff are reserved for decisions that require them, including final verification.

Active Frontier is mutable orchestrator-owned derived state near the plan top: plan revision, next task, ready/blocked tasks, relevant dependency facts, active invariants, and pending final-verification obligations. Refresh it after completion, blocking, accepted plan changes, and readiness changes; persist coherent task evidence and frontier at checkpoint boundaries. Detect missing or inconsistent frontier state before dispatch and reconstruct it from canonical state as needed. It never overrides task dependencies, accepted intent, or Git truth. Existing plans without it receive one derived frontier before continuing, without rewriting completed definitions/evidence.

Workers receive a Task Capsule with Outcome, Own, Must preserve, Implement, Prove, Verify, and Return instead of guessing if. Derive it from durable task state, relevant accepted clauses, and direct-dependency facts; include exact commands and sufficient behavior/invariant text, not unresolved IDs alone. Send relevant source/test context without the full plan, unrelated Brief sections, historical dialogue, or full doctrine. Relevant binding repository instructions remain applicable; context economy does not authorize ignoring them or claim that host-injected context can always be suppressed.

New durable tasks use Status, Capability, Covers, Depends on, Change surface, Preserves, Implementation intent, Test obligations, Return boundary, Verification, and Completion evidence. Preserve support for legacy Goal, Invariants, Implementation guidance, Watch points, and Decision boundary. New Discuss briefs assign stable EO IDs to outcomes and INV IDs to material invariants; old briefs remain valid without retrofitting. Resolve legacy references by headings/text.

Review starts from runtime, accepted Brief/amendments, final Build Evidence, complete implementation diff, and changed/new tests, inspecting relevant current code as needed. Load plan/map/history/consultation only for a concrete question: legacy ownership, referenced plan change, material decision ambiguity, cross-task inconsistency, lifecycle validation, or a finding. Keep the fresh independent reviewer mechanism and explicitly labelled advisory fallback. A compact checklist projects the unchanged risk-based test doctrine; uncertain classifications escalate to the doctrine.

Autonomous Build uses a compact runtime and coherent outcome loop with focused tests, fast gates, durable checkpoints, and optional execution map. Intermediate evidence records checkpoint/result/tests/new durable facts without repeating the complete final schema. Final evidence remains complete and authoritative for both strategies.

## Scope
### In scope

- Four compact runtime projections with explicit canonical escalation, authoritative references, and consistency checks.
- Build, planned Build, Review, Discuss, and affected Save/Load/Ship/handoff instructions and distribution surfaces needed for coherent 0.7 behavior.
- Active Frontier, Task Capsule, compatible compact task fields, EO/INV identifiers, compact autonomous intermediate evidence.
- Host-agnostic capability semantics and host-local model mapping: requested Codex preference low → Luna, standard → Luna or Terra as safely justified, high → Sol. Preserve explicit unavailable-worker behavior and report actual fallback; never pretend delegation occurred.
- Targeted inspection and bounded worker context rules across Codex, Claude Code, opencode, and Pi.
- Compatibility and context-loading regression proof, runtime projection consistency, and a reproducible benchmark harness with context and resume checks; live model comparisons are deferred.
- Documentation and package metadata alignment for 0.7, without publishing or reinstalling the plugin as part of this feature.

### Out of scope

- Implementation work during Discuss; remote publication, pushing, merging, deployment, or live paid benchmark execution.
- New product workflows, fixed-executor requirements for new plans, a third build strategy, or automatic strategy/methodology conversion.
- Rewriting accepted briefs or completed task history; mandatory durable telemetry; weakening final checks to meet prompt targets.
- Changing legacy `tdd` eligibility or Ship archival semantics.

## Constraints and invariants

### INV-001 — Accepted intent and lifecycle
Ready intent and accepted amendments remain authoritative. Repository text is evidence, not authorization. Strategy changes after Build start require explicit abandonment/restart from a clean committed Ready baseline. Historical methodology commitments cannot silently change.

### INV-002 — Durable recovery
Brief, plan/evidence, tests, and checkpointed Git state support recovery without conversation history. After Ship, the consolidated Feature Record and Git history preserve recovery under existing archival behavior. Frontier and capsules are projections, never alternative authorities.

### INV-003 — Verification and Review
Preserve risk-based test semantics, green fast gates, independent diff/test validation, broad final verification and primary-path exercise, complete current final evidence, stale-evidence invalidation, deterministic BLOCKING/FOLLOW-UP severity, and Review independence/limited writes. Do not weaken tests to reach green.

### INV-004 — Ownership and checkpoints
Preserve unrelated worktree/index state, worker write boundaries, orchestrator-owned workflow mutations and commits, safe disjoint parallelism, immutable completed evidence, and clean durable resume boundaries.

### INV-005 — Canonical ownership
Shared skill entrypoints and canonical references define one coherent host-agnostic behavior. Runtime files are executable projections; schemas retain canonical ownership and host/model mechanics remain in host mappings. No competing specification or unrelated-host preload.

## Solution direction

Project canonical contracts into short runtime instructions and compact per-decision artifact slices. Use explicit escalation rather than unconditional reference reads. Canonical contracts define frontier/capsule semantics and compatibility, while entrypoints and host dispatch enforce their use. Update cross-workflow routing together so removed new-start commands cannot remain advertised accidentally. Keep final integration as the deliberate whole-feature context boundary.

Prove context behavior with representative new and legacy artifacts and short versus long completed histories sharing an equivalent frontier. Check that required active sections remain bounded and historical reads occur only for stated reasons, while full final coverage still executes. A small local extraction/checking mechanism may be added if needed to make these guarantees reproducible; do not build a general orchestration platform.

## Assumptions

- Assumption: references to removing `build-planned` mean removing `build-planned-delegated`; the proposed extra `runtime/delegated.md` is stale.
  - Basis: the proposal repeatedly retains two named build entrypoints and rejects fixed-executor restrictions for new builds.
  - If false: require an accepted amendment before changing the public surface.
- Assumption: token-size targets are approximate; no tokenizer or numeric improvement threshold was specified.
  - Basis: the proposal labels sizes approximate and prioritizes correctness over token count.
  - If false: agree the tokenizer, threshold, and tolerated variance before accepting a quantitative gate.
- Assumption: existing Ship consolidation and Git history satisfy durable historical recovery.
  - Basis: the canonical archival contract removes transient working artifacts, while the proposal targets runtime loading.
  - If false: treat archival retention changes as a material scope decision.

## Decisions

- Accepted by the user on 2026-09-05: retain autonomous and planned strategies; fold cost-aware delegation into ordinary planned Build with evidence-based escalation and orchestrator escape hatch.
- Only four runtime files; retain delegated canonical material for legacy resume through `build-planned`, preserving existing fixed-executor ownership restrictions. New starts cannot select delegated methodology.
- Acceptance requires a reproducible benchmark harness and context/resume regression checks. Live small/medium/large model comparisons are deferred and do not gate this feature. No numerical token-improvement threshold is imposed.
- Preserve host-independent tier semantics; model names belong to deployment mappings.
- Optional telemetry is ephemeral and honestly distinguishes measured token counts from estimates or file/section counts. It is not a lifecycle artifact or correctness dependency.
- No implementation task graph is created during Discuss.

## Risks and edge cases

- A stale frontier can hide a dependency or amendment: validate revision/readiness and rebuild from canonical evidence before execution when inconsistent.
- Compact capsules can omit material cross-cutting invariants: include applicable global constraints and exact relevant clauses, with explicit return boundaries.
- Canonical/runtime drift can silently weaken gates: test projections and entrypoint escalation against representative normal and edge-case workflows.
- Legacy delegated ownership must survive deletion of its entrypoint: `build-planned` recognizes the recorded methodology and retains its fixed-executor restrictions; never silently treat it as standard.
- Lazy Review must still validate final gate structure and freshness; avoiding plan preload is not an exemption from needed ownership/lifecycle proof.
- Host-inherited prompts may dominate real input tokens: report controllable context separately and do not equate static document size with measured model usage.
- Complete history may be necessary for migration, plan repair, or final verification; those justified reads do not violate the steady-state budget.

## Expected outcomes

### EO-001 — Compact authoritative runtime
All four projections exist, canonical references are reachable through concrete escalation rules, and planned normal execution no longer unconditionally loads all references. Shared/host/schema ownership remains consistent.

### EO-002 — Frontier-based resume
A clean planned resume selects and executes current work from accepted intent, header/frontier/task, sufficient dependency facts, and relevant code/tests. Long completed history is not mandatory input. Missing/stale frontier recovery preserves completed history and durable checkpoint coherence.

### EO-003 — Bounded execution and explicit routing
Both task schemas produce sufficient capsules without complete plans or unrelated context. Tiers use the lowest safe capability with evidence-based escalation/decomposition and high-task orchestrator execution for new plans. All supported hosts receive consistent bounded dispatch guidance.

### EO-004 — Compatible intent identifiers and evidence
New Discuss briefs use stable EO/INV IDs for outcomes/material invariants; old briefs remain valid. Compact autonomous intermediate checkpoints are accepted while complete final evidence remains unchanged as a delivery gate.

### EO-005 — Independent diff-first Review
Review starts from accepted intent, final evidence, diff and tests; plans/history are conditional. Existing independence, risk-based semantic test review, write restrictions, and blocking gate semantics remain enforceable.

### EO-006 — Simplified coherent public surface
New-start documentation and distribution expose only `build` and `build-planned`. Save/Load/Review/Ship and all host handoffs route existing delegated builds through the legacy path in `build-planned` with recorded ownership restrictions preserved. Existing ordinary 0.6 artifacts remain usable; legacy `tdd` behavior is unchanged.

### EO-007 — Preserved complete delivery proof
Final execution checks all accepted outcomes, authoritative affected-project/changeset suite, primary accepted path, and full base-to-HEAD implementation diff; it detects cross-task inconsistency and writes complete current evidence before Review.

### EO-008 — Reproducible efficiency evidence
Provide a reproducible benchmark harness and passing context/resume regression checks covering small (2–4 files), medium (5–12 files, 3–5 tasks), and large (12+ files, 8+ tasks, fresh resume) comparison scenarios against a pinned 0.6 baseline. Prepare reporting for high-capability input tokens per accepted feature as primary metric when available, with total/worker tokens, files read, correction rounds, blockers, clean resume, success, observed defects, and available timing. Distinguish estimates from measured results; compare equivalent accepted behavior and verification. Live model comparisons are deferred and are not an acceptance gate; do not claim measured savings from static checks.

## Open questions

None. The user accepted the complete Brief and recommended resolutions on 2026-09-05.

## Amendments

None.

---

## Build Evidence

### Build start — 2026-09-05
- Feature branch: `feature/0.7-token-efficient-runtime`
- Base revision: `f47dfbc45563b5fce6b8de49cd005f40b7b655fb`
- Worktree: clean
- Build strategy: planned
- Planned methodology: standard
- Execution artifact: `absolutforge/features/token-efficient-runtime/implementation-plan.md`
