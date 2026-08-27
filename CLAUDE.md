# AbsolutForge Development Context

AbsolutForge is a standalone intent-driven development workflow for Claude Code
and Codex. It is not an AbsolutPowers light mode and must not silently inherit the
classic detailed-task and repeated-gate pipeline.

## Required reading order

Before planning or implementing work in this repository:

1. Read `docs/product-vision.md` completely. It is the durable source of truth
   for accepted product behavior and cross-phase contracts.
2. Read `absolutforge/features/absolutforge-mvp/planning-main.md` for the epic
   roadmap, dependencies, and current phase statuses.
3. Read only the phase document relevant to the current task.
4. Read applicable ADRs and active project-memory entries when they exist.

Do not reconstruct product decisions from memory or from AbsolutPowers. Current
repository documents take precedence.

## Current state

The repository is in design/planning state. The plugin skills and manifests have
not been implemented yet. Phase documents are stubs until explicitly planned.

## Binding product constraints

- Core workflow: `discuss -> build -> review -> ship`.
- Standalone tools: `debug` and `tech-debt`.
- One host-agnostic skill tree; Claude Code and Codex only for MVP.
- No SessionStart hook or globally injected pipeline context.
- Core skills are explicit-only; only `debug` may auto-trigger for a concrete
  failure.
- No `generate-tasks`, QA-enrichment gate, plan/task/phase review, implementation
  review, or automatic triada in the standard workflow.
- Feature intent becomes immutable at `Ready`; material change requires an
  explicit amendment.
- `build` owns optional outcome planning and verification.
- `review` is one independent fresh-context review using `BLOCKING` and
  `FOLLOW-UP`.
- `ship` runs after review fixes and creates a Feature Record plus human-facing
  Executive Summary HTML.
- ADR and project-memory behavior must follow `docs/product-vision.md`.
- AbsolutPowers and AbsolutForge should not be enabled together as overlapping
  workflows.

## Planning discipline

`planning-main.md` is a lightweight roadmap, not an implementation plan. Plan one
phase at a time and preserve accepted cross-phase contracts from the Product
Vision. Do not fill future phase stubs speculatively.

No implementation should begin until the relevant phase design is explicitly
accepted.

## Repository language

Use English for technical source, skill bodies, schemas, and public product
documentation. User-facing conversational prompts may follow the user's language.

