# Review: AbsolutForge 0.7 — Token-Efficient Runtime Contract

## Status
Complete

## Context
- Feature Brief: `absolutforge/features/token-efficient-runtime/feature-brief.md`
- Build strategy: planned
- Planned methodology: standard
- Base revision: `f47dfbc45563b5fce6b8de49cd005f40b7b655fb`
- Reviewed revision: `69d8a49fc5774a6308a10af65b50a2137816008d`
- Review range: `f47dfbc45563b5fce6b8de49cd005f40b7b655fb..69d8a49fc5774a6308a10af65b50a2137816008d`
- Execution artifact read: implementation-plan — header/status/frontier for lifecycle and completion validation; targeted PC-001, PC-002 and PC-003 entries referenced by final Build Evidence; correction diff inspected to verify preservation of completed tasks. No task-history or consultation preload.

## Findings

### F-001 — BLOCKING
- Evidence: `tools/context_package.py:302` returns unresolved prose for references without EO IDs; accepted heading/text resolution at `tools/context_package.py:345` runs only for legacy Goal tasks. Modern Covers explicitly permits exact legacy outcome headings/text (`references/planned-build-contract.md:65`), which must resolve to accepted text (`references/artifact-contracts.md:89`). With the existing fixture's Brief heading changed to `### Bounded` and modern Covers changed to `Bounded`, the capsule emits `Outcome: ['Bounded']`, omitting the accepted clause `Only send bounded work.` Replacing Covers with `Invented unaccepted behavior` also succeeds and emits that unaccepted text.
- Impact: a supported modern-task/no-ID-Brief combination silently drops accepted behavior, and an unresolved reference can become worker intent. EO-003/EO-004 and INV-001 are not fully satisfied. The optional helper's orchestrator inspection requirement does not correct its misleading successful projection.
- Smallest sensible correction: resolve modern Covers against unambiguous accepted headings/text as well as EO IDs; reject unknown or ambiguous references. Add regression tests proving accepted clause preservation and unknown/ambiguous reference refusal for modern tasks using older Briefs without IDs.
- Resolution: fixed
- Resolution details: reproduced in Pass 1 and corrected in `b317784`. Pass 2 independently confirmed that modern Covers resolves full accepted legacy heading/text, including comma-containing headings, and rejects unknown, mixed ID-plus-invented and ambiguous references. Two regression cases protect clause preservation and refusal; all 28 tests pass. No implementation or test edits made during Review.

Historical Pass 1 reproduction from the repository root (before correction):

```sh
rtk proxy python3 -c 'import runpy; from tools.context_package import build_capsule; f=runpy.run_path("tests/test_context_package.py"); b=f["BRIEF"].replace("### EO-001 — Bounded", "### Bounded"); p=f["PLAN"].replace("- Covers: EO-001", "- Covers: Bounded"); print("valid legacy heading:",build_capsule(p,b,"T-002")["Outcome"]); print("unaccepted heading:",build_capsule(p.replace("- Covers: Bounded", "- Covers: Invented unaccepted behavior"),b,"T-002")["Outcome"])'
```

Observed in Pass 1:

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

### Pass 2 — 2026-09-05
- Mode: fresh
- Reviewed revision: `69d8a49fc5774a6308a10af65b50a2137816008d`
- Review range: `f47dfbc45563b5fce6b8de49cd005f40b7b655fb..69d8a49fc5774a6308a10af65b50a2137816008d`
- Scope: exactly one fresh generic read-only reviewer with no inherited conversation reviewed accepted intent/amendments, final Build Evidence, the complete implementation diff, changed/new tests and relevant current implementation/contracts. The primary context separately validated lifecycle, final evidence freshness, plan header/completion and referenced PC-001 through PC-003. No execution-history preload.
- Delivery gate: initial worktree/index clean; accepted intent unchanged from the Ready baseline; base resolves and is an ancestor of reviewed HEAD; planned/standard strategy consistent. Plan Complete at revision 4. The current final Build Evidence contains every required field, green verification and a valid local whole-feature path. The final handoff changes only lifecycle/evidence and derived plan completion/frontier; no later source/test changes invalidate delivery proof. Prior completed tasks remain unchanged by the correction. Gate passes.
- Verification: independent reviewer ran `rtk python3 -m unittest discover -s tests -v` — all 28 tests pass; `rtk python3 tools/context_package.py benchmark` — all three static scenarios pass; full-range `git diff --check` through RTK — pass.
- Test value: observable capsule content, invalid-reference/frontier/dependency refusal, accepted amendment and invariant retention, read-only inputs, legacy compatibility and history-independent output have meaningful coverage. Fresh-process resume/capsule tests exercise local recovery. Instruction/distribution assertions cover repository-owned contracts, supplemented by direct semantic review of the full changes. F-001 now has clause-preservation and unknown/ambiguous-reference regression coverage. No existing assertions were weakened.
- Outcome coverage: EO-001 through EO-008 and INV-001 through INV-005 have supporting implementation and verification evidence. Four runtimes retain canonical escalation, bounded frontier/capsule behavior and capability routing; identifiers, compact checkpoints, independent Review, two builders and legacy policy remain coherent; complete delivery gates and pinned-baseline benchmark remain intact.
- Limitations: static contract checks and local packaging do not prove live model adherence or measured token savings. Live model comparisons remain deferred by accepted scope.
- Outcome: F-001 fixed; no open BLOCKING or FOLLOW-UP findings. Review Complete and Ready for ship. Brief remains In Review as required for Ship. Only this report changed during Review.

## Decision
Ready for ship
