---
name: build-planned-delegated
description: "Explicitly implement an accepted Ready Feature Brief through a plan written by a high-capability orchestrator for a fixed host-mapped executor. The executor owns all source and test edits; the orchestrator owns planning, supervision, verification, and integration. Use only when the user invokes AbsolutForge build-planned-delegated."
---

# Build — Planned Delegated Methodology

Use this planned methodology when a high-capability planner can resolve the architecture and prepare bounded implementation work for the host's fixed delegated executor. This is not opportunistic delegation: every source and test change, including corrections, belongs to that executor profile.

Read `../../references/planned-build-contract.md`, `../../references/planned-delegated-contract.md`, `../../references/artifact-contracts.md`, `../../references/verification-doctrine.md`, `../../references/model-routing.md`, `../../references/harness-command-contract.md`, and the active host mapping.

## Start or resume

Accept only the canonical Feature Brief path.

For `Ready`, require a non-detached feature branch, clean worktree, empty index, and committed Brief. The permitted uncommitted consultation report is the only exception. Reject an existing `execution-map.md` or `implementation-plan.md`; a new Build never adopts or overwrites stale execution state.

Before changing lifecycle state, confirm that the invoking context satisfies the active host's high-capability planner profile and can guarantee the fixed executor's effective model and reasoning effort after host/environment overrides. If either condition fails, stop without starting Build; never mutate the user's environment, substitute the orchestrator, or select another model.

Record HEAD as `base_commit`, append Build start evidence with strategy `planned`, planned methodology `delegated`, and the implementation-plan path, set the Brief to `Building`, and create a local Build-start checkpoint commit before source edits. Include the consultation report when present.

For `Building`, require strategy `planned` and methodology `delegated`. Standard planned state hands off to `build-planned`; legacy `tdd` state is not convertible and requires a compatible older release or explicit abandonment and restart from a clean committed Ready baseline. Load the existing plan rather than recreating it. If no plan exists, compile it before source edits. When the sibling `review.md` contains open blockers, read it as required correction input without editing it. A completed plan returned by Review appends one `PC-` entry that adds a corrective delegated task and increments the revision, then returns to `Executing`; completed task history remains unchanged.

## Compile for the executor

Inspect the accepted Brief, amendments, linked project authority, relevant current code/tests, and the active host's delegated-executor mapping. Resolve architectural choices before dispatch and create the smallest useful acyclic graph using the shared and delegated planned contracts. Record `Planned methodology: delegated`.

Write each task for an early-mid implementation executor. State the intended responsibility and integration approach, relevant symbols and bounded paths, dependency facts, invariants, edge cases, likely traps, applicable Test Obligations, fast verification commands, and decisions the worker must return rather than guess. Explain what and how in precise prose, but do not include implementation code, pseudocode, method bodies, pseudo-diffs, or line-by-line edit scripts.

Every task must be executable by the fixed delegated profile after reading its contract and minimum supporting context. Resolve high-level design questions in the plan and decompose work until no task requires the executor to invent architecture or broaden intent. If that cannot be done safely, stop before implementation and report that this methodology is unsuitable; never retain a `high` task for direct orchestrator implementation.

Map every Expected Outcome to tasks or final verification. Bound production and test write surfaces, order shared contracts before consumers, name risk-based Test Obligations, and separate fast task gates from final broad and integration verification. Validate outcome coverage, dependency order, write ownership, delegated guidance, decision boundaries, test obligations, final checks, and absence of new product intent. Mark the plan `Ready` and create a local plan checkpoint commit before any source edit.

Build never automatically offers or waits for consultation. Treat a supplied report only as evidence under the planned Build contract. Intent findings require a Brief amendment.

## Delegate and validate

Mark the plan `Executing`. Dispatch one dependency-ready task at a time to the exact host-mapped executor and reasoning effort. Give it the bounded task contract and only the Brief, authority, dependency evidence, code/tests, and commands needed for that task. The executor owns all implementation and test edits within the declared surface; it owns no lifecycle artifacts, plan mutations, commits, remote state, or broader redesign.

The orchestrator never writes or repairs production code or tests. It independently inspects each returned diff and test value, confirms the write boundary and accepted behavior, and reruns the task's fast gate when evidence is incomplete. If correction is needed, record the evidence and redispatch a bounded correction to the same executor profile. Do not silently finish the patch in the primary context or route it to a stronger worker.

After a valid green result, write concise Completion Evidence, mark the task complete, and create its checkpoint commit. Leave a clean committed boundary sufficient for a fresh high-capability orchestrator to resume from the Brief, plan, Git, and relevant code/tests without previous conversation.

When evidence invalidates pending execution details, append one `PC-` entry and revise only the affected pending frontier. When it changes accepted intent, stop for an amendment. Never weaken or skip an existing test to reach green.

At a clean task boundary, resume by invoking this skill again with the canonical Brief. Use `save` only for a mid-task or otherwise unresolved stop. Rotate the orchestrator context under the shared planned contract when intent or causal reasoning is under pressure.

## Finish

After every task has a checkpoint commit, rehydrate from durable artifacts and:

1. validate Expected Outcome coverage and delegated ownership again;
2. run the authoritative full suite for the affected project or changeset once per final-verification attempt, without separately rerunning included integration/e2e suites, and exercise the primary accepted path;
3. inspect `base_commit..HEAD` against the immutable Brief for correctness, cross-task consistency, test value, scope, and diff garbage;
4. route any required source or test correction back to the fixed executor, checkpoint it as a `PC-` task, and repeat affected verification;
5. append final Build Evidence with planned methodology `delegated`, every current-schema field, named tests/cases and results or valid exemptions, whole-feature path evidence, plan revision, task IDs, plan changes, and material routing escalations;
6. mark the plan `Complete`, set the Brief to `In Review`, and create a final local handoff commit.

Before transition, verify that the final entry describes the implementation state being handed off and satisfies the delivery gate in `artifact-contracts.md`. Any later source or test change invalidates it and must return through a delegated corrective task. Compilation, bundling, packaging, or artifact production alone is not a whole-feature exercise unless it is the accepted behavior. Never move a failing feature to Review.

Handoff to `review` by reporting the canonical Brief and Review paths, then end with the copy-ready active-host `review` invocation required by `harness-command-contract.md`. Resolve the real paths; do not merely name the skill or show multiple host variants. Do not invoke Review unless the human explicitly invoked it or authorized this request through Review. Never push, create a PR, merge, deploy, or rewrite history.
