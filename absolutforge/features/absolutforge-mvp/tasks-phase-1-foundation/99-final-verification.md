# Final Verification: Phase 1 — Product foundation

## Status
pending

## Parent
`absolutforge/features/absolutforge-mvp/tasks-phase-1-foundation.md`

## Scope

Verify the integrated Phase 1 foundation without installing or enabling AbsolutForge.

## Traces to

AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12

## Commands

1. JSON validation:
   `for f in $(git ls-files '*.json' --others --exclude-standard); do python3 -m json.tool "$f" >/dev/null; done`
2. Foundation tests:
   `python3 -m unittest discover -s tests -t . -p 'test_*.py'`
3. Strict Claude validation:
   `claude plugin validate --strict .`
4. Codex validator preflight:
   `python3 -c 'import yaml'`
5. If preflight succeeds:
   `python3 /Users/kamil/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .`
6. AC traceability:
   `for n in $(seq 1 12); do grep -R "AC${n}\|AC-${n}" tests >/dev/null || exit 1; done`
7. Repository state:
   `git status --short`

## Completion Criteria

- JSON validation exits zero.
- Foundation tests exit zero with all named AC tests passing.
- Strict Claude validation exits zero.
- Codex validator exits zero, or the PyYAML preflight failure is recorded as the documented non-mutating skip.
- Every AC-1 through AC-12 appears in a test method or explicit foundation assertion.
- No plugin install, activation, push, or commit was performed.

## Verification Results

- Commands executed: pending
- Results: pending
- Skipped checks: pending

