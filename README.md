# AbsolutForge

AbsolutForge is an intent-driven delivery workflow for Claude Code, Codex, opencode and Pi. It separates accepted product intent from implementation strategy and gives one independent whole-feature review before local closeout.

**Current release: 0.7.0.** New features have exactly two commands: autonomous `build` and standard `build-planned`. Recorded legacy delegated features resume safely through `build-planned` with their original fixed-executor rules.

## Dual Build

The core workflow is:

```text
                 ┌─ build ─────────────────────┐
discuss -> Ready ┤                             ├-> review -> ship
                 └─ planned strategy ──────────┘
                    └─ build-planned
```

Both strategies consume the same committed Ready Feature Brief. After the developer explicitly accepts the complete proposal, `discuss` commits only the canonical Brief path locally and reports the baseline revision; it never includes unrelated staged or dirty changes.

### `build` — autonomous

Use a high-capability coding model as the direct owner of implementation. It chooses local implementation steps, optionally persists an outcome-oriented `execution-map.md`, verifies coherent outcomes, then performs final whole-feature checks.

Each outcome is `implement -> cover applicable risks -> green fast unit gate -> checkpoint commit`. Test obligations cover the primary behavior plus relevant failure/boundary, state/data, seam-contract, security, persistence, concurrency, migration, or regression risks. Tests must assert repository-owned observable behavior rather than mock setup, framework internals, or incidental implementation details. Broad regression and integration/e2e checks run only at final whole-feature verification. The number of tests follows distinct risks, not the number of outcomes.

### `build-planned` — planner/orchestrator + capability-routed workers

Use this higher-overhead strategy when durable decomposition, bounded delegation, or cross-session resume justifies `implementation-plan.md`. The plan is a bounded dependency graph with change surfaces, invariants, capability tiers, Test Obligations, fast green task gates, and final verification. Broad regression and integration/e2e checks run only at final whole-feature verification. The orchestrator validates every result and the semantic value of its tests, owns plan changes and checkpoint commits, and executes high-risk tasks when appropriate.

The planned path is not a handoff of feature ownership to small models. Workers receive one bounded task and cannot rewrite the plan, Brief, lifecycle, branch history or remote state. Dependency-ready tasks may run in a parallel wave only when their write surfaces are fully disjoint; the orchestrator validates and commits each task separately.

The active orchestrator context is disposable. Where the host supports it, workers use fresh bounded context with no inherited full orchestrator chat. Every completed-task checkpoint leaves the Brief, plan, source, tests and Git history sufficient for a fresh high-capability context to continue without the previous conversation. At a clean task boundary, invoke `build-planned` again with the canonical Brief; use `save/load` mainly for a mid-task or otherwise unresolved stop. Planned per-task evidence lives only in the plan, while the Brief receives one consolidated final Build Evidence entry.

### Legacy delegated resumes

New delegated Build is no longer offered. A feature that already recorded `planned` / `delegated` resumes through `build-planned`, retaining its fixed host executor profile and the rule that only that executor edits source and tests. If the exact legacy profile is unavailable, work stops at the last clean boundary; the orchestrator neither substitutes a worker nor takes over implementation.

## Strategy selection

After `discuss`, explicitly choose one of two first-class strategies. Prefer `build` by default; choose `build-planned` when the feature is large or separable enough to repay planning and delegation overhead. Strategy and planned methodology cannot change after Build start.

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

Pi:

```text
/skill:build absolutforge/features/my-feature/feature-brief.md
/skill:build-planned absolutforge/features/my-feature/feature-brief.md
```

The selected strategy and planned methodology are recorded in Build start evidence. A Building feature resumes through the matching builder, and Review blockers return to that builder. Do not silently switch strategy or methodology mid-feature.

At each Build/Review boundary, AbsolutForge ends with one copy-ready continuation prompt for the active host, using the feature's resolved canonical paths. Build points to Review; Review points back to the recorded builder when blockers remain, or to Ship when the feature is ready. Printing that prompt does not run or authorize the next explicit stage.

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

Pi:

```text
/skill:consult absolutforge/features/my-feature/implementation-plan.md
```

The consulting session appends immutable `C-{NNN}` findings to `absolutforge/features/{slug}/consult-{slug}.md`. The receiving `discuss` or Build context decides whether they still apply and records accepted changes in its own artifact. Build never offers, awaits, or settles consultation; findings are evidence, never authorization.

## Skills

- `discuss` — inspect evidence, create and accept one Feature Brief, then commit its Ready baseline locally.
- `consult` — optional bounded second opinion on a Draft/Ready Brief, or critique of a pending planned implementation plan; writes one `consult-{slug}.md` report and nothing else.
- `build` — autonomous high-capability implementation.
- `build-planned` — high-capability planning/orchestration with bounded, capability-routed worker delegation.
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

Deployment-specific mappings live only in the active host reference. This keeps workflow artifacts portable while allowing each installation to use its available worker profiles. Cross-family Review is preferable when available.

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

Claude Code and Codex install the repository as a local plugin through their normal local-plugin flow. The repository root is the plugin root; installation must ship the shared `skills/`, `references/`, and `runtime/` directories together. Claude installations that must resume a legacy delegated feature also need `agents/delegated-executor.md`; copying only `skills/` cannot preserve that legacy executor contract.

Pi consumes the repository as a Pi Package declared by the root `package.json`:

```bash
pi install /absolute/path/to/absolut-forge
```

Invoke stages as `/skill:{name}`. Pi core has no native subagents, so a clean-context Review uses a fresh session after Build handoff:

```text
/new
/skill:review absolutforge/features/my-feature/feature-brief.md absolutforge/features/my-feature/review.md
```

Use `/reload` after local changes. See [`references/pi-tools.md`](references/pi-tools.md) for planned-worker behavior and Review isolation.

opencode has no plugin format that packages skills, but it reads the same `SKILL.md` tree natively. Register it once in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": { "paths": ["/absolute/path/to/absolut-forge/skills"] }
}
```

opencode also auto-loads `~/.agents/skills/<name>/` and `~/.claude/skills/<name>/`, so symlinking the skill directories there registers the same tree without config.

Keep the repository's `references/` and `runtime/` directories beside the registered `skills/` tree: the skills link to them for the executable workflow contract.

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
