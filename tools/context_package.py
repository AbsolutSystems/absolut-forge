#!/usr/bin/env python3
"""Read-only bounded context projections for planned-build artifacts."""

from __future__ import annotations
import argparse, json, re, subprocess
from dataclasses import dataclass
from pathlib import Path

BASELINE = "f47dfbc45563b5fce6b8de49cd005f40b7b655fb"
TASK_RE = re.compile(r"^### (T-\d+)\s+—\s+(.+)$", re.M)
FIELD_RE = re.compile(r"^- ([A-Za-z][A-Za-z -]+):\s*(.*)$")


class ContextError(ValueError):
    pass


def _sections(text, level):
    # Fenced examples are content, never section boundaries.
    out, name, lines, fence = {}, None, [], None

    def save():
        if name is not None:
            if name in out:
                raise ContextError("ambiguous section: " + name)
            out[name] = "".join(lines).strip()

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
        heading = (
            re.match(r"^" + "#" * level + r" (.+?)\s*$", line)
            if fence is None
            else None
        )
        if heading:
            save()
            name, lines = heading.group(1), []
        elif name is not None:
            lines.append(line)
    if fence is not None:
        raise ContextError("unclosed fenced block")
    save()
    return out


def _fields(text):
    out, key, values = {}, None, []

    def save():
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


def _require(data, key):
    value = data.get(key, "").strip()
    if not value:
        raise ContextError("missing required field: " + key)
    return value


def _ids(value, prefix):
    if value.strip().lower() == "none":
        return []
    parts = [x.strip() for x in value.split(",")]
    pattern = re.compile(prefix + r"-\d+")
    if (
        not parts
        or any(not pattern.fullmatch(x) for x in parts)
        or len(set(parts)) != len(parts)
    ):
        raise ContextError("invalid or ambiguous " + prefix + " identifiers: " + value)
    return parts


def _blocked(value):
    if value.strip().lower() == "none":
        return []
    out = []
    for item in value.split(","):
        match = re.fullmatch(r"\s*(T-\d+)(?:\s*->\s*[^,]+)?\s*", item)
        if not match:
            raise ContextError("invalid blocked task: " + item)
        out.append(match.group(1))
    if len(out) != len(set(out)):
        raise ContextError("ambiguous blocked tasks")
    return out


def _items(body):
    result = []
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


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    fields: dict


def parse_plan(text):
    top = _sections(text, 2)
    if "Context" not in top or "Task graph" not in top:
        raise ContextError("plan needs Context and Task graph")
    graph, tasks = top["Task graph"], {}
    matches = list(TASK_RE.finditer(graph))
    for i, match in enumerate(matches):
        ident, title = match.groups()
        if ident in tasks:
            raise ContextError("ambiguous task: " + ident)
        tasks[ident] = Task(
            ident,
            title,
            _fields(
                graph[
                    match.end() : matches[i + 1].start()
                    if i + 1 < len(matches)
                    else len(graph)
                ]
            ),
        )
    if not tasks:
        raise ContextError("plan has no tasks")
    body = top.get("Active frontier")
    if body is None:
        return _fields(top["Context"]), tasks, {}
    nested = _sections(body, 3)
    direct = _fields(body.split("###", 1)[0])
    for key in (
        "Relevant dependency facts",
        "Active invariants",
        "Pending final-verification obligations",
    ):
        if key not in nested:
            raise ContextError("missing frontier section: " + key)
    return _fields(top["Context"]), tasks, {**direct, **nested}


def _validate(context, tasks, frontier):
    for key in ("Plan revision", "Next task", "Ready tasks", "Blocked tasks"):
        _require(frontier, key)
    if _require(context, "Plan revision") != frontier["Plan revision"]:
        raise ContextError("stale frontier plan revision")
    if not re.fullmatch(r"[1-9]\d*", frontier["Plan revision"]):
        raise ContextError("invalid plan revision")
    next_task = _ids(frontier["Next task"], "T")
    if len(next_task) != 1:
        raise ContextError("Next task must name exactly one task")
    ready, blocked = (
        _ids(frontier["Ready tasks"], "T"),
        _blocked(frontier["Blocked tasks"]),
    )
    for invariant in _items(frontier["Active invariants"]):
        if "INV-" in invariant and not re.match(r"^INV-\d+(?::|\s|$)", invariant):
            raise ContextError("invalid active invariant: " + invariant)
    if next_task[0] not in ready or set(ready) & set(blocked):
        raise ContextError("inconsistent frontier task sets")
    for ident in ready + blocked:
        if ident not in tasks:
            raise ContextError("frontier names unknown task: " + ident)
    for ident in ready:
        if tasks[ident].fields.get("Status") not in ("pending", "in-progress"):
            raise ContextError("ready task is not pending: " + ident)
        for dep in _ids(_require(tasks[ident].fields, "Depends on"), "T"):
            if dep not in tasks or tasks[dep].fields.get("Status") != "complete":
                raise ContextError("ready task has incomplete dependency: " + ident)
            if _require(tasks[dep].fields, "Completion evidence").lower() == "pending":
                raise ContextError("dependency has no completion evidence: " + dep)
    for ident in blocked:
        if tasks[ident].fields.get("Status") != "blocked":
            raise ContextError("blocked task status disagrees: " + ident)
    return {
        "plan_revision": frontier["Plan revision"],
        "next_task": next_task[0],
        "ready_tasks": ready,
        "blocked_tasks": blocked,
        "relevant_dependency_facts": _items(frontier["Relevant dependency facts"]),
        "active_invariants": _items(frontier["Active invariants"]),
        "pending_final_verification_obligations": _items(
            frontier["Pending final-verification obligations"]
        ),
    }


def _shape(task):
    f, modern = task.fields, "Covers" in task.fields or "Preserves" in task.fields
    capability = _require(f, "Capability")
    if capability not in ("low", "standard", "high"):
        raise ContextError("invalid task capability")
    return {
        "status": _require(f, "Status"),
        "capability": capability,
        "covers": _require(f, "Covers") if modern else _require(f, "Goal"),
        "depends": _require(f, "Depends on"),
        "surface": _require(f, "Change surface"),
        "preserves": _require(f, "Preserves") if modern else _require(f, "Invariants"),
        "implement": _require(f, "Implementation intent")
        if modern
        else f.get("Implementation guidance", ""),
        "prove": _require(f, "Test obligations"),
        "verify": _require(f, "Verification"),
        "return": _require(f, "Return boundary")
        if modern
        else f.get("Decision boundary", ""),
        "watch": f.get("Watch points", ""),
        "legacy": not modern,
    }


def build_resume(plan_text):
    context, tasks, frontier = parse_plan(plan_text)
    active = _validate(context, tasks, frontier)
    task = _shape(tasks[active["next_task"]])
    return {
        "resume": {
            "feature_brief": _require(context, "Feature Brief"),
            "base_revision": _require(context, "Base revision"),
            "plan_revision": active["plan_revision"],
        },
        "active_frontier": active,
        "current_task": {
            "id": active["next_task"],
            "title": tasks[active["next_task"]].title,
            **task,
        },
    }


def _catalog(text, prefix):
    result = {}
    for title, body in _sections(text, 3).items():
        match = re.match(r"(" + prefix + r"-\d+)\s+—\s+.+$", title)
        if not match:
            if title.startswith(prefix + "-"):
                raise ContextError("malformed identifier heading: " + title)
            continue
        identifier = match.group(1)
        if identifier in result:
            raise ContextError("ambiguous identifier: " + identifier)
        if not body:
            raise ContextError("empty accepted clause: " + identifier)
        result[identifier] = "### " + title + "\n" + body
    return result


def _accepted(brief):
    body = _sections(brief, 2).get("Amendments", "")
    out = []
    for title, content in _sections(body, 3).items():
        if not re.match(r"A-\d+\s+—", title):
            raise ContextError("unsupported amendment heading: " + title)
        fields = _fields(content)
        status = _require(fields, "Status")
        if status not in ("Accepted", "Proposed", "Rejected"):
            raise ContextError("invalid amendment status")
        if status == "Accepted":
            _require(fields, "Change")
            out.append("### " + title + "\n" + content)
    return out


def _resolve(value, prefix, catalog, legacy):
    prose = []
    try:
        refs = _ids(value, prefix)
    except ContextError:
        pattern = r"\b" + prefix + r"-\d+\b"
        refs = list(dict.fromkeys(re.findall(pattern, value)))
        remainder = re.sub(pattern, "", value)
        if re.search(r"\b" + prefix + r"-", remainder):
            raise ContextError("malformed clause reference: " + value)
        if not refs:
            return [legacy]
        # Legacy invariants often mix identifiers and task-local prose.
        # Preserve that prose in addition to resolved accepted clauses.
        prose = [value]
    missing = [ref for ref in refs if ref not in catalog]
    if missing:
        raise ContextError("Brief cannot resolve: " + ", ".join(missing))
    return [catalog[ref] for ref in refs] + prose


def _dependency_facts(tasks, deps, frontier):
    out = []
    for dep in deps:
        found = [fact for fact in frontier if re.match(re.escape(dep) + r"\s*:", fact)]
        if len(found) > 1:
            raise ContextError("ambiguous dependency fact: " + dep)
        if found:
            out += found
            continue
        evidence = _require(tasks[dep].fields, "Completion evidence")
        if evidence.lower() == "pending":
            raise ContextError("dependency has no completion evidence: " + dep)
        out.append(dep + ": " + evidence)
    return out


def build_capsule(plan_text, brief_text, task_id):
    context, tasks, frontier = parse_plan(plan_text)
    active = _validate(context, tasks, frontier)
    if task_id != active["next_task"] or task_id not in tasks:
        raise ContextError("task is not dispatch-ready: " + task_id)
    shape = _shape(tasks[task_id])
    top = _sections(brief_text, 2)
    amendments = _accepted(brief_text)
    outcome_text = _require(top, "Expected outcomes")
    constraint_text = _require(top, "Constraints and invariants")
    outcomes = _catalog(outcome_text, "EO")
    invariants = _catalog(constraint_text, "INV")
    outcome = _resolve(shape["covers"], "EO", outcomes, shape["covers"])
    if not outcome:
        raise ContextError("task must cover an accepted outcome")
    preserve = _resolve(shape["preserves"], "INV", invariants, shape["preserves"])
    if shape["legacy"]:
        coverage = _sections(plan_text, 2).get("Coverage", "")
        covered = []
        for line in coverage.splitlines():
            if task_id in re.findall(r"\bT-\d+\b", line):
                covered.extend(re.findall(r"\bEO-\d+\b", line))
        if covered and outcomes:
            outcome += _resolve(", ".join(dict.fromkeys(covered)), "EO", outcomes, "")
        elif not re.search(r"\bEO-\d+\b", shape["covers"]):
            # Resolve legacy heading/text, never send every unrelated outcome
            # to compensate for a plan paraphrase with no accepted mapping.
            clauses = [
                "### " + title + "\n" + body
                for title, body in _sections(outcome_text, 3).items()
            ]
            clauses += outcome_text.split("\n\n") if not clauses else []
            matches = [clause for clause in clauses if shape["covers"] in clause]
            if len(matches) != 1:
                raise ContextError(
                    "legacy outcome needs unambiguous accepted heading/text or coverage mapping"
                )
            outcome.append(matches[0])
    global_text = re.split(r"^### ", constraint_text, flags=re.M)[0].strip()
    if global_text:
        preserve.append(global_text)
    for title, body in _sections(constraint_text, 3).items():
        if not title.startswith("INV-"):
            preserve.append("### " + title + "\n" + body)
    for invariant in active["active_invariants"]:
        if invariant.lower() == "none":
            continue
        match = re.match(r"^(INV-\d+)(?::|\s|$)", invariant)
        if match:
            identifier = match.group(1)
            if identifier not in invariants:
                raise ContextError(
                    "Brief cannot resolve active invariant: " + identifier
                )
            preserve.append(invariants[identifier])
        else:
            preserve.append(invariant)
    preserve += amendments + ([shape["watch"]] if shape["watch"] else [])
    deps = _ids(shape["depends"], "T")
    facts = _dependency_facts(tasks, deps, active["relevant_dependency_facts"])
    return {
        "Outcome": list(dict.fromkeys(outcome)),
        "Own": shape["surface"],
        "Must preserve": list(dict.fromkeys(preserve + facts)),
        "Implement": shape["implement"]
        or "Return to the orchestrator for missing legacy guidance.",
        "Prove": shape["prove"],
        "Verify": shape["verify"],
        "Return instead of guessing if": shape["return"]
        or "Return ambiguity to the orchestrator.",
        "Relevant dependency facts": facts,
        "Plan revision": context["Plan revision"],
    }


def _synthetic(label, files, tasks):
    brief = "## Constraints and invariants\nGlobal read-only constraint.\n### INV-001 — Safety\nDo not mutate.\n## Expected outcomes\n### EO-001 — Bounded\nBounded work.\n## Amendments\nNone.\n"
    old = "\n".join(
        "### T-%03d — Done\n- Status: complete\n- Capability: low\n- Covers: EO-001\n- Depends on: none\n- Change surface: src/%d.py\n- Preserves: INV-001\n- Implementation intent: done\n- Test obligations: done\n- Return boundary: none\n- Verification: true\n- Completion evidence: evidence"
        % (n, n)
        for n in range(1, tasks)
    )
    current = (
        "### T-%03d — Current\n- Status: pending\n- Capability: standard\n- Covers: EO-001\n- Depends on: T-%03d\n- Change surface: src/current.py\n- Preserves: INV-001\n- Implementation intent: bounded\n  continuation\n- Test obligations: focused\n- Return boundary: ambiguity\n- Verification: python -m unittest\n- Completion evidence: pending"
        % (tasks, tasks - 1)
    )
    plan = (
        "## Context\n- Feature Brief: brief.md\n- Base revision: base\n- Plan revision: 1\n## Active frontier\n- Plan revision: 1\n- Next task: T-%03d\n- Ready tasks: T-%03d\n- Blocked tasks: none\n### Relevant dependency facts\n- None\n### Active invariants\n- INV-001: Do not mutate.\n### Pending final-verification obligations\n- integration\n## Coverage\n- EO-001: T-%03d\n## Task graph\n%s\n%s"
        % (tasks, tasks, tasks, old, current)
    )
    return (
        plan,
        brief,
        ["# %s file %d\n" % (label, n) + "x" * (20 + n) for n in range(files)],
    )


def benchmark_report(repo=None):
    repo = repo or Path(__file__).resolve().parents[1]

    def old(path):
        return subprocess.run(
            ["git", "show", BASELINE + ":" + path],
            cwd=repo,
            text=True,
            capture_output=True,
            check=True,
        ).stdout

    def current(path):
        return (repo / path).read_text()

    shared = [
        "references/artifact-contracts.md",
        "references/verification-doctrine.md",
        "references/harness-command-contract.md",
        "references/codex-tools.md",
    ]
    baseline_paths = [
        "skills/build-planned/SKILL.md",
        "references/planned-build-contract.md",
        "references/model-routing.md",
        *shared,
    ]
    current_paths = [
        "skills/build-planned/SKILL.md",
        "runtime/common.md",
        "runtime/planned.md",
        "references/codex-tools.md",
    ]
    baseline_contracts = [old(path) for path in baseline_paths]
    current_contracts = [current(path) for path in current_paths]
    rows = []

    def count(value):
        return len(json.dumps(value, sort_keys=True, ensure_ascii=False))

    for label, files, tasks in (("small", 3, 3), ("medium", 7, 5), ("large", 13, 8)):
        plan, brief, sources = _synthetic(label, files, tasks)
        # Hold relevant code/test evidence equal on both sides; this measures
        # workflow packaging, not a fictional reduction in repository reads.
        relevant = sources[-2:]
        old_package = {
            "contracts": baseline_contracts,
            "brief": brief,
            "plan": plan,
            "source": relevant,
        }
        new_package = {
            "contracts": current_contracts,
            "brief": brief,
            "resume": build_resume(plan),
            "source": relevant,
        }
        capsule = build_capsule(plan, brief, "T-%03d" % tasks)
        worker = {"capsule": capsule, "source": relevant}
        before, after = count(old_package), count(new_package)
        rows.append(
            {
                "size": label,
                "synthetic_source_files": files,
                "synthetic_tasks": tasks,
                "relevant_files_both_packages": len(relevant),
                "baseline_serialized_characters": before,
                "projection_serialized_characters": after,
                "worker_serialized_characters": count(worker),
                "estimated_baseline_tokens": (before + 3) // 4,
                "estimated_projection_tokens": (after + 3) // 4,
                "live_metrics": {
                    key: "unavailable"
                    for key in (
                        "high_capability_input_tokens_per_accepted_feature",
                        "total_tokens",
                        "worker_input_tokens",
                        "repository_files_read",
                        "implementation_success",
                        "review_blockers",
                        "correction_rounds",
                        "successful_clean_resume",
                        "final_defect_rate",
                        "wall_clock_seconds",
                    )
                },
            }
        )
    autonomous_base = [old(path) for path in ["skills/build/SKILL.md", *shared]]
    autonomous_current = [
        current(path)
        for path in [
            "skills/build/SKILL.md",
            "runtime/common.md",
            "runtime/autonomous.md",
            "references/codex-tools.md",
        ]
    ]
    return {
        "baseline_revision": BASELINE,
        "measurement": "Static serialized characters and character/4 token estimates, NOT live model input or measured savings.",
        "baseline_contract_paths": baseline_paths,
        "projection_contract_paths": current_paths,
        "autonomous_small_steady_state": {
            "baseline_serialized_characters": count({"contracts": autonomous_base}),
            "projection_serialized_characters": count(
                {"contracts": autonomous_current}
            ),
            "note": "Fixed contract overhead only; initial-start and final-gate canonical reads excluded from projection.",
        },
        "results": rows,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("resume")
    a.add_argument("plan", type=Path)
    b = sub.add_parser("capsule")
    b.add_argument("plan", type=Path)
    b.add_argument("brief", type=Path)
    b.add_argument("task_id")
    c = sub.add_parser("benchmark")
    c.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        result = (
            build_resume(args.plan.read_text())
            if args.command == "resume"
            else build_capsule(
                args.plan.read_text(), args.brief.read_text(), args.task_id
            )
            if args.command == "capsule"
            else benchmark_report(args.repo)
        )
    except (OSError, subprocess.SubprocessError, ContextError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    main()
