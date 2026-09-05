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

For later live runs, hold accepted intent, repository base, test gates and host
configuration constant across 0.6/0.7. Record provider/tokenizer and actual host
input counters, include correction loops and independent Review, and compare
only completed accepted features. Live runs are deferred, not a delivery gate.

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
