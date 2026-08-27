# Implementation Context: Phase 2 — Discuss and optional consultation

## Purpose
Concise durable handoff between Phase 2 workers. Add only facts needed by later phases.

## Completed Phases
- Phase 2 contracts and ADR: canonical consultation and native handoff boundaries are complete.

## Created / Changed API
- `consult` accepts `Draft`/`Ready` Briefs at `absolutforge/features/{slug}/feature-brief.md`; it has no durable report.
- `discuss` owns explicit-only discovery, adaptive Draft persistence, and the single Draft → Ready acceptance transition; its Codex metadata disables implicit invocation.
- Phase 3 consult implementation is complete: `skills/consult/SKILL.md` and Codex metadata enforce explicit, approval-controlled findings with Draft merges and Ready amendments.

## Decisions Made
- `consult` is explicit-only and optional; the normal workflow remains `discuss -> build`.
- Ready intent changes only through accepted amendments; consultation creates no durable report.
- Building/In Review consultation routes material changes back to `discuss` without mutation; no-findings returns `no material findings`.

## Test Utilities / Fixtures
- Existing standard-library unittest conventions live in `tests/test_foundation.py`.

## Constraints For Next Phases
- Skills must remain in the shared `skills/` tree and link canonical contracts rather than copy full schemas.
- No hooks, MCP, apps, registered agents, Pi/Grok integrations, plugin activation, or dependency installation.

## Verification History
- Phase contract grep checks passed for consultation semantics, statuses, and Claude/Codex command forms.
- `python3 -m unittest tests.test_discuss_contract` passes; Ruby YAML parsing validates `skills/discuss/agents/openai.yaml`.
- `python3 -m unittest tests.test_consult_contract` passes; Ruby YAML parsing validates `skills/consult/agents/openai.yaml`.
- Consult frontmatter, canonical-link, forbidden-string, and YAML checks pass.
- Integrated verification: `python3 -m unittest discover -s tests -t . -p 'test_*.py'` passed (33 tests).
- Integrated verification: all tracked/untracked JSON descriptors parsed successfully; `claude plugin validate --strict .` passed.
- Integrated verification: `AGENTS.md` symlink and both skill frontmatter preflights passed; AC-1 through AC-15 token check passed.
- Codex validator skipped because PyYAML is unavailable (`ModuleNotFoundError: No module named 'yaml'`); no dependency was installed.
