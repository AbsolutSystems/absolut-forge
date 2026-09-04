---
name: ship
description: "Explicitly close a review-complete AbsolutForge feature into durable documentation and one local commit, for either autonomous or planned Build strategy."
---

# Ship

Read `../../references/artifact-contracts.md` and `../../references/verification-doctrine.md` before evaluating the closeout gate.

Require a matching `In Review` Brief and `Complete` Review with decision `Ready for ship` and no open BLOCKING finding. Require the branch still points at the Reviewed revision and source state remains clean. Revalidate that final Build Evidence satisfies the delivery gate in `../../references/artifact-contracts.md`; refuse Ship if it is stale, structurally incomplete, or missing required verification proof even when Review mislabeled the defect as `FOLLOW-UP`.

Ship never backfills Build Evidence, changes implementation or reclassifies Review findings. Return a Build-owned evidence defect to the recorded builder and an incomplete or inconsistent Review to `review`. Valid FOLLOW-UP findings do not block Ship and are preserved in the Feature Record.

Prepare a closeout preview before mutation. The preview includes archive files, active-artifact cleanup, memory candidates, exact staging set and local conventional commit message. Ask explicitly whether to generate the optional HTML executive summary and whether to promote each durable memory candidate.

After approval, create `absolutforge/archives/{slug}/feature-record.md`. Preserve original intent separately from as-built result, accepted amendments, Build strategy, planned methodology, verification, Review findings/follow-ups and durable knowledge.

For autonomous Build, consolidate useful execution-map/checkpoint facts. For planned Build, read and remove the active `implementation-plan.md`, and consolidate plan revision count, completed task outcomes, material plan changes, routing/escalation summary without provider identity, and final integration verification. For delegated methodology also record that implementation remained executor-owned and whether any dispatch failure or correction materially affected delivery, never provider identity or raw worker dialogue. When closing an already-complete legacy TDD feature, preserve its recorded task modes and concise cycle evidence as historical data.

Read `consult-{slug}.md` before removing it and consolidate it to the Feature Record contract in `../../references/artifact-contracts.md`: which artifacts were consulted, and each finding accepted by the owning context that changed the delivered feature, traced through its Brief amendment or `PC-` plan entry. Consulted with none accepted is still recorded. Nothing else from the report survives.

Remove active Brief, execution map or implementation plan, consultation report, save and review artifacts as applicable. Stage only approved paths and create one local commit. Never push, create a PR, merge, deploy or rewrite history.
