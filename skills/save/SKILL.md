---
name: save
description: "Explicitly capture durable Build progress before pausing or switching feature branches; use only for a Building AbsolutForge feature."
disable-model-invocation: true
---

# Save

`save` is an explicit-only pause command for one `Building` AbsolutForge
feature. It accepts the repository-relative Feature Brief path and creates or
replaces only the matching save path:

```text
absolutforge/features/{slug}/feature-brief.md -> absolutforge/features/{slug}/save-{slug}.md
```

Use the native command forms in the
[harness command contract](../../references/harness-command-contract.md). The
[artifact contract](../../references/artifact-contracts.md#build-save-contract)
owns the save schema.

## Validate and capture the pause point

Require a normalized repository-relative canonical Brief path, a matching
`Building` Brief, a readable recorded `base_commit`, and a non-detached local
feature branch. Reject a missing or malformed Brief, mismatched slug, invalid
Build start evidence, or an active Review. Preserve all source and unrelated
files on invalid input.

Read the Brief, Build Evidence, optional Execution Map, current branch state,
completed verification, and current diff. Write the canonical Build Save with
only factual, secret-redacted context:

- completed outcomes and their evidence;
- the current outcome, changed areas, and verification state;
- exactly one concrete next action;
- open blockers, assumptions, failures, or `none`; and
- minimal resume notes, including relevant files and commands.

Do not record a guessed plan as completed work. Do not copy credentials, tokens,
private keys, or source excerpts into the save. A save may supersede an earlier
save for the same feature, but it must not overwrite another feature's save.

## Pause safely

`save` captures context only. It never commits, stashes, switches or creates
branches, edits source, changes the Brief status, runs implementation, or
claims verification passed.

Explain that a save alone does not preserve dirty code across a branch switch.
Before switching, the developer must make a local WIP commit containing both the
save and current feature changes, or stash both. Do not perform either action
without an explicit request.

After writing the save, report its path and the current worktree state. Do not
emit a Build handoff: the developer must first preserve the code and later use
`load`.
