# ADR: Fixed-executor planned methodology

**Date:** 2026-09-04
**Status:** Accepted

## Decision

Replace experimental `build-planned-tdd` with `build-planned-delegated`, a methodology inside the existing first-class `planned` Build strategy. Preserve the repository invariant that a Ready Feature Brief has exactly two first-class implementation strategies: autonomous and planned.

In delegated methodology, a high-capability primary model is the planner and orchestrator. It reads the accepted Brief and repository, resolves architecture, and writes a durable task graph for an early-mid executor. Task contracts explain responsibilities, integration approach, relevant paths and symbols, invariants, edge cases, likely traps, test obligations, verification, and the boundary between local choices and decisions that must return to the orchestrator. They do not contain implementation code, pseudocode, pseudo-diffs, or line-by-line edit scripts.

Every production and test edit, including corrections after orchestrator validation or Review, belongs to one fixed host-mapped executor profile. The orchestrator owns lifecycle state, the plan, plan changes, worker supervision, verification, checkpoint commits, and whole-feature integration, but never completes or repairs implementation itself. If the fixed executor is unavailable or a task cannot be made safe for it through planning and decomposition, stop rather than substitute a model or silently change methodology.

Keep model identities out of shared skill and artifact semantics. Host references bind the deployment profiles: Codex uses Luna with high reasoning effort; Claude dispatches the plugin agent `absolutforge:delegated-executor`, whose descriptor sets Opus 5 with low reasoning effort. Preflight must reject host or environment overrides that would change the effective profile, without mutating the user's environment. Other hosts require an explicitly configured equivalent and otherwise refuse the methodology before Build start.

Record `Planned methodology: delegated` throughout Build, Save, Review, and Ship. Methodology remains immutable after Build start. Legacy `tdd` artifacts remain valid evidence but have no current builder: unfinished work must resume with a compatible older release or be explicitly abandoned and restarted from a clean committed Ready baseline.

## Consequences

- The plan carries more senior implementation judgment than standard planned Build, while still avoiding code written in prose.
- Executor cost and capability are predictable because task-by-task model routing is disabled for this methodology.
- The planner must settle architecture and decompose away high-capability implementation decisions before dispatch.
- Primary-context takeovers are contract violations, including small fixes that appear faster to make directly.
- Standard `build-planned` remains available for flexible task routing and orchestrator-executed high-capability work.
- The experimental TDD skill, contract, commands, and active workflow state are removed. This ADR supersedes `2026-09-02-experimental-planned-tdd-methodology.md` and the TDD-specific consequence in `2026-09-04-green-tests-and-semantic-review.md`.
