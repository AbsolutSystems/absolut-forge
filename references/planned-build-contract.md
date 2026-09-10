# Planned Build Contract

## Purpose

Planned execution is the higher-overhead internal strategy of `build`, alongside autonomous execution. New plans use standard methodology: a high-capability orchestrator compiles accepted intent into bounded work, while fresh workers own every production-code and test edit at low, standard and high execution risk. Existing delegated plans resume through this same entrypoint with the legacy fixed-executor contract in `planned-delegated-contract.md`; no new delegated start is allowed. Use planned Build when durable decomposition, bounded execution, or cross-session resume repays its overhead. The orchestrator owns the complete feature, decisions, lifecycle and validation, but not implementation edits.

## Active artifact and lifecycle

Planned Build owns `absolutforge/features/{slug}/implementation-plan.md`.

Plan lifecycle:

`Ready -> Executing -> Complete`

After Review returns a blocker, and only then, a `Complete` plan may reopen to `Executing`: append one `PC-` entry that preserves completed tasks, adds the bounded corrective task, increments the plan revision, and changes plan status to `Executing`. A `Complete` plan never reopens for new product intent or unrelated work.

Task lifecycle:

`pending -> in-progress -> complete`

A task may be `blocked` while the orchestrator revises the pending plan or waits for a Brief amendment. Completed task definitions and evidence are immutable.

## Canonical schema

```markdown
# Implementation Plan: {feature name}

## Status
Ready | Executing | Complete

## Context
- Feature Brief: `absolutforge/features/{slug}/feature-brief.md`
- Feature branch: `{branch}`
- Base revision: `{base_commit}`
- Plan revision: {integer starting at 1}
- Build strategy: planned
- Planned methodology: standard | delegated

## Strategy
Concise implementation architecture, ordering rationale, and integration approach.

## Active frontier
- Plan revision: {same as Context}
- Next task: none | T-NNN
- Ready tasks: none | {dependency-ready pending IDs}
- Blocked tasks: none | {ID -> dependency ID or concrete reason}

### Relevant dependency facts
- None | {T-ID: fact required by current frontier}

### Active invariants
- None | {INV-ID or heading: applicable accepted constraint text}

### Pending final-verification obligations
- {remaining primary-path and integration checks}

## Coverage
- Brief expected outcome -> task IDs and/or final verification.

## Task graph

### T-001 — {title}
- Status: pending | in-progress | complete | blocked
- Capability: low | standard | high
- Covers: {EO-IDs or exact legacy outcome headings/text}
- Depends on: none | T-NNN, ...
- Change surface: {bounded repository-relative production and test paths}
- Preserves: {INV-IDs or relevant invariant text and material exclusions}
- Implementation intent: {one coherent result, responsibility and integration approach}
- Test obligations: {applicable risks and observable behaviors from verification-doctrine.md} | none — {exemption reason}
- Risk controls: none | {for high execution: settled decision; assumptions; failure containment; rollback when applicable; intermediate proof obligations}
- Return boundary: {evidence or decisions that require returning to the orchestrator}
- Verification: {fast task-owned unit-test targets and cheap build/type/lint checks}
- Completion evidence: pending | {changed paths; tests and cases; commands/green results; local decisions; new dependency or invariant facts; delegated return and orchestrator validation when applicable}

## Final verification
- Changed/new tests, focused affected regression targets, targeted integration/e2e checks for changed boundaries, and the primary accepted path. Name any broad suite deferred to required PR CI; require canonical justification for a local full suite.

## Plan changes
None yet, or append entries below.
```

For plans created before `Planned methodology` existed, absence means `standard`. Legacy `tdd` plans remain historical evidence but cannot be started or resumed by the current builders; see `planned-delegated-contract.md`.

Existing tasks with `Goal`, `Invariants`, `Implementation guidance`, `Watch points`, and `Decision boundary` remain valid unchanged. Capsule generation combines those fields into Outcome, Must preserve, Implement and Return boundary without dropping their obligations. Legacy delegated tasks retain their execution-owner and guidance requirements. Do not rewrite completed definitions or evidence to modernize a schema.

## Task design

Use the smallest useful acyclic graph. Map every accepted Expected Outcome to tasks or final verification. Put shared contracts before consumers and give each task one bounded production write surface.

For new standard plans, prefer one coherent behavior slice per task, including implementation, wiring and focused tests across the necessary files. For example, filtering a list with input validation and regression tests is one task when its contracts are settled; separate function, caller and test tasks only add handoffs without independent value. Split for a real dependency, independently verifiable result, ownership conflict, or material risk/context boundary. Do not split solely by file, layer or code-versus-test work, and do not merge unrelated outcomes just to reduce task count. No fixed file/task count sets the boundary.

For every adjacent task or outcome boundary, ask whether it provides concrete recovery, dependency ordering, independent acceptance, write ownership, risk containment or context value. If it provides none, merge the adjacent work into one coherent slice. Record the actual reason when retaining a boundary; checkpoint durability alone does not justify avoidable owner or worker rehydration.

A broader task still needs settled shared contracts, explicit production/test ownership, sufficient relevant context, concrete test obligations, a meaningful fast gate and a return boundary. If those do not fit one bounded capsule, split coherently or return the unresolved decision to the orchestrator; higher worker reasoning effort does not authorize wider scope. Architecture, migration strategy, security/data policy, concurrency semantics and other material ambiguity must be settled by the orchestrator before dispatch. If owner acceptance is required between implementation phases, split at that real dependency boundary. Grouping never removes targeted final integration checks or permits overlapping parallel writes.

Do not encode an unresolved high-tier decision inside an implementation task. At compilation, investigate and record that decision before defining or dispatching the coherent implementation task. Classify the resulting task on its execution risk: it may remain `high` when applying the settled decision still crosses a migration, security/data, concurrency/state, large-blast-radius or similarly sensitive boundary. Such a task stays worker-owned and must carry explicit Risk controls. This is a real decision/risk boundary, not permission to fragment by file or encode most of the patch in a worker capsule.

Apply this granularity policy when compiling new standard plans. Existing completed task definitions and evidence remain unchanged. On resume, pending standard tasks adopt the worker-owned runtime boundary; this ownership transition alone does not rewrite their definitions. A pending `high` task created before `Risk controls` existed must be blocked and receive a canonical PC entry supplying those controls before dispatch. Other pending definition changes still require a PC entry. Legacy delegated ownership and decomposition rules remain authoritative.

A task states WHAT result must change, WHERE responsibility lives, WHY its invariants matter, and HOW correctness will be demonstrated. It does not prescribe method bodies, helper decomposition, naming, pseudo-patches, or ordered edit scripts. If safe execution appears to require describing most of the patch, the orchestrator must improve the decision boundary, evidence or decomposition rather than implement it in prose. Under standard methodology every production-code and test task remains worker-owned; legacy delegated methodology retains its separate fixed-executor constraints.

Every behavior-changing task carries concrete `Test obligations` derived from `verification-doctrine.md`. Name the applicable risks and observable behavior, not a test count or implementation recipe. Test paths belong to the task's change surface. Keep unit tests in the fast task gate and require green results; map risks observable only across a real integration boundary to final verification.

Two tasks never own the same production path or new test file. They may add separately named cases to an existing test file, but tasks sharing any writable path must execute sequentially and may not be in the same parallel wave. The delegated methodology executes one fixed-executor task at a time under `planned-delegated-contract.md`.

## Dispatch and waves

Under standard methodology, select only dependency-ready tasks and dispatch each to a fresh worker. A parallel wave is allowed only when every task in the wave has a fully disjoint write surface and all shared contracts are already complete. Direct orchestrator implementation is unavailable. Delegated methodology dispatches one dependency-ready task at a time to its fixed executor under `planned-delegated-contract.md`; parallel waves remain unavailable.

Give a worker one generated Task Capsule (below), exact relevant Brief/ADR/rule clauses and sufficient direct-dependency facts, plus relevant source/tests. Do not send the full plan, unrelated Brief sections, all ADRs, full verification doctrine, completed history or worker dialogue. Binding repository guidance still applies; omit unrelated guidance, never required instructions. The task is incomplete until its tests meaningfully cover the applicable repository-owned behavior and its fast gate is green. A worker may inspect neighboring code but may write only inside its surface. It never edits the Brief, plan, other tasks, review, branch history, remote state, or existing tests merely to reach green.

After return, the orchestrator independently inspects the task diff and test value, confirms the write boundary and the inventory of exact test files/cases added or changed, and reruns the fast task gate when evidence is incomplete or stale. It rejects tests that mainly validate mocks, framework behavior, or incidental implementation details instead of the task's observable contract. Only then does it fill Completion Evidence, mark the task complete, and create the task checkpoint commit. Under standard methodology, results from a parallel wave are validated and committed one task at a time by staging only that task's paths.

## Context rotation

Treat the active orchestrator context as disposable. At every completed-task boundary, the committed Brief, plan, source, tests, and Git history must be sufficient for a fresh high-capability orchestrator to continue without the previous conversation.

Durable state has one owner:

- accepted intent: Brief and amendments;
- execution order and pending work: current plan;
- completed work and new dependency/invariant facts: task Completion Evidence;
- implementation truth: checkpointed Git state;
- plan corrections: `PC-` entries;
- verification truth: committed tests and named commands/results.

Do not copy raw worker conversations, full logs, or facts already recoverable from Git into the plan. After a task is validated, reduce its result to concise durable evidence and let the raw interaction leave active context.

At a clean task boundary, resume through `build` with the canonical Brief for both standard and legacy delegated state, preserving recorded methodology. `save` is unnecessary because the plan and Git are the resume record. Use `save` when stopping mid-task or while unresolved context exists that has not reached a durable task or `PC-` boundary. Save still does not preserve dirty source by itself.

Use the active host's fresh-owner continuation after a substantial standard-methodology checkpoint, a `PC-` change or a long diagnosis, and before a substantial standard `high` task or final integration. If the host has no such primitive, compact to durable current facts and continue. Use no fixed task count. Normal resume reads runtime, Brief status and accepted intent/amendments, plan header and Active Frontier, current task, and relevant code/tests. Load completion evidence only for direct dependencies whose necessary facts are absent or uncertain. Do not preload all completed bodies, plan-change history, full schemas/doctrine, unrelated host mappings or the base-to-HEAD diff. Use current code as implementation truth; individual checkpoint diffs need a concrete regression, ownership or history question.

## Active Frontier rules

The frontier is mutable derived state owned by the orchestrator. Refresh it after completion, blocking, accepted PC changes or any dependency-readiness change, and commit it with the associated checkpoint. Ordinary frontier refresh does not increment plan revision; a PC change does. Validate its revision against Context and verify selected task status and direct dependencies before dispatch. Completed dependencies must have committed completion evidence; frontier summaries never override the task graph or accepted intent. Missing, stale, contradictory or ambiguous facts require targeted reconstruction, not guessed readiness.

When a legacy plan has no frontier, read enough task status/dependency state once to derive it, validate and persist it before continuing. This may require a broad read once; it does not authorize a broad preload on subsequent resumes. Preserve completed definitions/evidence. A stale frontier follows the same repair path. Do not copy raw dialogue, full completion records, every prior result or facts trivially recovered from current code. Include only active facts and applicable invariants; outstanding whole-feature obligations remain visible until final verification.

## Task Capsule

The capsule is generated execution context, not a second durable task authority. Canonical task metadata remains in the plan. Use this projection for both task shapes:

```markdown
# Task T-004 — {title}
## Outcome
{Covers resolved to accepted outcome text, or legacy Goal and coverage}
## Own
{exact production and test write surface}
## Must preserve
{Preserves resolved to accepted text, legacy Invariants/Watch points, applicable global constraints and direct dependency facts}
## Implement
{Implementation intent or legacy Implementation guidance; responsibility and approach}
## Prove
{concrete Test obligations, including any valid exemption}
## Verify
{exact fast commands}
## Return instead of guessing if
{Return boundary or legacy Decision boundary and material Watch points}
## Risk controls
{for high execution: settled decision, assumptions, failure containment, rollback when applicable, and intermediate proof obligations; otherwise none}
```

Include enough exact clauses to preserve meaning: unresolved EO/INV IDs are insufficient, and untagged global constraints are not optional. Include the canonical Scout rule in `Must preserve` and `Return instead of guessing if`: a worker may make a qualifying maintenance fix only inside `Own`, with focused proof, and must return larger, behavior-changing or cross-owner observations without editing them. Do not duplicate all durable fields after generating the capsule. In legacy plans without explicit guidance, derive the approach/boundary from relevant evidence; return ambiguity to the orchestrator. Workers never expand their write boundary to fix an invalid plan or scout observation. Inspect named symbols/paths, direct callers, targeted tests and dependency-local files before broader searches.

## Capability routing

Use the lowest capability tier that accurately describes execution risk under Task design. Low covers mechanical/local work with explicit contracts and fast gates; standard covers bounded multi-file behavior with settled contracts, implementation/wiring and focused tests; high covers execution across migration, security/data, concurrency/state, large-blast-radius or similarly sensitive boundaries after the controlling decisions are settled. Decision risk and execution risk are separate: unresolved intent, architecture, migration strategy, data policy, security semantics or concurrency behavior returns to the orchestrator before dispatch and is never hidden inside a `high` task. Do not fragment work merely to lower its tier or downgrade risk because a worker has more reasoning effort. Evidence of underestimated complexity requires a PC revision escalating the pending task or splitting it at a real boundary. A worker fixes local failures, repeats its fast gate and reports every high-risk proof obligation inside the current task. Failures discovered later by orchestrator validation or final verification first receive an owner decision and corrected contract when needed, then every production-code and test correction returns to a fresh bounded worker. Two failed attempts at the same blocker require re-opening the decision or decomposition rather than a substantially identical third capsule. Legacy delegated restrictions remain in force. Model names, reasoning profiles and unavailable-dispatch mechanics belong in the active host mapping.

## Plan changes

When repository evidence invalidates a pending task, dependency, or change surface without changing accepted intent, block the affected task and append one entry:

```markdown
### PC-{NNN} — YYYY-MM-DD
- Evidence: {path/symbol/check/result, or consultation report and C-IDs}
- Reason: {invalidated assumption or accepted consultation finding}
- Preserved completed tasks: none | {IDs}
- Revised pending tasks: none | {IDs and change}
- Removed pending tasks: none | {IDs and reason}
- Added tasks: none | {IDs and reason}
- Dependency changes: none | {changes and reason}
- Plan revision: {old} -> {new}
- Validation: outcomes covered; dependencies acyclic; write surfaces valid; test obligations complete; no intent expansion
```

Revise only the affected pending frontier and preserve completed evidence. Return blocked tasks to `pending` when the revised contract is executable.

If evidence would change behavior, scope, public contract, security/data handling, migration, or material cost, stop for an explicit Brief amendment. After acceptance, record the amendment as the reason for the next `PC-` entry before continuing.

An optional consultation report is evidence, not plan state. The orchestrator decides whether its findings still apply, records accepted plan findings through a `PC-` entry, and leaves the report unchanged. Consultation is never required and never automatically offered by Build.

## Completion

Mark the plan `Complete` only when every task is complete, Expected Outcome coverage still holds, final whole-feature verification passes, the complete implementation diff has been inspected against the Brief, and the final Build Evidence satisfies the delivery gate in `artifact-contracts.md`. Final verification uses the doctrine's affected test set and targeted integration policy; the mere fact that this is the final gate does not require a full suite. Any later source or test change invalidates that gate and requires a new final-verification attempt and final evidence entry before Review handoff. For a long Build, prefer performing this final integration pass from a fresh orchestrator context rehydrated from the durable artifacts.

If final verification fails before completion, preserve completed tasks and append one `PC-` entry adding a bounded corrective task with a new plan revision. Execute and checkpoint it under the selected planned methodology, then repeat final verification.
