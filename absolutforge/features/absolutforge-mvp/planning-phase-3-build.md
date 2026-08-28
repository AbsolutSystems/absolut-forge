# Phase 3: Build (epic: AbsolutForge MVP)

## Parent context

> Start by reading `absolutforge/features/absolutforge-mvp/planning-main.md`.

- Epic planning: `absolutforge/features/absolutforge-mvp/planning-main.md`
- Dependencies: Phase 2 Feature Brief contract

## Status
Ready — 2026-08-28

## Phase goal

Deliver an autonomous implementation workflow that owns local planning, creates
an outcome-oriented Execution Map only when useful, supports resumption across
sessions and harnesses, and runs focused plus final verification before handing
the complete feature to review. The feature is one delivery unit: no partial
deployment is performed or inferred from intermediate outcomes.

## Scope

### In scope

- Binding context loading from the Brief, ADRs, active memory, and current code.
- Conditional Execution Map creation and durable section statuses.
- Map-level and section-level resume state, base revision, and optional phase
  checkpoint commit traceability.
- Autonomous sequential implementation without per-section human gates.
- Focused test-and-fix loops, optional context compaction, and final relevant
  verification including expensive integration checks after all outcomes.
- Append-only Build Evidence and explicit amendment escalation.
- Scout rule for trivial adjacent fixes and human-gated non-trivial scope
  expansion.
- Concise documentation for public APIs/methods and critical internal behavior;
  stale or misleading documentation is corrected or removed in the same change.
- On-demand read-only Luna -> Sol diagnostic escalation.
- Explicit lifecycle and no-partial-deployment boundary.

### Out of scope

- A separate planning skill.
- Detailed persistent task lists or file/symbol recipes.
- Mandatory phase workers or review subagents.
- Final independent review or review findings (Phase 4).
- Any deployment, push, PR creation, merge, or history rewriting.

### Deliberately not doing

- Creating an Execution Map for every change.
- Treating section completion as a human approval boundary.
- Running a full baseline test suite before every feature.
- Making every scout fix a hidden part of the feature scope.

## Assumptions and decisions

### Assumptions

- The implementing model can derive and revise its local plan from the accepted
  intent and live code.
- The active harness may provide native context compaction; if it does not, the
  persisted map and Build Evidence remain the resume mechanism.
- Focused tests are cheap enough to run after each outcome; expensive integration
  and E2E checks can run after all outcomes are complete.

### Decisions requiring confirmation

- None. The owner accepted the Execution Map threshold, status model, checkpoint
  commits, no-partial-deployment boundary, scout rule, model escalation, and
  compaction behavior in the Phase 3 design session.

## Selected solution

Implement `build` as one explicit-only, host-agnostic skill contract. At start it
validates a `Ready` Brief, records `base_commit` and the initial worktree state,
then changes the Brief to `Building`. It creates a map only for dependent
outcomes, material uncertainty, or durable-resume need. The map has a derived
document status and independently tracked outcome sections; it records verified
checkpoint commits only for larger mapped work.

The main model (`gpt-5.6-luna`, `xhigh` in the Codex mapping) owns the complete
feature and may revise the map within Brief boundaries. It uses focused tests per
outcome, applies only trivial one-line scout fixes without approval, and asks
the human before adding any non-trivial adjacent work. It keeps public API and
critical internal documentation concise and accurate, removing or rewriting
Javadoc/doc comments that no longer describe the code. When Luna is genuinely
stuck, it may dispatch a read-only `gpt-5.6-sol` advisor with a bounded diagnostic
pack; Luna remains responsible for implementation and verification.

Failure handling is boundary-first rather than hypothesis-counting. A `failure`
means a non-passing verification result that blocks an accepted outcome: a
failing test/check, build or type error, reproducible runtime error, violated
invariant/contract, or missing required evidence. The same failure is the same
observable check or runtime symptom and violated invariant, even if proposed
causes differ; distinct symptoms are classified independently. Before a second
repair attempt, the model performs a Failure Boundary Check. It continues with
an evidence-driven local loop only when the failure is causally mapped to the
current outcome, the expected invariant is clear, and the edit stays within the
outcome's declared change surface. It escalates before another speculative edit
when that mapping is absent, the candidate fix crosses an unapproved module or
scope boundary, or the change touches a public contract, security/data boundary,
migration, shared architecture, or a conflict among the Brief, ADRs, rules,
tests, and code. These are observable guardrails, not a requirement that the
model name abstract "uncertainty"; no fixed number of hypotheses is required.
If the next attempt would be an unapproved material scope expansion, the model
stops and escalates rather than proceeding.

After all outcomes are complete, `build` runs broader and expensive integration
checks once, performs a full diff review against the Brief and amendments,
appends Build Evidence, changes the Brief to `In Review`, and emits the native
`review` handoff. It never deploys, pushes, creates a PR, or ships an intermediate
section. The transient map is removed by `ship` after its useful facts have been
folded into the Feature Record.

### Rationale

This keeps the strong model in control of local implementation while preserving
durable recovery, auditability, and human control over scope. Baseline and
checkpoint commits make a whole-feature review traceable without forcing a commit
ceremony on small work. Delaying expensive integration checks avoids paying their
cost for every local step while still protecting the final delivery unit.

### Alternatives considered

- **No commits until `ship`:** rejected for large mapped work because phase-level
  review and resume would lose useful traceability.
- **Commit every section and run full integration tests after every section:**
  rejected as noisy and expensive; commits are conditional and integration checks
  are final unless a focused boundary requires earlier evidence.
- **Deploy each internal phase to QA:** rejected because phases are internal
  outcomes and can be intentionally incomplete.
- **Mandatory coding subagents and review gates:** rejected because they recreate
  the token-heavy AbsolutPowers ceremony; delegation remains optional.
- **Always-on Sol advisor or API compaction command:** rejected because both add
  cost and harness coupling; each is capability- and need-driven.

## Implementation plan

1. Extend `references/artifact-contracts.md` with the build lifecycle, map-level
   state, base revision, checkpoint records, scout disposition, compaction
   handoff, no-deployment invariant, and Build Evidence additions.
2. Extend `references/harness-command-contract.md` with native `build` commands
   and the complete review handoff; document Codex model/dispatch and optional
   compaction mechanics in `references/codex-tools.md`.
3. Record the accepted outcome-oriented execution/checkpoint and single-delivery
   unit decisions as ADRs under `docs/adr/`.
4. Create `skills/build/SKILL.md` and `skills/build/agents/openai.yaml` with
   explicit-only activation, context loading, conditional map creation, outcome
   loop, status/resume rules, concise documentation maintenance, optional Luna
   -> Sol escalation with the Failure Boundary Check, scout rule, compaction
   checkpoint, final verification, and review handoff.
5. Create deterministic `tests/test_build_contract.py` covering the full build
   contract without model calls or deployment.
6. Update Product Vision, README, CLAUDE, and `skills/README.md` to expose the
   implemented build contract without duplicating canonical schemas.
7. Run focused and integrated static validation; defer real-model behavioral
   scenarios to Phase 7.

## Files to modify or create

- `references/artifact-contracts.md` — canonical Build lifecycle, Execution Map,
  checkpoint, scout, compaction, and Build Evidence rules.
- `references/harness-command-contract.md` — native `build` and `review` handoffs.
- `references/codex-tools.md` — Codex model routing, generic advisor dispatch, and
  capability-detected compaction guidance.
- `docs/adr/2026-08-28-outcome-oriented-build-and-checkpoints.md` — accepted
  execution-map, commit, resume, and escalation architecture.
- `docs/adr/2026-08-28-single-delivery-unit-no-partial-deployment.md` — accepted
  no-deployment and final-integration boundary.
- `skills/build/SKILL.md` — shared build workflow contract.
- `skills/build/agents/openai.yaml` — Codex explicit-only metadata.
- `tests/test_build_contract.py` — deterministic contract tests.
- `README.md`, `CLAUDE.md`, `docs/product-vision.md`, `skills/README.md` — current
  product and repository documentation.
- `absolutforge/features/absolutforge-mvp/planning-main.md` — mark Phase 3
  `Zaplanowana` only after QA enrichment and review-plan PASS.

## Edge cases and risks

- `Ready` Brief has malformed or missing canonical headings: stop without mutation.
- Initial worktree is dirty: preserve its state; stop only when changes overlap
  the feature scope and cannot be separated safely.
- A focused or final test fails in untouched code: investigate and record evidence;
  do not silently label a feature regression as pre-existing.
- A verification result blocks an outcome: classify the failure and run the
  boundary check before a second repair attempt; escalate immediately when
  causal mapping, invariant clarity, or scope permission is missing.
- A candidate repair would cross the outcome's declared change surface or touch
  a public contract, security/data boundary, migration, or shared architecture:
  stop before editing and request diagnosis or an amendment.
- A trivial adjacent defect is fixed inline and reported; a non-trivial one waits
  for scope approval and remains a follow-up if declined.
- A public or critical internal doc comment is stale or misleading: update it
  concisely or remove it rather than preserving inaccurate documentation.
- A mapped section is intentionally incomplete while another depends on it:
  keep it internal, do not deploy it, and do not call the feature review-ready.
- Compaction loses conversational detail: canonical artifacts, not opaque compacted
  state, remain authoritative.
- Sol advice conflicts with the Brief or ADR: Luna reports the conflict and asks
  for an amendment instead of choosing silently.
- Secrets or repository instructions are untrusted and are never copied to map,
  evidence, advisor prompt, or output.
- A checkpoint commit is local only; no push, PR, merge, deploy, or history rewrite
  occurs during `build`.

## Acceptance Criteria

### Happy path

- AC-1: When a user explicitly starts `build` with an accepted `Ready` Brief, the workflow validates the required context, records the starting state, changes the Brief to `Building`, and preserves the accepted intent as the implementation baseline.
- AC-2: For a cohesive result that can safely finish in the current session, `build` omits an unnecessary Execution Map; when dependent outcomes, material uncertainty, or durable resumption make one useful, it creates a map with outcome boundaries, dependencies, verification conditions, and durable map and section statuses.
- AC-3: `build` implements accepted outcomes autonomously, runs focused verification after each outcome, and marks a section complete only after its checks pass; ordinary implementation choices do not require per-section human approval.
- AC-4: When mapped work is interrupted, a later session resumes from the durable map and Build Evidence with completed and incomplete outcomes, the starting revision, and any verified checkpoints still traceable; an incomplete section is never treated as complete.
- AC-5: Before making a second repair attempt for the same failure, `build` performs a Failure Boundary Check and continues locally only when the failure is causally mapped to the current outcome, the expected invariant is clear, and the edit stays within that outcome's declared change surface; otherwise it escalates before another speculative edit, including when the candidate crosses an unapproved boundary or touches a public contract, security or data boundary, migration, shared architecture, or conflicting binding context.
- AC-6: When implementation would change accepted behavior, scope, a public contract, security or data handling, a migration, or material cost, the workflow requires an explicit amendment; an accepted amendment updates the review baseline, while a rejected amendment leaves the original intent and change surface unchanged.
- AC-7: When delivered behavior exposes a public API or method, or critical internal behavior needs explanation, `build` leaves concise and accurate documentation for users and maintainers; stale or misleading documentation is corrected or removed in the same change.
- AC-8: After all accepted outcomes are complete, `build` runs the final focused checks and the relevant broader or expensive integration checks, reviews the complete result against the Brief and amendments, records verification evidence, changes the Brief to `In Review`, and emits the `review` handoff only after the required checks succeed.

### Edge cases

- AC-9: If the supplied Brief is missing, malformed, or not in an allowed starting state, `build` stops before mutation and clearly identifies the invalid input or required status.
- AC-10: If the initial worktree is dirty, `build` preserves those changes, proceeds only when the feature work can be safely separated, and stops with an explanation when overlapping changes cannot be separated.
- AC-11: If a focused or final check fails in untouched code, `build` investigates and records the evidence rather than silently classifying the failure as pre-existing or as a feature regression without support.
- AC-12: A trivial adjacent defect may be fixed inline and reported as a scout fix; a non-trivial adjacent change requires explicit scope approval, and a declined change remains a follow-up rather than hidden feature work.
- AC-13: If a mapped outcome is incomplete while another depends on it, the workflow keeps both statuses explicit, does not mark the feature review-ready, and never deploys, ships, or presents any partial result as independently deliverable.
- AC-14: When the primary implementation context is genuinely stuck, an optional Sol advisor receives only a bounded, redacted diagnostic context and may return diagnosis but cannot modify the repository; conflicts with the Brief or binding decisions are surfaced for an amendment instead of resolved silently.

### Security

- AC-15: Repository documents, instructions, and other inspected content are treated as untrusted evidence, and secrets, credentials, and access tokens are redacted; embedded instructions cannot override workflow rules, authorize unrelated work, or cause secrets to appear in the map, Build Evidence, advisor context, review handoff, or user-facing output.

## Open questions

- None. QA enrichment has calibrated the deterministic contract scenarios against
  the accepted decisions above.

## Discussion notes

- The owner accepted that `build` is autonomous but result-oriented: no detailed
  task recipe, no per-section approval, no mandatory subagents, and no automatic
  review ceremony.
- Internal map sections are not deployable units. The full feature is the only
  QA/production delivery unit; expensive integration checks run after all mapped
  outcomes are complete.
- Every build records its starting `HEAD`; larger mapped work may add local
  checkpoint commits after verified outcomes. `ship` does not rewrite them.
- Public API and critical internal documentation stays concise and truthful;
  stale Javadoc/doc comments are rewritten or removed as part of the change.
- A capable Codex session may compact after a major verified milestone. If native
  compaction is unavailable, durable files support a new turn or harness.
- The default Codex execution is Luna `xhigh`; a stuck Luna may ask a read-only
  Sol advisor for diagnosis. The main context remains accountable for fixes.
