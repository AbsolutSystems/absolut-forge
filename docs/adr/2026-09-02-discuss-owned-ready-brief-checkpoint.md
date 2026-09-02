# ADR: Discuss-owned Ready Brief checkpoint

**Date:** 2026-09-02  
**Status:** Accepted

## Decision

Treat explicit acceptance of the complete Feature Brief as authorization for `discuss` to set it to `Ready` and immediately create one local acceptance commit. The commit contains only the canonical `absolutforge/features/{slug}/feature-brief.md` and uses `git commit --only` or an equivalent path-scoped Git operation so unrelated staged or dirty work remains untouched.

Before requesting final acceptance, Discuss requires a non-detached intended feature branch. After committing, it verifies both the Ready content and the commit's exact path set and reports the revision. It reuses an identical Ready Brief already committed at HEAD rather than creating an empty commit.

Commit or verification failure blocks Build handoff but does not discard the accepted Brief. Discuss reports the blocker and never amends history, pushes, or includes another path to force the checkpoint through.

## Consequences

- The developer moves directly from accepted intent to Build strategy selection without a manual commit step.
- Build retains its existing requirement for a clean worktree and committed Ready baseline.
- Unrelated local changes may remain outside the acceptance commit, but they must be resolved before Build starts.
- An optional consultation report remains separate evidence and is never swept into the Ready checkpoint.
