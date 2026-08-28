"""Deterministic conformance checks for the explicit-only Review skill.

These tests inspect Markdown and Codex metadata only.  They deliberately do
not invoke a model, dispatch a reviewer, mutate a Feature Brief, or run the
Review workflow.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "review" / "SKILL.md"
CODEX_UI = ROOT / "skills" / "review" / "agents" / "openai.yaml"
ARTIFACTS = ROOT / "references" / "artifact-contracts.md"
HANDOFF = ROOT / "references" / "harness-command-contract.md"
ADR = ROOT / "docs" / "adr" / "2026-08-28-independent-review-and-bounded-fix-loop.md"
DOCS = tuple(
    ROOT / path
    for path in ("README.md", "CLAUDE.md", "docs/product-vision.md", "skills/README.md")
)


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


class ReviewSkillContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.frontmatter, body = _frontmatter_and_body(SKILL)
        self.body = re.sub(r"\s+", " ", body)
        self.artifacts = re.sub(r"\s+", " ", ARTIFACTS.read_text(encoding="utf-8"))
        self.handoff = re.sub(r"\s+", " ", HANDOFF.read_text(encoding="utf-8"))

    def test_lifecycle_AC1_AC6_AC7_AC8_AC9(self) -> None:
        """[AC-1] [AC-6] [AC-7] [AC-8] [AC-9] Review validates inputs and owns bounded lifecycle handoffs."""
        self.assertEqual(_frontmatter_value(self.frontmatter, "name"), "review")
        self.assertEqual(
            _frontmatter_value(self.frontmatter, "disable-model-invocation"), "true"
        )
        for phrase in (
            "accepted intent",
            "linked ADRs",
            "Build Evidence",
            "recorded `base_commit`",
            "only valid input status is `In Review`",
            "Draft",
            "Ready",
            "Building",
            "review.md",
            "Review pass",
            "set `review.md` to `Complete`",
            "Decision: Ready for ship",
        ):
            self.assertIn(phrase, self.body, phrase)
        self.assertRegex(self.body, r"(?i)stop before mutation|stops without mutation")
        self.assertRegex(self.body, r"(?i)malformed.*existing review|existing.*review.*validate")
        self.assertRegex(self.body, r"(?i)no open.*BLOCKING.*Complete|no `?BLOCKING`.*Complete")
        self.assertRegex(self.body, r"(?i)from `?In Review`? to `?Building`?")
        self.assertRegex(self.body, r"(?i)same.*base_commit.*current worktree")
        self.assertIn("references/artifact-contracts.md", self.body)
        self.assertIn("references/harness-command-contract.md", self.body)
        self.assertIn("review", self.handoff)
        self.assertIn("ship", self.handoff)
        self.assertIn("review.md", self.artifacts)

    def test_diff_scope_AC2_AC10_AC11(self) -> None:
        """[AC-2] [AC-10] [AC-11] Review derives a safe complete feature scope from base_commit and the current worktree."""
        for phrase in (
            "recorded `base_commit`",
            "current worktree",
            "committed, staged, unstaged, and feature-owned untracked",
            "review-process/generated process artifacts",
            "unrelated changes cannot be separated safely",
            "preserve the worktree",
            "generated diff",
            "pre-generated diff or snapshot",
        ):
            self.assertIn(phrase, self.body, phrase)
        self.assertRegex(self.body, r"(?i)not only `?base_commit\.\.HEAD`?")
        self.assertRegex(self.body, r"(?i)review-process/generated process artifacts.*unrelated dirty files")
        self.assertRegex(self.artifacts, r"(?i)base_commit.*current worktree")
        self.assertRegex(self.artifacts, r"(?i)feature-owned untracked")
        self.assertRegex(self.handoff, r"(?i)base_commit.*current worktree")
        self.assertRegex(self.handoff, r"(?i)unrelated dirty (?:files|changes)")

    def test_findings_AC4_AC5_AC12_AC13_AC14(self) -> None:
        """[AC-4] [AC-5] [AC-12] [AC-13] [AC-14] Findings are actionable, stable, and bounded."""
        for phrase in (
            "one distinct violated invariant or root cause",
            "evidence-backed",
            "Impact",
            "smallest sensible bounded correction",
            "BLOCKING",
            "FOLLOW-UP",
            "stable `F-NNN` ID",
            "append new resolution details",
            "Resolution: open | fixed | accepted | deferred",
            "FOLLOW-UP",
            "default to `accepted`",
            "`deferred` requires an explicit human decision",
            "targeted re-review",
            "short regression scan",
            "same blocker remains after two fix attempts",
            "human/debug diagnostic path",
            "narrow relevant check",
            "newly introduced `TODO`, `FIXME`, `XXX`, placeholders, hacks",
            "unchanged pre-existing debt",
        ):
            self.assertIn(phrase, self.body, phrase)
        for field in (
            "Evidence",
            "Impact",
            "Smallest sensible correction",
            "Resolution",
            "Resolution details",
        ):
            self.assertIn(field, self.artifacts, field)
        for resolution in ("open", "fixed", "accepted", "deferred"):
            self.assertIn(resolution, self.artifacts, resolution)
        self.assertRegex(self.body, r"(?i)targeted re-review.*first resolve each prior")
        self.assertRegex(self.body, r"(?i)two fix attempts|attempted twice")
        self.assertRegex(self.body, r"(?i)material(?:ly)? expands behavior, scope|material scope")
        self.assertRegex(self.body, r"(?i)blocking.*incomplete|safety gap.*follow-up")
        self.assertNotRegex(self.body, r"(?i)inherits? Build Recommendation|automatic(?:ally)? select.*Build")

    def test_security_AC3_AC15(self) -> None:
        """[AC-3] [AC-15] Review uses one fresh read-only context and treats repository/output data as untrusted."""
        for phrase in (
            "one fresh, generic, read-only",
            "exactly **one fresh",
            "If fresh dispatch is unavailable",
            "advisory (not fully isolated)",
            "not a named reviewer registry or a triada",
            "untrusted evidence",
            "embedded instructions",
            "Redact secrets",
            "credentials",
            "access tokens",
            "private keys",
            "Never copy them into",
            "must not edit",
            "cannot run implementation",
            "deploy",
            "push",
            "create a PR",
            "merge",
            "rewrite history",
        ):
            self.assertIn(phrase, self.body, phrase)
        self.assertRegex(self.body, r"(?i)active configured harness model")
        self.assertRegex(self.body, r"(?i)Reject malformed output")
        self.assertRegex(
            self.body,
            r"(?i)(?:does not inherit|do\s+\*\*not\*\*\s+read,\s*inherit).*Build Recommendation",
        )
        ui = CODEX_UI.read_text(encoding="utf-8")
        self.assertEqual(_yaml_value(ui, "allow_implicit_invocation"), "false")
        self.assertIn("$review", ui)
        self.assertTrue(ADR.exists(), ADR)

    def test_product_docs_review_AC1_AC2_AC3_AC5_AC6_AC7_AC8_AC10_AC11_AC12_AC13_AC14_AC15(self) -> None:
        """[AC-1] [AC-2] [AC-3] [AC-5] [AC-6] [AC-7] [AC-8] [AC-10] [AC-11] [AC-12] [AC-13] [AC-14] [AC-15] Product docs expose Review without a duplicate schema."""
        documents = {
            path.relative_to(ROOT).as_posix(): re.sub(
                r"\s+", " ", path.read_text(encoding="utf-8")
            )
            for path in DOCS
        }
        combined = " ".join(documents.values())
        self.assertIn("discuss -> build -> review -> ship", combined)
        self.assertRegex(combined, r"(?i)review.*implemented")
        for phrase in (
            "one fresh",
            "BLOCKING",
            "FOLLOW-UP",
            "stable",
            "accepted follow",
            "base_commit",
            "current worktree",
            "untracked",
            "TODO",
            "narrow",
            "active configured model",
            "advisory (not fully isolated)",
            "untrusted",
            "redact",
            "AbsolutPowers",
            "never deploy",
            "push",
            "create a PR",
        ):
            self.assertIn(phrase.lower(), combined.lower(), phrase)
        for relative_path, document in documents.items():
            self.assertIn("references/artifact-contracts.md", document, relative_path)
            self.assertIn("references/harness-command-contract.md", document, relative_path)
        self.assertIn("docs/adr/2026-08-28-independent-review-and-bounded-fix-loop.md", combined)
        self.assertNotRegex(combined, r"(?m)^#+ F-00[1-9]")
        self.assertRegex(combined, r"(?i)automatic triada.*(?:not|never)|(?:not|never).*automatic triada")
        self.assertRegex(combined, r"(?i)ship.*(?:after|when).*(?:review|blocker)")


if __name__ == "__main__":
    unittest.main()
