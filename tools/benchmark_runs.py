#!/usr/bin/env python3
"""Validate and aggregate secret-redacted host benchmark run exports."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


SCHEMA_VERSION = 1
RECORD_TYPE = "absolutforge.token-efficiency-run"
ROLES = {"owner", "worker", "reviewer"}
STAGES = {
    "bootstrap",
    "implementation",
    "validation",
    "correction",
    "final_verification",
    "review",
}
OUTCOMES = {"accepted", "rejected", "incomplete"}
METRIC_STATUSES = {"measured", "estimated", "unavailable"}
ROTATION_REASONS = {
    "build_invocation",
    "implementation_checkpoint",
    "context_pressure",
    "replan_or_diagnosis",
    "independent_high_risk_phase",
    "final_verification",
    "unsafe_compaction",
}
SECRET_RE = re.compile(
    r"(?:sk-[A-Za-z0-9_-]{16,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
)


class BenchmarkRecordError(ValueError):
    pass


def _object(value, path, required, optional=()):
    if not isinstance(value, dict):
        raise BenchmarkRecordError(f"{path} must be an object")
    missing = set(required) - set(value)
    extra = set(value) - set(required) - set(optional)
    if missing:
        raise BenchmarkRecordError(f"{path} missing: {', '.join(sorted(missing))}")
    if extra:
        raise BenchmarkRecordError(f"{path} has unsupported fields: {', '.join(sorted(extra))}")
    return value


def _string(value, path, nullable=False):
    if nullable and value is None:
        return value
    if not isinstance(value, str) or not value.strip():
        raise BenchmarkRecordError(f"{path} must be a non-empty string")
    if SECRET_RE.search(value):
        raise BenchmarkRecordError(f"{path} appears to contain a secret")
    return value


def _integer(value, path, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise BenchmarkRecordError(f"{path} must be an integer >= {minimum}")
    return value


def _choice(value, choices, path):
    if not isinstance(value, str) or value not in choices:
        raise BenchmarkRecordError(f"{path} is invalid")
    return value


def _metric(value, path):
    _object(value, path, ("status",), ("value", "source", "counter", "method", "reason"))
    status = value["status"]
    _choice(status, METRIC_STATUSES, f"{path}.status")
    if status == "measured":
        _integer(value.get("value"), f"{path}.value")
        _string(value.get("source"), f"{path}.source")
        _string(value.get("counter"), f"{path}.counter")
        if set(value) - {"status", "value", "source", "counter"}:
            raise BenchmarkRecordError(f"{path} measured metric has incompatible fields")
    elif status == "estimated":
        _integer(value.get("value"), f"{path}.value")
        _string(value.get("method"), f"{path}.method")
        if set(value) - {"status", "value", "method"}:
            raise BenchmarkRecordError(f"{path} estimated metric has incompatible fields")
    else:
        _string(value.get("reason"), f"{path}.reason")
        if set(value) - {"status", "reason"}:
            raise BenchmarkRecordError(f"{path} unavailable metric has incompatible fields")
    return value


def _sha256(value, path):
    _string(value, path)
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", value):
        raise BenchmarkRecordError(f"{path} must be a sha256 digest")


def validate_record(record):
    """Return *record* after strict, non-mutating validation."""
    _object(
        record,
        "record",
        (
            "schema_version",
            "record_type",
            "run_id",
            "feature_id",
            "experiment_id",
            "variant",
            "attempt",
            "continuation_of",
            "outcome",
            "controlled_run",
            "events",
            "gates",
            "review_blockers",
            "wall_time_seconds",
            "redaction",
        ),
    )
    if isinstance(record["schema_version"], bool) or record["schema_version"] != SCHEMA_VERSION:
        raise BenchmarkRecordError("unsupported schema_version")
    if record["record_type"] != RECORD_TYPE:
        raise BenchmarkRecordError("unsupported record_type")
    for field in ("run_id", "feature_id", "experiment_id", "variant"):
        _string(record[field], field)
    _integer(record["attempt"], "attempt", 1)
    _string(record["continuation_of"], "continuation_of", nullable=True)
    _choice(record["outcome"], OUTCOMES, "outcome")

    controlled = _object(
        record["controlled_run"],
        "controlled_run",
        ("accepted_intent_sha256", "base_revision", "gates_sha256", "host_config_sha256", "order"),
    )
    for key in ("accepted_intent_sha256", "gates_sha256", "host_config_sha256"):
        _sha256(controlled[key], f"controlled_run.{key}")
    _string(controlled["base_revision"], "controlled_run.base_revision")
    _integer(controlled["order"], "controlled_run.order", 1)

    if not isinstance(record["events"], list) or not record["events"]:
        raise BenchmarkRecordError("events must be a non-empty array")
    for index, event in enumerate(record["events"]):
        path = f"events[{index}]"
        _object(
            event,
            path,
            ("role", "stage", "provider", "model", "effort", "launch_count", "correction_attempts", "rotation_reasons", "tokens"),
        )
        _choice(event["role"], ROLES, f"{path}.role")
        _choice(event["stage"], STAGES, f"{path}.stage")
        for field in ("provider", "model", "effort"):
            _string(event[field], f"{path}.{field}")
        _integer(event["launch_count"], f"{path}.launch_count")
        _integer(event["correction_attempts"], f"{path}.correction_attempts")
        if not isinstance(event["rotation_reasons"], list):
            raise BenchmarkRecordError(f"{path}.rotation_reasons must be an array")
        for reason in event["rotation_reasons"]:
            _choice(reason, ROTATION_REASONS, f"{path}.rotation_reasons")
        unknown = set(event["rotation_reasons"]) - ROTATION_REASONS
        if unknown:
            raise BenchmarkRecordError(f"{path} has invalid rotation reasons: {', '.join(sorted(unknown))}")
        if len(event["rotation_reasons"]) != len(set(event["rotation_reasons"])):
            raise BenchmarkRecordError(f"{path}.rotation_reasons contains duplicates")
        tokens = _object(event["tokens"], f"{path}.tokens", ("input", "output", "cached"))
        for key in ("input", "output", "cached"):
            _metric(tokens[key], f"{path}.tokens.{key}")

    if not isinstance(record["gates"], list) or not record["gates"]:
        raise BenchmarkRecordError("gates must be a non-empty array")
    gate_names = set()
    for index, gate in enumerate(record["gates"]):
        path = f"gates[{index}]"
        _object(gate, path, ("name", "result"))
        name = _string(gate["name"], f"{path}.name")
        if name in gate_names:
            raise BenchmarkRecordError("gate names must be unique")
        gate_names.add(name)
        _choice(gate["result"], {"pass", "fail", "unavailable"}, f"{path}.result")

    blockers = _object(record["review_blockers"], "review_blockers", ("observed", "escaped"))
    _integer(blockers["observed"], "review_blockers.observed")
    _integer(blockers["escaped"], "review_blockers.escaped")
    _metric(record["wall_time_seconds"], "wall_time_seconds")
    redaction = _object(record["redaction"], "redaction", ("raw_traces_included", "secrets_removed"))
    if (
        redaction["raw_traces_included"] is not False
        or redaction["secrets_removed"] is not True
    ):
        raise BenchmarkRecordError("redaction must exclude raw traces and confirm secret removal")
    if record["outcome"] == "accepted" and any(g["result"] != "pass" for g in record["gates"]):
        raise BenchmarkRecordError("accepted run requires every declared gate to pass")
    return record


def load_records(paths):
    records = []
    for path in paths:
        text = path.read_text()
        try:
            value = json.loads(text)
            values = value if isinstance(value, list) else [value]
        except json.JSONDecodeError:
            values = []
            for line_number, line in enumerate(text.splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    values.append(json.loads(line))
                except json.JSONDecodeError as error:
                    raise BenchmarkRecordError(f"{path}:{line_number}: {error.msg}") from error
        records.extend(validate_record(value) for value in values)
    return records


def _measured(metric):
    return metric["value"] if metric["status"] == "measured" else 0


def aggregate_records(records):
    """Aggregate attempts; only a chain ending in acceptance becomes accepted cost."""
    records = [validate_record(record) for record in records]
    by_id = {}
    for record in records:
        if record["run_id"] in by_id:
            raise BenchmarkRecordError("duplicate run_id: " + record["run_id"])
        by_id[record["run_id"]] = record
    children = defaultdict(list)
    for record in records:
        parent_id = record["continuation_of"]
        if parent_id is None:
            continue
        if parent_id not in by_id:
            raise BenchmarkRecordError("unknown continuation_of: " + parent_id)
        parent = by_id[parent_id]
        for field in ("feature_id", "experiment_id", "variant"):
            if record[field] != parent[field]:
                raise BenchmarkRecordError(f"continuation changes {field}")
        for field in (
            "accepted_intent_sha256",
            "base_revision",
            "gates_sha256",
            "host_config_sha256",
        ):
            if record["controlled_run"][field] != parent["controlled_run"][field]:
                raise BenchmarkRecordError(f"continuation changes controlled_run.{field}")
        if record["attempt"] != parent["attempt"] + 1:
            raise BenchmarkRecordError("continuation attempt must increment by one")
        if parent["outcome"] == "accepted":
            raise BenchmarkRecordError("accepted run cannot be continued")
        children[parent_id].append(record["run_id"])
    if any(len(value) > 1 for value in children.values()):
        raise BenchmarkRecordError("attempt chains may not branch")

    def chain(record):
        seen, result = set(), []
        while record is not None:
            if record["run_id"] in seen:
                raise BenchmarkRecordError("continuation cycle")
            seen.add(record["run_id"])
            result.append(record)
            parent = record["continuation_of"]
            record = by_id[parent] if parent else None
        return list(reversed(result))

    accepted, incomplete = [], []
    accepted_ids = set()
    for terminal in records:
        if terminal["outcome"] != "accepted":
            continue
        attempts = chain(terminal)
        accepted_ids.update(item["run_id"] for item in attempts)
        roles = defaultdict(lambda: {"input": 0, "output": 0, "cached": 0, "launches": 0, "corrections": 0})
        total = {"input": 0, "output": 0, "cached": 0}
        rotations = defaultdict(int)
        metric_statuses = defaultdict(lambda: defaultdict(int))
        for attempt in attempts:
            for event in attempt["events"]:
                role = roles[event["role"]]
                role["launches"] += event["launch_count"]
                role["corrections"] += event["correction_attempts"]
                for kind in total:
                    metric_statuses[kind][event["tokens"][kind]["status"]] += 1
                    amount = _measured(event["tokens"][kind])
                    total[kind] += amount
                    role[kind] += amount
                for reason in event["rotation_reasons"]:
                    rotations[reason] += 1
        accepted.append({
            "feature_id": terminal["feature_id"],
            "experiment_id": terminal["experiment_id"],
            "variant": terminal["variant"],
            "accepted_run_id": terminal["run_id"],
            "attempt_run_ids": [item["run_id"] for item in attempts],
            "measured_tokens": {**total, "total": total["input"] + total["output"]},
            "token_metric_statuses": {
                kind: dict(sorted(statuses.items()))
                for kind, statuses in sorted(metric_statuses.items())
            },
            "roles": {key: value for key, value in sorted(roles.items())},
            "rotation_reasons": dict(sorted(rotations.items())),
            "review_blockers": {
                "observed": sum(item["review_blockers"]["observed"] for item in attempts),
                "escaped": terminal["review_blockers"]["escaped"],
            },
            "measured_wall_time_seconds": sum(_measured(item["wall_time_seconds"]) for item in attempts),
        })
    for record in records:
        if record["run_id"] not in accepted_ids:
            incomplete.append({"run_id": record["run_id"], "outcome": record["outcome"]})
    per_feature = defaultdict(
        lambda: {"accepted_runs": 0, "attempts": 0, "input": 0, "output": 0, "cached": 0, "total": 0}
    )
    per_role = defaultdict(
        lambda: {"input": 0, "output": 0, "cached": 0, "launches": 0, "corrections": 0}
    )
    for item in accepted:
        feature = per_feature[item["feature_id"]]
        feature["accepted_runs"] += 1
        feature["attempts"] += len(item["attempt_run_ids"])
        for kind in ("input", "output", "cached", "total"):
            feature[kind] += item["measured_tokens"][kind]
        for role_name, role_values in item["roles"].items():
            for key, value in role_values.items():
                per_role[role_name][key] += value
    return {
        "schema_version": SCHEMA_VERSION,
        "accepted_feature_costs": sorted(accepted, key=lambda item: item["accepted_run_id"]),
        "per_feature_totals": {key: value for key, value in sorted(per_feature.items())},
        "per_role_totals": {key: value for key, value in sorted(per_role.items())},
        "not_counted_as_accepted": sorted(incomplete, key=lambda item: item["run_id"]),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("records", type=Path, nargs="+")
    aggregate = subparsers.add_parser("aggregate")
    aggregate.add_argument("records", type=Path, nargs="+")
    args = parser.parse_args(argv)
    try:
        records = load_records(args.records)
        result = (
            {"schema_version": SCHEMA_VERSION, "valid_records": len(records)}
            if args.command == "validate"
            else aggregate_records(records)
        )
    except (OSError, BenchmarkRecordError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    main()
