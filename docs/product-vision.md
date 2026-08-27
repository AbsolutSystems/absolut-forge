# AbsolutForge Product Vision

## Status

Accepted product design — 2026-08-27.

This document is the durable source of truth for the product behavior agreed
before implementation. Phase plans may refine implementation details, but they
must not silently change these contracts. A material change to product behavior
requires an explicit decision and an update to this document.

## Product thesis

AbsolutForge is an intent-driven development workflow for strong coding models.
It assumes that frontier models can plan local implementation work when given a
precise goal, current-code evidence, durable constraints, and observable outcome
boundaries.

The product moves quality investment away from detailed task decomposition and
repeated process gates. It concentrates quality in three places:

1. a precise, accepted Feature Brief,
2. autonomous implementation with mandatory test-and-fix loops,
3. one independent review of the completed change.

The operating principle is:

> Control the delivered result, not every implementation step.

AbsolutForge is a separate product, not an AbsolutPowers light mode. The classic
AbsolutPowers plugin remains separately installable and may be kept disabled.

## Product boundary

### MVP skills

Core workflow:

```text
discuss -> build -> review -> ship
```

Standalone workflows:

```text
debug
tech-debt
```

### MVP harnesses

- Claude Code
- Codex

One host-agnostic skill tree serves both harnesses through thin integrations.
Pi and Grok are deferred until the workflow has been validated on real work.

### Activation and isolation

- There is no SessionStart hook and no global pipeline prompt.
- `discuss`, `build`, `review`, `ship`, and `tech-debt` are explicit-only.
- Only `debug` may auto-trigger, and only for a concrete failure such as an error,
  failing test, crash, regression, or other unexpected behavior.
- Skill descriptions must remain narrow enough that generic coding requests do
  not start the workflow automatically.
- AbsolutPowers and AbsolutForge must not be active together during normal use.
  Installation may coexist, but exactly one overlapping workflow is enabled.
- The product is model-agnostic but intentionally optimized for strong frontier
  coding models rather than compensating for weak planning ability with ceremony.

### Deliberate exclusions

The MVP does not include:

- `generate-tasks`, detailed task documents, QA enrichment, plan review,
  task review, per-phase review, implementation review, or automatic triada;
- `problem-discuss`, `qa-review`, `constitution`, module documentation,
  explanation/onboarding as a separate skill, or learned-skill mining;
- automatic push, PR creation, merge, or history rewriting;
- Pi or Grok integrations;
- a compatibility runtime shared with AbsolutPowers.

## Artifact lifecycle

An active change lives under:

```text
absolutforge/features/{slug}/
├── feature-brief.md
├── execution-map.md   # optional; created by build only when useful
└── review.md          # created by review
```

After `ship`:

```text
absolutforge/archives/{slug}/
├── feature-record.md
└── executive-summary.html
```

The transient Execution Map is not archived. Its useful outcome and verification
facts are consolidated into the Feature Record. The original intent must remain
distinguishable from the as-built result.

## `discuss` contract

`discuss` is the only deliberately interactive core stage. It determines what
and why before recommending how.

### Behavior

1. Clarify the problem, desired behavior, audience, scope, and constraints.
2. Adapt question depth to uncertainty and risk. Do not enforce one question per
   turn or section-by-section approval as a universal ceremony.
3. Inspect current code before recommending a technical direction.
4. Recommend one approach and briefly explain material alternatives and
   tradeoffs.
5. Create ADRs only for decisions with durable architectural consequences.
6. Present one complete Feature Brief for explicit acceptance.
7. On acceptance, mark it `Ready` and hand it directly to `build`.

`discuss` does not create an Execution Map, detailed tasks, file-by-file recipes,
QA enrichment, or a review-plan gate.

### Feature Brief format

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
Observed behavior and repository-relative evidence anchors. This is evidence
about the current system, not a future file-change list.

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
Decisions with rationale and ADR links where appropriate.

## Risks and edge cases
Only risks grounded in the domain or current code.

## Expected outcomes
Observable conditions that demonstrate the change is correct. This is not an
automatically expanded acceptance-criteria taxonomy.

## Open questions
No question that changes contract, scope, security, data, migration, or material
cost may remain when status becomes Ready.

## Amendments
Explicitly accepted changes made after Ready.

---

## Build Evidence
Append-only delivery evidence owned by build.
```

### Immutable intent and amendments

When status becomes `Ready`, sections from `Problem and goal` through `Expected
outcomes` form the immutable intent baseline. `build` may update status and append
delivery evidence, but may not rewrite the baseline to match its implementation.

A material change uses:

```markdown
### A-{N} — YYYY-MM-DD
- Reason:
- Change:
- Accepted by:
```

An amendment is required when new information changes behavior, scope, a public
contract, security, data handling, migration, or material cost. Non-blocking
uncertainty belongs under explicit assumptions, not unresolved hidden intent.

## `build` contract

`build` owns implementation from accepted Brief to review-ready change. There is
no separate planning skill.

### Context

Before changing code, `build` reads:

- the complete accepted Feature Brief,
- linked ADRs,
- active relevant project-memory entries and scoped Gotchas,
- current project instructions,
- current code and tests needed to validate the Brief's evidence and direction.

Fresh code evidence overrides stale memory. A contradiction with binding intent
or an ADR is reported, not silently resolved.

### Conditional Execution Map

No map is created for one cohesive result that can safely finish in the current
session. A map is created when work has multiple dependent outcomes or requires
durable resumption.

The decision is based on cohesion, dependencies, uncertainty, and resumability,
not line count or file count.

Each map section contains only:

```markdown
## Section {N}: {outcome name}
- Status: pending | in-progress | complete
- Goal:
- Boundaries:
- Dependencies:
- Verification:
- Result:
- Material deviations:
```

The map must not contain micro-tasks, symbol recipes, or a prescriptive file list.

### Autonomous execution

For each result, `build` performs:

```text
implementation -> focused tests -> diagnosis -> fixes
```

After all results, it performs:

```text
relevant broader tests
-> lint/typecheck/build where applicable
-> whole-diff inspection against the Feature Brief
-> fixes
```

It updates durable map status only after the section's verification succeeds and
appends concise Build Evidence including changed areas, verification commands and
results, material implementation decisions, deviations, and possible durable
memory lessons.

`build` does not ask for approval at every section or for ordinary local
implementation choices. It stops only for:

- a material unresolved product decision,
- required scope expansion,
- a migration or security risk absent from the Brief,
- contradiction between Brief, ADR, binding project rules, and current evidence,
- a genuine external blocker that cannot be resolved from available context.

If new information changes the immutable baseline, `build` requests an explicit
amendment. It does not silently edit intent.

Subagents are optional for genuinely independent research or disjoint work. They
are never mandatory workers or quality gates. The primary implementing context
retains ownership of the whole result.

## `review` contract

There is one independent review after `build` finishes all verification. It runs
in a fresh context: a new session or one isolated reviewer.

### Inputs

- accepted Feature Brief and amendments,
- linked ADRs and binding project rules,
- complete final diff,
- Build Evidence and Execution Map when present,
- test and verification results.

### Review scope

The reviewer checks:

- intent and scope fidelity,
- correctness and meaningful edge cases,
- security and data integrity,
- adequacy of tests,
- regressions and compatibility,
- unintended changes outside scope,
- garbage left in the diff.

It does not report:

- subjective preferences,
- an alternative architecture merely because the reviewer prefers it,
- unrelated existing problems,
- formatting already enforced by deterministic tooling,
- hypothetical risks without a concrete failure scenario.

### Finding contract

Findings use only:

- `BLOCKING` — must be fixed before ship;
- `FOLLOW-UP` — valuable but not required for this feature to ship.

Every finding contains concrete evidence, impact, and the smallest sensible
correction. The result is persisted in `review.md`.

### Fix loop

```text
review
  -> no BLOCKING: ship
  -> BLOCKING: build fixes -> verification -> targeted re-review
```

No task document or repair planning stage is created. Targeted re-review first
resolves previous blockers, then performs a short regression scan of the changed
diff. It does not restart an open-ended search for stylistic improvements.
Accepted unresolved `FOLLOW-UP` items are preserved for the Feature Record.

Automatic triada is not part of the standard workflow. A specialist or
multi-agent audit may be invoked manually for unusually high-risk work.

## `ship` contract

`ship` runs only after final review has no open `BLOCKING` findings and all review
fixes have been re-verified.

### Sources of truth

- Feature Brief: why the change was requested and what was accepted.
- Final diff: what was actually built.
- Verification and review evidence: why the final state is believed ready.

`ship` explicitly reports differences rather than rewriting the Brief after the
fact.

### Feature Record format

The final `feature-record.md` contains:

```markdown
# Feature: {name}

## Status
Shipped date and commit.

## Original intent
Preserved accepted intent baseline.

## What was built
Outcome summary derived from the final diff.

## Deviations from the Brief
Different implementation, omitted scope, added scope, or explicitly none.

## Verification
Final commands, results, and meaningful manual checks.

## Review outcome
Resolved blockers and accepted follow-ups.

## Architectural decisions
Links to ADRs.

## Durable knowledge
Promoted project memory and scoped Gotchas.

## Open follow-ups
Explicitly deferred work.
```

### Executive Summary HTML

`executive-summary.html` is generated from the final post-review state for a
human PR reviewer. It is self-contained and includes:

- TL;DR,
- problem and business value,
- final scope,
- primary behavior/data flow,
- changed-component map,
- key decisions and rationale,
- rejected alternatives when material,
- deviations from the Brief,
- tests and verification,
- blockers found and fixed by review,
- remaining follow-ups and risks,
- recommended file review order,
- links to ADRs and durable documentation.

Small diagrams may show before/after flow, component relationships, or the main
sequence. The HTML is not an input to model review and is never generated before
review fixes finish.

### Human gate and closeout

Before mutation, `ship` shows:

- files to stage,
- proposed Feature Record,
- Executive Summary preview/path,
- proposed memory promotions and destinations,
- commit message,
- PR description,
- archive and deletion operations.

Only after approval does it:

1. promote approved durable memory,
2. create the final archive,
3. remove active Brief, map, and review artifacts,
4. stage the agreed files,
5. create the local commit.

It does not push, create a PR, merge, or rewrite history without a separate
explicit request.

## ADR and project-memory contracts

### ADRs

- ADRs live under `docs/adr/`.
- They capture architecture decisions with durable consequences, alternatives,
  rationale, and consequences.
- They are not created for file naming, ordinary implementation detail, or a
  decision local to one disposable implementation step.
- Feature Briefs and Feature Records link to relevant ADRs rather than duplicate
  their full content.

### Project memory

- Cross-cutting durable lessons live in `absolutforge/project-memory.md`.
- A trap relevant only inside one package belongs in that package's `CLAUDE.md`
  under `Gotchas`, mirrored to `AGENTS.md` where both harnesses are supported.
- Memory stores recurring traps, warning signs, root causes, and reusable
  resolutions, not feature status, one-off incident history, ADR decisions, or
  temporary hypotheses.
- Existing memory is prior context, not current proof. Fresh evidence wins.
- Promotion requires explicit user approval and a stated destination.
- Prefer updating or superseding an existing matching lesson over duplication.

`build` and `debug` may collect candidates. `ship` presents relevant candidates
for promotion as part of closeout.

## `debug` contract

`debug` is autonomous and may auto-trigger only for a concrete failure. It finds
root cause before proposing or implementing a fix.

### Diagnosis-only request

Reproduce, gather evidence, trace data flow, test a focused hypothesis, and report
the confirmed root cause. Do not change code and do not create delivery artifacts.

### Diagnosis and fix request

```text
reproduce
-> evidence
-> root-cause hypothesis
-> minimal hypothesis test
-> failing regression test where feasible
-> compact Fix Brief
-> implementation
-> test-and-fix loop
-> final verification
-> review handoff
```

The Fix Brief uses the normal feature lifecycle and contains:

- symptoms and reproduction,
- confirmed root cause with evidence,
- expected behavior,
- fix scope,
- solution direction,
- failing test or other failure proof,
- verification conditions,
- Build Evidence.

It does not require a separate `discuss` session when root cause and expected
behavior make the contract unambiguous. If investigation reveals a product
decision, public-contract change, major architectural redesign, or comparable
ambiguity, `debug` creates a draft Fix Brief with its evidence and hands it to
`discuss` instead of guessing.

Large fixes are not routed to detailed task generation. `debug` remains
autonomous unless a material product/architecture decision requires discussion.

## `tech-debt` contract

`tech-debt` is explicit-only, static, evidence-based, and read-only. It answers:

> Which current compromises create the highest ongoing engineering cost, and
> what is the smallest safe next action?

It may inspect code, tests, configuration, manifests, relevant documentation,
and limited history. It does not run application code, edit audited source, or
claim current dependency/security facts without verified evidence.

Each concise finding includes:

- category,
- priority,
- impact and confidence,
- repository-relative evidence,
- ongoing cost,
- smallest safe next action,
- route.

Routes are:

- `discuss` when remediation needs product or architecture decisions,
- `debug` when evidence suggests an active defect,
- `WATCH` when evidence is insufficient or cost does not justify action.

A simple remediation still needs a compact accepted Brief before `build`; the
audit itself never implements findings. Multi-agent waves are optional, not a
mandatory part of the workflow.

## Validation strategy

### Deterministic checks

- valid Claude and Codex manifests,
- valid skill frontmatter,
- correct native handoff syntax and artifact paths,
- absence of forbidden classic-pipeline stages,
- no SessionStart hook,
- self-contained Executive Summary output,
- `ship` cannot push or create a PR without explicit permission.

### Behavioral scenarios

1. `discuss` creates a precise Brief without task decomposition.
2. Small `build` does not create an unnecessary Execution Map.
3. Larger `build` creates and resumes from an outcome-oriented map.
4. Scope-changing discovery triggers an amendment rather than silent intent edit.
5. `review` reports concrete `BLOCKING`/`FOLLOW-UP` findings without style noise.
6. `ship` preserves original intent, records deviations, and creates final HTML.
7. Fixing `debug` creates a compact Fix Brief; diagnosis-only `debug` does not.
8. `tech-debt` stays read-only and routes findings correctly.

Behavioral model tests are run deliberately, not on every CI commit.

### Comparative pilot

Run AbsolutPowers and AbsolutForge separately on 3-5 representative real changes.
Measure:

- total token use,
- elapsed delivery time,
- handoff and artifact count,
- blockers found only at final review,
- findings later discovered by a human,
- fidelity to original intent,
- rework rounds,
- ease of resumption in a fresh session.

The pilot should identify where AbsolutForge works best, not manufacture a
universal winner.

## Known planning questions

The product behavior above is accepted. The following implementation-level
questions remain intentionally deferred to phase planning:

- minimum supported Claude Code and Codex versions,
- exact manifest and local enable/disable mechanics,
- precise fresh-context mechanism for review in each harness,
- self-contained diagram rendering implementation for Executive Summary,
- representative projects and changes used in the comparative pilot.

