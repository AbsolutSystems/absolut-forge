"""Deterministic Markdown and Git primitives for runtime projections."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

FIELD_RE = re.compile(r"^- ([A-Za-z][A-Za-z /-]+):\s*(.*)$")


class ContextError(ValueError):
    pass


def sections(text: str, level: int) -> dict[str, str]:
    out: dict[str, str] = {}
    for name, body in section_blocks(text, level):
        if name in out:
            raise ContextError("ambiguous section: " + name)
        out[name] = body
    return out


def section_blocks(text: str, level: int) -> list[tuple[str, str]]:
    """Return ordered sections while ignoring headings inside fenced blocks."""
    out: list[tuple[str, str]] = []
    name, lines, fence = None, [], None

    def save() -> None:
        if name is not None:
            out.append((name, "".join(lines).strip()))

    for line in text.splitlines(keepends=True):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            if name is not None:
                lines.append(line)
            continue
        heading = re.match(r"^" + "#" * level + r" (.+?)\s*$", line) if fence is None else None
        if heading:
            save()
            name, lines = heading.group(1), []
        elif name is not None:
            lines.append(line)
    if fence is not None:
        raise ContextError("unclosed fenced block")
    save()
    return out


def fields(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    key, values = None, []

    def save() -> None:
        if key:
            if key in out:
                raise ContextError("ambiguous field: " + key)
            out[key] = "\n".join(values).strip()

    for line in text.splitlines():
        found = FIELD_RE.match(line)
        if found:
            save()
            key, values = found.group(1).strip(), [found.group(2).strip()]
        elif key is not None:
            values.append(line.strip())
    save()
    return out


def require(data: dict[str, str], key: str) -> str:
    value = data.get(key, "").strip()
    if not value:
        raise ContextError("missing required field: " + key)
    return value


def items(body: str) -> list[str]:
    result: list[str] = []
    for line in body.splitlines():
        if line.startswith("- "):
            result.append(line[2:].strip())
        elif line.strip():
            if not result:
                raise ContextError("frontier content must use bullet items")
            result[-1] += "\n" + line.strip()
    if not result:
        raise ContextError("missing frontier facts")
    return result


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=False
    )
    if result.returncode:
        raise ContextError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def repo_path(repo: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError as error:
        raise ContextError(f"artifact is outside repository: {path}") from error
