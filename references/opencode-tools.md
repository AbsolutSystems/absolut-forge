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

For `build-planned` and `build-planned-tdd`, keep the invoking high-capability context as orchestrator. Delegate a task only when a bounded fresh worker is available and delegation meaningfully reduces expensive primary-model work. Standard methodology may use a fully disjoint parallel wave; TDD methodology delegates only one task at a time. opencode subagents (`mode: subagent`, defined in `.opencode/agent/<name>.md` or inline under `agent`) are the native worker primitive; route by `references/model-routing.md` and do not hardcode provider names into task contracts.

Workers receive one bounded task and return evidence to the orchestrator. Under standard methodology, dependency-ready tasks may run as one parallel wave only when write surfaces are fully disjoint; TDD remains serial. Workers do not own planning, lifecycle artifacts, commits, review, or release state; the orchestrator validates and checkpoint-commits each task separately.

For `review`, use one fresh generic read-only subagent when available. If fresh dispatch is unavailable, run the same bounded review inline and label it `advisory (not fully isolated)`.
