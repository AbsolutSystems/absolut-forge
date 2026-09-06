# AbsolutForge

AbsolutForge is an intent-driven delivery workflow for Claude Code, Codex and Pi. It separates accepted product intent from implementation strategy and gives one independent whole-feature review before local closeout.

**Current release: 0.8.1.** `discuss` can recover an idea from the active
conversation, accept one bounded Feature Brief, or first plan oversized product
intent as independently discussable phases. One `build` command still selects
autonomous or planned execution only from an accepted Ready Brief and preserves
that strategy on resume.

## Conversation-derived Discuss in 0.8.1

If the idea has already been explored in the active conversation, invoke
`discuss` without arguments. It recovers the latest coherent change intent,
including user corrections, and derives a provisional slug and artifact path.
Assistant suggestions remain proposals unless the user explicitly accepted
them, and all normal questions and acceptance checkpoints still apply.

```text
$absolutforge discuss
```

## Feature-family planning in 0.8.0

When an idea contains several independently valuable, cancellation-safe
outcomes, `discuss` recommends a non-buildable Feature Plan instead of forcing
the entire idea into one speculative Ready Brief. After explicit acceptance,
the plan commits stable Phase Seeds with behavior custody, dependencies, shared
invariants, uncertainties, and coherent stop states. Each eligible seed returns
through `discuss` and becomes its own self-contained Ready Brief before Build.

Planning is triggered by product and delivery boundaries, not document length,
file count, or implementation complexity. Accepted reconciliation may adjust
only unexpanded seeds; existing Ready and Shipped phases remain governed by
their own immutable Briefs.

## Targeted final verification in 0.7.2

Build derives its final gate from the complete diff and worker-reported test
inventories. It reuses current green evidence, reruns stale or doubtful targets,
and adds focused regressions plus targeted integration/e2e checks for changed
boundaries. Full local suites are reserved for cross-cutting or unselectable
risk, repository mandates, or the absence of a required CI gate.

## Cost-aware Build ownership in 0.7.1

On Codex, a Build invocation launches one fresh GPT-5.6 Sol owner with medium
reasoning before repository inspection or mutation. The invoking context only
handles compact rotation signals and relays the result. Every clean
implementation/test checkpoint and the boundary before final verification
rotate remaining work to another fresh Sol owner, rehydrated from durable
artifacts and Git rather than accumulated dialogue.

Settled low/standard outcomes and local corrections default to fresh bounded
workers. The owner keeps intent, shared contracts, high-tier decisions,
validation, checkpoints and final integration. Repetitive inventories and
verified classifications become durable evidence instead of being rebuilt in
later turns. Each worker runs and repairs its own focused gate until green;
Sol reruns it only for missing, stale or doubtful evidence. One bounded
read-only Astra advisor may be used for an exact unresolved high-tier decision;
it never owns or inherits the Build.

## Runtime context in 0.7.0

Build and Review load compact runtime instructions and consult canonical
references when a decision needs more detail. A clean planned resume uses the
Active Frontier, current task, relevant dependency facts, accepted intent, and
source/tests. Planned workers receive a bounded Task Capsule containing the outcome,
owned files, invariants, implementation intent, proof obligations, verification
commands, and return boundary.

Older Briefs and task schemas remain supported. Modern `Covers` references can
resolve an accepted outcome by EO identifier or exact legacy heading/text;
unknown or ambiguous references stop capsule generation for inspection.

Review starts from accepted intent, final Build Evidence, the complete
implementation diff, and changed tests. Plans and history are conditional
supporting evidence. Both builders perform affected final verification and
exercise the accepted primary path before Review; required PR CI can own broad
unrelated regression coverage.

The optional [context helper and benchmark](docs/runtime-benchmark.md) provide
read-only artifact projections and reproducible comparisons against a pinned
0.6 baseline. Static sizes and token estimates do not establish measured model
savings; live comparisons remain deferred. See the [changelog](CHANGELOG.md)
for the full release notes.

## One Build, two execution strategies

The ordinary bounded-feature workflow is:

```text
discuss -> Ready -> build -> review -> ship
                     ├─ autonomous
                     └─ planned
```

Both strategies consume the same committed Ready Feature Brief. After the developer explicitly accepts the complete proposal, `discuss` commits only the canonical Brief path locally and reports the baseline revision; it never includes unrelated staged or dirty changes.

For a feature containing several independently valuable delivery outcomes,
`discuss` may recommend a planning-family route before any Ready Brief exists:

```text
discuss -> Planned Feature Plan -> discuss Phase Seed -> Ready Brief -> build
                                      ↑
                         repeat for later eligible phases
```

The developer must explicitly agree to that route and later accept the complete
Feature Plan plus its Phase Seeds. Planning artifacts map coarse end-to-end
behavior, stable phase IDs, behavior custody, dependencies, shared invariants,
uncertainties, and coherent stop states. They are deliberately non-buildable.
Each seed is discussed separately into a self-contained ordinary Feature Brief;
only that committed Ready Brief may enter Build. File count, document length,
generic complexity, or implementation-task decomposition alone do not justify
feature-family planning.

### Autonomous execution

Use a high-capability coding model as the owner of the feature. It chooses local implementation steps, optionally persists an outcome-oriented `execution-map.md`, verifies coherent outcomes, then performs final whole-feature checks.

The owner delegates one bounded low/standard outcome at a time by default, including implementation and focused tests. An inline exception is allowed only when completing the work requires fewer owner interactions than preparing and validating the handoff, and its reason is recorded. A worker receives fresh context with only the accepted outcome, owned paths, constraints, relevant dependency facts, test obligations, verification commands and return conditions. This requires no implementation plan or strategy change.

In Codex, the Build owner is a fresh Sol `medium` agent; local low-tier work uses Luna `high` and standard behavior slices use Luna `xhigh`. Local test-gate corrections retain their low/standard tier and return to a fresh worker, while high-risk decisions remain with the Sol owner. Newly discovered ambiguity or risk returns to the owner, who can clarify the scope or take over. The owner checks the diff and tests and alone updates lifecycle evidence and commits. If the requested worker is unavailable, the owner reports the limitation and continues inline when capable of handling the work. See [outcome routing](references/model-routing.md#autonomous-outcome-routing) and the host mappings for dispatch details. These defaults do not establish measured cost savings.

Each outcome is `implement -> cover applicable risks -> green fast unit gate -> checkpoint commit`. Test obligations cover the primary behavior plus relevant failure/boundary, state/data, seam-contract, security, persistence, concurrency, migration, or regression risks. Tests must assert repository-owned observable behavior rather than mock setup, framework internals, or incidental implementation details. Workers inventory exact tests added or changed. Final verification reuses current green evidence, reruns stale or doubtful targets, and adds targeted integration/e2e checks; a full suite needs cross-cutting risk, unreliable target selection, a repository mandate, or no required CI fallback. The number of tests follows distinct risks, not the number of outcomes.

### Planned execution — orchestrator and capability-routed workers

Use this higher-overhead strategy when durable decomposition, coordination of multiple delegated tasks, or cross-session resume justifies `implementation-plan.md`. The plan is a bounded dependency graph with change surfaces, invariants, capability tiers, Test Obligations, fast green task gates, and final verification. The final gate is built from task test inventories, reusable current evidence, focused affected regressions, targeted integration/e2e checks, and the primary accepted path; broad unrelated coverage may be deferred to required PR CI. The orchestrator validates every result and the semantic value of its tests, owns plan changes and checkpoint commits, and executes high-risk tasks when appropriate.

New standard plans favor complete behavior slices: implementation, wiring and focused tests can belong to one bounded task across several files. Split at meaningful dependency, acceptance, ownership or risk boundaries, rather than making a task per file or separating code from its tests. Larger tasks still require settled shared contracts and explicit return boundaries; unrelated outcomes stay separate.

The planned path is not a handoff of feature ownership to small models. Workers receive one bounded task and cannot rewrite the plan, Brief, lifecycle, branch history or remote state. Dependency-ready tasks may run in a parallel wave only when their write surfaces are fully disjoint; the orchestrator validates and commits each task separately.

The active orchestrator context is disposable. Where the host supports it, workers use fresh bounded context with no inherited full orchestrator chat. Every completed-task checkpoint leaves the Brief, plan, source, tests and Git history sufficient for a fresh high-capability context to continue without the previous conversation. Codex rotates substantial standard Builds between fresh Sol owners automatically; on other hosts, invoke `build` again at a clean task boundary when a fresh-owner primitive is unavailable. Use `save/load` mainly for a mid-task or otherwise unresolved stop. Planned per-task evidence lives only in the plan, while the Brief receives one consolidated final Build Evidence entry.

### Legacy delegated resumes

New delegated Build is no longer offered. A feature that already recorded `planned` / `delegated` resumes through `build`, retaining its fixed host executor profile and the rule that only that executor edits source and tests. If the exact legacy profile is unavailable, work stops at the last clean boundary; the orchestrator neither substitutes a worker nor takes over implementation.

## Strategy selection

After `discuss` has accepted a Ready Brief, invoke `build` with that canonical Brief. It defaults to autonomous execution. Planned execution needs a concrete benefit from independent work, dependency coordination, coordinating multiple delegated tasks, or durable progress across sessions; file count or generic complexity alone is insufficient. Delegating one autonomous outcome needs no task graph and does not change strategy. Build announces its choice and reason, records them before implementation, and continues without another confirmation.

Claude Code:

```text
/absolutforge:build absolutforge/features/my-feature/feature-brief.md
```

Codex:

```text
$absolutforge build absolutforge/features/my-feature/feature-brief.md
```

Pi:

```text
/skill:build absolutforge/features/my-feature/feature-brief.md
```

To force a strategy before Build starts, append `--strategy=autonomous` or
`--strategy=planned` on any host. For example:

```text
$absolutforge build absolutforge/features/my-feature/feature-brief.md --strategy=planned
```

At Building, `build` reads the recorded strategy and methodology instead of
selecting again. A conflicting override is refused; changing strategy requires
explicit abandonment and a restart from a clean committed Ready baseline.
Review corrections and Load handoffs also use `build` with the same Brief.
Existing planned artifacts need no migration: replace old `build-planned`
invocations with `build`. Legacy delegated ownership and unsupported legacy
`tdd` eligibility remain unchanged.

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

Pi:

```text
/skill:consult absolutforge/features/my-feature/implementation-plan.md
```

The consulting session appends immutable `C-{NNN}` findings to `absolutforge/features/{slug}/consult-{slug}.md`. The receiving `discuss` or Build context decides whether they still apply and records accepted changes in its own artifact. Build never offers, awaits, or settles consultation; findings are evidence, never authorization.

## Skills

- `discuss` — inspect evidence; accept one bounded Feature Brief, or first accept a non-buildable Feature Plan and later expand one Phase Seed into its own Brief.
- `consult` — optional bounded second opinion on a Draft/Ready Brief, or critique of a pending planned implementation plan; writes one `consult-{slug}.md` report and nothing else.
- `build` — select autonomous or planned execution once, then implement and resume the recorded strategy with verified checkpoints.
- `save` / `load` — durable cross-session context without hidden state.
- `review` — one fresh read-only whole-feature review.
- `ship` — archive durable context and create one local closeout commit.
- `debug` — evidence-first diagnosis and bounded explicit fix.
- `tech-debt` — static read-only debt audit.

## Artifact layout

An accepted large-feature planning family uses:

```text
absolutforge/features/{family-slug}/
├── feature-plan.md
└── phases/
    ├── P01-{phase-slug}.md
    └── P02-{phase-slug}.md
```

Each seed declares a sibling canonical feature directory for the phase Brief.
Once a phase is accepted, it uses the ordinary layout below.

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

Deployment-specific mappings live only in the active host reference. For new standard builds, the [Codex mapping](references/codex-tools.md#build-owner) uses a fresh Sol `medium` owner and specifies Luna worker profiles; the [Claude Code mapping](references/claude-tools.md#planned-build) specifies worker models and reasoning profiles by task capability while retaining its invoking orchestrator. High tasks stay with the owner, while bounded standard tasks may include a complete behavior slice and its tests. Missing worker profiles use an explicitly reported owner fallback only under standard methodology. Legacy delegated builds retain their fixed profile and ownership. Cross-family Review is preferable when available.

Assess this policy by the cost of an accepted task, including preparation, validation and corrections. Higher worker reasoning effort and fewer handoffs are not measured token savings by themselves.

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

Claude Code and Codex install the repository as a local plugin through their normal local-plugin flow. The repository root is the plugin root; installation must ship the shared `skills/`, `references/`, and `runtime/` directories together. Claude installations also ship `agents/planned-worker.md` for standard task dispatch and retain `agents/delegated-executor.md` for legacy delegated resume. These descriptors have distinct ownership rules; copying only `skills/` cannot provide either named worker.

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

opencode is no longer packaged as a supported host by this repository. The
shared `skills/`, `references/`, and `runtime/` trees remain host-agnostic, so
an installation may still consume them through its own configuration. This
repository does not ship opencode command wrappers or installation commands.

## Validation

Run the contract and context regression suite, including fresh-process resume
and capsule checks:

```bash
rtk python3 -m unittest discover -s tests -v
```

Generate the small, medium, and large static benchmark report (requires the
pinned baseline revision in local Git history):

```bash
rtk python3 tools/context_package.py benchmark
```

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
