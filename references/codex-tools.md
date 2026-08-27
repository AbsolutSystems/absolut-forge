# Codex Primitive Mapping

**Status:** Canonical Codex integration reference — accepted 2026-08-27

AbsolutForge skills use actions such as “read a file”, “run verification”, and
“review in a fresh context”. On Codex, resolve those actions to the primitives
below. This file documents Codex mechanics; workflow behavior and artifact
schemas remain in [`artifact-contracts.md`](artifact-contracts.md) and the
[Product Vision](../docs/product-vision.md).

## Skill invocation

Codex has no separate `Skill` tool for this pilot. An explicitly invoked skill
uses the native command form from [`harness-command-contract.md`](harness-command-contract.md):

```text
$absolutforge {skill} [every path and argument]
```

The command must include a complete feature or artifact path when a stage is
being handed off. Never use the legacy `@skill` form. Core skills are not
implicitly selected from ordinary coding prompts; only `debug` can auto-trigger
for a concrete failure.

## Files, execution, and verification

- Read repository files with the available file-reading primitive.
- Run focused tests, broader tests, and applicable build/type checks with the
  shell execution primitive.
- Keep all artifact paths repository-relative and follow the canonical schemas.
- Do not install or enable the local plugin as part of validation. A JSON/schema
  validator is non-mutating; the current pilot does not require a separate Codex
  `plugin validate` command.

## Fresh-context review

The `review` stage requires one independent review after `build` completes.
AbsolutForge does not define or require a named review agent. When Codex exposes
`multi_agent=true`, dispatch one generic fresh agent with a bounded prompt that
includes the accepted Feature Brief, amendments, linked ADRs/rules, complete
diff, Build Evidence, and verification results. Then wait for that agent's
evidence-based result and persist it as `review.md` using only `BLOCKING` and
`FOLLOW-UP` findings.

The generic agent is a fresh context, not a registered role. Do not attempt to
resolve a Claude-only named agent type or invent a required review-agent
registry. Keep the main context responsible for applying any `BLOCKING` fixes,
re-running verification, and requesting a targeted re-review.

## Inline fallback

If `multi_agent`/fresh-agent dispatch is unavailable, run the same review prompt
sequentially in the current context as an explicit fallback. Mark the result
`advisory (not fully isolated)` because it cannot provide the required fresh
context, and surface that limitation to the human. Do not silently skip the
review or claim isolation that did not occur. A later fresh Codex session may
replace the advisory result before `ship`.

The same fallback applies to any optional independent research: preserve the
scope and evidence boundary, but do not create a mandatory role or gate that
the product contract does not define.

## Local plugin isolation

The repository's local manifests and marketplace entries describe a private
pilot; validation does not mutate Codex configuration. Before normal use,
disable the overlapping AbsolutPowers workflow using the user's existing local
plugin controls before enabling/using AbsolutForge. Do not enable both
workflows concurrently, and do not change user configuration automatically.
Installation, cache, and exact enable/disable commands depend on the local
Codex host and are intentionally not inferred by this reference.

There is no SessionStart hook, MCP server, app, or global prompt in the
AbsolutForge pilot. A project-opened session therefore remains unaffected until
the user explicitly invokes a supported command.
