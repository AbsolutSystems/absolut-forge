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

When such a worker primitive exists, apply the same capability tiers, minimum-context package, write boundaries, and orchestrator validation as the shared planned contract. Standard methodology may use a fully disjoint parallel wave only when the extension supports isolation.

`build-planned-delegated` requires a trusted extension that can request one explicitly configured fixed executor and reasoning profile. Without it, refuse the methodology before Build start. With it, dispatch one fresh bounded task at a time and keep every production/test edit in that executor; never fall back to direct primary-context implementation.

## Clean-context Review

Pi's normal Review handoff uses a fresh top-level session rather than an unavailable native subagent. After Build reaches `In Review` and commits its handoff, instruct the human to run:

```text
/new
/skill:review absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md
```

The post-`/new` context is the fresh read-only reviewer context and may record Review mode `fresh`. It must rehydrate only from the Brief, completed execution artifact, Git range, source, and tests; it must not receive implementation conversation or conclusions.

If a trusted extension provides a fresh reviewer primitive, dispatch exactly one generic read-only reviewer instead. If Review is run in the Build session without either `/new` or a fresh worker, use the shared inline fallback and label it `advisory (not fully isolated)`.
