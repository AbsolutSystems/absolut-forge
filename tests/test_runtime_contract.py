"""Distribution and safety contracts for the executable Markdown workflow.

These checks exercise the repository-owned instruction surface. They do not
claim to measure an LLM's adherence or live token usage.
"""

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = "f47dfbc45563b5fce6b8de49cd005f40b7b655fb"


def read(path):
    return (ROOT / path).read_text()


def baseline(path):
    return subprocess.check_output(
        ["git", "show", f"{BASE}:{path}"], cwd=ROOT, text=True
    )


def section(text, title):
    active = False
    fenced = False
    lines = []
    for line in text.splitlines(keepends=True):
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("## "):
            if active:
                return "".join(lines)
            active = line.strip() == "## " + title
            continue
        if active:
            lines.append(line)
    if active:
        return "".join(lines)
    raise AssertionError(f"Missing section: {title}")


class RuntimeContractTests(unittest.TestCase):
    def test_clean_process_resume_to_capsule_preserves_intent_without_history(self):
        from tools.context_package import _synthetic

        plan, brief, _ = _synthetic("large", 13, 8)
        with tempfile.TemporaryDirectory() as directory:
            plan_path = Path(directory) / "implementation-plan.md"
            brief_path = Path(directory) / "feature-brief.md"
            plan_path.write_text(plan)
            brief_path.write_text(brief)
            before = (plan_path.read_bytes(), brief_path.read_bytes())
            command = [sys.executable, str(ROOT / "tools/context_package.py")]
            # Separate processes simulate total loss of previous in-memory state.
            resume = json.loads(
                subprocess.check_output(command + ["resume", str(plan_path)], text=True)
            )
            self.assertEqual(resume["active_frontier"]["next_task"], "T-008")
            capsule = json.loads(
                subprocess.check_output(
                    command + ["capsule", str(plan_path), str(brief_path), "T-008"],
                    text=True,
                )
            )
            self.assertIn("Bounded work.", str(capsule["Outcome"]))
            self.assertIn("Do not mutate.", str(capsule["Must preserve"]))
            self.assertEqual(capsule["Own"], "src/current.py")
            self.assertEqual(capsule["Verify"], "python -m unittest")
            self.assertNotIn("T-001", str(capsule))
            self.assertNotIn("Task graph", str(capsule))
            self.assertEqual((plan_path.read_bytes(), brief_path.read_bytes()), before)
            # A missing frontier is not silently rebuilt by a read-only helper.
            plan_path.write_text(
                plan.replace("## Active frontier", "## Legacy frontier absent")
            )
            refused = subprocess.run(
                command + ["resume", str(plan_path)], text=True, capture_output=True
            )
            self.assertNotEqual(refused.returncode, 0)
            self.assertEqual(refused.stdout, "")

    def test_runtime_is_packaged_and_all_local_links_resolve(self):
        self.assertEqual(
            {path.name for path in (ROOT / "runtime").glob("*.md")},
            {"common.md", "autonomous.md", "planned.md", "review.md"},
        )
        for directory in ("runtime", "references", "skills"):
            for path in (ROOT / directory).rglob("*.md"):
                text = path.read_text()
                # Links form the escalation interface; also validate literal
                # relative .md references used by skill entrypoints.
                targets = re.findall(r"\]\(([^)]+)\)", text)
                targets += re.findall(r"`(\.\./[^`]+\.md)`", text)
                for target in targets:
                    if "://" in target or "{" in target or target.startswith("#"):
                        continue
                    with self.subTest(path=str(path.relative_to(ROOT)), target=target):
                        self.assertTrue((path.parent / target.split("#")[0]).exists())

    def test_two_build_entrypoints_and_explicit_host_commands(self):
        builders = {
            p.name
            for p in (ROOT / "skills").glob("build*")
            if (p / "SKILL.md").exists()
        }
        self.assertEqual(builders, {"build", "build-planned"})
        self.assertFalse(
            (
                ROOT / ".opencode/command/absolutforge-build-planned-delegated.md"
            ).exists()
        )
        commands = read("references/harness-command-contract.md")
        for prefix in ("/absolutforge:", "$absolutforge ", "/absolutforge-", "/skill:"):
            self.assertIn(prefix + "build absolutforge/features/", commands)
            self.assertIn(prefix + "build-planned absolutforge/features/", commands)
            self.assertNotIn(
                prefix + "build-planned-delegated absolutforge/features/", commands
            )
        # The descriptor is still needed for already-recorded Claude ownership.
        self.assertTrue((ROOT / "agents/delegated-executor.md").exists())

    def test_entrypoints_select_runtime_instead_of_full_reference_preload(self):
        for skill, runtime in (
            ("build", "autonomous"),
            ("build-planned", "planned"),
            ("review", "review"),
        ):
            text = read(f"skills/{skill}/SKILL.md")
            self.assertIn("../../runtime/common.md", text)
            self.assertIn(f"../../runtime/{runtime}.md", text)
            # Canonical material is reachable via projection, not embedded again
            # as a second long normal-invocation prompt.
            self.assertLess(len(text), len(baseline(f"skills/{skill}/SKILL.md")))
            for template in ("### PC-{NNN}", "### Build evidence — YYYY-MM-DD"):
                self.assertNotIn(template, text)

    def test_final_evidence_schema_and_risk_charter_are_preserved(self):
        def evidence_template(text):
            return re.search(
                r"```markdown\n(### Build evidence — .*?)```", text, re.S
            ).group(1)

        self.assertEqual(
            evidence_template(read("references/artifact-contracts.md")),
            evidence_template(baseline("references/artifact-contracts.md")),
        )
        for name in (
            "Test charter",
            "Test value",
            "Recorded exemption",
            "Fast and final verification",
        ):
            self.assertEqual(
                section(read("references/verification-doctrine.md"), name),
                section(baseline("references/verification-doctrine.md"), name),
            )
        artifacts = read("references/artifact-contracts.md")
        self.assertIn(
            "A later source or test change invalidates that final entry", artifacts
        )
        self.assertIn(
            "Lifecycle-only and Review-artifact commits do not invalidate it", artifacts
        )
        self.assertIn("Compact intermediate evidence never substitutes", artifacts)

    def test_legacy_policy_preserves_ownership_and_tdd_rejection(self):
        legacy = read("references/planned-delegated-contract.md")
        self.assertIn("`build-planned`", legacy)
        for name in (
            "Orchestrator ownership",
            "Durable methodology and legacy TDD state",
        ):
            self.assertEqual(
                section(legacy, name),
                section(baseline("references/planned-delegated-contract.md"), name),
            )
        self.assertIn("no current builder starts or resumes", legacy)
        planned = read("runtime/planned.md")
        self.assertIn("legacy contract", planned)
        self.assertIn("never convert, substitute or take over", planned)
        for skill in ("load", "build", "review"):
            text = read(f"skills/{skill}/SKILL.md")
            self.assertNotRegex(text, r"(?:->|→|for|to) `build-planned-delegated`")

    def test_review_context_and_write_boundary(self):
        text = read("runtime/review.md")
        for phrase in (
            "Do not preload implementation-plan.md",
            "final Build Evidence",
            "base_commit..HEAD",
            "changed/new tests",
            "fresh generic read-only reviewer",
            "advisory (not fully isolated)",
            "Write only review.md and Brief lifecycle status",
            "BLOCKING",
            "FOLLOW-UP",
            "Never invoke Ship without explicit authorization",
        ):
            self.assertIn(phrase, text)
        self.assertIn(
            "Recorded delegated methodology creates a concrete fixed-owner question",
            text,
        )
        # Targeted canonical reads must not drop severity/write restrictions
        # behind an unrelated section heading (PC-001 regression).
        review = section(read("references/artifact-contracts.md"), "Review")
        self.assertIn("Review finding severity is deterministic", review)
        self.assertIn("Review may write only", review)

    def test_host_packages_do_not_reintroduce_historical_preload(self):
        for host in ("codex", "claude", "opencode", "pi"):
            text = read(f"references/{host}-tools.md")
            with self.subTest(host=host):
                self.assertIn("Task Capsule", text)
                self.assertIn("final Build Evidence", text)
                self.assertNotIn("Brief, completed execution artifact", text)

    def test_frontier_capsule_and_final_escalation_remain_canonical(self):
        planned = read("references/planned-build-contract.md")
        for heading in (
            "Active Frontier rules",
            "Task Capsule",
            "Capability routing",
            "Plan changes",
            "Completion",
        ):
            self.assertTrue(section(planned, heading).strip())
        for field in (
            "Plan revision",
            "Next task",
            "Ready tasks",
            "Blocked tasks",
            "Relevant dependency facts",
            "Active invariants",
            "Pending final-verification obligations",
        ):
            self.assertIn(field, planned)
        self.assertIn(
            "Completed dependencies must have committed completion evidence", planned
        )
        self.assertIn("preserve completed", planned.lower())
        runtime = read("runtime/planned.md")
        self.assertIn("complete plan coverage", runtime)
        self.assertIn("base_commit..HEAD", runtime)
        self.assertIn("primary accepted path", runtime)
        self.assertIn("PC", runtime)

    def test_distribution_json_release_and_skill_roots(self):
        descriptors = [
            ROOT / "package.json",
            *ROOT.glob(".*-plugin/*.json"),
            ROOT / ".agents/plugins/marketplace.json",
        ]
        for path in descriptors:
            with self.subTest(path=str(path.relative_to(ROOT))):
                data = json.loads(path.read_text())
                if "version" in data:
                    self.assertTrue(data["version"].startswith("0.7.0"))
        self.assertEqual(json.loads(read("package.json"))["pi"]["skills"], ["skills"])
        self.assertEqual(
            json.loads(read(".codex-plugin/plugin.json"))["skills"], "./skills/"
        )


if __name__ == "__main__":
    unittest.main()
