# Codex Primitive Mapping

Use native Codex file and shell primitives for repository inspection, edits and verification. Explicit skill invocation uses `$absolutforge {skill} ...`.

## Planned Build

The orchestrator is the model and reasoning profile of the main session that invoked `build`; the skill does not switch it automatically. That session owns planning, difficult decisions, validation and integration, and must be capable of high-tier work.

For new standard planned builds, use this dispatch mapping:

| Task capability | Execution model | Reasoning effort |
| --- | --- | --- |
| `low` | `gpt-5.6-luna` | `high` |
| `standard` | `gpt-5.6-luna` | `xhigh` |
| `high` | Main-session orchestrator | Current session setting |

Use explicit model and reasoning-effort overrides for low/standard workers; do not rely on inherited defaults. Dispatch one fresh bounded context per task with no inherited orchestrator conversation (`fork_turns="none"` when using Codex spawn_agent). A fully disjoint dependency-ready wave may run in parallel. High tasks and high-risk corrections stay with the main-session orchestrator under standard methodology.

Luna `xhigh` may own a larger coherent behavior slice across multiple files, including implementation, wiring and its focused tests, when shared contracts are settled, ownership is bounded, and the result has one meaningful acceptance gate. Follow Task design in `planned-build-contract.md`; do not fragment that slice into per-file or code-versus-test tasks merely to use a cheaper tier. More reasoning does not make unresolved architecture, migration, security/data or concurrency decisions standard work. Return such evidence for a PC escalation to high rather than repeatedly retrying the same inadequate task.

If dispatch or the exact requested worker profile is unavailable, report the unavailable profile and execute the standard-methodology task in the main session; never silently substitute another worker model/effort or pretend delegation occurred. If the main session cannot safely handle it, preserve the last clean boundary and report the limitation. This fallback never applies to legacy delegated state.

These are defaults for new standard builds. Existing standard plans retain completed definitions/evidence and any explicitly recorded execution commitments; changing pending task granularity or capability requires a PC entry. Never migrate legacy delegated ownership or its fixed profile to the new mapping.

A worker gets one Task Capsule only, using the canonical fields in `planned-build-contract.md`. Add only the applicable accepted clauses, dependency facts and relevant source/tests needed to execute it; never preload the full Brief, plan, history or orchestrator dialogue. It may edit only the approved task surface. Dependency-ready tasks may run as one parallel wave only when write surfaces are fully disjoint. The primary context validates and checkpoint-commits each task separately before marking it complete.

### Legacy delegated resume

New delegated starts are unavailable. A feature whose durable Build evidence records `planned` / `delegated` resumes through `build`. Keep the invoking high-capability primary context as planner/orchestrator; its fixed legacy executor is Luna with high reasoning effort. Require native subagent dispatch with an explicit model and reasoning-effort override before continuing.

Dispatch every implementation task and correction with model `gpt-5.6-luna` and reasoning effort `high`. Use one fresh bounded subagent per task with no inherited conversation and send only its minimum execution package. The primary context may inspect files, update workflow artifacts, run checks, and commit accepted results, but it never edits production code or tests. If Luna high cannot be requested or a delegated task remains `high` after planning, stop without substituting another model or taking over implementation.

## Review

When fresh agents are available, dispatch exactly one fresh generic read-only reviewer. Its startup package is only the Brief and accepted amendments, final Build Evidence, `base_commit..HEAD` diff, and changed/new tests. Load plan or history lazily only for a concrete coverage, lifecycle, or legacy-ownership question; never preload implementation conversation or conclusions. If unavailable, use the same bounded package inline and label it `advisory (not fully isolated)`.
