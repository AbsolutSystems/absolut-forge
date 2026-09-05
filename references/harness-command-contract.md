# Harness Command Contract

AbsolutForge stages are explicit unless `debug` is auto-triggered by a concrete failure.

## Native forms

Claude Code:

```text
/absolutforge:discuss "Feature name" "absolutforge/features/{slug}/feature-brief.md"
/absolutforge:consult <absolutforge/features/{slug}/feature-brief.md OR absolutforge/features/{slug}/implementation-plan.md> [extra-context-path ...]
/absolutforge:build absolutforge/features/{slug}/feature-brief.md
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

- Discuss -> Build: invoke `build` with the canonical Feature Brief path after the verified acceptance checkpoint.
- Load -> Build: invoke `build` with the canonical Feature Brief path, preserving recorded strategy and methodology.
- Build -> Review: invoke `review` with the canonical Feature Brief and `review.md` paths.
- Review with blockers -> Build: invoke `build` with the canonical Feature Brief path; it resumes recorded strategy and methodology without selecting again. The builder derives and reads the sibling `review.md`; do not add it as an unsupported positional argument.
- Review ready for Ship -> Ship: invoke `ship` with the canonical Feature Brief and `review.md` paths.

For Pi's Build -> Review handoff, the single copy-ready block contains two lines: `/new`, then the resolved `/skill:review ...` invocation. Other handoffs contain one invocation line. Reporting a continuation prompt does not invoke or authorize the next stage.

## Cross-session consultation

`consult` may run outside the owning session so a second opinion can come from a different model family. It writes immutable evidence to `absolutforge/features/{slug}/consult-{slug}.md`; the human may return that report to `discuss` or the selected builder. Consultation never opens, settles, pauses, or resumes workflow state, and Build never offers it automatically.

## Build strategy choice

After explicit acceptance, `discuss` creates and verifies a local path-scoped commit containing only the Ready Brief, then offers one `build` continuation. Build selects its internal strategy under [Build strategy selection](artifact-contracts.md#build-strategy-selection); autonomous is the default and planned needs concrete benefits that repay its overhead. The choice and reason are announced and checkpointed before implementation, without another confirmation.

On every host, append at most one `--strategy=autonomous` or `--strategy=planned` after the Brief path to override automatic selection at Ready. For example on Codex:

```text
$absolutforge build absolutforge/features/{slug}/feature-brief.md --strategy=planned
```

Unknown/repeated options are refused before mutation. On resume an override must match the recorded strategy and cannot change methodology. Normal continuations omit the option because durable state already owns that choice. Old `build-planned` prompts must use `build` with the same Brief path; existing planned/standard and planned/delegated artifacts remain valid without rewriting history. Legacy `tdd` still requires a compatible older release or explicit abandonment/restart.

The selected builder creates a local Build-start checkpoint commit before source edits. Autonomous outcomes and planned tasks receive orchestrator-owned checkpoint commits after meaningful behavior tests pass their fast unit-test gate. Broad regression and integration/e2e checks run at final verification before the `In Review` handoff commit.

## Resume invariant

The selected strategy and planned methodology are durable execution state. Any resume, correction after Review, or saved-context handoff returns to `build`, which reads Build start evidence without reselecting; delegated legacy state retains its fixed-executor restrictions.

For planned Build, a clean completed-task checkpoint is also a context-rotation boundary. A fresh session resumes by invoking `build` with the canonical Brief and rehydrating from the Brief status and accepted amendments, plan header plus Active Frontier, current task, and sufficient direct dependency facts from Git. Load plan history only for a concrete correction, ownership, lifecycle, or legacy-ownership question. Standard work routes by capability; delegated legacy work preserves its fixed executor profile and primary-context ownership boundary. No `save` artifact is required at that boundary; `save/load` covers mid-task or otherwise unresolved interruption.
