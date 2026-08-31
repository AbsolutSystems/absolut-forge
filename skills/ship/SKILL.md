---
name: ship
description: "Explicitly close a review-complete AbsolutForge feature into durable documentation and one local commit, for either autonomous or planned Build strategy."
---

# Ship

Require a matching `In Review` Brief and `Complete` Review with no open BLOCKING finding. Require the branch still points at the Reviewed revision and source state remains clean.

Prepare a closeout preview before mutation. The preview includes archive files, active-artifact cleanup, memory candidates, exact staging set and local conventional commit message. Ask explicitly whether to generate the optional HTML executive summary and whether to promote each durable memory candidate.

After approval, create `absolutforge/archives/{slug}/feature-record.md`. Preserve original intent separately from as-built result, accepted amendments, Build strategy, verification, Review findings/follow-ups and durable knowledge.

For autonomous Build, consolidate useful execution-map/checkpoint facts. For planned Build, read and remove the active `implementation-plan.md`, and consolidate plan revision count, completed task outcomes, material deviations/replans, routing/escalation summary without provider identity, and final integration verification.

Read `consult-{slug}.md` before removing it and consolidate it to the Feature Record contract in `../../references/artifact-contracts.md`: which artifacts were consulted, and each accepted finding that changed the delivered feature with the amendment or plan revision it produced. Consulted with none accepted is still recorded. Nothing else from the report survives.

Remove active Brief, execution map or implementation plan, consultation report, save and review artifacts as applicable. Stage only approved paths and create one local commit. Never push, create a PR, merge, deploy or rewrite history.
