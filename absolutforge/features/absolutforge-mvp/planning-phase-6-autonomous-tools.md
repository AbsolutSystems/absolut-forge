# Phase 6: Autonomous tools (epic: AbsolutForge MVP)

## Parent context

> Start by reading `absolutforge/features/absolutforge-mvp/planning-main.md`.

- Epic planning: `absolutforge/features/absolutforge-mvp/planning-main.md`
- Dependencies: Phase 1 memory contract and Phase 2 Feature Brief contract

## Status
To plan — 2026-08-27

## Phase goal

Deliver an autonomous root-cause `debug` workflow and a static, read-only
`tech-debt` workflow adapted to AbsolutForge without importing the classic
task-generation pipeline.

## Scope

### In scope

- Root-cause investigation, hypothesis testing, failing-test fix workflow, and
  memory capture for `debug`.
- Compact automatic Fix Brief creation when `debug` implements a fix.
- Product/contract uncertainty handoff from `debug` to `discuss`.
- Evidence-based, prioritized, static technical-debt reports.
- Routes from selected debt findings to `discuss` or `debug`.

### Out of scope

- `problem-discuss`, QA review, or broad client-intake workflows.
- Routing large fixes or debt items to `generate-tasks`.
- Mandatory multi-agent waves for technical-debt audits.

### Deliberately not doing

- Creating a Fix Brief for diagnosis-only requests that make no change.
- Allowing `tech-debt` to edit audited source or implement findings.

## Assumptions and decisions

### Assumptions

- Debugging and debt discovery are autonomous tools whose value does not depend
  on detailed implementation task artifacts.

### Decisions requiring confirmation

- TODO — finalize concise output schemas and handoffs during phase planning.

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

- Should a debug fix automatically enter `review`, or only emit the explicit
  review handoff command?

## Discussion notes

- Fix Briefs use the same lifecycle as feature Briefs so `ship` remains uniform.

