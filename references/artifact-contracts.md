# AbsolutForge Delivery Artifact Contracts

**Status:** Canonical dual-build contract.

## Active layout

```text
absolutforge/features/{slug}/
├── feature-brief.md
├── execution-map.md          # optional; autonomous build only
├── implementation-plan.md    # planned build only
├── consult-{slug}.md         # optional; one consultation report per feature
├── save-{slug}.md            # optional during either Building strategy
└── review.md
```

After Ship:

```text
absolutforge/archives/{slug}/
├── feature-record.md
└── executive-summary.html    # optional
```

`execution-map.md` and `implementation-plan.md` are mutually exclusive for a normal feature. They, `consult-{slug}.md` and `save-{slug}.md` are transient evidence and are removed at Ship after useful facts are consolidated into the Feature Record.

## Lifecycle

```text
Draft -> Ready -> Building -> In Review -> Shipped
```

`Ready` is the immutable intent baseline. The explicit invocation of either `build` or `build-planned` selects the feature's Build strategy. `Building` resumes only through that selected strategy. A Review blocker returns to the selected strategy. Switching strategy requires human abandonment/restart from a clean committed Ready baseline, never silent conversion of in-progress execution state.

## Feature Brief

```markdown
# Feature: {name}

## Status
Draft | Ready | Building | In Review

## Change type
Feature | Fix | Refactor

## Problem and goal

## Users

## Current state and evidence

## Expected behavior

## Scope
### In scope
### Out of scope

## Constraints and invariants

## Solution direction

## Assumptions
- Assumption
- Basis
- What Build must do if false

## Decisions

## Risks and edge cases

## Expected outcomes

## Open questions

## Amendments
### A-{N} — YYYY-MM-DD
- Status: Proposed | Accepted | Rejected
- Reason:
- Change:
- Accepted by:

---

## Build Evidence
```

The immutable Ready baseline is `## Problem and goal` through `## Expected outcomes`, plus accepted amendments. Build may change lifecycle status and append Build Evidence only.

## Build start evidence

Append exactly once before the first source edit:

```markdown
### Build start — YYYY-MM-DD
- Feature branch: `{branch}`
- Base revision: `{base_commit}`
- Worktree: clean
- Build strategy: autonomous | planned
- Execution artifact: none | `absolutforge/features/{slug}/execution-map.md` | `absolutforge/features/{slug}/implementation-plan.md`
```

A dirty worktree, detached HEAD, or uncommitted Ready Brief blocks Build start.

## Build evidence

Append after coherent verified outcomes/tasks and after final verification:

```markdown
### Build evidence — YYYY-MM-DD
- Base revision / review diff: `{base_commit}..HEAD`
- Build strategy: autonomous | planned
- Changed areas: {repository-relative areas}
- Tests added/updated: {test paths and cases} | none — {exemption reason and observable check performed instead}
- Verification commands and results: {command -> pass|fail}
- Whole-feature path exercised: final entry only — {integration-level check and result} | not available — {reason and closest check performed}
- Execution state: {autonomous outcomes/checkpoints OR planned task IDs/plan revision}
- Material implementation decisions: none | {decision}
- Deviations from accepted baseline: none | {accepted amendment}
- Plan deviations/replans: not applicable | none | {D/R IDs}
- Scout disposition: none | {result}
- Documentation maintenance: none | {result}
- Durable memory lesson: none | {candidate}
```

## Autonomous Execution Map

Autonomous `build` may create `execution-map.md` for dependent outcomes, meaningful uncertainty or durable resume. It is outcome-oriented, not a task recipe.

```markdown
# Execution Map: {feature name}

## Status
pending | in-progress | complete

## Build start
- branch: {branch}
- base_commit: {base_commit}

## Checkpoints
- None yet | {commit}: {verified outcome}; verification: {result}

## Section {N}: {outcome}
- Status: pending | in-progress | complete
- Goal:
- Boundaries:
- Dependencies:
- Tests: {behavior to assert} | none — {exemption reason}
- Verification:
- Result:
- Material deviations:
```

## Planned Implementation Plan

The exact planned schema, task contract, deviations and replans are owned by [`planned-build-contract.md`](planned-build-contract.md). A planned feature must have `implementation-plan.md` before the first delegated source edit. The high-capability orchestrator owns all plan mutations.

## Consultation report

`consult` writes exactly one report per feature at `absolutforge/features/{slug}/consult-{slug}.md`, appending a new block per consultation. The report exists so a consultation can run in a separate session or a different model family and be read back by the original context.

```markdown
# Consultation report: {feature name}

## Consultation {N} — YYYY-MM-DD
- Subject: `{feature-brief.md | implementation-plan.md path}`
- Mode: brief | plan
- Subject status: {Draft | Ready | Needs Replan}
- Plan revision: not applicable | {integer}
- Additional context read: none | {repository-relative paths}
- Result: no material findings | {count} findings

### C-{NNN} — {class}
- Evidence: {exact Brief section, task ID, or repository path}
- Impact: {concrete consequence if the artifact is used unchanged}
- Proposed change: {smallest sensible change}
- Disposition: open | accepted | rejected | routed to Brief amendment
```

`C-` IDs are numbered from `C-001` and continue across consultation blocks within the report; they are never reused and never written into the Brief, plan, execution map or review. Findings are always written at `Disposition: open`. Only the context that consumes the report sets any other disposition — the Build owner for a plan consultation, or the Brief-mode `consult` session acting on explicit per-ID human acceptance — and it never rewrites a recorded finding, its evidence or its proposed change.

The report is advice, not authority. It changes no status, and it is never an input to `review`: Review reads the Brief as intent and `base_commit..HEAD` as truth.

## Save

```markdown
# Build save: {feature name}

## Status
Saved

## Context
- Feature Brief:
- Build strategy: autonomous | planned
- Execution artifact: none | execution-map path | implementation-plan path
- Feature branch:
- Base revision:
- Current revision:
- Saved at:

## Completed work

## Current work

## Next action

## Open items

## Resume notes
```

Save is context only; it does not preserve dirty source by itself.

## Review

```markdown
# Review: {feature name}

## Status
In Review | Complete

## Context
- Feature Brief:
- Build strategy: autonomous | planned
- Base revision:
- Reviewed revision:
- Review range:
- Execution artifact read: none | execution-map | implementation-plan

## Findings
### F-{NNN} — BLOCKING | FOLLOW-UP
- Evidence:
- Impact:
- Smallest sensible correction:
- Resolution: open | fixed | accepted | deferred
- Resolution details:

## Review passes
### Pass {N} — YYYY-MM-DD
- Mode: fresh | advisory (not fully isolated)
- Scope:
- Outcome:

## Decision
Fixes required | Ready for ship
```

Review treats the Brief as intent authority, source/tests and `base_commit..HEAD` as implementation truth, and execution artifacts only as supporting evidence. It never excuses a Brief violation because the plan/map said otherwise.

## Feature Record

Ship archives one record containing original intent, accepted amendments, as-built result, verification, Review findings, deviations, build strategy, execution summary, durable knowledge, follow-ups and recommended review order. Planned Build includes plan revision count, task outcomes, deviations/replans and final integration verification. Autonomous Build includes execution-map/checkpoint facts when present.
