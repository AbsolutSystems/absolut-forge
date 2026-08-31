---
name: build
description: "Explicitly implement an accepted Ready Feature Brief autonomously with a high-capability primary coding model, focused verification, optional outcome map, and whole-feature handoff to Review. Use only when the user invokes AbsolutForge build."
disable-model-invocation: true
---

# Build — Autonomous Strategy

`build` is one of two first-class implementation strategies. It preserves the original AbsolutForge model: the active high-capability context owns local planning and implementation for the complete accepted Feature Brief.

Read `../../references/artifact-contracts.md`, `../../references/verification-doctrine.md`, `../../references/harness-command-contract.md`, and host mapping as needed.

## Start or resume

Accept only `absolutforge/features/{slug}/feature-brief.md`.

For `Ready`, require a non-detached feature branch, clean worktree, empty index, and committed Brief. An uncommitted `consult-{slug}.md` is the only permitted exception, per the Build start rule in `../../references/artifact-contracts.md`. Record current HEAD as `base_commit`; append Build start evidence with `Build strategy: autonomous`; change Brief status to `Building` before source edits.

If an `implementation-plan.md` exists for this feature, stop: planned execution state cannot be converted silently to autonomous Build.

For `Building`, require Build start evidence whose strategy is `autonomous`. If the recorded strategy is `planned`, stop and hand off to `build-planned` instead.

## Execute outcomes

Read the accepted Brief, amendments, linked ADRs/rules/memory, and relevant current code/tests. The accepted baseline is immutable. Material changes require an explicit amendment.

Own the local implementation plan. Create `execution-map.md` only for dependent outcomes, meaningful uncertainty, or durable resume need. It is outcome-oriented, not a symbol-by-symbol task recipe.

For each coherent outcome:

```text
implement -> test the changed behavior -> focused verification -> diagnosis -> bounded fix
```

Focused verification means executable evidence, not inspection. Per `verification-doctrine.md`, an outcome that changes observable behavior lands with automated tests written after its implementation, matching the repository's existing test framework and layout, covering the accepted behavior and the realistic failure or boundary the change introduces — not speculative edge cases. Omit tests only under a recorded exemption.

When you keep an `execution-map.md`, record each section's `Tests` expectation or its exemption there, so the autonomous path leaves the same testable trail a planned task does.

Mark outcome complete only after those tests and the focused checks pass. Before a second speculative repair for the same observable failure, verify causal mapping, the violated invariant, and scope boundary. Escalate rather than broadening scope blindly. Never weaken or skip an existing test to reach green.

A strictly trivial adjacent defect inside the touched surface may be fixed and reported; non-trivial adjacent work remains follow-up unless explicitly approved.

## Finish

After all accepted outcomes, run relevant broader checks once and exercise the feature's primary accepted path at integration level as `verification-doctrine.md` requires, inspect the complete `base_commit..HEAD` diff against the Brief, then append final Build Evidence to the evidence schema in `../../references/artifact-contracts.md`, naming `Tests added/updated` with any recorded exemption and `Whole-feature path exercised` with its result or the recorded reason it was not available. Set the Brief to `In Review` and leave all feature source/artifacts committed locally.

Handoff to `review`. Never push, create a PR, merge, deploy, or rewrite history.
