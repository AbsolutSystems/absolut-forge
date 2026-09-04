# AbsolutForge

AbsolutForge is an intent-driven delivery workflow for Claude Code, Codex, opencode and Pi. It separates accepted product intent from implementation strategy and gives one independent whole-feature review before local closeout.

**Current release: 0.6.0.** This release replaces experimental planned TDD with a strong-planner/fixed-executor methodology while retaining the same two first-class Build strategies.

## Dual Build

The core workflow is:

```text
                 ┌─ build ─────────────────────┐
discuss -> Ready ┤                             ├-> review -> ship
                 └─ planned strategy ──────────┘
                    ├─ build-planned
                    └─ build-planned-delegated
```

Both strategies consume the same committed Ready Feature Brief. After the developer explicitly accepts the complete proposal, `discuss` commits only the canonical Brief path locally and reports the baseline revision; it never includes unrelated staged or dirty changes.

### `build` — autonomous

Use a high-capability coding model as the direct owner of implementation. It chooses local implementation steps, optionally persists an outcome-oriented `execution-map.md`, verifies coherent outcomes, then performs final whole-feature checks.

Each outcome is `implement -> cover applicable risks -> green fast unit gate -> checkpoint commit`. Test obligations cover the primary behavior plus relevant failure/boundary, state/data, seam-contract, security, persistence, concurrency, migration, or regression risks. Tests must assert repository-owned observable behavior rather than mock setup, framework internals, or incidental implementation details. Broad regression and integration/e2e checks run only at final whole-feature verification. The number of tests follows distinct risks, not the number of outcomes.

### `build-planned` — planner/orchestrator + workers

Use this higher-overhead strategy when durable decomposition, bounded delegation, or cross-session resume justifies `implementation-plan.md`. The plan is a bounded dependency graph with change surfaces, invariants, capability tiers, Test Obligations, fast green task gates, and final verification. Broad regression and integration/e2e checks run only at final whole-feature verification. The orchestrator validates every result and the semantic value of its tests, owns plan changes and checkpoint commits, and executes high-risk tasks when appropriate.

The planned path is not a handoff of feature ownership to small models. Workers receive one bounded task and cannot rewrite the plan, Brief, lifecycle, branch history or remote state. Dependency-ready tasks may run in a parallel wave only when their write surfaces are fully disjoint; the orchestrator validates and commits each task separately.

The active orchestrator context is disposable. Every completed-task checkpoint leaves the Brief, plan, source, tests and Git history sufficient for a fresh high-capability context to continue without the previous conversation. At a clean task boundary, invoke `build-planned` again with the canonical Brief; use `save/load` mainly for a mid-task or otherwise unresolved stop. Planned per-task evidence lives only in the plan, while the Brief receives one consolidated final Build Evidence entry.

### `build-planned-delegated` — strong planner + fixed executor

This explicit alternative selects the same first-class `planned` strategy but makes methodology durable as `delegated`. A high-capability orchestrator reads the Brief and repository, settles architecture, and writes bounded tasks for an early-mid executor. Each task explains responsibilities, integration approach, relevant symbols, invariants, traps, decision boundaries, Test Obligations, and verification in precise prose without implementation code, pseudocode, or pseudo-diffs.

Every source/test edit and correction is dispatched to one fixed host-mapped executor profile. The orchestrator owns the plan, supervision, verification, plan changes, integration, and checkpoint commits, but never implements or repairs the code itself. Codex passes Luna with high reasoning effort directly when spawning each worker. Claude dispatches the plugin agent `absolutforge:delegated-executor`, whose descriptor sets Opus 5 with low reasoning effort; preflight rejects environment overrides that would change the effective profile. If the exact executor cannot be guaranteed or the work cannot be decomposed safely for it, Build stops instead of silently changing model or methodology.

## Strategy selection

After `discuss`, explicitly choose one of two first-class strategies. Prefer `build` by default; choose planned Build when the feature is large or separable enough to repay planning and delegation overhead. Within planned Build, use `build-planned` for flexible capability routing or `build-planned-delegated` when the strong planner/fixed-executor boundary is desired. Strategy and planned methodology cannot change after Build start.

Claude Code:

```text
/absolutforge:build absolutforge/features/my-feature/feature-brief.md
/absolutforge:build-planned absolutforge/features/my-feature/feature-brief.md
/absolutforge:build-planned-delegated absolutforge/features/my-feature/feature-brief.md
```

Codex:

```text
$absolutforge build absolutforge/features/my-feature/feature-brief.md
$absolutforge build-planned absolutforge/features/my-feature/feature-brief.md
$absolutforge build-planned-delegated absolutforge/features/my-feature/feature-brief.md
```

opencode:

```text
/absolutforge-build absolutforge/features/my-feature/feature-brief.md
/absolutforge-build-planned absolutforge/features/my-feature/feature-brief.md
/absolutforge-build-planned-delegated absolutforge/features/my-feature/feature-brief.md
```

Pi:

```text
/skill:build absolutforge/features/my-feature/feature-brief.md
/skill:build-planned absolutforge/features/my-feature/feature-brief.md
/skill:build-planned-delegated absolutforge/features/my-feature/feature-brief.md
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
- `build-planned` — high-capability planning/orchestration with bounded worker delegation.
- `build-planned-delegated` — high-capability planning with all implementation forced through one fixed host-mapped executor profile.
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

- OpenAI/Codex: Sol high/orchestrator, Terra standard worker, Luna low worker; delegated methodology fixes Luna at high reasoning effort.
- Claude: Opus high/orchestrator/reviewer, Sonnet standard worker; delegated methodology uses the plugin agent `absolutforge:delegated-executor`, fixed to Opus 5 at low reasoning effort.

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

Claude Code and Codex install the repository as a local plugin through their normal local-plugin flow. The repository root is the plugin root. Claude installation must include the plugin's `agents/delegated-executor.md`; copying only `skills/` does not provide the fixed Opus 5 low executor and therefore cannot run `build-planned-delegated`.

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
