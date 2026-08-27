# ADR-002: Explicit Activation Without SessionStart Hooks

- **Status:** Accepted
- **Date:** 2026-08-27
- **Decision owners:** AbsolutForge maintainers
- **Scope:** AbsolutForge MVP activation and workflow selection

## Context

AbsolutForge is intended to improve delivery quality without changing unrelated
coding conversations or injecting a global pipeline prompt. The overlapping
AbsolutPowers workflow remains separately installable, so an implicit activation
could make workflow selection ambiguous or activate both products together.

## Decision

Do not provide a `SessionStart` hook, global pipeline prompt, MCP server, app, or
other project-opened behavior. `discuss`, `build`, `review`, `ship`, and
`tech-debt` are explicit-only and use the native commands in
[`harness-command-contract.md`](../../references/harness-command-contract.md).
Only `debug` may auto-trigger, and only when the user presents a concrete
failure such as an error, failing test, crash, regression, or other unexpected
behavior. Its trigger description remains narrow enough that a generic coding
request does not start the workflow.

Normal use requires that exactly one overlapping workflow is enabled: users may
install both products, but must disable AbsolutPowers before enabling/using
AbsolutForge (or vice versa). Validation and handoffs do not mutate user
configuration or infer a user's enable/disable choice.

## Alternatives considered

1. **Inject the workflow from a SessionStart hook.** Rejected: it changes every
   session, violates explicit activation, and can conflict with AbsolutPowers.
2. **Auto-trigger every core skill from natural-language intent.** Rejected:
   generic coding requests must remain ordinary sessions until explicitly
   invoked.
3. **Make every skill explicit, including `debug`.** Rejected: concrete active
   failures are the one narrowly defined case where automatic diagnosis is
   useful and safe to recognize.
4. **Automatically toggle whichever plugin was most recently invoked.**
   Rejected: plugin configuration is user-owned and silent mutation would hide
   the isolation boundary.

## Consequences

### Benefits

- Opening a project or starting a session has no AbsolutForge side effect.
- Ordinary coding conversations remain unaffected.
- Workflow selection is visible, deterministic, and compatible with a separate
  AbsolutPowers installation.
- Concrete failures can still reach `debug` without requiring a ritual command.

### Costs and constraints

- Users must intentionally invoke the core workflow commands.
- Harness descriptions and manifests must not add hooks or broad trigger text.
- A human must manage local enable/disable state when switching products.
- Codex fresh-review dispatch may require an available generic-agent primitive;
  any inline fallback must be disclosed as advisory rather than falsely called
  independent.

## Related decisions and requirements

- [AbsolutForge Product Vision](../product-vision.md), especially Activation
  and isolation, MVP skills, and security acceptance criteria.
- [Phase 1 planning](../../absolutforge/features/absolutforge-mvp/planning-phase-1-foundation.md),
  explicit-only activation and absence of hooks.
- [Native handoff contract](../../references/harness-command-contract.md).
- [Codex primitive mapping](../../references/codex-tools.md).
