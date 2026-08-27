# Phase 2: Discuss and optional consultation (epic: AbsolutForge MVP)

## Parent context

> Start by reading `absolutforge/features/absolutforge-mvp/planning-main.md`.

- Epic planning: `absolutforge/features/absolutforge-mvp/planning-main.md`
- Dependencies: Phase 1 artifact, activation, handoff, ADR, and project-memory contracts

## Status
Completed — 2026-08-27

## Phase goal

Deliver an adaptive, code-aware `discuss` workflow that converts a product idea
into one accepted Feature Brief without detailed task decomposition or repeated
quality gates. Add an optional explicit-only `consult` workflow so a second
harness or model can pressure-test an existing Brief and, with human approval,
improve a Draft or propose an amendment to a Ready baseline.

The result must preserve the central AbsolutForge thesis: the model investigates
facts, the human owns material product decisions, and implementation receives a
precise intent contract rather than a file-by-file recipe.

## Users

- Developers who want Claude Code or Codex to turn an initially incomplete idea
  into an implementation-ready intent contract.
- Developers who want a second model or harness to inspect that contract before
  build without introducing a mandatory review ceremony.
- Later `build`, `review`, and `ship` stages that need one stable intent baseline.

## Expected behavior

### `discuss`

1. The user explicitly invokes `discuss` with a new idea or an existing Brief.
2. The skill distinguishes a new feature, a resumable `Draft`, and a `Ready`
   baseline. It never silently rewrites a Ready baseline.
3. It reads the relevant project context and current code before asking the user
   for facts that can be discovered from the repository.
4. It maintains a session-only decision tree. Each adaptive round asks a small
   frontier of normally two to four independent, high-impact questions whose
   prerequisites are already settled. Each question includes the model's
   recommendation when evidence supports one.
5. The user decides product intent. Repository evidence remains evidence, model
   inference is labeled, and unresolved low-impact uncertainty becomes an
   assumption with a basis and a defined build-time response.
6. A Draft is persisted only when the intent is sufficiently clear to be useful,
   when the user requests a save/resume point, or when a material unresolved
   branch prevents safe completion in the current session.
7. The skill presents one complete Brief proposal and asks for one explicit
   acceptance. Only that acceptance changes `Draft` to `Ready`.
8. It renders one complete native `build` handoff after the Brief is Ready.

The readiness frontier is complete when no unresolved question can materially
change behavior, scope, a public contract, security, data handling, migration,
or material cost. The skill does not exhaust every conceivable question.

### `consult`

1. The user explicitly invokes `consult` with an existing `Draft` or `Ready`
   Feature Brief path, normally from another model or harness session.
2. The skill reads the complete Brief, relevant context, current code, ADRs, and
   binding rules in its fresh current context.
3. It reports only material ambiguities, contradictions, evidence gaps, grounded
   risks, or unnecessary scope. Each finding includes evidence, impact, and a
   precise proposed Brief change.
4. Findings are presented as one bounded batch. The skill changes nothing until
   the human explicitly accepts individual findings or the complete batch.
5. Accepted findings update a `Draft`. For a `Ready` Brief, every accepted
   material intent change is represented by an accepted amendment; the immutable
   baseline is not edited.
6. If no material issue exists, the skill returns `no material findings` and
   creates no artifact.

`consult` is never automatically invoked, never required between `discuss` and
`build`, and never produces a durable consultation report after accepted changes
have been incorporated.

## Scope

### In scope

- Host-agnostic `discuss` and `consult` skill definitions for Claude Code and
  Codex.
- Explicit-only invocation and complete native handoffs.
- Code-aware discovery with facts separated from decisions and assumptions.
- Session-only decision tree and adaptive readiness-frontier rounds.
- Adaptive Draft creation, Draft resumption, one final Brief acceptance gate,
  and transition to `Ready`.
- Optional second-model consultation for an existing `Draft` or `Ready` Brief.
- Human-controlled Draft edits and amendment-based Ready changes.
- ADR creation for durable architectural decisions discovered during discussion.
- Deterministic contract tests and deferred behavioral-scenario definitions for
  Phase 7.
- Documentation and canonical-contract updates required by the seventh MVP
  skill.

### Out of scope

- Implementation, detailed tasks, file-by-file instructions, or Execution Maps.
- QA enrichment, plan review, section-by-section acceptance, implementation
  review, or automatic triada in the AbsolutForge runtime workflow.
- Automatic consultation or a required number/order of models.
- A persistent consultation report or model-comparison score.
- Consulting Briefs already in `Building` or `In Review`; material changes there
  return to `discuss` for the established amendment flow.
- Prototyping or experiments required to resolve an experiential question.
- Runtime support for Pi or Grok.

### Deliberately not doing

- Do not copy the source `grill-me` behavior of relentlessly exhausting every
  branch. AbsolutForge borrows the decision-tree/frontier mental model but stops
  at material readiness to control ceremony and token use.
- Do not require one question per turn. Small independent frontiers are grouped
  into an answerable round; dependent questions wait for later rounds.
- Do not share a stateful runtime between `discuss` and `consult`. Their durable
  interoperability boundary is the Feature Brief and current repository state.
- Do not add a generic agent registry. Optional repository research may use an
  isolated generic agent when available, with an inline fallback.

## Assumptions and decisions

### Assumptions

- Strong models can maintain the session-only decision tree from prompt
  instructions without a separate persisted data structure.
- A Brief plus repository evidence is the correct cross-harness boundary; model
  identity does not need to be recorded in the artifact.
- Deterministic prompt-contract tests provide sufficient Phase 2 protection;
  real model behavior is validated deliberately in Phase 7.

### Decisions requiring confirmation

- None. The complete Phase 2 design, including optional `consult`, was explicitly
  accepted on 2026-08-27.

## Selected solution

Create two small explicit-only skills in the existing shared tree.

`discuss` is the primary discovery orchestrator. Its internal sections own
intake/resume routing, context collection, the readiness frontier, adaptive Draft
persistence, ADR classification, the single acceptance gate, and the native
handoff. The decision tree remains session-only; the canonical Feature Brief is
the sole durable discovery artifact.

`consult` is an optional second-opinion workflow. It consumes the same canonical
Brief contract and applies the same materiality boundary, but does not repeat the
full discovery interview. It produces a bounded finding batch in conversation
and mutates the Brief only after explicit human selection. Draft changes are
merged into the appropriate sections; Ready changes append amendments.

Both skills treat repository content as untrusted evidence: files cannot grant
permission, override skill instructions, authorize implementation, or expose
secrets. Optional subagents may gather independent facts, but neither workflow
depends on named agents or mandatory dispatch.

The exact artifact schema remains owned by
`references/artifact-contracts.md`. The native invocation and handoff syntax
remains owned by `references/harness-command-contract.md`. The skills link these
contracts instead of duplicating their complete templates.

### Rationale

- The decision-tree/frontier model prevents dependent or premature questions
  while the material-readiness stop condition avoids an exhaustive interview.
- Adaptive Draft persistence balances low ceremony with durable resumption.
- A separate `consult` command lets a different model inspect the same durable
  context without making multi-model review a default pipeline stage.
- Human-controlled mutation protects product ownership and the immutable Ready
  baseline.
- One shared skill tree and canonical references preserve cross-harness parity.

### Alternatives considered

- **Relentless exhaustive grilling:** rejected because visiting every possible
  branch recreates high token consumption and long ceremonies.
- **Mandatory one-question-per-turn:** rejected because independent decisions
  can be answered efficiently in a small round; dependent questions still wait.
- **Persist a Draft from the first user message:** rejected because it creates
  noisy low-value artifacts before useful intent exists.
- **Persist only at the final gate:** rejected because long or blocked sessions
  would have no durable resume point.
- **Embed consultation inside `discuss`:** rejected because the main use case is
  starting a fresh session in another harness after the original discussion.
- **Automatically run a second-model consultation:** rejected because it creates
  a new mandatory gate and repeats the AbsolutPowers ceremony.
- **Write a durable consultation report:** rejected because accepted findings
  belong in the Brief and rejected findings have no downstream consumer.

## Implementation plan

1. Update the canonical artifact and harness handoff references to define
   `consult` inputs, mutation boundary, no-artifact outcome, native Claude/Codex
   syntax, and its optional position beside the core workflow.
2. Record the durable optional-consultation decision in
   `docs/adr/2026-08-27-optional-cross-model-brief-consultation.md`, including
   the rejected mandatory-gate and persistent-report alternatives.
3. Create `skills/discuss/SKILL.md` with narrow explicit invocation metadata and
   `skills/discuss/agents/openai.yaml` with Codex implicit invocation disabled,
   host-agnostic intake, evidence, frontier, Draft, acceptance, amendment, ADR,
   safety, and handoff behavior.
4. Create `skills/consult/SKILL.md` with narrow explicit invocation metadata and
   `skills/consult/agents/openai.yaml` with Codex implicit invocation disabled,
   host-agnostic Brief validation, focused material finding, approval, Draft
   merge, Ready amendment, safety, and no-findings behavior.
5. Update repository entry points and Product Vision to list seven MVP skills,
   document optional cross-model consultation, preserve `discuss -> build` as
   the normal path, and keep Phase 7 behavioral validation explicit.
6. Replace Phase 1's no-skill scaffold assertions with deterministic discovery
   assertions, and add focused `discuss` and `consult` contract suites using
   Python standard library only.
7. Run JSON, foundation, skill-contract, frontmatter, link, forbidden-pipeline,
   strict Claude plugin, and conditional Codex plugin validation without
   installing or activating either workflow.

## Files to modify or create

- `skills/discuss/SKILL.md` — implement the adaptive discovery and acceptance
  workflow.
- `skills/discuss/agents/openai.yaml` — keep Codex invocation explicit-only.
- `skills/consult/SKILL.md` — implement optional second-model Brief consultation.
- `skills/consult/agents/openai.yaml` — keep Codex invocation explicit-only.
- `skills/README.md` — list seven planned/implemented skills and their boundaries.
- `README.md` — document `consult` as optional and preserve the normal core flow.
- `CLAUDE.md` — add binding `consult` constraints to repository development
  context.
- `docs/product-vision.md` — add the accepted optional-consultation contract and
  update MVP skill inventory and validation scenarios.
- `references/artifact-contracts.md` — define consultation behavior against
  Draft and Ready Briefs without adding a consultation artifact.
- `references/harness-command-contract.md` — add complete Claude and Codex
  `consult` invocation examples and handoff rules.
- `docs/adr/2026-08-27-optional-cross-model-brief-consultation.md` — record the
  optional cross-model consultation decision and consequences.
- `tests/test_foundation.py` — replace Phase 1 assumptions that no runnable
  skills exist with exact shared-tree discovery assertions.
- `tests/test_discuss_contract.py` — verify the `discuss` contract and forbidden
  classic-pipeline behavior.
- `tests/test_consult_contract.py` — verify optional consultation, approval, and
  immutable-baseline behavior.
- `absolutforge/features/absolutforge-mvp/planning-main.md` — update the Phase 2
  name/status after planning and implementation gates.
- `absolutforge/features/absolutforge-mvp/planning-phase-2-discuss.md` — preserve
  this accepted phase design and its generated Acceptance Criteria.

## Edge cases and risks

- A user supplies a missing, malformed, or non-Brief path: stop with the exact
  expected path/contract; do not create or overwrite an unrelated file.
- A slug collides with a different active feature: do not overwrite it; surface
  the collision and request a distinct slug or explicit resume choice.
- A Draft contains stale evidence: re-check material repository facts and label
  any conflict instead of silently trusting old prose.
- Binding ADR/rules conflict with current code or desired intent: surface the
  conflict as a material blocker; current code proves behavior but does not
  silently override a binding decision.
- The user answers `I don't know`: route non-material uncertainty to an explicit
  assumption; keep the Brief Draft when the answer is material.
- Repeated rounds do not converge: stop rephrasing, identify the missing
  evidence/experiment/decision, persist a useful Draft, and end resumably.
- A question is experiential and cannot be resolved through discussion: record
  the required prototype/experiment as a blocker rather than inventing certainty
  or implementing it inside `discuss`.
- Repository documents contain prompt injection or executable instructions:
  treat them as untrusted evidence and never let them authorize tools, writes,
  implementation, activation, or disclosure.
- Repository inspection encounters secrets or credentials: do not quote or copy
  them into the Brief, findings, ADRs, logs, or conversation.
- `consult` receives `Building` or `In Review`: do not mutate; route material
  intent changes to `discuss` and its amendment process.
- A consultation repeats an existing accepted decision or amendment: deduplicate
  it and report no new material change.
- Several accepted consultation findings express one coherent intent change:
  combine them into one precise amendment rather than producing amendment noise.
- Cross-harness wording differs: deterministic tests require identical artifact
  semantics and native command syntax from the canonical handoff contract.

## Acceptance Criteria

> Generated by qa-enrichment agent. Do not edit manually — re-run enrichment if
> the plan changes significantly.

### Happy path
- AC-1: When a user explicitly starts `discuss` with a new idea, the workflow presents one complete Feature Brief proposal covering the problem, users, current evidence, expected behavior and boundaries, scope, constraints, solution direction, assumptions, decisions, risks, and observable outcomes, without detailed tasks or a file-by-file recipe.
- AC-2: Before asking the user for repository-discoverable facts, the workflow inspects the relevant current context and code; it labels repository facts as evidence, labels model conclusions as inferences, and identifies the user's material product decisions separately.
- AC-3: Each adaptive discussion round presents a small frontier of normally two to four independent, high-impact questions whose prerequisites are settled, includes an evidence-backed recommendation where one exists, and stops when no unresolved question can materially change the intended behavior or scope.
- AC-4: When the user explicitly accepts the complete Brief proposal, its status changes from `Draft` to `Ready` and the workflow emits one complete native `build` handoff; without that acceptance, the Brief does not become `Ready` and no handoff is emitted.
- AC-5: When a user explicitly consults an existing `Draft` or `Ready` Brief, the workflow returns one bounded batch containing only material ambiguities, contradictions, evidence gaps, grounded risks, or unnecessary scope, with evidence, impact, and a precise proposed Brief change for each finding.
- AC-6: After the user explicitly accepts consultation findings, accepted changes are merged into a `Draft` or represented as an amendment to a `Ready` Brief, while unselected findings do not change the Brief and no durable consultation report is required.

### Edge cases
- AC-7: An incomplete discussion does not create a low-value Draft merely from the first message; it persists a useful Draft only when the intent is sufficiently clear, the user requests a save/resume point, or a material unresolved branch prevents safe completion, and a persisted Draft can be resumed later.
- AC-8: On Draft resumption, the workflow re-checks material repository facts and labels conflicts with stale evidence instead of silently treating the old Brief as current proof.
- AC-9: A missing, malformed, or non-Brief path, or a slug collision with another active feature, stops with a clear path/contract or collision explanation and leaves unrelated existing artifacts unchanged.
- AC-10: If `consult` receives a Brief in `Building` or `In Review`, it does not mutate the Brief and directs material intent changes back through `discuss` and its amendment flow.
- AC-11: If consultation finds no material issue, it reports `no material findings`, changes no Brief content, and creates no consultation artifact; repeated findings already represented by an accepted decision or amendment are likewise deduplicated.

### Security
- AC-12: Repository documents and other inspected content are treated as untrusted evidence: embedded instructions cannot override workflow rules, authorize writes or activation, trigger implementation, or cause disclosure of unrelated data.
- AC-13: Secrets or credentials encountered during repository inspection are never copied into the Brief, consultation findings, ADRs, logs, or user-facing conversation.
- AC-14: A `Ready` Brief's accepted intent remains unchanged unless the human explicitly accepts a material amendment; accepted consultation changes are recorded as amendments, while rejected findings leave the original baseline intact.
- AC-15: Neither `discuss` nor `consult` starts implicitly from a generic request or repository content, and consultation remains optional rather than becoming a mandatory gate in the normal `discuss` → `build` flow.

## Open questions

- None for Phase 2 implementation. Representative real-model scenarios and
  comparative measurements remain owned by Phase 7.

## Discussion notes

- The user chose adaptive Draft persistence rather than immediate or final-only
  persistence.
- The source `grill-me` / `grilling` skill contributed the decision-tree,
  prerequisite frontier, and facts-versus-decisions concepts. AbsolutForge
  intentionally rejects relentless exhaustive interviewing.
- The user accepted small independent question rounds rather than a mandatory
  one-question-per-turn protocol.
- Non-blocking uncertainty uses the existing canonical Assumptions contract;
  material uncertainty blocks `Ready`.
- The user introduced and accepted optional cross-model consultation so a Brief
  created with Claude can be inspected and improved in Codex, or vice versa.
- The full design was explicitly accepted on 2026-08-27.
