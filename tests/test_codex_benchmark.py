import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.codex_benchmark import CodexCollectorError, _role_stage, arm, finish, scan_sessions, start


def write_session(root, name, session_id, cwd, usage, *, timestamp, model, effort, parent=None, agent_path=""):
    path = root / (name + ".jsonl")
    source = "cli"
    thread_source = "cli"
    if parent:
        source = {"subagent": {"thread_spawn": {"parent_thread_id": parent, "agent_path": agent_path}}}
        thread_source = "subagent"
    rows = [
        {"timestamp": timestamp, "type": "session_meta", "payload": {"cwd": str(cwd), "source": source, "thread_source": thread_source}},
        {"timestamp": timestamp, "type": "response_item", "payload": {"message": "must never be copied"}},
        {"timestamp": timestamp, "type": "turn_context", "payload": {"model": model, "effort": effort, "model_provider": "openai"}},
        {"timestamp": timestamp, "type": "token_usage_record", "payload": {"session_id": session_id, "thread_token_usage": {"input_tokens": usage[0], "output_tokens": usage[1], "cached_input_tokens": usage[2]}}},
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
    return path


class TestCodexBenchmark(unittest.TestCase):
    def test_role_uses_leaf_assignment_before_model_or_ancestor_name(self):
        for model in ("gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol"):
            for path, source, expected in (
                ("", "cli", ("owner", "bootstrap", 0)),
                ("/root/build_owner", "subagent", ("owner", "bootstrap", 0)),
                ("/root/build_owner_final", "subagent", ("owner", "final_verification", 0)),
                ("/root/build_owner_correction", "subagent", ("owner", "correction", 1)),
                ("/root/build_owner/build_worker", "subagent", ("worker", "implementation", 0)),
                ("/root/build_owner/build_worker_correction", "subagent", ("worker", "correction", 1)),
                ("/root/build_owner_correction/build_advisor", "subagent", ("owner", "validation", 0)),
                ("/root/build_owner/build_review", "subagent", ("reviewer", "review", 0)),
            ):
                with self.subTest(model=model, path=path):
                    self.assertEqual(_role_stage({"agent_path": path, "thread_source": source, "model": model}), expected)

    def test_arm_start_finish_generates_valid_redacted_record(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, sessions, output = root / "repo", root / "sessions", root / "out"
            repo.mkdir()
            sessions.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            intent, gates, config = repo / "brief.md", repo / "gates.txt", root / "config.toml"
            intent.write_text("accepted intent")
            gates.write_text("tests\nreview\n")
            config.write_text("model = 'test'")
            write_session(sessions, "root", "root-id", repo, (100, 10, 80), timestamp="2026-09-10T08:00:00Z", model="gpt-5.6-luna", effort="xhigh")
            arm(repo, "feature", "baseline", "0.10", intent, gates, output, config)
            with patch("tools.codex_benchmark._git_head", return_value="abc123"), patch("tools.codex_benchmark._now", return_value="2026-09-10T08:01:00Z"):
                state_path = start(repo, sessions)
            write_session(sessions, "root", "root-id", repo, (130, 15, 100), timestamp="2026-09-10T08:00:00Z", model="gpt-5.6-luna", effort="xhigh")
            write_session(sessions, "advisor", "advisor-id", repo, (10, 2, 5), timestamp="2026-09-10T08:02:00Z", model="gpt-5.6-sol", effort="medium", parent="root-id", agent_path="/root/build_advisor")
            write_session(sessions, "owner", "owner-id", repo, (15, 2, 10), timestamp="2026-09-10T08:02:30Z", model="gpt-5.6-luna", effort="xhigh", parent="root-id", agent_path="/root/build_owner")
            write_session(sessions, "worker", "worker-id", repo, (50, 7, 40), timestamp="2026-09-10T08:02:00Z", model="gpt-5.6-luna", effort="high", parent="root-id", agent_path="/root/t_001")
            write_session(sessions, "review", "review-id", repo, (20, 3, 10), timestamp="2026-09-10T08:03:00Z", model="gpt-6-astra", effort="low", parent="root-id", agent_path="/root/review")
            current = scan_sessions(sessions, repo)
            self.assertEqual(set(current), {"root-id", "owner-id", "advisor-id", "worker-id", "review-id"})
            self.assertEqual(current["root-id"]["usage"]["input_tokens"], 130)
            output_path = finish(repo, sessions, "accepted", ["tests=pass", "review=pass"], 0, 0, state_path)
            record = json.loads(output_path.read_text())
            self.assertEqual(sum(event["tokens"]["input"]["value"] for event in record["events"]), 125)
            self.assertEqual({event["role"] for event in record["events"]}, {"owner", "worker", "reviewer"})
            by_session = {event["tokens"]["input"]["source"]: event for event in record["events"]}
            advisor = by_session["codex-session:advisor-id"]
            self.assertEqual((advisor["role"], advisor["stage"], advisor["launch_count"]), ("owner", "validation", 1))
            self.assertEqual(advisor["rotation_reasons"], [])
            self.assertEqual(by_session["codex-session:owner-id"]["role"], "owner")
            self.assertEqual(by_session["codex-session:root-id"]["role"], "owner")
            self.assertEqual(by_session["codex-session:root-id"]["launch_count"], 0)
            self.assertNotIn("must never be copied", output_path.read_text())
            self.assertFalse((repo / ".git" / "absolutforge-benchmark" / "config.json").exists())

    def test_scanner_rejects_contradictory_session_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, sessions = root / "repo", root / "sessions"
            repo.mkdir()
            sessions.mkdir()
            path = write_session(sessions, "bad", "one", repo, (1, 1, 1), timestamp="2026-09-10T08:00:00Z", model="model", effort="high")
            row = {"timestamp": "2026-09-10T08:01:00Z", "type": "token_usage_record", "payload": {"session_id": "two", "thread_token_usage": {"input_tokens": 2, "output_tokens": 2, "cached_input_tokens": 2}}}
            with path.open("a") as handle:
                handle.write(json.dumps(row) + "\n")
            with self.assertRaisesRegex(CodexCollectorError, "contradictory"):
                scan_sessions(sessions, repo)


if __name__ == "__main__":
    unittest.main()
