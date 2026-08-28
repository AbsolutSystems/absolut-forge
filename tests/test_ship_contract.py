"""Deterministic conformance checks for the explicit-only Ship closeout.

The suite inspects the canonical Markdown contracts, skill instructions,
metadata, and pure fixtures. It never invokes a model, mutates a repository,
activates a plugin, creates a transaction, or contacts a remote service.
"""

from __future__ import annotations

import hashlib
import html
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHIP = ROOT / "skills" / "ship" / "SKILL.md"
SHIP_UI = ROOT / "skills" / "ship" / "agents" / "openai.yaml"
REVIEW = ROOT / "skills" / "review" / "SKILL.md"
ARTIFACTS = ROOT / "references" / "artifact-contracts.md"
HANDOFF = ROOT / "references" / "harness-command-contract.md"
ADR = ROOT / "docs" / "adr" / "2026-08-28-ship-post-review-closeout.md"
DOCS = tuple(ROOT / path for path in ("README.md", "CLAUDE.md", "docs/product-vision.md", "skills/README.md"))

COMMIT_SUBJECT_RE = r"^(feat|fix|refactor|docs|test|chore|perf)(\([a-z0-9][a-z0-9-]*\))?!?: [^\r\n]+$"


def _contract(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))


def _manifest_line(path: bytes, state: str, mode: str, content_hash: str) -> bytes:
    """Return one canonical raw-byte manifest line from a pure fixture."""
    return b"\x00".join((path.hex().encode("ascii"), state.encode(), mode.encode(), content_hash.encode())) + b"\n"


def _fingerprint(entries: tuple[bytes, ...]) -> str:
    """Hash a canonical raw-byte manifest fixture without touching Git."""
    return hashlib.sha256(b"".join(sorted(entries))).hexdigest()


FINGERPRINT_FIXTURES = {
    "canonical ordering": (
        _manifest_line(b"src/z.py", "present", "100644", "a" * 64),
        _manifest_line(b"src/a.py", "present", "100755", "b" * 64),
    ),
    "raw path bytes": (
        _manifest_line(b"caf\xc3\xa9.md", "present", "100644", "c" * 64),
        _manifest_line(b"cafe\xcc\x81.md", "present", "100644", "d" * 64),
    ),
    "present/deleted entries": (
        _manifest_line(b"new.txt", "present", "120000", "e" * 64),
        _manifest_line(b"old.txt", "deleted", "000000", "0" * 64),
    ),
    "git modes and content hashes": tuple(
        _manifest_line(path, "present", mode, hashlib.sha256(content).hexdigest())
        for path, mode, content in ((b"regular", "100644", b"x"), (b"exec", "100755", b"y"), (b"link", "120000", b"target"), (b"submodule", "160000", b"object-id"))
    ),
}

JOURNAL_FIXTURE = {
    "state": "applying",
    "preview_digest": "a" * 64,
    "fingerprint": "b" * 64,
    "approved_paths": ("absolutforge/archives/demo/feature-record.md",),
    "pre_transaction_index_tree": "c" * 40,
    "lock": {"transaction_id": "txn-1", "process": 1234, "host": "worker", "start_time": "2026-08-28T00:00:00Z"},
    "operations": ({"name": "archive", "state": "completed", "paths": ("absolutforge/archives/demo/feature-record.md",), "output_hashes": ("d" * 64,)},),
    "commit_intent": {"target_ref": "refs/heads/main", "expected_parent": "e" * 40, "frozen_tree_id": "f" * 40, "commit_message_digest": "0" * 64},
}


class ShipContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ship = _contract(SHIP)
        self.review = _contract(REVIEW)
        self.artifacts = _contract(ARTIFACTS)
        self.handoff = _contract(HANDOFF)
        self.adr = _contract(ADR)

    def test_ship_validation_AC1_AC2_AC3_AC7_AC9_AC10_AC11(self) -> None:
        """[AC-1] [AC-2] [AC-3] [AC-7] [AC-9] [AC-10] [AC-11] validate eligibility, preview binding, freshness, collisions, and dirty-scope refusal."""
        for phrase in (
            "Invoke it only with matching repository-relative paths",
            "matching repository-relative paths",
            "In Review",
            "Complete",
            "no open `BLOCKING` finding",
            "final Review pass",
            "immutable Brief baseline",
            "accepted amendments",
            "base_commit",
            "safe scope is separable",
            "archive collisions",
            "unrelated dirty work",
            "missing, malformed, or different manifest/fingerprint",
            "freshness failure",
            "Before rendering",
            "bound to the validated manifest and fingerprint",
            "one explicit closeout approval",
        ):
            self.assertIn(phrase, self.ship, phrase)
        self.assertRegex(self.ship, r"preserve the active artifacts and worktree")
        self.assertRegex(self.ship, r"pre-existing staged.*outside.*approved")

    def test_ship_feature_record_AC2_AC4_AC14(self) -> None:
        """[AC-2] [AC-4] [AC-14] Feature Record preserves intent, outcomes, evidence, and map consolidation."""
        required_sections = (
            "# Feature: {name}",
            "## Status",
            "## Original intent",
            "## What was built",
            "## Deviations from the Brief",
            "## Verification",
            "## Review outcome",
            "## Architectural decisions",
            "## Durable knowledge",
            "## Open follow-ups",
            "## Recommended review order",
        )
        for section in required_sections:
            self.assertIn(section, self.ship, section)
            self.assertIn(section, self.artifacts, section)
        for phrase in (
            "Preserve original accepted intent separately",
            "as-built result",
            "accepted amendments",
            "Build Evidence",
            "Review outcome",
            "linked ADRs",
            "Execution Map",
            "never archive the map itself",
            "deviations",
            "Open follow-ups",
        ):
            self.assertIn(phrase, self.ship, phrase)
        self.assertIn("accepted FOLLOW-UP", self.artifacts)

    def test_ship_executive_summary_AC5_AC6_AC15(self) -> None:
        """[AC-5] [AC-6] [AC-15] Executive Summary is self-contained, link-only, escaped, and redacted."""
        for phrase in (
            "self-contained",
            "inline CSS",
            "TL;DR",
            "problem and business value",
            "final scope",
            "primary behavior/data flow",
            "changed-component map",
            "key decisions and rationale",
            "rejected alternatives",
            "deviations",
            "tests and verification",
            "Review blockers found and fixed",
            "follow-ups and risks",
            "recommended file-review order",
            "documentation/ADR links",
            "no network resource",
            "secret",
            "Escape every untrusted text and attribute value",
            "prospective frozen commit tree",
            "../../../{repository-relative-path}",
        ):
            self.assertIn(phrase, self.ship, phrase)
        for forbidden in ("external URLs", "protocol-relative URLs", "absolute URLs", "file:", "javascript:", "data:"):
            self.assertIn(forbidden, self.ship, forbidden)
        self.assertRegex(self.ship + self.artifacts, r"source(?:-code)? excerpt")
        self.assertEqual(html.escape("<secret>&"), "&lt;secret&gt;&amp;")
        self.assertNotIn("<script src=", self.ship.lower())

    def test_ship_fingerprint_fixtures_AC3_AC7_AC9_AC10(self) -> None:
        """[AC-3] [AC-7] [AC-9] [AC-10] Pure fixtures prove canonical ordering, raw paths, modes, deletion, scope drift, and final freshness refusal."""
        self.assertEqual(
            sorted(FINGERPRINT_FIXTURES["canonical ordering"]),
            [FINGERPRINT_FIXTURES["canonical ordering"][1], FINGERPRINT_FIXTURES["canonical ordering"][0]],
        )
        self.assertTrue(FINGERPRINT_FIXTURES["raw path bytes"][0].startswith(b"caf\xc3\xa9".hex().encode()))
        deleted = FINGERPRINT_FIXTURES["present/deleted entries"][1]
        self.assertIn(b"deleted\x00000000\x00" + b"0" * 64, deleted)
        self.assertEqual(len(b"0" * 64), 64)
        self.assertEqual(len(FINGERPRINT_FIXTURES["git modes and content hashes"]), 4)
        baseline = _fingerprint(FINGERPRINT_FIXTURES["present/deleted entries"])
        drifted = _fingerprint(
            FINGERPRINT_FIXTURES["present/deleted entries"]
            + (_manifest_line(b"new.txt", "present", "100644", "f" * 64),)
        )
        self.assertEqual(baseline, baseline.lower())
        self.assertNotEqual(baseline, drifted)
        self.assertIn("union the base-revision feature scope", self.ship)
        self.assertIn("path set is the union", self.artifacts)
        for phrase in ("immediately after the single approval", "immediately before freezing"):
            self.assertIn(phrase, self.artifacts, phrase)
        self.assertNotEqual(baseline, drifted, "scope drift must refuse final freshness")

    def test_ship_transaction_recovery_AC7_AC8_AC10_AC11_AC12_AC13(self) -> None:
        """[AC-7] [AC-8] [AC-10] [AC-11] [AC-12] [AC-13] transaction fixtures cover approval, journal, lock, commit intent, and conflict-safe recovery."""
        journal_fields = (
            ".ship-txn/{txid}/journal.json",
            "state",
            "approved path set",
            "original bytes",
            "modes",
            "pre-transaction index tree",
            "prepared -> applying -> staged -> committing -> committed",
            "recovery-required",
            "resume",
            "rollback",
            "rolled-back",
            ".ship-txn/lock",
            "transaction ID",
            "process",
            "host",
            "start time",
            "commit_intent",
            "target ref",
            "expected parent",
            "frozen tree ID",
            "commit-message digest",
            "post-commit drift",
            "interrupted",
            "real index",
            "rollback",
            "external edit",
            "conflict",
            "idempotent",
        )
        for phrase in journal_fields:
            self.assertIn(phrase, self.ship, phrase)
            self.assertIn(phrase, self.artifacts, phrase)
        self.assertIn("paths and output hashes", self.ship)
        self.assertIn("expected path/output hash", self.artifacts)
        self.assertIn("stale lock metadata", self.ship)
        self.assertIn("stale metadata authorization", self.artifacts)
        self.assertIn("a third time immediately before freezing", self.ship)
        self.assertIn("once more while locked immediately before freezing", self.artifacts)
        self.assertIn("acquire and hold the OS advisory lock through commit", self.ship)
        self.assertIn("before post-approval revalidation", self.artifacts)
        self.assertIn("before revalidating the fingerprint", self.adr)
        self.assertEqual(
            tuple(operation["state"] for operation in JOURNAL_FIXTURE["operations"]),
            ("completed",),
        )
        self.assertEqual(
            JOURNAL_FIXTURE["operations"][0]["output_hashes"],
            ("d" * 64,),
        )
        self.assertEqual(
            JOURNAL_FIXTURE["commit_intent"]["expected_parent"],
            "e" * 40,
        )
        self.assertIn("preview_digest", self.ship)
        self.assertIn("preview digest", self.artifacts)
        self.assertRegex(self.ship, r"pending.*running.*completed")
        self.assertIn("pending | running | completed", self.artifacts)
        self.assertIn("individual promotion decisions", self.ship)
        self.assertIn("individual memory decisions", self.artifacts)
        for owner in (self.ship, self.artifacts, self.adr):
            self.assertIn(COMMIT_SUBJECT_RE, owner)
        accepted = ("feat: ship closeout", "fix(core): recover transaction", "docs!: revise contract")
        rejected = ("feature: missing type", "feat(scope_with_underscore): bad", "feat: newline\nforbidden")
        for subject in accepted:
            self.assertRegex(subject, COMMIT_SUBJECT_RE)
        for subject in rejected:
            self.assertNotRegex(subject, COMMIT_SUBJECT_RE)

    def test_ship_disallows_remote_effects_AC8_AC15(self) -> None:
        """[AC-8] [AC-15] Ship is explicit-only and local: no push, PR, merge, deploy, or history rewrite."""
        for phrase in (
            "explicit-only",
            "local-only",
            "never pushes",
            "create a PR",
            "merge",
            "deploy",
            "rewrite history",
            "Do not perform a remote action",
            "local commit",
        ):
            self.assertIn(phrase, self.ship, phrase)
        self.assertIn("No remote side effect is permitted", self.artifacts)
        self.assertRegex(self.artifacts, r"(?i)never pushes, creates a PR, merges, deploys, or rewrites history")

    def test_product_docs_ship_AC1_AC2_AC4_AC5_AC6_AC7_AC8_AC9_AC10_AC12_AC13_AC14_AC15(self) -> None:
        """[AC-1] [AC-2] [AC-4] [AC-5] [AC-6] [AC-7] [AC-8] [AC-9] [AC-10] [AC-12] [AC-13] [AC-14] [AC-15] docs describe implemented Ship without a duplicate schema."""
        documents = [_contract(path) for path in DOCS]
        combined = " ".join(documents)
        self.assertRegex(combined, r"(?i)ship.*implemented")
        self.assertIn("$absolutforge ship absolutforge/features/{slug}/feature-brief.md absolutforge/features/{slug}/review.md", combined)
        for phrase in (
            "Feature Record",
            "Executive Summary",
            "post-review",
            "one explicit closeout approval",
            "memory",
            "archive",
            "journal",
            "recovery",
            "local commit",
            "does not push",
            "create a PR",
            "merge",
            "deploy",
            "There is no SessionStart hook",
            "debug",
            "tech-debt",
            "references/artifact-contracts.md",
            "references/harness-command-contract.md",
        ):
            self.assertIn(phrase.lower(), combined.lower(), phrase)
        self.assertNotIn("ship remains the next closeout phase", combined.lower())


if __name__ == "__main__":
    unittest.main()
