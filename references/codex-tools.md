# Codex Primitive Mapping

Use native Codex file and shell primitives for repository inspection, edits and verification. Explicit skill invocation uses `$absolutforge {skill} ...`.

## Planned Build

Keep the configured high-capability primary context as orchestrator. If `multi_agent=true` or an equivalent fresh-worker primitive is available, dispatch one bounded task at a time. Use task capability tiers from `references/model-routing.md`. Typical deployment guidance is Sol for orchestration/high tasks, Terra for standard tasks, and Luna for low tasks, but this mapping is not a workflow contract.

A worker gets the smallest redacted package that can execute its task: task contract, needed Brief/ADR invariants, dependency facts, relevant source/tests and verification commands. It may edit only the approved task surface. The primary context validates the worker diff and verification before marking the task complete.

If worker dispatch is unavailable, the orchestrator executes the task itself; do not pretend delegation occurred.

## Review

When fresh agents are available, dispatch exactly one fresh generic read-only reviewer. Review remains whole-feature and derives `base_commit..HEAD` itself. If unavailable, use the inline advisory fallback and label it explicitly.
