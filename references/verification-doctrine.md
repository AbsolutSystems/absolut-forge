# Verification Doctrine

Binding for `build` (both strategies, including legacy delegated resume), `review`, and a `debug` fix made inside an active feature. Planners read this doctrine at compilation, materially revised obligations or coverage ambiguity. Executors receive concrete projected obligations; reviewers use the runtime checklist and escalate uncertain classifications here. This changes loading policy only.

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

A useful test exercises repository-owned observable behavior: a business result, state transition, persisted effect, error, or contract at a meaningful seam. Its assertions must establish that outcome rather than merely repeat setup, prove that a mock was configured, count calls with no behavioral significance, or validate framework/library behavior that the repository does not own.

Mocks and fakes are acceptable at external or expensive seams, but the test must still assert the resulting repository-owned behavior or an outbound contract that is itself part of the accepted behavior. Avoid tests coupled mainly to private helpers, incidental implementation structure, dependency-injection wiring, framework defaults, or snapshots that restate undifferentiated output. Review judges this from the test, production diff, and accepted behavior; Build does not deliberately break working production code to prove that a test can fail.

All required test targets must be green before an outcome, task, or final gate completes. Never weaken, skip, or delete an existing assertion to reach green unless an accepted Brief change explicitly requires the old behavior to change.

Do not introduce a new test framework or restructure unrelated production code solely for testing without accepted product or architecture authority.

## Recorded exemption

Omit automated tests only when there is no behavior to assert or the behavior cannot be exercised within accepted scope: documentation or configuration only, a pure rename/move, generated output, missing runnable test infrastructure, or required external infrastructure outside the Brief.

Record `Tests: none — {reason}` and the closest observable check performed. Difficulty, time, or unfamiliarity are not exemptions.

## Fast and final verification

During an outcome or task, run only its exact or smallest relevant unit-test targets plus cheap build, type, or lint checks that directly cover its surface. Do not run the full changeset, workspace suite, integration suite, or end-to-end suite at an intermediate checkpoint. Map obligations observable only across a real integration boundary to final verification. Evidence names test files and cases, commands, and results; `tests pass` alone is not sufficiently specific evidence.

At finish, run the authoritative full suite for the affected project or changeset once per final-verification attempt and exercise the feature's primary accepted path. Include the planned integration and end-to-end checks without rerunning a suite separately when the full command already contains it. If that layer is unavailable or outside accepted scope, record the reason and the closest whole-feature check actually performed.

A compile, bundle, package, or artifact-production command is not by itself an exercised whole-feature path unless producing that artifact is the accepted behavior under review. Otherwise record it only as the closest check, together with the reason the primary accepted path could not be exercised.

## Delegated methodology

Legacy delegated resume through `build` applies this charter through `planned-delegated-contract.md`. The fixed executor writes and runs focused tests; the orchestrator independently judges their semantic value and reruns required gates. A missing or weak guard returns as a bounded correction to the same executor profile rather than being repaired in the orchestrator context.
