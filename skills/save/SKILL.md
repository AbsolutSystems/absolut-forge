---
name: save
description: "Explicitly persist concise, secret-redacted resume context for an active Building feature while preserving its selected autonomous or planned Build strategy."
disable-model-invocation: true
---

# Save

Accept one canonical `Building` Feature Brief. Read Build start evidence and determine the recorded strategy. Validate the current branch/base revision and actual worktree.

Write only `absolutforge/features/{slug}/save-{slug}.md` using the Save contract. Include strategy, execution artifact path, verified completed work, current work, next action and open items. For planned Build include current plan revision/task, any open deviation, and the fact that the plan's `## Consultation` carries an `awaiting` entry for that revision, pointing at it rather than restating the command it already holds; for autonomous Build include current outcome/map/checkpoint facts.

Save does not preserve dirty source by itself and never commits, stashes, switches branches, pushes or changes lifecycle state.
