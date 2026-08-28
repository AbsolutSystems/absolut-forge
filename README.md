# AbsolutForge

AbsolutForge is an intent-driven delivery workflow for Claude Code and Codex.
It gives a coding model a precise, accepted product intent, durable decisions,
and clear outcome boundaries, then lets it implement and verify the complete
change before one independent review.

**Release candidate.** The RC includes the complete core workflow:

```text
discuss -> build -> review -> ship
```

It also includes the optional `consult` workflow for a bounded second opinion on
an existing Feature Brief. `debug` and `tech-debt` are not part of this release
candidate.

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
- `review` performs one fresh, read-only, evidence-based review of the complete
  change and records only `BLOCKING` and `FOLLOW-UP` findings.
- `ship` closes a review-complete feature into durable documentation and one
  local commit after a single approval preview.

Core skills are explicit-only. There is no SessionStart hook, global workflow
prompt, MCP server, or automatic activation.

## Requirements

- Claude Code or Codex.
- A repository with the AbsolutForge plugin installed through the host's normal
  local plugin mechanism.
- A cleanly separable worktree. Existing unrelated changes may remain, but
  they must not overlap the feature being delivered.

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

When useful, `discuss` may add an advisory Build Recommendation. It can suggest
the simple/single or complex/phased execution profile, but it never selects a
model automatically, creates an extra approval gate, or authorizes partial
delivery.

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

Build records the starting `base_commit` and initial worktree state. For a
cohesive change it may work without a map. For dependent outcomes, meaningful
uncertainty, or cross-session work it may create an `execution-map.md`.

The map is an internal resume aid, not a task list, approval gate, release unit,
or partial delivery. Build appends secret-redacted Build Evidence and performs:

```text
implementation -> focused verification -> diagnosis -> bounded fix
```

After all outcomes are complete, Build runs relevant broader checks, inspects
the whole diff against the Brief, and changes the Brief to `In Review`. It does
not deploy, push, create a pull request, merge, or rewrite history.

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
current worktree. Its scope starts at `base_commit` and includes committed,
staged, unstaged, and feature-owned untracked files. It excludes review-process
artifacts and unrelated dirty files.

One fresh generic read-only reviewer checks intent fidelity, correctness,
concrete edge cases, security and data integrity, test value, compatibility,
unintended scope, and diff garbage. If fresh dispatch is unavailable, the
inline result must be labelled `advisory (not fully isolated)`.

Review findings use stable IDs and only two classes:

- `BLOCKING` — must be fixed before shipping.
- `FOLLOW-UP` — concrete, non-blocking work preserved for the Feature Record.

An open blocker returns the same Brief to Build for a focused correction and
targeted re-review. The same blocker may be attempted twice before escalation.
When no blockers remain, Review records a canonical source manifest and SHA-256
fingerprint, marks `review.md` `Complete`, and makes the feature eligible for
Ship.

### 5. Ship locally

Run Ship only after Review is `Complete`, has no open `BLOCKING` findings, and
its source fingerprint still matches the current worktree:

Claude Code:

```text
/absolutforge:ship absolutforge/features/import-preview/feature-brief.md absolutforge/features/import-preview/review.md
```

Codex:

```text
$absolutforge ship absolutforge/features/import-preview/feature-brief.md absolutforge/features/import-preview/review.md
```

Ship renders a complete preview before mutation. The preview includes the
archive files, active-artifact cleanup, memory decisions, commit message, PR
description, and exact staging set. One explicit approval binds the preview to
the reviewed source fingerprint.

After approval, Ship runs one journaled local transaction. It creates the
Feature Record and Executive Summary, promotes only individually approved
memory entries, removes the active Brief/map/Review artifacts, stages only the
approved paths, and creates one local conventional commit.

The transaction is recoverable through `.ship-txn/{txid}/journal.json`. Ship
never pushes, creates a remote pull request, merges, deploys, or rewrites
history. A source change after review routes the feature back to Review instead
of silently shipping stale documentation.

## Artifact lifecycle

Active feature artifacts live under one canonical directory:

```text
absolutforge/features/{slug}/
├── feature-brief.md       # intent and lifecycle state
├── execution-map.md       # optional Build resume state
└── review.md              # Review passes and findings
```

The lifecycle is:

```text
Draft -> Ready -> Building -> In Review -> Complete -> Shipped
```

The Brief remains `In Review` while Ship performs closeout. After a successful
transaction, active artifacts are removed and the durable archive is:

```text
absolutforge/archives/{slug}/
├── feature-record.md
└── executive-summary.html
```

The Feature Record preserves the original intent separately from the as-built
result and records deviations, verification, Review findings, linked ADRs,
durable knowledge, open follow-ups, and a recommended review order.

The Executive Summary is self-contained HTML with inline CSS. It contains
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
  Brief, Build, Review, Ship, memory, and fingerprint schemas.
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
