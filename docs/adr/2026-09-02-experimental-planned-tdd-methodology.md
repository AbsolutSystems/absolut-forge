# ADR: Experimental TDD methodology for planned Build

**Date:** 2026-09-02  
**Status:** Accepted

## Decision

Add `build-planned-tdd` as an experimental execution methodology within the existing first-class `planned` Build strategy. Keep `build-planned` unchanged as the standard methodology and preserve the repository invariant that a Ready Feature Brief has exactly two first-class implementation strategies: autonomous and planned.

Record `Planned methodology: standard | tdd` in Build start evidence, the implementation plan, final Build evidence, saved context, Review, and the shipped Feature Record. Missing methodology in legacy planned artifacts means `standard`. Strategy or methodology may change only by abandoning the active Build and restarting from a clean committed Ready baseline.

For TDD tasks that change observable behavior, require auditable RED-GREEN-REFACTOR cycles derived from the existing risk-based Test Obligations. Permit characterization-first execution for behavior-preserving refactors and the existing verification exemptions where no automated behavior test applies. Do not manufacture RED failures or measure quality by test count or coverage alone.

Treat a test as a bound guard only after a targeted mutation proof: temporarily removing or reversing the production behavior it claims to protect must make the narrow test fail for the expected reason, and restoring the implementation must return it to green. Apply the same binding proof to characterization tests without fabricating an initial RED.

Execute TDD tasks serially. This sacrifices planned parallel-wave throughput so failure attribution and test-before-production chronology remain clear. Workers may execute bounded cycles, but the high-capability orchestrator still validates test value, the final diff, fast task gates, binding proofs, task evidence, commits, and whole-feature integration.

Keep execution feedback cost-tiered: RED and GREEN run one unit case or the narrowest unit target, task checkpoints run only owned fast unit tests and cheap static checks, and the authoritative broad regression plus integration/e2e suite runs at final whole-feature verification. Integration-only risks remain explicit final-verification obligations rather than being replaced with mocks that erase the real contract.

## Consequences

- Existing `build-planned` behavior remains available and is the normal planned methodology.
- TDD experiments share the same Brief, plan, Review, and Ship contracts, enabling comparable outcomes without a third strategy or artifact type.
- Slow integration and full-suite cost is paid at the final gate rather than once per behavior cycle or task.
- Each guard costs one additional narrow mutation/restore check but exposes tests that pass without depending on the production behavior they claim to protect.
- A fair comparison requires independent branches or worktrees from the same clean committed Ready baseline.
- TDD adds execution time and evidence overhead and deliberately gives up parallel task waves.
