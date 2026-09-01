# Harness Command Contract

AbsolutForge stages are explicit unless `debug` is auto-triggered by a concrete failure.

## Native forms

Claude Code:

```text
/absolutforge:discuss "Feature name" "absolutforge/features/{slug}/feature-brief.md"
/absolutforge:consult <absolutforge/features/{slug}/feature-brief.md OR absolutforge/features/{slug}/implementation-plan.md> [extra-context-path ...]
/absolutforge:build absolutforge/features/{slug}/feature-brief.md
/absolutforge:build-planned absolutforge/features/{slug}/feature-brief.md
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
/absolutforge-review absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/absolutforge-save absolutforge/features/{slug}/feature-brief.md
/absolutforge-load absolutforge/features/{slug}/save-{slug}.md
/absolutforge-ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/absolutforge-tech-debt [repository-relative-path]
```

opencode exposes no per-skill implicit-invocation switch, so these command wrappers are the authoritative explicit entry points on that host. See [`opencode-tools.md`](opencode-tools.md).

## Cross-session consultation

`consult` may run outside the owning session so a second opinion can come from a different model family. It writes immutable evidence to `absolutforge/features/{slug}/consult-{slug}.md`; the human may return that report to `discuss` or the selected builder. Consultation never opens, settles, pauses, or resumes workflow state, and Build never offers it automatically.

## Build strategy choice

After `discuss` produces a committed Ready Brief, the developer explicitly chooses exactly one strategy:

- `build`: default; a high-capability model owns implementation directly.
- `build-planned`: use when durable decomposition, meaningful bounded delegation, or cross-session resume justifies a task graph.

Invocation is the strategy selection. The selected builder records `Build strategy: autonomous | planned` in the Build start evidence. A Building Brief resumes only through that same skill. Review blockers return to the recorded builder. Do not silently switch build strategy mid-feature.

The selected builder creates a local Build-start checkpoint commit before source edits. Autonomous outcomes and planned tasks receive orchestrator-owned checkpoint commits after focused verification. Final Build evidence and the `In Review` transition receive a final local handoff commit.

## Resume invariant

The selected strategy is durable execution state. Any resume, correction after Review, or saved-context handoff returns to the same builder that recorded Build start evidence.

For planned Build, a clean completed-task checkpoint is also a context-rotation boundary. A fresh session resumes by invoking `build-planned` with the canonical Brief and rehydrating from the Brief, plan and Git. No `save` artifact is required at that boundary; `save/load` covers mid-task or otherwise unresolved interruption.
