# ADR-001: One Host-Agnostic Skill Tree

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** AbsolutForge maintainers
- **Scope:** Claude Code and Codex MVP; future harness integrations

## Context

AbsolutForge must expose the same intent-driven workflow to Claude Code and
Codex while remaining a separate product from AbsolutPowers. Maintaining a
copy of each skill per harness would make behavioral fixes and artifact
contracts diverge. The product vision deliberately defers Pi and Grok until the
MVP is validated, but the repository should not make adding them a rewrite.

## Decision

Use one host-agnostic source tree:

```text
skills/{name}/SKILL.md
```

Claude Code and Codex receive thin manifests/integrations that resolve this
same root tree. Harness-specific primitive differences belong only in
`references/{harness}-tools.md`. Exact delivery schemas have one canonical
owner in `references/`; product behavior remains in
[`docs/product-vision.md`](../product-vision.md). There are no parallel
`claude/skills` or `codex/skills` trees.

## Alternatives considered

1. **Separate `claude/skills` and `codex/skills` trees.** Rejected: it starts
   with duplicate behavior and guarantees cross-harness drift.
2. **Nested `plugins/absolutforge/` root.** Rejected: a one-plugin repository
   gains needless nesting and splits repository context from plugin context.
3. **Create Pi and Grok placeholders now.** Rejected: an empty integration
   implies tested support and increases the surface before the MVP is validated.
4. **Share an AbsolutPowers runtime or skill tree.** Rejected: AbsolutForge is
   a separate product with a different workflow and must remain independently
   enabled/disabled.

## Consequences

### Benefits

- A behavior or contract change is made once and is available to every current
  harness.
- Future harness support has a narrow, reviewable integration boundary.
- Canonical references prevent exact schemas from being copied into skills and
  silently diverging.

### Costs and constraints

- Skills must remain host-agnostic and describe harness differences through the
  references rather than embedding CLI-specific assumptions.
- Each harness integration must be validated independently.
- Deferred Pi/Grok support is not implied by the shared tree.

## Future-harness procedure

When a future harness is approved:

1. Add a thin manifest/integration that points to the existing root
   `skills/` tree; do not fork or copy a skill.
2. Add `references/{harness}-tools.md` only if its primitives differ enough to
   require a mapping.
3. Document native explicit command and fresh-review handoff behavior.
4. Validate the new integration and its isolation behavior without changing
   existing skill bodies or enabling it alongside an overlapping workflow.

## Related decisions and requirements

- [AbsolutForge Product Vision](../product-vision.md), especially Product
  boundary, MVP harnesses, and validation strategy.
- [Phase 1 planning](../../absolutforge/features/absolutforge-mvp/planning-phase-1-foundation.md),
  selected single-tree solution and alternatives.
- [Artifact contracts](../../references/artifact-contracts.md).
- [Codex primitive mapping](../../references/codex-tools.md).
