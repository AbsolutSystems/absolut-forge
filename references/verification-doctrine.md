# Verification Doctrine

Binding for `build`, `build-planned`, `review`, and a `debug` fix made inside an active feature.

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

## Recorded exemption

Omit automated tests only when there is no behavior to assert or the behavior cannot be exercised within accepted scope: documentation or configuration only, a pure rename/move, generated output, missing runnable test infrastructure, or required external infrastructure outside the Brief.

Record `Tests: none — {reason}` and the closest observable check performed. Difficulty, time, or unfamiliarity are not exemptions.

## Focused and final verification

Focused verification runs the tests owned by the outcome or task plus the narrow build, type, lint, or integration checks capable of exposing its risks. Evidence names test files and cases, commands, and results; `tests pass` alone is not evidence.

At finish, run relevant broader checks and exercise the feature's primary accepted path at integration level once through an existing integration/e2e suite, a supported integration test, or a scripted run of the real entry point. If that layer is unavailable or outside accepted scope, record the reason and the closest whole-feature check actually performed.
