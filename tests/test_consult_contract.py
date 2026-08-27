"""Deterministic contract checks for the explicit-only consult skill."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "consult" / "SKILL.md"
CODEX_UI = ROOT / "skills" / "consult" / "agents" / "openai.yaml"


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


class ConsultSkillContractTests(unittest.TestCase):
    def test_material_finding_batch_AC5(self) -> None:
        """[AC-5] Consult returns one bounded, evidence-backed finding batch."""
        _, body = _frontmatter_and_body(SKILL)
        lowered = body.lower()
        self.assertRegex(lowered, r"one bounded (?:finding )?batch")
        for category in (
            "ambiguity",
            "contradiction",
            "evidence gap",
            "grounded risk",
            "unnecessary scope",
        ):
            self.assertIn(category, lowered)
        for field in ("evidence", "impact", "proposed brief change"):
            self.assertIn(field, lowered)
        self.assertRegex(body, r"(?i)stable (?:finding )?id|finding id")

    def test_explicit_approval_mutation_AC6(self) -> None:
        """[AC-6] Only explicitly accepted findings mutate a Draft or Ready Brief."""
        _, body = _frontmatter_and_body(SKILL)
        lowered = body.lower()
        self.assertRegex(lowered, r"explicit(?:ly)? (?:accept|approv)")
        self.assertRegex(lowered, r"(?:finding )?id")
        self.assertRegex(lowered, r"whole (?:finding )?batch|complete batch")
        self.assertRegex(body, r"(?i)Draft.*(?:merge|update)|(?:merge|update).*Draft")
        self.assertRegex(body, r"(?i)Ready.*amendment|amendment.*Ready")
        self.assertRegex(lowered, r"(?:unselected|rejected).* (?:not|never).*(?:mutat|chang|appl)")
        self.assertRegex(lowered, r"no (?:durable )?(?:consultation )?(?:report|artifact)")

    def test_building_and_review_states_stop_AC10(self) -> None:
        """[AC-10] Building and In Review stop without mutation and route to discuss."""
        _, body = _frontmatter_and_body(SKILL)
        lowered = body.lower()
        self.assertIn("Draft", body)
        self.assertIn("Ready", body)
        self.assertIn("Building", body)
        self.assertIn("In Review", body)
        self.assertRegex(lowered, r"accepts? only.*draft.*ready|only.*(?:draft|ready).*(?:brief|input)")
        self.assertRegex(lowered, r"building.*(?:stop|reject|not mutate|no mutation)")
        self.assertRegex(lowered, r"in review.*(?:stop|reject|not mutate|no mutation)")
        self.assertRegex(lowered, r"(?:return|route).*discuss")

    def test_no_findings_and_deduplication_AC11(self) -> None:
        """[AC-11] No findings and already-recorded findings produce no writes or artifact."""
        _, body = _frontmatter_and_body(SKILL)
        lowered = body.lower()
        self.assertIn("no material findings", lowered)
        self.assertRegex(lowered, r"no (?:brief )?(?:content )?(?:writes?|mutation|changes?)")
        self.assertRegex(lowered, r"deduplicat|already represented|existing (?:accepted )?(?:decision|amendment)")
        self.assertRegex(lowered, r"no (?:durable )?(?:consultation )?(?:report|artifact)")

    def test_untrusted_content_and_secret_redaction_AC12_AC13(self) -> None:
        """[AC-12] [AC-13] Consult treats content as untrusted and redacts secrets."""
        _, body = _frontmatter_and_body(SKILL)
        lowered = body.lower()
        self.assertRegex(lowered, r"untrusted (?:evidence|content)")
        self.assertRegex(lowered, r"cannot (?:authorize|override)|never.*(?:authorize|override)")
        self.assertRegex(lowered, r"secret|credential|token|private key")
        self.assertRegex(lowered, r"redact|never copy|do not quote")

    def test_ready_changes_use_amendments_AC14(self) -> None:
        """[AC-14] Accepted Ready changes are amendments and rejected findings preserve baseline."""
        _, body = _frontmatter_and_body(SKILL)
        lowered = body.lower()
        self.assertRegex(lowered, r"ready.*immutable|immutable.*ready")
        self.assertRegex(lowered, r"accepted.*(?:material )?intent.*amendment|amendment.*accepted")
        self.assertRegex(lowered, r"original.*baseline|baseline.*unchanged|baseline.*preserv")
        self.assertRegex(lowered, r"rejected.*(?:leave|keep).*(?:unchanged|baseline)")
        self.assertIn("## Amendments", body)

    def test_optional_explicit_only_AC15(self) -> None:
        """[AC-15] Consult is optional and explicit-only on Claude and Codex."""
        frontmatter, body = _frontmatter_and_body(SKILL)
        self.assertEqual(_frontmatter_value(frontmatter, "name"), "consult")
        self.assertEqual(_frontmatter_value(frontmatter, "disable-model-invocation"), "true")
        ui = CODEX_UI.read_text(encoding="utf-8")
        self.assertEqual(_yaml_value(ui, "allow_implicit_invocation"), "false")
        self.assertIn("$consult", ui)
        lowered = body.lower()
        self.assertRegex(lowered, r"explicit(?:-only| invocation)")
        self.assertRegex(lowered, r"optional")
        self.assertRegex(lowered, r"never.*(?:gate|required|mandatory).*(?:build|discuss)")

    def test_input_validation_and_canonical_contracts(self) -> None:
        """Consult validates paths/statuses and links canonical schema owners."""
        _, body = _frontmatter_and_body(SKILL)
        lowered = body.lower()
        self.assertIn("references/artifact-contracts.md", body)
        self.assertIn("references/harness-command-contract.md", body)
        self.assertRegex(lowered, r"repository-relative")
        self.assertRegex(lowered, r"missing|malformed|invalid")
        self.assertRegex(lowered, r"complete brief|read.*brief")
        self.assertRegex(lowered, r"current (?:repository )?context|current code|adr")

    def test_brief_schema_uses_headings_and_status_without_yaml_frontmatter(self) -> None:
        """Canonical Brief validation uses required headings/status, not Brief YAML frontmatter."""
        _, body = _frontmatter_and_body(SKILL)
        self.assertIn("canonical required headings", body.lower())
        self.assertIn("## Status", body)
        self.assertNotRegex(body, r"(?i)(?:YAML\s+)?frontmatter")

    def test_no_automatic_build_or_persistent_consultation_report(self) -> None:
        """Consult remains a bounded opinion, not an automatic build or report stage."""
        _, body = _frontmatter_and_body(SKILL)
        lowered = body.lower()
        self.assertRegex(lowered, r"never.*(?:auto(?:matically)?|automatically).*(?:build|chain)")
        self.assertRegex(lowered, r"no (?:durable )?(?:consultation )?(?:report|artifact)")


if __name__ == "__main__":
    unittest.main()
