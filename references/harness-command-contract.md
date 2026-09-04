# Harness Command Contract

AbsolutForge stages are explicit unless `debug` is auto-triggered by a concrete failure.

## Native forms

Claude Code:

```text
/absolutforge:discuss "Feature name" "absolutforge/features/{slug}/feature-brief.md"
/absolutforge:consult <absolutforge/features/{slug}/feature-brief.md OR absolutforge/features/{slug}/implementation-plan.md> [extra-context-path ...]
/absolutforge:build absolutforge/features/{slug}/feature-brief.md
/absolutforge:build-planned absolutforge/features/{slug}/feature-brief.md
/absolutforge:build-planned-delegated absolutforge/features/{slug}/feature-brief.md
/absolutforge:review absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/absolutforge:save absolutforge/features/{slug}/feature-brief.md
/absolutforge:load absolutforge/features/{slug}/save-{slug}.md
/absolutforge:ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/absolutforge:tech-debt [repository-relative-path]
```

Codex:

```text
$absolutforge discuss "Feature name" "absolutforge/features/{slug}/feature-brief.md"
$absolutforge consult <absolutforge/features/{slug}/feature-brief.md OR absolutforge/features/{slug}/implementation-plan.md> [extra-context-path ...]
$absolutforge build absolutforge/features/{slug}/feature-brief.md
$absolutforge build-planned absolutforge/features/{slug}/feature-brief.md
$absolutforge build-planned-delegated absolutforge/features/{slug}/feature-brief.md
$absolutforge review absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
$absolutforge save absolutforge/features/{slug}/feature-brief.md
$absolutforge load absolutforge/features/{slug}/save-{slug}.md
$absolutforge ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
$absolutforge tech-debt [repository-relative-path]
```

opencode:

```text
/absolutforge-discuss "Feature name" "absolutforge/features/{slug}/feature-brief.md"
/absolutforge-consult <absolutforge/features/{slug}/feature-brief.md OR absolutforge/features/{slug}/implementation-plan.md> [extra-context-path ...]
/absolutforge-build absolutforge/features/{slug}/feature-brief.md
/absolutforge-build-planned absolutforge/features/{slug}/feature-brief.md
/absolutforge-build-planned-delegated absolutforge/features/{slug}/feature-brief.md
/absolutforge-review absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/absolutforge-save absolutforge/features/{slug}/feature-brief.md
/absolutforge-load absolutforge/features/{slug}/save-{slug}.md
/absolutforge-ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/absolutforge-tech-debt [repository-relative-path]
```

opencode exposes no per-skill implicit-invocation switch, so these command wrappers are the authoritative explicit entry points on that host. See [`opencode-tools.md`](opencode-tools.md).

Pi:

```text
/skill:discuss "Feature name" "absolutforge/features/{slug}/feature-brief.md"
/skill:consult <absolutforge/features/{slug}/feature-brief.md OR absolutforge/features/{slug}/implementation-plan.md> [extra-context-path ...]
/skill:build absolutforge/features/{slug}/feature-brief.md
/skill:build-planned absolutforge/features/{slug}/feature-brief.md
/skill:build-planned-delegated absolutforge/features/{slug}/feature-brief.md
/skill:review absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/skill:save absolutforge/features/{slug}/feature-brief.md
/skill:load absolutforge/features/{slug}/save-{slug}.md
/skill:ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/skill:tech-debt [repository-relative-path]
```

Pi exposes loaded skills through `/skill:{name}`. Because Pi core has no native subagents, the normal clean Review handoff is `/new` followed by `/skill:review ...`; see [`pi-tools.md`](pi-tools.md).

## Copy-ready continuation prompts

Whenever a stage stops at an explicit workflow boundary, its final response must end with a `Next prompt:` label followed immediately by a fenced `text` block containing the exact native invocation for the active host. Resolve every canonical repository-relative artifact path for the current feature. Do not leave `{slug}` or other placeholders, put prose inside the block, merely name the next skill, or show commands for multiple hosts.

Use the native forms above for the one eligible continuation:

- Build -> Review: invoke `review` with the canonical Feature Brief and `review.md` paths.
- Review with blockers -> Build: invoke the builder selected by recorded strategy and planned methodology with the canonical Feature Brief path. The builder derives and reads the sibling `review.md`; do not add it as an unsupported positional argument.
- Review ready for Ship -> Ship: invoke `ship` with the canonical Feature Brief and `review.md` paths.

For Pi's Build -> Review handoff, the single copy-ready block contains two lines: `/new`, then the resolved `/skill:review ...` invocation. Other handoffs contain one invocation line. Reporting a continuation prompt does not invoke or authorize the next stage.

## Cross-session consultation

`consult` may run outside the owning session so a second opinion can come from a different model family. It writes immutable evidence to `absolutforge/features/{slug}/consult-{slug}.md`; the human may return that report to `discuss` or the selected builder. Consultation never opens, settles, pauses, or resumes workflow state, and Build never offers it automatically.

## Build strategy choice

After explicit acceptance, `discuss` creates and verifies a local path-scoped commit containing only the Ready Brief. The developer then chooses one of two strategies and, for planned Build, one methodology:

- `build`: default; a high-capability model owns implementation directly.
- `build-planned`: use the standard methodology when durable decomposition, meaningful bounded delegation, or cross-session resume justifies a task graph.
- `build-planned-delegated`: use when a high-capability planner should resolve design for a fixed lower-cost executor that owns every source and test edit.

Invocation selects the strategy and, for planned Build, its methodology. The selected builder records `Build strategy: autonomous | planned` and `Planned methodology: not applicable | standard | delegated` in Build start evidence. A Building Brief resumes only through the matching skill. Review blockers return to the recorded builder. Do not silently switch strategy or planned methodology mid-feature. Legacy `tdd` state requires a compatible older release or explicit abandonment and restart.

The selected builder creates a local Build-start checkpoint commit before source edits. Autonomous outcomes and planned tasks receive orchestrator-owned checkpoint commits after meaningful behavior tests pass their fast unit-test gate. Broad regression and integration/e2e checks run at final verification before the `In Review` handoff commit.

## Resume invariant

The selected strategy and planned methodology are durable execution state. Any resume, correction after Review, or saved-context handoff returns to the matching builder recorded in Build start evidence.

For planned Build, a clean completed-task checkpoint is also a context-rotation boundary. A fresh session resumes by invoking `build-planned` for `standard` or `build-planned-delegated` for `delegated` with the canonical Brief and rehydrating from the Brief, plan and Git. No `save` artifact is required at that boundary; `save/load` covers mid-task or otherwise unresolved interruption.
