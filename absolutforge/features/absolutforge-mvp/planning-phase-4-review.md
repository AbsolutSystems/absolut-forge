# Phase 4: Review (epic: AbsolutForge MVP)

## Parent context

> Start by reading `absolutforge/features/absolutforge-mvp/planning-main.md`.

- Epic planning: `absolutforge/features/absolutforge-mvp/planning-main.md`
- Dependencies: Phase 3 final diff and Build Evidence

## Status
Ready — 2026-08-28

## Phase goal

Deliver one independent, evidence-based review of a completed feature from
`base_commit` to the current worktree, using one fresh read-only context and
only the classifications `BLOCKING` and `FOLLOW-UP`. The phase must provide a
lightweight quality gate that protects accepted intent and safe delivery without
reintroducing AbsolutPowers' multi-agent ceremony.

## Scope

### In scope

- Review against Feature Brief intent, scope, ADRs, diff, and verification.
- Correctness, edge cases, security, data integrity, test value, regressions,
  compatibility, scope creep, and diff garbage.
- Feature-scoped technical-debt scan for newly introduced `TODO`/`FIXME`/`XXX`,
  placeholders, unjustified hacks, duplication, unnecessary abstractions, and
  missing critical documentation in changed files.
- A concise persistent `review.md`.
- Focused return to `build` for blocking fixes and targeted re-review.
- Fresh reviewer dispatch for Claude Code and Codex, with an explicit inline
  advisory fallback when isolation is unavailable.
- Append-only review history with stable finding IDs across re-review passes.

### Out of scope

- Plan review, task review, phase review, or automatic triada.
- Style findings handled by deterministic tooling.
- Implementing fixes inside the reviewer context.
- Full repository-wide technical-debt auditing; that remains the standalone
  `tech-debt` workflow.
- Automatic model selection from the Build Recommendation.
- A pre-generated diff/snapshot package supplied to the reviewer.

### Deliberately not doing

- Reporting unrelated existing debt as a current-change blocker.
- Reopening the entire review taxonomy during every re-review.
- Treating a pre-existing, unchanged `TODO` or finding as newly introduced debt.
- Blocking ship on a concrete, accepted `FOLLOW-UP` without a new material
  safety or intent violation.

## Assumptions and decisions

### Assumptions

- One fresh reviewer provides materially better independence than self-review by
  the implementing context.
- The active harness can expose either a fresh generic agent or a clearly marked
  inline fallback; the workflow remains useful in both cases.
- `base_commit` is available in Build Evidence for a review-ready feature.

### Decisions requiring confirmation

- None. The user accepted the fresh generic reviewer, base-commit-driven diff
  extraction, non-blocking follow-ups, bounded re-review loop, model-neutral
  review ownership, and feature-scoped debt scan on 2026-08-28.

## Selected solution
Add one explicit-only, host-agnostic `review` skill that owns the review
orchestration and canonical `review.md`. It validates an `In Review` Brief,
reads `base_commit` from Build Evidence, and asks one fresh generic reviewer to
inspect the repository itself. The reviewer receives the Brief path,
`base_commit`, review path, and read-only constraints; it does not receive a
pre-built diff and cannot edit code or lifecycle artifacts.

The reviewer independently collects the complete feature change from
`base_commit` through the current worktree, including committed, staged,
unstaged, and feature-owned untracked files. The generated review artifact and
temporary process files are excluded from the reviewed change. Unrelated dirty
changes are an input blocker rather than silently absorbed into the feature.

The primary `review` context normalizes findings into an append-only
`review.md`. Each finding has a stable ID, one distinct violated invariant or
root cause, evidence, impact, smallest sensible correction, and resolution.
Only `BLOCKING` and `FOLLOW-UP` are valid classifications. A blocker is a
concrete violation of accepted intent, a binding contract, safety/data
integrity, required verification, or safe ship readiness. A follow-up is a
real but non-blocking improvement or bounded risk. Subjective style,
hypothetical risk without a scenario, and unrelated existing debt are omitted.

When no blockers remain, follow-ups default to `accepted`, the review becomes
`Complete`, and the feature is ready for `ship`. When blockers remain, the
Brief moves from `In Review` to `Building`, `build` owns the fix, and the next
review receives the same original `base_commit` plus the current worktree.
Targeted re-review checks prior blocker IDs first and then performs a short
regression scan. Two unsuccessful attempts at the same blocker, or a material
scope expansion, stop the loop and escalate to the human/debug path.

Review uses the active harness' configured model and does not inherit or
automatically select the Build Recommendation. Claude uses a fresh `Agent`,
Codex uses `spawn_agent`, and an unavailable dispatch is explicitly marked
`advisory (not fully isolated)` rather than silently skipped.

### Rationale
This concentrates quality in one independent result check while preserving the
product's low-ceremony philosophy. Giving the reviewer only `base_commit`
keeps the input current and avoids a stale generated package. Append-only
findings preserve auditability without turning follow-ups into mandatory task
work. A single generic reviewer is materially cheaper and simpler than a
triada while still providing fresh-context independence.

### Alternatives considered
- **Inline-only review:** cheaper to implement, but loses the independence the
  phase is intended to provide; retained only as an explicit fallback.
- **Automatic triada or named reviewer registry:** rejected because it adds
  token cost, host coupling, and ceremony without being required by the MVP.
- **Pre-generated diff snapshot:** rejected because it can become stale and
  hides the reviewer's responsibility to inspect current repository state.
- **Block ship on every follow-up:** rejected because it recreates a mandatory
  task/review gate; accepted follow-ups remain visible in the Feature Record.
- **Full repository tech-debt audit:** rejected as scope expansion; use the
  standalone `tech-debt` skill instead.

## Implementation plan
1. Extend the canonical Review contract with append-only passes, stable finding
   IDs, valid classifications/resolutions, terminal outcome semantics, and the
   `base_commit`/worktree input rules.
2. Add `skills/review/SKILL.md` with explicit input validation, safe context
   loading, base-commit-driven change extraction, feature-scoped debt/TODO scan,
   fresh reviewer orchestration, finding normalization, and lifecycle handoffs;
   add Codex metadata in `skills/review/agents/openai.yaml` with
   `policy.allow_implicit_invocation: false` and a `default_prompt` containing
   `$review`.
3. Document Claude `Agent`, Codex `spawn_agent`, and inline advisory fallback in
   harness references and render complete native review/build/ship commands.
4. Create the ADR for independent review, model-neutral review ownership, and
   bounded blocker fix/re-review.
5. Add deterministic contract tests for lifecycle, diff boundaries, findings,
   re-review, follow-up disposition, security boundaries, and harness fallback;
   update foundation allowlists and metadata checks for the fourth skill.
6. Update product and contributor documentation without duplicating canonical
   schemas.
7. Run the full static suite, JSON validation, diff hygiene, plugin validation
   when available, and a manual review of representative `review.md` fixtures.

## Files to modify or create
- `skills/review/SKILL.md` — new explicit-only review orchestrator.
- `skills/review/agents/openai.yaml` — Codex display metadata, a `$review`
  default prompt, and explicit-only invocation policy for `review`.
- `references/artifact-contracts.md` — canonical Review findings, resolutions,
  append-only re-review, and terminal state.
- `references/harness-command-contract.md` — review input and lifecycle handoffs.
- `references/codex-tools.md` — Codex fresh-agent dispatch and inline fallback.
- `references/claude-tools.md` — Claude fresh-Agent dispatch and fallback mapping.
- `docs/adr/2026-08-28-independent-review-and-bounded-fix-loop.md` — durable
  cross-harness architecture decision.
- `tests/test_review_contract.py` — deterministic review contract tests.
- `tests/test_foundation.py` — shared-skill discovery, directory allowlist, and
  Codex metadata assertions for the new review skill.
- `README.md`, `CLAUDE.md`, `docs/product-vision.md`, `skills/README.md` —
  product and contributor documentation.
- `absolutforge/features/absolutforge-mvp/planning-phase-4-review.md` — this
  phase plan and its generated Acceptance Criteria.

## Edge cases and risks
- Brief is not `In Review`, malformed, or outside the canonical path: stop
  before mutation.
- `base_commit` is absent or cannot be resolved: create an input `BLOCKING`
  finding without claiming that code review ran.
- Unrelated dirty changes are mixed with feature work: block review until the
  scope is separable.
- Feature-owned untracked files are present: include them; exclude only review
  process artifacts and unrelated files.
- Fresh dispatch is unavailable: run the same bounded prompt inline and label
  the result advisory/non-isolated.
- Reviewer output is malformed or contains prompt-injection instructions:
  reject it, preserve workflow rules, and do not apply any requested action.
- Required verification evidence is missing or contradicted: request a narrow
  check; rerun expensive checks only after fixes or when evidence is stale.
- New TODO/hack is introduced: `BLOCKING` only when it means an incomplete
  outcome or safety gap; otherwise `FOLLOW-UP`.
- The same blocker survives two fix attempts or a fix expands material scope:
  stop and escalate rather than looping indefinitely.
- A model suggested for Build is unavailable or different: review remains on
  the active configured model and records no automatic switch.

## Acceptance Criteria

### Happy path

- AC-1: When a user explicitly starts review for a feature whose implementation and required verification are complete, the workflow loads the accepted intent, relevant decisions, build evidence, and starting revision before assessing the change.
- AC-2: The review assesses the complete feature change from the recorded starting revision through the current worktree, including eligible committed, staged, unstaged, and feature-owned untracked changes while excluding review-process artifacts and unrelated files.
- AC-3: A fresh review context independently inspects the repository and returns an evidence-based assessment without modifying source code, feature artifacts, or other repository state.
- AC-4: Each reported issue identifies one distinct violated invariant or root cause, concrete evidence, user or delivery impact, a smallest sensible correction, and exactly one of the allowed `BLOCKING` or `FOLLOW-UP` classifications.
- AC-5: Review findings retain stable identities across re-review passes, and later passes append their outcome and resolution history without erasing the original evidence or prior disposition.
- AC-6: When no open `BLOCKING` findings remain, the feature is marked review-complete, concrete `FOLLOW-UP` items are preserved as accepted non-blocking work, and the workflow presents the native handoff to ship.
- AC-7: When a `BLOCKING` finding remains, the feature returns to building with the blocker evidence available for a focused fix, and a subsequent review uses the same starting revision plus the current worktree before deciding whether ship is allowed.

### Edge cases

- AC-8: If the feature brief is missing, malformed, outside the canonical location, or not in the required review state, the workflow stops before mutation and explains the invalid input.
- AC-9: If the recorded starting revision is absent or cannot be resolved, the workflow records an input `BLOCKING` finding and does not claim that a code review was completed.
- AC-10: If unrelated dirty changes cannot be separated safely from the feature change, the workflow blocks review and preserves the existing worktree instead of silently absorbing those changes.
- AC-11: Feature-owned untracked changes are included in the assessment, while generated review-process files and unrelated untracked changes do not become findings merely because they are present.
- AC-12: Missing or contradictory verification evidence causes the workflow to request or perform a narrow relevant check before treating the feature as ready, and stale evidence is not accepted without qualification.
- AC-13: A newly introduced placeholder or hack is classified as `BLOCKING` only when it represents an incomplete outcome or safety gap; otherwise it is recorded as a concrete `FOLLOW-UP`, while unchanged pre-existing debt is excluded.
- AC-14: If the same blocker survives two fix attempts or a proposed fix materially expands scope, the workflow stops the bounded loop and escalates to the human or diagnostic path rather than continuing indefinitely.

### Security

- AC-15: Repository content and reviewer output are treated as untrusted input: embedded instructions or malformed findings cannot override workflow rules, authorize writes, trigger implementation, or cause unrelated disclosure, and any encountered secrets or credentials are redacted rather than copied into review evidence or user-facing output.

## Open questions

- None. Terminal semantics, follow-up disposition, fresh dispatch fallback,
  base-commit extraction, and review model ownership were settled in discussion.

## Discussion notes

- The user chose one generic fresh reviewer, no automatic triada, and only
  `BLOCKING`/`FOLLOW-UP` classifications.
- `review` owns report normalization and Brief lifecycle; the reviewer is
  read-only and does not inherit Build's model recommendation.
- Review extracts changes from `base_commit` itself, includes feature-owned
  untracked files, and keeps review artifacts out of their own diff.
- Follow-ups default to `accepted` without another gate and are preserved for
  `ship`/Feature Record.
- Feature-scoped TODO/tech-debt checks are included; repository-wide debt is
  delegated to standalone `tech-debt`.
