# AbsolutForge Delivery Artifact Contracts

**Status:** Canonical dual-build contract.

## Active layout

Large features may first use a non-buildable planning family:

```text
absolutforge/features/{family-slug}/
├── feature-plan.md
└── phases/
    ├── P01-{phase-slug}.md
    └── P02-{phase-slug}.md
```

Each Phase Seed declares the canonical sibling feature directory where its
ordinary Brief will be created, for example
`absolutforge/features/{family-slug}-p01-{phase-slug}/feature-brief.md`.
Planning artifacts are durable product-planning context, not transient Build
artifacts.

An independently accepted phase uses the normal layout:

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
absolutforge/
├── follow-ups.md                         # created when the first actionable follow-up ships
└── archives/
    ├── {slug}/
    │   ├── feature-record.md
    │   └── executive-summary.html        # optional
    └── families/{family-slug}/
        └── feature-family.md             # created when the first family member ships
```

`execution-map.md` and `implementation-plan.md` are mutually exclusive for a normal feature. They, `consult-{slug}.md` and `save-{slug}.md` are transient evidence and are removed at Ship after useful facts are consolidated into the Feature Record.

## Lifecycle

```text
Draft -> Ready -> Building -> In Review -> Shipped
```

`Ready` is the immutable intent baseline. One public `build` command selects either `autonomous` or `planned` under Build strategy selection below. New planned work uses `standard` methodology. Separate planned and delegated entrypoints are removed. Existing `delegated` builds resume through `build` under the unchanged fixed-executor restrictions in `planned-delegated-contract.md`; routing never converts methodology. `Building` resumes only through recorded strategy and methodology. Review blockers return to `build`. Switching strategy or methodology requires human abandonment/restart from a clean committed Ready baseline, never silent conversion of in-progress execution state.

Feature-family planning precedes and does not extend this lifecycle:

```text
Feature Plan: Draft -> Planned
Phase Seed -> discuss -> Feature Brief: Draft -> Ready -> Building -> In Review -> Shipped
```

`Planned` means the coarse family behavior and phase boundaries were explicitly
accepted. It is not `Ready`, conveys no implementation authority, and cannot be
passed to Build. Every phase enters the ordinary lifecycle only through its own
self-contained accepted Feature Brief.

## Feature Plan

Use a Feature Plan only when one proposal contains multiple independently
valuable and cancellation-safe delivery outcomes, later outcomes need material
learning or product decisions from earlier delivery, or a single Ready Brief
would freeze speculative detail across distinct rollout, migration, security,
or operational boundaries. Document length, file count, generic complexity,
and implementation-task decomposition are not triggers.

The canonical path is
`absolutforge/features/{family-slug}/feature-plan.md`. Its schema is:

```markdown
# Feature Plan: {name}

## Artifact kind
Feature Plan — not buildable

## Status
Draft | Planned

## Plan revision
{positive integer}

## Problem and end-to-end behavior

## Users and value

## Current state and evidence

## Shared constraints and invariants
### PI-{NNN} — {title}

## Behaviors and custody
### PB-{NNN} — {behavior}
- Custody: P{NN} | shared | deferred
- Reason:
- Revisit trigger: not applicable | {trigger}

## Phase order
### P{NN} — {phase name}
- Stable slug: {phase-slug}
- Seed: `absolutforge/features/{family-slug}/phases/P{NN}-{phase-slug}.md`
- Intended Brief: `absolutforge/features/{family-slug}-p{nn}-{phase-slug}/feature-brief.md`
- Depends on: none | P{NN}, ...
- Goal and user value:
- Stop state:

## Cross-phase decisions

## Uncertainties

## Next eligible phase
P{NN}

## Reconciliation
None yet.
```

`PI-`, `PB-`, and `P` IDs are unique and stable within the family. Phase order
and dependencies may change without renaming phase IDs. Every behavior has
exactly one custody classification. A phase boundary must not split one
user-visible transaction, migration obligation, security boundary,
compatibility window, or rollback unit unless the plan explicitly establishes
an independently coherent intermediate contract.

Only the next phase may carry near-term detail. Later phases retain goals,
boundaries, dependencies, uncertainties, and stop states without speculative
implementation decisions. Shared constraints remain canonical planning context;
Discuss copies every applicable constraint and owned behavior into a phase's
Feature Brief before it can become Ready, so Build never depends on a mutable
Feature Plan.

## Phase Seed

Each declared phase has one canonical seed at
`absolutforge/features/{family-slug}/phases/P{NN}-{phase-slug}.md`:

```markdown
# Phase Seed: P{NN} — {name}

## Artifact kind
Phase Seed — not buildable

## Feature Plan
- Path: `absolutforge/features/{family-slug}/feature-plan.md`
- Revision: {positive integer}

## Phase identity
- ID: P{NN}
- Stable slug: {phase-slug}
- Intended Brief: `absolutforge/features/{family-slug}-p{nn}-{phase-slug}/feature-brief.md`

## Goal and user value

## Scope boundary
### In scope
### Out of scope

## Behavior custody
- PB-{NNN}

## Dependencies and entry evidence

## Inherited constraints
- PI-{NNN}

## Open questions for Discuss

## Coherent stop state

## Evidence to revisit
```

A Phase Seed has no `Ready` state and cannot authorize implementation. Discuss
validates its family path, plan revision, intended Brief path, behavior custody,
dependencies, and current evidence. It then creates or resumes that ordinary
Feature Brief and excludes later-phase scope. An accepted phase Brief snapshots
all applicable behavior and invariants in its own Ready baseline; a link to the
plan alone is insufficient.

## Feature Plan acceptance and reconciliation

Discuss recommends planning with evidence and requires explicit human agreement
before changing from the single-Brief route. It then presents the complete
Feature Plan and all Phase Seeds for one explicit acceptance. Acceptance changes
the plan to `Planned` and creates one local path-scoped commit containing exactly
`feature-plan.md` and its declared seeds. Preserve unrelated index/worktree
state, never include source or another workflow artifact, and verify that the
commit changed exactly the accepted planning set. Reuse an identical accepted
set already at HEAD instead of creating an empty commit. A commit or verification
failure leaves the artifacts intact but blocks the phase handoff.

As with Brief acceptance, Discuss requires a non-detached intended feature
branch before requesting final planning acceptance. It never pushes, amends, or
rewrites history as part of this checkpoint.

After acceptance, Discuss emits one resolved continuation for the plan's `Next
eligible phase`; it never emits Build for a Feature Plan or Phase Seed. Build
must refuse both artifact kinds before mutation.

Before discussing a later phase, reconcile the plan against shipped predecessor
evidence and current repository truth. A material change to shared behavior,
custody, dependencies, or an unexpanded seed requires a new explicit human
acceptance, increments `Plan revision`, and appends an immutable entry:

```markdown
### PR-{NNN} — YYYY-MM-DD
- Evidence:
- Change:
- Affected unexpanded phases:
- Ready/Shipped phases unaffected: {IDs and reason}
- Accepted by:
```

Reconciliation may replace only unexpanded seeds named by the accepted entry.
Never silently rewrite a seed already used to create a Ready Brief, alter a Ready
Brief, or make an accepted phase inherit changed plan text retroactively. If a
change affects accepted intent, use that Brief's amendment rules independently.
After explicit acceptance, create and verify one path-scoped local commit
containing exactly the changed `feature-plan.md` and affected unexpanded seeds;
unrelated paths remain outside it.

## Feature Brief

```markdown
# Feature: {name}

## Status
Draft | Ready | Building | In Review

## Change type
Feature | Fix | Refactor

## Feature family
- Family slug: standalone | {family-slug}
- Family name: not applicable | {family name}
- Phase: not applicable | P{NN} — {phase name}
- Lineage: standalone | new family | feature-plan: `{path}` | existing manifest: `{path}`

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

The immutable Ready baseline is `## Feature family` through `## Expected outcomes`, plus accepted amendments. Build may change lifecycle status and append Build Evidence only.

`Feature family` is required for newly accepted Briefs and is part of the
immutable Ready baseline. Historical Briefs without it remain valid and are
treated as `standalone`; Ship never infers their family from a branch or slug.
A Brief expanded from a Phase Seed takes its family slug, name, phase identity
and lineage from the validated Feature Plan. For an ordinary Brief, Discuss may
use the current branch, recent archive commits and semantic similarity only to
rank candidates. It records `standalone`, a new family, or one existing family
in the complete proposal; ambiguity that could change the durable grouping is
resolved by the human before acceptance. A branch name is never family identity.

New Discuss briefs give Expected Outcomes stable `### EO-001 — {title}` headings and material Constraints and invariants stable `### INV-001 — {title}` headings. IDs are unique within their category and remain stable after acceptance; amendments introduce new IDs rather than reassigning existing ones. Do not ID every paragraph. Older briefs without IDs remain valid unchanged: use headings and exact text matching. A task's `Covers` and `Preserves` references resolve to accepted text, including applicable amendments; an ID alone is not sufficient executor context. Ambiguous references require targeted inspection or clarification, never guessed intent.

## Ready acceptance checkpoint

Explicit human acceptance authorizes `discuss` to set the complete Brief to `Ready` and create its local acceptance commit. The commit contains exactly `absolutforge/features/{slug}/feature-brief.md`; unrelated staged or dirty paths and an optional consultation report remain outside it. Discuss verifies the committed Ready content and changed path before handing off to Build, and reports the revision. An identical Ready Brief already committed at HEAD is reused without an empty commit.

Discuss requires a non-detached intended feature branch before requesting final acceptance. Commit failure leaves the Ready Brief intact but blocks Build handoff until resolved; Discuss never amends, rewrites history, pushes, or commits another path as part of acceptance.

## Build strategy selection

The public `build <brief-path>` chooses once at Ready, before the Build-start checkpoint or implementation. It accepts at most one optional `--strategy=autonomous` or `--strategy=planned`; reject unknown values/options or repeated overrides before mutation. An explicit valid override wins over automatic selection, but never bypasses lifecycle, verification or host ownership requirements.

Without an override, inspect accepted intent/amendments and relevant repository evidence using targeted reads. Default to autonomous for a cohesive change with little independent work. Choose planned only when concrete independent write surfaces/dependencies, useful bounded delegation, or a durable multi-session task graph repay compilation and coordination overhead. File count or generic complexity alone is insufficient; security or architecture risk alone does not require a graph. Lack of workers removes delegation as a benefit, but standard planned execution may still be justified by durable recovery. If no concrete benefit is established, select autonomous. Do not compile a plan or load both execution runtimes merely to make this decision.

Autonomous execution compiles each bounded low, standard or high outcome just in time and dispatches every production-code and test edit under `model-routing.md#autonomous-outcome-routing`; that handoff alone is not a reason to select planned. A graph is justified only when coordinating multiple tasks provides the benefit above. Worker execution does not change recorded strategy or methodology and adds no artifact requirement.

Announce the chosen strategy and concise evidence-based reason without another confirmation. Record `Strategy selection` in the Build-start checkpoint alongside the strategy, methodology and artifact path. Then continue the chosen runtime within the same invocation. Automatic selection is implementation organization inside accepted intent, not authorization to change scope.

At Building, read durable Build-start strategy and methodology before routing; never rerun automatic selection. A matching override is harmless; a conflicting override is rejected before mutation and requires explicit abandonment/restart to change strategy. Missing strategy, unknown values or inconsistent Brief/plan/Save evidence require reconciliation, never guessing from file count or an existing artifact. Missing historical methodology retains the established default; missing historical selection rationale is valid and must not be backfilled. Planned/delegated retains its fixed executor; legacy tdd remains unsupported. An override cannot convert methodology. Draft, In Review and Shipped are not new-start states.

## Scout rule

Build leaves the code its assigned executor already touches better than it
found it. Without a separate amendment or confirmation, that executor may make
a scout fix only when all of these are true:

- it was discovered while implementing or verifying accepted work;
- it is confined to the current autonomous outcome or planned task's owned
  paths and directly related local seam;
- the correction is unambiguous, localized and low risk;
- it preserves accepted behavior, public contracts, compatibility, persisted
  data, security boundaries, dependencies, configuration and migration state;
- it introduces no broad formatting churn or speculative cleanup; and
- the executor can run a focused proof and include it in the current checkpoint.

Typical scout fixes include an obsolete local import, a typo in touched
documentation, or a clearly redundant local branch. A nearby behavior change,
public API adjustment, dependency update, schema/data change, security decision,
cross-owner edit or cleanup that materially enlarges Review is not a quick fix.
Do not silently widen a task surface or create a plan change merely to perform
scout work.

When every condition holds, the assigned executor makes and verifies the fix
without interrupting Build, then reports what was found, changed and proved.
The Build owner may classify the observation, include it in the current worker
package or a correction package, validate it and record its disposition, but it
never implements a production-code or test Scout fix. Otherwise do not edit it:
record a concise scout observation and why it was deferred. Autonomous checkpoints use
their existing result/new-facts evidence; planned tasks use Completion Evidence.
The final Build Evidence `Scout disposition` summarizes fixes and deferred
observations, using `none` only when nothing material was found. Deferred scout
observations are not accepted feature scope and do not enter the global
follow-up register unless Review independently records them as a valid
`FOLLOW-UP`. Review judges every scout edit against this boundary from the
complete diff.

## Build start evidence

Append exactly once before the first source edit:

```markdown
### Build start — YYYY-MM-DD
- Feature branch: `{branch}`
- Base revision: `{base_commit}`
- Worktree: clean
- Build strategy: autonomous | planned
- Strategy selection: automatic | explicit override — {concise repository/Brief-based reason or user choice}
- Planned methodology: not applicable | standard | delegated
- Execution artifact: none | `absolutforge/features/{slug}/execution-map.md` | `absolutforge/features/{slug}/implementation-plan.md`
```

The Strategy selection field is required for new starts only; historical starts remain valid unchanged without it.

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

Ship archives one record containing original intent, accepted amendments, as-built result, verification, Review findings, deviations, build strategy, planned methodology, execution summary, consultation, durable knowledge, follow-ups, recommended review order and the exact Feature-family metadata from the Brief. Historical Briefs without family metadata are recorded as `standalone`; Ship never derives family identity from the branch. Planned Build includes plan revision count, task outcomes, `PC-` plan changes and final integration verification. A delegated record also notes whether implementation remained executor-owned and records material dispatch/correction outcomes without provider identity or raw dialogue. Autonomous Build includes execution-map/checkpoint facts when present.

Consultation is recorded as one line when a `consult-{slug}.md` existed: which artifacts were consulted, and each finding that the owning context accepted, with the amendment or plan revision it produced. A consultation with no accepted finding is recorded as consulted with none accepted. No consultation means the field is omitted. The report itself is removed, so anything not consolidated here is gone.

Verification in the record names the tests and cases that cover the delivered behavior, their commands and green results, any recorded exemption and its reason, and the whole-feature path exercised or the recorded reason it was not available.

## Feature Family manifest

Every non-standalone shipped record belongs to exactly one primary family. Ship
creates or updates
`absolutforge/archives/families/{family-slug}/feature-family.md` in the same
closeout commit as the member record. Existing record paths never move merely
to create a family. The manifest is a durable navigational history, not mutable
intent authority:

```markdown
# Feature Family: {family name}

## Identity
- Family slug: {family-slug}
- Feature Plan: none | `absolutforge/features/{family-slug}/feature-plan.md`

## Goal
{concise end-to-end goal from the plan or first accepted family Brief}

## Delivered work
### {phase ID or member number} — {feature name}
- Shipped: YYYY-MM-DD
- Reviewed revision: `{reviewed revision}`
- Record: `../../{slug}/feature-record.md`
- Outcome: {concise as-built result}
```

Entries are append-only in ship order. A source record naming a family must
have exactly one matching manifest entry, and every manifest entry must resolve
to a record naming that same family. Ship refuses an inconsistent family slug,
name, duplicate record, missing member or broken relative link before commit.
Family renames, aliases, overlapping topic collections and post-hoc adoption of
historical standalone records are outside the current lifecycle contract and
must not be inferred or rewritten during ordinary Discuss or Ship.

## Follow-up register

`absolutforge/follow-ups.md` is the operational index of actionable work that
Review explicitly allowed to ship. Feature Records remain the evidence authority.
Ship creates the register when needed and appends one entry for each `FOLLOW-UP`
finding whose Review resolution is `open` or `deferred`; `fixed` and `accepted`
findings remain only in the Feature Record. IDs are repository-global,
monotonically increasing `FU-{NNN}` values and are never reused.

```markdown
# AbsolutForge Follow-ups

## FU-{NNN} — {short title}
- Status: open | promoted | resolved | dismissed
- Source record: `archives/{slug}/feature-record.md`
- Review finding: F-{NNN}
- Family: standalone | {family-slug}
- Added: YYYY-MM-DD
- Impact: {concise impact from Review}
- Suggested next action: {smallest sensible correction from Review}
- Promoted to: none | `absolutforge/features/{slug}/feature-brief.md`
- Resolution: none | {concise result and durable evidence link}
```

The source tuple of archive record and Review finding ID is unique. A retried
closeout reuses an identical existing entry and refuses conflicting content;
it never allocates a duplicate. The register does not assign priority, owner or deadline
and does not turn a follow-up into accepted scope. Promotion or closure
requires a later explicit workflow decision; ordinary Ship only appends newly
actionable entries. Ship validates the archive, family manifest when applicable,
and follow-up-register changes as one closeout set before staging any of them.

## Runtime projections and escalation

`runtime/common.md` and the active stage runtime are compact executable projections, not alternative specifications. Canonical references win on disagreement. Load this contract's relevant sections for a lifecycle transition, Build Evidence schema validation, amendments, Review/Ship eligibility, or legacy artifact ambiguity. Load the planned contract for compilation, frontier repair, PC changes, write ownership or final completion semantics; load the verification doctrine for planning, materially revised test obligations, or uncertain test/exemption classification. Normal task execution uses concrete projected obligations. Final verification deliberately reloads complete coverage and implementation diff.
