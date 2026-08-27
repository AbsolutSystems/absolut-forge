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

    def test_no_discoverable_stubs_AC7(self) -> None:
        """[AC-7] Foundation reservations expose no runnable skills or agents."""
        self.assertEqual(list((ROOT / "skills").rglob("SKILL.md")), [])
        self.assertEqual(
            [path.name for path in (ROOT / "skills").iterdir()],
            ["README.md"],
        )
        self.assertEqual(
            [path.name for path in (ROOT / "agents").iterdir()],
            ["README.md"],
        )
        for descriptor_path in (CLAUDE_MANIFEST, CODEX_MANIFEST):
            descriptor = _read_json(descriptor_path)
            self.assertNotIn("agents", descriptor)
            self.assertNotIn("commands", descriptor)

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
