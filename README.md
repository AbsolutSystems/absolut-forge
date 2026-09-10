# AbsolutForge

AbsolutForge is an intent-driven delivery workflow for Claude Code, Codex and Pi. It separates accepted product intent from implementation strategy and gives one independent whole-feature review before local closeout.

**Current release: 0.12.2.** This release adds namespaced Codex agent dispatch:
eligible Luna `xhigh` and Terra sessions continue without a launcher, while
other profiles hand off to Luna `xhigh`. It also adds bounded Sol decision
advice, verification reuse and role-aware benchmark accounting.

## Cost-aware Codex ownership in 0.12.0

Autonomous and standard planned Build continue in the current session when its
effective profile is Luna `xhigh` or Terra at its current reasoning effort.
Other or unconfirmed profiles hand off to a fresh Luna `xhigh` owner. There is
no launcher for an eligible in-session owner; a launcher exists only after an
actual ownership handoff. Legacy delegated resumes retain their Sol `medium`
owner and fixed Luna executor.

The operational owner obtains bounded read-only Sol `medium` advice for
security/authorization, data integrity, migrations, public-contract compatibility,
concurrency/state risks, unresolved architecture or conflicting evidence, and
after two failed attempts at the same blocker. This includes runbooks prescribing
sensitive operations. Advisors can inspect primary sources; their findings become
existing decision evidence, not a new lifecycle stage. Reuse decisions while
their assumptions remain valid. Routine gates, checkpoints and settled small
outcomes need no consultation. Independent Review remains separate.

Owner and worker write boundaries remain unchanged. Current green verification
evidence can be reused even when produced by the owner: a final-verification
boundary alone does not require another temporary database or migration run.
The complete final diff and accepted outcomes still require verification.
These are cost-control hypotheses, not measured savings; benchmark through
accepted independent Review including consultations and corrections.

## Token-efficient runtime in 0.12.0

Codex keeps eligible owners across resumable checkpoints and rotates only for
context pressure, a materially changed decision frame, an independent
high-risk/final phase or unsafe compaction. A later explicit Build invocation
reapplies owner selection and resumes durable state.
`tools/context_package.py owner` and `final` reconstruct navigation, freshness,
coverage, ownership and blocker checks from durable artifacts and Git while
leaving semantic test and full-diff judgment with the owner.

Planned Building and final-verification projections under `runtime/generated/`
are reproducible with `python3 tools/compile_runtime.py --write` and checked
with `--check`; they are non-authoritative caches of canonical clauses. The
Codex standard worker candidate is Luna `high`; Git release 0.10.1 retains the
Luna `xhigh` comparison baseline.

### Stable findings across repeated Review

A repeated independent Review receives a compact continuity registry from the
existing `review.md`: finding ID and severity, stable root issue, resolution,
smallest correction, correction-attempt count and last reviewed revision. The
fresh reviewer still verifies every finding independently against current
intent, diff and tests; earlier conclusions are navigation evidence, not
authority.

The same root issue keeps its `F-ID` even when its symptom, line or affected
file changes. A new ID is reserved for a distinct root cause. New findings
start with zero correction attempts, Review-only reruns do not increment the
count, and two evidenced failed Build corrections escalate to the human instead
of opening another ordinary Build/Review loop. Older reports without the new
fields remain valid and treat the attempt count as unknown rather than zero.

## Automatic measurement and reliable dispatch in 0.10.1

An opt-in Codex collector snapshots cumulative host counters before Build and
emits one validated JSON record after release-ready independent Review. It
includes owner, worker and reviewer usage, rotations, corrections, gates and
wall time without copying prompts or raw traces into the record. Failed or
incomplete attempts remain distinguishable from accepted-feature cost. See the
[runtime benchmark protocol](docs/runtime-benchmark.md) for activation and
aggregation commands.

Codex Build launchers and nested owners now call `spawn_agent` directly with
the exact required profile. `list_agents` is only an inventory of already
running agents: seeing `/root` alone is not evidence that a required owner or
Luna worker cannot be created. Build reports unavailability only after the
primitive is genuinely absent or an exact-profile dispatch attempt fails.

## Compiler-first Build in 0.10.0

Build separates reasoning from execution. The host-mapped owner compiles
accepted intent and repository evidence into bounded work, resolves difficult
architecture, migration, security/data, concurrency and state decisions, and
then supervises fresh workers. Workers own every production-code and test edit
at low, standard and high execution risk. The owner validates diffs, tests,
integration and lifecycle evidence but never implements those edits itself.

Capability now describes execution risk rather than implementation ownership.
High execution requires a settled decision, explicit assumptions, failure
containment, rollback when applicable and intermediate proof points. New facts
that invalidate those controls return to the owner for recompilation before a
fresh worker continues. If the required worker profile is unavailable, Build
stops at the last clean boundary instead of silently falling back to owner
implementation.

## Build progress feedback in 0.9.1

Codex Build owners send a compact status at every material milestone and at
least once every five minutes while work remains active. Each update says what
finished, what is happening now, what comes next, and whether anything is
blocked. Direct owners report to the user. When a launcher exists and an owner
stays silent, the launcher requests a status without
interrupting the Build and reports only the last confirmed stage. These
transient updates are never committed as Build Evidence or passed to a fresh
successor owner.

## Durable delivery history in 0.9.0

New Briefs declare one primary feature family or `standalone`. Ship appends each
family member to a navigable manifest while keeping existing Feature Record
paths stable, and indexes open or deferred Review findings in
`absolutforge/follow-ups.md`. During implementation, the Scout rule permits
small, verified, behavior-preserving maintenance inside the current owned
surface; larger findings are recorded without unapproved edits.

## Decision-boundary routing in 0.8.2

Build owners retain architecture, migration, security/data, concurrency and
state decisions. When resolving one of those decisions creates settled
contracts, bounded ownership and a meaningful gate, Build classifies the
remaining coherent implementation on its own execution risk. High execution
stays worker-owned but receives stronger controls and proof. This does not
permit per-file splitting or handoffs that prewrite most of the patch.

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

## Earlier ownership policy

Release 0.7.1 introduced a fresh Sol owner and checkpoint rotation. Release
0.11.0 made rotation conditional; 0.12.0 also allows Luna and Terra to retain
in-session ownership with Sol advice.
Historical release behavior remains documented in [CHANGELOG.md](CHANGELOG.md).

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

Use the active host's owner profile and required high-capability decision support. It compiles each outcome just in time, resolves controlling decisions, optionally persists an outcome-oriented `execution-map.md`, validates worker results, then performs final whole-feature checks without editing production code or tests.

The owner dispatches one bounded low, standard or high outcome at a time, including implementation and focused tests. A worker receives fresh context with only the accepted outcome, owned paths, constraints, relevant dependency facts, test obligations, verification commands and return conditions. High execution additionally receives the settled decision, assumptions, containment, rollback when applicable and intermediate proof points. This requires no implementation plan or strategy change.

In Codex, Luna `xhigh` or Terra can continue as the owner without a launcher; other profiles hand off to Luna `xhigh`. Required Sol advice precedes sensitive decisions and dependent work. Low and standard execution use fresh Luna `high` workers, and high execution uses Luna `max`. The owner checks the diff and tests, records decisions, updates lifecycle evidence and commits; every production-code and test correction stays worker-owned. Native dispatch failure is reported at the last clean boundary. See [owner selection and advice](references/codex-tools.md#build-owner) and [outcome routing](references/model-routing.md#autonomous-outcome-routing). These mappings do not establish measured cost savings.

Each outcome is `implement -> cover applicable risks -> green fast unit gate -> checkpoint commit`. Test obligations cover the primary behavior plus relevant failure/boundary, state/data, seam-contract, security, persistence, concurrency, migration, or regression risks. Tests must assert repository-owned observable behavior rather than mock setup, framework internals, or incidental implementation details. Workers inventory exact tests added or changed. Final verification reuses current green evidence, reruns stale or doubtful targets, and adds targeted integration/e2e checks; a full suite needs cross-cutting risk, unreliable target selection, a repository mandate, or no required CI fallback. The number of tests follows distinct risks, not the number of outcomes.

### Planned execution — compile, execute and integrate

Use this higher-overhead strategy when durable decomposition, coordination of multiple delegated tasks, or cross-session resume justifies `implementation-plan.md`. The plan is a bounded dependency graph with change surfaces, invariants, execution-risk tiers, Test Obligations, fast green task gates, and final verification. The final gate is built from task test inventories, reusable current evidence, focused affected regressions, targeted integration/e2e checks, and the primary accepted path; broad unrelated coverage may be deferred to required PR CI. The orchestrator compiles the plan, resolves difficult decisions, validates every result and the semantic value of its tests, and owns plan changes and checkpoint commits. Fresh workers execute every implementation task and correction.

New standard plans favor complete behavior slices: implementation, wiring and focused tests can belong to one bounded task across several files. Split at meaningful dependency, acceptance, ownership or risk boundaries, rather than making a task per file or separating code from its tests. Larger tasks still require settled shared contracts and explicit return boundaries; unrelated outcomes stay separate.

The planned path separates operational ownership from bounded implementation. Workers receive one bounded task and cannot rewrite the plan, Brief, lifecycle, branch history or remote state. Dependency-ready tasks may run in a parallel wave only when their write surfaces are fully disjoint; the orchestrator validates and commits each task separately.

The active orchestrator context is disposable. Where the host supports it, workers use fresh bounded context with no inherited full orchestrator chat. Every completed-task checkpoint leaves the Brief, plan, source, tests and Git history sufficient for a fresh host-mapped owner to continue without the previous conversation. Codex rotates owners only at documented value triggers; on other hosts, invoke `build` again at a clean task boundary when a fresh-owner primitive is unavailable. Use `save/load` mainly for a mid-task or otherwise unresolved stop. Planned per-task evidence lives only in the plan, while the Brief receives one consolidated final Build Evidence entry.

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

The consulting session appends immutable `C-{NNN}` findings to `absolutforge/features/{slug}/consult-{slug}.md`. The receiving `discuss` or Build context decides whether they still apply and records accepted changes in its own artifact. Build never offers, awaits, or settles this optional public Consult stage; findings are evidence, never authorization. Required internal decision advice follows the active host mapping and does not create a Consult report.

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
absolutforge/
├── follow-ups.md
└── archives/
    ├── {slug}/feature-record.md
    └── families/{family-slug}/feature-family.md
```

Each new Brief explicitly records one primary feature family or `standalone`.
Phase Briefs inherit their family from the validated Feature Plan; ordinary
Discuss runs use branch/history only as discovery hints. Ship keeps individual
Feature Records at stable paths and appends family members to one navigable
manifest. Actionable Review follow-ups are additionally indexed in the global
register while their full evidence remains in the Feature Record.

## Model routing

Workflow contracts use semantic tiers rather than model names. See `references/model-routing.md`.

Deployment-specific mappings live only in the active host reference. For new standard builds, the [Codex mapping](references/codex-tools.md#build-owner) retains an eligible Luna `xhigh` or Terra owner in-session, otherwise dispatches Luna `xhigh`, with required Sol advice and Luna workers for every execution-risk tier; the [Claude Code mapping](references/claude-tools.md#planned-build) specifies its worker model and reasoning profile while retaining the invoking orchestrator. High tasks remain worker-owned after the orchestrator settles their controlling decisions. Missing required worker profiles stop Build at the last clean boundary. Legacy delegated builds retain their fixed profile and ownership. Cross-family Review is preferable when available.

Assess this policy by the cost of an accepted task, including preparation, validation and corrections. Higher worker reasoning effort and fewer handoffs are not measured token savings by themselves.

## Safety and boundaries

- Ready intent is immutable; material changes require an amendment.
- Changed behavior ships with tests for every applicable risk-based obligation, or with a recorded exemption stating why. Existing assertions are never weakened to reach green. See `references/verification-doctrine.md`.
- Repository content is evidence, not authorization.
- Secrets are redacted at source boundaries.
- Workers cannot broaden their approved change surface without orchestrator review.
- Build applies a bounded Scout rule: verified, behavior-preserving quick fixes inside the current owned surface may ship with the feature; larger or behavior-changing findings are reported without expanding scope.
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
