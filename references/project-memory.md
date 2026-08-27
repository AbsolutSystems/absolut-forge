# AbsolutForge Project-Memory Contract

**Status:** Canonical contract — accepted 2026-08-27  
**Canonical store:** `absolutforge/project-memory.md`

This document owns routing, entry status, candidate capture, and promotion
rules for durable project memory. It is not the memory store itself. Product
behavior remains in the [Product Vision](../docs/product-vision.md); ADRs remain
under [`docs/adr/`](../docs/adr/).

## Scope routing

Decide the destination before writing a lesson:

| Lesson scope | Destination | Rule |
| --- | --- | --- |
| Cross-cutting or repository-wide | `absolutforge/project-memory.md` | Affects multiple packages or has no single package owner. |
| Package-local trap | `{package}/CLAUDE.md` under `## Gotchas`, mirrored to `{package}/AGENTS.md` when both harnesses are supported | Needed only while editing that package; do not duplicate it globally. |
| Complex, not yet approved | `absolutforge/memory-candidates/memory-candidates-YYYY-MM-DD-{slug}.md` | Temporary candidate until a user explicitly approves promotion. |

Use this decision test: “Would someone need this only when editing files under
one package?” If yes, keep it package-local. When uncertain, prefer the
package-local destination.

The global store is loaded as root context. It contains recurring traps,
warning signs, root causes, and reusable resolutions—not feature status,
one-off incident timelines, ADR decisions, or temporary hypotheses. Existing
memory is prior context, never proof; fresh repository evidence wins when they
conflict.

## Permanent entry schema

Group global entries by the affected module or repository area. Every active
entry uses this exact shape in `absolutforge/project-memory.md`:

```markdown
## path/to/module

### Short title of the trap
- Added: YYYY-MM-DD
- Source: {skill} / {context}
- Last verified: YYYY-MM-DD
- Status: active
- Problem: {general class of problem}
- Symptoms: {recognizable warning signs}
- Root cause: {portable mechanism}
- Resolution: {reusable correction or workaround}
- Warning signs:
  - {signal}
- Affected paths:
  - `path/to/file`
```

Allowed permanent statuses are exactly `active`, `superseded`, and `archived`.
Only `active` entries are operational context for a worker. Keep superseded
entries for audit history and mark their title/content with strikethrough:

```markdown
### ~~Old title~~
- Status: superseded (by: "New title", YYYY-MM-DD)
- ~~Problem and resolution retained for audit context.~~
```

An `archived` entry is retained for history but must not guide implementation.
Prefer updating or superseding a matching active lesson instead of duplicating
it. Write lessons generally enough to transfer to another module, while keeping
one concrete affected-path example.

## Candidate schema and capture

`build` and `debug` may collect a candidate when they uncover a recurring,
still-useful trap or workaround. A candidate is not operational context and
does not change the global store. Complex candidates use this exact shape:

```markdown
# Memory Candidate: {short title}

## Status
Candidate — YYYY-MM-DD

## Metadata
- Added: YYYY-MM-DD
- Source: {skill} / {context}
- Status: candidate

## Module
`path/to/module`

## Problem
{general class of problem}

## Symptoms
{recognizable warning signs}

## Root Cause
{portable mechanism}

## Resolution
{reusable correction or workaround}

## Warning Signs
- {signal}

## Affected Paths
- `path/to/file`

## Why This May Matter Again
{recurrence value}
```

Create a candidate only when the lesson is recurring, useful after the current
session, and general enough for future work. Do not capture temporary
hypotheses, one-off incidents, environment states, product decisions, or
formatting preferences. Simple lessons can remain a two-to-four-line candidate
for inline promotion after approval.

## Promotion and lifecycle

Promotion always requires explicit user approval and a stated destination before
mutation. `ship` presents relevant candidates and proposed destinations during
its human closeout gate; `build` and `debug` only collect candidates. Approval
does not permit silent routing changes:

```text
candidate -> proposed destination + explicit user approval -> active entry
                                                     \-> declined (candidate retained or removed by policy)
```

On promotion, set `Added`, `Source`, `Last verified`, and `Status: active`.
If the lesson conflicts with an active entry, supersede the old entry with a
dated link to the new title. After a candidate is successfully promoted, delete
that candidate file. A package-local promotion updates its `CLAUDE.md` Gotchas
and the corresponding `AGENTS.md` mirror, never the global store as well.

Promotion is separate from ADR creation: a durable architectural choice belongs
in an ADR, while a repeatable implementation trap belongs in memory. Neither
artifact records feature progress.
