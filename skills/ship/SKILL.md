---
name: ship
description: "Explicitly close a review-complete AbsolutForge feature into durable documentation and one local commit, for either autonomous or planned Build strategy."
---

# Ship

Read `../../references/artifact-contracts.md` and `../../references/verification-doctrine.md` before evaluating the closeout gate.

Require a matching `In Review` Brief and `Complete` Review with decision `Ready for ship` and no open BLOCKING finding. Require the branch still points at the Reviewed revision and source state remains clean. Revalidate that final Build Evidence satisfies the delivery gate in `../../references/artifact-contracts.md`; refuse Ship if it is stale, structurally incomplete, or missing required verification proof even when Review mislabeled the defect as `FOLLOW-UP`.

Ship never backfills Build Evidence, changes implementation or reclassifies Review findings. Return a Build-owned evidence defect to the recorded builder and an incomplete or inconsistent Review to `review`. Valid FOLLOW-UP findings do not block Ship and are preserved in the Feature Record. Findings resolved `open` or `deferred` are also indexed in `absolutforge/follow-ups.md`; `fixed` and `accepted` findings are not actionable register entries.

Prepare a closeout preview before mutation. The preview includes the Feature Record, applicable family-manifest change, applicable follow-up-register entries, active-artifact cleanup, memory candidates, exact staging set and local conventional commit message. Ask explicitly whether to generate the optional HTML executive summary and whether to promote each durable memory candidate.

After approval, create `absolutforge/archives/{slug}/feature-record.md`. Preserve original intent separately from as-built result, accepted amendments, Build strategy, planned methodology, verification, Review findings/follow-ups, durable knowledge and the Brief's exact Feature-family metadata. Treat a historical Brief without family metadata as `standalone`; never infer family identity from its branch or slug.

For a non-standalone member, create or update `absolutforge/archives/families/{family-slug}/feature-family.md` under the canonical manifest contract. Append the shipped outcome and relative Feature Record link without moving any existing archive. Validate both directions of membership and refuse family-name/slug conflicts, duplicate records or broken links.

Create `absolutforge/follow-ups.md` when the first actionable follow-up ships. Allocate the next never-reused global `FU-{NNN}` for every `FOLLOW-UP` resolved `open` or `deferred`, copy only its impact and smallest sensible next action, and identify its archived Feature Record plus stable Review finding ID. Reuse an identical source entry on retry and refuse conflicting or duplicate source tuples. Do not assign priority, owner or deadline, and do not treat registration as scope acceptance.

For autonomous Build, consolidate useful execution-map/checkpoint facts. For planned Build, read and remove the active `implementation-plan.md`, and consolidate plan revision count, completed task outcomes, material plan changes, routing/escalation summary without provider identity, and final integration verification. For delegated methodology also record that implementation remained executor-owned and whether any dispatch failure or correction materially affected delivery, never provider identity or raw worker dialogue. When closing an already-complete legacy TDD feature, preserve its recorded task modes and concise cycle evidence as historical data.

Read `consult-{slug}.md` before removing it and consolidate it to the Feature Record contract in `../../references/artifact-contracts.md`: which artifacts were consulted, and each finding accepted by the owning context that changed the delivered feature, traced through its Brief amendment or `PC-` plan entry. Consulted with none accepted is still recorded. Nothing else from the report survives.

Validate the Feature Record, applicable family manifest and applicable follow-up-register changes as one closeout set before staging. Remove active Brief, execution map or implementation plan, consultation report, save and review artifacts as applicable. Stage only approved paths and create one local commit. Never push, create a PR, merge, deploy or rewrite history.
