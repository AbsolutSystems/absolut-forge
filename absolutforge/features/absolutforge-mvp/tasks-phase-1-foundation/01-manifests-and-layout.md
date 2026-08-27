# Phase 1: Create manifests and extensible repository layout

## Status
completed

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation.md`

## Shared Context

Read before starting:
- `absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation/implementation-context.md`
- `docs/product-vision.md`

## Context Contract

### Requires (from previous phases)
- None (first phase).

### Provides (for later phases)
- Codex manifest `.codex-plugin/plugin.json` for plugin `absolutforge` version `0.1.0` with `skills: "./skills/"`.
- Claude manifest `.claude-plugin/plugin.json` for the same plugin identity and version.
- Repo-local marketplace entries resolving plugin source path `.` for both harnesses.
- Root `skills/` and `agents/` reservations without runnable skill or agent definitions.

## Read Scope

- `README.md`
- `CLAUDE.md`
- `docs/product-vision.md`
- `/Users/kamil/Projekty/absolut-ai-skills/.codex-plugin/plugin.json`
- `/Users/kamil/Projekty/absolut-ai-skills/.claude-plugin/plugin.json`
- `/Users/kamil/Projekty/absolut-ai-skills/.agents/plugins/marketplace.json`
- `/Users/kamil/Projekty/absolut-ai-skills/.claude-plugin/marketplace.json`

## Write Scope

- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`
- `skills/README.md`
- `agents/README.md`
- `.gitignore`

## Objective

Create the private-pilot plugin descriptors and reserve the host-agnostic source layout. The descriptors must agree on identity and version, expose only the shared future skills directory, and contain no capability that can inject behavior at session start.

## Tasks

### Task 1: Create Codex plugin and marketplace descriptors
**Status:** completed
**Traces to:** AC-1, AC-2, AC-5, AC-6, AC-9, AC-10, AC-11
**Test-first:** no (JSON configuration scaffolding)
**Produces:** `.codex-plugin/plugin.json` identity `absolutforge@0.1.0` with `skills: "./skills/"`, and `.agents/plugins/marketplace.json` source `.`
**Consumes:** none

**Requirements:**

- Create a strict-semver Codex manifest with `name: "absolutforge"`, `version: "0.1.0"`, `description: "Intent-driven development workflow for strong coding models."`, `author.name: "Absolut Systems"`, and `skills: "./skills/"`.
- Set interface fields exactly to: `displayName: "AbsolutForge"`, `shortDescription: "Intent-driven delivery for strong coding models"`, `longDescription: "Discuss intent, build autonomously, run one independent review, and ship with durable human and AI context."`, `developerName: "Absolut Systems"`, `category: "Coding"`, `capabilities: ["Interactive", "Write"]`, `defaultPrompt: ["Use AbsolutForge to discuss and deliver this change from intent to review."]`, and `brandColor: "#C2410C"`.
- Set `skills` to `./skills/`; omit `hooks`, `mcpServers`, and `apps`.
- Create a repo-local marketplace named `absolutforge` with one `AVAILABLE`/`ON_INSTALL` Coding entry whose local source path is `.`.
- Omit `homepage`, `repository`, `license`, `websiteURL`, `privacyPolicyURL`, `termsOfServiceURL`, icons, screenshots, and product gating for the private pilot.

**Tests:**

- `test_manifest_identity_AC1` with `[AC-1]` evidence will observe `absolutforge` and `0.1.0`.
- `test_shared_skill_tree_AC2` with `[AC-2]` evidence will observe `./skills/`.
- `test_private_metadata_optional_AC5` with `[AC-5]` evidence will observe absence of deferred public fields.
- `test_marketplace_root_AC6` with `[AC-6]` evidence will observe source path `.`.
- `test_no_implicit_capabilities_AC9_AC10_AC11` with `[AC-9] [AC-10] [AC-11]` evidence will observe absence of hooks, MCP, and apps.

### Task 2: Create Claude plugin and marketplace descriptors
**Status:** completed
**Traces to:** AC-1, AC-2, AC-5, AC-6, AC-9, AC-10, AC-11
**Test-first:** no (JSON configuration scaffolding)
**Produces:** `.claude-plugin/plugin.json` identity `absolutforge@0.1.0` and `.claude-plugin/marketplace.json` source `.`
**Consumes:** `.codex-plugin/plugin.json` identity from Task 1

**Requirements:**

- Create the thin Claude manifest with `name: "absolutforge"`, `version: "0.1.0"`, `description: "Intent-driven development workflow for strong coding models."`, and `author.name: "Absolut Systems"`.
- Rely on Claude's conventional root `skills/` discovery; do not add host-specific skill paths or hooks.
- Create a local Claude marketplace named `absolutforge` with one development-category plugin sourced from `.`.
- Omit public URLs and licensing metadata during the private pilot.

**Tests:**

- `test_manifest_identity_AC1` with `[AC-1]` evidence will compare both descriptors.
- `test_shared_skill_tree_AC2` with `[AC-2]` evidence will confirm implicit Claude discovery uses the same root and no host-specific tree exists.
- `test_private_metadata_optional_AC5` with `[AC-5]` evidence and `test_marketplace_root_AC6` with `[AC-6]` evidence cover private metadata and source resolution.
- `test_no_implicit_capabilities_AC9_AC10_AC11` with `[AC-9] [AC-10] [AC-11]` evidence covers absence of injected behavior.

### Task 3: Reserve non-discoverable shared directories
**Status:** completed
**Traces to:** AC-2, AC-7, AC-10
**Test-first:** no (directory documentation and ignore configuration)
**Produces:** `skills/README.md`, `agents/README.md`, and repository ignore policy
**Consumes:** `.codex-plugin/plugin.json` field `skills: "./skills/"` from Task 1

**Requirements:**

- Document the six planned skills and single-source rule in `skills/README.md` without creating any `SKILL.md`.
- Document that `agents/` is optional infrastructure for future isolated roles and contains no registered role in Phase 1.
- Add exact `.gitignore` entries `.DS_Store`, `__pycache__/`, `*.py[cod]`, `.venv/`, and `.superpowers/`.
- State the future-harness extension rule: thin integration plus optional `references/{harness}-tools.md`, zero skill forks.

**Tests:**

- `test_shared_skill_tree_AC2` with `[AC-2]` evidence will reject `claude/skills` and `codex/skills`.
- `test_no_discoverable_stubs_AC7` with `[AC-7]` evidence will find no `SKILL.md` or agent definition.
- `test_no_implicit_capabilities_AC9_AC10_AC11` with `[AC-10]` evidence will find no hooks directory or hook manifest.

## Phase Verification

Run:

- `for f in .codex-plugin/plugin.json .claude-plugin/plugin.json .claude-plugin/marketplace.json .agents/plugins/marketplace.json; do python3 -m json.tool "$f" >/dev/null; done`
- `find skills agents -name 'SKILL.md' -o -name '*.md'`
- `find . -maxdepth 2 -type d -name hooks -o -name '.pi'`

## Completion Criteria

- All three tasks are completed.
- All changes remain inside Write Scope.
- Every JSON descriptor parses.
- No runnable skill, registered agent, hook, Pi, or Grok integration exists.
- Context Contract provides are fulfilled and recorded in `implementation-context.md`.

## Implementation Decisions / Remarks
- Created matching private-pilot Claude and Codex manifests at version `0.1.0`.
- Codex exposes only the shared `./skills/` tree; neither manifest defines hooks, MCP servers, apps, or public metadata.
- Added local marketplace entries resolving the repository root (`.`), plus reservation READMEs and the requested ignore policy.
