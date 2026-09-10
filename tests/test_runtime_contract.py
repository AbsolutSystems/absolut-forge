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

    def test_bare_discuss_recovers_active_conversation_without_accepting_it(self):
        discuss = read("skills/discuss/SKILL.md")
        for obligation in (
            "When invoked without arguments",
            "most recent coherent product or change topic",
            "including later user corrections and constraints",
            "Treat user messages as intent evidence",
            "only as proposals or inference",
            "conversation context actually available in the active thread",
            "ask one targeted question before writing an artifact",
            "A bare invocation supplies context, not acceptance",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, discuss)

        commands = read("references/harness-command-contract.md")
        for bare in (
            "/absolutforge:discuss\n",
            "$absolutforge discuss\n",
            "/skill:discuss\n",
        ):
            self.assertIn(bare, commands)
        self.assertIn("most recent coherent product/change topic", commands)
        self.assertIn("does not imply access to other threads", commands)

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

    def test_feature_family_identity_and_archive_manifest_are_durable(self):
        artifacts = read("references/artifact-contracts.md")
        brief = section(artifacts, "Feature Brief")
        manifest = section(artifacts, "Feature Family manifest")
        discuss = read("skills/discuss/SKILL.md")
        ship = read("skills/ship/SKILL.md")

        for field in (
            "## Feature family",
            "Family slug: standalone | {family-slug}",
            "Family name: not applicable | {family name}",
            "Phase: not applicable | P{NN}",
            "Lineage: standalone | new family",
        ):
            self.assertIn(field, brief)
        for obligation in (
            "Historical Briefs without it remain valid",
            "A branch name is never family identity",
        ):
            self.assertIn(obligation, brief)
        for obligation in (
            "archives/families/{family-slug}/feature-family.md",
            "Existing record paths never move",
            "exactly one matching manifest entry",
            "every manifest entry must resolve",
        ):
            self.assertIn(obligation, manifest)
        self.assertIn("current branch may rank candidates but never defines", discuss)
        self.assertIn("acceptance covers that durable grouping", discuss)
        self.assertIn("never infer family identity from its branch or slug", ship)
        self.assertIn("Validate both directions of membership", ship)

    def test_ship_indexes_actionable_review_followups_once(self):
        followups = section(
            read("references/artifact-contracts.md"), "Follow-up register"
        )
        ship = read("skills/ship/SKILL.md")
        for obligation in (
            "absolutforge/follow-ups.md",
            "`open` or `deferred`",
            "`fixed` and `accepted`",
            "FU-{NNN}",
            "never reused",
            "source tuple",
            "does not assign priority, owner or deadline",
            "one closeout set",
        ):
            self.assertIn(obligation, followups)
        for obligation in (
            "first actionable follow-up ships",
            "next never-reused global `FU-{NNN}`",
            "Reuse an identical source entry on retry",
            "do not treat registration as scope acceptance",
            "one closeout set before staging",
        ):
            self.assertIn(obligation, ship)

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

    def test_build_scout_rule_improves_owned_code_without_scope_drift(self):
        artifacts = read("references/artifact-contracts.md")
        scout = section(artifacts, "Scout rule")
        for obligation in (
            "leaves the code its assigned executor already touches better than it",
            "current autonomous outcome or planned task's owned",
            "unambiguous, localized and low risk",
            "preserves accepted behavior, public contracts, compatibility",
            "focused proof",
            "Otherwise do not edit it",
            "concise scout observation",
            "`Scout disposition`",
            "do not enter the global",
            "follow-up register unless Review",
            "complete diff",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, scout)

        common = read("runtime/common.md")
        self.assertIn("Apply the canonical Scout rule", common)
        self.assertIn("assigned executor may immediately fix", common)
        self.assertIn("owner never implements the fix", common)
        self.assertIn("Report the fix after completing it", common)

        self.assertIn("assigned executor already touches", scout)
        self.assertIn("never implements a production-code or test Scout fix", scout)

        autonomous = read("runtime/autonomous.md")
        self.assertIn("canonical Scout boundary in every package", autonomous)
        self.assertIn("plus any scout fix or deferred observation", autonomous)
        self.assertIn("Scout disposition", autonomous)

        planned = read("runtime/planned.md")
        self.assertIn("canonical Scout rule in Must preserve and Return", planned)
        self.assertIn("Scout work never expands Own", planned)

        capsule = section(read("references/planned-build-contract.md"), "Task Capsule")
        self.assertIn("qualifying maintenance fix only inside `Own`", capsule)
        self.assertIn("cross-owner observations without editing them", capsule)

        self.assertIn("canonical Scout rule", read("skills/build/SKILL.md"))
        self.assertIn("Build owner never implements a Scout fix", read("skills/build/SKILL.md"))
        worker = read("agents/planned-worker.md")
        self.assertIn("Apply the capsule's Scout boundary", worker)
        self.assertIn("report larger, behavior-changing or cross-owner observations", worker)

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
            "fresh high-capability generic read-only reviewer",
            "inline pass is valid only in a high-capability context",
            "otherwise stop before writing Review",
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
            ("standard", "`gpt-5.6-luna`", "`high`"),
            ("high", "`gpt-5.6-luna`", "`max`"),
        ])
        for obligation in (
            "For new standard planned builds",
            "selected Build owner",
            "explicit model and reasoning-effort overrides for every worker",
            'fork_turns="none"',
            "exact requested worker profile is unavailable",
            "never silently substitute another worker model/effort",
            "never edits production code or tests",
            "stop at the last clean boundary",
            "Luna `max` owns high execution",
            "assumptions, containment, rollback when applicable and intermediate proof points",
            "Pending standard tasks adopt this worker-owned mapping on resume",
            "historical pending `high` task first receives Risk controls",
            "Each Luna worker fixes local failures and repeats its focused gate",
            "Corrections discovered later by owner validation or final verification",
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

    def test_codex_owner_selection_and_bounded_advice_contract(self):
        owner = section(read("references/codex-tools.md"), "Build owner")
        rows = re.findall(r"^\| (.*?) \| (.*?) \|$", owner, re.M)
        actions = dict(rows[2:])
        self.assertEqual(set(actions), {
            "`gpt-5.6-luna` with `xhigh` reasoning",
            "`gpt-5.6-terra` with any current reasoning effort",
            "Any other or unconfirmed profile",
        })
        self.assertIn("no launcher or owner spawn", actions["`gpt-5.6-luna` with `xhigh` reasoning"])
        self.assertIn("preserve that effort", actions["`gpt-5.6-terra` with any current reasoning effort"])
        self.assertIn("fresh `gpt-5.6-luna` owner with `xhigh`", actions["Any other or unconfirmed profile"])
        for obligation in (
            "effective model and reasoning effort reported for the active session",
            "not a config default",
            "never recursively dispatch another owner to repair confirmation",
            "role marker alone is not proof of the effective profile",
            "Legacy delegated resumes keep a fresh `gpt-5.6-sol` owner",
            "Do not route legacy ownership through the standard table",
            "does not merge owner and worker write authority",
            "stop before Build mutation",
            "no conversation is inherited",
            "only the `ROTATE` control envelope",
            "its existence alone never triggers rotation",
            "does not by itself force an eligible session to spawn",
            "becomes the launcher for one fresh successor",
            "never build a nested successor chain",
            "only the owner marker and canonical command are passed",
            "fresh read-only `gpt-5.6-sol` advisor with `medium` reasoning",
            "Give the advisor read-only repository access",
            "does not edit, commit, inherit the Build conversation or take over execution",
            "stop the dependent work at the last clean boundary",
            "do not call `list_agents` first",
            "absent from the actual tool registry",
            "direct attempted dispatch with the required model and reasoning effort",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, owner)
        entry = read("skills/build/SKILL.md")
        self.assertIn("Before loading runtime or repository evidence", entry)
        self.assertIn("select an in-session or freshly dispatched Build owner", entry)
        self.assertIn("compaction does not provide independence", read("references/planned-build-contract.md"))

    def test_decision_advice_and_verification_reuse_preserve_gates(self):
        advice = section(read("references/model-routing.md"), "Decision advice")
        for obligation in (
            "authorization/security", "data integrity", "migration strategy",
            "public-contract compatibility", "concurrency/state transitions",
            "conflicting requirements/evidence", "two attempts have failed",
            "documentation-only", "confidence alone never waives a mandatory trigger",
            "reconsult when relevant evidence invalidates an assumption",
            "rather than issuing a substantially identical third capsule",
            "not the advisor's sole evidence", "Required advice must complete",
            "never replaces independent Review",
        ):
            self.assertIn(obligation, advice)
        for path in ("runtime/common.md", "references/codex-tools.md", "references/planned-build-contract.md"):
            self.assertIn("model-routing.md#decision-advice", read(path))
        doctrine = read("references/verification-doctrine.md")
        for obligation in (
            "checks run by the owner as well as workers",
            "relevant dependencies/environment, exact command and result",
            "distinct accepted path requires fresh-state proof",
            "checkpoint, owner rotation or entry into final verification alone",
            "exact final operation was exercised",
        ):
            self.assertIn(obligation, doctrine)

    def test_codex_build_owner_reports_progress_without_inheriting_supervision(self):
        owner = section(read("references/codex-tools.md"), "Build owner")
        for obligation in (
            "compact user-facing `STATUS:` message",
            "no five-minute period passes without an update",
            "what completed, what is happening now, what comes next, and any blocker",
            "waits in intervals short enough to enforce that deadline",
            "requests a status without interrupting the owner",
            "using only the last confirmed stage",
            "not Build evidence",
            "never passed to a successor owner",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, owner)

    def test_compiler_first_routing_separates_decisions_from_execution(self):
        routing = section(read("references/model-routing.md"), "Autonomous outcome routing")
        for obligation in (
            "dispatches one fresh worker for all production-code and test edits",
            "mixed outcome is not wholly `high`",
            "genuinely high execution remains worker-owned",
            "settled decision, assumptions, containment, rollback when applicable",
            "never takes over production-code or test edits",
            "repetitive inventories, matrices, report rows",
            "treat it as durable evidence",
            "worker owns the local implementation loop",
            "repeat that gate until green",
            "run and report every intermediate proof obligation",
            "When owner validation or final verification discovers a failure",
            "settled API-usage corrections retain their tier",
            "then to a fresh worker for any production-code or test edit",
            "Never reload the full Brief, history or raw prior logs",
            "stop at the last clean boundary",
            "never substitute a profile, implement inline or claim delegation",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, routing)
        common = read("runtime/common.md")
        self.assertIn("A checkpoint alone does not require a fresh owner", common)
        self.assertIn("value-triggered continuation", common)
        autonomous = read("runtime/autonomous.md")
        self.assertIn("just-in-time compilation", autonomous)
        self.assertIn("Dispatch every bounded low, standard or high outcome", autonomous)
        self.assertIn("never edits production code or tests", autonomous)
        self.assertIn("failure containment, rollback when applicable", autonomous)
        self.assertIn("verified checkpointed inventory or classification", autonomous)
        planned = read("runtime/planned.md")
        self.assertIn("Classify failures found during owner validation", planned)
        self.assertIn("fix local failures and repeat until green", planned)
        self.assertIn("every low, standard and high production-code or test task", planned)
        self.assertIn("never implements them", planned)
        self.assertIn("two failed attempts at the same blocker", planned)
        self.assertIn("does not itself require rotation", planned)
        self.assertIn("active host's value triggers", planned)
        self.assertIn("older standard runtime began a task inline", planned)
        self.assertIn("historical `high` task without Risk controls", planned)

    def test_claude_standard_worker_profile_and_methodology_boundary(self):
        mapping = section(read("references/claude-tools.md"), "Planned Build")
        current, legacy = mapping.split("### Legacy delegated resume", 1)
        rows = re.findall(
            r"^\| `(low|standard|high)` \| (.*?) \| (.*?) \|$", current, re.M
        )
        self.assertEqual(rows, [
            ("low", "`claude-opus-5`", "`low`"),
            ("standard", "`claude-opus-5`", "`low`"),
            ("high", "`claude-opus-5`", "`low`"),
        ])
        self.assertIn('subagent_type: "absolutforge:planned-worker"', current)
        self.assertIn("one fresh call per task", current)
        self.assertIn("does not switch it automatically", current)
        self.assertIn("every low, standard and high task", current)
        self.assertIn("High execution also requires the owner-settled decision", current)
        self.assertIn("never silently substitute another worker model/effort, implement in the main session", current)
        self.assertIn("Pending standard tasks adopt this worker-owned mapping on resume", current)
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
        self.assertIn("Accept high execution risk only with settled decisions", worker)
        self.assertIn("Never accept legacy delegated work", worker)
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
            "both new standard and legacy delegated work stop before implementation",
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
            "Do not encode an unresolved high-tier decision inside an implementation task",
            "Classify the resulting task on its execution risk",
            "Such a task stays worker-owned",
            "must carry explicit Risk controls",
            "do not merge unrelated outcomes", "No fixed file/task count",
            "split coherently or return the unresolved decision", "Grouping never removes targeted final integration checks",
            "Other pending definition changes still require a PC entry",
            "Legacy delegated ownership and decomposition rules remain authoritative",
        ):
            self.assertIn(obligation, design)
        routing = section(read("references/planned-build-contract.md"), "Capability routing")
        self.assertIn("Decision risk and execution risk are separate", routing)
        self.assertIn("every production-code and test correction returns to a fresh bounded worker", routing)
        self.assertIn("Two failed attempts at the same blocker", routing)
        self.assertIn("pending standard tasks adopt the worker-owned runtime boundary", design)
        self.assertIn("pending `high` task created before `Risk controls` existed", design)
        runtime = read("runtime/planned.md")
        self.assertIn("group implementation, wiring and focused tests", runtime)
        self.assertIn("classify the resulting implementation on its own execution risk", runtime)
        self.assertIn("does not inherit `high` solely from an enclosing outcome", runtime)
        self.assertIn("higher reasoning effort does not lower task risk", runtime)
        self.assertIn("shared writable paths execute sequentially", runtime)
        # Provider-specific policy must stay in the active host mapping.
        for path in ("references/planned-build-contract.md", "references/model-routing.md",
                     "runtime/planned.md", "skills/build/SKILL.md"):
            self.assertNotRegex(read(path), r"gpt-5\.6|Luna|Terra|Sol|xhigh")

    def test_review_routes_corrections_through_owner_compilation_and_workers(self):
        review = section(read("runtime/review.md"), "Record and route")
        self.assertIn("Build owner classifies each blocker", review)
        self.assertIn("settles any decision it exposes", review)
        self.assertIn("every production-code or test edit returns to a fresh worker", review)
        self.assertIn("Review never reopens the plan itself or dispatches an executor", review)
        self.assertIn("After two evidenced failed correction attempts", review)

        autonomous = section(read("runtime/autonomous.md"), "Final verification")
        self.assertIn("owner classifies each final-verification failure", autonomous)
        self.assertIn("dispatches a fresh worker for every production-code or test correction", autonomous)

        codex_review = section(read("references/codex-tools.md"), "Review")
        for obligation in (
            "fresh read-only `gpt-6-astra` reviewer with `low` reasoning",
            'fork_turns="none"',
            "different model family from Luna execution",
            "fresh `gpt-5.6-sol` reviewer with `medium` reasoning",
            "no fresh high-capability reviewer",
            "advisory (not fully isolated)",
        ):
            self.assertIn(obligation, codex_review)

        host_review_obligations = {
            "claude": (
                "effective profile is guaranteed high-capability",
                "invoking Review context is itself high-capability",
                "stop before writing Review",
            ),
            "opencode": (
                "installation guarantees a high-capability profile",
                "invoking Review context is itself high-capability",
                "stop before writing Review",
            ),
            "pi": (
                "select a high-capability model/profile",
                "may record Review mode `fresh` only when its selected profile is high-capability",
                "stop before writing Review",
            ),
        }
        for host, obligations in host_review_obligations.items():
            mapping = section(
                read(f"references/{host}-tools.md"),
                "Clean-context Review" if host == "pi" else "Review"
                if host == "claude" else "Planned Build and Review dispatch",
            )
            for obligation in obligations:
                with self.subTest(host=host, obligation=obligation):
                    self.assertIn(obligation, mapping)

    def test_standard_build_is_executor_owned_across_hosts(self):
        shared = read("references/model-routing.md")
        self.assertIn("fresh workers own every production-code and test edit", shared)
        self.assertIn("Capability tier always changes preparation and validation intensity", shared)
        self.assertIn("when the active host mapping differentiates tiers", shared)
        self.assertIn("never changes that ownership boundary", shared)

        host_obligations = {
            "codex": ("never edits production code or tests", "stop at the last clean boundary"),
            "claude": ("every low, standard and high task", "implement in the main session"),
            "opencode": ("worker owns every production-code and test edit", "orchestrator implementation is unavailable"),
            "pi": ("executor-owned production-code and test edits", "never implement directly"),
        }
        for host, obligations in host_obligations.items():
            text = read(f"references/{host}-tools.md")
            for obligation in obligations:
                with self.subTest(host=host, obligation=obligation):
                    self.assertIn(obligation, text)

        legacy = read("references/planned-delegated-contract.md")
        self.assertIn("one fixed, lower-cost host-mapped executor profile", legacy)
        self.assertIn("orchestrator must not reserve implementation work for itself", legacy)

    def test_repeated_review_preserves_finding_identity_and_attempt_count(self):
        review = read("runtime/review.md")
        for obligation in (
            "existing `review.md`",
            "continuity registry",
            "same root issue",
            "new ID only for a distinct root issue",
            "Correction attempts",
            "two evidenced failed correction attempts",
            "Prior findings are navigation evidence, not authority",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, review)
        artifact = section(read("references/artifact-contracts.md"), "Review")
        self.assertIn("- Root issue:", artifact)
        self.assertIn("- Correction attempts:", artifact)
        codex = section(read("references/codex-tools.md"), "Review")
        self.assertIn("continuity registry from the existing `review.md`", codex)
        self.assertIn("never prior reviewer conclusions as authority", codex)

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
                    self.assertTrue(data["version"].startswith("0.12.0"))
        self.assertEqual(json.loads(read("package.json"))["pi"]["skills"], ["skills"])
        self.assertEqual(
            json.loads(read(".codex-plugin/plugin.json"))["skills"], "./skills/"
        )


if __name__ == "__main__":
    unittest.main()
