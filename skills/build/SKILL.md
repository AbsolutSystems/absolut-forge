---
name: build
description: "Explicitly implement an accepted Ready Feature Brief autonomously with a high-capability primary coding model, risk-based tests, checkpoint commits, and whole-feature handoff to Review. Use only when the user invokes AbsolutForge build."
---

# Build — Autonomous Strategy

Use autonomous Build as the default strategy when one high-capability context can efficiently own the complete feature.

Read `../../references/artifact-contracts.md`, `../../references/verification-doctrine.md`, and `../../references/harness-command-contract.md`, plus the active host mapping as needed.

## Start or resume

Accept only `absolutforge/features/{slug}/feature-brief.md`.

For `Ready`, require a non-detached feature branch, clean worktree, empty index, and committed Brief. The uncommitted consultation report allowed by the artifact contract is the only exception. Reject an existing `implementation-plan.md`.

Record HEAD as `base_commit`, append Build start evidence with strategy `autonomous` and planned methodology `not applicable`, set the Brief to `Building`, and create a local Build-start checkpoint commit before any source edit. Include the permitted consultation report when present.

For `Building`, require Build start evidence whose strategy is `autonomous`. A planned strategy hands off by recorded methodology: `build-planned-delegated` for `delegated`, `build-planned` for `standard` or a legacy missing field. Legacy `tdd` state requires a compatible older release or explicit abandonment and restart; never convert execution state. When the sibling `review.md` contains open blockers, read it as required correction input without editing it.

## Execute outcomes

Read the immutable accepted Brief, amendments, linked project authority, and relevant current code/tests. Material intent changes require an explicit amendment.

Own the local implementation trajectory. Create `execution-map.md` only when dependencies, uncertainty, or cross-session resume justify it; keep it outcome-oriented.

For each coherent outcome:

1. implement the accepted behavior;
2. derive applicable test obligations from `verification-doctrine.md` and add tests for the distinct risks;
3. inspect the tests for meaningful coverage of repository-owned behavior, then run the outcome's exact or smallest relevant unit tests and cheap build, type, or lint checks to green;
4. diagnose and make one bounded evidence-backed repair when needed;
5. append intermediate Build Evidence, update the map when present, and create a local checkpoint commit containing the outcome's source, tests, and artifacts.

Do not run the full changeset, integration suite, or end-to-end suite at an outcome checkpoint. Map integration-only obligations to final verification. Do not mark the outcome complete without its green fast gate or a recorded exemption. Never weaken an existing test to reach green. Before a second speculative repair for the same failure, establish causal mapping and scope or escalate.

A strictly trivial adjacent defect inside the touched surface may be fixed and reported. Non-trivial adjacent work remains follow-up unless explicitly approved.

## Finish

After every accepted outcome has a checkpoint commit:

1. run the authoritative full suite for the affected project or changeset once per final-verification attempt, without separately rerunning integration/e2e suites already included, and exercise the primary accepted path;
2. inspect `base_commit..HEAD` against the Brief;
3. append final Build Evidence with planned methodology `not applicable`, including every current-schema field, named tests/cases and results or valid exemptions, and whole-feature path evidence under the verification doctrine;
4. verify that this final entry describes the implementation state being handed off, then set the Brief to `In Review` and create a final local handoff commit containing the completed feature artifacts.

Any later source or test change invalidates the final Build Evidence. Return the Brief to `Building`, repeat the affected final verification, and append a new complete final entry before another Review handoff. A compile, bundle, package, or produced artifact is not a whole-feature exercise unless artifact production is itself the accepted behavior.

If final verification fails, preserve completed outcome history, diagnose the cause, add one bounded corrective outcome with an appropriate green fast test gate, checkpoint it, and repeat final verification. Do not move a failing feature to Review.

Handoff to `review` by reporting the canonical Brief and Review paths, then end with the copy-ready active-host `review` invocation required by `harness-command-contract.md`. Resolve the real paths; do not merely name the skill or show multiple host variants. Do not invoke Review unless the human explicitly invoked it or authorized this request through Review. Never push, create a PR, merge, deploy, or rewrite history.
