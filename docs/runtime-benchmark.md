# Runtime context benchmark

Run the reproducible synthetic report with:

```sh
rtk python3 tools/context_package.py benchmark
```

The report builds actual synthetic artifacts for small (3 source files, 3
tasks), medium (7 files, 5 tasks), and large (13 files, 8 tasks). It reads the
pinned 0.6 entrypoint and its unconditional references at
`f47dfbc45563b5fce6b8de49cd005f40b7b655fb` with read-only `git show`, and compares
the serialized full synthetic baseline to the current skill, common/planned
runtime, active Codex mapping and actual resume projection. Both packages carry
the same accepted Brief and relevant code evidence. Worker capsule size is
reported separately. Autonomous small-feature fixed contract overhead is also
reported; new-start/final-gate escalations are excluded from steady-state
projections, so these figures are not an end-to-end cost comparison.

`*_serialized_characters` measure those generated strings. Token estimates use
ceil(characters / 4); they are not tokenizer counts or measured savings. The
report lists exact baseline/current contract paths. All live metrics remain
`unavailable`: high-capability input per accepted feature, total/worker tokens,
files actually read, implementation success, blockers, correction rounds,
clean resume, defect rate and time require controlled live execution. Do not
infer success or zero defects from a static count. A shallow checkout lacking
the pinned revision must fetch/restore that history separately before running
the comparison; the tool never fetches or substitutes another baseline.

## Controlled live-run protocol

Live measurements use the versioned, secret-redacted record contract in
`references/benchmark-run-record-v1.schema.json`. Raw host traces, prompts,
messages, credentials and repository content stay outside feature artifacts and
Git. Convert an export to the narrow record locally, then validate and aggregate
it with:

```sh
rtk python3 tools/benchmark_runs.py validate path/to/run.json
rtk python3 tools/benchmark_runs.py aggregate path/to/run-*.json
```

For each paired comparison:

1. Freeze the accepted intent, base revision, named gates and host
   configuration. Record SHA-256 digests for intent, gates and configuration.
2. Use the same replay fixture and complete gates for both variants. Alternate
   order across pairs or randomize it before launch, and record the order.
3. Record every owner, worker and reviewer launch by role and stage. Each actual
   host counter is `measured` and names its export source and counter. Missing
   counters are `unavailable`; static approximations are `estimated` with their
   method and are excluded from measured totals.
4. Preserve failed/corrected attempts as a linear chain using `continuation_of`.
   The accepted feature cost includes every attempt in that chain. An incomplete
   or rejected chain is reported but never counted as accepted-feature cost.
5. Run the fixed tests and independent Review. Acceptance requires all declared
   gates to pass. Record observed blockers, escaped blockers, corrections,
   rotations and wall time even when a run fails.
6. Compare total measured input plus output tokens per accepted feature first.
   Use accepted-feature rate, escaped blockers, correction attempts, final
   verification validity and clean resume as guardrails. Treat role splits,
   launches, cached tokens and wall time as diagnostics.

`tests/fixtures/token-efficiency-runs.json` is synthetic proof of validation,
role totals, correction attribution and redaction behavior; it is never a live
baseline. `docs/token-efficiency-corpus-manifest.json` records the only locally
retained replayable execution and fails the required 10–20 item selection in an
explicit `blocked` state. Populate it only from verified external history or
purpose-built fixtures before running the baseline. Do not begin a dependent
rotation, projection, generated-runtime or effort experiment until that corpus
and the real baseline records exist.

### Automatic Codex capture

Codex runs can opt into automatic, secret-redacted collection. Arm a feature
once from its repository; use an output directory outside Git:

```sh
rtk python3 /path/to/installed/absolutforge/tools/codex_benchmark.py \
  --repo . arm \
  --feature-id my-feature \
  --experiment-id 0.10-baseline \
  --variant current-rotation \
  --intent absolutforge/features/my-feature/feature-brief.md \
  --gates absolutforge/features/my-feature/feature-brief.md \
  --output-dir /private/tmp/absolutforge-benchmarks
```

When capture was explicitly requested, the Codex mapping runs `start` before
the Build-owner handoff and `finish` after release-ready independent Review.
Transient state is stored below the repository's Git directory, so it neither
dirties checkpoints nor enters commits. Owner rotations, Luna workers,
corrections and separate Review sessions are included. Only `session_meta`,
`turn_context` and `token_usage_record` lines are parsed; prompt/message records
are ignored and never copied into output.

This adapter targets the currently observed Codex session format and is not a
public OpenAI log-format contract. It fails closed on unknown shapes or counters
that move backwards. Keep a benchmarked repository isolated from other Codex
work until the run finishes. Other hosts still require their own adapters or a
sanitized export accepted by `benchmark_runs.py`.

## Read-only artifact projection

```sh
rtk python3 tools/context_package.py resume path/to/implementation-plan.md
rtk python3 tools/context_package.py capsule path/to/implementation-plan.md path/to/feature-brief.md T-002
rtk python3 -m unittest discover -s tests -v
```

These optional helpers print JSON for a human/orchestrator to inspect. They
read files locally but send only selected sections in output; local file bytes
read are not the same as model input tokens. They never execute verification
commands embedded in artifacts or mutate lifecycle, source, plan or Git state.
Canonical Markdown headings, multiline bullet fields, modern Covers/Preserves
and legacy Goal/Invariants are supported. Accepted amendments and active/global
constraints are retained; proposed/rejected amendments are excluded. The
orchestrator still judges relevance, committed evidence, semantic sufficiency
and safe routing before dispatch.

Missing/stale frontier, unknown/duplicate IDs, incomplete dependencies and
unsupported ambiguous shapes fail closed. The capsule helper handles the
selected Next task only; parallel wave selection remains orchestrator-owned.
An all-complete frontier has no executable task and belongs to final verification,
not this task-dispatch helper. Novel amendment-defined IDs or legacy guidance
that cannot be resolved automatically require targeted canonical inspection;
the helper does not invent or migrate task metadata. Missing legacy guidance
is explicitly returned as an orchestrator decision, not fabricated code advice.

The harness is a regression check for bounded projections, not a general
workflow engine or a claim about production model cost.
