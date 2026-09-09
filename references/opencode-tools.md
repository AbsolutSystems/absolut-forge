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

Follow [autonomous outcome routing](model-routing.md#autonomous-outcome-routing). Keep the invoking context as owner and require a native subagent (`mode: subagent`) with an explicit low/standard/high capability mapping and fresh bounded context. Send only the outcome package, one worker at a time, without a planned artifact or inherited conversation. The owner resolves high-risk decisions; the worker owns every production-code and test edit. If the profile or dispatch is unavailable, report it and stop at the last clean boundary; do not guess a provider equivalent or continue inline.

## Planned Build and Review dispatch

When `build` selects or resumes planned execution, keep the invoking high-capability context as orchestrator. Require a bounded fresh worker with no inherited full orchestrator conversation for every implementation task. A fully disjoint dependency-ready wave may run in parallel. opencode subagents (`mode: subagent`, defined by the host installation or inline under `agent`) are the native worker primitive; route all execution-risk tiers by `references/model-routing.md` and do not hardcode provider names into task contracts.

Workers receive one Task Capsule only: Outcome, Own, Must preserve, Implement, Prove, Verify, Return, and high-risk controls when applicable. Add only applicable accepted clauses, dependency facts, relevant source/tests, and verification commands; never preload the full Brief, plan, history, or orchestrator dialogue. Dependency-ready tasks may run as one parallel wave only when write surfaces are fully disjoint. Workers do not own planning, lifecycle artifacts, commits, review, or release state; the orchestrator validates and checkpoint-commits each task separately. If the required worker cannot be dispatched, stop at the last clean boundary; orchestrator implementation is unavailable.

New delegated starts are unavailable. A feature that already records delegated methodology resumes through `build` only if its installation still defines the recorded fixed subagent model and reasoning profile. Every implementation task and correction uses that exact profile, one fresh bounded subagent per task. The primary context never edits production code or tests. If the profile is unavailable, stop at the last clean boundary without guessing an equivalent, falling back to a generic worker, or taking over implementation.

For `review`, use exactly one fresh read-only subagent only when the installation guarantees a high-capability profile, preferably from a different model family than the implementation worker. Its startup package is only the Brief and accepted amendments, final Build Evidence, `base_commit..HEAD` diff, and changed/new tests. Load plan or history lazily only for a concrete coverage, lifecycle, or legacy-ownership question; never preload implementation conversation or conclusions. If fresh high-capability dispatch is unavailable but the invoking Review context is itself high-capability, run the same bounded package inline and label it `advisory (not fully isolated)`. Otherwise stop before writing Review and request a high-capability Review invocation.
