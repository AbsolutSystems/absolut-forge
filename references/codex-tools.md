# Codex Primitive Mapping

Use native Codex file and shell primitives for repository inspection, edits and verification. Explicit skill invocation uses `$absolutforge {skill} ...`.

## Planned Build

For `build-planned`, keep the configured high-capability primary context as orchestrator. If `multi_agent=true` or an equivalent fresh-worker primitive is available, dispatch bounded tasks by the capability tiers in `references/model-routing.md`, using fresh bounded contexts with no inherited full orchestrator chat. A fully disjoint dependency-ready wave may run in parallel. Codex deployment guidance is Sol for orchestration and high tasks, Luna with high reasoning effort for low tasks, and Luna or Terra for standard tasks according to the task's coordination complexity.

A worker gets one Task Capsule only, using the canonical fields in `planned-build-contract.md`. Add only the applicable accepted clauses, dependency facts and relevant source/tests needed to execute it; never preload the full Brief, plan, history or orchestrator dialogue. It may edit only the approved task surface. Dependency-ready tasks may run as one parallel wave only when write surfaces are fully disjoint. The primary context validates and checkpoint-commits each task separately before marking it complete.

If worker dispatch is unavailable, the orchestrator executes the task itself; do not pretend delegation occurred.

### Legacy delegated resume

New delegated starts are unavailable. A feature whose durable Build evidence records `planned` / `delegated` resumes through `build-planned`. Keep the invoking high-capability primary context as planner/orchestrator; its fixed legacy executor is Luna with high reasoning effort. Require native subagent dispatch with an explicit model and reasoning-effort override before continuing.

Dispatch every implementation task and correction with model `gpt-5.6-luna` and reasoning effort `high`. Use one fresh bounded subagent per task with no inherited conversation and send only its minimum execution package. The primary context may inspect files, update workflow artifacts, run checks, and commit accepted results, but it never edits production code or tests. If Luna high cannot be requested or a delegated task remains `high` after planning, stop without substituting another model or taking over implementation.

## Review

When fresh agents are available, dispatch exactly one fresh generic read-only reviewer. Its startup package is only the Brief and accepted amendments, final Build Evidence, `base_commit..HEAD` diff, and changed/new tests. Load plan or history lazily only for a concrete coverage, lifecycle, or legacy-ownership question; never preload implementation conversation or conclusions. If unavailable, use the same bounded package inline and label it `advisory (not fully isolated)`.
