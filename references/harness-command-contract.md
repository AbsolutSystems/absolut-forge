# Harness Command Contract

AbsolutForge stages are explicit unless `debug` is auto-triggered by a concrete failure.

## Native forms

Claude Code:

```text
/absolutforge:discuss "Feature name" "absolutforge/features/{slug}/feature-brief.md"
/absolutforge:consult absolutforge/features/{slug}/feature-brief.md
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
$absolutforge consult absolutforge/features/{slug}/feature-brief.md
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
/absolutforge-consult absolutforge/features/{slug}/feature-brief.md
/absolutforge-build absolutforge/features/{slug}/feature-brief.md
/absolutforge-build-planned absolutforge/features/{slug}/feature-brief.md
/absolutforge-review absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/absolutforge-save absolutforge/features/{slug}/feature-brief.md
/absolutforge-load absolutforge/features/{slug}/save-{slug}.md
/absolutforge-ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
/absolutforge-tech-debt [repository-relative-path]
```

opencode exposes no per-skill implicit-invocation switch, so these command wrappers are the authoritative explicit entry points on that host. See [`opencode-tools.md`](opencode-tools.md).

## Build strategy choice

After `discuss` produces a committed Ready Brief, the developer explicitly chooses exactly one strategy:

- `build`: high-capability model owns implementation directly.
- `build-planned`: high-capability orchestrator creates a durable task graph and delegates bounded tasks when useful.

Invocation is the strategy selection. The selected builder records `Build strategy: autonomous | planned` in the Build start evidence. A Building Brief resumes only through that same skill. Review blockers return to the recorded builder. Do not silently switch build strategy mid-feature.

## Resume invariant

The selected strategy is durable execution state. Any resume, correction after Review, or saved-context handoff returns to the same builder that recorded Build start evidence.
