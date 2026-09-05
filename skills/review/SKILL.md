---
name: review
description: "Explicitly run one independent evidence-based whole-feature review after Build. Use only when the user invokes AbsolutForge review with matching Brief and review paths."
---

# Review

Use only with matching canonical Brief and Review paths. Read [runtime common](../../runtime/common.md), then the [review runtime](../../runtime/review.md), and the matching active-host reviewer mechanics in `../../references/`. These documents own the fresh read-only independence requirement, delivery gate, bounded evidence reads, findings, allowed writes, routing, and final continuation.

Keep the review independent: start from accepted intent, final Build Evidence, complete implementation diff, and changed/new tests. Do not preload execution history. For recorded delegated methodology, load its legacy contract and only the targeted ownership evidence the runtime requires. Write only the Brief lifecycle status and `review.md`; never repair implementation or Build evidence.

Read the artifact-contract eligibility and evidence sections for delivery-gate validation; load additional artifact sections for findings ambiguity. Load verification doctrine for uncertain test-value classification and the harness contract only when emitting the resolved Build or Ship continuation. A completed review must pass the delivery gate before it may return `Ready for ship`.
