# Final Verification: Phase 2 — Discuss and optional consultation

## Status
pending

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-2-discuss.md`

## Scope

Verify the integrated Phase 2 skills, canonical contracts, documentation, and
deterministic AC coverage without installing or activating AbsolutForge.

## Traces to

AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15

## Commands

1. Complete unittest suite:
   `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
2. JSON validation:
   `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`
3. Strict Claude validation:
   `claude plugin validate --strict .`
4. Codex validator preflight:
   `python3 -c 'import yaml'`
5. When preflight succeeds:
   `python3 /Users/kamil/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .`
6. Skill frontmatter:
   `for f in skills/discuss/SKILL.md skills/consult/SKILL.md; do test "$(head -n 1 "$f")" = "---"; done`
7. Exact AC traceability:
   `python3 -c 'import re; from pathlib import Path; text="\n".join(p.read_text() for p in Path("tests").glob("test_*.py")); missing=[f"AC-{n}" for n in range(1,16) if not re.search(rf"(?<!\d)AC-{n}(?!\d)", text)]; assert not missing, missing'`
8. Shared-tree and hook boundary:
   `test ! -d claude/skills && test ! -d codex/skills && test ! -d hooks`
9. Context mirror:
   `test -L AGENTS.md && test "$(readlink AGENTS.md)" = "CLAUDE.md"`
10. Repository state:
    `git status --short`

## Completion Criteria

- The complete test suite exits zero with literal AC-1 through AC-15 coverage.
- Every JSON descriptor parses and strict Claude validation exits zero.
- The canonical Codex validator exits zero or the missing-PyYAML skip is recorded without installation.
- Both skills have valid frontmatter in the one shared tree.
- No hook, host-specific skill tree, or plugin configuration mutation exists.
- The final implementation review gate passes.

## Verification Results

- Commands executed: pending
- Results: pending
- Skipped checks: pending
