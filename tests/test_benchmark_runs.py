import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.benchmark_runs import (
    BenchmarkRecordError,
    aggregate_records,
    load_records,
    validate_record,
)


FIXTURE = Path(__file__).parent / "fixtures" / "token-efficiency-runs.json"


class TestBenchmarkRuns(unittest.TestCase):
    def setUp(self):
        self.records = json.loads(FIXTURE.read_text())

    def test_failed_attempt_cost_and_corrections_roll_into_acceptance(self):
        report = aggregate_records(self.records)
        self.assertEqual(report["not_counted_as_accepted"], [])
        accepted = report["accepted_feature_costs"][0]
        self.assertEqual(accepted["attempt_run_ids"], ["synthetic-a1", "synthetic-a2"])
        self.assertEqual(
            accepted["measured_tokens"],
            {"input": 180, "output": 35, "cached": 15, "total": 215},
        )
        self.assertEqual(accepted["roles"]["worker"]["input"], 0)
        self.assertEqual(accepted["roles"]["worker"]["corrections"], 1)
        self.assertEqual(accepted["measured_wall_time_seconds"], 20)
        self.assertEqual(
            accepted["token_metric_statuses"]["input"],
            {"estimated": 1, "measured": 3},
        )
        self.assertEqual(report["per_feature_totals"]["synthetic-feature"]["total"], 215)
        self.assertEqual(report["per_role_totals"]["owner"]["input"], 130)

    def test_incomplete_run_is_never_accepted_feature_cost(self):
        incomplete = copy.deepcopy(self.records[0])
        incomplete["run_id"] = "incomplete-only"
        incomplete["outcome"] = "incomplete"
        report = aggregate_records([incomplete])
        self.assertEqual(report["accepted_feature_costs"], [])
        self.assertEqual(
            report["not_counted_as_accepted"],
            [{"run_id": "incomplete-only", "outcome": "incomplete"}],
        )

    def test_metric_statuses_are_disjoint_and_measured_requires_provenance(self):
        invented = copy.deepcopy(self.records[0])
        invented["events"][0]["tokens"]["input"] = {
            "status": "measured",
            "value": 999,
        }
        with self.assertRaisesRegex(BenchmarkRecordError, "source"):
            validate_record(invented)
        mixed = copy.deepcopy(self.records[0])
        mixed["events"][0]["tokens"]["input"]["method"] = "guess"
        with self.assertRaisesRegex(BenchmarkRecordError, "incompatible"):
            validate_record(mixed)

    def test_raw_trace_fields_and_secret_shaped_values_are_rejected(self):
        raw = copy.deepcopy(self.records[0])
        raw["prompt"] = "do work"
        with self.assertRaisesRegex(BenchmarkRecordError, "unsupported fields"):
            validate_record(raw)
        secret = copy.deepcopy(self.records[0])
        secret["variant"] = "sk-abcdefghijklmnopqrstuvwxyz123456"
        with self.assertRaisesRegex(BenchmarkRecordError, "secret"):
            validate_record(secret)

    def test_accepted_run_requires_green_gates(self):
        invalid = copy.deepcopy(self.records[1])
        invalid["gates"][0]["result"] = "fail"
        with self.assertRaisesRegex(BenchmarkRecordError, "every declared gate"):
            validate_record(invalid)

    def test_wrong_scalar_types_fail_closed(self):
        wrong = copy.deepcopy(self.records[0])
        wrong["schema_version"] = True
        with self.assertRaises(BenchmarkRecordError):
            validate_record(wrong)
        wrong = copy.deepcopy(self.records[0])
        wrong["events"][0]["rotation_reasons"] = [{}]
        with self.assertRaises(BenchmarkRecordError):
            validate_record(wrong)
        wrong = copy.deepcopy(self.records[0])
        wrong["redaction"]["secrets_removed"] = 1
        with self.assertRaises(BenchmarkRecordError):
            validate_record(wrong)

    def test_loader_accepts_json_array_and_jsonl(self):
        self.assertEqual(load_records([FIXTURE]), self.records)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runs.jsonl"
            path.write_text("\n".join(json.dumps(record) for record in self.records))
            self.assertEqual(load_records([path]), self.records)

    def test_continuations_cannot_change_control_identity_or_branch(self):
        changed = copy.deepcopy(self.records)
        changed[1]["variant"] = "candidate"
        with self.assertRaisesRegex(BenchmarkRecordError, "continuation changes variant"):
            aggregate_records(changed)
        branch = copy.deepcopy(self.records[1])
        branch["run_id"] = "synthetic-a2-branch"
        with self.assertRaisesRegex(BenchmarkRecordError, "may not branch"):
            aggregate_records(self.records + [branch])


if __name__ == "__main__":
    unittest.main()
