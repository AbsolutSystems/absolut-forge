import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.artifact_state import ContextError
from tools.build_projection import final_projection, owner_projection
from tools.compile_runtime import OUTPUTS, ROOT, compile_state


def run(repo, *args):
    subprocess.run(args, cwd=repo, check=True, text=True, capture_output=True)


class ProjectionRepo:
    def __init__(self, root):
        self.root = Path(root)
        run(self.root, "git", "init", "-q")
        run(self.root, "git", "config", "user.email", "test@example.com")
        run(self.root, "git", "config", "user.name", "Test")
        (self.root / "src").mkdir()
        (self.root / "tests").mkdir()
        (self.root / "feature").mkdir()
        (self.root / "src/a.py").write_text("VALUE = 1\n")
        (self.root / "tests/test_a.py").write_text("assert True\n")
        run(self.root, "git", "add", ".")
        run(self.root, "git", "commit", "-qm", "base")
        self.base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.root, check=True, text=True, capture_output=True).stdout.strip()

    def finish(self, unowned=False, blocker=False):
        brief = f"""# Feature
## Status
In Review
## Constraints and invariants
### INV-001 — Keep behavior
Keep behavior.
## Expected outcomes
### EO-001 — Deliver
Deliver it.
## Amendments
### A-001 — Candidate
- Status: Accepted
- Change: compare later
## Build Evidence
### Build start — 2026-09-10
- Base revision: `{self.base}`
- Build strategy: planned
- Planned methodology: standard
- Execution artifact: `feature/implementation-plan.md`
### Build evidence — 2026-09-10
- Base revision / review diff: `{self.base}..HEAD`
- Build strategy: planned
- Planned methodology: standard
- Changed areas: src and tests
- Tests added/updated: tests/test_a.py — observable case
- Verification commands and results: python tests -> pass
- Whole-feature path exercised: projection fixture -> pass
- Execution state: T-001 complete
- Material implementation decisions: experimental candidate
- Deviations from accepted baseline: A-001
- Plan changes: none
- Scout disposition: none
- Documentation maintenance: none
- Durable memory lesson: none
"""
        plan = """# Plan
## Status
Complete
## Context
- Feature Brief: feature/feature-brief.md
- Base revision: base
- Plan revision: 1
## Coverage
- EO-001: T-001
## Active frontier
- Plan revision: 1
- Next task: none
- Ready tasks: none
- Blocked tasks: none
### Relevant dependency facts
- None
### Active invariants
- INV-001
### Pending final-verification obligations
- None
## Task graph
### T-001 — Implement
- Status: complete
- Capability: standard
- Covers: EO-001
- Depends on: none
- Change surface: `src/a.py`; `tests/test_a.py`
- Preserves: INV-001
- Implementation intent: implement
- Test obligations: observable behavior
- Risk controls: none
- Return boundary: ambiguity
- Verification: python tests
- Completion evidence: pass
"""
        review = f"""# Review
## Status
Complete
## Findings
### F-001 — BLOCKING
- Resolution: {'open' if blocker else 'fixed'}
"""
        (self.root / "feature/feature-brief.md").write_text(brief)
        (self.root / "feature/implementation-plan.md").write_text(plan)
        (self.root / "feature/review.md").write_text(review)
        (self.root / "src/a.py").write_text("VALUE = 2\n")
        if unowned:
            (self.root / "outside.txt").write_text("not owned\n")
        run(self.root, "git", "add", ".")
        run(self.root, "git", "commit", "-qm", "finish")
        return tuple(self.root / value for value in ("feature/feature-brief.md", "feature/implementation-plan.md", "feature/review.md"))


class TestBuildProjection(unittest.TestCase):
    def test_owner_and_final_derive_durable_state_without_diff_duplication(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = ProjectionRepo(tmp)
            brief, plan, review = fixture.finish()
            owner = owner_projection(fixture.root, brief, plan, review)
            final = final_projection(fixture.root, brief, plan, review)
            self.assertEqual(owner["checks"], "PASS")
            self.assertIsNone(owner["current_task"])
            self.assertEqual(final["evidence_freshness"], "PASS")
            self.assertEqual(final["changed_paths"], ["feature/feature-brief.md", "feature/implementation-plan.md", "feature/review.md", "src/a.py"])
            self.assertNotIn("diff", final)
            self.assertIn("inspect the complete diff range", final["semantic_exceptions"][0])

    def test_final_fails_closed_for_dirty_unowned_and_blocking_state(self):
        for mode in ("dirty", "unowned", "blocker", "stale", "incomplete"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                fixture = ProjectionRepo(tmp)
                brief, plan, review = fixture.finish(unowned=mode == "unowned", blocker=mode == "blocker")
                if mode == "dirty":
                    (fixture.root / "src/a.py").write_text("dirty\n")
                elif mode == "stale":
                    (fixture.root / "src/a.py").write_text("VALUE = 3\n")
                    run(fixture.root, "git", "add", "src/a.py")
                    run(fixture.root, "git", "commit", "-qm", "late source change")
                elif mode == "incomplete":
                    plan.write_text(plan.read_text().replace("- Status: complete", "- Status: pending"))
                    run(fixture.root, "git", "add", "feature/implementation-plan.md")
                    run(fixture.root, "git", "commit", "-qm", "contradict final state")
                with self.assertRaises(ContextError):
                    final_projection(fixture.root, brief, plan, review)

    def test_owner_rejects_illegal_lifecycle_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = ProjectionRepo(tmp)
            brief, plan, review = fixture.finish()
            plan.write_text(plan.read_text().replace("Complete\n## Context", "Executing\n## Context"))
            with self.assertRaisesRegex(ContextError, "illegal lifecycle state"):
                owner_projection(fixture.root, brief, plan, review)

    def test_generated_runtime_is_deterministic_and_covers_sources(self):
        for state, relative in OUTPUTS.items():
            generated = compile_state(ROOT, state)
            self.assertEqual((ROOT / relative).read_text(), generated)
            self.assertIn("Non-authoritative generated projection", generated)
            for rule in ("build-entrypoint", "common-runtime", "planned-runtime", "codex-host"):
                self.assertIn(f"rule `{rule}`", generated)
        before = compile_state(ROOT, "planned-building")
        common = ROOT / "runtime/common.md"
        original = common.read_text()
        try:
            common.write_text(original + "\n")
            self.assertNotEqual(before, compile_state(ROOT, "planned-building"))
        finally:
            common.write_text(original)


if __name__ == "__main__":
    unittest.main()
