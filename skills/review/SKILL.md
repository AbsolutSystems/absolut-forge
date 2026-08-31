---
name: review
description: "Explicitly run one independent evidence-based whole-feature review after either autonomous or planned Build. Use only when the user invokes AbsolutForge review with matching Brief and review paths."
---

# Review

Review is common to both Build strategies. Require an `In Review` Brief, valid append-only Build start/evidence, a resolvable `base_commit`, and a clean committed source worktree (the active `review.md` is the only permitted uncommitted workflow artifact).

Read the immutable Brief/amendments, linked ADRs/rules/memory, Build Evidence, current source/tests and the selected execution artifact when present:

- autonomous -> optional `execution-map.md`;
- planned -> required completed `implementation-plan.md`.

Execution artifacts are supporting evidence only. The Brief is intent authority and `base_commit..HEAD` is implementation truth.

Request exactly one fresh generic read-only reviewer when the harness can provide it. Prefer an independent model family when practical, but do not make provider identity part of the contract. Inline fallback must be labelled `advisory (not fully isolated)`.

Check intent/scope fidelity, correctness, concrete edge cases, security/data integrity, test value, regressions/compatibility, unintended scope, missing critical docs and diff garbage. Findings are only `BLOCKING` or `FOLLOW-UP`, with stable IDs, evidence, impact and smallest sensible correction.

Judge tests against `../../references/verification-doctrine.md`. Accepted behavior shipped with neither an automated test nor a recorded exemption is a finding, as is test theater, a test whose assertions bind nothing the change actually produces, or an existing assertion weakened or skipped without an accepted Brief basis. Judge that binding by reading the test against the diff; never revert production code to prove it, and leave the worktree clean. Do not raise findings demanding speculative edge cases or coverage targets the doctrine excludes.

Check the final Build Evidence entry against the evidence schema in `../../references/artifact-contracts.md`: a `Whole-feature path exercised` field that is absent, blank, or `not available` without both a reason and the closest whole-feature check actually performed is a finding, at the severity the evidence warrants.

A `consult-{slug}.md` report, when present, is context only and never enters the judgment: it is neither intent nor absolution. An accepted consult finding does not license a Brief deviation, and a rejected one is not a Review finding by itself.

When no BLOCKING finding remains, record exact reviewed HEAD/range, set Review `Complete`, decision `Ready for ship`, and hand off to `ship`.

When blockers remain, return Brief status to `Building` and hand off to the strategy recorded in Build start evidence:

- `autonomous` -> `build`;
- `planned` -> `build-planned`.

A planned blocker should normally become a focused existing-task correction or an orchestrator-created replan entry; do not make Review mutate the plan itself. After two failed attempts on the same blocker or material scope expansion, escalate to the human rather than loop indefinitely.
