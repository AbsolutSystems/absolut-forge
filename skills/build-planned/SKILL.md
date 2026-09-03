---
name: build-planned
description: "Explicitly implement an accepted Ready Feature Brief through a durable task graph, bounded worker delegation, and fresh-context rotation when that overhead is justified. The high-capability orchestrator owns tests, checkpoint commits, plan changes, and integration. Use only when the user invokes AbsolutForge build-planned."
---

# Build — Planned Strategy

Use this higher-overhead strategy when durable decomposition, meaningful bounded delegation, or cross-session resume is expected to pay for the plan. Otherwise prefer autonomous `build`.

Read `../../references/planned-build-contract.md`, `../../references/artifact-contracts.md`, `../../references/verification-doctrine.md`, `../../references/model-routing.md`, and the active host mapping.

## Start or resume

Accept only the canonical Feature Brief path.

For `Ready`, require a non-detached feature branch, clean worktree, empty index, and committed Brief. The permitted uncommitted consultation report is the only exception. Reject an existing `execution-map.md` or `implementation-plan.md`; a new Build never adopts or overwrites stale execution state.

Record HEAD as `base_commit`, append Build start evidence with strategy `planned` and planned methodology `standard`, set the Brief to `Building`, and create a local Build-start checkpoint commit before source edits. Include the consultation report when present.

For `Building`, require strategy `planned` and methodology `standard`; absence of methodology in legacy evidence means `standard`. An autonomous strategy hands off to `build`, while methodology `tdd` hands off to `build-planned-tdd`. Load the existing plan rather than recreating it. If no plan exists, compile it before source edits. A completed plan returned by Review appends a `PC-` entry that adds one corrective task and increments the revision, then returns to `Executing`; completed task history remains unchanged.

## Compile the plan

Inspect the accepted Brief, amendments, linked project authority, and relevant current code/tests. Create the smallest useful acyclic graph using `planned-build-contract.md`.

Every Expected Outcome maps to tasks or final verification. Record `Planned methodology: standard`. Each behavior-changing task names applicable risk-based Test Obligations, not merely a test count. Bound production and test write surfaces, order shared contracts before consumers, assign a capability tier, and define each task's fast unit-test gate separately from final broad and integration verification.

Validate outcome coverage, dependency order, write ownership, test obligations, final integration checks, and absence of new product intent. Mark the plan `Ready` and create a local plan checkpoint commit before any source edit.

Build never automatically offers or waits for consultation. If the human supplies a consultation report, treat it as evidence: accept only findings that still apply, record plan changes in a `PC-` entry, and leave the report unchanged. Intent findings require a Brief amendment.

## Execute and validate

Mark the plan `Executing` when work begins. Select one dependency-ready task or a parallel wave whose write surfaces are fully disjoint, as allowed by the planned-build contract.

Delegate only when useful. A worker receives one bounded task, minimum relevant context, its write boundary, Test Obligations, fast verification commands, and the targeted mutation proofs required for new or materially changed guards. It owns local implementation choices but no lifecycle, plan, commits, remote state, or broader redesign. A worker executing alone may produce the mutation evidence; workers in a parallel wave leave targeted mutation to the orchestrator so temporary production changes cannot contaminate another task's test run.

The orchestrator independently inspects every task diff and its tests, confirms the write boundary, mutation evidence, and restored production state, and reruns the task's fast unit-test gate when evidence is incomplete. For a parallel wave, it performs each task's targeted mutations sequentially during that task's validation. Do not run the full changeset, integration suite, or end-to-end suite at a task checkpoint; map integration-only obligations to final verification. Validate and checkpoint-commit one task at a time, staging only its paths when a parallel wave returned multiple results. A task is complete only when its obligations are covered, its unit guards are mutation-bound, and its fast gate passes or its exemption is recorded.

After each task, reduce the result to concise Completion Evidence, including any new dependency or invariant fact. Leave a clean committed boundary from which a fresh orchestrator can resume using the Brief, plan, Git, and relevant code/tests without the earlier conversation. Do not retain raw worker dialogue or logs as durable plan content.

When evidence invalidates pending execution details, append one `PC-` entry and revise only the affected pending frontier. When it changes accepted intent, stop for an amendment. Never weaken or skip an existing test to reach green.

Rotate to a fresh session when context pressure threatens intent or causal reasoning, particularly after a large wave, a `PC-` change, or a long diagnosis, and before a substantial `high` task or final integration when practical. At a clean task boundary, resume by invoking this skill again with the canonical Brief; no `save` artifact is needed. Use `save` only for a mid-task or otherwise unresolved stop, remembering that it does not preserve dirty source.

## Finish

After every task has a checkpoint commit, rehydrate from durable artifacts rather than conversational memory; for a long Build, prefer a fresh orchestrator context for this pass:

1. validate Expected Outcome coverage again;
2. perform the exact-case mutation proofs and checks mapped to real integration boundaries, then run the authoritative full suite for the affected project or changeset once per final-verification attempt, without separately rerunning integration/e2e suites already included, and exercise the primary accepted path;
3. inspect `base_commit..HEAD` against the immutable Brief and detect cross-task inconsistencies or diff garbage;
4. append final Build Evidence with planned methodology `standard`, every current-schema field, named tests/cases, targeted mutation proofs or valid exemptions, whole-feature path evidence, plan revision, task IDs, plan changes, and material routing escalations;
5. mark the plan `Complete`, set the Brief to `In Review`, and create a final local handoff commit.

Before the transition, verify that the final entry describes the implementation state being handed off and satisfies the delivery gate in `artifact-contracts.md`. Any later source or test change invalidates it: return to `Building`, append one `PC-` corrective task when work is required, repeat affected final verification, and append a new complete final entry before another Review handoff. Compilation, bundling, packaging, or artifact production alone is not a whole-feature exercise unless it is the accepted behavior.

If final verification fails, preserve completed task history, append one `PC-` entry that adds a bounded corrective task, execute and checkpoint it with the same fast verification and mutation rules, then repeat final verification. Do not move a failing feature to Review.

Handoff to `review` by reporting the canonical Brief and Review paths. Do not invoke Review unless the human explicitly invoked it or authorized this request through Review. Never push, create a PR, merge, deploy, or rewrite history.
