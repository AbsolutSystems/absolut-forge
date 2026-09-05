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

Explicit-only activation therefore rests on two mechanisms:

- `.opencode/command/absolutforge-{skill}.md` wrappers, which only a human can invoke. These are the authoritative entry points on this host.
- Skill descriptions that gate on explicit invocation, which is the pattern opencode's own guidance recommends for skills that must stay quiet on adjacent topics.

Treat the second as soft. When explicit-only matters, use the command.

`debug` is the single exception, as on every other host: it may auto-trigger for a concrete failure, and auto-triggering authorizes diagnosis rather than a source change.

## Planned Build and Review dispatch

For `build-planned`, keep the invoking high-capability context as orchestrator. Delegate a task only when a bounded fresh worker with no inherited full orchestrator conversation is available and delegation meaningfully reduces expensive primary-model work. A fully disjoint dependency-ready wave may run in parallel. opencode subagents (`mode: subagent`, defined in `.opencode/agent/<name>.md` or inline under `agent`) are the native worker primitive; route by `references/model-routing.md` and do not hardcode provider names into task contracts.

Workers receive one Task Capsule only: Outcome, Own, Must preserve, Implement, Prove, Verify, and Return. Add only applicable accepted clauses, dependency facts, relevant source/tests, and verification commands; never preload the full Brief, plan, history, or orchestrator dialogue. Dependency-ready tasks may run as one parallel wave only when write surfaces are fully disjoint. Workers do not own planning, lifecycle artifacts, commits, review, or release state; the orchestrator validates and checkpoint-commits each task separately. If an ordinary standard worker cannot be dispatched, the orchestrator executes that task itself and does not claim delegation.

New delegated starts are unavailable. A feature that already records delegated methodology resumes through `build-planned` only if its installation still defines the recorded fixed subagent model and reasoning profile. Every implementation task and correction uses that exact profile, one fresh bounded subagent per task. The primary context never edits production code or tests. If the profile is unavailable, stop at the last clean boundary without guessing an equivalent, falling back to a generic worker, or taking over implementation.

For `review`, use exactly one fresh generic read-only subagent when available. Its startup package is only the Brief and accepted amendments, final Build Evidence, `base_commit..HEAD` diff, and changed/new tests. Load plan or history lazily only for a concrete coverage, lifecycle, or legacy-ownership question; never preload implementation conversation or conclusions. If fresh dispatch is unavailable, run the same bounded package inline and label it `advisory (not fully isolated)`.
