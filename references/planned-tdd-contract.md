# Planned TDD Contract

## Purpose and relationship

`build-planned-tdd` is an experimental execution methodology within the first-class `planned` Build strategy. It inherits the complete planned Build, artifact, verification, routing, and host contracts. This document defines only the TDD-specific deltas.

The methodology is durable execution state. Record `Planned methodology: tdd` at Build start and in `implementation-plan.md`. Absence of the field in an artifact created before this contract means `standard`; never infer TDD from test layout or conversation history.

## Plan extension

Every TDD plan uses the canonical schema in `planned-build-contract.md` with these task fields:

```markdown
- TDD mode: required | characterization | exempt — {verification-doctrine reason}
- TDD evidence: pending | {concise ordered cycle evidence} | exempt — {reason and closest observable check}
```

Use `required` for a task that changes observable behavior. Use `characterization` for a behavior-preserving refactor whose safety is established by a focused test or existing suite before production edits. Use `exempt` only where `verification-doctrine.md` permits no automated behavior test.

For a completed `required` task, evidence identifies every distinct cycle and keeps chronology auditable without retaining raw logs:

```text
R-001: {test file and case}; RED: {command -> expected failure and why}; GREEN: {command -> pass}; REFACTOR: {scope -> command/result}
```

When no refactor is useful, record `REFACTOR: none — design adequate; {green check}` rather than changing code ceremonially. Characterization evidence records the test or suite and its before/after commands and results.

One cycle may satisfy multiple obligations when one observable test genuinely binds them. Several distinct risks require several tests or an explicit explanation of how the evidence covers them. The ordinary Completion Evidence still records changed paths, final commands/results, local decisions, and new dependency or invariant facts.

## Valid cycles

Run the relevant baseline before the first RED so pre-existing failures cannot masquerade as TDD evidence. Test-only fixtures or support may be added before RED, but no production behavior for the slice may be implemented first.

A valid RED:

- asserts an externally observable value or effect required by the Brief or Test Obligation;
- fails because that accepted behavior is missing or defective;
- uses the repository's existing test framework and conventions;
- is narrow enough that its failure cause is attributable.

Syntax errors, broken fixtures, unrelated suite failures, and assertions that do not bind changed behavior are invalid RED evidence. A compile or type failure is valid only when it is narrowly and directly caused by the intentionally missing accepted contract exercised by the new test; test-harness or dependency breakage is not. A test that passes before production changes triggers investigation: the behavior may already exist, the assertion may be weak, or the plan may need a `PC-` correction. Do not falsify a RED or make an unrelated change merely to produce failure.

GREEN is the smallest sensible production change that makes the RED test pass without violating accepted scope or existing contracts. In REFACTOR, assess the resulting design and improve production or test structure only where useful while the relevant tests remain green; do not create ceremonial churn. Repeat the cycle for the task's remaining distinct risks, then run ordinary focused verification.

Characterization establishes a passing protective test or focused existing suite before behavior-preserving edits and keeps it passing afterward; it does not fabricate a RED. An exemption records the canonical reason and closest observable check.

## Dispatch, validation, and commits

Execute one dependency-ready task at a time. Parallel waves are disabled for this methodology so concurrent dirty changes cannot obscure RED attribution or production-before-test ordering.

A delegated worker owns the complete cycles for one bounded task and reports ordered evidence. The orchestrator independently inspects the diff, verifies that tests bind changed behavior, confirms the write boundary, and reruns final focused checks. Because final code cannot reproduce historical RED without reverting production, the orchestrator validates the recorded failure cause against the test and diff rather than manufacturing a second RED.

Create one orchestrator-owned checkpoint commit after the complete task is green, refactored, focused checks pass, and evidence is recorded. Separate RED/GREEN commits are optional and not required; workers never commit.

If interrupted mid-cycle, use `save` for concise chronology and resume context, while remembering that Save does not preserve dirty source itself; the working tree must still survive independently. A completed task checkpoint remains the clean context-rotation boundary.

## Evaluation boundary

Comparing `build-planned` with `build-planned-tdd` requires independent runs from the same clean committed Ready baseline on separate branches or worktrees. Never switch methodology during an active Build. Evaluate whole-feature Review findings, risk coverage, test value, regression resistance, implementation clarity, verification stability, and execution cost; raw test count or line coverage alone is not a quality result.
