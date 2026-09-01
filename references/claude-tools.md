# Claude Code Primitive Mapping

Use native Claude Code file/shell primitives for repository inspection, edits and verification.

For `build-planned`, keep the invoking high-capability context as orchestrator. Delegate a task only when the host exposes a fresh bounded worker/subagent mechanism and the delegation meaningfully reduces expensive primary-model work. Route by `references/model-routing.md`; do not hardcode provider names into task contracts.

Workers receive one bounded task and return evidence to the orchestrator. Dependency-ready tasks may run as one parallel wave only when write surfaces are fully disjoint. Workers do not own planning, lifecycle artifacts, commits, review, or release state; the orchestrator validates and checkpoint-commits each task separately.

For `review`, use one fresh generic read-only reviewer when available. If fresh dispatch is unavailable, run the same bounded review inline and label it `advisory (not fully isolated)`.
