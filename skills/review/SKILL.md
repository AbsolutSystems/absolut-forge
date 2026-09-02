---
name: review
description: "Explicitly run one independent evidence-based whole-feature review after either autonomous or planned Build. Use only when the user invokes AbsolutForge review with matching Brief and review paths."
---

# Review

Review is common to both Build strategies and both planned methodologies. Require an `In Review` Brief, valid append-only Build start/evidence with consistent methodology, a resolvable `base_commit`, and a clean committed source worktree (the active `review.md` is the only permitted uncommitted workflow artifact).

Read `../../references/artifact-contracts.md`, `../../references/verification-doctrine.md`, and the active host mapping before selecting the fresh-reviewer mechanism.

Read the immutable Brief/amendments, linked ADRs/rules/memory, Build Evidence, current source/tests and the selected execution artifact when present:

- autonomous -> optional `execution-map.md`;
- planned -> required completed `implementation-plan.md`.

Execution artifacts are supporting evidence only. The Brief is intent authority and `base_commit..HEAD` is implementation truth.

Request exactly one fresh generic read-only reviewer when the harness can provide it. Prefer an independent model family when practical, but do not make provider identity part of the contract. Inline fallback must be labelled `advisory (not fully isolated)`.

Check intent/scope fidelity, correctness, concrete edge cases, security/data integrity, test value, regressions/compatibility, unintended scope, missing critical docs and diff garbage. Findings are only `BLOCKING` or `FOLLOW-UP`, with stable IDs, evidence, impact and smallest sensible correction.

Judge tests against the risk-based obligations in `../../references/verification-doctrine.md`. Raise a finding when an applicable primary, failure/boundary, state/data, seam-contract, or regression obligation is uncovered without an exemption; when assertions bind nothing the change produces; when current evidence lacks credible targeted mutation proof for a new or materially changed guard; or when an existing assertion was weakened without accepted Brief authority. Legacy evidence without the binding-proof field is not a finding by itself, but the test must still bind the delivered behavior on inspection. For methodology `tdd`, also validate that every behavior-changing task records credible ordered RED-GREEN-REFACTOR evidence under `../../references/planned-tdd-contract.md`. Review remains read-only: validate RED and mutation evidence against the tests and diff rather than recreating failures by changing production code.

Check the final Build Evidence entry against the evidence schema in `../../references/artifact-contracts.md`: a `Whole-feature path exercised` field that is absent, blank, or `not available` without both a reason and the closest whole-feature check actually performed is a finding, at the severity the evidence warrants.

A `consult-{slug}.md` report, when present, is context only and never enters the judgment: it is neither intent nor absolution. An accepted consult finding does not license a Brief deviation, and a rejected one is not a Review finding by itself.

When no BLOCKING finding remains, record exact reviewed HEAD/range, set Review `Complete`, decision `Ready for ship`, and hand off to `ship`.

When blockers remain, return Brief status to `Building` and hand off to the strategy recorded in Build start evidence:

- `autonomous` -> `build`;
- `planned` with methodology `standard` or a legacy missing field -> `build-planned`;
- `planned` with methodology `tdd` -> `build-planned-tdd`.

A planned blocker should become a new bounded corrective task recorded through a `PC-` plan entry; Review never mutates the plan itself. After two failed attempts on the same blocker or material scope expansion, escalate to the human rather than loop indefinitely.
