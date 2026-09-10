#!/usr/bin/env python3
"""Compile non-authoritative Codex planned-runtime projections."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path

try:
    from artifact_state import ContextError, section_blocks
except ImportError:  # pragma: no cover
    from tools.artifact_state import ContextError, section_blocks

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    "planned-building": "runtime/generated/codex-planned-building.md",
    "planned-final": "runtime/generated/codex-planned-final.md",
}
SOURCES = {
    "build-entrypoint": "skills/build/SKILL.md",
    "common-runtime": "runtime/common.md",
    "planned-runtime": "runtime/planned.md",
    "codex-host": "references/codex-tools.md",
}
RULES = {
    "planned-building": {
        "build-entrypoint": None,
        "common-runtime": None,
        "planned-runtime": ["Start and resume", "Compile", "Execute and validate"],
        "codex-host": ["Build owner", "Planned Build"],
    },
    "planned-final": {
        "build-entrypoint": None,
        "common-runtime": None,
        "planned-runtime": ["Start and resume", "Escalate and finish"],
        "codex-host": ["Build owner", "Planned Build"],
    },
}


def _select(text: str, headings: list[str] | None) -> str:
    if headings is None:
        return text.strip()
    available = dict(section_blocks(text, 2))
    missing = [item for item in headings if item not in available]
    if missing:
        raise ContextError("missing compiler source section: " + ", ".join(missing))
    return "\n\n".join(f"## {item}\n\n{available[item]}" for item in headings)


def _rewrite_links(text: str, source: Path, output: Path) -> str:
    def replace(match: re.Match) -> str:
        label, target = match.groups()
        if target.startswith(("#", "http://", "https://")):
            return match.group(0)
        path, marker, anchor = target.partition("#")
        resolved = (source.parent / path).resolve()
        relative = os.path.relpath(resolved, output.parent.resolve())
        return f"[{label}]({Path(relative).as_posix()}{marker}{anchor})"

    return re.sub(r"\[([^]]+)\]\(([^)]+)\)", replace, text)


def compile_state(root: Path, state: str) -> str:
    if state not in RULES:
        raise ContextError("unsupported runtime state: " + state)
    chunks, provenance = [], []
    output = root / OUTPUTS[state]
    for rule, path in SOURCES.items():
        source = (root / path).read_text()
        digest = hashlib.sha256(source.encode()).hexdigest()
        provenance.append(f"- `{path}` sha256 `{digest}`; rule `{rule}`")
        selected = _rewrite_links(_select(source, RULES[state][rule]), root / path, output)
        chunks.append(f"<!-- source: {path}; rule: {rule} -->\n\n{selected}")
    return (
        "# Generated Codex runtime: " + state + "\n\n"
        "> Non-authoritative generated projection. Do not edit. Canonical source files below win.\n\n"
        "## Provenance and rule coverage\n\n" + "\n".join(provenance) + "\n\n"
        + "\n\n---\n\n".join(chunks) + "\n"
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    stale = []
    for state, relative in OUTPUTS.items():
        expected, target = compile_state(args.root, state), args.root / relative
        if args.write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(expected)
        elif not target.exists() or target.read_text() != expected:
            stale.append(relative)
    if stale:
        parser.error("stale generated runtime: " + ", ".join(stale))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
