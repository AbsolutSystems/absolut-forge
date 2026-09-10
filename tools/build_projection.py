"""Read-only owner and final-verification projections from durable state."""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path

try:
    from artifact_state import ContextError, fields, git, repo_path, section_blocks, sections
except ImportError:  # pragma: no cover
    from tools.artifact_state import ContextError, fields, git, repo_path, section_blocks, sections


def _status(brief: str) -> str:
    value = sections(brief, 2).get("Status", "").strip()
    if value not in {"Building", "In Review"}:
        raise ContextError("owner projection requires Brief status Building or In Review")
    return value


def _evidence(brief: str) -> tuple[dict[str, str], dict[str, str]]:
    blocks = section_blocks(sections(brief, 2).get("Build Evidence", ""), 3)
    starts = [fields(body) for title, body in blocks if title.startswith("Build start")]
    finals = [fields(body) for title, body in blocks if title.startswith("Build evidence")]
    if not starts:
        raise ContextError("missing Build start evidence")
    return starts[-1], finals[-1] if finals else {}


def _review_blockers(review: str | None) -> list[str]:
    if not review:
        return []
    blockers = []
    for title, body in section_blocks(sections(review, 2).get("Findings", ""), 3):
        if "— BLOCKING" in title and fields(body).get("Resolution", "open").lower() == "open":
            blockers.append(title.split(" —", 1)[0])
    return blockers


def _base(start: dict[str, str], final: dict[str, str]) -> str:
    value = final.get("Base revision / review diff", "")
    return value.split("..", 1)[0].strip(" `") if ".." in value else start.get("Base revision", "").strip(" `")


def _patterns(surface: str) -> list[str]:
    quoted = re.findall(r"`([^`]+)`", surface)
    values = quoted or re.split(r"[;\n,]", surface)
    return [value.strip().rstrip("/") for value in values if value.strip()]


def _owned(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) or path == pattern or path.startswith(pattern + "/") for pattern in patterns)


def _plan_state(execution: str) -> dict:
    top = sections(execution, 2)
    context = fields(top.get("Context", ""))
    frontier_body = top.get("Active frontier", "")
    frontier = fields(frontier_body.split("###", 1)[0])
    tasks = []
    for title, body in section_blocks(top.get("Task graph", ""), 3):
        match = re.match(r"(T-\d+)\s+—\s+(.+)", title)
        if match:
            tasks.append({"id": match.group(1), "title": match.group(2), **fields(body)})
    if not tasks:
        raise ContextError("planned execution artifact has no tasks")
    return {
        "status": top.get("Status", "").strip(),
        "revision": context.get("Plan revision"),
        "frontier": frontier,
        "tasks": tasks,
        "coverage": top.get("Coverage", "").strip(),
        "pending_final_obligations": sections(frontier_body, 3).get("Pending final-verification obligations", "").strip(),
    }


def _validate_plan(plan: dict, final: bool) -> None:
    by_id = {task["id"]: task for task in plan["tasks"]}
    if len(by_id) != len(plan["tasks"]):
        raise ContextError("duplicate task identifier")
    for task in plan["tasks"]:
        for key in ("Status", "Capability", "Depends on", "Change surface", "Test obligations", "Verification", "Completion evidence"):
            if not task.get(key, "").strip():
                raise ContextError(f"{task['id']} missing required field: {key}")
        if final and task["Status"] != "complete":
            raise ContextError(f"incomplete task at final verification: {task['id']}")
    ready = [x.strip() for x in plan["frontier"].get("Ready tasks", "").split(",") if x.strip() and x.strip() != "none"]
    for index, left in enumerate(ready):
        if left not in by_id:
            raise ContextError("frontier names unknown task: " + left)
        for right in ready[index + 1 :]:
            if right not in by_id:
                raise ContextError("frontier names unknown task: " + right)
            if set(_patterns(by_id[left]["Change surface"])) & set(_patterns(by_id[right]["Change surface"])):
                raise ContextError(f"overlapping ready-task write surfaces: {left}, {right}")
    if final:
        accepted = set(re.findall(r"^### (EO-\d+)", plan.get("accepted_outcomes", ""), re.M))
        covered = set(re.findall(r"^\s*- (EO-\d+):", plan["coverage"], re.M))
        if accepted - covered:
            raise ContextError("incomplete accepted outcome coverage: " + ", ".join(sorted(accepted - covered)))


def _evidence_commit(repo: Path, brief_rel: str, marker: str) -> str | None:
    current_count = git(repo, "show", f"HEAD:{brief_rel}").count(marker)
    if not current_count:
        return None
    for commit in git(repo, "log", "--reverse", "--format=%H", "--", brief_rel).splitlines():
        if git(repo, "show", f"{commit}:{brief_rel}").count(marker) >= current_count:
            return commit
    return None


def owner_projection(repo: Path, brief_path: Path, execution_path: Path, review_path: Path | None = None) -> dict:
    brief, execution = brief_path.read_text(), execution_path.read_text()
    start, final_evidence = _evidence(brief)
    strategy = start.get("Build strategy", "")
    if strategy not in {"planned", "autonomous"}:
        raise ContextError("unsupported Build strategy")
    head, base = git(repo, "rev-parse", "HEAD"), _base(start, final_evidence)
    if not base:
        raise ContextError("missing base revision")
    git(repo, "merge-base", "--is-ancestor", base, head)
    result = {
        "brief": repo_path(repo, brief_path), "brief_status": _status(brief),
        "strategy": strategy, "methodology": start.get("Planned methodology", "not applicable"),
        "base": base, "head": head, "execution_artifact": repo_path(repo, execution_path),
        "unresolved_review_blockers": _review_blockers(review_path.read_text() if review_path and review_path.exists() else None),
        "evidence_freshness": "present-unverified" if final_evidence else "not-finalized", "checks": "PASS",
        "semantic_exceptions": ["owner must resolve material intent, risk and test-quality judgments"],
    }
    if strategy == "planned":
        plan = _plan_state(execution)
        _validate_plan(plan, final=False)
        if result["brief_status"] == "In Review" and plan["status"] != "Complete":
            raise ContextError("illegal lifecycle state: In Review Brief requires Complete plan")
        current = plan["frontier"].get("Next task", "none")
        result["frontier"] = plan["frontier"]
        result["current_task"] = next((task for task in plan["tasks"] if task["id"] == current), None)
    else:
        outcomes = sections(brief, 2).get("Expected outcomes", "")
        completed = set(re.findall(r"^### Outcome checkpoint — (EO-\d+)", execution, re.M))
        accepted = re.findall(r"^### (EO-\d+)\s+—", outcomes, re.M)
        result["current_outcome"] = next((item for item in accepted if item not in completed), None)
    return result


def final_projection(repo: Path, brief_path: Path, execution_path: Path, review_path: Path | None = None) -> dict:
    if git(repo, "status", "--porcelain"):
        raise ContextError("final projection requires a clean checkpoint")
    result = owner_projection(repo, brief_path, execution_path, review_path)
    if result["unresolved_review_blockers"]:
        raise ContextError("unresolved blocking Review findings: " + ", ".join(result["unresolved_review_blockers"]))
    brief, top = brief_path.read_text(), sections(brief_path.read_text(), 2)
    plan = _plan_state(execution_path.read_text()) if result["strategy"] == "planned" else None
    if plan:
        plan["accepted_outcomes"] = top.get("Expected outcomes", "")
        _validate_plan(plan, final=True)
        if plan["status"] != "Complete":
            raise ContextError("planned final projection requires Complete plan")
        if plan["pending_final_obligations"] and "None" not in plan["pending_final_obligations"]:
            raise ContextError("pending final-verification obligations remain")
    changed = [line for line in git(repo, "diff", "--name-only", f"{result['base']}..{result['head']}").splitlines() if line]
    allowed = {result["brief"], result["execution_artifact"]}
    if review_path:
        allowed.add(repo_path(repo, review_path))
    patterns = [pattern for task in (plan or {}).get("tasks", []) for pattern in _patterns(task["Change surface"])]
    unowned = [path for path in changed if path not in allowed and not _owned(path, patterns)]
    if unowned:
        raise ContextError("changed paths lack task ownership: " + ", ".join(unowned))
    _, evidence = _evidence(brief)
    tests = evidence.get("Tests added/updated", "")
    if not tests:
        raise ContextError("missing validated test inventory")
    whole_path = evidence.get("Whole-feature path exercised", "")
    evidence_commit = _evidence_commit(repo, result["brief"], "### Build evidence —") if whole_path else None
    if not evidence_commit:
        raise ContextError("cannot establish final evidence commit")
    implementation_paths = [item for item in changed if item not in allowed and _owned(item, patterns)]
    for path in implementation_paths:
        latest = git(repo, "log", "-1", "--format=%H", "--", path)
        if latest:
            try:
                git(repo, "merge-base", "--is-ancestor", latest, evidence_commit)
            except ContextError as error:
                raise ContextError("stale final evidence after source/test change: " + path) from error
    result.update({
        "accepted_outcomes": top.get("Expected outcomes", ""), "accepted_constraints": top.get("Constraints and invariants", ""),
        "accepted_amendments": top.get("Amendments", ""), "coverage": plan["coverage"] if plan else "autonomous outcome checkpoints",
        "changed_paths": changed, "validated_test_inventory": tests,
        "pending_final_obligations": plan["pending_final_obligations"] if plan else "none",
        "diff_range": f"{result['base']}..{result['head']}", "evidence_freshness": "PASS",
        "semantic_exceptions": ["inspect the complete diff range; JSON intentionally omits diff content", "judge semantic test quality and boundary classification", "exercise the primary accepted path"],
    })
    return result
