---
name: load
description: "Explicitly restore saved Build context for one paused AbsolutForge feature; use only with its canonical Build Save path."
disable-model-invocation: true
---

# Load

`load` is an explicit-only context restoration command for a paused
`Building` AbsolutForge feature. It accepts only:

```text
absolutforge/features/{slug}/save-{slug}.md
```

Use the native command forms in the
[harness command contract](../../references/harness-command-contract.md). The
[artifact contract](../../references/artifact-contracts.md#build-save-contract)
owns the save schema.

## Validate the saved context

Read the complete save, matching Feature Brief, Build Evidence, optional
Execution Map, and current branch state. Require all of the following:

1. the save path, Brief path, and slug match;
2. the Brief is `Building` and has valid recorded `base_commit` evidence;
3. the current local branch matches the saved feature branch and is not
   detached; and
4. the saved base revision is an ancestor of the current `HEAD`.

If the save is missing, malformed, stale, or belongs to another branch or
feature, stop and report the exact mismatch. Do not write, commit, stash,
switch branches, or repair the save.

## Restore only durable facts

Treat the save as a concise handoff, not as proof that its source diff, tests,
or working tree still exist. Compare its completed work, current work, next
action, and open items with the actual Brief, map, commits, and worktree. State
any drift clearly and preserve current repository state.

When the context is consistent, load it into the active conversation and emit
exactly one native Build handoff with the matching Brief path. `load` does not
implement or verify the feature itself; `build` remains the sole implementation
stage.
