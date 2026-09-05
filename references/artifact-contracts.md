# AbsolutForge Delivery Artifact Contracts

**Status:** Canonical dual-build contract.

## Active layout

```text
absolutforge/features/{slug}/
├── feature-brief.md
├── execution-map.md          # optional; autonomous build only
├── implementation-plan.md    # planned build, standard or delegated methodology
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

`Ready` is the immutable intent baseline. Exactly two new-start commands exist: `build` selects `autonomous`; `build-planned` selects `planned` with methodology `standard`. The separate `build-planned-delegated` entrypoint is removed. Existing `delegated` builds resume through `build-planned` under the unchanged fixed-executor restrictions in `planned-delegated-contract.md`; this routing change does not convert their methodology. `Building` resumes only through the recorded strategy and methodology. A Review blocker returns to the matching builder. Switching strategy or methodology requires human abandonment/restart from a clean committed Ready baseline, never silent conversion of in-progress execution state.

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

New Discuss briefs give Expected Outcomes stable `### EO-001 — {title}` headings and material Constraints and invariants stable `### INV-001 — {title}` headings. IDs are unique within their category and remain stable after acceptance; amendments introduce new IDs rather than reassigning existing ones. Do not ID every paragraph. Older briefs without IDs remain valid unchanged: use headings and exact text matching. A task's `Covers` and `Preserves` references resolve to accepted text, including applicable amendments; an ID alone is not sufficient executor context. Ambiguous references require targeted inspection or clarification, never guessed intent.

## Ready acceptance checkpoint

Explicit human acceptance authorizes `discuss` to set the complete Brief to `Ready` and create its local acceptance commit. The commit contains exactly `absolutforge/features/{slug}/feature-brief.md`; unrelated staged or dirty paths and an optional consultation report remain outside it. Discuss verifies the committed Ready content and changed path before handing off to Build, and reports the revision. An identical Ready Brief already committed at HEAD is reused without an empty commit.

Discuss requires a non-detached intended feature branch before requesting final acceptance. Commit failure leaves the Ready Brief intact but blocks Build handoff until resolved; Discuss never amends, rewrites history, pushes, or commits another path as part of acceptance.

## Build start evidence

Append exactly once before the first source edit:

```markdown
### Build start — YYYY-MM-DD
- Feature branch: `{branch}`
- Base revision: `{base_commit}`
- Worktree: clean
- Build strategy: autonomous | planned
- Planned methodology: not applicable | standard | delegated
- Execution artifact: none | `absolutforge/features/{slug}/execution-map.md` | `absolutforge/features/{slug}/implementation-plan.md`
```

Artifacts created before the methodology field was introduced remain valid: absence means `not applicable` for autonomous Build and `standard` for planned Build. Legacy value `tdd` remains valid historical evidence but cannot be selected or resumed by a current builder.

A dirty worktree, detached HEAD, or uncommitted Ready Brief blocks Build start. An uncommitted `consult-{slug}.md` is the one exception: a consultation may run between the committed Ready Brief and Build start, so the report is a permitted uncommitted workflow artifact there, exactly as the active `review.md` is at Review. Any uncommitted source change still blocks Build start.

Before any source edit, the selected builder appends this evidence, changes the Brief to `Building`, and creates a local Build-start checkpoint commit. Planned Build later commits its validated Ready plan before its first source edit. Every verified outcome or task receives an orchestrator-owned checkpoint commit, and final evidence plus the `In Review` transition receive a final handoff commit. Workers never commit.

## Build evidence

Autonomous Build appends evidence after coherent verified outcomes and after final verification. Planned Build keeps per-task evidence in `implementation-plan.md` and appends one consolidated Build evidence entry only after final verification, avoiding duplicate state in the Brief.

```markdown
### Build evidence — YYYY-MM-DD
- Base revision / review diff: `{base_commit}..HEAD`
- Build strategy: autonomous | planned
- Planned methodology: not applicable | standard | delegated
- Changed areas: {repository-relative areas}
- Tests added/updated: {test paths and cases} | none — {exemption reason and observable check performed instead}
- Verification commands and results: {command -> pass|fail}
- Whole-feature path exercised: {integration-level check and result} | not available — {reason and closest whole-feature check performed}  (final entry only)
- Execution state: {autonomous outcomes/checkpoints OR planned task IDs/plan revision}
- Material implementation decisions: none | {decision}
- Deviations from accepted baseline: none | {accepted amendment}
- Plan changes: not applicable | none | {PC-IDs}
- Scout disposition: none | {result}
- Documentation maintenance: none | {result}
- Durable memory lesson: none | {candidate}
```

The `(final entry only)` marker is not part of the recorded value. The final entry writes that field without the marker and includes every other field above. New autonomous intermediate entries use this compact schema instead:

```markdown
### Outcome checkpoint — O-003
- Commit: {checkpoint revision or this checkpoint, resolved through Git}
- Result: {verified accepted outcome}
- Tests: {named cases; commands and results} | none — {reason and observable check}
- New durable facts: none | {facts needed by later work}
```

An entry included in its own checkpoint uses `this checkpoint`; resolve it from the commit introducing the entry, avoiding an impossible self-referential hash. Existing full intermediate entries remain valid append-only history. Compact intermediate evidence never substitutes for the complete final delivery gate.

Legacy Build Evidence and completed planned-task evidence may retain `Test binding proofs` fields created under the previous mutation-proof policy. Do not rewrite append-only history, but omit that field from new evidence; its presence or absence is no longer a delivery gate.

The final Build Evidence entry is a delivery gate, not optional documentation. It must use the complete current schema, describe verification of the implementation state handed to Review, and contain a valid `Whole-feature path exercised` value under `verification-doctrine.md`. A later source or test change invalidates that final entry; the matching builder must repeat affected final verification and append a new final entry before setting the Brief to `In Review` again. Lifecycle-only and Review-artifact commits do not invalidate it.

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
- Test obligations: {applicable risks and observable behaviors} | none — {exemption reason}
- Verification: {fast unit-test targets and cheap build/type/lint checks}
- Result:
- Material deviations:
```

## Planned Implementation Plan

The exact planned schema, Active Frontier, Task Capsule, and `PC-` change log are owned by [`planned-build-contract.md`](planned-build-contract.md). Legacy fixed-executor behavioral deltas are owned by [`planned-delegated-contract.md`](planned-delegated-contract.md) and loaded only for recorded `delegated` state. A planned feature must have a committed `implementation-plan.md` before the first source edit. The high-capability orchestrator owns all plan mutations and task checkpoint commits.

## Consultation report

`consult` writes one report per feature at `absolutforge/features/{slug}/consult-{slug}.md`, appending an immutable block per consultation. The report is optional evidence and never controls lifecycle state.

```markdown
# Consultation report: {feature name}

## Consultation {N} — YYYY-MM-DD
- Subject: `{feature-brief.md | implementation-plan.md path}`
- Mode: brief | plan
- Subject status: {Draft | Ready | Executing}
- Subject revision: {git HEAD}
- Plan revision: not applicable | {integer}
- Additional context read: none | {repository-relative paths}
- Result: no material findings | {count} findings

### C-{NNN} — {class}
- Evidence: {exact Brief section, task ID, or repository path}
- Impact: {concrete consequence if the artifact is used unchanged}
- Proposed change: {smallest sensible change}
```

`C-` IDs are numbered from `C-001` and continue across consultation blocks; they are never reused. Earlier blocks and findings are never edited. The receiving `discuss` or Build context decides whether a finding still applies and records accepted changes in its own Brief amendment or plan-change entry. The report itself carries no disposition.

The report is advice, not authority. Duplicate or stale consultations are harmless evidence. Review reads the Brief as intent and `base_commit..HEAD` as truth; a consultation never excuses a Brief violation.

## Save

```markdown
# Build save: {feature name}

## Status
Saved

## Context
- Feature Brief:
- Build strategy: autonomous | planned
- Planned methodology: not applicable | standard | delegated
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

Save is context only; it does not preserve dirty source by itself. At a clean planned-task boundary, the committed plan and Git state are already the canonical resume record, so Save is normally unnecessary. Use it for a mid-task or otherwise unresolved stop.

## Review

```markdown
# Review: {feature name}

## Status
In Review | Complete

## Context
- Feature Brief:
- Build strategy: autonomous | planned
- Planned methodology: not applicable | standard | delegated
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

Review starts with accepted Brief/amendments, final Build Evidence, the complete implementation diff and changed/new tests. Do not preload the plan, map, consultation, all completion evidence or checkpoint diffs. Read targeted supporting sections only for a concrete decision: a referenced PC change, material decision ambiguity, cross-task inconsistency, lifecycle evidence, or a finding. Recorded `delegated` methodology is itself a concrete ownership question requiring the relevant plan/commit evidence and legacy contract. A planned final gate still requires a completed plan; inspect its header/status to validate this without loading task history. Any missing proof remains BLOCKING.

Review finding severity is deterministic:

- `BLOCKING` means a correction or missing delivery proof is required before Ship. This includes stale or structurally incomplete final Build Evidence, an invalid or missing whole-feature-path record, or tests that fail to meaningfully cover an applicable accepted behavior or risk without a valid exemption.
- `FOLLOW-UP` means no correction is required for this feature before Ship. It is never used to waive a failed delivery gate.

Review may write only `review.md` and the Feature Brief lifecycle status. It never changes production code, tests, execution artifacts, or Build Evidence. A Build-owned evidence defect returns to the builder recorded in Build start evidence.

Workflow handoff reports the eligible next stage and required artifact paths, then ends with the copy-ready, active-host continuation prompt defined in `harness-command-contract.md`. The prompt uses resolved canonical paths and contains only the one eligible invocation; naming a skill or listing artifacts without the invocation is not a complete handoff. Emitting the prompt does not invoke that skill automatically. A downstream skill runs in the same request only when the human explicitly invoked it or expressly authorized the workflow through that stage.

## Feature Record

Ship archives one record containing original intent, accepted amendments, as-built result, verification, Review findings, deviations, build strategy, planned methodology, execution summary, consultation, durable knowledge, follow-ups and recommended review order. Planned Build includes plan revision count, task outcomes, `PC-` plan changes and final integration verification. A delegated record also notes whether implementation remained executor-owned and records material dispatch/correction outcomes without provider identity or raw dialogue. Autonomous Build includes execution-map/checkpoint facts when present.

Consultation is recorded as one line when a `consult-{slug}.md` existed: which artifacts were consulted, and each finding that the owning context accepted, with the amendment or plan revision it produced. A consultation with no accepted finding is recorded as consulted with none accepted. No consultation means the field is omitted. The report itself is removed, so anything not consolidated here is gone.

Verification in the record names the tests and cases that cover the delivered behavior, their commands and green results, any recorded exemption and its reason, and the whole-feature path exercised or the recorded reason it was not available.

## Runtime projections and escalation

`runtime/common.md` and the active stage runtime are compact executable projections, not alternative specifications. Canonical references win on disagreement. Load this contract's relevant sections for a lifecycle transition, Build Evidence schema validation, amendments, Review/Ship eligibility, or legacy artifact ambiguity. Load the planned contract for compilation, frontier repair, PC changes, write ownership or final completion semantics; load the verification doctrine for planning, materially revised test obligations, or uncertain test/exemption classification. Normal task execution uses concrete projected obligations. Final verification deliberately reloads complete coverage and implementation diff.
