# Verification Doctrine

Binding for `build`, `build-planned`, `build-planned-tdd`, `review`, and a `debug` fix made inside an active feature.

## Test charter

For every coherent outcome or task that changes observable behavior, identify the distinct risks introduced by the change and add automated tests for every applicable obligation:

1. the primary accepted behavior;
2. an error or boundary introduced by the change;
3. a state or data-integrity invariant placed at risk;
4. a contract at a seam used by an existing caller or consumer;
5. a regression test for a defect fixed during the work.

The number of tests follows the number of distinct risks, not the number of outcomes or tasks. One test per task is not a default. Tests land with the outcome or task before it is complete and use the repository's existing framework, layout, fixtures, and helpers.

Apply extra attention where relevant:

- authorization or security: denied behavior and absence of an unintended effect;
- persistence: partial failure, atomicity, or idempotency;
- public contracts: compatibility with existing consumers;
- asynchronous or concurrent work: the material ordering, retry, or duplicate-delivery risk;
- migrations: representative old state and the resulting state.

An outcome or task has no obligation to invent inapplicable cases. Its evidence must nevertheless make the applicable obligations visible through named tests or a recorded exemption.

## Test value

A useful test binds an observable value or effect produced by the change and would fail if that behavior were absent. Prefer meaningful assertions over mock configuration, framework behavior, tautologies, or snapshots that merely restate whole output. Never weaken, skip, or delete an existing assertion to reach green unless an accepted Brief change explicitly requires the old behavior to change.

Do not introduce a new test framework or restructure unrelated production code solely for testing without accepted product or architecture authority.

## Binding proof

Every new or materially changed test recorded as a guard needs targeted mutation proof. Temporarily remove or reverse the smallest production behavior that it claims to protect, run the exact test case or narrowest supported target, and confirm it fails for the expected reason. Restore the intended implementation, rerun the same target to green, and inspect the production diff before checkpointing. If the mutation survives, strengthen or replace the test; never cite an unbound test as delivery evidence.

Keep the mutation temporary and local, and never commit mutated production state. A narrowly targeted mutation-testing command may replace the manual change, but a broad mutation suite is not required. Perform unit-level mutation proofs inside the outcome or task's fast gate. When a risk is observable only through integration, map both its exact-case mutation proof and its ordinary verification to the final gate rather than replacing the real boundary with mocks.

## Recorded exemption

Omit automated tests only when there is no behavior to assert or the behavior cannot be exercised within accepted scope: documentation or configuration only, a pure rename/move, generated output, missing runnable test infrastructure, or required external infrastructure outside the Brief.

Record `Tests: none — {reason}` and the closest observable check performed. Difficulty, time, or unfamiliarity are not exemptions.

## Fast and final verification

During an outcome or task, run only its exact or smallest relevant unit-test targets plus cheap build, type, or lint checks that directly cover its surface. Do not run the full changeset, workspace suite, integration suite, or end-to-end suite at an intermediate checkpoint. Map obligations observable only across a real integration boundary to final verification. Evidence names test files and cases, commands, mutation results, and ordinary results; `tests pass` alone is not evidence.

At finish, first perform the targeted proofs and checks mapped to real integration boundaries. Then run the authoritative full suite for the affected project or changeset once per final-verification attempt and exercise the feature's primary accepted path. Include the planned integration and end-to-end checks without rerunning a suite separately when the full command already contains it. If that layer is unavailable or outside accepted scope, record the reason and the closest whole-feature check actually performed.

## TDD methodology

`build-planned-tdd` adds chronological RED-GREEN-REFACTOR evidence and applies the shared binding and cost rules through `planned-tdd-contract.md`; it does not replace or reduce this risk-based charter. Do not manufacture a RED for a behavior-preserving refactor or valid exemption; characterization uses mutation proof instead.
