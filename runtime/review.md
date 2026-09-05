# Review Runtime

Use with [common](common.md) and active host reviewer mechanics. [Artifact contracts](../references/artifact-contracts.md) own eligibility, evidence schemas and findings. Review is one independent whole-feature judgment.

## Start from intent and implementation

Require matching canonical Brief/Review paths, an In Review Brief, consistent recorded strategy/methodology, resolvable base and clean committed source. Only the active review artifact may be uncommitted. Read accepted Brief/amendments, final Build Evidence, complete `base_commit..HEAD` and changed/new tests. Inspect relevant current implementations/callers as needed.

Do not preload implementation-plan.md, execution-map.md, consultation, all completion evidence or individual checkpoint diffs. Execution history supports judgment and never excuses a Brief violation. Load targeted history only for a referenced PC change, material decision ambiguity, cross-task inconsistency, ownership/lifecycle proof or a concrete finding. Validate planned completion from header/status without loading all task bodies. Recorded delegated methodology creates a concrete fixed-owner question: read the legacy contract and relevant task/commit evidence, including correction ownership.

Use exactly one fresh generic read-only reviewer when the host provides isolation, preferably another model family when practical. Provide the same bounded starting package; builder dialogue is not reviewer evidence. If isolation is unavailable, explicitly label the inline pass `advisory (not fully isolated)`. A different role name alone does not establish independence.

## Delivery gate first

Read artifact eligibility/evidence sections to validate structure and freshness. Final evidence includes every required nonblank current field, valid whole-feature path, green verification and the implementation state delivered. Later source/test changes make it stale; lifecycle-only and Review-artifact commits do not. Compilation/packaging alone does not exercise the primary path unless artifact production is accepted behavior.

A `not available` path record is valid only with a credible reason and closest whole-feature check performed. Missing, stale or incomplete delivery proof is BLOCKING even when logs or future documentation could reconstruct it. Review never backfills Build Evidence or repairs source/tests.

## Inspect behavior and tests

Map the complete diff to accepted Expected Outcomes. Inspect changed behavior, security/data integrity, applicable edges, compatibility, scope, critical documentation and diff garbage. Apply this test-value checklist:

- Accepted primary behavior covered?
- Applicable failure/boundary covered?
- Material state/data invariant covered?
- Owned seam contract covered when relevant?
- Fixed defect protected by regression guard?
- Assertions prove repository-owned observable behavior?

Consult [verification doctrine](../references/verification-doctrine.md) when classification, applicability or exemption is uncertain. Mock configuration, framework behavior, private helpers, incidental structure or insignificant counts do not discharge obligations. Mocks/fakes at external seams are valid when proving owned behavior or an accepted outbound contract. Existing assertions cannot be weakened without accepted intent authority. Judge committed green tests semantically; never edit production to force a failure.

Resolve missing facts through targeted code or historical sections. Consultation findings are neither automatic Review findings nor absolution. Accepted intent and implementation evidence determine judgment. Short context or a clean benchmark does not substitute for correctness.

## Record and route

Write only review.md and Brief lifecycle status. Never change execution artifacts, Build Evidence, source or tests. Use stable finding IDs with evidence, impact, smallest correction and resolution. BLOCKING requires correction or missing delivery proof before Ship; FOLLOW-UP requires no correction to this feature before Ship. Never downgrade failed gates to FOLLOW-UP.

With blockers, set Brief Building and return to `build`, which resumes the recorded strategy without selecting again: autonomous stays autonomous; planned standard/missing methodology stays standard; planned delegated retains legacy restrictions. Legacy tdd has no current builder: require a compatible older release or explicit clean Ready restart. Planned corrections become builder-owned PC tasks; Review never reopens the plan itself. After two failed attempts at the same blocker or material scope expansion, escalate to the human.

Without blockers, record exact reviewed HEAD/range, Review Complete and Ready for ship. Read [harness syntax](../references/harness-command-contract.md) and emit one resolved active-host continuation. Never invoke Ship without explicit authorization.
