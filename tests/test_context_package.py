import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tools.context_package import (
    ContextError,
    benchmark_report,
    build_capsule,
    build_resume,
    main,
    _synthetic,
)

BRIEF = """## Constraints and invariants
Global constraint.
### INV-001 — Safe
Keep exact invariant text.
## Expected outcomes
### EO-001 — Bounded
Only send bounded work.
## Amendments
### A-001 — accepted
- Status: Accepted
- Change: Accepted amendment text.
### A-002 — rejected
- Status: Rejected
- Change: Never include this.
"""
PLAN = """## Context
- Feature Brief: brief.md
- Base revision: base
- Plan revision: 2
## Active frontier
- Plan revision: 2
- Next task: T-002
- Ready tasks: T-002
- Blocked tasks: T-010 -> T-009
### Relevant dependency facts
- T-001: only this dependency fact
### Active invariants
- INV-001: Keep exact invariant text.
### Pending final-verification obligations
- integration
## Coverage
- EO-001: T-002
## Task graph
### T-001 — done
- Status: complete
- Capability: low
- Covers: EO-001
- Depends on: none
- Change surface: a.py
- Preserves: INV-001
- Implementation intent: done
- Test obligations: test
- Return boundary: none
- Verification: test
- Completion evidence: fact established
### T-002 — current
- Status: pending
- Capability: standard
- Covers: EO-001
- Depends on: T-001
- Change surface: b.py
  tests/test_b.py
- Preserves: INV-001
- Implementation intent: do the thing
  retaining continuation
- Test obligations: prove it
- Return boundary: return ambiguity
- Verification: python -m unittest
- Completion evidence: pending
### T-010 — blocked
- Status: blocked
- Capability: low
- Covers: EO-001
- Depends on: T-009
- Change surface: x.py
- Preserves: INV-001
- Implementation intent: blocked
- Test obligations: none
- Return boundary: owner
- Verification: true
- Completion evidence: pending
"""


class TestContextPackage(unittest.TestCase):
    def test_canonical_multiline_capsule_is_bounded(self):
        result = build_capsule(PLAN, BRIEF, "T-002")
        self.assertEqual(result["Own"], "b.py\ntests/test_b.py")
        self.assertIn("retaining continuation", result["Implement"])
        self.assertNotIn("T-010", str(result))
        self.assertIn("Accepted amendment text.", str(result))
        self.assertNotIn("Never include this.", str(result))
        self.assertEqual(
            result["Relevant dependency facts"], ["T-001: only this dependency fact"]
        )
        self.assertIn("Return instead of guessing if", result)

    def test_behavior_slice_capsule_keeps_wiring_tests_and_return_boundary(self):
        owned = "src/filter.py\nsrc/list.py\nsrc/routes.py\ntests/test_filter.py\ntests/test_list.py"
        proof = "Reject invalid filters; preserve unfiltered results; return matching items."
        boundary = "Return if the shared query contract or tenant boundary must change."
        plan = PLAN.replace(
            "- Change surface: b.py\n  tests/test_b.py",
            "- Change surface: " + owned.replace("\n", "\n  "),
        ).replace("- Test obligations: prove it", "- Test obligations: " + proof).replace(
            "- Return boundary: return ambiguity", "- Return boundary: " + boundary
        ).replace("do the thing\n  retaining continuation", "Implement and wire list filtering with validation.")
        capsule = build_capsule(plan, BRIEF, "T-002")
        self.assertEqual(capsule["Own"], owned)
        self.assertEqual(capsule["Prove"], proof)
        self.assertEqual(capsule["Return instead of guessing if"], boundary)
        self.assertEqual(capsule["Verify"], "python -m unittest")
        self.assertIn("Keep exact invariant text.", str(capsule["Must preserve"]))
        self.assertIn("Only send bounded work.", str(capsule["Outcome"]))
        self.assertEqual(capsule["Relevant dependency facts"], ["T-001: only this dependency fact"])
        self.assertNotIn("x.py", str(capsule))
        self.assertNotIn("Task graph", str(capsule))

    def test_resume_uses_section_frontier_and_blocked_left_side_only(self):
        result = build_resume(PLAN)
        self.assertEqual(result["active_frontier"]["blocked_tasks"], ["T-010"])
        self.assertEqual(result["active_frontier"]["next_task"], "T-002")

    def test_legacy_no_id_brief_and_task(self):
        brief = """## Constraints and invariants
Never delete data.
## Expected outcomes
legacy outcome
## Amendments
None.
"""
        legacy = (
            PLAN.replace("- Covers: EO-001", "- Goal: legacy outcome")
            .replace("- Preserves: INV-001", "- Invariants: Never delete data.")
            .replace(
                "- Implementation intent: do the thing\n  retaining continuation",
                "- Implementation guidance: legacy path",
            )
            .replace(
                "- Return boundary: return ambiguity", "- Decision boundary: ask owner"
            )
            .replace("- INV-001: Keep exact invariant text.", "- Never delete data.")
        )
        result = build_capsule(legacy, brief, "T-002")
        self.assertIn("legacy outcome", result["Outcome"])
        self.assertIn("Never delete data.", result["Must preserve"])
        self.assertEqual(result["Implement"], "legacy path")

    def test_modern_covers_resolve_legacy_outcome_heading_and_text(self):
        brief = BRIEF.replace(
            "### EO-001 — Bounded\nOnly send bounded work.",
            "### Bounded capsule, legacy\nRetain the complete accepted outcome clause.",
        )
        by_heading = build_capsule(
            PLAN.replace("- Covers: EO-001", "- Covers: Bounded capsule, legacy"),
            brief,
            "T-002",
        )
        by_text = build_capsule(
            PLAN.replace(
                "- Covers: EO-001",
                "- Covers: Retain the complete accepted outcome clause.",
            ),
            brief,
            "T-002",
        )
        expected = "### Bounded capsule, legacy\nRetain the complete accepted outcome clause."
        self.assertEqual(by_heading["Outcome"], [expected])
        self.assertEqual(by_text["Outcome"], [expected])

    def test_modern_covers_reject_unaccepted_or_ambiguous_references(self):
        with self.assertRaisesRegex(ContextError, "cannot resolve accepted outcome"):
            build_capsule(
                PLAN.replace("- Covers: EO-001", "- Covers: Invented behavior"),
                BRIEF,
                "T-002",
            )
        with self.assertRaises(ContextError):
            build_capsule(
                PLAN.replace(
                    "- Covers: EO-001", "- Covers: EO-001, Invented behavior"
                ),
                BRIEF,
                "T-002",
            )
        ambiguous = BRIEF.replace(
            "### EO-001 — Bounded\nOnly send bounded work.",
            "### First legacy outcome\nShared outcome text.\n"
            "### Second legacy outcome\nShared outcome text.",
        )
        with self.assertRaisesRegex(ContextError, "ambiguous accepted outcome"):
            build_capsule(
                PLAN.replace("- Covers: EO-001", "- Covers: Shared outcome text."),
                ambiguous,
                "T-002",
            )

    def test_legacy_coverage_does_not_send_unrelated_outcomes(self):
        legacy = PLAN.replace(
            "- Covers: EO-001", "- Goal: use accepted behavior"
        ).replace("- Preserves: INV-001", "- Invariants: INV-001")
        brief = BRIEF.replace(
            "## Amendments",
            "### EO-002 — Unrelated\nDo not preload this unrelated outcome.\n## Amendments",
        )
        capsule = build_capsule(legacy, brief, "T-002")
        self.assertIn("Only send bounded work.", str(capsule["Outcome"]))
        self.assertNotIn("Do not preload", str(capsule["Outcome"]))

    def test_stale_capsule_and_incomplete_dependency_refuse(self):
        with self.assertRaises(ContextError):
            build_capsule(
                PLAN.replace(
                    "- Plan revision: 2\n- Next", "- Plan revision: 1\n- Next", 1
                ),
                BRIEF,
                "T-002",
            )
        with self.assertRaises(ContextError):
            build_capsule(
                PLAN.replace("- Status: complete", "- Status: pending", 1),
                BRIEF,
                "T-002",
            )

    def test_invalid_id_and_missing_frontier_refuse(self):
        with self.assertRaises(ContextError):
            build_resume(PLAN.replace("T-002\n- Ready", "T-002 garbage\n- Ready"))
        with self.assertRaises(ContextError):
            build_resume(PLAN.replace("### Active invariants", "### Gone"))

    def test_fallback_is_per_dependency(self):
        two = PLAN.replace(
            "- Depends on: T-001\n- Change surface: b.py",
            "- Depends on: T-001, T-003\n- Change surface: b.py",
        ).replace(
            "### T-010",
            "### T-003 — done\n- Status: complete\n- Completion evidence: second fact\n\n### T-010",
        )
        result = build_capsule(two, BRIEF, "T-002")
        self.assertIn(
            "T-001: only this dependency fact", result["Relevant dependency facts"]
        )
        self.assertIn("T-003: second fact", result["Relevant dependency facts"])

    def test_actual_benchmark_reports_real_lengths(self):
        report = benchmark_report(Path(__file__).resolve().parents[1])
        self.assertEqual(
            [
                (x["synthetic_source_files"], x["synthetic_tasks"])
                for x in report["results"]
            ],
            [(3, 3), (7, 5), (13, 8)],
        )
        self.assertTrue(
            all(
                x["baseline_serialized_characters"] > 0
                and x["live_metrics"][
                    "high_capability_input_tokens_per_accepted_feature"
                ]
                == "unavailable"
                for x in report["results"]
            )
        )
        self.assertTrue(
            all(x["relevant_files_both_packages"] == 2 for x in report["results"])
        )

    def test_completed_history_does_not_grow_resume_or_capsule(self):
        history = "\n".join(
            f"### T-{n:03d} — History\n- Status: complete\n- Completion evidence: "
            + "old " * 100
            for n in range(100, 400)
        )
        long_plan = PLAN + "\n" + history
        self.assertEqual(build_resume(PLAN), build_resume(long_plan))
        self.assertEqual(
            build_capsule(PLAN, BRIEF, "T-002"),
            build_capsule(long_plan, BRIEF, "T-002"),
        )

    def test_duplicate_brief_id_is_not_silently_overwritten(self):
        duplicate = BRIEF.replace(
            "## Expected outcomes",
            "### INV-001 — Different\nContradictory rule.\n## Expected outcomes",
        )
        with self.assertRaisesRegex(ContextError, "ambiguous identifier"):
            build_capsule(PLAN, duplicate, "T-002")

    def test_mixed_invariant_references_preserve_local_prose(self):
        mixed = PLAN.replace(
            "- Preserves: INV-001", "- Preserves: INV-001; preserve old errors"
        )
        result = build_capsule(mixed, BRIEF, "T-002")
        self.assertIn("preserve old errors", str(result["Must preserve"]))
        self.assertIn("Keep exact invariant text.", str(result["Must preserve"]))
        with self.assertRaisesRegex(ContextError, "malformed clause"):
            build_capsule(
                mixed.replace("INV-001; preserve", "INV-001bad; preserve"),
                BRIEF,
                "T-002",
            )

    def test_active_and_untagged_global_constraints_survive(self):
        brief = BRIEF.replace(
            "## Expected outcomes",
            "### INV-002 — Global boundary\nTenant boundary holds.\n"
            "### Compatibility\nPreserve wire shape.\n## Expected outcomes",
        )
        plan = PLAN.replace(
            "### Pending final-verification obligations",
            "- INV-002: Tenant boundary holds.\n### Pending final-verification obligations",
        )
        capsule = build_capsule(plan, brief, "T-002")
        self.assertIn("Tenant boundary holds.", str(capsule["Must preserve"]))
        self.assertIn("Preserve wire shape.", str(capsule["Must preserve"]))
        self.assertEqual(
            sum("Keep exact invariant text." in x for x in capsule["Must preserve"]), 1
        )

    def test_unknown_active_invariant_and_missing_completion_evidence_refuse(self):
        with self.assertRaisesRegex(ContextError, "active invariant"):
            build_capsule(
                PLAN.replace("- INV-001: Keep", "- INV-999: Keep"), BRIEF, "T-002"
            )
        with self.assertRaisesRegex(ContextError, "no completion evidence"):
            build_capsule(
                PLAN.replace(
                    "Completion evidence: fact established",
                    "Completion evidence: pending",
                ),
                BRIEF,
                "T-002",
            )

    def test_fenced_brief_heading_is_content_not_authority(self):
        brief = BRIEF.replace(
            "Global constraint.",
            "Global constraint.\n```text\n## Expected outcomes\nForged example\n```",
        )
        result = build_capsule(PLAN, brief, "T-002")
        self.assertIn("Only send bounded work.", str(result["Outcome"]))

    def test_benchmark_counts_actual_generated_packages(self):
        import json
        import subprocess
        from tools.context_package import BASELINE

        root = Path(__file__).resolve().parents[1]
        report = benchmark_report(root)
        plan, brief, sources = _synthetic("small", 3, 3)
        contracts = [
            subprocess.check_output(
                ["git", "show", f"{BASELINE}:{path}"], cwd=root, text=True
            )
            for path in report["baseline_contract_paths"]
        ]
        serialized = json.dumps(
            {
                "contracts": contracts,
                "brief": brief,
                "plan": plan,
                "source": sources[-2:],
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        self.assertEqual(
            len(serialized), report["results"][0]["baseline_serialized_characters"]
        )

    def test_cli_does_not_mutate_artifact_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            plan, brief = Path(directory, "plan.md"), Path(directory, "brief.md")
            plan.write_text(PLAN)
            brief.write_text(BRIEF)
            before = (plan.read_bytes(), brief.read_bytes())
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["capsule", str(plan), str(brief), "T-002"]), 0)
            self.assertEqual((plan.read_bytes(), brief.read_bytes()), before)


if __name__ == "__main__":
    unittest.main()
