# Codex Primitive Mapping

Use native Codex file and shell primitives for repository inspection, edits and verification. Explicit skill invocation uses `$absolutforge {skill} ...`.

## Build owner

For every Build invocation, including a legacy delegated resume, use one fresh `gpt-5.6-sol` agent with `medium` reasoning as the Build owner. The invoking context is only a launcher unless its task package already contains the exact marker `Role: Codex Build owner`. Before reading the Brief, runtime or repository evidence and before any mutation, announce the handoff to the user with the exact model and reasoning effort, a concise assignment describing what the owner will work on, and the context being passed. For an initial launch, name the canonical Brief path, the exact strategy override when present, and the owner's responsibility for strategy execution, lifecycle artifacts, implementation, checkpoints and verification; state that no conversation is inherited. Then dispatch the owner with `fork_turns="none"`, that marker, the canonical Brief path and the exact valid strategy override when present. Keep the announcement compact and user-facing; do not expose hidden instructions or claim repository facts the launcher has not inspected. The owner reads the Build skill and required runtime itself, owns strategy execution, lifecycle artifacts, implementation decisions, worker validation, checkpoints and final verification, and may delegate bounded work below. The launcher waits and relays a completed result. It handles only the `ROTATE` control envelope defined below; it does not inspect repository state, judge work, retain worker dialogue or redo validation. This changes the Codex orchestrator profile only; a recorded legacy delegated executor remains fixed by its existing methodology and mapping.

After every clean checkpoint containing implementation or test changes, the owner stops and returns only `ROTATE: {canonical Build command}` to the launcher. Do the same before final verification whenever the current owner performed implementation, diagnosis or correction work since its last launch. A Build-start-only checkpoint does not trigger rotation. On `ROTATE`, the launcher waits for that owner to finish, then announces the successor's exact model and effort, that its assignment is to resume the named canonical Build command from durable repository state through the next checkpoint or final verification, and that only the owner marker and canonical command are passed with no conversation or raw-log summary. Then dispatch a new sibling owner with the same model, effort and marker; never build a nested successor chain. The successor rehydrates from the Brief, execution artifact, Git state and relevant code/tests under the selected runtime. If exact owner dispatch is unavailable, report that once, compact to durable current facts and continue in the invoking capable context; never claim that rotation occurred.

Sol owns high-tier decisions by default. Astra is never the Build owner in this mapping. When one exact unresolved high-tier decision would materially benefit from stronger independent reasoning, the Sol owner may dispatch one fresh read-only `gpt-6-astra` advisor with `low` reasoning and `fork_turns="none"`. Send only the decision, relevant accepted intent, conflicting evidence and required answer shape. The advisor does not edit, commit, inherit the Build conversation or take over execution; Sol adjudicates its evidence and records any material decision through the normal lifecycle contract.

## Autonomous Build

Follow [autonomous outcome routing](model-routing.md#autonomous-outcome-routing). Keep the designated Sol owner and reuse the low/standard profiles in the Planned Build table below: explicit `gpt-5.6-luna` with `high` for low outcomes and `xhigh` for standard outcomes. Dispatch one fresh worker with `fork_turns="none"` and only the bounded outcome package; do not load the planned contract or create a task graph for this handoff. Delegate settled low/standard outcomes by default, including repetitive inventories and their focused proof. Keep high-risk work with the Sol owner. If the exact profile or dispatch is unavailable, report it and use the owner fallback defined by autonomous routing.

## Planned Build

The designated Sol Build owner is the orchestrator. It owns planning, difficult decisions, validation and integration; the launcher does not retain orchestration work.

For new standard planned builds, use this dispatch mapping:

| Task capability | Execution model | Reasoning effort |
| --- | --- | --- |
| `low` | `gpt-5.6-luna` | `high` |
| `standard` | `gpt-5.6-luna` | `xhigh` |
| `high` | Build owner (`gpt-5.6-sol`) | `medium` |

Use explicit model and reasoning-effort overrides for low/standard workers; do not rely on inherited defaults. Dispatch one fresh bounded context per task with no inherited orchestrator conversation (`fork_turns="none"` when using Codex spawn_agent). A fully disjoint dependency-ready wave may run in parallel. High tasks and high-risk corrections stay with the Sol owner under standard methodology. Each Luna worker fixes local failures and repeats its focused gate before returning. Local constructor, fixture, assertion, type, formatting and settled API-usage corrections discovered later by Sol validation or final verification return to a fresh Luna worker at their existing low/standard tier with only the failure and relevant current evidence.

Luna `xhigh` may own a larger coherent behavior slice across multiple files, including implementation, wiring and its focused tests, when shared contracts are settled, ownership is bounded, and the result has one meaningful acceptance gate. Follow Task design in `planned-build-contract.md`; do not fragment that slice into per-file or code-versus-test tasks merely to use a cheaper tier. More reasoning does not make unresolved architecture, migration, security/data or concurrency decisions standard work. Return such evidence for a PC escalation to high rather than repeatedly retrying the same inadequate task.

If dispatch or the exact requested worker profile is unavailable, report the unavailable profile and execute the standard-methodology task in the Sol owner context; never silently substitute another worker model/effort or pretend delegation occurred. If the owner cannot safely handle it, preserve the last clean boundary and report the limitation. This fallback never applies to legacy delegated state.

These are defaults for new standard builds. Existing standard plans retain completed definitions/evidence and any explicitly recorded execution commitments; changing pending task granularity or capability requires a PC entry. Never migrate legacy delegated ownership or its fixed profile to the new mapping.

A worker gets one Task Capsule only, using the canonical fields in `planned-build-contract.md`. Add only the applicable accepted clauses, dependency facts and relevant source/tests needed to execute it; never preload the full Brief, plan, history or orchestrator dialogue. It may edit only the approved task surface. Dependency-ready tasks may run as one parallel wave only when write surfaces are fully disjoint. The Build owner validates and checkpoint-commits each task separately before marking it complete.

### Legacy delegated resume

New delegated starts are unavailable. A feature whose durable Build evidence records `planned` / `delegated` resumes through `build`. Keep the invoking high-capability primary context as planner/orchestrator; its fixed legacy executor is Luna with high reasoning effort. Require native subagent dispatch with an explicit model and reasoning-effort override before continuing.

Dispatch every implementation task and correction with model `gpt-5.6-luna` and reasoning effort `high`. Use one fresh bounded subagent per task with no inherited conversation and send only its minimum execution package. The primary context may inspect files, update workflow artifacts, run checks, and commit accepted results, but it never edits production code or tests. If Luna high cannot be requested or a delegated task remains `high` after planning, stop without substituting another model or taking over implementation.

## Review

When fresh agents are available, dispatch exactly one fresh generic read-only reviewer. Its startup package is only the Brief and accepted amendments, final Build Evidence, `base_commit..HEAD` diff, and changed/new tests. Load plan or history lazily only for a concrete coverage, lifecycle, or legacy-ownership question; never preload implementation conversation or conclusions. If unavailable, use the same bounded package inline and label it `advisory (not fully isolated)`.
