# Legacy Planned Delegated Build Contract

## Purpose

Only already-started `delegated` builds use this contract. Resume and Review corrections now invoke `build-planned`, preserving every fixed-executor restriction below. The separate `build-planned-delegated` skill is removed; new starts cannot choose this methodology. Validate the effective fixed host profile before resuming implementation, not merely at the original Build start.

`build-planned-delegated` is a methodology of the first-class `planned` Build strategy. A high-capability orchestrator resolves design and compiles a durable implementation plan for one fixed, lower-cost host-mapped executor profile. The executor owns every production and test edit; the orchestrator owns the plan, lifecycle, supervision, verification, plan changes, commits, and whole-feature integration.

The fixed executor is deployment mechanics, not artifact semantics. Provider and model names belong only in host mappings. Durable artifacts record `Planned methodology: delegated` and never record provider identity.

## Planner-to-executor contract

The orchestrator reads enough repository evidence to settle implementation direction before dispatch. It chooses one coherent architecture within the accepted Brief rather than handing alternatives or unresolved design decisions to the executor.

Every delegated task adds these fields to the shared planned-task schema:

```markdown
- Execution owner: fixed delegated executor
- Implementation guidance: {precise prose describing responsibility, integration approach, relevant symbols, sequencing, and expected result}
- Watch points: {edge cases, likely traps, compatibility concerns, and invariants most likely to be violated}
- Decision boundary: {local choices the executor owns; questions or evidence that must return to the orchestrator}
```

These fields make the task executable by an early-mid coding worker. They complement rather than duplicate `Goal`, `Change surface`, `Invariants`, `Test obligations`, and `Verification`.

Guidance must not contain implementation code, pseudocode, method bodies, pseudo-diffs, copy-ready snippets, or line-by-line edit instructions. It should remove architectural ambiguity without pre-writing the patch. Name existing paths and symbols when repository inspection supports them; do not invent future helper names merely to make the plan look specific.

Plan validation rejects a delegated task when:

- accepted behavior or architecture remains undecided;
- its write surface is unbounded or overlaps another concurrently writable task;
- it requires high-capability product, architecture, migration, security, concurrency, or data-integrity judgment during implementation;
- its test obligations or observable completion criteria are unclear;
- safe execution would require embedding most of the patch in the plan.

Resolve such issues in the high-capability planning context, decompose the task further, or stop and declare the delegated methodology unsuitable. The orchestrator must not reserve implementation work for itself.

## Fixed executor dispatch

Before Build start, the host must be able to guarantee the effective delegated model and reasoning profile in its active host mapping, including any environment or host-level overrides that take precedence over a descriptor. Every implementation dispatch and every correction uses that profile. There is no automatic fallback to the orchestrator, a generic worker, or a stronger model, and Build never changes the user's environment to manufacture compliance.

Execute one dependency-ready task at a time. Use a fresh bounded executor context for each task unless the host can prove equivalent isolation. The executor receives:

- a compact Task Capsule derived from its complete task contract, preserving ownership, guidance, watch points and decision boundaries;
- only the relevant accepted Brief, amendment, ADR, rule, and dependency facts;
- the relevant source and tests or permission to inspect them;
- its exact write boundary and verification commands.

The executor may make local implementation choices inside `Decision boundary`. It must return evidence when the plan is wrong, a dependency is missing, a write outside the surface is required, verification fails for an unrelated reason, or an architectural decision remains. It never edits the Brief, plan, review, lifecycle state, Git history, remote state, or another task's surface.

## Orchestrator ownership

The orchestrator may inspect source and tests, run verification, update workflow artifacts, and create checkpoint commits. It may not write, repair, or complete production code or tests, including trivial-looking corrections. A rejected result returns to the same fixed executor with the smallest evidence-backed correction contract.

The orchestrator validates every returned diff for intent, correctness, write ownership, test value, and task completion. Completion Evidence records the delegated return and independent orchestrator validation without provider identity or raw worker dialogue. A task completes only after its meaningful fast gate is green and the orchestrator accepts the diff.

If the executor repeatedly cannot satisfy a valid task, preserve the last clean checkpoint and stop with concrete evidence. Do not escape the methodology by taking over implementation or silently changing the executor profile.

## Durable methodology and legacy TDD state

Record `Planned methodology: delegated` in Build start evidence, the implementation plan, final Build evidence, Save, Review, and the Feature Record. It cannot change during an active Build.

Artifacts with legacy methodology `tdd` remain historical valid evidence, but no current builder starts or resumes that methodology. An unfinished legacy TDD Build must use a compatible older AbsolutForge release or be explicitly abandoned and restarted from a clean committed Ready baseline. Never convert it to `standard` or `delegated` in place.
