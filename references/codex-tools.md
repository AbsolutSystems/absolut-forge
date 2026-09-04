# Codex Primitive Mapping

Use native Codex file and shell primitives for repository inspection, edits and verification. Explicit skill invocation uses `$absolutforge {skill} ...`.

## Planned Build

For `build-planned`, keep the configured high-capability primary context as orchestrator. If `multi_agent=true` or an equivalent fresh-worker primitive is available, dispatch bounded tasks by the capability tiers in `references/model-routing.md`. A fully disjoint dependency-ready wave may run in parallel. Typical deployment guidance is Sol for orchestration/high tasks, Terra for standard tasks, and Luna for low tasks.

A worker gets the smallest redacted package that can execute its task: task contract, needed Brief/ADR invariants, dependency facts, relevant source/tests and verification commands. It may edit only the approved task surface. Dependency-ready tasks may run as one parallel wave only when write surfaces are fully disjoint. The primary context validates and checkpoint-commits each task separately before marking it complete.

If worker dispatch is unavailable, the orchestrator executes the task itself; do not pretend delegation occurred.

### Planned delegated methodology

For `build-planned-delegated`, keep the invoking high-capability primary context as planner/orchestrator; Sol with high reasoning effort is the recommended profile. Before Build start, require native subagent dispatch with an explicit model and reasoning-effort override.

Dispatch every implementation task and correction with model `gpt-5.6-luna` and reasoning effort `high`. Use one fresh bounded subagent per task with no inherited conversation and send only its minimum execution package. The primary context may inspect files, update workflow artifacts, run checks, and commit accepted results, but it never edits production code or tests. If Luna high cannot be requested or a delegated task remains `high` after planning, stop without substituting another model or taking over implementation.

## Review

When fresh agents are available, dispatch exactly one fresh generic read-only reviewer. Review remains whole-feature and derives `base_commit..HEAD` itself. If unavailable, use the inline advisory fallback and label it explicitly.
