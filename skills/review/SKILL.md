---
name: review
description: "Explicitly run one independent evidence-based whole-feature review after either autonomous or planned Build. Use only when the user invokes AbsolutForge review with matching Brief and review paths."
---

# Review

Review is common to both Build strategies and current planned methodologies. Require an `In Review` Brief, valid append-only Build start/evidence with consistent methodology, a resolvable `base_commit`, and a clean committed source worktree (the active `review.md` is the only permitted uncommitted workflow artifact).

Read `../../references/artifact-contracts.md`, `../../references/verification-doctrine.md`, `../../references/harness-command-contract.md`, and the active host mapping before selecting the fresh-reviewer mechanism.

Read the immutable Brief/amendments, linked ADRs/rules/memory, Build Evidence, current source/tests and the selected execution artifact when present:

- autonomous -> optional `execution-map.md`;
- planned -> required completed `implementation-plan.md`.

Execution artifacts are supporting evidence only. The Brief is intent authority and `base_commit..HEAD` is implementation truth.

## Authority and delivery gate

Review may create or update `review.md` and change only the Feature Brief lifecycle status. It must not change production code, tests, an execution artifact, or Build Evidence. Inspection may validate recorded verification, but it never manufactures or backfills Build-owned evidence.

Before judging implementation quality, verify the final Build Evidence delivery gate in `../../references/artifact-contracts.md`. Treat every gate defect as `BLOCKING`, including:

- the final entry predates a later source or test change;
- a required current-schema field is absent or blank;
- `Whole-feature path exercised` is absent, invalid, or claims only compilation/packaging when that is not the accepted behavior.

A properly recorded `not available — {reason and closest whole-feature check}` value is not missing evidence; judge whether its reason and closest check are credible. Never downgrade a delivery-gate defect to `FOLLOW-UP` because the missing information might be reconstructed from logs, another entry, test inspection, or a future Feature Record.

Request exactly one fresh generic read-only reviewer when the harness can provide it. Prefer an independent model family when practical, but do not make provider identity part of the contract. Inline fallback must be labelled `advisory (not fully isolated)`.

Check intent/scope fidelity, correctness, concrete edge cases, security/data integrity, test value, regressions/compatibility, unintended scope, missing critical docs and diff garbage. Findings are only `BLOCKING` or `FOLLOW-UP`, with stable IDs, evidence, impact and smallest sensible correction.

Judge tests against the risk-based obligations and test-value rules in `../../references/verification-doctrine.md`. Raise a finding when an applicable primary, failure/boundary, state/data, seam-contract, or regression obligation is uncovered without an exemption; when assertions do not establish an observable business result, state transition, error, or owned seam contract; when a test mainly verifies mock setup or insignificant call counts, framework/library behavior, dependency-injection wiring, private helpers, or incidental implementation structure; or when an existing assertion was weakened without accepted Brief authority. Mocks are acceptable at external seams when assertions still establish repository-owned behavior or when the outbound interaction is itself an accepted contract. For methodology `delegated`, also validate from the plan and commits that source/test changes were executor-owned and corrections were not silently implemented by the orchestrator. Review remains read-only and judges the committed green tests against the implementation diff; it never changes production code to force a failure.

Classify findings deterministically: `BLOCKING` requires a correction or missing delivery proof before Ship; `FOLLOW-UP` requires no correction to this feature before Ship. Never use `FOLLOW-UP` to waive a delivery gate.

A `consult-{slug}.md` report, when present, is context only and never enters the judgment: it is neither intent nor absolution. An accepted consult finding does not license a Brief deviation, and a rejected one is not a Review finding by itself.

When no BLOCKING finding remains, record exact reviewed HEAD/range, set Review `Complete`, decision `Ready for ship`, and hand off to `ship`.

When blockers remain, return Brief status to `Building` and hand off to the strategy recorded in Build start evidence:

- `autonomous` -> `build`;
- `planned` with methodology `standard` or a legacy missing field -> `build-planned`;
- `planned` with methodology `delegated` -> `build-planned-delegated`;
- `planned` with legacy methodology `tdd` -> no current builder; require a compatible older release or explicit abandonment and restart.

A planned blocker should become a new bounded corrective task recorded through a `PC-` plan entry; Review never mutates the plan itself. After two failed attempts on the same blocker or material scope expansion, escalate to the human rather than loop indefinitely.

Whenever Review reaches a valid workflow handoff, report the eligible next skill and canonical artifact paths, then end with the one copy-ready active-host continuation prompt required by `harness-command-contract.md`. Resolve the real paths and do not merely name the skill or show multiple host variants. With blockers, invoke the recorded builder with only the canonical Brief path; when ready for Ship, invoke `ship` with the Brief and Review paths. Emitting the prompt does not invoke the next stage. Do not invoke `ship` unless the human explicitly invoked it or expressly authorized this request to continue through Ship.
