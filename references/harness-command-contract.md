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

Core skills `discuss`, `build`, `review`, and `ship`, optional `consult`, plus
standalone `tech-debt`, are explicit-only. `debug` may be auto-triggered only by a
concrete failure (error, failing test, crash, regression, or unexpected
behavior); it remains explicitly invocable as well. No generic coding request
may be rewritten as an implicit workflow invocation.

## Complete handoff examples

These are canonical output shapes. A real handoff must include the actual
repository-relative path and all arguments needed by the next stage.

Claude Code:

Generic consultation form (replace `{slug}` with the actual feature slug):

```text
/absolutforge:consult absolutforge/features/{slug}/feature-brief.md
```

```text
/absolutforge:discuss "Add import preview" "absolutforge/features/import-preview/feature-brief.md"
```

```text
/absolutforge:consult absolutforge/features/import-preview/feature-brief.md
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

Generic consultation form (replace `{slug}` with the actual feature slug):

```text
$absolutforge consult absolutforge/features/{slug}/feature-brief.md
```

```text
$absolutforge discuss "Add import preview" "absolutforge/features/import-preview/feature-brief.md"
```

```text
$absolutforge consult absolutforge/features/import-preview/feature-brief.md
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
rewritten contract. `consult` is an optional, explicit-only handoff for an
existing `Draft` or `Ready` Brief; it is never required before `build` and
produces no durable consultation artifact.

When present, the optional `## Build Recommendation` travels with the complete
Brief into `build`. It is advisory execution metadata outside the immutable
intent baseline: `simple/single` recommends Claude `sonnet` or Codex
`gpt-5.6-luna`, while `complex/phased` recommends Claude `opus` or Codex
`gpt-5.6-terra`. Actual model availability and an explicit user choice remain
authoritative. A missing, malformed, unavailable, or overridden recommendation
must not invalidate the Brief; `build` records the fallback or override reason
in append-only `## Build Evidence`. Handoff never performs automatic model
switching or provider configuration and never authorizes partial delivery.

## Build and review handoff semantics

`build` accepts the complete repository-relative Feature Brief path. It may
resume a `Building` feature from its durable `execution-map.md` (when present)
and append-only `## Build Evidence`; neither an internal map section nor a
local checkpoint is a separate handoff or delivery unit. After all accepted
outcomes and final verification succeed, `build` changes the Brief to `In
Review` and hands the complete feature to `review` with the matching
repository-relative review artifact path.

`review` accepts only the repository-relative Feature Brief path and matching
repository-relative review artifact path. It reads `base_commit` from Build
Evidence, then derives the complete feature change from that revision through
the current worktree itself. Its scope includes committed, staged, unstaged, and
feature-owned untracked files. It excludes generated review/process artifacts
and unrelated dirty changes; when unrelated changes cannot be safely separated,
review records an input blocker and preserves the worktree. It never receives
only an internal section, checkpoint, partial result, or pre-generated diff.

The normal lifecycle is `build -> review -> ship`: after Build verification,
review evaluates the accepted Brief and amendments, linked ADRs/rules, Build
Evidence, and current worktree. Review may hand off to `ship` only when there
are no open `BLOCKING` findings. Concrete accepted `FOLLOW-UP` items remain
visible for ship and do not create a task handoff.

Before its final Ship handoff, Review records the canonical sorted reviewed-path
manifest and source fingerprint in `review.md`. The manifest covers the safe
feature scope across committed, staged, unstaged, and feature-owned untracked
files (including relevant deleted paths), while excluding `review.md`,
review/process artifacts, and unrelated dirty files. Ship receives that Review
fingerprint with the matching Brief and Review paths and recomputes it before
rendering or local closeout. A missing, rejected, or stale Review input returns
to Review without mutation.

Render the native forms above exactly for the active harness; for example:

Claude Code:

```text
/absolutforge:build absolutforge/features/{slug}/feature-brief.md
```

```text
/absolutforge:review absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
```

If Review reports a blocker, the bounded return is to Build for the same Brief:

```text
/absolutforge:build absolutforge/features/{slug}/feature-brief.md
```

Codex:

```text
$absolutforge build absolutforge/features/{slug}/feature-brief.md
```

```text
$absolutforge review absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
```

If Review reports a blocker, the bounded return is to Build for the same Brief:

```text
$absolutforge build absolutforge/features/{slug}/feature-brief.md
```

When Review is `Complete` with no open `BLOCKING` finding and its source
fingerprint is current, it hands the matching Brief and Review paths to the
explicit-only, local-only Ship stage:

```text
/absolutforge:ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
```

```text
$absolutforge ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
```

Review uses the active configured model; it does not inherit or automatically
select a model from the Brief's `## Build Recommendation`. A blocker handoff is
for a focused Build correction and targeted re-review only. It does not
authorize deployment, push, PR creation, merge, or history rewrite.

Ship prepares a local commit and PR description as human-facing local outputs
only. Neither a Ship handoff nor its closeout preview pushes, creates a remote
PR, merges, deploys, or rewrites history.

Rendering or presenting a handoff never installs, enables, disables, deploys,
pushes, creates a PR, merges, or rewrites history.

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
