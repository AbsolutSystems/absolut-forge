# Planned TDD Contract

## Purpose and relationship

`build-planned-tdd` is an experimental execution methodology within the first-class `planned` Build strategy. It inherits the complete planned Build, artifact, verification, routing, and host contracts. This document defines only the TDD-specific deltas.

The methodology is durable execution state. Record `Planned methodology: tdd` at Build start and in `implementation-plan.md`. Absence of the field in an artifact created before this contract means `standard`; never infer TDD from test layout or conversation history.

## Verification cost model

TDD execution uses three explicit verification levels:

1. **Inner loop** — run one new unit test case or the narrowest unit-test target supported by the repository during RED and GREEN. During REFACTOR, add only the smallest containing unit-test target needed for confidence.
2. **Task gate** — after the task's cycles, run its owned fast unit tests plus cheap compile, type, or lint checks that directly cover its surface.
3. **Final gate** — after all tasks are checkpointed, run the authoritative full suite for the affected project or changeset once per final-verification attempt. Include the planned integration and end-to-end checks and primary accepted path, but do not rerun those suites separately when the full command already includes them.

Do not run the full changeset, workspace, integration, or end-to-end suite in the inner loop or task gate. The point of the methodology is fast causal feedback, not repeated broad regression checks. A risk observable only across a real integration boundary belongs to the final gate and must be mapped there explicitly; do not hide that limitation behind mocks that remove the contract being tested.

For a TDD plan, each task's `Verification` distinguishes `Inner loop` from `Task gate`, and `Final verification` owns all integration, end-to-end, and broad regression commands. Prefer an observable unit-level contract over an implementation-detail assertion, and select the cheapest command that faithfully tests it.

## Plan extension

Every TDD plan uses the canonical schema in `planned-build-contract.md` with these task fields:

```markdown
- TDD mode: required | characterization | exempt — {verification-doctrine reason}
- TDD evidence: pending | {concise ordered cycle evidence} | exempt — {reason and closest observable check}
```

Use `required` for a task that changes observable behavior. Use `characterization` for a behavior-preserving refactor whose safety is established by a focused test or existing suite before production edits. Use `exempt` only where `verification-doctrine.md` permits no automated behavior test.

For a completed `required` task, evidence identifies every distinct cycle and keeps chronology auditable without retaining raw logs:

```text
R-001: {test file and case}; RED: {command -> expected failure and why}; GREEN: {command -> pass}; REFACTOR: {scope -> command/result}; MUTATION: {guarded production behavior and temporary reversal}; KILL: {same narrow command -> expected failure}; RESTORE: {command -> pass}
```

When no refactor is useful, record `REFACTOR: none — design adequate; {green check}` rather than changing code ceremonially. Characterization evidence records the test or suite and its before/after commands and results.

One cycle may satisfy multiple obligations when one observable test genuinely binds them. Several distinct risks require several tests or an explicit explanation of how the evidence covers them. Every claimed guard needs mutation evidence showing that removal or reversal of the production behavior it protects makes the narrow test fail for the expected reason. The ordinary Completion Evidence still records changed paths, final commands/results, local decisions, and new dependency or invariant facts.

## Valid cycles

Run the narrow unit-test baseline for the touched contract before the first RED so pre-existing failures cannot masquerade as TDD evidence. Do not use the complete changeset or an integration suite as this baseline. Test-only fixtures or support may be added before RED, but no production behavior for the slice may be implemented first.

A valid RED:

- asserts an externally observable value or effect required by the Brief or Test Obligation;
- fails because that accepted behavior is missing or defective;
- uses the repository's existing test framework and conventions;
- is narrow enough that its failure cause is attributable.

Syntax errors, broken fixtures, unrelated suite failures, and assertions that do not bind changed behavior are invalid RED evidence. A compile or type failure is valid only when it is narrowly and directly caused by the intentionally missing accepted contract exercised by the new test; test-harness or dependency breakage is not. A test that passes before production changes triggers investigation: the behavior may already exist, the assertion may be weak, or the plan may need a `PC-` correction. Do not falsify a RED or make an unrelated change merely to produce failure.

GREEN is the smallest sensible production change that makes the RED test pass without violating accepted scope or existing contracts. In REFACTOR, assess the resulting design and improve production or test structure only where useful while the new test and smallest relevant unit-test target remain green; do not create ceremonial churn. Repeat the cycle for the task's remaining distinct risks, then run the task gate defined by the verification cost model.

After REFACTOR, prove that each test remains bound to its claimed guard. Temporarily remove or reverse the smallest relevant production behavior, run the exact test case or narrowest target, confirm that it fails for the expected reason, restore the intended implementation, and confirm GREEN again. If the mutation survives, the test is not valid evidence: strengthen or replace it and repeat. A narrowly targeted mutation-testing tool may perform this proof, but a broad mutation suite does not belong in the inner loop. Never commit the mutated state; inspect the production diff after restoration.

Characterization establishes a passing protective unit test or fast focused unit suite before behavior-preserving edits, proves that it fails under a targeted mutation of the behavior it claims to protect, and keeps it passing afterward; it does not fabricate a RED. An exemption records the canonical reason and closest observable check.

## Dispatch, validation, and commits

Execute one dependency-ready task at a time. Parallel waves are disabled for this methodology so concurrent dirty changes cannot obscure RED attribution or production-before-test ordering.

A delegated worker owns the complete cycles for one bounded task and reports ordered evidence. The orchestrator independently inspects the diff, verifies each test's mutation evidence, confirms the write boundary and restored production state, and reruns the fast task gate. Because final code cannot reproduce historical RED without reverting production, the orchestrator validates the recorded RED and mutation failure causes against the test and diff rather than manufacturing another failure.

Create one orchestrator-owned checkpoint commit after the complete task is green, refactored, its task gate passes, and evidence is recorded. Separate RED/GREEN commits are optional and not required; workers never commit.

If the final gate fails, preserve all completed task definitions and evidence, append one `PC-` entry that adds a bounded corrective TDD task, increment the plan revision, and return to task execution. After that task is checkpointed, repeat the final gate before handoff.

If interrupted mid-cycle, use `save` for concise chronology and resume context, while remembering that Save does not preserve dirty source itself; the working tree must still survive independently. A completed task checkpoint remains the clean context-rotation boundary.

## Evaluation boundary

Comparing `build-planned` with `build-planned-tdd` requires independent runs from the same clean committed Ready baseline on separate branches or worktrees. Never switch methodology during an active Build. Evaluate whole-feature Review findings, risk coverage, test value, regression resistance, implementation clarity, verification stability, and execution cost; raw test count or line coverage alone is not a quality result.
