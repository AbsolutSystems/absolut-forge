# ADR: Lean planned Build, context rotation, and risk-based tests

**Accepted:** 2026-09-01

## Decision

Keep autonomous `build` and `build-planned` as the two first-class implementation strategies, while recommending autonomous Build by default. Planned Build is selected when durable decomposition, meaningful bounded delegation, or cross-session resume is expected to repay its overhead.

Simplify the planned lifecycle to `Ready -> Executing -> Complete`. Replace separate deviation and replan records with one append-only `PC-` plan-change entry that preserves completed task evidence and revises only the affected pending frontier.

Remove consultation from plan control flow. `consult` remains an explicitly requested, immutable evidence report for a Brief or plan. It never opens, settles, pauses, or resumes Build state, and Build never offers it automatically.

Replace primarily exclusion-framed verification guidance with a positive Test Charter. Each changed behavior identifies applicable primary, failure/boundary, state/data, seam-contract, and regression obligations. Specialized risks include authorization, persistence, public compatibility, concurrency, and migration. The number of tests follows distinct risks rather than tasks.

Require orchestrator-owned local checkpoint commits at Build start, after every verified autonomous outcome or planned task, and at final `In Review` handoff. Planned Build also commits its Ready plan before source edits. Dependency-ready tasks may form one parallel wave only when their write surfaces are fully disjoint; each result is validated and committed separately.

Treat the active planned-build orchestrator context as disposable. Every completed-task checkpoint must leave the Brief, plan, committed source/tests and Git history sufficient for a fresh high-capability orchestrator to continue without prior conversation. Per-task durable evidence lives in the plan; the Brief receives one consolidated final Build Evidence entry. `save/load` is reserved mainly for a mid-task or otherwise unresolved interruption.

## Rationale

The 0.3 consultation state machine added substantial instruction and artifact complexity without demonstrated delivery benefit. Its safeguards prevented duplicate consultation more rigorously than the underlying risk justified and increased resume-state interpretation burden.

Observed harness evaluation also showed that adding stricter verification prose did not necessarily produce broader test suites. Negative guidance such as avoiding speculative cases and preferring few assertions can anchor a model on minimizing tests. Explicit risk obligations direct attention toward behavior that can fail while still avoiding test theater.

Checkpoint commits make `base_commit..HEAD` complete and reviewable, protect verified work across session interruption, and remove ambiguity about when source becomes part of the Review range.

Long-lived orchestrator conversations accumulate discovery, worker results, diffs, diagnostics and plan history until compaction can discard causal detail. Explicit rotation boundaries make conversation memory a cache rather than execution authority. They also let a fresh high-capability context own a difficult task or final integration without loading raw interactions from earlier work.

## Superseded decisions

This ADR supersedes the plan-consultation control-state decision and the exclusion-led test framing in `2026-08-31-verification-doctrine-and-plan-consultation.md`. It preserves optional cross-session consultation, executable behavior tests, recorded exemptions, and final whole-feature verification.
