# Phase 3: Build (epic: AbsolutForge MVP)

## Parent context

> Start by reading `absolutforge/features/absolutforge-mvp/planning-main.md`.

- Epic planning: `absolutforge/features/absolutforge-mvp/planning-main.md`
- Dependencies: Phase 2 Feature Brief contract

## Status
To plan — 2026-08-27

## Phase goal

Deliver an autonomous implementation workflow that owns local planning, creates
an outcome-oriented Execution Map only when useful, supports resumption, and runs
focused plus final verification before handing the complete change to review.

## Scope

### In scope

- Binding context loading from the Brief, ADRs, active memory, and current code.
- Conditional Execution Map creation and durable section statuses.
- Autonomous sequential implementation without per-section human gates.
- Focused test-and-fix loops and final relevant verification.
- Append-only Build Evidence and explicit amendment escalation.

### Out of scope

- A separate planning skill.
- Detailed persistent task lists or file/symbol recipes.
- Mandatory phase workers or review subagents.
- Final independent review.

### Deliberately not doing

- Creating an Execution Map for every change.
- Treating section completion as a human approval boundary.

## Assumptions and decisions

### Assumptions

- The implementing model can derive and revise its local plan from the accepted
  intent and live code.

### Decisions requiring confirmation

- TODO — define the exact threshold and resumability contract for creating an
  Execution Map.

## Selected solution
TODO — to plan in a separate phase session.

### Rationale
TODO

### Alternatives considered
TODO

## Implementation plan
TODO — to plan in a separate phase session.

## Files to modify or create
TODO

## Edge cases and risks
TODO

## Acceptance Criteria
TODO — define during phase planning without an automatic QA-enrichment gate.

## Open questions

- How should pre-existing test failures be recorded without allowing them to
  hide regressions caused by the feature?

## Discussion notes

- Delegation is optional for independent research or genuinely disjoint areas,
  never a required ceremony.

