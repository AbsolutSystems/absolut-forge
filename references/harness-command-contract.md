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

Core skills `discuss`, `build`, `review`, and `ship`, optional `consult`, pause
helpers `save` and `load`, plus standalone `tech-debt`, are explicit-only.
`debug` may be auto-triggered only by a
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
/absolutforge:save absolutforge/features/import-preview/feature-brief.md
```

```text
/absolutforge:load absolutforge/features/import-preview/save-import-preview.md
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
$absolutforge save absolutforge/features/import-preview/feature-brief.md
```

```text
$absolutforge load absolutforge/features/import-preview/save-import-preview.md
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
review to create `absolutforge/archives/{slug}/feature-record.md` and, only on
explicit request, a self-contained `executive-summary.html`.

Handoffs must preserve the accepted intent. A `Ready` Feature Brief is
immutable from `Problem and goal` through `Expected outcomes`; a change to
behavior, scope, public contract, security, data, migration, or material cost
must be an explicitly accepted amendment. Do not hand off a hidden or silently
rewritten contract. `consult` is an optional, explicit-only handoff for an
existing `Draft` or `Ready` Brief; it is never required before `build` and
produces no durable consultation artifact.

## Build and review handoff semantics

`build` accepts the complete repository-relative Feature Brief path. It starts
only on a clean, non-detached local feature branch, records its `HEAD` as
`base_commit`, and may resume a `Building` feature from its durable
`execution-map.md` (when present) and append-only `## Build Evidence`; neither
an internal map section nor a local checkpoint is a separate handoff or delivery
unit. After all accepted outcomes and final verification succeed, `build`
commits the feature state locally, changes the Brief to `In Review`, and hands
the complete feature to `review` with the matching repository-relative review
artifact path.

While a Brief is `Building`, `save` accepts its Brief path and writes only the
matching `save-{slug}.md` context artifact. It never commits, stashes, switches
branches, or saves source bytes. The developer must commit the save with WIP
source, or stash both, before changing branches. `load` accepts the canonical
save path, verifies the matching branch and `base_commit`, loads its context,
and hands back to `build`; it never restores source or mutates repository state.

`review` accepts only the repository-relative Feature Brief path and matching
repository-relative review artifact path. It reads `base_commit` from Build
Evidence, then derives the complete feature change as `base_commit..HEAD`.
Staged, unstaged, or untracked source changes are an input blocker; only the
active `review.md` may be uncommitted. It never receives only an internal
section, checkpoint, partial result, or pre-generated diff.

The normal lifecycle is `build -> review -> ship`: after Build verification,
review evaluates the accepted Brief and amendments, linked ADRs/rules, Build
Evidence, and current worktree. Review may hand off to `ship` only when there
are no open `BLOCKING` findings. Concrete accepted `FOLLOW-UP` items remain
visible for ship and do not create a task handoff.

Before its final Ship handoff, Review records the reviewed `HEAD` in `review.md`.
Ship requires that the branch still points to that revision and that only the
active `review.md` is uncommitted. If source changes, commit it and invoke
Review again before Ship. A missing, rejected, or changed Review input returns
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

When Review is `Complete` with no open `BLOCKING` finding and a recorded
reviewed revision, it hands the matching Brief and Review paths to the
explicit-only, local-only Ship stage:

```text
/absolutforge:ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
```

```text
$absolutforge ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
```

Review uses the active configured model. A blocker handoff is
for a focused Build correction and targeted re-review only. It does not
authorize deployment, push, PR creation, merge, or history rewrite.

Ship prepares a local commit only. Neither a Ship handoff nor its closeout
preview pushes, creates a remote PR, merges, deploys, or rewrites history.

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
