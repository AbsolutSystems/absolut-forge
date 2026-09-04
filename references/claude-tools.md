# Claude Code Primitive Mapping

Use native Claude Code file/shell primitives for repository inspection, edits and verification.

For `build-planned`, keep the invoking high-capability context as orchestrator. Delegate a task only when the host exposes a fresh bounded worker/subagent mechanism and the delegation meaningfully reduces expensive primary-model work. A fully disjoint dependency-ready wave may run in parallel. Route by `references/model-routing.md`; do not hardcode provider names into task contracts.

Workers receive one bounded task and return evidence to the orchestrator. Dependency-ready tasks may run as one parallel wave only when write surfaces are fully disjoint. Workers do not own planning, lifecycle artifacts, commits, review, or release state; the orchestrator validates and checkpoint-commits each task separately.

For `build-planned-delegated`, keep the invoking high-capability context as planner/orchestrator. Before Build start, require the plugin agent type `absolutforge:delegated-executor` to appear in the native Agent tool's available types. Its descriptor at `agents/delegated-executor.md` sets `model: claude-opus-5`, `effort: low`, and a bounded implementation tool set.

Validate the effective profile, not only the descriptor. Inspect only `CLAUDE_CODE_EFFORT_LEVEL`, `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, and `CLAUDE_CODE_SUBAGENT_MODEL`. `CLAUDE_CODE_EFFORT_LEVEL` must be unset or `low`; the environment variable overrides the descriptor's `effort`. When `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` is unset, the descriptor's model wins and `CLAUDE_CODE_SUBAGENT_MODEL` alone is only a lower-precedence default. When `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` is exactly `1`, require `CLAUDE_CODE_SUBAGENT_MODEL` to be exactly `claude-opus-5`; forcing without that value would replace the descriptor model. Treat any other non-empty force value as unsupported and stop rather than guessing its semantics. Report only the conflicting named variable or pair, without printing unrelated environment data. Do not unset or rewrite the user's environment automatically.

Dispatch every implementation task and correction through the Agent tool with `subagent_type: "absolutforge:delegated-executor"`, one fresh call per task, and pass the minimum execution package in `prompt`. Do not use `general-purpose`, a fork, an inline implementation, or a command-line Claude session as fallback. The primary context may inspect, update workflow artifacts, verify, and commit, but never edits production code or tests. If the named agent is unavailable or its effective model/effort cannot be guaranteed, stop without starting or continuing implementation.

For `review`, use one fresh generic read-only reviewer when available. If fresh dispatch is unavailable, run the same bounded review inline and label it `advisory (not fully isolated)`.
