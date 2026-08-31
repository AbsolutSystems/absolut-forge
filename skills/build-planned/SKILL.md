---
name: build-planned
description: "Explicitly implement an accepted Ready Feature Brief using a high-capability planner/orchestrator that creates a durable implementation task graph, delegates bounded low/standard tasks when useful, validates worker results, replans on evidence, and performs whole-feature integration verification. Use only when the user invokes AbsolutForge build-planned."
---

# Build Planned

`build-planned` is the second first-class implementation strategy. The invoking high-capability model remains owner of the complete feature. Delegated workers are bounded executors, not planners or lifecycle owners.

Read `../../references/planned-build-contract.md`, `../../references/artifact-contracts.md`, `../../references/verification-doctrine.md`, `../../references/model-routing.md`, and the active host mapping.

## Start or resume

Accept only the canonical Feature Brief path.

For `Ready`, require a non-detached feature branch, clean worktree, empty index, and committed Brief. An uncommitted `consult-{slug}.md` is the only permitted exception, per the Build start rule in `../../references/artifact-contracts.md`. Record HEAD as `base_commit`; append Build start evidence with `Build strategy: planned`; change Brief to `Building`.

If `execution-map.md` exists, stop: autonomous execution state cannot be converted silently to planned Build.

For `Building`, require Build start evidence whose strategy is `planned` and load the canonical `implementation-plan.md`. If strategy is `autonomous`, stop and hand off to `build`.

An existing plan is never recreated on resume. Continue from its recorded status:

- `Draft`: finish compiling and validating that same file;
- `Ready`: execute it, or revise it first, after reading `## Consultation`: an `awaiting` entry for the current revision holds the plan and is re-stated, not re-decided;
- `Executing`: select the next dependency-ready task;
- `Needs Replan`: replan before execution, or continue an already-appended replan, reading `## Consultation` the same way;
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
- every behavior-changing task has a test expectation or a recorded exemption, with its test paths inside its own change surface, and path ownership follows the overlap rule in `planned-build-contract.md`;
- final integration checks defined, including at least one whole-feature path exercised at integration level;
- no task introduces unaccepted product intent.

Then mark the plan `Ready`.

## Optional plan consultation

Plan validation above is self-assessment by the context that wrote the plan, so a `Ready` plan is consultable through `consult` in Plan mode before execution. Consultation runs in a separate session and preferably a different model family; it hands its result back through `absolutforge/features/{slug}/consult-{slug}.md`.

`## Consultation` tracks one thing only, per `planned-build-contract.md`: whether a question is open. `awaiting` holds the plan; `settled` releases it; no entry means nothing was ever asked, which is the normal case. Write an entry only when you actually offer or dispose a consultation.

### Offer

Offer only when the plan carries material risk: several tasks rather than one or two, planned delegation, cross-cutting or shared-contract tasks, or coverage that leans mainly on final verification. For a small direct plan, say in one line that consultation is available, write no entry, and continue. Never require consultation as ceremony.

To offer: write the plan to disk, record `Revision {N}: awaiting — {exact command}` against the current revision, print that command from the active host mapping in `../../references/harness-command-contract.md` with the plan path and any extra context paths worth passing, state the two choices plainly — consult first, or say to execute now — and end the turn. Until the human answers, select no task, edit no source, and do not advance the plan past its current status.

If the host cannot ask a human at all, record `settled — host cannot prompt` and execute.

At most one offer per revision. On resume, read `## Consultation` before deciding anything: an `awaiting` entry means re-state that same offer and keep holding, which is not a second offer; a `settled` entry or no entry means continue without asking again, unless the human is handing you a report right now. If the resuming host cannot ask a human at all, do not hold indefinitely: advance that entry to `settled — host cannot prompt` and execute, exactly as an offer on such a host would have.

### Consume

When the human says the consultation is ready, read `consult-{slug}.md` and its newest block. Findings are evidence, not instructions. Decide each `C-` ID yourself, set its `Disposition` in the report to `accepted`, `rejected` or `routed to Brief amendment`, and add nothing else to that file.

Then advance that revision's entry to `settled — consulted {report path}, accepted {C-IDs | none}`, writing a new entry where none exists yet. The question is answered whatever you decided, so record that before acting on any finding. Accepting no plan finding leaves the revision as it is and execution continues.

A finding classified `intent` is never a plan edit and never merely a note: append an `intent deviation` and stop for an explicit Brief amendment exactly as `## Handle deviations` requires, before any further execution. Use the pre-execution deviation form in `planned-build-contract.md` — `no task` in the header, the report path and accepted `C-IDs` as its observable evidence — so the finding stays traceable to the amendment it forces.

If you accepted any plan finding, revise the plan for it and record that bump the way every bump is recorded: append an `R-` entry whose trigger is the consultation and the accepted `C-IDs`, increment the revision to `N+1`, and re-run the validation list for whatever you changed. That bump is not a replan, so leave the status where it was — a `Ready` plan stays `Ready`, a `Needs Replan` plan stays `Needs Replan` until the replan that owns it finishes, per `### After a replan` — and carry `none` in the entry's task fields that do not apply. Write no `## Consultation` entry for `N+1` — a revision produced by consuming a consultation is never consulted again, and only a replan reopens the offer.

When the human declines and tells you to execute now, advance the entry to `settled — declined` and continue.

A consultation you never requested carries no weight of its own: read it and dispose of its findings the same way. Record `settled — consulted ...` against the current revision when that revision has no entry yet, or when its entry reads `settled — host cannot prompt` and a consultation has now actually happened. If it already reads any other `settled`, that settlement is final — dispose the findings, write no second entry, reword nothing, and act on any accepted finding exactly as above.

### After a replan

A replan that materially changes the pending frontier may be consulted once at its new revision. Append the `R-` entry and increment the revision first, then offer against that new revision, holding the plan at `Needs Replan` until the entry is `settled`.

Then, in this order: settle the entry, dispose the findings, and apply whatever you accepted — including the consultation `R-` bump, which leaves the status at `Needs Replan` like every consultation bump. Only after that does the replan itself finish: return the plan to `Executing`. An `intent` finding stops here instead, for the Brief amendment.

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
5. append final Build Evidence to the evidence schema in `../../references/artifact-contracts.md`, naming `Tests added/updated`, `Whole-feature path exercised` with its result or the recorded reason it was not available, plan revision, task IDs, recorded test exemptions, deviations/replans and capability escalations;
6. mark `implementation-plan.md` `Complete`;
7. set Brief status to `In Review` and commit all feature source/artifacts locally.

Then hand off to the common `review` skill. Never push, create a PR, merge, deploy, or rewrite history.
