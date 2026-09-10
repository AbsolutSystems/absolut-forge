import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.codex_benchmark import CodexCollectorError, arm, finish, scan_sessions, start


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
            write_session(sessions, "root", "root-id", repo, (100, 10, 80), timestamp="2026-09-10T08:00:00Z", model="gpt-5.6-sol", effort="medium")
            arm(repo, "feature", "baseline", "0.10", intent, gates, output, config)
            with patch("tools.codex_benchmark._git_head", return_value="abc123"), patch("tools.codex_benchmark._now", return_value="2026-09-10T08:01:00Z"):
                state_path = start(repo, sessions)
            write_session(sessions, "root", "root-id", repo, (130, 15, 100), timestamp="2026-09-10T08:00:00Z", model="gpt-5.6-sol", effort="medium")
            write_session(sessions, "worker", "worker-id", repo, (50, 7, 40), timestamp="2026-09-10T08:02:00Z", model="gpt-5.6-luna", effort="high", parent="root-id", agent_path="/root/t_001")
            write_session(sessions, "review", "review-id", repo, (20, 3, 10), timestamp="2026-09-10T08:03:00Z", model="gpt-6-astra", effort="low", parent="root-id", agent_path="/root/review")
            current = scan_sessions(sessions, repo)
            self.assertEqual(set(current), {"root-id", "worker-id", "review-id"})
            self.assertEqual(current["root-id"]["usage"]["input_tokens"], 130)
            output_path = finish(repo, sessions, "accepted", ["tests=pass", "review=pass"], 0, 0, state_path)
            record = json.loads(output_path.read_text())
            self.assertEqual(sum(event["tokens"]["input"]["value"] for event in record["events"]), 100)
            self.assertEqual({event["role"] for event in record["events"]}, {"owner", "worker", "reviewer"})
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
