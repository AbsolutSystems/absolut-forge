---
name: build-planned
description: "Explicitly implement an accepted Ready Feature Brief using a high-capability planner/orchestrator that creates a durable implementation task graph, delegates bounded low/standard tasks when useful, validates worker results, replans on evidence, and performs whole-feature integration verification. Use only when the user invokes AbsolutForge build-planned."
disable-model-invocation: true
---

# Build Planned

`build-planned` is the second first-class implementation strategy. The invoking high-capability model remains owner of the complete feature. Delegated workers are bounded executors, not planners or lifecycle owners.

Read `../../references/planned-build-contract.md`, `../../references/artifact-contracts.md`, `../../references/model-routing.md`, and the active host mapping.

## Start or resume

Accept only the canonical Feature Brief path.

For `Ready`, require a non-detached feature branch, clean worktree, empty index, and committed Brief. Record HEAD as `base_commit`; append Build start evidence with `Build strategy: planned`; change Brief to `Building`.

If `execution-map.md` exists, stop: autonomous execution state cannot be converted silently to planned Build.

For `Building`, require Build start evidence whose strategy is `planned` and load the canonical `implementation-plan.md`. If strategy is `autonomous`, stop and hand off to `build`.

## Compile intent into an implementation plan

Before source edits, inspect the accepted Brief, amendments, ADRs/rules/memory and relevant current code/tests. Create `implementation-plan.md` using the canonical planned-build contract.

Design the smallest useful acyclic task graph. Every accepted Expected Outcome must map to one or more tasks or final verification. Each task must have a bounded change surface, explicit invariants, dependencies, capability tier and focused verification.

Plan WHAT must change, WHERE the bounded responsibility lives, WHY the constraints exist, and HOW correctness will be verified. Do not prescribe HOW the code is locally implemented. Leave concrete control flow, helper structure, method bodies, naming, and equivalent local coding choices to the worker.

Do not produce line-by-line patch recipes, pseudo-patches, ordered edit scripts, code-shaped prose, or instructions such as "add this call after X" when the same outcome can be expressed as a behavioral contract. Useful symbol anchors may identify ownership or integration boundaries, but must not become a symbol-by-symbol edit checklist.

Prescribe a specific implementation mechanism only when that mechanism is itself binding: it is explicitly required by the accepted Brief, an accepted amendment, a linked ADR/binding project rule, or current compatibility/security/data evidence leaves no materially equivalent safe choice. Record that basis in the task constraints instead of presenting a planner preference as a requirement.

Give workers enough architecture, contract, boundary, and verification guidance to execute correctly while leaving local coding details local. If a task cannot be safely delegated without specifying most of its implementation, classify it `high` and keep it with the primary orchestrator rather than turning the plan into code written in prose.

Validate before execution:

- all accepted outcomes covered;
- dependencies acyclic and executable;
- task write surfaces sufficiently bounded;
- shared contracts ordered before consumers;
- final integration checks defined;
- no task introduces unaccepted product intent.

Then mark the plan `Ready`, then `Executing` when the first task starts.

## Execute one task at a time

Select only a dependency-ready task. Mark it `in-progress` before work.

### Route

- `low`: delegate when a reliable cheap worker is available.
- `standard`: delegate to a mid-tier worker when useful.
- `high`: prefer the primary orchestrator or an equivalently capable worker.

Do not delegate merely for ceremony. If fresh worker dispatch is unavailable or the delegation package would be larger/more expensive than direct execution, execute the task in the primary context and record no false delegation claim.

### Dispatch

Give a worker only the bounded task contract plus minimum relevant Brief/ADR/rule/dependency context, relevant paths/tests, write boundary and verification commands. Never hand it the authority to mutate the Brief, task graph, other tasks, review, branch history or remote state.

### Validate

After a worker returns, the orchestrator must independently inspect the changed paths/diff, confirm writes stayed in the task surface, inspect verification evidence, and run or rerun the focused check when evidence is incomplete or stale. The worker's claim is not proof.

Only then fill Completion Evidence and mark the task `complete`.

## Handle deviations

If evidence invalidates repository assumptions, dependencies, or the required change surface while accepted intent remains valid, mark the task `blocked`, append a `plan deviation`, and set the plan to `Needs Replan`.

Only the high-capability orchestrator replans. Preserve completed task history; revise only the blocked task and affected pending frontier unless evidence proves broader pending invalidity. Append a Replan entry, increment plan revision, validate coverage/dependency acyclicity, return to `Executing`.

If evidence would change behavior, scope, public contract, security/data handling, migration or material cost, append an `intent deviation` and stop for explicit Brief amendment. Do not hide product redesign in a replan.

## Failure boundary

A failing focused check may receive one evidence-backed bounded repair inside the task. Before a second speculative repair for the same observable failure, verify root-cause mapping and task scope. If unclear, return the failure to the orchestrator for diagnostic reasoning or replan instead of letting a low/standard worker broaden the change.

## Whole-feature integration

After every task is complete:

1. validate Expected Outcome coverage again;
2. run the defined final verification plus relevant broader build/integration/type/lint checks;
3. inspect the complete `base_commit..HEAD` diff against the immutable Brief, not merely against the plan;
4. detect cross-task inconsistencies, duplicate abstractions, stale docs and diff garbage;
5. append final Build Evidence including plan revision, task IDs, deviations/replans and capability escalations;
6. mark `implementation-plan.md` `Complete`;
7. set Brief status to `In Review` and commit all feature source/artifacts locally.

Then hand off to the common `review` skill. Never push, create a PR, merge, deploy, or rewrite history.
