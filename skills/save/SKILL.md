---
name: save
description: "Explicitly persist concise, secret-redacted resume context for an active Building feature while preserving its selected autonomous or planned Build strategy."
---

# Save

Accept one canonical `Building` Feature Brief. Read Build start evidence and determine the recorded strategy and planned methodology. Validate the current branch/base revision and actual worktree.

For planned Build at a clean completed-task boundary, explain that the committed plan and Git state already support direct resume through the matching planned builder; do not create redundant save context unless the human still requests it. Save is useful for a mid-task or otherwise unresolved stop, including an unfinished delegated-worker correction.

Write only `absolutforge/features/{slug}/save-{slug}.md` using the Save contract. Include strategy, planned methodology, execution artifact path, verified completed work, current work, next action and open items. For planned Build include current plan revision/task, any outstanding delegated-worker correction, and any blocked task or unresolved intent change; for autonomous Build include current outcome/map/checkpoint facts.

Save does not preserve dirty source by itself and never commits, stashes, switches branches, pushes or changes lifecycle state.
