# Planned Build Contract

## Purpose

`build-planned` is an alternative implementation strategy for the same immutable Ready Feature Brief consumed by autonomous `build`. The strong primary model remains the Build owner: it creates and maintains the implementation plan, delegates bounded tasks when useful, validates worker results, integrates the whole feature, and owns final verification.

## Active artifact

Planned Build owns one transient artifact:

`absolutforge/features/{slug}/implementation-plan.md`

The plan is implementation evidence, not product intent and not a partial release unit. Review and Ship remain whole-feature stages.

## Plan lifecycle

`Draft -> Ready -> Executing -> Needs Replan -> Executing -> Complete`

Task lifecycle:

`pending -> in-progress -> complete`

A task may become `blocked`; execution cannot continue through that task until the orchestrator records a replan, accepted Brief amendment, or bounded diagnostic resolution.

## Canonical schema

```markdown
# Implementation Plan: {feature name}

## Status
Draft | Ready | Executing | Needs Replan | Complete

## Revision
{integer starting at 1}

## Context
- Feature Brief: `absolutforge/features/{slug}/feature-brief.md`
- Feature branch: `{branch}`
- Base revision: `{base_commit}`
- Build strategy: planned

## Strategy
Concise implementation architecture, ordering rationale, and integration approach.

## Global invariants
- Cross-task behavior, compatibility, security/data, architecture, and scope invariants.

## Coverage
- Brief expected outcome -> task IDs and/or final verification.

## Task graph

### T-001 — {title}
- Status: pending | in-progress | complete | blocked
- Capability: low | standard | high
- Goal: {one coherent result}
- Depends on: none | T-NNN, ...
- Change surface: {repository-relative modules/paths; symbol anchors only when they identify ownership/integration boundaries, never as an edit checklist}
- Required behavior: {what must become true}
- Constraints and invariants: {task-local rules and explicit exclusions}
- Implementation guidance: {WHAT/WHERE/WHY plus verification-relevant guidance; omit local HOW unless a specific mechanism is binding}
- Verification: {focused commands/checks}
- Completion evidence: pending | {changed areas; checks/results; local decisions}
- Deviation: none | D-NNN

## Final verification
- Whole-feature integration/build/test checks.

## Deviations and replans
None yet, or append entries below.
```

## Task design

A task is a bounded execution contract, not a checklist item. The orchestrator owns decomposition, dependency order, change-surface accuracy, cross-task contracts and verification design. A worker owns only local coding choices inside the task boundary.

Do not encode new product intent in tasks. A behavior/scope/public-contract/security/data/migration/material-cost change requires a Feature Brief amendment.

Avoid over-planning. Do not turn a one-file mechanical change into many tasks. Prefer the smallest graph that externalizes decisions a cheaper worker would otherwise need to rediscover.

### Planner/executor abstraction boundary

Write each task as an execution contract, not code in prose. Specify:

- **WHAT** observable result or contract must change;
- **WHERE** responsibility and write boundaries live at module/path level, with only useful ownership or integration symbol anchors;
- **WHY** constraints, ordering, dependencies, and invariants matter; and
- **HOW correctness is verified** with focused evidence.

Do **not** prescribe local implementation HOW: method-body structure, exact helper decomposition, equivalent API call ordering, variable names, line-relative edits, pseudo-diffs, code snippets that effectively dictate the patch, or a symbol-by-symbol edit sequence. A worker must retain meaningful local engineering ownership.

A specific implementation mechanism may be mandatory only when its necessity is evidenced by the accepted Brief/amendment, a linked ADR or binding project rule, or concrete compatibility/security/data constraints that leave no materially equivalent safe choice. State that evidence as a constraint. Do not elevate a planner preference into a task requirement.

If safe delegation would require the planner to describe most of the patch, do not increase plan detail. Route the task as `high` and let the primary orchestrator implement it directly.

## Worker dispatch contract

Give a worker only:

- one task contract;
- the minimum relevant accepted Brief/ADR/rule context;
- dependency completion facts needed by that task;
- relevant repository paths/symbols/tests;
- explicit write boundary and verification command(s).

The worker may inspect neighboring code needed to implement the task, but may write only inside the approved task change surface unless the orchestrator expands it after evidence review. It returns changed paths, verification evidence, local decisions, and any deviation. It never edits the Feature Brief, plan lifecycle, other task definitions, review artifact, branch history, remote state, or release state.

## Deviation

Append; never rewrite prior deviation history.

```markdown
### D-{NNN} — YYYY-MM-DD — T-{NNN}
- Classification: plan deviation | intent deviation
- Observable evidence: {path/symbol/check/result}
- Planned assumption invalidated: {precise assumption or boundary}
- Execution state: {coherent completed work and remaining work}
- Affected tasks: {blocked task and likely pending dependents}
- Required next action: replan | amendment
- Resolution: open | replanned in R-NNN | amended by A-N
```

A plan deviation means the accepted intent is still valid but the decomposition, dependency, repository assumption, or change surface is wrong. An intent deviation means implementation evidence would change accepted behavior or another material Brief boundary.

## Replan

Only the high-capability orchestrator may replan. Preserve completed task evidence.

```markdown
### R-{NNN} — YYYY-MM-DD
- Trigger: D-{NNN}
- Evidence reviewed: {repository-relative evidence}
- Preserved completed tasks: {IDs}
- Revised tasks: {IDs}
- Removed pending tasks: none | {IDs and reason}
- Added tasks: none | {IDs and reason}
- Dependency changes: none | {changes and reason}
- Plan revision: {old} -> {new}
- Validation: coverage complete; dependencies acyclic; no intent expansion
```

Replan the blocked task and transitive pending frontier only, unless evidence proves a broader pending frontier invalid. Never rewrite completed task history to hide divergence.

## Completion

The orchestrator marks the plan `Complete` only when every task is complete, coverage still maps every accepted Brief outcome, final whole-feature verification passes, and the complete diff is inspected against the Brief. Planned Build then follows the same `In Review` handoff contract as autonomous Build.
