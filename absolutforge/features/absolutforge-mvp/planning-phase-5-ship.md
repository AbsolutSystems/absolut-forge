# Phase 5: Ship (epic: AbsolutForge MVP)

## Parent context

> Start by reading `absolutforge/features/absolutforge-mvp/planning-main.md`.

- Epic planning: `absolutforge/features/absolutforge-mvp/planning-main.md`
- Dependencies: Phase 4 Review with no open `BLOCKING` findings

## Status
Ready — 2026-08-28

## Phase goal

Deliver the explicit closeout stage that turns a review-complete feature into a
durable, human-readable delivery record and a local commit. Ship must preserve
the accepted intent separately from the as-built result, generate the Executive
Summary from the final post-review state, and keep every mutation behind one
human approval gate.

## Scope

### In scope

- Canonical Ship input validation and final Review eligibility checks.
- A post-review source-state fingerprint that prevents a stale summary when
  code changes after Review.
- Consolidated `absolutforge/archives/{slug}/feature-record.md` preserving
  original intent, outcomes, deviations, verification, Review findings, ADRs,
  durable knowledge, and open follow-ups.
- Self-contained `executive-summary.html` for a human PR reviewer, generated
  from the final post-review state with inline styling and no external runtime
  assets.
- Human preview and approval of the Feature Record, HTML, archive/deletion
  operations, memory promotions, commit message, and PR description.
- Explicit project-memory promotion routing and approval, including global
  candidates and package-local Gotchas.
- Reversible active-artifact cleanup, explicit staging, and a local
  conventional commit only.

### Out of scope

- Generating or presenting a final summary before Review fixes and freshness
  checks finish.
- Automatic push, PR creation, merge, deployment, or history rewriting.
- Rewriting the accepted Brief, Review history, or Build Evidence to hide a
  deviation.
- Archiving unrelated reports, another feature's artifacts, or the transient
  Execution Map as a separate file.
- A second review taxonomy, automatic triada, or a new implementation/fix loop.

### Deliberately not doing

- Copying source-code excerpts into Executive Summary; repository-relative paths
  and recommended review order are enough and avoid duplication/secrets.
- Adding a release platform integration or remote API for PR creation.
- Treating a successful archive write as shipped before the local commit is
  created and verified.
- Silently overwriting an existing archive directory or unresolved dirty work.

## Assumptions and decisions

### Assumptions

- The final Review pass can record a deterministic fingerprint of the reviewed
  feature-owned source scope. Review's safe-scope rule is authoritative: it
  includes committed, staged, unstaged, and feature-owned untracked files;
  excludes `review.md`, Review/process artifacts, and unrelated dirty files;
  and records an input blocker when unrelated changes cannot be separated. The
  fingerprint is a SHA-256 over a canonical, sorted manifest:
  each entry is `path-hex NUL state NUL mode NUL content-sha256 LF`, where
  `path-hex` is the lowercase hex of raw repository-relative path bytes, `state`
  is `present` or `deleted`, `mode` is the Git mode (`100644`, `100755`, `120000`,
  or `160000`; `000000` for deleted), `content-sha256` is the SHA-256 of the
  present path's Git content bytes (including symlink target bytes or a gitlink
  object ID), and a deleted entry uses 64 zeroes; raw bytes and LF/NUL
  delimiters are hashed, with mtimes and filesystem ordering ignored. The path
  set is the union of the base revision and current worktree scope, so
  deletions are represented.
- A Ship invocation runs in the same repository and can resolve the Review's
  recorded `base_commit` and current-worktree scope.
- Archive writes, approved memory changes, active-artifact cleanup, staging, and
  the local commit are one local repository transaction after approval. Remote
  push, PR creation, merge, and deployment remain outside Ship. A pre-existing
  index entry must be listed in the approved path set; any pre-existing staged
  path outside that set is an input blocker and is never included accidentally.

### Decisions requiring confirmation

- None. The user accepted link/path-only Executive Summary content and the
  post-review freshness guard on 2026-08-28.

## Selected solution

Implement one explicit-only, host-agnostic `ship` skill. It validates matching
repository-relative Brief and Review paths, requires Brief `In Review`, Review
`Complete`, no open `BLOCKING` findings, and a valid final Review pass. Review
records a sorted path manifest and deterministic source fingerprint for the
feature-owned scope; Ship recomputes the same algorithm before rendering and
again immediately after approval, before any archive, memory, cleanup, or
staging mutation. A missing or changed fingerprint stops without mutation and
emits a native Review handoff. After that final check Ship does not pause for
more input; it performs the transaction serially and checks the fingerprint once
more immediately before freezing the commit tree. The HTML link allowlist
accepts only normalized repository-relative paths (optionally with a fragment),
renders them as `../../../{repo-relative-path}` from
`absolutforge/archives/{slug}/executive-summary.html`, and rejects targets that
escape the repository or do not exist in the prospective frozen commit tree
(newly added files therefore remain linkable). It also rejects
external, protocol-relative, `file:`, `javascript:`, `data:`, and absolute URLs;
all rendered text is escaped. Ship acquires an exclusive OS advisory lock at
`.ship-txn/lock` before the post-approval check and holds it through commit;
lock metadata records the transaction ID, process, host, and start time, while
the kernel releases the lock on process death. The final commit uses the
immutable tree captured after the last fingerprint check, so a non-cooperating
source edit cannot alter the committed tree; a post-commit drift check reports
the active-worktree change and routes it back to Review without rewriting
history.

Ship reads the immutable Brief baseline, accepted amendments, final diff,
Build Evidence, Execution Map when present, Review passes/findings, linked ADRs,
active memory, and relevant candidates. It renders a Feature Record and a
self-contained HTML Executive Summary in memory (or ignored scratch space) so
the active artifacts remain untouched before approval. The HTML embeds its CSS
and any small diagrams, escapes untrusted text, contains no source excerpts,
and links to repository paths/ADRs and a recommended review order.

Before mutation, Ship presents the exact proposed archive files, active-file
deletions, memory destinations and candidate changes, commit message, PR
description, and rendered summaries. One closeout approval binds the complete
preview to the source fingerprint; each memory candidate is accepted or
rejected individually before the transaction starts. A rejected candidate is
simply omitted and remains unchanged while the approved archive may proceed.

After approval, Ship creates `.ship-txn/{txid}/journal.json` (ignored by Git)
before any mutation. The journal records the transaction state, preview digest,
fingerprint/manifest, exact approved path set, original bytes/modes/existence of
every path it may change, the pre-transaction index tree, candidate promotion
decisions, the generated commit message, and one `pending|running|completed`
operation record per memory, archive, cleanup, staging, and commit action. The
normal state machine is `prepared -> applying -> staged -> committing ->
committed`; any failure branches to `recovery-required`. Recovery then takes an
explicit `resume` branch back to `applying` or an explicit `rollback` branch to
the terminal `rolled-back` state. A new invocation detects an unfinished journal
and must explicitly resume or roll it back, never duplicate archive or memory
work. Resume skips a completed operation only after verifying its recorded
output hash/path; a missing or mismatched output is rolled back before replay.
It promotes approved memory first, writes the archive, removes active Brief/map/Review artifacts,
stages only the agreed paths in a transaction-private index, performs the final
fingerprint check while holding the lock, freezes the resulting tree, atomically
records `commit_intent` with the target ref, expected parent `HEAD`, frozen tree
ID, and commit-message digest, creates a conventional local commit from that
tree whose subject matches
`^(feat|fix|refactor|docs|test|chore|perf)(\([a-z0-9][a-z0-9-]*\))?!?: [^\r\n]+$`,
atomically updates the target ref with the expected parent, and replaces the
real index with the frozen tree only if it still equals the journaled
pre-transaction index (otherwise it preserves the external index and reports a
post-commit index conflict).
If interrupted, recovery first checks whether the target ref already points to
a commit matching the intent; when it does, it records that result, replays the
conditional real-index replacement, and verifies every archive, memory, and
cleanup output hash before marking the commit operation `completed` and the
journal `committed`. A moved ref, non-matching commit, or finalization conflict
is a recovery conflict that keeps the journal open, never creates a duplicate,
and stops for explicit resolution.
The pre-transaction index snapshot is the target restoration state on failure;
pre-existing staged paths not listed in the approved feature set are an input
blocker and are never silently included. If any step fails, Ship compares each current path and
index entry with the transaction-owned output and the journaled original before
restoring. It restores only entries still matching one of those states; a
non-matching user or external edit is preserved, recorded as a recovery conflict,
and escalated rather than overwritten. It removes only archive files created by
this transaction, retains the journal at the canonical
`.ship-txn/{txid}/journal.json` location with `state: recovery-required`, and
reports the exact failure. Recovery is idempotent: the next invocation must
explicitly choose `resume` or `rollback`, reuses the same transaction ID, and
never duplicates archive or memory work.
The OS lock is reacquired for recovery; a stale metadata file alone never
authorizes mutation, and a live owner blocks until it exits. Rollback attempts
every journaled path/index entry; conflicting external edits are preserved and
escalated instead of overwritten. If restoration fails, Ship stops and leaves
the journal in `recovery-required` for escalation; it does not claim Shipped. A
successful rollback marks the journal `rolled-back`, records the clean rollback,
removes the ignored journal, and releases the lock. A successful commit marks
the journal `committed`, records the
resulting commit ID in the closeout output, then removes the ignored journal
and releases the lock.

### Rationale

This keeps the human-facing explanation trustworthy: the Brief explains why,
the final diff explains what, and Build/Review evidence explains why the result
is ready. Generating from a verified post-review state prevents the stale-summary
problem, while one preview gate avoids both silent archive mutation and a heavy
multi-stage ceremony. Link-only summaries stay compact and make the diff the
single place for source detail.

### Alternatives considered

- **Generate Summary before Review:** rejected because Review fixes or later
  changes could make the explanation stale.
- **Trust the textual Review scope without a fingerprint:** rejected because a
  user can change source files after Review and the drift would be invisible.
- **Copy code excerpts into HTML:** rejected because it duplicates the diff,
  increases size, and expands secret-redaction risk; paths and review order are
  sufficient.
- **Write archive and delete active files before approval:** rejected because a
  rejected preview would already mutate delivery state.
- **Push/create a PR automatically:** rejected because remote side effects are
  outside the MVP and require separate user authorization.

## Implementation plan

1. Extend the canonical artifact contract with Ship preconditions, the exact
   canonical fingerprint manifest/algorithm, Feature Record and Executive
   Summary fields, memory-promotion approval, archive cleanup, transaction
   journal/recovery, commit handling, and failure semantics. Add the Review
   fingerprint and reviewed-path manifest fields required by Ship.
2. Update the Review contract/skill to record the deterministic reviewed-scope
   path manifest and fingerprint without changing Review ownership or its
   one-reviewer model.
3. Add native Claude/Codex Ship handoffs and create explicit-only
   `skills/ship/SKILL.md` plus `skills/ship/agents/openai.yaml` covering
   validation, rendering, preview, approval, promotion, archive, cleanup,
   staging, local commit, and no-remote-side-effect boundaries.
4. Add deterministic Ship contract tests and extend foundation discovery to the
   fifth skill. Use pure fixture assertions for canonical path ordering,
   present/deleted entries, raw path-byte encoding, deleted mode/hash sentinels,
   approval binding, per-item memory rejection, journal state transitions,
   normal/failure state graph with terminal rollback, idempotent resume/rollback,
   advisory-lock ownership/stale metadata handling,
   exact staging/index preservation, immutable commit-tree and post-commit drift
   behavior, commit-intent recovery after interruption, conditional index
   reconciliation, final output-hash verification, expected-parent ref
   validation, conventional-commit grammar, and no-remote-side-effect commands;
   structurally validate self-contained HTML, archive-relative links, target
   existence, and its link allowlist without invoking a model or mutating a
   repository.
5. Update README, CLAUDE.md, product vision, skills index, and harness
   references to mark Ship implemented and preserve the separate Phase 6
   autonomous-tools scope.
6. Run static tests, JSON/manifest validation, diff hygiene, an HTML structural
   check, and a manual review of representative archive/preview fixtures.

## Files to be modified / created

- `references/artifact-contracts.md` — canonical Ship lifecycle, fingerprint
  manifest/algorithm, Feature Record, Executive Summary, memory, archive,
  transaction journal, and failure contracts.
- `references/harness-command-contract.md` — native Ship commands and final
  handoff semantics for Claude Code and Codex.
- `references/claude-tools.md` — Claude Ship invocation and local-commit mapping.
- `references/codex-tools.md` — Codex Ship invocation and explicit-only metadata.
- `skills/review/SKILL.md` — record the reviewed source fingerprint for Ship.
- `skills/review/agents/openai.yaml` — preserve Review metadata while adding no
  new activation path.
- `skills/ship/SKILL.md` — new explicit-only closeout orchestrator.
- `skills/ship/agents/openai.yaml` — Codex `$ship` metadata with implicit
  invocation disabled.
- `tests/test_review_contract.py` — verify the reviewed path manifest and
  fingerprint handoff remains compatible with Review.
- `tests/test_ship_contract.py` — deterministic Ship lifecycle, rendering,
  freshness, archive, memory, journal/recovery, staging, and safety coverage.
- `tests/test_foundation.py` — fifth-skill discovery and metadata assertions.
- `README.md`, `CLAUDE.md`, `docs/product-vision.md`, `skills/README.md` —
  current Ship behavior and closeout boundaries.
- `docs/adr/2026-08-28-ship-post-review-closeout.md` — durable decision for
  post-review rendering, freshness, approval, and local-only closeout.
- `.gitignore` — keep `.ship-txn/` recovery journals out of delivery commits.
- `absolutforge/features/absolutforge-mvp/planning-main.md` — mark Phase 5
  `Zaplanowana` after this plan is accepted and verified.

## Edge cases and risks

- Brief or Review path is missing, malformed, outside the canonical feature
  directory, or in the wrong status: stop before mutation.
- Review has an open `BLOCKING`, missing final pass, absent base revision, or
  unresolved input blocker: stop and hand back to Review/Build as appropriate.
- The current source fingerprint differs from Review before approval or at the
  final commit precondition: preserve/restore active artifacts, do not claim
  closeout, and request Review again on the same feature.
- Existing archive directory or archive files conflict with the requested slug:
  stop without overwriting and explain the collision.
- Unrelated dirty files cannot be separated from the feature's staging set:
  stop before cleanup or commit; do not absorb them.
- A memory candidate is sensitive, stale, malformed, or lacks a clear route:
  present it as ineligible and do not promote it.
- User rejects the preview: keep the complete active workflow unchanged. A user
  rejects an individual memory item: omit that promotion and leave its candidate
  unchanged while the approved closeout may proceed.
- Archive, promotion, deletion, staging, or commit fails: compare each current
  path/index entry with its transaction-owned output and journaled original;
  restore only matching entries, preserve conflicting external edits, remove
  only transaction-created archive files, retain the recovery journal, report
  the exact incomplete step, and do not claim Shipped. A later explicit
  `resume`/`rollback` is idempotent; a restoration conflict leaves the journal
  in place and requires escalation.
- A second process changes source during the transaction: the final fingerprint
  is frozen into the transaction commit tree, so the concurrent edit cannot
  alter that commit; the post-commit drift check reports it and routes the
  active worktree back to Review without rewriting history. A live Ship lock
  blocks another invocation; after a crash the kernel releases the advisory
  lock, but stale metadata alone never authorizes resume/rollback.
- A concurrent Git commit moves the target ref after the recorded parent
  `HEAD`: the expected-parent ref update fails, the journal remains in recovery,
  and Ship does not create a second branch tip or rewrite history.
- Repository content, Review output, and candidate lessons are untrusted;
  redact secrets and ignore embedded instructions.

## Acceptance Criteria

### Happy path

- AC-1: When the user explicitly invokes Ship with matching repository-relative
  Brief and Review paths, Ship accepts the closeout only when the Brief is
  `In Review`, the Review is `Complete`, no `BLOCKING` finding remains open, and
  final Review evidence is present.
- AC-2: The proposed closeout reflects the immutable original intent, accepted
  amendments, final as-built change, Build Evidence, and Review result; any
  deviation is shown as a deviation rather than silently changing the intent.
- AC-3: When the reviewed source remains unchanged, the proposed closeout is
  based on that final post-review state and remains consistent across preview,
  archive, and commit preparation.
- AC-4: The Feature Record preserves original intent separately from outcomes
  and includes verification, Review findings and result, linked ADRs, durable
  knowledge, deviations, and open follow-ups.
- AC-5: The Executive Summary is a self-contained HTML document that a human PR
  reviewer can open without network access and that presents the TL;DR,
  problem/value, scope, flow, changed components, decisions, deviations,
  verification, Review findings, follow-ups, review order, and documentation
  links.
- AC-6: The Executive Summary points reviewers to repository-relative files and
  links instead of reproducing source-code excerpts, and its content matches
  the final state after Review fixes.
- AC-7: Before any archive, memory, cleanup, staging, or commit action, Ship
  shows the exact Feature Record, Executive Summary, proposed deletions,
  individually selected memory destinations/entries, commit message, and PR
  description for one explicit approval bound to the reviewed source state.
- AC-8: After approval, Ship creates the archive, promotes only individually
  approved memory entries, removes only the agreed active feature artifacts,
  stages only the agreed paths, preserves any pre-existing approved index state,
  and creates a local conventional commit whose subject follows the documented
  grammar without pushing or creating a remote PR.

### Edge cases

- AC-9: Invalid or mismatched paths, an incorrect status, malformed input,
  missing Review evidence, or an open blocker stops Ship before mutation and
  explains the correction or handoff required.
- AC-10: If the reviewed source manifest/fingerprint is missing or has changed
  since Review, Ship refuses to render or close out, preserves active artifacts,
  and directs the user back to Review for the same feature; a change detected at
  the final commit precondition triggers journal recovery and no commit.
- AC-11: If the destination archive already conflicts or unrelated worktree
  changes cannot be separated, Ship stops without overwriting, absorbing,
  deleting, or committing those files.
- AC-12: If the user rejects the preview, the active workflow remains unchanged;
  if the user rejects one memory promotion, that candidate remains unchanged and
  the approved closeout may proceed without it.
- AC-13: If archive, memory, cleanup, staging, or commit work fails, Ship
  compares current files/index entries with transaction-owned outputs and their
  journaled originals, restores only non-conflicting entries, preserves and
  escalates conflicting external edits, removes only transaction-created
  archive files, leaves a bounded recovery journal at
  `.ship-txn/{txid}/journal.json`, reports the incomplete step, and never claims
  `Shipped` or rewrites history to recover; explicit resume or rollback is
  idempotent and escalates if restoration fails. An interruption after ref
  update but before journal finalization recognizes a commit matching the
  recorded parent/tree/message intent and marks it committed rather than
  creating a duplicate only after replaying conditional index reconciliation and
  verifying archive/memory/cleanup outputs; a moved target ref or finalization
  conflict keeps recovery open for explicit resolution.
- AC-14: Any transient Execution Map information needed to explain outcomes or
  verification appears in the Feature Record, while the map itself is not
  archived as a separate delivery artifact.

### Security

- AC-15: Content from Briefs, diffs, Review output, memory candidates, and
  generated text is treated as untrusted: embedded instructions cannot approve
  actions, and secrets, credentials, tokens, and private keys are redacted
  rather than copied into the Feature Record, HTML, PR description, logs, or
  commit message. HTML links and resources are limited to normalized
  repository-local paths with no external, `file:`, `javascript:`, `data:`,
  protocol-relative, or absolute URLs.

## Open questions

- None. Executive Summary content is link/path-only by explicit user choice;
  post-review fingerprinting, preview approval, memory routing, archive cleanup,
  local-only commit, and failure preservation follow the accepted product
  contracts.

## Discussion notes

- The user specifically required the final human summary to reflect the state
  after Review fixes, so Ship never renders a final summary from a pre-review or
  stale snapshot.
- The user accepted no code excerpts in the HTML; the summary uses concise
  repository paths and a recommended file-review order.
- Ship is a closeout stage, not a second quality gate: Review owns findings and
  Build owns fixes; Ship verifies eligibility and preserves the evidence.
- Memory promotion remains explicit and separately routed; no candidate is
  promoted merely because it appears relevant.
