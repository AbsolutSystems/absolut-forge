# Implementation Context: Phase 1 — Product foundation

## Purpose
Concise durable handoff between Phase 1 workers. Add only facts needed by later phases.

## Completed Phases
- Phase 1: shared plugin manifests, local marketplaces, and non-discoverable `skills/` / `agents/` reservations verified.
- Phase 2: canonical artifact, memory, handoff, and Codex contracts plus two accepted foundation ADRs verified.

## Created / Changed API
- Added private-pilot Claude/Codex manifests for `absolutforge@0.1.0`; Codex exposes `./skills/`.
- Added local Claude and Codex marketplace entries resolving plugin source path `.`.

## Decisions Made
- Repository root is the plugin root; marketplace source path is `.`.
- No plugin installation or activation in Phase 1.

## Test Utilities / Fixtures
- None yet.

## Constraints For Next Phases
- No active `SKILL.md`, hook, MCP, app, Pi, or Grok integration in this phase.
- Shared `skills/` is the single source of truth; future harnesses use thin integrations and optional `references/{harness}-tools.md`.

## Phase 2 Handoff
- Canonical artifact paths, statuses, lifecycle, immutable intent/amendments, and templates: `references/artifact-contracts.md`.
- Memory routing/promotion contract: `references/project-memory.md`; permanent store remains `absolutforge/project-memory.md`.
- Native Claude/Codex handoffs and Codex fresh-agent/inline fallback: `references/harness-command-contract.md`, `references/codex-tools.md`.
- Accepted architecture decisions: `docs/adr/2026-08-27-host-agnostic-skill-tree.md`, `docs/adr/2026-08-27-explicit-activation-without-hooks.md`.

## Verification History
- JSON parse loop and Claude marketplace strict validation passed; Codex validator was unavailable because PyYAML is not installed.

## Phase 3 Handoff
- Fresh-session read order is documented in `CLAUDE.md` (mirrored by `AGENTS.md`): Product Vision, epic main, phase plan, canonical references, then ADRs and active memory.
- `README.md` documents private-pilot, non-mutating validation and requires disabling AbsolutPowers before later AbsolutForge activation.
- `docs/product-vision.md` retains semantic behavior and links exact schemas to canonical references; Phase 1 ADR links are included.
- `absolutforge/project-memory.md` is the empty canonical store; only `active` entries are operational and promotion requires explicit approval.
