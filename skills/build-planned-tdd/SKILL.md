---
name: build-planned-tdd
description: "Explicitly implement an accepted Ready Feature Brief through the planned Build strategy with a durable task graph and test-driven RED-GREEN-REFACTOR execution. Use only when the user invokes AbsolutForge build-planned-tdd."
---

# Build — Planned TDD Methodology

Use this experimental methodology when the human wants to evaluate strict test-driven execution inside the planned Build strategy. It is not a third first-class Build strategy: record strategy `planned` and methodology `tdd` for the feature's complete Build lifecycle.

Read `../../references/planned-build-contract.md`, `../../references/planned-tdd-contract.md`, `../../references/artifact-contracts.md`, `../../references/verification-doctrine.md`, `../../references/model-routing.md`, and the active host mapping.

## Start or resume

Accept only the canonical Feature Brief path.

For `Ready`, require a non-detached feature branch, clean worktree, empty index, and committed Brief. The permitted uncommitted consultation report is the only exception. Reject an existing `execution-map.md` or `implementation-plan.md`; a new Build never adopts or overwrites stale execution state.

Record HEAD as `base_commit`, append Build start evidence with strategy `planned`, planned methodology `tdd`, and the implementation-plan path, set the Brief to `Building`, and create a local Build-start checkpoint commit before source edits. Include the consultation report when present.

For `Building`, require strategy `planned` and methodology `tdd`. A missing methodology on legacy evidence means `standard` and hands off to `build-planned`; an autonomous or standard-planned Build must never be converted in place. Load the existing plan rather than recreating it. If no plan exists, compile it before source edits. A completed plan returned by Review appends a `PC-` entry that adds one corrective TDD task and increments the revision, then returns to `Executing`; completed task history remains unchanged.

## Compile the plan

Inspect the accepted Brief, amendments, linked project authority, and relevant current code/tests. Create the smallest useful acyclic graph using the planned Build contract, record `Planned methodology: tdd`, and add the TDD fields required by the TDD contract.

Every Expected Outcome maps to tasks or final verification. Each behavior-changing task names risk-based Test Obligations and uses TDD mode `required` unless a valid verification-doctrine exemption applies. A behavior-preserving task may use `characterization`; only a valid doctrine exemption uses `exempt`. Bound production and test write surfaces, order shared contracts before consumers, assign a capability tier, and define focused executable verification.

Validate outcome coverage, dependency order, write ownership, TDD modes, test obligations, final integration checks, and absence of new product intent. Mark the plan `Ready` and create a local plan checkpoint commit before any source edit.

Build never automatically offers or waits for consultation. Treat a supplied report only as evidence under the planned Build contract. Intent findings require a Brief amendment.

## Execute with TDD

Mark the plan `Executing`. Select exactly one dependency-ready task; this methodology does not use parallel waves because isolated RED attribution and production-before-test ordering must remain auditable.

Delegate only when useful. A worker receives one bounded task, minimum relevant context, its write boundary, Test Obligations, TDD mode and verification commands. It owns local implementation choices and the task's RED-GREEN-REFACTOR cycles, but no lifecycle, plan, commits, remote state, or broader redesign.

For every behavior slice in a `required` task:

1. establish that relevant baseline tests pass;
2. **RED** — add the smallest meaningful test for an applicable obligation, run it, and confirm it fails because accepted behavior is absent;
3. **GREEN** — make the smallest production change that satisfies that behavior and confirm the RED test passes;
4. **REFACTOR** — assess the resulting design, improve production or test structure where useful, and keep the relevant suite green;
5. repeat for remaining distinct risks, then run the task's focused verification.

Test fixtures and test-only support may be prepared before RED; production behavior may not. Syntax errors, broken fixtures, unrelated failures, and assertions that bind no changed behavior are not valid RED evidence. A compile or type failure is valid only when it is narrowly and directly caused by the intentionally missing accepted contract exercised by the new test. If the new test passes before production changes, do not invent a failure or continue to implementation: determine whether the behavior already exists, the test is weak, or the pending plan is invalid.

For `characterization`, prove the protective test or existing focused suite passes before a behavior-preserving production change, then keep it green through refactoring. For `exempt`, record the contract reason and closest observable check; difficulty, schedule, or unfamiliarity never qualify.

The orchestrator independently inspects every task diff and test value, confirms its write boundary and chronology evidence, and reruns focused checks. It records concise TDD evidence under the task contract, marks the task complete, and creates one checkpoint commit for the verified task. RED and GREEN do not require separate commits. Leave a clean committed boundary sufficient for a fresh orchestrator to resume without prior conversation.

When evidence invalidates pending execution details, append one `PC-` entry and revise only the affected pending frontier. When it changes accepted intent, stop for an amendment. Never weaken or skip an existing test to reach GREEN.

At a clean task boundary, resume by invoking this skill again with the canonical Brief; use `save` only for a mid-task or otherwise unresolved stop. Rotate context under the planned Build contract when causal or intent reasoning is under pressure.

## Finish

After every task has a checkpoint commit, rehydrate from durable artifacts and:

1. validate Expected Outcome and Test Obligation coverage again;
2. run final broader checks and exercise the primary accepted path at integration level;
3. inspect `base_commit..HEAD` against the immutable Brief, including test value and cross-task consistency;
4. append final Build Evidence with strategy `planned`, methodology `tdd`, named tests/cases, whole-feature path evidence, plan revision, task IDs, plan changes, and material routing escalations;
5. mark the plan `Complete`, set the Brief to `In Review`, and create a final local handoff commit.

Handoff to `review`. Never push, create a PR, merge, deploy, or rewrite history.
