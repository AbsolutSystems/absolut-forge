# Planned Build Contract

## Purpose

`build-planned` is the higher-overhead alternative to autonomous `build`. `build-planned-tdd` uses the same first-class planned strategy and artifact with the additional methodology contract in `planned-tdd-contract.md`. Use planned Build when a feature benefits materially from durable decomposition, bounded delegation, or cross-session resume. The high-capability orchestrator remains owner of the complete feature and validates every result.

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
- Planned methodology: standard | tdd

## Strategy
Concise implementation architecture, ordering rationale, and integration approach.

## Coverage
- Brief expected outcome -> task IDs and/or final verification.

## Task graph

### T-001 — {title}
- Status: pending | in-progress | complete | blocked
- Capability: low | standard | high
- Goal: {one coherent result}
- Depends on: none | T-NNN, ...
- Change surface: {bounded repository-relative production and test paths}
- Invariants: {task-local and cross-boundary rules; explicit exclusions when material}
- Test obligations: {applicable risks and observable behaviors from verification-doctrine.md} | none — {exemption reason}
- TDD mode: required | characterization | exempt — {reason}  (tdd methodology only)
- TDD evidence: pending | {ordered cycle evidence} | exempt — {reason and closest check}  (tdd methodology only)
- Verification: {focused commands/checks}
- Completion evidence: pending | {changed paths; tests and cases; commands/results; local decisions; new dependency or invariant facts}

## Final verification
- Whole-feature integration/build/test checks, including the primary accepted path.

## Plan changes
None yet, or append entries below.
```

For plans created before `Planned methodology` existed, absence means `standard`.

## Task design

Use the smallest useful acyclic graph. Map every accepted Expected Outcome to tasks or final verification. Put shared contracts before consumers and give each task one bounded production write surface.

A task states WHAT result must change, WHERE responsibility lives, WHY its invariants matter, and HOW correctness will be demonstrated. It does not prescribe method bodies, helper decomposition, naming, pseudo-patches, or ordered edit scripts. If safe delegation would require describing most of the patch, mark the task `high` and keep it with the orchestrator.

Every behavior-changing task carries concrete `Test obligations` derived from `verification-doctrine.md`. Name the applicable risks and observable behavior, not a test count or implementation recipe. Test paths belong to the task's change surface.

Two tasks never own the same production path or new test file. They may add separately named cases to an existing test file, but tasks sharing any writable path must execute sequentially and may not be in the same parallel wave. The TDD methodology is stricter and executes only one task at a time under `planned-tdd-contract.md`.

## Dispatch and waves

Select only dependency-ready tasks. Execute one directly or dispatch a parallel wave only when every task in the wave has a fully disjoint write surface and all shared contracts are already complete.

Give a worker one task contract, the minimum relevant Brief/ADR/rule and dependency facts, its write boundary, and verification commands. The task is incomplete until its tests exist and pass. A worker may inspect neighboring code but may write only inside its surface. It never edits the Brief, plan, other tasks, review, branch history, remote state, or existing tests merely to reach green.

After return, the orchestrator independently inspects the task diff and test value, confirms the write boundary, and reruns focused checks when evidence is incomplete or stale. Only then does it fill Completion Evidence, mark the task complete, and create the task checkpoint commit. Results from a parallel wave are validated and committed one task at a time by staging only that task's paths.

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

At a clean task boundary, resume directly by invoking the planned builder matching `Planned methodology` with the canonical Brief: `build-planned` for `standard`, or `build-planned-tdd` for `tdd`. `save` is unnecessary because the plan and Git are the resume record. Use `save` when stopping mid-task or while unresolved context exists that has not reached a durable task or `PC-` boundary. Save still does not preserve dirty source by itself.

Rotate to a fresh session when context pressure risks losing intent or causal reasoning, especially after a large wave, a `PC-` change, or a long diagnosis, and before a substantial `high` task or final integration when practical. Use no fixed task count. On resume, rehydrate from the complete Brief, current plan and Git, then load only the pending task, completion evidence of its dependencies, and relevant code/tests.

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

Mark the plan `Complete` only when every task is complete, Expected Outcome coverage still holds, final whole-feature verification passes, and the complete implementation diff has been inspected against the Brief. For a long Build, prefer performing this final integration pass from a fresh orchestrator context rehydrated from the durable artifacts.
