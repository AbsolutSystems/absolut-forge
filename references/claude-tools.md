# Claude Code Primitive Mapping

Use native Claude Code file/shell primitives for repository inspection, edits and verification.

## Autonomous Build

Follow [autonomous outcome routing](model-routing.md#autonomous-outcome-routing). Keep the invoking model and reasoning profile as owner. Reuse the low/standard/high profile in the Planned Build table and the `absolutforge:planned-worker` agent with one fresh call containing only the bounded outcome package. Validate its effective profile under Effective executor profile before dispatch. The agent name does not require a planned artifact: label this an autonomous outcome, without loading the planned contract. The owner resolves high-risk decisions and supplies execution controls; the worker owns every production-code and test edit. If the agent or exact profile is unavailable, report it and stop at the last clean boundary.

## Planned Build

The orchestrator is the model and reasoning profile of the main session that invoked `build`; the skill does not switch it automatically. That session owns planning, difficult decisions, validation and integration, and must be capable of high-tier judgment without editing production code or tests.

For new standard planned builds, use this dispatch mapping:

| Task capability | Execution model | Reasoning effort |
| --- | --- | --- |
| `low` | `claude-opus-5` | `low` |
| `standard` | `claude-opus-5` | `low` |
| `high` | `claude-opus-5` | `low` |

Require the plugin agent type `absolutforge:planned-worker` in the native Agent tool's available types and validate its effective profile below. Its descriptor at [agents/planned-worker.md](../agents/planned-worker.md) sets the explicit model, effort and bounded tool set. Dispatch every low, standard and high task with `subagent_type: "absolutforge:planned-worker"`, one fresh call per task with only the Task Capsule and relevant evidence in `prompt`; no fork or inherited full orchestrator conversation. Do not silently use `general-purpose`, the legacy executor or a command-line Claude session as a substitute.

Workers may own complete behavior slices across multiple files, including implementation, wiring and focused tests, under Task design in `planned-build-contract.md`. Settled shared contracts, bounded ownership, a meaningful gate and a return boundary remain mandatory. High execution also requires the owner-settled decision, assumptions, containment, rollback when applicable and intermediate proof points. Evidence of underestimated complexity returns for a PC escalation or coherent split instead of repeated retries under an inadequate contract.

Workers receive one Task Capsule only: Outcome, Own, Must preserve, Implement, Prove, Verify, and Return. Add only applicable accepted clauses, dependency facts, relevant source/tests, and verification commands; never preload the full Brief, plan, history, or orchestrator dialogue. A fully disjoint dependency-ready wave may run in parallel. Workers do not own planning, lifecycle artifacts, commits, review, or release state; the orchestrator validates and checkpoint-commits each task separately.

If dispatch or the exact requested worker profile is unavailable, report the unavailable profile and stop at the last clean boundary; never silently substitute another worker model/effort, implement in the main session or pretend delegation occurred.

Existing standard plans retain completed definitions and evidence. Pending standard tasks adopt this worker-owned mapping on resume; a historical pending `high` task first receives Risk controls through the canonical PC process. Changing its granularity or capability still requires a PC entry. Never migrate legacy delegated ownership to this worker merely because its model/effort matches.

### Legacy delegated resume

New delegated starts are unavailable. A feature with recorded `planned` / `delegated` state resumes through `build`; keep the invoking high-capability context as its planner/orchestrator. Before continuing implementation, validate the effective profile below and require the plugin agent type `absolutforge:delegated-executor` to appear in the native Agent tool's available types. Its descriptor at `agents/delegated-executor.md` retains the legacy fixed model, effort, and bounded implementation tool set.

Dispatch every implementation task and correction through the Agent tool with `subagent_type: "absolutforge:delegated-executor"`, one fresh call per task, and pass the minimum execution package in `prompt`. Do not use `general-purpose`, a fork, an inline implementation, or a command-line Claude session as fallback. The primary context may inspect, update workflow artifacts, verify, and commit, but never edits production code or tests. If the named agent is unavailable or its effective model/effort cannot be guaranteed, stop without starting or continuing implementation.

## Effective executor profile

Validate the effective profile before dispatching either named executor, not only its descriptor. Inspect only `CLAUDE_CODE_EFFORT_LEVEL`, `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, and `CLAUDE_CODE_SUBAGENT_MODEL`. `CLAUDE_CODE_EFFORT_LEVEL` must be unset or `low`; the environment variable overrides the descriptor's `effort`. When `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` is unset, the descriptor's model wins and `CLAUDE_CODE_SUBAGENT_MODEL` alone is only a lower-precedence default. When `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` is exactly `1`, require `CLAUDE_CODE_SUBAGENT_MODEL` to be exactly `claude-opus-5`; forcing without that value would replace the descriptor model. Treat any other non-empty force value as unsupported rather than guessing its semantics; the requested profile is unavailable. Report only the conflicting named variable or pair, without printing unrelated environment data. Do not unset or rewrite the user's environment automatically.

If the named agent is missing or this profile check fails, both new standard and legacy delegated work stop before implementation. Identical model/effort settings do not make the two agents interchangeable: their methodology and ownership boundaries differ.

## Review

For `review`, use exactly one fresh read-only reviewer only when its effective profile is guaranteed high-capability, preferably from a different model family than the implementation worker. Its startup package is only the Brief and accepted amendments, final Build Evidence, `base_commit..HEAD` diff, and changed/new tests. Load plan or history lazily only for a concrete coverage, lifecycle, or legacy-ownership question; never preload implementation conversation or conclusions. If fresh high-capability dispatch is unavailable but the invoking Review context is itself high-capability, run the same bounded package inline and label it `advisory (not fully isolated)`. Otherwise stop before writing Review and request a high-capability Review invocation.
