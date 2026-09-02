# Harness Command Contract

AbsolutForge stages are explicit unless `debug` is auto-triggered by a concrete failure.

## Native forms

Claude Code:

```text
/absolutforge:discuss "Feature name" "absolutforge/features/{slug}/feature-brief.md"
/absolutforge:consult <absolutforge/features/{slug}/feature-brief.md OR absolutforge/features/{slug}/implementation-plan.md> [extra-context-path ...]
/absolutforge:build absolutforge/features/{slug}/feature-brief.md
/absolutforge:build-planned absolutforge/features/{slug}/feature-brief.md
/absolutforge:build-planned-tdd absolutforge/features/{slug}/feature-brief.md
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
$absolutforge build-planned-tdd absolutforge/features/{slug}/feature-brief.md
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
/absolutforge-build-planned-tdd absolutforge/features/{slug}/feature-brief.md
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
/skill:build-planned-tdd absolutforge/features/{slug}/feature-brief.md
/skill:review absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/skill:save absolutforge/features/{slug}/feature-brief.md
/skill:load absolutforge/features/{slug}/save-{slug}.md
/skill:ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/skill:tech-debt [repository-relative-path]
```

Pi exposes loaded skills through `/skill:{name}`. Because Pi core has no native subagents, the normal clean Review handoff is `/new` followed by `/skill:review ...`; see [`pi-tools.md`](pi-tools.md).

## Cross-session consultation

`consult` may run outside the owning session so a second opinion can come from a different model family. It writes immutable evidence to `absolutforge/features/{slug}/consult-{slug}.md`; the human may return that report to `discuss` or the selected builder. Consultation never opens, settles, pauses, or resumes workflow state, and Build never offers it automatically.

## Build strategy choice

After explicit acceptance, `discuss` creates and verifies a local path-scoped commit containing only the Ready Brief. The developer then chooses one of two strategies and, for planned Build, one methodology:

- `build`: default; a high-capability model owns implementation directly.
- `build-planned`: use the standard methodology when durable decomposition, meaningful bounded delegation, or cross-session resume justifies a task graph.
- `build-planned-tdd`: experimental TDD methodology within the same `planned` strategy; use when the human explicitly wants auditable RED-GREEN-REFACTOR execution.

Invocation selects the strategy and, for planned Build, its methodology. The selected builder records `Build strategy: autonomous | planned` and `Planned methodology: not applicable | standard | tdd` in Build start evidence. A Building Brief resumes only through the matching skill. Review blockers return to the recorded builder. Do not silently switch strategy or planned methodology mid-feature.

The selected builder creates a local Build-start checkpoint commit before source edits. Autonomous outcomes and planned tasks receive orchestrator-owned checkpoint commits after their fast unit-test gate and targeted test-binding proofs. Broad regression and integration/e2e checks run at final verification before the `In Review` handoff commit.

## Resume invariant

The selected strategy and planned methodology are durable execution state. Any resume, correction after Review, or saved-context handoff returns to the matching builder recorded in Build start evidence.

For planned Build, a clean completed-task checkpoint is also a context-rotation boundary. A fresh session resumes by invoking `build-planned` for `standard` or `build-planned-tdd` for `tdd` with the canonical Brief and rehydrating from the Brief, plan and Git. No `save` artifact is required at that boundary; `save/load` covers mid-task or otherwise unresolved interruption.
