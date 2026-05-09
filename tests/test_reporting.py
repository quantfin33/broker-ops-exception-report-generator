from __future__ import annotations

import csv
import os
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ORDER_EVENTS = ROOT / "data" / "sample_order_events.csv"
MARKET_EVENTS = ROOT / "data" / "sample_market_events.csv"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from broker_ops_report.config import LIVE_INTEGRATIONS_ALLOWED, NETWORK_DEPENDENCIES
from broker_ops_report.reporting import ORDER_EXCEPTION_LOG_HEADERS
from broker_ops_report.schema import ORDER_EVENT_HEADERS


class ExceptionLogReportTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC)
        return subprocess.run(
            [sys.executable, "-m", "broker_ops_report", *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_generate_exception_log_cli_writes_expected_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            result = self.run_cli(
                "generate-reports",
                "--report",
                "exception-log",
                "--orders",
                str(ORDER_EVENTS),
                "--market-events",
                str(MARKET_EVENTS),
                "--output-dir",
                str(output_dir),
            )

            output_path = output_dir / "order_exception_log.csv"
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Report generated: exception-log", result.stdout)
            self.assertTrue(output_path.is_file())

            with output_path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)

            self.assertEqual(reader.fieldnames, ORDER_EXCEPTION_LOG_HEADERS)
            self.assertEqual(len(rows), 14)
            for row in rows:
                with self.subTest(row=row):
                    self.assertTrue(row["exception_type"])
                    self.assertTrue(row["severity"])
                    self.assertTrue(row["recommended_action"])

            severity_counts = Counter(row["severity"] for row in rows)
            self.assertEqual(severity_counts["Critical"], 4)
            self.assertEqual(severity_counts["Warning"], 10)
            self.assertEqual(severity_counts["Info"], 0)

            self.assertFalse((output_dir / "broker_ops_shift_summary.json").exists())
            self.assertFalse((output_dir / "by_symbol_trading_stats.csv").exists())
            self.assertFalse((output_dir / "broker_ops_shift_report.md").exists())
            self.assertEqual(list(output_dir.glob("*.xlsx")), [])

    def test_generate_exception_log_validation_failure_does_not_write_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            bad_orders = tmp_path / "bad_orders.csv"
            output_dir = tmp_path / "outputs"
            with ORDER_EVENTS.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["status"] = "bad_status"
            with bad_orders.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=ORDER_EVENT_HEADERS)
                writer.writeheader()
                writer.writerows(rows)

            result = self.run_cli(
                "generate-reports",
                "--report",
                "exception-log",
                "--orders",
                str(bad_orders),
                "--market-events",
                str(MARKET_EVENTS),
                "--output-dir",
                str(output_dir),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Validation failed.", result.stdout)
            self.assertFalse((output_dir / "order_exception_log.csv").exists())

    def test_no_network_or_live_dependency(self) -> None:
        self.assertFalse(LIVE_INTEGRATIONS_ALLOWED)
        self.assertEqual(NETWORK_DEPENDENCIES, ())


if __name__ == "__main__":
    unittest.main()
