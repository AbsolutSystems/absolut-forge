# Native Harness Command and Handoff Contract

**Status:** Canonical contract — accepted 2026-08-27  
**Scope:** Explicit AbsolutForge skill invocation and delivery handoffs.

Every executable handoff that invokes an AbsolutForge skill or passes a path must
be one standalone, copy-pasteable command line in a fenced `text` block. Keep
the skill invocation, every path, and every argument on that line. Quote an
argument containing spaces. Do not use `@` before a skill or path, and do not
emit a prose instruction in place of the command.

## Native skill syntax

Use the active harness's native prefix:

| Harness | Explicit command form |
| --- | --- |
| Claude Code | `/absolutforge:{skill} [path and arguments]` |
| Codex | `$absolutforge {skill} [path and arguments]` |

Core skills `discuss`, `build`, `review`, and `ship`, plus standalone
`tech-debt`, are explicit-only. `debug` may be auto-triggered only by a
concrete failure (error, failing test, crash, regression, or unexpected
behavior); it remains explicitly invocable as well. No generic coding request
may be rewritten as an implicit workflow invocation.

## Complete handoff examples

These are canonical output shapes. A real handoff must include the actual
repository-relative path and all arguments needed by the next stage.

Claude Code:

```text
/absolutforge:discuss "Add import preview" "absolutforge/features/import-preview/feature-brief.md"
```

```text
/absolutforge:build absolutforge/features/import-preview/feature-brief.md
```

```text
/absolutforge:review absolutforge/features/import-preview/feature-brief.md absolutforge/features/import-preview/review.md
```

```text
/absolutforge:ship absolutforge/features/import-preview/feature-brief.md absolutforge/features/import-preview/review.md
```

```text
/absolutforge:debug "tests/test_import.py::test_preview" "absolutforge/features/import-preview/feature-brief.md"
```

```text
/absolutforge:tech-debt src/imports
```

Codex:

```text
$absolutforge discuss "Add import preview" "absolutforge/features/import-preview/feature-brief.md"
```

```text
$absolutforge build absolutforge/features/import-preview/feature-brief.md
```

```text
$absolutforge review absolutforge/features/import-preview/feature-brief.md absolutforge/features/import-preview/review.md
```

```text
$absolutforge ship absolutforge/features/import-preview/feature-brief.md absolutforge/features/import-preview/review.md
```

```text
$absolutforge debug "tests/test_import.py::test_preview" "absolutforge/features/import-preview/feature-brief.md"
```

```text
$absolutforge tech-debt src/imports
```

## Artifact handoff rules

The exact artifact schemas and lifecycle are canonical in
[`artifact-contracts.md`](artifact-contracts.md). In summary, `discuss` hands
an accepted `absolutforge/features/{slug}/feature-brief.md` to `build`; `build`
may create the optional `execution-map.md` and appends Build Evidence; `review`
creates `review.md`; and `ship` consumes the final brief, map when present, and
review to create `absolutforge/archives/{slug}/feature-record.md` and a
self-contained `executive-summary.html`.

Handoffs must preserve the accepted intent. A `Ready` Feature Brief is
immutable from `Problem and goal` through `Expected outcomes`; a change to
behavior, scope, public contract, security, data, migration, or material cost
must be an explicitly accepted amendment. Do not hand off a hidden or silently
rewritten contract.

## Activation and isolation

Command rendering does not install, enable, disable, or otherwise mutate plugin
configuration. Foundation validation is non-mutating. During normal use,
AbsolutForge and the overlapping AbsolutPowers workflow must not be enabled at
the same time: before invoking one, use the harness's existing local plugin
controls to disable the other. Do not infer or automate a user's enable/disable
choice, and do not modify their configuration as part of a handoff.

There is no SessionStart hook or global pipeline prompt. Explicit command
syntax is therefore part of the isolation contract, not merely a presentation
preference.
