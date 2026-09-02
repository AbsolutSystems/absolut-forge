---
name: build
description: "Explicitly implement an accepted Ready Feature Brief autonomously with a high-capability primary coding model, risk-based tests, checkpoint commits, and whole-feature handoff to Review. Use only when the user invokes AbsolutForge build."
---

# Build — Autonomous Strategy

Use autonomous Build as the default strategy when one high-capability context can efficiently own the complete feature.

Read `../../references/artifact-contracts.md` and `../../references/verification-doctrine.md`, plus the active host mapping as needed.

## Start or resume

Accept only `absolutforge/features/{slug}/feature-brief.md`.

For `Ready`, require a non-detached feature branch, clean worktree, empty index, and committed Brief. The uncommitted consultation report allowed by the artifact contract is the only exception. Reject an existing `implementation-plan.md`.

Record HEAD as `base_commit`, append Build start evidence with strategy `autonomous` and planned methodology `not applicable`, set the Brief to `Building`, and create a local Build-start checkpoint commit before any source edit. Include the permitted consultation report when present.

For `Building`, require Build start evidence whose strategy is `autonomous`. A planned strategy hands off by recorded methodology: `build-planned-tdd` for `tdd`, otherwise `build-planned`; never convert execution state.

## Execute outcomes

Read the immutable accepted Brief, amendments, linked project authority, and relevant current code/tests. Material intent changes require an explicit amendment.

Own the local implementation trajectory. Create `execution-map.md` only when dependencies, uncertainty, or cross-session resume justify it; keep it outcome-oriented.

For each coherent outcome:

1. implement the accepted behavior;
2. derive applicable test obligations from `verification-doctrine.md` and add tests for the distinct risks;
3. run focused executable verification;
4. diagnose and make one bounded evidence-backed repair when needed;
5. append intermediate Build Evidence, update the map when present, and create a local checkpoint commit containing the outcome's source, tests, and artifacts.

Do not mark the outcome complete without passing tests or a recorded exemption. Never weaken an existing test to reach green. Before a second speculative repair for the same failure, establish causal mapping and scope or escalate.

A strictly trivial adjacent defect inside the touched surface may be fixed and reported. Non-trivial adjacent work remains follow-up unless explicitly approved.

## Finish

After every accepted outcome has a checkpoint commit:

1. run relevant broader checks and exercise the primary accepted path at integration level;
2. inspect `base_commit..HEAD` against the Brief;
3. append final Build Evidence with planned methodology `not applicable`, including named tests/cases and whole-feature path evidence;
4. set the Brief to `In Review` and create a final local handoff commit containing the completed feature artifacts.

Handoff to `review`. Never push, create a PR, merge, deploy, or rewrite history.
