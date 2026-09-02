# Changelog

All notable changes to AbsolutForge are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.2] - 2026-09-02

### Changed

- After explicit acceptance, `discuss` now sets the Feature Brief to `Ready`
  and creates a verified local commit containing only the canonical Brief path.
- The acceptance checkpoint preserves unrelated staged and dirty work, excludes
  consultation reports and source files, and blocks Build handoff on commit or
  verification failure instead of asking the developer to commit manually.

### Documentation

- Added the Discuss-owned Ready Brief checkpoint ADR and updated the lifecycle,
  artifact, harness, product-vision, and README guidance.
- Package, Codex, and Claude plugin manifests bumped to base release version
  `0.5.2`.

## [0.5.1] - 2026-09-02

### Changed

- All three Build paths now keep intermediate feedback fast by running exact or
  narrowly scoped unit targets plus cheap static checks. Full regression and
  integration/e2e suites run at final whole-feature verification.
- New or materially changed test guards now require targeted mutation proof:
  reversing the protected production behavior must make the narrow test fail
  before the intended implementation is restored and reconfirmed green.
- Standard planned parallel waves defer temporary production mutations to the
  orchestrator's sequential task validation so one proof cannot contaminate
  another worker's test run.
- Build Evidence, implementation plans, Review, and shipped Feature Records now
  preserve test-binding evidence, with compatibility for legacy artifacts.

### Documentation

- Updated the verification doctrine, all Build entrypoints, shared contracts,
  README, product vision, and planned TDD ADR for the fast-feedback and mutation
  policy.
- Package, Codex, and Claude plugin manifests bumped to base release version
  `0.5.1`.

## [0.5.0] - 2026-09-02

### Added

- Added experimental `build-planned-tdd`, a RED-GREEN-REFACTOR methodology
  within the existing first-class planned Build strategy. It keeps the same
  implementation plan, lifecycle, checkpoint, Review, and Ship contracts while
  recording durable TDD cycle evidence and executing tasks serially.
- Added Pi support through a root Pi Package manifest and host mapping. Pi uses
  the shared skill tree, native `/skill:{name}` invocation, and a `/new` Review
  handoff so independent Review starts with clean context despite Pi core not
  shipping a native subagent primitive.

### Changed

- Build artifacts now record `Planned methodology: not applicable | standard |
  tdd`; legacy planned artifacts without the field remain `standard`.
- Resume, Review correction, Save/Load, Debug, and Ship routing preserve the
  selected planned methodology.

### Documentation

- Added the planned TDD contract and ADR, documented native invocation on all
  four supported hosts, and updated the workflow and artifact documentation.
- Codex and Claude plugin manifests bumped to the base release version `0.5.0`.

## [0.4.0] - 2026-09-01

### Changed

- Autonomous `build` is now the recommended default. `build-planned` remains a
  first-class strategy for features where durable decomposition, meaningful
  bounded delegation, or cross-session resume repays its overhead.
- Planned Build has a smaller lifecycle (`Ready -> Executing -> Complete`) and
  one append-only `PC-` plan-change record. The previous `Needs Replan`, `D-`,
  `R-`, and consultation-control states were removed while completed task
  evidence, outcome coverage, dependency validation, write ownership, and
  orchestrator verification remain binding.
- Consultation is evidence rather than workflow state. Build no longer offers,
  awaits, settles, or limits consultations by plan revision. Reports are
  immutable, carry the subject Git/plan revision, and leave accepted-change
  recording to the owning Brief or plan context.
- Verification now uses a positive risk-based Test Charter. Every changed
  behavior considers primary, failure/boundary, state/data, seam-contract, and
  regression obligations, with additional attention to security, persistence,
  compatibility, concurrency, and migrations. Test count follows distinct
  risks rather than task count.
- Both builders now require local orchestrator-owned checkpoint commits for
  Build start, every verified outcome/task, and the final Review handoff.
  Planned Build also commits the validated Ready plan before source edits.
- Planned Build may dispatch one dependency-ready parallel wave when all write
  surfaces are fully disjoint; the orchestrator still validates, stages, and
  checkpoint-commits each task separately.
- Planned Build now treats the active orchestrator context as disposable. Every
  completed-task checkpoint must let a fresh high-capability session resume
  from the Brief, plan and Git without prior conversation. Rotation is
  recommended under context pressure, after large waves or plan changes, and
  before substantial high-capability work or final integration when practical.
- Planned per-task Completion Evidence is stored only in the implementation
  plan; the Brief receives one consolidated final Build Evidence entry. This
  removes duplicate state and keeps rehydration smaller. `save/load` is now
  positioned for mid-task or otherwise unresolved interruption rather than
  routine clean task boundaries.
- Core skill entrypoints were shortened and conditional detail consolidated in
  canonical references to reduce instruction load and drift.

### Removed

- Automatic pre-execution plan-consultation offers and their `awaiting`,
  `settled`, `host cannot prompt`, per-revision refusal, and consultation-driven
  replan rules.
- Finding dispositions from consultation reports; reports are never rewritten.

### Documentation

- Added ADR `2026-09-01-lean-planned-build-and-risk-based-tests.md`, which
  supersedes the plan-consultation state machine and test-framing portions of
  the 2026-08-31 ADR, and records durable fresh-context rotation for long
  planned builds.
- Codex and Claude plugin manifests bumped to the base release version `0.4.0`.

## [0.3.1] - 2026-08-31

### Changed

- All ten AbsolutForge skills are now available in the Codex session context.
  The nine explicit workflow skills no longer set
  `policy.allow_implicit_invocation: false`, which prevented the model from
  resolving a typed invocation and caused it to report that only `debug` was
  available. Their descriptions still require explicit user invocation.
- Removed `disable-model-invocation: true` from the shared skill frontmatter.
  Codex does not support that Claude-specific field and its bundled plugin and
  skill validators reject it. Claude Code now relies on the same
  description-level explicit-invocation guard as other hosts without a hard
  per-skill switch.
- Plugin manifests bumped to `0.3.1`.

## [0.3.0] - 2026-08-31

### Added

- `references/verification-doctrine.md`: canonical meaning of focused and final
  verification for both Build strategies, and for a `debug` fix made inside a
  feature under Build. Automated tests for changed behavior are the default per
  outcome or task, written by default after that stage's implementation and in
  every case before it is marked complete; omission requires a recorded
  exemption with reason. Defines the test value bar, explicitly excludes
  speculative edge cases, coverage targets and test theater, forbids weakening
  existing assertions to reach green, and requires the feature's primary
  accepted path to be exercised at integration level at finish.
- Consultation report artifact `absolutforge/features/{slug}/consult-{slug}.md`,
  with a canonical schema in `references/artifact-contracts.md`. `consult` is
  the one stage meant to run in a separate session and preferably another model
  family: it appends a consultation block with `C-{NNN}` findings at
  `Disposition: open`, and the requesting context reads the report back and
  disposes each finding. Only the consuming context sets any other disposition —
  the Build owner for a plan consultation, or the Brief-mode session acting on
  explicit per-ID human acceptance. The report is transient evidence, removed at
  Ship, and is never an input to `review`.
- `consult` gains a second subject: an `implementation-plan.md` at `Ready`, or
  at `Needs Replan` once the replan entry exists and the revision was
  incremented. Plan mode critiques the pending frontier — coverage,
  decomposition, dependencies, change-surface overlap, capability routing,
  verification and planner/executor-boundary violations — against the accepted
  Brief, and writes nothing but its own report. A finding that would change
  accepted behavior or scope is classified `intent` and routed to a Brief
  amendment. `execution-map.md` is not a valid subject, and neither is a
  revision that was itself produced by consuming a consultation.
- `build-planned` offers plan consultation after marking the plan `Ready`, and
  again once after a replan that materially changes the pending frontier, but
  only when the plan carries material risk: several tasks, planned delegation,
  cross-cutting or shared-contract tasks, or coverage leaning on final
  verification. The offer is a hard stop that prints the exact command for the
  other session and ends the turn with the plan persisted. A new plan
  `## Consultation` section tracks only whether a question is open, in two
  states: `awaiting` holds the plan at its current status, `settled` releases it
  whatever the answer was, and no entry means nothing was ever asked. It carries
  at most one entry per revision and is append-only; the sole permitted rewrite
  is advancing that revision's `awaiting` to `settled`. A resuming context
  re-states an open offer and keeps holding, and never re-asks a settled
  question. A host that cannot prompt records `settled — host cannot prompt` and
  executes, whether it is the offering host or a later one resuming an open
  entry, so an unanswered question cannot deadlock a plan.
- `docs/adr/2026-08-31-verification-doctrine-and-plan-consultation.md` records
  both decisions and the rejected alternatives, including richer consultation
  state and letting `consult` edit a plan.

### Changed

- `build` and `build-planned` now make behavior tests part of stage completion
  instead of leaving "focused verification" open to interpretation. The
  autonomous outcome loop is `implement -> test the changed behavior -> focused
  verification -> diagnosis -> bounded fix`. Planned tasks carry an explicit
  `Tests` expectation, own their test paths in the change surface, and are
  validated by the orchestrator for real assertions rather than worker claims.
  Two tasks may share an existing test file when each adds named distinct cases;
  no two tasks own the same production path or the same new test file.
- `review` judges test value against the doctrine: accepted behavior with no
  test and no recorded exemption is a finding, as is a test whose assertions
  bind nothing the change produces. That is judged by reading the test against
  the diff — never by reverting production code — and the worktree stays clean.
  `review` also checks the final Build Evidence entry for the whole-feature
  integration path: absent, blank, or `not available` without a reason and the
  closest check actually performed is a finding.
- `build-planned` resume is now exhaustive over plan status, closing the gap
  that left a Review blocker with nowhere to go: `Draft` finishes compilation,
  `Ready` executes or revises, `Executing` selects the next task, `Needs Replan`
  replans, and `Complete` reopens through a task or replan entry and returns to
  `Executing`. An existing plan is never recreated; only a `Building` Brief with
  no plan file at all returns to plan compilation.
- Replan validation now also checks the test expectations of revised tasks, and
  every plan revision increment is recorded as an `R-` entry whatever caused it:
  a deviation, or accepted consultation findings named by `C-ID` in its trigger.
  A plan revision can no longer move without a record of what changed. A
  consultation-driven bump is not a replan: the plan keeps the status it had, a
  `Ready` plan never passes through `Needs Replan`, and inapplicable task fields
  of the entry carry `none`.
- A consultation finding classified `intent` is now a hard stop rather than a
  note: `build-planned` settles the consultation entry, appends an intent
  deviation in the pre-execution form and waits for an explicit Brief amendment
  before further execution.
- `build` and `build-planned` name the Build evidence fields they must fill at
  finish — `Tests added/updated` and `Whole-feature path exercised` — instead of
  leaving `review` to police a field neither builder was told to write.
  Autonomous Build records the same `Tests` expectation per execution-map
  section when it keeps a map.
- `consult` reads `references/artifact-contracts.md` explicitly instead of
  referring to schemas by name, and fixes its finding ID scheme to `C-{NNN}`
  with class, evidence anchor, impact and proposed change. Acceptance is per ID,
  not per batch, and a finding that cannot be applied without rewriting the
  immutable Ready baseline is reported for a human amendment-or-`Draft` decision
  instead of applied. Additional context paths may follow the subject path.
- Schemas: `Tests` added to the planned task contract and the autonomous
  execution map section; `Tests added/updated` and `Whole-feature path
  exercised` added to Build evidence, the latter carrying a `(final entry only)`
  marker beside the field rather than inside its own value alternation;
  `## Consultation` added to the plan; the `D-` deviation entry gained a
  pre-execution form — `no task` in the header, a consultation report and its
  `C-IDs` as observable evidence — so an intent finding raised before any task
  ran stays traceable to the amendment it forces.
- `save` records that the plan carries an open `awaiting` consultation entry and
  points at it rather than copying the command it already holds, so a resumed
  session does not lose the question and cannot drift from the plan.
- `docs/product-vision.md` states the shared verification bar and the optional
  second-opinion stage.
- `debug` is bound by the verification doctrine when it fixes inside an active
  feature: pin the defect with a regression test or record the exemption in that
  stage's evidence, and never weaken an existing test to reach green.
  Diagnosis-only runs and read-only `tech-debt` are unaffected.
- `references/harness-command-contract.md` documents the cross-session
  consultation handoff and states the `consult` argument form as
  `<brief OR plan> [extra-context-path ...]` instead of a `|` alternation that
  read like a shell pipe.
- `ship` removes the consultation report with the other transient artifacts and
  consolidates only what changed the delivered feature, against a Feature Record
  contract that now names consultation and verification as recorded fields.
  Consulted with nothing accepted is still recorded; anything not consolidated
  is gone with the report.
- Build start no longer trips over its own second opinion. A Brief-mode
  consultation on a committed Ready Brief left an uncommitted
  `consult-{slug}.md`, which the Build start cleanliness rule read as a dirty
  worktree and refused to start on, with nobody holding authority to commit it.
  The report is now a permitted uncommitted workflow artifact at Build start,
  exactly as `review.md` is at Review, and Build's first artifact commit picks it
  up. Uncommitted source still blocks Build start.
- A plan revision is consultable exactly once, and `consult` now enforces it on
  both paths. The previous guard caught only a revision produced by consuming a
  consultation, so a revision whose findings were all rejected — or that found
  nothing, leaving no `R-` entry and no bump — could be consulted again and then
  had nowhere legal to be recorded. `consult` also refuses a revision whose
  `## Consultation` entry already reads `settled`, unless that settlement is
  `host cannot prompt`, which records that no question ever reached a human.
- A `settled` consultation entry is explicitly final for its revision. A report
  arriving for an already-settled revision is still read and its findings still
  disposed, but it adds no second entry and does not reword the settlement,
  which keeps `## Consultation` append-only instead of leaving the unrequested
  report path with an impossible write.
- The post-replan consultation path states its order and its status handoff: the
  consultation bump leaves the plan at `Needs Replan` like every consultation
  bump, and the replan returns it to `Executing` only after the entry is settled
  and accepted findings are applied. An `intent` finding stops there instead.
- `references/artifact-contracts.md` and `review` agree on the report's standing:
  Review may read it as context on how the implementation arrived, but it never
  enters the judgment. Neither an accepted nor a rejected finding moves a Review
  outcome by itself.
- `skills/README.md` states the shared verification doctrine and the two
  `consult` subjects instead of listing `consult` as an unqualified optional.
- Plugin manifests bumped to `0.3.0`.

## [0.2.0] - 2026-08-30

### Added

- `build-planned` skill: a second first-class implementation strategy. A
  high-capability orchestrator compiles a Ready Feature Brief into a durable
  task graph, delegates bounded tasks by capability tier, validates every worker
  result, replans on evidence, and owns whole-feature integration verification.
- `references/planned-build-contract.md`: canonical `implementation-plan.md`
  schema, plan and task lifecycles, worker dispatch contract, and append-only
  deviation (`D-NNN`) and replan (`R-NNN`) records.
- `references/model-routing.md`: capability-tier routing (`low` / `standard` /
  `high`) for every role. Model names are deployment guidance, not workflow
  semantics.
- `docs/adr/2026-08-30-dual-build-strategies.md`: the accepted decision to keep
  one lifecycle with two explicit implementation strategies.
- opencode support as a third host. opencode has no plugin format that packages
  skills, so it consumes the shared `skills/` tree directly through
  `skills.paths`, through an auto-loaded `~/.agents/skills/` symlink, or through
  `~/.claude/skills/`. No host-specific skill fork was introduced.
- `references/opencode-tools.md`: opencode primitive mapping, skill
  registration, subagent dispatch for planned Build and Review, and the
  explicit-activation caveat below.
- `.opencode/command/absolutforge-*.md`: ten human-invocable command wrappers.
  opencode exposes no per-skill implicit-invocation switch — it has no
  equivalent of Claude Code's `disable-model-invocation` or Codex's
  `policy.allow_implicit_invocation` — so these wrappers are the only hard
  explicit-only mechanism available on that host. Description-level gating
  remains the soft fallback.
- This changelog.

### Changed

- The Build stage now has two peer strategies rather than one. The explicit
  builder invocation selects the strategy, `Build strategy: autonomous | planned`
  is recorded in Build start evidence, and `save`, `load`, and Review blocker
  handoffs all return to the recorded strategy.
- `execution-map.md` (autonomous) and `implementation-plan.md` (planned) are
  mutually exclusive. Each builder refuses to silently convert the other's
  in-progress execution state.
- Documentation consolidated substantially: `README.md`, `docs/product-vision.md`,
  `references/artifact-contracts.md`, `references/harness-command-contract.md`,
  and every `skills/*/SKILL.md` were rewritten to remove duplication. Skills link
  to canonical contracts instead of restating them.
- Plugin manifests bumped to `0.2.0` with dual-build descriptions.
- `agents/README.md`: AbsolutForge requires no named agent registry. Fresh
  reviewers and planned-build workers use native generic subagent primitives.

### Fixed

- `.agents/plugins/marketplace.json` restored to the Codex marketplace schema.
  The flattened form was rejected at load time with
  `invalid marketplace file: missing field 'plugins'`, which made the plugin
  unloadable for every locally configured Codex host.
- `.claude-plugin/marketplace.json` restored its `$schema`, marketplace
  `description`, plugin `category`, and its stable `absolutforge` marketplace
  identity. Renaming the marketplace would have forced existing installations to
  re-add it.
- `skills/*/agents/openai.yaml` restored `policy.allow_implicit_invocation`.
  Codex defaults this to `true`, so dropping it silently injected all ten skills
  into every Codex session context and allowed implicit activation. This
  contradicted the explicit-only activation guarantee. The nine explicit skills
  are `false`; `debug` remains `true` because it is the only skill permitted to
  auto-trigger on a concrete failure.
- `skills/*/agents/openai.yaml` restored `interface.default_prompt`, the only
  place a Codex user sees an example invocation.
- `README.md` validation snippet now actually validates the descriptors. The
  `find`-based form descended into `.git/` and any vendored directory, while the
  `git ls-files ... --others` form it replaced had always matched zero files,
  because `--others` alone lists untracked files only. Both forms were wrong;
  the snippet now passes `--cached --others --exclude-standard` and covers the
  four real descriptors.
- `.gitignore` restored `__pycache__/`, `*.py[cod]`, `.venv/`, and
  `.superpowers/` alongside the newly added editor and log patterns.

### Removed

- Seven superseded ADRs dated 2026-08-27 and 2026-08-28, and five generated
  `docs/onboarding/*.html` decision records. No remaining reference points at
  them.

### Known issues

- The bundled Codex plugin validator
  (`~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py`) rejects
  `disable-model-invocation: true` in skill frontmatter. That field is the only
  mechanism Claude Code offers for explicit-only activation, and the Codex
  runtime does not parse it — the string appears in the Codex binary solely
  inside the embedded copy of that validator script. The field is therefore kept
  for Claude Code, and the validator finding is a known cross-host false
  positive rather than a runtime defect.

## [0.1.0] - 2026-08-28

### Added

- Initial release candidate: the `discuss -> build -> review -> ship` core
  workflow, the optional `consult` second opinion, `save` and `load` for durable
  cross-session Build context, the `debug` guardian, and the read-only
  `tech-debt` audit.
- One host-agnostic `skills/` tree with thin Claude Code and Codex metadata.
