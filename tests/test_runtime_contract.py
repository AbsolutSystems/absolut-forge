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

    def test_one_build_entrypoint_and_explicit_host_commands(self):
        builders = {
            p.name
            for p in (ROOT / "skills").glob("build*")
            if (p / "SKILL.md").exists()
        }
        self.assertEqual(builders, {"build"})
        self.assertFalse((ROOT / ".opencode").exists())
        commands = read("references/harness-command-contract.md")
        for prefix in ("/absolutforge:", "$absolutforge ", "/skill:"):
            self.assertIn(prefix + "build absolutforge/features/", commands)
            self.assertNotRegex(commands, re.escape(prefix) + r"build-planned(?:-delegated)? ")
        # The descriptor is still needed for already-recorded Claude ownership.
        self.assertTrue((ROOT / "agents/delegated-executor.md").exists())

    def test_build_selection_and_resume_contract(self):
        entry = read("skills/build/SKILL.md")
        selection = section(read("references/artifact-contracts.md"), "Build strategy selection")
        for option in ("--strategy=autonomous", "--strategy=planned"):
            for path in ("skills/build/SKILL.md", "references/harness-command-contract.md",
                         "README.md"):
                with self.subTest(option=option, path=path):
                    self.assertIn(option, read(path))
        for obligation in (
            "Default to autonomous", "repay compilation and coordination overhead",
            "File count or generic complexity alone is insufficient",
            "An explicit valid override wins", "repeated overrides before mutation",
            "without another confirmation", "At Building", "never rerun automatic selection",
            "conflicting override is rejected before mutation", "matching override is harmless",
            "Missing strategy", "must not be backfilled", "legacy tdd remains unsupported",
            "An override cannot convert methodology",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, selection)
        self.assertIn("Load only the selected", entry)
        self.assertIn("within this invocation", entry)
        self.assertIn("Draft requires accepted Ready intent", entry)
        self.assertIn("Shipped is closed", entry)
        self.assertIn("never convert, substitute or take over", entry)

    def test_selection_evidence_is_start_only_and_legacy_compatible(self):
        artifacts = read("references/artifact-contracts.md")
        start = section(artifacts, "Build start evidence")
        self.assertIn("- Strategy selection: automatic | explicit override", start)
        self.assertIn("required for new starts only", start)
        self.assertIn("historical starts remain valid unchanged without it", start)
        self.assertNotIn("- Strategy selection:", section(artifacts, "Build evidence"))
        for runtime in ("autonomous", "planned"):
            text = read(f"runtime/{runtime}.md")
            self.assertIn("selection reason", text)
            self.assertIn("checkpoint before source edits", text)

    def test_lifecycle_handoffs_use_build_without_reselection(self):
        discuss = read("skills/discuss/SKILL.md")
        self.assertIn("single public `build`", discuss)
        self.assertIn("do not select a strategy", discuss)
        self.assertIn("Printing the continuation does not invoke Build", discuss)
        self.assertIn("without selecting again", read("skills/load/SKILL.md"))
        self.assertIn("without selecting again", read("runtime/review.md"))
        for path in ("skills/save/SKILL.md", "skills/debug/SKILL.md",
                     "references/planned-build-contract.md"):
            self.assertIn("`build`", read(path))
            self.assertNotIn("`build-planned`", read(path))
        for host in ("codex", "claude", "opencode", "pi"):
            text = read(f"references/{host}-tools.md")
            self.assertIn("`build`", text)
            self.assertNotIn("`build-planned`", text)

    def test_discuss_routes_oversized_product_scope_before_ready(self):
        discuss = read("skills/discuss/SKILL.md")
        for obligation in (
            "multiple independently valuable, cancellation-safe outcomes",
            "Document length, file count, generic complexity",
            "obtain explicit human agreement",
            "Never split one user-visible transaction",
            "Stable phase IDs identify phases",
            "Every behavior is assigned to one phase, marked shared, or explicitly deferred",
            "A Feature Plan and Phase Seed are never `Ready`",
            "Materialize all applicable shared invariants",
            "Keep later-phase scope out",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, discuss)

    def test_feature_plan_and_phase_seed_contracts_are_non_buildable(self):
        artifacts = read("references/artifact-contracts.md")
        plan = section(artifacts, "Feature Plan")
        seed = section(artifacts, "Phase Seed")
        reconciliation = section(
            artifacts, "Feature Plan acceptance and reconciliation"
        )
        for field in (
            "## Artifact kind",
            "Feature Plan — not buildable",
            "## Behaviors and custody",
            "## Phase order",
            "## Next eligible phase",
        ):
            self.assertIn(field, plan)
        for field in (
            "Phase Seed — not buildable",
            "## Phase identity",
            "## Behavior custody",
            "## Coherent stop state",
            "## Evidence to revisit",
        ):
            self.assertIn(field, seed)
        self.assertIn("containing exactly", reconciliation)
        self.assertIn("Never silently rewrite a seed already used", reconciliation)
        self.assertIn(
            "Build\nmust refuse both artifact kinds", reconciliation
        )
        self.assertIn("explicitly refuse `feature-plan.md` and Phase Seed inputs",
                      read("skills/build/SKILL.md"))
        self.assertIn("planning context, never Ready intent or Build inputs",
                      read("runtime/common.md"))

    def test_planning_handoffs_are_native_and_resolved(self):
        commands = read("references/harness-command-contract.md")
        for prefix in ("/absolutforge:", "$absolutforge ", "/skill:"):
            self.assertIn(
                prefix
                + "discuss absolutforge/features/{family-slug}/phases/P{NN}-{phase-slug}.md",
                commands,
            )
        self.assertIn("Feature Plan -> Discuss", commands)
        self.assertIn("Phase Discuss -> Build", commands)
        self.assertIn("A planning artifact never routes to Build", commands)

    def test_entrypoints_select_runtime_instead_of_full_reference_preload(self):
        for skill, runtime in (
            ("build", "autonomous"),
            ("build", "planned"),
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
        ):
            self.assertEqual(
                section(read("references/verification-doctrine.md"), name),
                section(baseline("references/verification-doctrine.md"), name),
            )
        final_verification = section(
            read("references/verification-doctrine.md"), "Fast and final verification"
        )
        for obligation in (
            "inventory of test files and named cases added or changed",
            "derive the affected test set",
            "Reuse a worker's green result",
            "targeted integration or end-to-end targets",
            "A full project, workspace, integration, or end-to-end suite is not a default final gate",
            "committed Ready baseline",
            "configured required CI gate",
        ):
            self.assertIn(obligation, final_verification)
        for runtime_name in ("autonomous", "planned"):
            runtime = read(f"runtime/{runtime_name}.md")
            with self.subTest(runtime=runtime_name):
                self.assertIn("exact test files and named cases added or changed", runtime)
                self.assertIn("Reuse current green worker results", runtime)
                self.assertIn("targeted integration/e2e checks for changed boundaries", runtime)
                self.assertIn("missing-CI justification", runtime)
                self.assertNotIn("authoritative affected-project/changeset suite", runtime)
        plan = read("references/planned-build-contract.md")
        self.assertIn("Name any broad suite deferred to required PR CI", plan)
        self.assertIn("mere fact that this is the final gate does not require a full suite", plan)
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
        self.assertIn("`build`", legacy)
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

    def test_codex_new_standard_profiles_and_explicit_dispatch(self):
        mapping = section(read("references/codex-tools.md"), "Planned Build")
        current = mapping.split("### Legacy delegated resume", 1)[0]
        rows = re.findall(
            r"^\| `(low|standard|high)` \| (.*?) \| (.*?) \|$",
            current, re.M,
        )
        self.assertEqual(rows, [
            ("low", "`gpt-5.6-luna`", "`high`"),
            ("standard", "`gpt-5.6-luna`", "`xhigh`"),
            ("high", "Build owner (`gpt-5.6-sol`)", "`medium`"),
        ])
        for obligation in (
            "For new standard planned builds",
            "designated Sol Build owner",
            "explicit model and reasoning-effort overrides",
            'fork_turns="none"',
            "exact requested worker profile is unavailable",
            "never silently substitute another worker model/effort",
            "This fallback never applies to legacy delegated state",
            "any explicitly recorded execution commitments",
            "Each Luna worker fixes local failures and repeats its focused gate",
            "corrections discovered later by Sol validation or final verification",
        ):
            self.assertIn(obligation, current)
        legacy = mapping.split("### Legacy delegated resume", 1)[1]
        # The pinned 0.6 layout predates this heading. Its exact dispatch rule
        # is still compared directly, preserving fixed model/effort ownership.
        dispatch = 'Dispatch every implementation task and correction with model `gpt-5.6-luna` and reasoning effort `high`.'
        self.assertIn(dispatch, legacy)
        self.assertIn(dispatch, baseline("references/codex-tools.md"))
        self.assertNotIn("xhigh", legacy)
        self.assertIn("stop without substituting another model or taking over implementation", legacy)

    def test_codex_build_owner_rotation_and_bounded_astra_advice(self):
        owner = section(read("references/codex-tools.md"), "Build owner")
        for obligation in (
            "`gpt-5.6-sol` agent with `medium` reasoning",
            "`Role: Codex Build owner`",
            'fork_turns="none"',
            "Before reading the Brief, runtime or repository evidence",
            "launcher waits and relays a completed result",
            "handles only the `ROTATE` control envelope",
            "After every clean checkpoint containing implementation or test changes",
            "A Build-start-only checkpoint does not trigger rotation",
            "returns only `ROTATE: {canonical Build command}`",
            "never build a nested successor chain",
            "before final verification",
            "Pass no conversation or raw-log summary",
            "`gpt-6-astra` advisor with `low` reasoning",
            "read-only",
            "Astra is never the Build owner",
            "does not edit, commit, inherit the Build conversation or take over execution",
            "recorded legacy delegated executor remains fixed",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, owner)
        entry = read("skills/build/SKILL.md")
        self.assertIn("Before loading runtime or repository evidence", entry)
        self.assertIn("launcher that hands off ownership does not inspect artifacts", entry)

    def test_cost_aware_routing_classifies_work_and_rotates_context(self):
        routing = section(read("references/model-routing.md"), "Autonomous outcome routing")
        for obligation in (
            "to one fresh worker by default",
            "fewer owner interactions than preparing and validating the handoff",
            "repetitive inventories, matrices, report rows",
            "treat it as durable evidence",
            "worker owns the local implementation loop",
            "repeat that gate until green",
            "owner does not interleave validation turns into this local loop",
            "When owner validation or final verification discovers a failure",
            "settled API-usage corrections remain low/standard work",
            "Never reload the full Brief, history or raw prior logs",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, routing)
        common = read("runtime/common.md")
        self.assertIn("At a substantial checkpoint and before final verification", common)
        self.assertIn("fresh-owner continuation", common)
        autonomous = read("runtime/autonomous.md")
        self.assertIn("Delegate a bounded low/standard outcome", autonomous)
        self.assertIn("verified checkpointed inventory or classification", autonomous)
        planned = read("runtime/planned.md")
        self.assertIn("Classify failures found during owner validation", planned)
        self.assertIn("fix local low/standard failures and repeat until green", planned)
        self.assertIn("fresh-owner continuation", planned)

    def test_claude_standard_worker_profile_and_methodology_boundary(self):
        mapping = section(read("references/claude-tools.md"), "Planned Build")
        current, legacy = mapping.split("### Legacy delegated resume", 1)
        rows = re.findall(
            r"^\| `(low|standard|high)` \| (.*?) \| (.*?) \|$", current, re.M
        )
        self.assertEqual(rows, [
            ("low", "`claude-opus-5`", "`low`"),
            ("standard", "`claude-opus-5`", "`low`"),
            ("high", "Main-session orchestrator", "Current session setting"),
        ])
        self.assertIn('subagent_type: "absolutforge:planned-worker"', current)
        self.assertIn("one fresh call per task", current)
        self.assertIn("This fallback never applies to legacy delegated state", current)
        self.assertIn("does not switch it automatically", current)
        self.assertIn("High tasks and high-risk corrections stay with the main-session", current)
        self.assertIn('subagent_type: "absolutforge:delegated-executor"', legacy)
        self.assertIn("never edits production code or tests", legacy)
        self.assertIn("stop without starting or continuing implementation", legacy)
        for name in ("planned-worker", "delegated-executor"):
            descriptor = read(f"agents/{name}.md")
            frontmatter = descriptor.split("---", 2)[1]
            for field, expected in (
                ("name", name), ("model", "claude-opus-5"), ("effort", "low"),
                ("tools", "Read, Edit, Write, Bash, Glob, Grep"),
            ):
                self.assertEqual(re.search(rf"^{field}: (.+)$", frontmatter, re.M).group(1), expected)
        worker = read("agents/planned-worker.md")
        self.assertIn("implementation, wiring and focused tests", worker)
        self.assertIn("fix local failures inside Own", worker)
        self.assertIn("repeat the focused gate until green", worker)
        self.assertIn("Write only inside Own", worker)
        self.assertIn("Never accept legacy delegated work or high-tier responsibilities", worker)
        self.assertIn("do not compensate by broad redesign", worker)
        self.assertIn("do not use for new plans", read("agents/delegated-executor.md"))

    def test_claude_effective_profile_overrides_and_fallback_are_explicit(self):
        mapping = read("references/claude-tools.md")
        profile = section(mapping, "Effective executor profile")
        for obligation in (
            "before dispatching either named executor",
            "CLAUDE_CODE_EFFORT_LEVEL` must be unset or `low`",
            "CLAUDE_CODE_SUBAGENT_MODEL_FORCE` is unset",
            "CLAUDE_CODE_SUBAGENT_MODEL_FORCE` is exactly `1`",
            "CLAUDE_CODE_SUBAGENT_MODEL` to be exactly `claude-opus-5`",
            "any other non-empty force value as unsupported",
            "Do not unset or rewrite the user's environment automatically",
            "new standard work uses the reported main-session fallback",
            "legacy delegated work stops before implementation",
        ):
            self.assertIn(obligation, profile)
        self.assertIn("validate its effective profile below", mapping)
        self.assertIn("validate the effective profile below", mapping)

    def test_coherent_task_design_preserves_boundaries_and_verification(self):
        design = section(read("references/planned-build-contract.md"), "Task design")
        for obligation in (
            "For new standard plans", "implementation, wiring and focused tests",
            "settled shared contracts", "explicit production/test ownership",
            "meaningful fast gate and a return boundary",
            "Do not split solely by file, layer or code-versus-test work",
            "do not merge unrelated outcomes", "No fixed file/task count",
            "split coherently or escalate", "Grouping never removes targeted final integration checks",
            "revising pending tasks requires a canonical PC entry",
            "Legacy delegated ownership and decomposition rules remain authoritative",
        ):
            self.assertIn(obligation, design)
        routing = section(read("references/planned-build-contract.md"), "Capability routing")
        self.assertIn("high-tier corrections owned by the orchestrator", routing)
        runtime = read("runtime/planned.md")
        self.assertIn("group implementation, wiring and focused tests", runtime)
        self.assertIn("higher reasoning effort does not lower task risk", runtime)
        self.assertIn("shared writable paths execute sequentially", runtime)
        # Provider-specific policy must stay in the active host mapping.
        for path in ("references/planned-build-contract.md", "references/model-routing.md",
                     "runtime/planned.md", "skills/build/SKILL.md"):
            self.assertNotRegex(read(path), r"gpt-5\.6|Luna|Terra|Sol|xhigh")

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
                    self.assertTrue(data["version"].startswith("0.8.0"))
        self.assertEqual(json.loads(read("package.json"))["pi"]["skills"], ["skills"])
        self.assertEqual(
            json.loads(read(".codex-plugin/plugin.json"))["skills"], "./skills/"
        )


if __name__ == "__main__":
    unittest.main()
