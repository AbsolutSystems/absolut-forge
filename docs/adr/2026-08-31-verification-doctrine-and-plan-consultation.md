# ADR: Verification doctrine and cross-session plan consultation

**Accepted:** 2026-08-31

## Decision

Add one host-agnostic verification doctrine binding on both Build strategies, and allow a not-yet-executed implementation plan to be consulted from a separate session.

`references/verification-doctrine.md` defines what focused and final verification mean. Changed observable behavior lands with automated tests inside the outcome or task that changed it, or with a recorded exemption naming the reason and the observable check performed instead. Existing assertions are never weakened to reach green. At finish, the feature's primary accepted path is exercised at integration level once, or the reason and the closest whole-feature check performed are recorded.

`consult` gains a second subject: `implementation-plan.md` at `Ready`, or at `Needs Replan` once the replan entry exists. It writes one report at `absolutforge/features/{slug}/consult-{slug}.md` and nothing else. The orchestrator reads the report back, disposes each `C-` finding, and remains the sole author of every plan mutation. The plan tracks only whether a consultation question is open, through `## Consultation` entries in two states: `awaiting` holds the plan, `settled` releases it, and no entry means nothing was asked.

## Rationale

Two gaps closed.

`focused verification` was undefined, so a Build could mark an outcome complete on inspection alone and Review had no stated bar to judge test value against. Making tests part of stage completion, with a recorded exemption as the only escape, gives Build a duty and Review an evidence-based finding instead of a taste argument. The doctrine deliberately excludes coverage targets, speculative edge cases and test theater, so the rule cannot be satisfied by ceremony.

Plan validation in `build-planned` was self-assessment by the context that wrote the plan: the same model judging its own decomposition, routing and coverage before spending delegated compute on it. A second opinion is worth most exactly there, and worth most from a different model family, which forces the result through a durable artifact rather than conversation state.

## Alternatives rejected

Consulting an `execution-map.md`: autonomous Build has no delegation surface for a plan critique to protect, and the map is optional.

Requiring consultation: it would become ceremony on small plans and dilute the signal. It is offered only when the plan carries material risk, and never blocks a plan the orchestrator can own directly.

Richer consultation state on the plan (`not offered`, `offered`, `declined`, `consulted` as distinct control values): the only decision a resuming context must make is whether to hold or continue. Encoding four values invited state the model would have to reason about at every resume; the detail now lives inside the `settled` text, where it is a record rather than control flow.

Letting `consult` edit the plan on human acceptance, as Brief mode may edit a Brief: a plan is implementation evidence owned by one orchestrator, and a second session editing it would split ownership of the task graph while execution state depends on it.
