from pathlib import Path
import sys
import tempfile
import unittest

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from analysis import analyze_ops_data, apply_owner_mapping, apply_sla_policy, load_sla_policy


class SlaPolicyTests(unittest.TestCase):
    def test_load_sla_policy_and_apply_team_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sla_policy.json"
            path.write_text(
                '{"priority_hours": {"Critical": 5}, "team_priority_hours": {"Support": {"Critical": 2}}}',
                encoding="utf-8",
            )

            policy = load_sla_policy(path)
            df = pd.DataFrame(
                [
                    {"team": "Support", "priority": "Critical", "sla_target_hours": 4},
                    {"team": "Training", "priority": "Critical", "sla_target_hours": 4},
                ]
            )
            updated = apply_sla_policy(df, policy)

        self.assertEqual(updated.loc[0, "sla_target_hours"], 2)
        self.assertEqual(updated.loc[1, "sla_target_hours"], 5)

    def test_owner_mapping_smoke_exports_backlog_by_owner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "ops_tickets.csv"
            output_dir = Path(tmp) / "out"
            pd.DataFrame(
                [
                    {
                        "ticket_id": "T-1",
                        "team": "Support",
                        "priority": "Critical",
                        "created_at": "2026-01-01",
                        "resolved_at": "2026-01-02",
                        "actual_resolution_hours": 6,
                        "sla_target_hours": 4,
                        "backlog_flag": 1,
                        "owner": "",
                    },
                    {
                        "ticket_id": "T-2",
                        "team": "Training",
                        "priority": "Low",
                        "created_at": "2026-01-01",
                        "resolved_at": "2026-01-01",
                        "actual_resolution_hours": 3,
                        "sla_target_hours": 48,
                        "backlog_flag": 0,
                        "owner": "",
                    },
                ]
            ).to_csv(input_path, index=False)

            analyze_ops_data(input_path=input_path, output_dir=output_dir)

            backlog_by_owner_path = output_dir / "backlog_by_owner.csv"
            self.assertTrue(backlog_by_owner_path.exists())
            exported = pd.read_csv(backlog_by_owner_path)

        self.assertIn("Customer Support Lead", set(exported["owner"]))
        self.assertIn("backlog_count", exported.columns)
        mapped = apply_owner_mapping(pd.DataFrame([{"team": "Support", "owner": ""}]))
        self.assertEqual(mapped.loc[0, "owner"], "Customer Support Lead")


if __name__ == "__main__":
    unittest.main()
