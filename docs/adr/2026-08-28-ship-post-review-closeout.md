# ADR: Post-review closeout with a freshness guard

## Date

2026-08-28

## Status

Accepted

## Context

AbsolutForge needs a lightweight closeout stage that turns a review-complete
feature into durable human documentation and a local commit. A summary rendered
before Review fixes, or from source changed after Review, can mislead the human
reviewer. Closeout also needs to preserve immutable intent, keep memory
promotion deliberate, and avoid remote side effects.

## Decision

`ship` renders the Feature Record and self-contained Executive Summary only from
the final post-review state. Review's safe source scope and canonical
fingerprint are Ship's only freshness baseline. Review's safe-scope rule is authoritative: it
includes committed, staged, unstaged, and feature-owned untracked files;
excludes `review.md`, Review/process artifacts, and unrelated dirty files; and
records an input blocker when unrelated changes cannot be separated. Review
records the exact eligible path manifest and a SHA-256 fingerprint over its
canonical sorted entries:
`path-hex NUL state NUL mode NUL content-sha256 LF`. `path-hex` is lowercase
hexadecimal of raw repository-relative path bytes; `state` is `present` or
`deleted`; mode is `100644`, `100755`, `120000`, or `160000` (`000000` for a
deletion); the content hash is SHA-256 of Git content bytes (including symlink
target bytes or a gitlink object ID); deleted entries use 64 zeroes. Raw bytes,
LF/NUL delimiters, and raw-path-byte ordering are part of the algorithm; mtimes
and filesystem enumeration order are not. The path set is the union of the
base revision and current worktree, with review/process and unrelated paths
excluded. Ship verifies that manifest and fingerprint before rendering and
again immediately after approval, before any repository mutation. A missing or
changed fingerprint stops closeout and routes the feature back to Review
without mutating active artifacts. The link target is rendered relative to the
archive location (`../../../{repo-relative-path}`), after normalization and
existence checking in the prospective frozen commit tree; deleted paths are
rendered as text. Links and resources are path-only: external,
protocol-relative, absolute, `file:`, `javascript:`, and `data:` URLs are
rejected, and rendered text/attributes are escaped.

Ship presents one complete preview gate covering generated artifacts, cleanup,
memory destinations, commit message, and PR description. Memory items are
accepted or rejected individually; rejected candidates remain unchanged while
the approved closeout proceeds. After explicit approval, Ship acquires an OS
advisory lock at `.ship-txn/lock` before revalidating the fingerprint, archive
collisions, approved scope, index baseline, and other transaction preconditions.
While holding the lock and before the first mutation it captures the exact
target ref and expected parent `HEAD`, writes the ignored canonical journal
`.ship-txn/{txid}/journal.json`, and holds the lock through commit. Lock
metadata records transaction ID, process, host, and start time; the kernel
releases the lock on process death, and stale metadata alone never authorizes
mutation. The journal stores the fingerprint/manifest, preview digest,
approved path set, original bytes/modes/existence, pre-transaction index tree,
captured target ref/expected parent, promotion decisions, commit message, and per-operation
`pending|running|completed` records. The normal state machine is `prepared ->
applying -> staged -> committing -> committed`; each operation is marked
`completed` only after its output path/hash or index/ref result is verified and
recorded; any failure branches to
`recovery-required`. Recovery takes an explicit `resume` branch back to
`applying` or an explicit `rollback` branch to terminal `rolled-back`. An
unfinished journal requires that explicit, idempotent choice and never
duplicates archive or memory work. Resume skips a completed operation only
after verifying its output hash/path; otherwise it rolls back before replay.
The transaction promotes
approved memory first, writes the archive, removes active Brief/map/Review
files, stages only the agreed paths, uses the pre-existing index as the
restoration baseline, freezes an immutable commit tree after the final
fingerprint check. Before creating the commit, Ship records `commit_intent`
with the previously captured target ref and expected parent `HEAD`, frozen tree ID, and commit-message
digest, creates a local commit from that tree whose subject matches
`^(feat|fix|refactor|docs|test|chore|perf)(\([a-z0-9][a-z0-9-]*\))?!?: [^\r\n]+$`,
atomically updates the target ref with the expected parent, and replaces the
real index with the frozen tree only if it still equals the journaled
pre-transaction index (otherwise it preserves the external index and reports a
post-commit index conflict). If interrupted, recovery first checks whether the
target ref already points to a matching commit; when it does, it replays the
conditional real-index replacement and verifies every archive, memory, and
cleanup output hash before marking the commit operation `completed` and the
journal `committed`. A moved ref, non-matching commit, or finalization conflict
keeps the journal open, never creates a duplicate, and stops for explicit
resolution.
Any pre-existing staged path not listed in the approved path set is rejected
before mutation. The commit is created from the frozen tree, so a
non-cooperating source edit cannot alter the committed tree; a post-commit drift
check reports the active-worktree change and routes it back to Review without
rewriting history. On failure, Ship compares each current path/index entry with
its transaction-owned output and journaled original, restores only
non-conflicting entries, preserves conflicting external edits, and escalates
instead of clobbering them. It removes only transaction-created archive files
and retains `state: recovery-required`; a restoration failure stops and
escalates with the journal path. A successful rollback marks the journal
`rolled-back`, records the clean rollback, removes the ignored journal, and
releases the lock. It never pushes, creates a PR, merges, deploys, or rewrites
history. Link/path-only summaries are used instead of copying source excerpts.

## Considered alternatives

- **Render before Review:** rejected because later fixes make the summary stale.
- **Trust only textual Review scope:** rejected because source drift is not
  reliably detectable without a recorded path manifest and fingerprint.
- **Copy source excerpts into HTML:** rejected due duplication, size, and secret
  exposure risk; paths and review order are sufficient.
- **Mutate archives before approval:** rejected because preview rejection must
  leave the active workflow intact.
- **Remote-first closeout:** rejected because network side effects require a
  separate explicit user action outside the MVP.

## Consequences

- Human documentation describes exactly the reviewed source state.
- Review gains one small durable output: a source-scope fingerprint.
- Ship has a clear, reversible approval boundary and local-only side effects.
- Archive failures require journal-based recovery and may leave an uncommitted
  generated directory, but cannot silently discard the active artifacts.
- Source detail remains in the diff, while the HTML stays concise and safe.

## Related

- Product behavior: `docs/product-vision.md#ship-contract`
- Product behavior: `docs/product-vision.md#ship-contract`
- Artifact schemas: `references/artifact-contracts.md`
