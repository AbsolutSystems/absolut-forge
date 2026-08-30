---
name: review
description: "Explicitly run one independent evidence-based whole-feature review after either autonomous or planned Build. Use only when the user invokes AbsolutForge review with matching Brief and review paths."
disable-model-invocation: true
---

# Review

Review is common to both Build strategies. Require an `In Review` Brief, valid append-only Build start/evidence, a resolvable `base_commit`, and a clean committed source worktree (the active `review.md` is the only permitted uncommitted workflow artifact).

Read the immutable Brief/amendments, linked ADRs/rules/memory, Build Evidence, current source/tests and the selected execution artifact when present:

- autonomous -> optional `execution-map.md`;
- planned -> required completed `implementation-plan.md`.

Execution artifacts are supporting evidence only. The Brief is intent authority and `base_commit..HEAD` is implementation truth.

Request exactly one fresh generic read-only reviewer when the harness can provide it. Prefer an independent model family when practical, but do not make provider identity part of the contract. Inline fallback must be labelled `advisory (not fully isolated)`.

Check intent/scope fidelity, correctness, concrete edge cases, security/data integrity, test value, regressions/compatibility, unintended scope, missing critical docs and diff garbage. Findings are only `BLOCKING` or `FOLLOW-UP`, with stable IDs, evidence, impact and smallest sensible correction.

When no BLOCKING finding remains, record exact reviewed HEAD/range, set Review `Complete`, decision `Ready for ship`, and hand off to `ship`.

When blockers remain, return Brief status to `Building` and hand off to the strategy recorded in Build start evidence:

- `autonomous` -> `build`;
- `planned` -> `build-planned`.

A planned blocker should normally become a focused existing-task correction or an orchestrator-created replan entry; do not make Review mutate the plan itself. After two failed attempts on the same blocker or material scope expansion, escalate to the human rather than loop indefinitely.
