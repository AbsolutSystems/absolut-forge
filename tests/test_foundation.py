"""Deterministic conformance checks for the AbsolutForge foundation."""

from __future__ import annotations

import json
import os
import re
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CODEX_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"

EXPECTED_NAME = "absolutforge"
EXPECTED_VERSION = "0.1.0"
EXPECTED_AUTHOR = "Absolut Systems"

OPTIONAL_RELEASE_METADATA = {
    "homepage",
    "repository",
    "bugs",
    "license",
    "legal",
    "legalUrl",
    "minimumVersion",
    "release",
}
FORBIDDEN_CAPABILITY_KEYS = {
    "hooks",
    "mcp",
    "mcpServers",
    "apps",
    "agents",
    "commands",
}
VALIDATION_COMMANDS = (
    "python3 -m unittest discover -s tests -t . -p 'test_*.py'",
    "claude plugin validate --strict .",
    "python3 /Users/kamil/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .",
)


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as descriptor:
        value = json.load(descriptor)
    if not isinstance(value, dict):
        raise TypeError(f"Expected an object in {path}")
    return value


def _all_json_descriptors() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.json")
        if ".git" not in path.parts
    )


def _all_repository_paths() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if ".git" not in path.parts
    ]


def _documented_code_blocks(*paths: Path) -> str:
    blocks: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        blocks.extend(re.findall(r"```(?:text|bash|sh)?\n(.*?)```", text, re.DOTALL))
    return "\n".join(blocks)


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


class FoundationContractTests(unittest.TestCase):
    def test_manifest_identity_AC1(self) -> None:
        """[AC-1] Both harness manifests carry one pilot identity."""
        claude = _read_json(CLAUDE_MANIFEST)
        codex = _read_json(CODEX_MANIFEST)
        for manifest in (claude, codex):
            self.assertEqual(manifest["name"], EXPECTED_NAME)
            self.assertEqual(manifest["version"], EXPECTED_VERSION)
            self.assertEqual(manifest["author"], {"name": EXPECTED_AUTHOR})
            self.assertEqual(manifest["description"], "Intent-driven development workflow for strong coding models.")

    def test_shared_skill_tree_AC2(self) -> None:
        """[AC-2] Claude and Codex resolve one repository-level skills tree."""
        claude = _read_json(CLAUDE_MANIFEST)
        codex = _read_json(CODEX_MANIFEST)
        self.assertNotIn("skills", claude)
        self.assertEqual(codex["skills"], "./skills/")
        skills = ROOT / "skills"
        self.assertTrue(skills.is_dir())
        self.assertFalse((ROOT / "claude" / "skills").exists())
        self.assertFalse((ROOT / "codex" / "skills").exists())
        self.assertFalse((ROOT / ".claude" / "skills").exists())
        self.assertFalse((ROOT / ".codex" / "skills").exists())

    def test_context_entrypoints_AC3(self) -> None:
        """[AC-3] Entry-point documents link the accepted context and contracts."""
        required_paths = (
            "docs/product-vision.md",
            "absolutforge/features/absolutforge-mvp/planning-main.md",
            "absolutforge/features/absolutforge-mvp/planning-phase-1-foundation.md",
            "references/artifact-contracts.md",
            "references/project-memory.md",
            "references/harness-command-contract.md",
            "docs/adr/2026-08-27-host-agnostic-skill-tree.md",
            "docs/adr/2026-08-27-explicit-activation-without-hooks.md",
            "absolutforge/project-memory.md",
        )
        for relative_path in required_paths:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        vision = (ROOT / "docs/product-vision.md").read_text(encoding="utf-8")
        phase_plan = (ROOT / "absolutforge/features/absolutforge-mvp/planning-phase-1-foundation.md").read_text(
            encoding="utf-8"
        )
        entrypoint_paths = (
            "docs/product-vision.md",
            "absolutforge/features/absolutforge-mvp/planning-main.md",
            "references/artifact-contracts.md",
            "references/project-memory.md",
            "references/harness-command-contract.md",
        )
        for relative_path in entrypoint_paths:
            self.assertIn(relative_path, readme, relative_path)
        self.assertIn("docs/product-vision.md", claude)
        self.assertIn("absolutforge/features/absolutforge-mvp/planning-main.md", claude)
        for link in (
            "../references/artifact-contracts.md",
            "../references/project-memory.md",
            "../references/harness-command-contract.md",
            "adr/2026-08-27-host-agnostic-skill-tree.md",
            "adr/2026-08-27-explicit-activation-without-hooks.md",
        ):
            self.assertIn(link, vision, link)
        for link in (
            "../../../references/artifact-contracts.md",
            "../../../references/project-memory.md",
            "../../../references/harness-command-contract.md",
            "../../../docs/adr/2026-08-27-host-agnostic-skill-tree.md",
            "../../../docs/adr/2026-08-27-explicit-activation-without-hooks.md",
        ):
            self.assertIn(link, phase_plan, link)
        agents = ROOT / "AGENTS.md"
        self.assertTrue(agents.is_symlink())
        self.assertEqual(os.readlink(agents), "CLAUDE.md")
        self.assertEqual(agents.resolve(), (ROOT / "CLAUDE.md").resolve())

    def test_non_mutating_validation_AC4(self) -> None:
        """[AC-4] Documented foundation validation inspects without activation."""
        for descriptor in _all_json_descriptors():
            _read_json(descriptor)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        phase_plan = (ROOT / "absolutforge/features/absolutforge-mvp/planning-phase-1-foundation.md").read_text(
            encoding="utf-8"
        )
        for command in VALIDATION_COMMANDS:
            self.assertIn(command, readme)
        self.assertIn("non-mutating", readme.lower())
        self.assertIn("claude plugin validate", phase_plan)
        self.assertIn("plugin-creator/scripts/validate_plugin.py", phase_plan)

        documented_commands = _documented_code_blocks(ROOT / "README.md", ROOT / "CLAUDE.md")
        mutating_words = re.compile(
            r"\b(?:install|uninstall|remove|enable|disable|activate|deactivate|add|delete)\b",
            re.IGNORECASE,
        )
        self.assertIsNone(mutating_words.search(documented_commands), documented_commands)

    def test_private_metadata_optional_AC5(self) -> None:
        """[AC-5] Deferred public and legal metadata is not required locally."""
        for descriptor_path in (CLAUDE_MANIFEST, CODEX_MANIFEST):
            descriptor = _read_json(descriptor_path)
            self.assertTrue({"name", "version", "description", "author"}.issubset(descriptor))
            self.assertTrue(OPTIONAL_RELEASE_METADATA.isdisjoint(descriptor))

    def test_marketplace_root_AC6(self) -> None:
        """[AC-6] Local marketplace entries resolve to the repository plugin root."""
        claude_marketplace = _read_json(CLAUDE_MARKETPLACE)
        codex_marketplace = _read_json(CODEX_MARKETPLACE)

        self.assertEqual(claude_marketplace["name"], EXPECTED_NAME)
        self.assertEqual(claude_marketplace["owner"], {"name": EXPECTED_AUTHOR})
        claude_plugin = claude_marketplace["plugins"][0]
        self.assertEqual(claude_plugin["name"], EXPECTED_NAME)
        self.assertEqual(claude_plugin["source"], ".")

        self.assertEqual(codex_marketplace["name"], EXPECTED_NAME)
        codex_plugin = codex_marketplace["plugins"][0]
        self.assertEqual(codex_plugin["name"], EXPECTED_NAME)
        self.assertEqual(codex_plugin["source"], {"source": "local", "path": "."})
        self.assertEqual(
            codex_plugin["policy"],
            {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        )

        self.assertEqual((ROOT / claude_plugin["source"]).resolve(), ROOT)
        self.assertEqual((ROOT / codex_plugin["source"]["path"]).resolve(), ROOT)

    def test_active_skills_are_explicit_and_safe_AC12_AC13_AC15(self) -> None:
        """[AC-12] [AC-13] [AC-15] Active skills are explicit-only and safe."""
        skills = ROOT / "skills"
        discovered = sorted(
            path.relative_to(ROOT).as_posix() for path in skills.rglob("SKILL.md")
        )
        self.assertEqual(
            discovered,
            ["skills/consult/SKILL.md", "skills/discuss/SKILL.md"],
        )
        self.assertEqual(
            sorted(path.name for path in skills.iterdir()),
            ["README.md", "consult", "discuss"],
        )
        self.assertEqual(
            [path.name for path in (ROOT / "agents").iterdir()],
            ["README.md"],
        )
        unsupported_integration_paths = {
            path
            for path in _all_repository_paths()
            if path.name.lower() in {"hooks", "mcp", "mcpservers", "apps", "pi", "grok"}
        }
        self.assertEqual(unsupported_integration_paths, set())

        for skill_name in ("discuss", "consult"):
            skill_dir = skills / skill_name
            skill = skill_dir / "SKILL.md"
            frontmatter, body = _frontmatter_and_body(skill)
            self.assertEqual(_frontmatter_value(frontmatter, "name"), skill_name)
            self.assertEqual(
                _frontmatter_value(frontmatter, "disable-model-invocation"), "true"
            )
            self.assertIn("references/artifact-contracts.md", body)
            self.assertIn("references/harness-command-contract.md", body)
            self.assertRegex(body, r"(?i)explicit(?:-only| invocation)")
            self.assertRegex(body, r"(?i)untrusted")
            self.assertRegex(body, r"(?i)secret|credential")

            codex_ui = skill_dir / "agents" / "openai.yaml"
            ui = codex_ui.read_text(encoding="utf-8")
            self.assertEqual(_yaml_value(ui, "allow_implicit_invocation"), "false")
            self.assertIn(f"${skill_name}", ui)

        vision = (ROOT / "docs/product-vision.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        for document in (vision, readme, claude):
            self.assertRegex(document, r"(?i)explicit-only|explicit-only")
            self.assertRegex(document, r"(?i)untrusted")
            self.assertRegex(document, r"(?i)secret|credential")
        self.assertRegex(vision, r"(?i)consult.*optional|optional.*consult")

    def test_product_docs_describe_discuss_AC1_AC4(self) -> None:
        """[AC-1] [AC-4] Product docs describe the adaptive flow and one acceptance gate."""
        documents = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in ("README.md", "docs/product-vision.md")
        )
        self.assertIn("readiness frontier", documents.lower())
        self.assertRegex(documents, r"(?i)two to four|2 to 4|2-4")
        self.assertRegex(documents, r"(?i)one acceptance gate")
        self.assertRegex(documents, r"(?i)Draft.*Ready|Ready.*Draft")
        self.assertRegex(documents, r"(?i)complete (?:Feature )?Brief")

    def test_product_docs_describe_optional_consult_AC5_AC6(self) -> None:
        """[AC-5] [AC-6] Product docs describe bounded optional consultation and approval."""
        documents = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in ("README.md", "docs/product-vision.md", "CLAUDE.md")
        )
        lowered = documents.lower()
        self.assertIn("consult", lowered)
        self.assertRegex(lowered, r"optional.*(?:second|opinion)|(?:second|opinion).*optional")
        self.assertIn("bounded batch", lowered)
        self.assertRegex(lowered, r"explicit(?:ly)? accept")
        self.assertRegex(lowered, r"no consultation artifact|no durable consultation")
        self.assertIn("optional-cross-model-brief-consultation.md", documents)

    def test_product_docs_keep_explicit_core_AC15(self) -> None:
        """[AC-15] Product docs preserve the direct explicit core workflow."""
        documents = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in ("README.md", "docs/product-vision.md", "CLAUDE.md")
        )
        self.assertIn("discuss -> build -> review -> ship", documents)
        self.assertRegex(documents, r"(?i)consultation.*never.*(?:mandatory|required|gate)")
        self.assertRegex(documents, r"(?i)consult.*explicit-only|explicit-only.*consult")

    def test_manifest_drift_rejected_AC8(self) -> None:
        """[AC-8] Identity drift between the two descriptors fails conformance."""
        claude = _read_json(CLAUDE_MANIFEST)
        codex = _read_json(CODEX_MANIFEST)
        identity = lambda descriptor: (
            descriptor["name"],
            descriptor["version"],
            descriptor["author"],
        )
        self.assertEqual(identity(claude), identity(codex))
        self.assertEqual(identity(claude), (EXPECTED_NAME, EXPECTED_VERSION, {"name": EXPECTED_AUTHOR}))

    def test_no_implicit_capabilities_AC9_AC10_AC11(self) -> None:
        """[AC-9] [AC-10] [AC-11] No hooks, global behavior, or extra capabilities exist."""
        for descriptor_path in (CLAUDE_MANIFEST, CODEX_MANIFEST):
            descriptor = _read_json(descriptor_path)
            self.assertTrue(FORBIDDEN_CAPABILITY_KEYS.isdisjoint(descriptor))

        forbidden_paths = {
            path
            for path in _all_repository_paths()
            if path.name.lower() in {"hooks", "mcp", "mcpservers", "apps"}
        }
        self.assertEqual(forbidden_paths, set())
        self.assertEqual(list(ROOT.rglob("session-start")), [])
        self.assertEqual(list(ROOT.rglob("SessionStart")), [])

        vision = (ROOT / "docs/product-vision.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("explicit-only", vision)
        self.assertIn("There is no SessionStart hook", vision)
        self.assertIn("globally injected workflow", readme)

    def test_concurrent_workflow_warning_AC12(self) -> None:
        """[AC-12] Documentation warns against concurrent AbsolutPowers use."""
        documents = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in ("README.md", "CLAUDE.md", "docs/product-vision.md")
        )
        self.assertRegex(documents, r"(?i)disable.{0,120}AbsolutPowers")
        self.assertRegex(documents, r"(?i)must not be enabled together|not be active together")
        self.assertRegex(documents, r"(?i)overlapping workflow")


if __name__ == "__main__":
    unittest.main()
