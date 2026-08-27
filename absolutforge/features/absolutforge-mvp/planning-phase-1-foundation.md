# Phase 1: Product foundation (epic: AbsolutForge MVP)

## Parent context

> Start by reading `absolutforge/features/absolutforge-mvp/planning-main.md`.

- Epic planning: `absolutforge/features/absolutforge-mvp/planning-main.md`
- Dependencies: none

Canonical contracts for this phase:

- [`references/artifact-contracts.md`](../../../references/artifact-contracts.md)
- [`references/project-memory.md`](../../../references/project-memory.md)
- [`references/harness-command-contract.md`](../../../references/harness-command-contract.md)
- [`docs/adr/2026-08-27-host-agnostic-skill-tree.md`](../../../docs/adr/2026-08-27-host-agnostic-skill-tree.md)
- [`docs/adr/2026-08-27-explicit-activation-without-hooks.md`](../../../docs/adr/2026-08-27-explicit-activation-without-hooks.md)

## Status
Ready — 2026-08-27

## Phase goal

Establish the standalone AbsolutForge repository, shared contracts, host-agnostic
skill layout, and thin Claude Code plus Codex integrations without activating any
product workflow globally.

## Scope

### In scope

- Repository conventions and public product documentation.
- Shared artifact, status, handoff, ADR, and project-memory contracts with one
  canonical owner for each exact schema.
- Claude Code and Codex manifests/integration references.
- Explicit-only activation rules and absence of a SessionStart hook.
- Deterministic foundation tests and local manifest validation.
- ADRs documenting the cross-harness skill-tree and activation strategy.

### Out of scope

- Implementing the behavior of the six product skills.
- Pi and Grok integrations.
- Migration tooling from AbsolutPowers.

### Deliberately not doing

- A shared runtime dependency on AbsolutPowers.
- A compatibility layer that allows both workflows to remain enabled together.

## Assumptions and decisions

### Assumptions

- Both target harnesses can load the same host-agnostic skill tree through thin
  manifests or integrations.
- The repository root can be the single plugin root, with repo-local marketplace
  entries using `source.path: "."`, as already validated by the current
  AbsolutPowers layout.
- The private pilot does not need public repository URLs, legal URLs, or a final
  license declaration in its manifests.

### Decisions requiring confirmation

- None. Minimum supported harness versions are deliberately deferred until the
  public-release decision; Phase 1 records only the locally validated versions.

## Selected solution

Use the host-agnostic single-tree architecture proven by AbsolutPowers:

- `skills/{name}/SKILL.md` is the future single source of skill behavior for all
  harnesses.
- Harness integrations remain thin: `.claude-plugin/`, `.codex-plugin/`, and
  repo-local marketplace manifests.
- Harness-specific primitive mappings live only in
  `references/{harness}-tools.md`; adding Pi or Grok later requires a thin
  integration plus an optional reference, not skill forks.
- No hooks, MCP servers, apps, vendored workflow tree, or active incomplete skill
  stubs are created in this phase.
- Product behavior remains in `docs/product-vision.md`; exact operational schemas
  are extracted to canonical reference files and linked from the vision.
- The private pilot uses plugin identifier `absolutforge`, version `0.1.0`, and
  author `Absolut Systems`.
- The plugin is validated but not installed or enabled during Phase 1, because
  AbsolutPowers is currently enabled and overlapping workflows must not run
  together.

### Rationale

The single-tree layout minimizes drift and preserves the low-cost path for adding
Pi, Grok, or another harness later. Keeping the repository itself as plugin root
avoids a redundant `plugins/absolutforge/` nesting level for a one-plugin repo.
Separating semantic product vision from exact reusable schemas prevents skills
from copying contracts and diverging.

### Alternatives considered

- **Nested `plugins/absolutforge/` plugin root:** aligns with the default personal
  marketplace scaffolder, but adds needless nesting and splits repository context
  from plugin context.
- **Separate `claude/skills` and `codex/skills` trees:** straightforward initially,
  but guarantees cross-harness drift and makes every future harness a copy.
- **Create Pi/Grok placeholders now:** rejected because empty integrations imply
  support that the MVP does not test.
- **Install the plugin during foundation work:** rejected because concurrent
  activation with AbsolutPowers violates the accepted isolation contract.

## Implementation plan

1. Create the `0.1.0` Codex and Claude manifests plus repo-local marketplace
   entries, pointing both harnesses at the same root `skills/` directory and
   declaring no hooks, MCP servers, or apps.
2. Reserve `skills/` and `agents/` with explanatory README files only; document
   the six planned skills without creating discoverable incomplete `SKILL.md`
   files or registered agents.
3. Extract canonical artifact, project-memory, and native command-handoff formats
   from Product Vision into shared `references/`; add a Codex-only primitive
   mapping reference and replace duplicated exact schemas in Product Vision with
   links while retaining its behavioral invariants.
4. Add ADRs for the host-agnostic skill tree and explicit activation without
   hooks; seed the empty project-memory document and update root development and
   public documentation to link every source of truth.
5. Add deterministic foundation tests covering manifests, version parity,
   marketplace paths, absence of hooks and active skills, symlink integrity, and
   required context links. Validate JSON, run the test suite, run the canonical
   non-mutating `plugin-creator/scripts/validate_plugin.py` validator for the
   Codex manifest when its PyYAML dependency is available, and run strict
   `claude plugin validate` without installing the plugin. If PyYAML is absent,
   record the canonical validator as skipped and rely on the repository's JSON
   schema assertions as the documented non-mutating fallback. The current Codex
   CLI has no separate `plugin validate` command.

## Files to modify or create

### Create

- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`
- `skills/README.md`
- `agents/README.md`
- `references/artifact-contracts.md`
- `references/project-memory.md`
- `references/harness-command-contract.md`
- `references/codex-tools.md`
- `docs/adr/2026-08-27-host-agnostic-skill-tree.md`
- `docs/adr/2026-08-27-explicit-activation-without-hooks.md`
- `absolutforge/project-memory.md`
- `tests/test_foundation.py`
- `.gitignore`

### Modify

- `README.md`
- `CLAUDE.md` (`AGENTS.md` remains its symlink mirror)
- `docs/product-vision.md` — replace duplicated operational templates with links
  to their canonical references while preserving accepted behavioral contracts.
- `absolutforge/features/absolutforge-mvp/planning-main.md` — update the Phase 1
  row from `To plan` to `Planned`, then let implementation own later statuses.
- `absolutforge/features/absolutforge-mvp/planning-phase-1-foundation.md` — set
  the phase to `Ready` after review-plan PASS; later implementation updates it
  according to the epic status contract.

## Edge cases and risks

- **Discoverable incomplete skills:** a stub `SKILL.md` could auto-trigger. Phase
  1 creates README placeholders only and tests that no `SKILL.md` exists.
- **Manifest drift:** Claude and Codex versions or identities could diverge.
  Foundation tests enforce the shared name and version.
- **Unsupported manifest fields:** Codex rejects fields such as hooks. The
  canonical `plugin-creator` validator and explicit negative assertions protect
  the manifest; no nonexistent Codex CLI validation command is assumed. The
  canonical validator is optional when its PyYAML runtime dependency is missing,
  and the skip must be reported rather than hidden.
- **Implicit Claude skill discovery:** Claude uses the conventional root
  `skills/` directory rather than a manifest `skills` field. Tests require the
  root directory, require Codex `skills: "./skills/"`, and reject parallel
  `claude/skills` or `codex/skills` trees.
- **Marketplace path ambiguity:** repo-local source paths must resolve to the
  repository plugin root. Tests require `source.path: "."` and both CLIs validate
  the actual repo layout.
- **Duplicate contract ownership:** Product Vision and operational references may
  drift. Exact templates move to references; Vision retains semantics and links.
- **False compatibility claim:** current local CLI validation does not prove a
  historical minimum version. Documentation records tested versions only.
- **Accidental concurrent activation:** Phase 1 does not install or enable the
  plugin; later testing must disable AbsolutPowers before enabling AbsolutForge.

## Acceptance Criteria

> Generated by qa-enrichment agent. Do not edit manually — re-run enrichment if the plan changes significantly.

### Happy path
- AC-1: Both supported harness manifests identify the product consistently as AbsolutForge version 0.1.0 during non-mutating foundation validation.
- AC-2: Both supported harness descriptors point to the same shared skill source, with no second harness-specific skill tree required by the repository layout.
- AC-3: A developer starting a fresh session can locate the accepted product vision, phase roadmap, artifact contracts, project-memory contract, and native handoff rules from the repository's documented entry points.
- AC-4: A maintainer can validate the local pilot's metadata and repository layout deterministically without installing or enabling the product in an active coding session.

### Edge cases
- AC-5: The local pilot remains valid when public repository URLs, legal metadata, and release-only information are absent; those deferred fields are not treated as required for local validation.
- AC-6: A repository-local marketplace entry resolves to the intended plugin root rather than to a nested or ambiguous source location.
- AC-7: Incomplete or placeholder workflow definitions are not presented to a harness as runnable skills or registered agents during the foundation phase.
- AC-8: If the two supported harness descriptors differ in product identity or version, deterministic validation reports the inconsistency and does not treat the foundation as valid.

### Security
- AC-9: Validating the local pilot does not activate any workflow merely because a new session starts or a project is opened.
- AC-10: The foundation exposes no globally injected session behavior, and ordinary coding conversations remain unaffected until a supported skill is explicitly invoked.
- AC-11: The local pilot does not request hooks, MCP servers, apps, or other additional capabilities beyond what is needed to resolve explicitly invoked skills.
- AC-12: Documentation and validation clearly require AbsolutForge and the overlapping AbsolutPowers workflow to be disabled from concurrent normal use, preventing ambiguous workflow selection.

## Open questions

- None blocking Phase 1. Exact installation, disable/enable, and cache-busting
  commands will be documented from validated local CLI behavior, while actual
  plugin activation remains deferred to product validation.

## Discussion notes

- The classic AbsolutPowers repository remains a separate, stable product.
- The MVP is a private/local pilot; public release metadata and licensing are
  deliberately deferred.
