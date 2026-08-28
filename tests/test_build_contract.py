"""Deterministic conformance checks for the explicit-only Build skill.

These tests intentionally scan the contract text instead of invoking a model or
running a project workflow.  They protect the product boundary and keep the
implementation prompt linked to the canonical artifact contracts.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "build" / "SKILL.md"
CODEX_UI = ROOT / "skills" / "build" / "agents" / "openai.yaml"
ARTIFACTS = ROOT / "references" / "artifact-contracts.md"
HANDOFF = ROOT / "references" / "harness-command-contract.md"
DOCS = tuple(ROOT / path for path in ("README.md", "CLAUDE.md", "docs/product-vision.md", "skills/README.md"))


def _frontmatter_and_body(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"missing frontmatter in {path}")
    marker = text.find("\n---\n", 4)
    if marker < 0:
        raise AssertionError(f"unterminated frontmatter in {path}")
    return text[4:marker], text[marker + len("\n---\n") :]


def _frontmatter_value(frontmatter: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        raise AssertionError(f"missing frontmatter key {key}")
    return match.group(1).strip().strip('"').strip("'")


def _yaml_value(text: str, key: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", text)
    if not match:
        raise AssertionError(f"missing YAML key {key}")
    return match.group(1).strip().strip('"').strip("'")


def _json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object in {path}")
    return value


class BuildSkillContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.frontmatter, self.body = _frontmatter_and_body(SKILL)
        # Contract assertions should not depend on Markdown line wrapping.
        self.body = re.sub(r"\s+", " ", self.body)
        self.artifacts = ARTIFACTS.read_text(encoding="utf-8")
        self.handoff = re.sub(r"\s+", " ", HANDOFF.read_text(encoding="utf-8"))

    def test_ready_lifecycle_AC1(self) -> None:
        """[AC-1] Build validates Ready input and records the Building lifecycle."""
        self.assertEqual(_frontmatter_value(self.frontmatter, "name"), "build")
        for status in ("Ready", "Building", "In Review"):
            self.assertIn(status, self.body)
        self.assertRegex(self.body, r"(?i)Ready.*valid.*start|valid.*start.*Ready")
        self.assertRegex(self.body, r"(?i)change only its status to `?Building")
        self.assertRegex(self.body, r"(?i)Building Brief is a resume|Building.*resume")

    def test_map_threshold_and_resume_AC2_AC4(self) -> None:
        """[AC-2] [AC-4] Execution Maps are conditional, statusful, and resumable."""
        self.assertRegex(self.body, r"(?i)Do not create an Execution Map merely")
        self.assertRegex(self.body, r"(?i)multiple dependent outcomes|durable resume")
        for phrase in ("pending", "in-progress", "complete", "base_commit", "checkpoints", "append-only Build Evidence"):
            self.assertIn(phrase, self.body)
        self.assertRegex(self.body, r"(?i)resume from evidence|resume handoff")
        self.assertIn("Execution Map contract", self.artifacts)
        self.assertIn("base_commit", self.artifacts)

    def test_autonomous_verification_AC3_AC8(self) -> None:
        """[AC-3] [AC-8] Build owns focused and final verification and fixes."""
        self.assertIn("implement -> focused verification -> diagnosis -> bounded fix", self.body)
        self.assertRegex(self.body, r"(?i)focused tests and relevant checks immediately")
        self.assertRegex(self.body, r"(?is)final focused checks.*broader|broader.*once")
        self.assertRegex(self.body, r"(?i)whole final diff|whole-feature")
        self.assertRegex(self.body, r"(?is)only after this evidence and final verification succeed")
        self.assertRegex(
            self.handoff,
            r"base_commit\.\.HEAD|base_commit.*current worktree",
        )

    def test_failure_boundary_AC5_AC6_AC10_AC13(self) -> None:
        """[AC-5] [AC-6] [AC-10] [AC-13] Failure boundaries prevent speculative scope growth."""
        for phrase in ("failure", "same observable check or runtime symptom", "violated invariant", "Failure Boundary Check"):
            self.assertIn(phrase, self.body)
        self.assertRegex(self.body, r"(?i)accepted amendment becomes review baseline context")
        self.assertRegex(self.body, r"(?i)rejected amendment leaves the original baseline and change surface unchanged")
        self.assertRegex(self.body, r"(?i)Before a second repair attempt")
        self.assertRegex(self.body, r"(?is)causally maps.*expected invariant.*change surface")
        self.assertRegex(self.body, r"(?i)escalate before a second speculative repair")
        self.assertRegex(self.body, r"(?i)material scope expansion.*stop condition")
        self.assertRegex(self.body, r"(?i)explicit amendment or scope approval")
        self.assertRegex(self.body, r"(?i)ordinary.*do not require.*approval")
        self.assertRegex(self.body, r"(?i)inspect the initial worktree before feature edits")
        self.assertRegex(self.body, r"(?i)preserve dirty, non-overlapping changes")
        self.assertRegex(self.body, r"(?i)dirty changes overlap.*stop and explain the conflict")
        self.assertRegex(self.body, r"(?i)rather than overwriting or absorbing them")

    def test_scout_rule_AC11_AC12(self) -> None:
        """[AC-11] [AC-12] Scout fixes are trivial, reported, and bounded."""
        self.assertRegex(self.body, r"(?i)Apply the scout rule narrowly")
        self.assertRegex(self.body, r"(?i)strictly trivial adjacent defect")
        self.assertRegex(self.body, r"(?i)non-trivial adjacent work remains a follow-up")
        self.assertRegex(self.body, r"(?i)reported as a scout fix")
        self.assertRegex(self.body, r"(?i)fails in apparently untouched code")
        self.assertRegex(self.body, r"(?i)investigate and record the observable evidence")
        self.assertRegex(self.body, r"(?i)do not silently label it pre-existing or a feature regression")
        self.assertIn("Scout disposition", self.artifacts)

    def test_documentation_rule_AC7(self) -> None:
        """[AC-7] Public and critical internal documentation stays concise and truthful."""
        self.assertRegex(self.body, r"(?i)public APIs and critical internal behavior documented")
        self.assertRegex(self.body, r"(?i)concisely and truthfully")
        self.assertRegex(self.body, r"(?i)(?:correct or remove|stale or misleading documentation).*(?:stale or misleading documentation|corrected or removed)")
        self.assertIn("Documentation maintenance", self.artifacts)

    def test_invalid_input_AC9(self) -> None:
        """[AC-9] Invalid paths, statuses, and malformed Briefs stop before mutation."""
        self.assertRegex(self.body, r"(?i)repository-relative canonical path")
        for phrase in ("absolute paths", "path traversal", "missing files", "malformed", "Draft", "In Review"):
            self.assertIn(phrase, self.body)
        self.assertRegex(self.body, r"(?i)stop before mutation")
        self.assertRegex(self.body, r"(?i)stop without mutation")

    def test_advisor_escalation_AC14(self) -> None:
        """[AC-14] Optional Sol advice is bounded, read-only, and never overrides intent."""
        self.assertRegex(self.body, r"(?i)optional")
        self.assertRegex(self.body, r"(?i)read-only")
        self.assertIn("gpt-5.6-sol", self.body)
        self.assertRegex(self.body, r"(?i)smallest redacted package")
        self.assertRegex(self.body, r"(?i)diagnosis and options only")
        self.assertRegex(self.body, r"(?i)must not edit files.*commit.*push.*deploy")
        self.assertRegex(self.body, r"(?i)conflicts.*accepted Brief.*explicit amendment")

    def test_build_recommendation_AC4_AC5_AC6_AC7_AC8_AC11(self) -> None:
        """[AC-4] [AC-5] [AC-6] [AC-7] [AC-8] [AC-11] Build consumes advisory profiles with explicit evidence and no partial delivery."""
        self.assertIn("Consume the advisory Build Recommendation", self.body)
        self.assertIn("simple`/`single", self.body)
        self.assertIn("gpt-5.6-luna", self.body)
        self.assertIn("complex`/`phased", self.body)
        self.assertIn("gpt-5.6-terra", self.body)
        self.assertRegex(self.body, r"(?i)advisory execution hint")
        self.assertRegex(self.body, r"(?i)active harness.*explicit user choice")
        self.assertRegex(self.body, r"(?i)recommendation received.*actually used.*selection source")
        for reason in ("absent", "malformed", "mismatched", "unavailable", "not selected"):
            self.assertIn(reason, self.body)
        self.assertRegex(self.body, r"(?i)precise fallback reason")
        self.assertRegex(self.body, r"(?i)actor-supplied.*reason.*override")
        self.assertRegex(self.body, r"(?i)override is execution evidence, not a product")
        self.assertRegex(self.body, r"(?i)keep the Brief and its recommendation unchanged")
        self.assertRegex(self.body, r"(?i)explicit amendment")
        self.assertRegex(self.body, r"(?i)cannot authorize unrelated edits")
        self.assertRegex(self.body, r"(?i)deployment.*partial delivery")

    def test_selected_model_owns_build_and_escalation_AC4_AC8(self) -> None:
        """[AC-4] [AC-8] Both recommendation profiles retain Build and escalation ownership in the selected context."""
        for profile, model in (("simple`/`single", "gpt-5.6-luna"), ("complex`/`phased", "gpt-5.6-terra")):
            self.assertIn(profile, self.body)
            self.assertIn(model, self.body)
        self.assertRegex(self.body, r"(?i)Whichever model/profile is selected.*owns implementation.*verification.*Execution Map.*Build Evidence.*escalation decisions")
        self.assertRegex(self.body, r"(?i)active Build context may request.*gpt-5.6-sol")
        self.assertRegex(self.body, r"(?i)active Build context remains responsible for decisions, edits, escalation, and verification")
        self.assertNotRegex(self.body, r"(?i)Luna remains responsible")

    def test_recommendation_handoff_AC1_AC4_AC5_AC6_AC7_AC8_AC11(self) -> None:
        """[AC-1] [AC-4] [AC-5] [AC-6] [AC-7] [AC-8] [AC-11] Handoff preserves advisory metadata and immutable intent."""
        self.assertIn("optional `## Build Recommendation` travels", self.handoff)
        self.assertRegex(self.handoff, r"(?i)outside the immutable.*baseline")
        self.assertRegex(self.handoff, r"(?i)missing, malformed, unavailable, or overridden")
        self.assertRegex(self.handoff, r"(?i)fallback or override reason")
        self.assertRegex(self.handoff, r"(?i)never.*automatic model switching")
        self.assertRegex(self.handoff, r"(?i)never authorizes partial delivery")

    def test_untrusted_and_redaction_AC15(self) -> None:
        """[AC-15] Build is explicit-only, rejects untrusted instructions, and redacts secrets."""
        self.assertEqual(_frontmatter_value(self.frontmatter, "disable-model-invocation"), "true")
        ui = CODEX_UI.read_text(encoding="utf-8")
        self.assertEqual(_yaml_value(ui, "allow_implicit_invocation"), "false")
        self.assertIn("$build", ui)
        self.assertRegex(self.body, r"(?i)untrusted evidence")
        self.assertRegex(self.body, r"(?i)cannot override")
        self.assertRegex(self.body, r"(?i)Redact secrets|Redact\s+secrets|secrets.*redact")
        self.assertRegex(self.body, r"(?i)never copy them")
        for forbidden in ("deploy", "push", "creates a PR", "merge", "rewrites history"):
            self.assertIn(forbidden, self.body)

    def test_canonical_contract_links(self) -> None:
        """Build links to canonical schemas rather than duplicating artifact templates."""
        self.assertIn("references/artifact-contracts.md", self.body)
        self.assertIn("references/harness-command-contract.md", self.body)
        self.assertIn("canonical", self.body.lower())
        self.assertIn("Execution Map contract", self.artifacts)
        self.assertIn("Build Evidence contract", self.artifacts)

    def test_model_recommendation_docs_AC1_AC2_AC3_AC4_AC5_AC6_AC7_AC8_AC11(self) -> None:
        """[AC-1] [AC-2] [AC-3] [AC-4] [AC-5] [AC-6] [AC-7] [AC-8] [AC-11] Product docs expose advisory model guidance and boundaries."""
        documents = {
            path.relative_to(ROOT).as_posix(): re.sub(
                r"\s+", " ", path.read_text(encoding="utf-8")
            )
            for path in DOCS
        }
        readme = documents["README.md"]
        claude = documents["CLAUDE.md"]
        vision = documents["docs/product-vision.md"]
        skills = documents["skills/README.md"]

        self.assertIn("discuss -> build -> review -> ship", readme)
        self.assertRegex(readme, r"(?i)build.*implemented")
        self.assertRegex(readme, r"(?i)Execution Map")
        self.assertRegex(readme, r"(?i)base_commit")
        self.assertRegex(readme, r"(?i)never deploy|no partial")
        self.assertRegex(readme, r"(?i)AbsolutPowers.*(?:disabled|not active)")

        self.assertIn("discuss -> build -> review -> ship", vision)
        self.assertRegex(vision, r"(?i)build.*implemented")
        for phrase in ("Execution Map", "base_commit", "Failure Boundary Check", "read-only", "Sol", "concise", "truthful", "never deploy"):
            self.assertIn(phrase.lower(), vision.lower(), phrase)
        self.assertRegex(vision, r"(?i)focused.*final.*verification")

        self.assertRegex(claude, r"(?i)build.*contracts exist")
        for phrase in ("Failure Boundary Check", "read-only Sol", "concise and truthful", "never deploy", "partial outcome"):
            self.assertIn(phrase.lower(), claude.lower(), phrase)

        self.assertRegex(skills, r"(?i)build.*implemented")
        for phrase in ("Failure Boundary Check", "read-only Sol", "concise and truthful", "never deploy", "independently shippable"):
            self.assertIn(phrase.lower(), skills.lower(), phrase)

        for name, document in documents.items():
            self.assertIn("simple/single", document, name)
            self.assertIn("gpt-5.6-luna", document, name)
            self.assertIn("complex", document, name)
            self.assertIn("gpt-5.6-terra", document, name)
            self.assertRegex(document, r"(?i)advisory", name)
            self.assertRegex(document, r"(?i)(?:missing|malformed|unavailable).*fallback|fallback.*(?:missing|malformed|unavailable)", name)
            self.assertRegex(document, r"(?i)overr(?:ide|idden).*reason|reason.*overr(?:ide|idden)", name)
            self.assertRegex(document, r"(?i)outside immutable intent|outside the immutable intent", name)
            self.assertRegex(document, r"(?i)automatic(?:ally)? switch|automatically.*switch|automatic switching|switch.*automatically", name)
            self.assertRegex(document, r"(?i)partial delivery|partial result|partial outcome", name)


if __name__ == "__main__":
    unittest.main()
