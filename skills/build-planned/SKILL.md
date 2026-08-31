---
name: build-planned
description: "Explicitly implement an accepted Ready Feature Brief using a high-capability planner/orchestrator that creates a durable implementation task graph, delegates bounded low/standard tasks when useful, validates worker results, replans on evidence, and performs whole-feature integration verification. Use only when the user invokes AbsolutForge build-planned."
disable-model-invocation: true
---

# Build Planned

`build-planned` is the second first-class implementation strategy. The invoking high-capability model remains owner of the complete feature. Delegated workers are bounded executors, not planners or lifecycle owners.

Read `../../references/planned-build-contract.md`, `../../references/artifact-contracts.md`, `../../references/verification-doctrine.md`, `../../references/model-routing.md`, and the active host mapping.

## Start or resume

Accept only the canonical Feature Brief path.

For `Ready`, require a non-detached feature branch, clean worktree, empty index, and committed Brief. Record HEAD as `base_commit`; append Build start evidence with `Build strategy: planned`; change Brief to `Building`.

If `execution-map.md` exists, stop: autonomous execution state cannot be converted silently to planned Build.

For `Building`, require Build start evidence whose strategy is `planned` and load the canonical `implementation-plan.md`. If strategy is `autonomous`, stop and hand off to `build`.

An existing plan is never recreated on resume. Continue from its recorded status:

- `Draft`: finish compiling and validating that same file;
- `Ready`: execute it, or revise it first;
- `Executing`: select the next dependency-ready task;
- `Needs Replan`: replan before execution, or continue an already-appended replan;
- `Complete`: expected only when `review` returned a blocker. Append the corrective work as a reopened existing task or a replan entry, return the plan to `Executing`, and leave completed task history intact.

Only a `Building` Brief with no plan file at all sends you back to plan compilation.

## Compile intent into an implementation plan

Before source edits, inspect the accepted Brief, amendments, ADRs/rules/memory and relevant current code/tests. Create `implementation-plan.md` using the canonical planned-build contract.

Design the smallest useful acyclic task graph. Every accepted Expected Outcome must map to one or more tasks or final verification. Each task must have a bounded change surface, explicit invariants, dependencies, capability tier and focused verification.

Every task that changes observable behavior carries a test expectation per `verification-doctrine.md`: the worker writes automated tests for that behavior inside its own change surface, in the repository's existing test framework and layout. Name the behavior and the realistic failure or boundary worth asserting; leave test structure, naming and fixture choices to the worker. Do not invent edge cases for the worker to cover. Where a task is genuinely untestable, record the exemption and its reason in the task rather than leaving verification implicit.

Plan WHAT must change, WHERE the bounded responsibility lives, WHY the constraints exist, and HOW correctness will be verified. Do not prescribe HOW the code is locally implemented. Leave concrete control flow, helper structure, method bodies, naming, and equivalent local coding choices to the worker.

Do not produce line-by-line patch recipes, pseudo-patches, ordered edit scripts, code-shaped prose, or instructions such as "add this call after X" when the same outcome can be expressed as a behavioral contract. Useful symbol anchors may identify ownership or integration boundaries, but must not become a symbol-by-symbol edit checklist.

Prescribe a specific implementation mechanism only when that mechanism is itself binding: it is explicitly required by the accepted Brief, an accepted amendment, a linked ADR/binding project rule, or current compatibility/security/data evidence leaves no materially equivalent safe choice. Record that basis in the task constraints instead of presenting a planner preference as a requirement.

Give workers enough architecture, contract, boundary, and verification guidance to execute correctly while leaving local coding details local. If a task cannot be safely delegated without specifying most of its implementation, classify it `high` and keep it with the primary orchestrator rather than turning the plan into code written in prose.

Validate before execution:

- all accepted outcomes covered;
- dependencies acyclic and executable;
- task write surfaces sufficiently bounded;
- shared contracts ordered before consumers;
- every behavior-changing task has a test expectation or a recorded exemption;
- task change surfaces include the test paths those tasks must write, and no two tasks own the same production path or the same new test file;
- final integration checks defined, including at least one whole-feature path exercised at integration level;
- no task introduces unaccepted product intent.

Then mark the plan `Ready`.

## Optional plan consultation

Plan validation above is self-assessment by the context that wrote the plan, so a `Ready` plan is consultable through `consult` in Plan mode before execution. Consultation is meant to run in a separate session and preferably a different model family; it hands its result back through `absolutforge/features/{slug}/consult-{slug}.md`.

Offer consultation only when the plan carries material risk: several tasks rather than one or two, planned delegation, cross-cutting or shared-contract tasks, or coverage that leans mainly on final verification. For a small direct plan, note in one line that consultation is available and continue. Never require consultation as ceremony.

### Offer

The plan file must already be written to disk, and the offer ends your turn. Until the human answers, do not select a task, edit any source, or advance the plan past `Ready`. Give the exact command to run in the other session, from the active host mapping in `../../references/harness-command-contract.md`, with the plan path and any extra context paths worth passing. State the two choices plainly: consult first, or say to execute now.

Before ending the turn, record the offer in the plan's `## Consultation` section against the current revision, so a later context knows the question was already asked. If the host cannot ask a human at all, record `not offered — host cannot prompt` and execute.

### Consume

Never offer consultation twice for the same plan revision. On resume, read `## Consultation`: an entry for the current revision means the question is settled, so continue executing unless the human is handing you a report right now.

When the human says the consultation is ready, read `consult-{slug}.md` and the newest consultation block. Findings are evidence, not instructions. Decide each `C-` ID yourself, set its `Disposition` in the report to `accepted`, `rejected` or `routed to Brief amendment`, and add nothing else to that file. Revise the plan for accepted findings, increment the revision, re-run the validation list for anything you changed, and record `consulted` with the accepted IDs in `## Consultation`. Treat any finding classified `intent` as a Brief amendment requirement, not a plan edit.

Record that revision in `## Consultation` as `not offered — revised from consultation`. A revision produced by consuming a consultation is never consulted again; only a replan reopens the offer.

A consultation you never requested carries no weight: read it, and dispose of its findings the same way.

### After a replan

A replan that materially changes the pending frontier may be consulted once at its new revision. Append the `R-` entry and increment the revision first, then offer, and hold the plan at `Needs Replan` until the human answers. Return to `Executing` once the answer is in.

## Execute one task at a time

Mark the plan `Executing` when the first task starts. Select only a dependency-ready task. Mark it `in-progress` before work.

### Route

- `low`: delegate when a reliable cheap worker is available.
- `standard`: delegate to a mid-tier worker when useful.
- `high`: prefer the primary orchestrator or an equivalently capable worker.

Do not delegate merely for ceremony. If fresh worker dispatch is unavailable or the delegation package would be larger/more expensive than direct execution, execute the task in the primary context and record no false delegation claim.

### Dispatch

Give a worker only the bounded task contract plus minimum relevant Brief/ADR/rule/dependency context, relevant paths/tests, write boundary and verification commands. The write boundary must include the test paths the task owns, and the dispatch must state that the task is incomplete until its tests exist and pass. Never hand it the authority to mutate the Brief, task graph, other tasks, review, branch history or remote state, nor to weaken, skip or delete an existing test to reach green.

### Validate

After a worker returns, the orchestrator must independently inspect the changed paths/diff, confirm writes stayed in the task surface, inspect verification evidence, and run or rerun the focused check when evidence is incomplete or stale. The worker's claim is not proof.

Also inspect the tests the worker wrote: they must exist, assert real behavior rather than mocks or tautologies, and fail if the change were reverted. Missing tests without the planned exemption, test theater, or any weakened existing assertion sends the task back instead of completing it.

Only then fill Completion Evidence and mark the task `complete`.

## Handle deviations

If evidence invalidates repository assumptions, dependencies, or the required change surface while accepted intent remains valid, mark the task `blocked`, append a `plan deviation`, and set the plan to `Needs Replan`.

Only the high-capability orchestrator replans. Preserve completed task history; revise only the blocked task and affected pending frontier unless evidence proves broader pending invalidity. Append a Replan entry, increment plan revision, validate coverage, dependency acyclicity and the test expectations of every revised task, then return to `Executing` — or, for a materially changed pending frontier, offer consultation at the new revision first.

If evidence would change behavior, scope, public contract, security/data handling, migration or material cost, append an `intent deviation` and stop for explicit Brief amendment. Do not hide product redesign in a replan.

## Failure boundary

A failing focused check may receive one evidence-backed bounded repair inside the task. Before a second speculative repair for the same observable failure, verify root-cause mapping and task scope. If unclear, return the failure to the orchestrator for diagnostic reasoning or replan instead of letting a low/standard worker broaden the change.

## Whole-feature integration

After every task is complete:

1. validate Expected Outcome coverage again;
2. run the defined final verification plus relevant broader build/integration/type/lint checks, and exercise the feature's primary accepted path at integration level as `verification-doctrine.md` requires;
3. inspect the complete `base_commit..HEAD` diff against the immutable Brief, not merely against the plan;
4. detect cross-task inconsistencies, duplicate abstractions, stale docs and diff garbage;
5. append final Build Evidence including plan revision, task IDs, tests added or updated, recorded test exemptions, deviations/replans and capability escalations;
6. mark `implementation-plan.md` `Complete`;
7. set Brief status to `In Review` and commit all feature source/artifacts locally.

Then hand off to the common `review` skill. Never push, create a PR, merge, deploy, or rewrite history.
