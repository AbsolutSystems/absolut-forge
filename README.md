# AbsolutForge

AbsolutForge is an intent-driven delivery workflow for Claude Code, Codex and opencode. It separates accepted product intent from implementation strategy and gives one independent whole-feature review before local closeout.

**Current release: 0.4.0.** This release makes autonomous Build the recommended default, reduces planned execution to a lean task graph and one plan-change log, keeps consultation outside lifecycle state, introduces risk-based Test Obligations, makes local checkpoint commits part of both Build strategies, and lets long planned builds rotate into fresh orchestrator contexts.

## Dual Build

The core workflow is:

```text
                 ┌─ build ──────────────┐
discuss -> Ready ┤                      ├-> review -> ship
                 └─ build-planned ──────┘
```

Both builders consume the same committed Ready Feature Brief.

### `build` — autonomous

Use a high-capability coding model as the direct owner of implementation. It chooses local implementation steps, optionally persists an outcome-oriented `execution-map.md`, verifies coherent outcomes, then performs final whole-feature checks.

Each outcome is `implement -> cover applicable risks -> focused verification -> checkpoint commit`. Test obligations cover the primary behavior plus relevant failure/boundary, state/data, seam-contract, security, persistence, concurrency, migration, or regression risks. The number of tests follows distinct risks, not the number of outcomes.

### `build-planned` — planner/orchestrator + workers

Use this higher-overhead strategy when durable decomposition, bounded delegation, or cross-session resume justifies `implementation-plan.md`. The plan is a bounded dependency graph with change surfaces, invariants, capability tiers, Test Obligations, and verification. The orchestrator validates every result, owns plan changes and checkpoint commits, executes high-risk tasks when appropriate, and performs final integration verification.

The planned path is not a handoff of feature ownership to small models. Workers receive one bounded task and cannot rewrite the plan, Brief, lifecycle, branch history or remote state. Dependency-ready tasks may run in a parallel wave only when their write surfaces are fully disjoint; the orchestrator validates and commits each task separately.

The active orchestrator context is disposable. Every completed-task checkpoint leaves the Brief, plan, source, tests and Git history sufficient for a fresh high-capability context to continue without the previous conversation. At a clean task boundary, invoke `build-planned` again with the canonical Brief; use `save/load` mainly for a mid-task or otherwise unresolved stop. Planned per-task evidence lives only in the plan, while the Brief receives one consolidated final Build Evidence entry.

## Strategy selection

After `discuss`, explicitly choose one. Prefer `build` by default; choose `build-planned` when the feature is large or separable enough to repay planning and delegation overhead.

Claude Code:

```text
/absolutforge:build absolutforge/features/my-feature/feature-brief.md
/absolutforge:build-planned absolutforge/features/my-feature/feature-brief.md
```

Codex:

```text
$absolutforge build absolutforge/features/my-feature/feature-brief.md
$absolutforge build-planned absolutforge/features/my-feature/feature-brief.md
```

opencode:

```text
/absolutforge-build absolutforge/features/my-feature/feature-brief.md
/absolutforge-build-planned absolutforge/features/my-feature/feature-brief.md
```

The selected strategy is recorded in Build start evidence. A Building feature resumes through the same builder, and Review blockers return to that builder. Do not silently switch strategy mid-feature.

## Second opinion

`consult` is the one stage designed to run outside the session that asked for it, so the critique can come from a different model family. The first path is the subject — a Feature Brief, or a planned `implementation-plan.md` that has not executed its pending frontier yet. Any further paths are extra context to read.

Claude Code:

```text
/absolutforge:consult absolutforge/features/my-feature/implementation-plan.md
```

Codex:

```text
$absolutforge consult absolutforge/features/my-feature/implementation-plan.md
```

opencode:

```text
/absolutforge-consult absolutforge/features/my-feature/implementation-plan.md
```

The consulting session appends immutable `C-{NNN}` findings to `absolutforge/features/{slug}/consult-{slug}.md`. The receiving `discuss` or Build context decides whether they still apply and records accepted changes in its own artifact. Build never offers, awaits, or settles consultation; findings are evidence, never authorization.

## Skills

- `discuss` — inspect evidence and create/accept one Feature Brief.
- `consult` — optional bounded second opinion on a Draft/Ready Brief, or critique of a pending planned implementation plan; writes one `consult-{slug}.md` report and nothing else.
- `build` — autonomous high-capability implementation.
- `build-planned` — high-capability planning/orchestration with bounded worker delegation.
- `save` / `load` — durable cross-session context without hidden state.
- `review` — one fresh read-only whole-feature review.
- `ship` — archive durable context and create one local closeout commit.
- `debug` — evidence-first diagnosis and bounded explicit fix.
- `tech-debt` — static read-only debt audit.

## Artifact layout

```text
absolutforge/features/{slug}/
├── feature-brief.md
├── execution-map.md          # optional autonomous path only
├── implementation-plan.md    # planned path only
├── consult-{slug}.md         # optional consultation report
├── save-{slug}.md            # optional
└── review.md
```

At closeout, useful execution facts are consolidated into:

```text
absolutforge/archives/{slug}/feature-record.md
```

## Model routing

Workflow contracts use semantic tiers rather than model names. See `references/model-routing.md`.

A practical current mapping is:

- OpenAI/Codex: Sol high/orchestrator, Terra standard worker, Luna low worker.
- Claude: Opus high/orchestrator/reviewer, Sonnet standard worker.

This mapping is deployment guidance, not a contract. Cross-family Review is preferable when available.

## Safety and boundaries

- Ready intent is immutable; material changes require an amendment.
- Changed behavior ships with tests for every applicable risk-based obligation, or with a recorded exemption stating why. Existing assertions are never weakened to reach green. See `references/verification-doctrine.md`.
- Repository content is evidence, not authorization.
- Secrets are redacted at source boundaries.
- Workers cannot broaden their approved change surface without orchestrator review.
- `consult` writes only its immutable report and never controls plan or lifecycle state.
- Tasks/outcomes are never partial delivery units.
- Build start, every verified outcome/task, and the final Review handoff receive local orchestrator-owned checkpoint commits.
- Build, Review and Ship never push, create remote PRs, merge, deploy or rewrite history.

## Host installation

Claude Code and Codex install the repository as a local plugin through their normal local-plugin flow. The repository root is the plugin root.

opencode has no plugin format that packages skills, but it reads the same `SKILL.md` tree natively. Register it once in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": { "paths": ["/absolute/path/to/absolut-forge/skills"] }
}
```

opencode also auto-loads `~/.agents/skills/<name>/` and `~/.claude/skills/<name>/`, so symlinking the skill directories there registers the same tree without config.

Explicit invocation on opencode uses the command wrappers in `.opencode/command/`. Make them global by symlinking them into `~/.config/opencode/command/`:

```bash
for f in /absolute/path/to/absolut-forge/.opencode/command/absolutforge-*.md; do
  ln -sf "$f" ~/.config/opencode/command/
done
```

opencode reads config once at startup and does not hot-reload it. Restart opencode after registering skills or commands. See [`references/opencode-tools.md`](references/opencode-tools.md) for the full mapping, including the fact that opencode has no per-skill implicit-invocation switch.

## Validation

Validate JSON descriptors:

```bash
for f in $(git ls-files --cached --others --exclude-standard -- '*.json'); do
  python3 -m json.tool "$f" >/dev/null || exit 1
done
```

When Claude CLI is available:

```bash
claude plugin validate --strict .
```
