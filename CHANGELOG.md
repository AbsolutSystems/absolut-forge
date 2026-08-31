# Changelog

All notable changes to AbsolutForge are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
  amendment. `execution-map.md` is not a valid subject.
- `build-planned` offers plan consultation after marking the plan `Ready`, and
  again once after a replan that materially changes the pending frontier, but
  only when the plan carries material risk: several tasks, planned delegation,
  cross-cutting or shared-contract tasks, or coverage leaning on final
  verification. The offer is a hard stop that prints the exact command for the
  other session and ends the turn with the plan persisted. A new plan
  `## Consultation` section carries one append-only entry per revision, one of
  `not offered`, `offered — awaiting answer`, `offered, declined` or
  `consulted`. A resuming context re-states an offer still `awaiting answer` and
  holds the plan, and never re-asks a settled question. Hosts that cannot prompt
  execute and record that fact instead of blocking.

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
- Replan validation now also checks the test expectations of revised tasks.
- `consult` reads `references/artifact-contracts.md` explicitly instead of
  referring to schemas by name, and fixes its finding ID scheme to `C-{NNN}`
  with class, evidence anchor, impact and proposed change. Acceptance is per ID,
  not per batch, and a finding that cannot be applied without rewriting the
  immutable Ready baseline is reported for a human amendment-or-`Draft` decision
  instead of applied. Additional context paths may follow the subject path.
- Schemas: `Tests` added to the planned task contract and the autonomous
  execution map section; `Tests added/updated` and final-entry `Whole-feature
  path exercised` added to Build evidence; `## Consultation` added to the plan.
- `debug` is bound by the verification doctrine when it fixes inside an active
  feature: pin the defect with a regression test or record the exemption in that
  stage's evidence, and never weaken an existing test to reach green.
  Diagnosis-only runs and read-only `tech-debt` are unaffected.
- `references/harness-command-contract.md` documents the cross-session
  consultation handoff and states the `consult` argument form as
  `<brief OR plan> [extra-context-path ...]` instead of a `|` alternation that
  read like a shell pipe.
- `ship` removes the consultation report with the other transient artifacts and
  consolidates only what changed the delivered feature.
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
