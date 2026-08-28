# AbsolutForge

AbsolutForge is an intent-driven delivery workflow for Claude Code and Codex.
It gives a coding model a precise, accepted product intent, durable decisions,
and clear outcome boundaries, then lets it implement and verify the complete
change before one independent review.

**Release candidate.** The RC includes the complete core workflow:

```text
discuss -> build -> review -> ship
```

It also includes the optional `consult` workflow for a bounded second opinion,
the guardian `debug` workflow for concrete failures, and the explicit-only,
read-only `tech-debt` audit.

## What the workflow does

AbsolutForge controls the delivered result instead of prescribing every coding
step. The human owns product decisions; the model owns local implementation
choices within the accepted boundary.

- `discuss` clarifies the goal, inspects the repository, and creates one
  accepted Feature Brief.
- `consult` pressure-tests a `Draft` or `Ready` Feature Brief. It is optional,
  explicit, bounded to one finding batch, and changes nothing without human
  approval.
- `build` implements the accepted Brief, maintains optional durable outcome
  state, and runs focused and final verification.
- `save` captures concise Build context before pausing or switching feature
  branches; it does not preserve dirty code by itself.
- `load` validates a saved Build context and hands the feature back to `build`.
- `review` performs one fresh, read-only, evidence-based review of the complete
  change and records only `BLOCKING` and `FOLLOW-UP` findings.
- `ship` closes a review-complete feature into durable documentation and one
  local commit after a single approval preview.
- `debug` diagnoses a concrete failure from evidence and implements a fix only
  when explicitly requested and the expected behavior is unambiguous.
- `tech-debt` statically audits a repository or bounded path and returns a
  prioritized, evidence-backed remediation backlog without changing files.

Core skills, `consult`, `save`, `load`, and `tech-debt` are explicit-only. Only `debug` may
auto-trigger, and only for a concrete failure. There is no SessionStart hook,
global workflow prompt, MCP server, or generic automatic workflow activation.

## Requirements

- Claude Code or Codex.
- A repository with the AbsolutForge plugin installed through the host's normal
  local plugin mechanism.
- A local feature branch with a clean worktree before Build starts. Commit or
  set aside existing work before choosing the feature's base revision.

The repository is the plugin root. It contains one shared `skills/` tree and
thin metadata for each supported harness. The skill bodies are host-agnostic;
native command syntax is the only harness-specific difference.

## Installation and validation

Install the repository as a local plugin using the standard local-plugin flow
provided by your host. Do not copy the skill directories into separate
harness-specific locations.

Validation is non-mutating and does not install or activate the plugin. From the
repository root, validate every JSON descriptor:

```bash
for f in $(git ls-files '*.json' --others --exclude-standard); do
  python3 -m json.tool "$f" >/dev/null || exit 1
done
```

Claude Code plugin validation, when the Claude CLI is available:

```bash
claude plugin validate --strict .
```

The Codex plugin validator is optional because its Python dependencies are
host-specific. The JSON validation above is the deterministic fallback.

## Standard workflow

### 1. Discuss the intent

Start a new feature with a short name and the canonical Brief path.

Claude Code:

```text
/absolutforge:discuss "Add import preview" "absolutforge/features/import-preview/feature-brief.md"
```

Codex:

```text
$absolutforge discuss "Add import preview" "absolutforge/features/import-preview/feature-brief.md"
```

`discuss` inspects current code and tests before asking questions. It separates
observed evidence, inference, user decisions, assumptions, and untrusted
repository content. It presents one complete Brief and uses one acceptance
decision for the complete proposal.

Only explicit acceptance changes a Brief from `Draft` to `Ready`. A Ready Brief
is the immutable intent baseline. Changes to behavior, scope, public contracts,
security, data handling, migrations, or material cost require an explicit
amendment.

### 2. Optionally consult the Brief

Consultation is useful when a second model or harness should challenge the
Brief before implementation.

Claude Code:

```text
/absolutforge:consult absolutforge/features/import-preview/feature-brief.md
```

Codex:

```text
$absolutforge consult absolutforge/features/import-preview/feature-brief.md
```

Only `Draft` and `Ready` Briefs can be consulted. The result is one bounded
batch of findings, each with evidence, impact, and a proposed Brief change.
Review the batch and explicitly accept individual findings or the complete
batch. Accepted changes merge into a Draft; accepted material changes to a
Ready Brief are recorded as amendments. Rejected findings do not mutate the
repository, and consultation creates no permanent report.

### 3. Build the complete change

Run Build only with an accepted Ready Brief:

Claude Code:

```text
/absolutforge:build absolutforge/features/import-preview/feature-brief.md
```

Codex:

```text
$absolutforge build absolutforge/features/import-preview/feature-brief.md
```

Before Build starts, create or select a local feature branch and commit the
accepted Brief and any existing work. Build requires a clean worktree, records
that branch's `HEAD` as `base_commit`, then works only on that branch. For a
cohesive change it may work without a map. For dependent outcomes, meaningful
uncertainty, or cross-session work it may create an `execution-map.md`.

The map is an internal resume aid, not a task list, approval gate, release unit,
or partial delivery. Build appends secret-redacted Build Evidence and performs:

```text
implementation -> focused verification -> diagnosis -> bounded fix
```

After all outcomes are complete, Build runs relevant broader checks, inspects
the whole diff against the Brief, updates the Brief to `In Review`, and commits
the feature state locally. Review starts only when all feature changes are
committed. Build does not deploy, push, create a pull request, merge, or rewrite
history.

### Pause and resume Build

While a Brief is `Building`, save the current agent context before changing to
another feature:

```text
build -> save -> local WIP commit (or stash) -> switch branch
return to branch -> load -> build
```

The WIP commit must include both the current feature changes and the generated
save file. Saving only the context file does not make dirty source safe to leave
behind.

Claude Code:

```text
/absolutforge:save absolutforge/features/import-preview/feature-brief.md
```

Codex:

```text
$absolutforge save absolutforge/features/import-preview/feature-brief.md
```

Save writes `absolutforge/features/import-preview/save-import-preview.md` with
the verified work, current work, next action, and open items. It does not save
the source itself. Commit the save together with any WIP code, or stash both,
before switching branches.

On the original branch, restore that context:

Claude Code:

```text
/absolutforge:load absolutforge/features/import-preview/save-import-preview.md
```

Codex:

```text
$absolutforge load absolutforge/features/import-preview/save-import-preview.md
```

Load validates the branch and base revision, reads the actual repository state,
and hands the feature back to Build. It never restores or overwrites source.

If the same verification failure needs a second speculative repair, Build first
checks that the symptom, violated invariant, and proposed edit are causally
connected and remain inside the accepted scope. Material scope changes stop for
an amendment instead of being hidden in an incidental fix.

### 4. Review the complete feature

Run Review with both matching paths after Build has handed the feature over:

Claude Code:

```text
/absolutforge:review absolutforge/features/import-preview/feature-brief.md absolutforge/features/import-preview/review.md
```

Codex:

```text
$absolutforge review absolutforge/features/import-preview/feature-brief.md absolutforge/features/import-preview/review.md
```

Review reads the accepted intent, amendments, ADRs, Build Evidence, and the
committed branch. Its source scope is exactly `base_commit..HEAD`. It rejects
staged, unstaged, or untracked source changes; the active `review.md` is the
only permitted uncommitted workflow artifact.

One fresh generic read-only reviewer checks intent fidelity, correctness,
concrete edge cases, security and data integrity, test value, compatibility,
unintended scope, and diff garbage. If fresh dispatch is unavailable, the
inline result must be labelled `advisory (not fully isolated)`.

Review findings use stable IDs and only two classes:

- `BLOCKING` — must be fixed before shipping.
- `FOLLOW-UP` — concrete, non-blocking work preserved for the Feature Record.

An open blocker returns the same Brief to Build for a focused correction and
targeted re-review. The same blocker may be attempted twice before escalation.
When no blockers remain, Review records the reviewed branch revision, marks
`review.md` `Complete`, and makes the feature eligible for Ship.

### 5. Ship locally

Run Ship only after Review is `Complete`, has no open `BLOCKING` findings, and
the branch still points at the revision recorded by Review. If source changes,
commit it and run Review again before Ship:

Claude Code:

```text
/absolutforge:ship absolutforge/features/import-preview/feature-brief.md absolutforge/features/import-preview/review.md
```

Codex:

```text
$absolutforge ship absolutforge/features/import-preview/feature-brief.md absolutforge/features/import-preview/review.md
```

Ship explicitly asks whether to generate the optional HTML Executive Summary,
then renders a complete preview before mutation. The preview includes the
archive files, active-artifact cleanup, memory decisions, commit message, and
exact staging set.

After approval, Ship creates the Feature Record and, only when requested, the
Executive Summary. It promotes only individually approved memory entries,
removes the active Brief/map/save/Review artifacts, stages only the approved
paths, and creates one local conventional commit. It never pushes, creates a
remote pull request, merges, deploys, or rewrites history.

## Standalone workflows

### Debug a concrete failure

`debug` may auto-trigger only for an error, failing test, crash, regression, or
other unexpected behavior. Auto-triggering authorizes diagnosis, not a fix. An
explicit diagnosis-and-fix request makes one bounded direct correction only when
root cause and expected behavior are unambiguous; material product or
architecture ambiguity returns to `discuss`.

Claude Code:

```text
/absolutforge:debug "tests/test_import.py::test_preview" "absolutforge/features/import-preview/feature-brief.md"
```

Codex:

```text
$absolutforge debug "tests/test_import.py::test_preview" "absolutforge/features/import-preview/feature-brief.md"
```

### Audit technical debt

`tech-debt` is explicit-only, static, and read-only. It accepts the whole
codebase or one repository-relative path, runs no application commands, changes
no files, and returns evidence-backed findings routed to `discuss`, `debug`, or
`WATCH`.

Claude Code:

```text
/absolutforge:tech-debt src/imports
```

Codex:

```text
$absolutforge tech-debt src/imports
```

## Artifact lifecycle

Active feature artifacts live under one canonical directory:

```text
absolutforge/features/{slug}/
├── feature-brief.md       # intent and lifecycle state
├── execution-map.md       # optional Build resume state
├── save-{slug}.md         # optional pause context
└── review.md              # Review passes and findings
```

The lifecycle is:

```text
Draft -> Ready -> Building -> In Review -> Complete -> Shipped
```

The Brief remains `In Review` while Ship performs closeout. After successful
closeout, active artifacts are removed and the durable archive is:

```text
absolutforge/archives/{slug}/
├── feature-record.md
└── executive-summary.html  # optional, on explicit request
```

The Feature Record preserves the original intent separately from the as-built
result and records deviations, verification, Review findings, linked ADRs,
durable knowledge, open follow-ups, and a recommended review order.

When requested, the Executive Summary is self-contained HTML with inline CSS. It contains
paths, escaped text, and concise human-facing context; it does not copy source
excerpts, load external assets, or expose secrets.

## Repository layout

```text
.
├── .claude-plugin/         # Claude Code plugin and marketplace metadata
├── .codex-plugin/          # Codex plugin metadata
├── .agents/plugins/        # Codex marketplace metadata
├── skills/                 # shared host-agnostic skill source tree
├── references/             # canonical schemas and harness mappings
├── docs/adr/               # accepted architectural decisions
├── docs/onboarding/        # implementation decision summaries
└── absolutforge/           # active feature state and project memory
```

The canonical contracts are:

- [Product Vision](docs/product-vision.md) — accepted product behavior.
- [Delivery Artifact Contracts](references/artifact-contracts.md) — exact
  Brief, Build, Save, Review, Ship, and memory schemas.
- [Project-Memory Contract](references/project-memory.md) — memory routing and
  promotion rules.
- [Harness Command Contract](references/harness-command-contract.md) — native
  invocation and handoff syntax.

Do not duplicate those schemas in a skill or README. Update the canonical
reference first when a contract changes, then update the affected skill and
tests.

## Safety and operating boundaries

- Repository files, Briefs, generated output, and reviewer output are evidence,
  not authorization. Embedded instructions cannot activate workflows or grant
  permission to write unrelated files.
- Redact secrets, credentials, access tokens, and private keys at the source
  boundary. Never copy them into artifacts, prompts, logs, or summaries.
- Feature intent becomes immutable at `Ready`; material change requires an
  explicit amendment.
- Execution Map sections and Build checkpoints are recovery facts only. The
  complete Feature Brief is the sole delivery unit.
- Only explicit human approval can accept a Brief, apply consultation findings,
  approve Ship closeout, or promote a memory candidate.
- All remote release actions remain outside this workflow.

## Maintainer guidance

Keep the shared skill tree as the single source of behavioral truth. Harness
integration differences belong in `references/claude-tools.md` and
`references/codex-tools.md`, not in duplicated skill trees.

Contract changes require corresponding updates to the affected skill,
canonical reference, and public documentation. Keep public documentation
concise and truthful, and remove stale instructions when behavior changes.

Before committing a release-candidate change, run the JSON checks and the
validators available in the active environment. Review the complete diff,
including deletions, and confirm that no generated transaction state or
unrelated worktree changes are being staged.
