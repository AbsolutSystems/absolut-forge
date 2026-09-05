# opencode Primitive Mapping

Use native opencode file/shell primitives for repository inspection, edits and verification.

## Skill registration

opencode reads the shared `skills/` tree directly; no host-specific fork exists. Register it once in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": { "paths": ["/absolute/path/to/absolut-forge/skills"] }
}
```

`skills.paths` is scanned recursively for `**/SKILL.md`. opencode also auto-loads `~/.agents/skills/<name>/SKILL.md` and `~/.claude/skills/<name>/SKILL.md`, so a symlink into either directory registers the same tree without config. Config is read once at startup and is not hot-reloaded.

## Explicit activation

opencode has no per-skill implicit-invocation switch. It exposes every loaded skill to the model and offers no equivalent of Claude Code's `disable-model-invocation` or Codex's `policy.allow_implicit_invocation`.

This repository no longer ships opencode command wrappers. Explicit invocation
must be provided by the host installation; skill descriptions remain the soft
fallback for skills that should stay quiet on adjacent topics.

`debug` is the single exception, as on every other host: it may auto-trigger for a concrete failure, and auto-triggering authorizes diagnosis rather than a source change.

## Autonomous Build dispatch

Follow [autonomous outcome routing](model-routing.md#autonomous-outcome-routing). Keep the invoking context as owner and use a native subagent (`mode: subagent`) only when the installation provides an explicit low/standard capability mapping and fresh bounded context. Send only the outcome package, one worker at a time, without a planned artifact or inherited conversation. High-risk work stays with the owner. If the profile or dispatch is unavailable, report it and continue inline under autonomous routing; do not guess a provider equivalent.

## Planned Build and Review dispatch

When `build` selects or resumes planned execution, keep the invoking high-capability context as orchestrator. Delegate a task only when a bounded fresh worker with no inherited full orchestrator conversation is available and delegation meaningfully reduces expensive primary-model work. A fully disjoint dependency-ready wave may run in parallel. opencode subagents (`mode: subagent`, defined by the host installation or inline under `agent`) are the native worker primitive; route by `references/model-routing.md` and do not hardcode provider names into task contracts.

Workers receive one Task Capsule only: Outcome, Own, Must preserve, Implement, Prove, Verify, and Return. Add only applicable accepted clauses, dependency facts, relevant source/tests, and verification commands; never preload the full Brief, plan, history, or orchestrator dialogue. Dependency-ready tasks may run as one parallel wave only when write surfaces are fully disjoint. Workers do not own planning, lifecycle artifacts, commits, review, or release state; the orchestrator validates and checkpoint-commits each task separately. If an ordinary standard worker cannot be dispatched, the orchestrator executes that task itself and does not claim delegation.

New delegated starts are unavailable. A feature that already records delegated methodology resumes through `build` only if its installation still defines the recorded fixed subagent model and reasoning profile. Every implementation task and correction uses that exact profile, one fresh bounded subagent per task. The primary context never edits production code or tests. If the profile is unavailable, stop at the last clean boundary without guessing an equivalent, falling back to a generic worker, or taking over implementation.

For `review`, use exactly one fresh generic read-only subagent when available. Its startup package is only the Brief and accepted amendments, final Build Evidence, `base_commit..HEAD` diff, and changed/new tests. Load plan or history lazily only for a concrete coverage, lifecycle, or legacy-ownership question; never preload implementation conversation or conclusions. If fresh dispatch is unavailable, run the same bounded package inline and label it `advisory (not fully isolated)`.
