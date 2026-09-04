# ADR: Green test gates and semantic test review

**Date:** 2026-09-04
**Status:** Accepted

## Decision

Remove mandatory targeted mutation proofs from autonomous Build, standard planned Build, planned TDD, Build Evidence, execution artifacts, Review, and Ship records. A completed outcome, task, or final verification gate requires its applicable test commands to pass, but Build does not deliberately remove or reverse working production behavior merely to prove that a test becomes red.

Keep the risk-based Test Charter. Tests must exercise repository-owned observable behavior such as business results, state transitions, persisted effects, errors, or meaningful seam contracts. Mocks and fakes remain valid at external or expensive seams, but assertions must establish repository-owned behavior or an outbound interaction that is itself part of the accepted contract. Tests that mainly verify mock configuration, insignificant call counts, framework/library behavior, dependency-injection wiring, private helpers, or incidental implementation structure do not satisfy an obligation.

Review judges test value by reading the accepted behavior, implementation diff, tests, and green execution evidence. It remains read-only and never changes production code to force a test failure.

Preserve the initial RED in experimental `build-planned-tdd`: it records that a test was written before the missing behavior. Remove the post-GREEN mutation/kill/restore cycle. Characterization uses green before/after evidence without a manufactured failure.

## Consequences

- Build verification is cheaper and leaves no intentional broken-code interval after implementation is green.
- Review carries explicit responsibility for detecting test theater and misplaced assertions.
- Existing append-only artifacts may retain historical `Test binding proofs` fields, but new evidence omits them and Review does not gate on them.
- This ADR supersedes the targeted mutation-proof requirements added in release `0.5.1` and the mutation-proof portions of `2026-09-02-experimental-planned-tdd-methodology.md`; its RED-GREEN-REFACTOR and serial-execution decisions remain in force.
