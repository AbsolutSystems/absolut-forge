# Pi Primitive Mapping

Use native Pi file and shell primitives for repository inspection, edits, and verification. AbsolutForge is a Pi Package whose root manifest exposes the shared `skills/` tree; do not fork skill behavior for Pi.

## Registration and invocation

Install the repository as a local package:

```bash
pi install /absolute/path/to/absolut-forge
```

Pi discovers every `skills/*/SKILL.md` through the root `package.json`. Explicit skill invocation uses Pi's native form:

```text
/skill:{skill-name} {arguments}
```

Use `/reload` after local skill changes, or start a new session. Skill descriptions remain the guard against unintended implicit activation.

## Planned Build

Pi core has no native subagent primitive. Keep the invoking high-capability context as orchestrator and execute tasks directly unless the user has installed a trusted extension that exposes genuinely fresh bounded workers. Never pretend delegation occurred.

When such a worker primitive exists, send one Task Capsule with relevant accepted clauses, direct dependency facts and source/tests, never the whole Brief/plan/history or inherited orchestrator dialogue. Apply the same capability tiers, write boundaries, fresh-context isolation and orchestrator validation as the shared planned contract. Standard methodology may use a fully disjoint parallel wave only when the extension supports isolation.

New delegated starts are unavailable. A feature that records legacy delegated methodology resumes through `build` only when a trusted extension can still request its explicitly configured fixed executor and reasoning profile. Dispatch one fresh bounded task at a time and keep every production/test edit in that executor; otherwise stop at the clean boundary and never fall back to direct primary-context implementation.

## Clean-context Review

Pi's normal Review handoff uses a fresh top-level session rather than an unavailable native subagent. After Build reaches `In Review` and commits its handoff, instruct the human to run:

```text
/new
/skill:review absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
```

The post-`/new` context is the fresh read-only reviewer context and may record Review mode `fresh`. Its startup package is only the Brief and accepted amendments, final Build Evidence, `base_commit..HEAD` diff, and changed/new tests. Load plan or history lazily only for a concrete coverage, lifecycle, or legacy-ownership question; never preload implementation conversation or conclusions.

If a trusted extension provides a fresh reviewer primitive, dispatch exactly one generic read-only reviewer with the same bounded startup package instead. If Review is run in the Build session without either `/new` or a fresh worker, use that same bounded package inline and label it `advisory (not fully isolated)`.
