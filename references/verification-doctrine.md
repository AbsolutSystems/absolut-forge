# Verification Doctrine

Defines what `focused verification` and `final verification` mean for both Build strategies. Host-agnostic and strategy-agnostic.

## Scope

Binding for `build` and `build-planned`, and for any bounded fix `debug` makes inside a feature under Build. A `debug` fix that changes observable behavior carries a regression test pinning the defect, under the same exemption rule; the Build owner records it in that stage's evidence. Standalone `debug` diagnosis writes no code and needs no test. `tech-debt` is read-only and out of scope.

## Default expectation

Every coherent outcome or task that changes observable behavior lands together with executable automated tests that exercise that behavior. By default write them after that stage's implementation; in every case before the stage is marked complete. An outcome or task whose behavior change has no executable test and no recorded exemption is not complete.

This is not test-driven development. Test-first is allowed but never required, and no ceremony, coverage target, or test plan artifact is expected.

## Test value bar

Aim at what a senior engineer would write to convince themselves the change actually works:

- the primary accepted behavior of the change;
- the realistic failure or boundary the change itself introduces — specified error paths, absent/empty input that is genuinely reachable, contract behavior at a seam other code depends on;
- a regression test pinning any defect fixed during the stage.

Prefer a few meaningful assertions over many shallow ones. A test must fail if the change is reverted; if it passes either way it has no value.

That criterion is judged by inspection: does at least one assertion bind an observable value or effect that only the change produces? Do not revert production code to prove it. Deliberately breaking the implementation to watch a test fail is a local scratch experiment only, and the worktree must be restored before the stage is marked complete.

## Explicitly out of scope

- speculative edge cases with no reachable caller;
- exhaustive input permutations, parameterized matrices for their own sake;
- tests asserting mock configuration, framework behavior, or tautologies;
- whole-output snapshots used as a substitute for a real assertion;
- coverage percentage goals;
- restructuring existing production code purely to make it testable, beyond the accepted change surface.

## Follow the repository

Discover the existing test framework, layout, naming, fixtures, and helpers, and match them. Introducing a new test framework, runner, or testing architecture is product-material: it needs Brief, amendment, ADR, or binding-rule basis, otherwise it is an intent deviation.

## Recorded exemption

Tests may be omitted for a stage only when the change is genuinely untestable or has no behavior to assert — configuration or docs only, pure rename/move, generated output, or a surface that cannot be exercised without infrastructure the Brief did not accept. Repository lacking any runnable test harness is also a valid exemption.

An exemption is never silent. Record `Tests: none — {reason}` plus whatever observable check was performed instead. Difficulty, time, or unfamiliarity is not a reason.

## Green is not negotiable

A failing check is evidence; handle it under the active Build failure boundary. Never delete, weaken, loosen, or skip an existing assertion or test to reach green. Changing an existing test is legitimate only when the accepted Brief changed that behavior; then state which accepted outcome authorizes it. Any other weakening of an existing test is a blocking deviation.

## Final whole-feature verification

At finish, beyond re-running relevant broader build/test/type/lint checks, exercise the feature's primary accepted path at integration level at least once — an existing integration/e2e suite, a new integration test where the repository already supports that layer, or a scripted end-to-end run of the real entry point.

Keep it to the main accepted path or two, not an integration matrix. If the repository cannot run that layer, or standing it up would exceed the accepted scope, record that plus the closest whole-feature check actually performed.

## Evidence

Verification evidence names test files and cases added or updated, the commands run, and their results. `tests pass` without command or scope is not evidence.
