# Review: AbsolutForge 0.7 — Token-Efficient Runtime Contract

## Status
Complete

## Context
- Feature Brief: `absolutforge/features/token-efficient-runtime/feature-brief.md`
- Build strategy: planned
- Planned methodology: standard
- Base revision: `f47dfbc45563b5fce6b8de49cd005f40b7b655fb`
- Reviewed revision: `2fb19cd01f44e3404554d7dae4d9e3cf95e19b0a`
- Review range: `f47dfbc45563b5fce6b8de49cd005f40b7b655fb..2fb19cd01f44e3404554d7dae4d9e3cf95e19b0a`
- Execution artifact read: implementation-plan — header/status/frontier for lifecycle and completion validation; targeted PC-001 and PC-002 entries referenced by final Build Evidence. No task-history or consultation preload.

## Findings

### F-001 — BLOCKING
- Evidence: `tools/context_package.py:302` returns unresolved prose for references without EO IDs; accepted heading/text resolution at `tools/context_package.py:345` runs only for legacy Goal tasks. Modern Covers explicitly permits exact legacy outcome headings/text (`references/planned-build-contract.md:65`), which must resolve to accepted text (`references/artifact-contracts.md:89`). With the existing fixture's Brief heading changed to `### Bounded` and modern Covers changed to `Bounded`, the capsule emits `Outcome: ['Bounded']`, omitting the accepted clause `Only send bounded work.` Replacing Covers with `Invented unaccepted behavior` also succeeds and emits that unaccepted text.
- Impact: a supported modern-task/no-ID-Brief combination silently drops accepted behavior, and an unresolved reference can become worker intent. EO-003/EO-004 and INV-001 are not fully satisfied. The optional helper's orchestrator inspection requirement does not correct its misleading successful projection.
- Smallest sensible correction: resolve modern Covers against unambiguous accepted headings/text as well as EO IDs; reject unknown or ambiguous references. Add regression tests proving accepted clause preservation and unknown/ambiguous reference refusal for modern tasks using older Briefs without IDs.
- Resolution: open
- Resolution details: independently reproduced during Review; no implementation or test edits made. Return to standard planned Build for a bounded PC correction, affected verification, and new complete final Build Evidence before another Review.

Read-only reproduction from the repository root:

```sh
rtk proxy python3 -c 'import runpy; from tools.context_package import build_capsule; f=runpy.run_path("tests/test_context_package.py"); b=f["BRIEF"].replace("### EO-001 — Bounded", "### Bounded"); p=f["PLAN"].replace("- Covers: EO-001", "- Covers: Bounded"); print("valid legacy heading:",build_capsule(p,b,"T-002")["Outcome"]); print("unaccepted heading:",build_capsule(p.replace("- Covers: Bounded", "- Covers: Invented unaccepted behavior"),b,"T-002")["Outcome"])'
```

Observed:

```text
valid legacy heading: ['Bounded']
unaccepted heading: ['Invented unaccepted behavior']
```

## Review passes

### Pass 1 — 2026-09-05
- Mode: fresh
- Scope: exactly one fresh generic read-only reviewer with no inherited builder conversation inspected accepted intent/amendments, final Build Evidence, the complete implementation diff and changed/new tests, then relevant current contracts and implementation. The primary context separately validated delivery/lifecycle evidence and confirmed the finding.
- Delivery gate: initial worktree/index clean; accepted Ready intent unchanged; base and reviewed revision resolve; recorded strategy/methodology consistent; plan Complete at revision 3. Final Build Evidence contains all required current fields, green verification and a valid local whole-feature path. The final handoff changes only lifecycle/final evidence and frontier completion state; no later source/test edits invalidate the evidence. The evidence gate passes, but F-001 blocks acceptance of the implementation.
- Verification: `rtk python3 -m unittest discover -s tests -v` passed all 26 tests, independently rerun by the reviewer; `rtk python3 tools/context_package.py benchmark` passed all three static scenarios; `rtk proxy git diff f47dfbc45563b5fce6b8de49cd005f40b7b655fb..HEAD --check` passed. The F-001 reproduction succeeds with incorrect output.
- Test value: helper tests assert observable content, refusal of invalid frontier/dependency states, amendment filtering, invariant retention, input immutability and bounded history-independent output. Separate-process resume/capsule tests establish local recovery without retained memory. Markdown tests cover repository-owned instruction/distribution contracts; keyword checks offer limited semantic protection, so the complete changed contracts were also reviewed directly. The modern-task/no-ID-Brief combination is missing, leaving the compatibility defect unguarded. No existing assertions were weakened.
- Outcome coverage: EO-001, EO-002, EO-005, EO-006, EO-007 and EO-008 have supporting implementation and local verification evidence; EO-003 and EO-004 remain incomplete due to F-001. Live model comparisons are deferred by accepted scope; static serialized-character results are not measured token savings or model-adherence proof.
- Outcome: one open BLOCKING finding; no FOLLOW-UP findings. Brief returned to Building with planned/standard strategy preserved. Review writes only this report and Brief lifecycle status.

## Decision
Fixes required
