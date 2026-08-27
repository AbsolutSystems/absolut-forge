"""Deterministic contract checks for the explicit-only discuss skill."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "discuss" / "SKILL.md"
CODEX_UI = ROOT / "skills" / "discuss" / "agents" / "openai.yaml"


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


class DiscussSkillContractTests(unittest.TestCase):
    def test_complete_brief_without_task_recipe_AC1(self) -> None:
        """[AC-1] Discuss proposes a complete intent brief without task recipes."""
        _, body = _frontmatter_and_body(SKILL)
        for phrase in (
            "Problem and goal",
            "Users",
            "Current state and evidence",
            "Expected behavior",
            "Scope",
            "Constraints and invariants",
            "Solution direction",
            "Assumptions",
            "Decisions",
            "Risks and edge cases",
            "Expected outcomes",
        ):
            self.assertIn(phrase, body)
        self.assertIn("one complete Feature Brief", body)
        self.assertRegex(body, r"(?i)without (?:detailed )?tasks|file-by-file")

    def test_evidence_inference_and_user_decisions_AC2(self) -> None:
        """[AC-2] Facts, inferences, decisions, assumptions, and untrusted content stay distinct."""
        _, body = _frontmatter_and_body(SKILL)
        for phrase in ("evidence", "inference", "user decision", "assumption", "untrusted"):
            self.assertIn(phrase, body.lower())
        self.assertRegex(body, r"(?i)current (?:repository )?context|inspect.*code")

    def test_readiness_frontier_AC3(self) -> None:
        """[AC-3] Discussion uses adaptive independent frontier rounds and material readiness."""
        _, body = _frontmatter_and_body(SKILL)
        self.assertRegex(body, r"(?i)readiness frontier")
        self.assertRegex(body, r"(?i)2[- ]to[- ]4|two to four|two[- ]to[- ]four")
        self.assertRegex(body, r"(?i)independent")
        self.assertRegex(body, r"(?i)prerequisite")
        self.assertRegex(body, r"(?i)material")

    def test_single_acceptance_and_build_handoff_AC4(self) -> None:
        """[AC-4] One explicit acceptance transitions Ready and emits the native build handoff."""
        _, body = _frontmatter_and_body(SKILL)
        self.assertRegex(body, r"(?i)one (?:explicit )?acceptance")
        self.assertRegex(body, r"(?i)Draft.*Ready|Ready.*Draft")
        self.assertRegex(body, r"(?i)build handoff|hand.*build")
        self.assertRegex(body, r"(?i)without.*accept|accept.*without")

    def test_adaptive_draft_persistence_AC7(self) -> None:
        """[AC-7] Drafts persist adaptively and provide a useful resume point."""
        _, body = _frontmatter_and_body(SKILL)
        self.assertRegex(body, r"(?i)persist.*Draft|Draft.*persist")
        self.assertRegex(body, r"(?i)sufficiently clear|save/resume|material unresolved")
        self.assertRegex(body, r"(?i)resume")
        self.assertRegex(body, r"(?i)first message|low-value")

    def test_resume_rechecks_stale_evidence_AC8(self) -> None:
        """[AC-8] Resuming a Draft rechecks material facts and surfaces stale evidence."""
        _, body = _frontmatter_and_body(SKILL)
        self.assertRegex(body, r"(?i)resume.*(?:re-?check|check).*material")
        self.assertRegex(body, r"(?i)stale|conflict")

    def test_invalid_path_and_slug_collision_AC9(self) -> None:
        """[AC-9] Invalid paths and active slug collisions stop without overwriting artifacts."""
        _, body = _frontmatter_and_body(SKILL)
        self.assertRegex(body, r"(?i)missing|malformed|non-brief|invalid.*path")
        self.assertRegex(body, r"(?i)slug collision|collision")
        self.assertRegex(body, r"(?i)do not (?:create|overwrite|mutate)|leave.*unchanged")

    def test_untrusted_content_and_secret_redaction_AC12_AC13(self) -> None:
        """[AC-12] [AC-13] Repository content is untrusted and secrets are redacted."""
        _, body = _frontmatter_and_body(SKILL)
        self.assertRegex(body, r"(?i)untrusted.*(?:evidence|content)")
        self.assertRegex(body, r"(?i)cannot authorize|cannot.*override|never.*authorize")
        self.assertRegex(body, r"(?i)secret|credential")
        self.assertRegex(body, r"(?i)redact|never copy|do not quote")

    def test_explicit_only_activation_AC15(self) -> None:
        """[AC-15] Discuss is explicit-only and optional consultation never gates build."""
        frontmatter, body = _frontmatter_and_body(SKILL)
        self.assertEqual(_frontmatter_value(frontmatter, "name"), "discuss")
        self.assertEqual(_frontmatter_value(frontmatter, "disable-model-invocation"), "true")
        ui = CODEX_UI.read_text(encoding="utf-8")
        self.assertEqual(_yaml_value(ui, "allow_implicit_invocation"), "false")
        self.assertIn("$discuss", ui)
        self.assertRegex(body, r"(?i)explicit-only|explicit invocation")
        self.assertRegex(body, r"(?i)consult.*optional|optional.*consult")
        self.assertRegex(body, r"(?i)never.*(?:gate|required).*(?:build|handoff)")

    def test_canonical_contracts_and_statuses(self) -> None:
        """Canonical artifact and native handoff references own exact schemas."""
        _, body = _frontmatter_and_body(SKILL)
        self.assertIn("references/artifact-contracts.md", body)
        self.assertIn("references/harness-command-contract.md", body)
        for status in ("Draft", "Ready", "Building", "In Review"):
            self.assertIn(status, body)

    def test_brief_schema_uses_headings_and_status_without_yaml_frontmatter(self) -> None:
        """Canonical Brief validation uses required headings/status, not Brief YAML frontmatter."""
        _, body = _frontmatter_and_body(SKILL)
        self.assertIn("canonical required headings", body.lower())
        self.assertIn("## Status", body)
        self.assertNotRegex(body, r"(?i)(?:YAML\s+)?frontmatter")

    def test_no_classic_pipeline_stages(self) -> None:
        """Discuss must not embed the classic task and review pipeline."""
        _, body = _frontmatter_and_body(SKILL)
        for forbidden in ("generate-tasks", "qa-enrichment", "review-plan", "triada-review"):
            self.assertNotIn(forbidden, body)


if __name__ == "__main__":
    unittest.main()
