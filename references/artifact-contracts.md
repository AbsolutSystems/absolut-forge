# AbsolutForge Delivery Artifact Contracts

**Status:** Canonical contract — accepted 2026-08-27  
**Owner:** AbsolutForge workflow; each artifact is owned by the stage listed below.

This document is the single canonical owner of the exact delivery-artifact paths,
statuses, transitions, and Markdown schemas. The [Product Vision](../docs/product-vision.md)
defines the product behavior and links here; skills and ADRs must link to this
contract instead of copying these templates.

## Artifact locations and ownership

An active change uses a repository-relative slug directory:

```text
absolutforge/features/{slug}/
├── feature-brief.md                 # required
├── execution-map.md                 # optional; build creates when useful
└── review.md                         # required before ship
```

After `ship` approves closeout, the durable archive is:

```text
absolutforge/archives/{slug}/
├── feature-record.md                 # required
└── executive-summary.html            # required, self-contained
```

The transient `execution-map.md` is not archived. Its useful outcome and
verification facts are consolidated into `feature-record.md`.

| Artifact | Active path | Archive path | Owner | Required status values |
| --- | --- | --- | --- | --- |
| Feature Brief | `absolutforge/features/{slug}/feature-brief.md` | content preserved in Feature Record | `discuss` (intent), then `build` (delivery evidence) | `Draft`, `Ready`, `Building`, `In Review` |
| Amendment | appended to the active Feature Brief under `## Amendments` | preserved under Original intent / deviations | `discuss` with explicit acceptance; `build` records the accepted change | `Proposed`, `Accepted`, `Rejected` |
| Execution Map | `absolutforge/features/{slug}/execution-map.md` | none | `build` | `pending`, `in-progress`, `complete` |
| Review | `absolutforge/features/{slug}/review.md` | outcome copied to Feature Record | `review`; `build` owns fixes | `In Review`, `Complete` |
| Feature Record | none while active | `absolutforge/archives/{slug}/feature-record.md` | `ship` | `Shipped` |
| Executive Summary | none while active | `absolutforge/archives/{slug}/executive-summary.html` | `ship` | generated after final review; no intermediate status |

## Lifecycle transitions

The normal lifecycle is:

```text
Feature Brief Draft
  -> Ready                 (discuss obtains explicit acceptance)
  -> Building              (build starts)
  -> In Review             (build verification succeeds and review starts)
  -> Shipped               (review has no open BLOCKING findings; ship is approved)
```

If review opens a `BLOCKING` finding, the brief follows the bounded fix loop
`In Review -> Building -> In Review`; it reaches `Shipped` only after the fix
and targeted re-review leave no open blocker. A `FOLLOW-UP` does not cause this
loop.

The brief may move from `Draft` to `Ready` only when no material contract,
scope, security, data, migration, or cost question remains unresolved. A
`Ready` brief establishes an immutable intent baseline. `build` may change its
status and append `## Build Evidence`, but it must not rewrite the baseline to
match the implementation.

Material new information follows this path:

```text
Ready baseline -> Proposed amendment -> Accepted amendment -> build continues
                                  \-> Rejected amendment -> original baseline remains
```

An accepted amendment is part of the intent baseline for review and ship. After
validating the accepted context, `build` moves the Brief from `Ready` to
`Building` without rewriting its immutable baseline. It moves the Brief to `In
Review` only after every accepted outcome and required final verification has
succeeded. A transient execution map and each of its sections may progress
`pending -> in-progress -> complete`; `complete` means verified and ready for
the whole-feature review, never deployed, shipped, or independently releasable.
`review` changes its artifact from `In Review` to `Complete` after the final
review result is recorded; a `BLOCKING` result returns work to `build` for fixes
and targeted re-review. `ship` creates the archive only after review is complete
and no open `BLOCKING` findings remain. It reports deviations explicitly rather
than rewriting accepted intent.

## Feature Brief contract

Create `absolutforge/features/{slug}/feature-brief.md` with this complete
template. Keep the headings and status values stable so later stages can find
the immutable baseline and delivery evidence.

```markdown
# Feature: {name}

## Status
Draft | Ready | Building | In Review

## Change type
Feature | Fix | Refactor

## Problem and goal
What is wrong today, why it matters, and what outcome is required.

## Users
Who benefits or which system process changes.

## Current state and evidence
Observed behavior and repository-relative evidence anchors. This describes the
current system, not a future file-change list.

## Expected behavior
Externally observable happy path, meaningful variants, failures, and boundaries.

## Scope
### In scope
### Out of scope

## Constraints and invariants
Contracts, compatibility, security, data, performance, and binding project rules.

## Solution direction
Architecture at component and data-flow level, without symbol-level tasks.

## Assumptions
- Assumption
- Basis
- What build must do if it proves false

## Decisions
Decisions with rationale and links to relevant ADRs.

## Risks and edge cases
Only risks grounded in the domain or current code.

## Expected outcomes
Observable conditions demonstrating that the change is correct. Do not expand
these automatically into a task or acceptance-criteria taxonomy.

## Build Recommendation (optional execution metadata)
This optional section is produced by `discuss` when the Brief has enough
evidence to recommend a Build tier. It must appear after `## Expected outcomes`
and before `## Open questions`. It is execution guidance, not product intent:
it is outside the immutable intent baseline and must never be used to rewrite
the sections above. Older Briefs may omit it and remain valid.

Use this shape:

```markdown
## Build Recommendation
- Complexity: simple | complex
- Execution shape: single | phased
- Claude model: sonnet | opus
- Codex model: gpt-5.6-luna | gpt-5.6-terra
- Rationale: concise, evidence-based reason for the selected profile
- Confidence: high | medium | low
- Override: none | {actor and reason, when an explicit override was made}
```

Exactly two profiles are valid and their values must stay aligned:

| Profile | Complexity | Execution shape | Claude model | Codex model |
| --- | --- | --- | --- | --- |
| Simple | `simple` | `single` | `sonnet` | `gpt-5.6-luna` |
| Complex | `complex` | `phased` | `opus` | `gpt-5.6-terra` |

`simple/single` is appropriate for one cohesive, low-risk outcome that follows
an established pattern and has no material unresolved boundary. `complex/phased`
is appropriate when outcomes are materially dependent or uncertain, or when the
change crosses a public contract, security or data boundary, migration, shared
architecture, or multiple subsystems. Do not classify from line count, file
count, or diff size alone. The rationale must cite repository or Brief evidence;
confidence describes how strongly that evidence supports the profile.

The recommendation is advisory. If it is absent, malformed, unavailable in the
active harness, or not selected by the user, `build` keeps its configured model
choice and records the fallback or selection reason in `## Build Evidence`.
An explicit user or model override is allowed only with a concise reason; it is
execution evidence, not a product amendment, model/provider configuration
change, deployment authorization, or permission to deliver a partial feature.

## Open questions
No question changing contract, scope, security, data, migration, or material
cost may remain when status becomes Ready.

## Amendments
### A-{N} — YYYY-MM-DD
- Status: Proposed | Accepted | Rejected
- Reason:
- Change:
- Accepted by:

---

## Build Evidence
Append-only evidence owned by build:
- Changed areas:
- Verification commands and results:
- Material implementation decisions:
- Deviations from the accepted baseline:
```

When the status first becomes `Ready`, the immutable intent baseline comprises
the sections from `## Problem and goal` through `## Expected outcomes`, plus any
accepted amendments. `Build Evidence` is not part of that baseline.

## Amendment contract

An amendment is required when discovery changes behavior, scope, a public
contract, security, data handling, migration, or material cost. Do not silently
edit the accepted baseline. Append this complete entry to `## Amendments` and
obtain explicit acceptance before implementing the change:

```markdown
### A-{N} — YYYY-MM-DD
- Status: Proposed | Accepted | Rejected
- Reason: {new evidence or decision}
- Change: {precise change to the accepted intent}
- Accepted by: {person or explicit product decision}
```

Non-blocking uncertainty belongs in `## Assumptions` with a basis and the
action `build` takes if it proves false. A rejected amendment leaves the
original baseline unchanged. An accepted amendment is immutable thereafter and
must be included in review and the Feature Record.

## Optional consultation contract

`consult` is an optional, explicit-only second opinion on an existing Feature
Brief. It is not a lifecycle stage or gate: the normal workflow remains
`discuss -> build -> review -> ship`. It accepts only a Brief with status
`Draft` or `Ready` at
`absolutforge/features/{slug}/feature-brief.md`.

Each consultation finding is bounded to a material ambiguity, contradiction,
evidence gap, grounded risk, or unnecessary scope. It must include:

- Evidence: the repository-relative fact, contract, or Brief passage.
- Impact: the concrete consequence if the issue remains unresolved.
- Proposed Brief change: the precise change recommended by the finding.

The findings are presented as one batch. `consult` must obtain explicit human
approval before changing the Brief; unselected findings do not mutate it.
Accepted findings are merged into the relevant sections of a `Draft`. For a
`Ready` Brief, an accepted material intent change is appended as an accepted
amendment under `## Amendments`; the immutable baseline is never edited.

`Building` and `In Review` inputs are not mutated by consultation. A material
intent change discovered for either status returns to `discuss` and its
amendment flow. If no material issue remains, consultation returns exactly
`no material findings`, changes no Brief content, and creates no consultation
artifact. Findings already represented by an accepted decision or amendment
are deduplicated rather than recorded again.

Consultation never creates a persistent report, records model identity in the
Brief, or becomes mandatory between `discuss` and `build`.

## Execution Map contract

`build` creates `execution-map.md` only when the work has multiple dependent
outcomes, meaningful uncertainty, or needs durable resumption. It is an
outcome-oriented map, not a task list, file recipe, or review gate. Every
map has one map-level status and every section has its own status. The map-level
status is `pending`, `in-progress`, or `complete`; it becomes `complete` only
when all sections and final whole-feature verification are complete. The map
records the starting Git revision and worktree state before implementation so a
later session can resume from durable facts rather than opaque conversation
state. Every section uses this complete shape:

```markdown
# Execution Map: {feature name}

## Status
pending | in-progress | complete

## Build start
- base_commit: {HEAD before feature work}
- Initial worktree state: clean | dirty, with repository-relative summary

## Checkpoints
- None yet, or:
- {checkpoint commit}: {verified coherent outcome}; verification: {result}

## Section {N}: {outcome name}
- Status: pending | in-progress | complete
- Goal: {observable result}
- Boundaries: {included and excluded behavior}
- Dependencies: {other sections or accepted context}
- Verification: {focused checks proving this outcome}
- Result: {filled after verification}
- Material deviations: {none, or an explicit deviation and amendment reference}
```

Checkpoint commits are optional, local-only records for coherent, verified
mapped outcomes; they are not required for small cohesive work. A review uses
the complete feature diff `base_commit..HEAD`, not an internal section or
checkpoint diff. The map is transient and `ship` removes it at closeout after
consolidating its useful outcomes, verification, checkpoints, and deviations
into the Feature Record. It must not be copied into the archive as a separate
artifact, and `ship` must not squash or rewrite checkpoint history.

## Build Evidence contract

`build` appends evidence to the active Feature Brief under `## Build Evidence`;
it never replaces or edits prior evidence or the accepted intent baseline. Each
entry is concise, factual, and redacted of secrets, credentials, access tokens,
and other sensitive values. Use this shape after a verified outcome or final
whole-feature verification:

```markdown
### Build evidence — YYYY-MM-DD
- Base revision / review diff: `{base_commit}..HEAD`
- Changed areas: repository-relative areas only
- Verification commands and results: command -> pass | fail, with concise evidence
- Checkpoints: none | local `{commit}` after verified {outcome}
- Material implementation decisions: none | concise decision and rationale
- Deviations from the accepted baseline: none | accepted amendment reference
- Scout disposition: none | trivial fix `{path}` reported | non-trivial follow-up awaiting approval
- Documentation maintenance: none | concise public/critical-internal docs updated or stale docs corrected/removed
- Compaction handoff: not requested | durable map/evidence persisted before optional native compaction
- Durable memory lesson: none | candidate path
```

Focus verification runs after each outcome; relevant broader and expensive
integration checks run once after all outcomes are complete. A failed check is
recorded with its observable evidence rather than silently classified as
pre-existing. A non-passing verification result that blocks an accepted outcome
is a **failure**. The same failure is the same observable check or runtime
symptom and violated invariant, even if a proposed cause changes.

Before a second repair attempt for the same failure, `build` performs a
**Failure Boundary Check**. It may continue only when evidence causally maps the
failure to the current outcome, the expected invariant is clear, and the edit
stays within that outcome's declared change surface. It escalates before another
speculative edit when any of those conditions is absent, or when the candidate
edit touches a public contract, security/data boundary, migration, shared
architecture, an unapproved module/scope boundary, or conflicting Brief, ADR,
rule, test, and code evidence. An unapproved material scope expansion is a stop
condition: request an explicit amendment or scope approval; do not implement it
as a scout fix.

`build` may fix and report a strictly trivial adjacent defect in the touched
change surface. Any non-trivial adjacent work remains a follow-up until explicit
scope approval. It keeps public APIs and critical internal behavior documented
concisely and truthfully; stale or misleading documentation is corrected or
removed in the same change. After a durable verified milestone, it may request
native context compaction when the harness supports it; otherwise the Execution
Map and append-only Build Evidence are the complete resume handoff.

No map state, evidence entry, checkpoint, or verified outcome authorizes a
partial release. The complete Feature Brief is the only delivery unit. `build`
never deploys, pushes, creates a PR, merges, ships, or rewrites history.

## Review contract

`review` creates `absolutforge/features/{slug}/review.md` from the accepted
Feature Brief and amendments, linked ADRs and rules, the complete final diff,
Build Evidence, and verification results. Findings are evidence-based and use
only the two severities below. Subjective preferences, unrelated existing
problems, and hypothetical risks without a concrete failure scenario are not
findings.

```markdown
# Review: {feature name}

## Status
In Review | Complete

## Context
- Feature Brief: `absolutforge/features/{slug}/feature-brief.md`
- ADRs:
- Diff / revision reviewed:
- Verification evidence:

## Findings

### {BLOCKING|FOLLOW-UP}: {short title}
- Evidence: `path/to/file:line` or an observable verification result.
- Impact: {concrete consequence}
- Smallest sensible correction: {bounded correction}
- Resolution: {open, or the fix and re-verification}

## Outcome
- BLOCKING findings open: {number}
- FOLLOW-UP findings accepted: {number}
- Decision: Ready for ship | Fixes required
```

`BLOCKING` findings must be fixed and re-verified before ship. `FOLLOW-UP`
findings may be accepted and are preserved in the Feature Record. A targeted
re-review checks prior blockers first, then performs a short regression scan of
the changed diff.

## Feature Record contract

After approval, `ship` creates
`absolutforge/archives/{slug}/feature-record.md`. It preserves the accepted
intent separately from the as-built result and records this complete template:

```markdown
# Feature: {name}

## Status
Shipped: YYYY-MM-DD; commit: {local commit or pending local commit}

## Original intent
The accepted Feature Brief baseline, including accepted amendments, preserved
without rewriting it to describe the implementation.

## What was built
Outcome summary derived from the final diff.

## Deviations from the Brief
Different implementation, omitted scope, added scope, or explicitly none.

## Verification
Final commands, results, and meaningful manual checks.

## Review outcome
Resolved BLOCKING findings and accepted FOLLOW-UP findings.

## Architectural decisions
Links to ADRs; do not duplicate their full text.

## Durable knowledge
Project-memory entries explicitly approved for promotion and scoped Gotchas.

## Open follow-ups
Explicitly deferred work.
```

## Executive Summary contract

`ship` also creates `absolutforge/archives/{slug}/executive-summary.html`
from the final post-review state. It is for a human PR reviewer and must be a
self-contained HTML document: all required styles, diagrams, and content are
embedded or expressed inline; it must not depend on a local server, runtime
bundle, or unavailable external asset. This contract defines content, not a
rendering implementation. The summary includes:

- TL;DR, problem, and business value;
- final scope and primary behavior/data flow;
- changed-component map;
- key decisions and rationale, plus material rejected alternatives;
- deviations from the accepted Brief;
- tests and verification;
- blockers found and fixed by review;
- remaining follow-ups and risks;
- recommended file review order;
- links to ADRs and durable documentation.

The HTML is generated only after review fixes finish. It is never model-review
input and is not a substitute for the Markdown Feature Record.
