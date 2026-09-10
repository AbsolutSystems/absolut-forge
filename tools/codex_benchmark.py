#!/usr/bin/env python3
"""Opt-in Codex session collector for token-efficiency benchmark records.

This adapter deliberately reads only session metadata, turn context metadata,
and token_usage_record lines. The local Codex session format is not a public
API; unknown or contradictory shapes fail closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

try:
    from tools.benchmark_runs import BenchmarkRecordError, validate_record
except ModuleNotFoundError:  # Direct execution from an installed plugin path.
    from benchmark_runs import BenchmarkRecordError, validate_record


ADAPTER_VERSION = 1
CONFIG_NAME = "config.json"
STATE_NAME = "state.json"
USAGE_KEYS = ("input_tokens", "output_tokens", "cached_input_tokens")


class CodexCollectorError(ValueError):
    pass


def _now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_time(value):
    if not isinstance(value, str):
        raise CodexCollectorError("session timestamp is missing")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise CodexCollectorError("invalid session timestamp") from error


def _digest(path):
    try:
        data = path.read_bytes()
    except OSError as error:
        raise CodexCollectorError(f"cannot hash {path}: {error}") from error
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _git_head(repo):
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
    except subprocess.SubprocessError as error:
        raise CodexCollectorError("cannot resolve repository HEAD") from error


def _marker(repo):
    try:
        path = subprocess.run(
            ["git", "rev-parse", "--git-path", "absolutforge-benchmark"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
    except subprocess.SubprocessError as error:
        raise CodexCollectorError("cannot resolve repository-local benchmark state") from error
    resolved = Path(path)
    return resolved if resolved.is_absolute() else (repo / resolved).resolve()


def _write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def arm(repo, feature_id, experiment_id, variant, intent, gates, output_dir, host_config):
    """Create a gitignored opt-in marker; no session data is read yet."""
    repo = repo.resolve()
    marker = _marker(repo)
    config_path = marker / CONFIG_NAME
    state_path = marker / STATE_NAME
    if config_path.exists() or state_path.exists():
        raise CodexCollectorError("benchmark capture is already armed or active")
    for path, label in ((intent, "accepted intent"), (gates, "gates"), (host_config, "host config")):
        if not path.is_file():
            raise CodexCollectorError(f"{label} file does not exist: {path}")
    config = {
        "adapter_version": ADAPTER_VERSION,
        "feature_id": feature_id,
        "experiment_id": experiment_id,
        "variant": variant,
        "accepted_intent": str(intent.resolve()),
        "gates": str(gates.resolve()),
        "host_config": str(host_config.resolve()),
        "output_dir": str(output_dir.resolve()),
    }
    _write_json(config_path, config)
    return config_path


def _read_relevant_lines(path):
    metadata = None
    metadata_time = None
    latest_context = {}
    latest_usage = None
    latest_usage_time = None
    session_id = None
    try:
        with path.open() as handle:
            for line in handle:
                if not any(marker in line for marker in ('"session_meta"', '"turn_context"', '"token_usage_record"')):
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as error:
                    raise CodexCollectorError(f"invalid JSON in Codex session {path.name}") from error
                payload = item.get("payload")
                if not isinstance(payload, dict):
                    raise CodexCollectorError(f"unsupported Codex session payload in {path.name}")
                if item.get("type") == "session_meta":
                    metadata = payload
                    metadata_time = item.get("timestamp")
                elif item.get("type") == "turn_context":
                    latest_context = payload
                elif item.get("type") == "token_usage_record":
                    usage = payload.get("thread_token_usage")
                    if not isinstance(usage, dict):
                        raise CodexCollectorError(f"missing cumulative token usage in {path.name}")
                    values = {}
                    for key in USAGE_KEYS:
                        value = usage.get(key)
                        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                            raise CodexCollectorError(f"invalid {key} in {path.name}")
                        values[key] = value
                    latest_usage = values
                    latest_usage_time = item.get("timestamp")
                    token_session_id = payload.get("session_id")
                    if not isinstance(token_session_id, str) or not token_session_id:
                        raise CodexCollectorError(f"missing Codex session id in {path.name}")
                    if session_id is not None and token_session_id != session_id:
                        raise CodexCollectorError(f"contradictory Codex session id in {path.name}")
                    session_id = token_session_id
    except OSError as error:
        raise CodexCollectorError(f"cannot read Codex session {path}: {error}") from error
    if metadata is None or latest_usage is None:
        return None
    source = metadata.get("source")
    spawn = source.get("subagent", {}).get("thread_spawn", {}) if isinstance(source, dict) else {}
    collaboration = metadata.get("collaboration_mode")
    settings = collaboration.get("settings", {}) if isinstance(collaboration, dict) else {}
    base = metadata.get("base_instructions")
    provenance = base.get("provenance", {}) if isinstance(base, dict) else {}
    return {
        "session_id": session_id,
        "cwd": metadata.get("cwd"),
        "created_at": metadata_time,
        "usage_at": latest_usage_time,
        "usage": latest_usage,
        "thread_source": metadata.get("thread_source"),
        "parent_session_id": spawn.get("parent_thread_id"),
        "agent_path": spawn.get("agent_path") or "",
        "model": latest_context.get("model") or settings.get("model") or provenance.get("model"),
        "effort": latest_context.get("effort") or metadata.get("effort") or settings.get("reasoning_effort"),
        "provider": latest_context.get("model_provider") or metadata.get("model_provider"),
    }


def scan_sessions(session_root, repo):
    repo = repo.resolve()
    sessions = {}
    for path in sorted(session_root.glob("**/*.jsonl")):
        session = _read_relevant_lines(path)
        if session is None:
            continue
        cwd = session["cwd"]
        if not isinstance(cwd, str) or Path(cwd).resolve() != repo:
            continue
        ident = session["session_id"]
        if ident in sessions:
            raise CodexCollectorError("duplicate Codex session id: " + ident)
        sessions[ident] = session
    return sessions


def start(repo, session_root, config_path=None):
    repo = repo.resolve()
    marker = _marker(repo)
    config_path = config_path or marker / CONFIG_NAME
    state_path = marker / STATE_NAME
    if state_path.exists():
        return state_path
    try:
        config = json.loads(config_path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise CodexCollectorError("benchmark capture is not armed with a valid config") from error
    if config.get("adapter_version") != ADAPTER_VERSION:
        raise CodexCollectorError("unsupported Codex benchmark adapter version")
    sessions = scan_sessions(session_root, repo)
    state = {
        "adapter_version": ADAPTER_VERSION,
        "run_id": "codex-" + uuid.uuid4().hex,
        "started_at": _now(),
        "repo": str(repo),
        "base_revision": _git_head(repo),
        "feature_id": config["feature_id"],
        "experiment_id": config["experiment_id"],
        "variant": config["variant"],
        "accepted_intent_sha256": _digest(Path(config["accepted_intent"])),
        "gates_sha256": _digest(Path(config["gates"])),
        "host_config_sha256": _digest(Path(config["host_config"])),
        "output_dir": config["output_dir"],
        "baseline_usage": {key: value["usage"] for key, value in sessions.items()},
    }
    _write_json(state_path, state)
    return state_path


def _delta(current, baseline):
    result = {}
    for key in USAGE_KEYS:
        value = current[key] - baseline.get(key, 0)
        if value < 0:
            raise CodexCollectorError("Codex cumulative usage moved backwards")
        result[key] = value
    return result


def _role_stage(session):
    path = session["agent_path"].lower()
    model = (session["model"] or "").lower()
    if "review" in path:
        return "reviewer", "review", 0
    if "correction" in path or "_fix" in path or "/fix" in path:
        return ("worker" if "luna" in model else "owner"), "correction", 1
    if "final" in path:
        return "owner", "final_verification", 0
    if "luna" in model:
        return "worker", "implementation", 0
    if session["thread_source"] == "subagent":
        return "owner", "validation" if "advisor" in path else "implementation", 0
    return "owner", "bootstrap", 0


def finish(repo, session_root, outcome, gates, observed_blockers, escaped_blockers, state_path=None):
    repo = repo.resolve()
    marker = _marker(repo)
    state_path = state_path or marker / STATE_NAME
    config_path = marker / CONFIG_NAME
    try:
        state = json.loads(state_path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise CodexCollectorError("no valid active benchmark state") from error
    if state.get("adapter_version") != ADAPTER_VERSION or state.get("repo") != str(repo):
        raise CodexCollectorError("benchmark state does not match this repository")
    started = _parse_time(state["started_at"])
    sessions = scan_sessions(session_root, repo)
    events = []
    owner_launch = 0
    for ident, session in sorted(sessions.items(), key=lambda item: item[1]["created_at"] or ""):
        baseline = state["baseline_usage"].get(ident, {})
        usage = _delta(session["usage"], baseline)
        if not any(usage.values()):
            continue
        if not baseline and _parse_time(session["created_at"]) < started:
            raise CodexCollectorError("newly discovered session predates capture start")
        role, stage, corrections = _role_stage(session)
        rotations = []
        if role == "owner" and session["thread_source"] == "subagent":
            rotations = ["build_invocation" if owner_launch == 0 else "implementation_checkpoint"]
            if stage == "final_verification":
                rotations = ["final_verification"]
            owner_launch += 1
        source = "codex-session:" + ident
        events.append({
            "role": role,
            "stage": stage,
            "provider": session["provider"] or "codex-host-unreported",
            "model": session["model"] or "codex-host-unreported",
            "effort": session["effort"] or "codex-host-unreported",
            "launch_count": 1 if session["thread_source"] == "subagent" else 0,
            "correction_attempts": corrections,
            "rotation_reasons": rotations,
            "tokens": {
                "input": {"status": "measured", "value": usage["input_tokens"], "source": source, "counter": "thread_token_usage.input_tokens"},
                "output": {"status": "measured", "value": usage["output_tokens"], "source": source, "counter": "thread_token_usage.output_tokens"},
                "cached": {"status": "measured", "value": usage["cached_input_tokens"], "source": source, "counter": "thread_token_usage.cached_input_tokens"},
            },
        })
    if not events:
        raise CodexCollectorError("no Codex token usage was recorded after capture start")
    gate_records = []
    for value in gates:
        if "=" not in value:
            raise CodexCollectorError("gate must use name=pass|fail|unavailable")
        name, result = value.split("=", 1)
        gate_records.append({"name": name, "result": result})
    elapsed = max(0, int((datetime.now(timezone.utc) - started).total_seconds()))
    record = {
        "schema_version": 1,
        "record_type": "absolutforge.token-efficiency-run",
        "run_id": state["run_id"],
        "feature_id": state["feature_id"],
        "experiment_id": state["experiment_id"],
        "variant": state["variant"],
        "attempt": 1,
        "continuation_of": None,
        "outcome": outcome,
        "controlled_run": {
            "accepted_intent_sha256": state["accepted_intent_sha256"],
            "base_revision": state["base_revision"],
            "gates_sha256": state["gates_sha256"],
            "host_config_sha256": state["host_config_sha256"],
            "order": 1,
        },
        "events": events,
        "gates": gate_records,
        "review_blockers": {"observed": observed_blockers, "escaped": escaped_blockers},
        "wall_time_seconds": {"status": "measured", "value": elapsed, "source": "codex-benchmark-clock", "counter": "elapsed_seconds"},
        "redaction": {"raw_traces_included": False, "secrets_removed": True},
    }
    try:
        validate_record(record)
    except BenchmarkRecordError as error:
        raise CodexCollectorError(str(error)) from error
    output = Path(state["output_dir"]) / (state["run_id"] + ".json")
    _write_json(output, record)
    state_path.unlink()
    config_path.unlink(missing_ok=True)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--session-root", type=Path, default=Path.home() / ".codex" / "sessions")
    sub = parser.add_subparsers(dest="command", required=True)
    arm_parser = sub.add_parser("arm")
    arm_parser.add_argument("--feature-id", required=True)
    arm_parser.add_argument("--experiment-id", required=True)
    arm_parser.add_argument("--variant", required=True)
    arm_parser.add_argument("--intent", type=Path, required=True)
    arm_parser.add_argument("--gates", type=Path, required=True)
    arm_parser.add_argument("--output-dir", type=Path, required=True)
    arm_parser.add_argument("--host-config", type=Path, default=Path.home() / ".codex" / "config.toml")
    sub.add_parser("start")
    finish_parser = sub.add_parser("finish")
    finish_parser.add_argument("--outcome", choices=("accepted", "rejected", "incomplete"), required=True)
    finish_parser.add_argument("--gate", action="append", default=[], required=True)
    finish_parser.add_argument("--observed-blockers", type=int, default=0)
    finish_parser.add_argument("--escaped-blockers", type=int, default=0)
    args = parser.parse_args(argv)
    try:
        if args.command == "arm":
            result = arm(args.repo, args.feature_id, args.experiment_id, args.variant, args.intent, args.gates, args.output_dir, args.host_config)
        elif args.command == "start":
            result = start(args.repo, args.session_root)
        else:
            result = finish(args.repo, args.session_root, args.outcome, args.gate, args.observed_blockers, args.escaped_blockers)
    except (OSError, CodexCollectorError) as error:
        parser.error(str(error))
    print(result)
    return 0


if __name__ == "__main__":
    main()
