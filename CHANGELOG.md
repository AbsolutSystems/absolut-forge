# Changelog

All notable changes to AbsolutForge are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
