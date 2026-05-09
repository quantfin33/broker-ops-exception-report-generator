from __future__ import annotations

import csv
import json
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
from broker_ops_report.exceptions import detect_exceptions
from broker_ops_report.reporting import (
    ORDER_EXCEPTION_LOG_HEADERS,
    SHIFT_SUMMARY_FILENAME,
    SYMBOL_STATS_FILENAME,
    SYMBOL_STATS_HEADERS,
)
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
            self.assertEqual(list(output_dir.glob("*.html")), [])

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

    def test_generate_shift_summary_cli_writes_expected_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            result = self.run_cli(
                "generate-reports",
                "--report",
                "shift-summary",
                "--orders",
                str(ORDER_EVENTS),
                "--market-events",
                str(MARKET_EVENTS),
                "--output-dir",
                str(output_dir),
            )

            output_path = output_dir / SHIFT_SUMMARY_FILENAME
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Report generated: shift-summary", result.stdout)
            self.assertTrue(output_path.is_file())

            summary = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(
                set(summary),
                {
                    "project_name",
                    "generated_at_utc",
                    "input_files",
                    "validation_summary",
                    "order_summary",
                    "exception_summary",
                    "severity_breakdown",
                    "exception_type_breakdown",
                    "unresolved_items",
                    "output_files",
                    "non_claims",
                },
            )
            self.assertEqual(summary["order_summary"]["total_order_rows"], 20)
            self.assertEqual(summary["order_summary"]["total_market_event_rows"], 5)
            self.assertEqual(summary["exception_summary"]["total_exceptions"], 14)
            self.assertEqual(summary["exception_summary"]["highest_severity_present"], "Critical")
            self.assertEqual(summary["exception_summary"]["unresolved_exception_count"], 4)
            self.assertEqual(summary["exception_summary"]["total_exceptions"], len(detect_exceptions(ORDER_EVENTS)))
            self.assertEqual(summary["severity_breakdown"], {"Critical": 4, "Warning": 10, "Info": 0})
            self.assertEqual(
                summary["exception_type_breakdown"],
                {
                    "received_not_transmitted": 1,
                    "transmitted_no_final_status": 1,
                    "rejected_without_reason": 1,
                    "bridge_failed_or_disconnected": 2,
                    "high_latency": 7,
                    "pending_follow_up": 2,
                },
            )

            validation_summary = summary["validation_summary"]
            self.assertTrue(validation_summary["validation_passed"])
            self.assertEqual(validation_summary["validation_error_count"], 0)
            self.assertEqual(validation_summary["duplicate_id_failures"], 0)
            self.assertEqual(validation_summary["missing_required_field_failures"], 0)
            self.assertIn("validation failures", validation_summary["note"])

            non_claims = " ".join(summary["non_claims"])
            self.assertIn("Static broker operations reporting demo only.", non_claims)
            self.assertIn("Does not perform live trading.", non_claims)
            self.assertIn("Does not integrate with broker APIs.", non_claims)
            self.assertIn("Does not integrate with MT4/MT5.", non_claims)
            self.assertIn("Does not perform live monitoring.", non_claims)
            self.assertIn("Does not prove broker administrator access.", non_claims)
            self.assertIn("Not investment or trading advice.", non_claims)

            self.assertFalse((output_dir / "order_exception_log.csv").exists())
            self.assertFalse((output_dir / "by_symbol_trading_stats.csv").exists())
            self.assertFalse((output_dir / "broker_ops_shift_report.md").exists())
            self.assertEqual(list(output_dir.glob("*.xlsx")), [])
            self.assertEqual(list(output_dir.glob("*.html")), [])

    def test_generate_symbol_stats_cli_writes_expected_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            result = self.run_cli(
                "generate-reports",
                "--report",
                "symbol-stats",
                "--orders",
                str(ORDER_EVENTS),
                "--market-events",
                str(MARKET_EVENTS),
                "--output-dir",
                str(output_dir),
            )

            output_path = output_dir / SYMBOL_STATS_FILENAME
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Report generated: symbol-stats", result.stdout)
            self.assertTrue(output_path.is_file())

            with ORDER_EVENTS.open(newline="", encoding="utf-8") as handle:
                order_rows = list(csv.DictReader(handle))
            unique_symbols = sorted({row["symbol"] for row in order_rows})

            with output_path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)

            self.assertEqual(reader.fieldnames, SYMBOL_STATS_HEADERS)
            self.assertEqual([row["symbol"] for row in rows], unique_symbols)
            self.assertEqual(len(rows), len(unique_symbols))
            self.assertEqual(sum(int(row["total_orders"]) for row in rows), 20)
            self.assertEqual(sum(int(row["exception_count"]) for row in rows), 14)
            self.assertEqual(sum(int(row["critical_exception_count"]) for row in rows), 4)
            self.assertEqual(sum(int(row["warning_exception_count"]) for row in rows), 10)

            numeric_fields = (
                "total_volume",
                "average_latency_ms",
                "max_latency_ms",
                "total_pnl_usd",
            )
            for row in rows:
                with self.subTest(symbol=row["symbol"]):
                    self.assertTrue(row["asset_class"])
                    for field_name in numeric_fields:
                        float(row[field_name])

            self.assertFalse((output_dir / "order_exception_log.csv").exists())
            self.assertFalse((output_dir / SHIFT_SUMMARY_FILENAME).exists())
            self.assertFalse((output_dir / "broker_ops_shift_report.md").exists())
            self.assertEqual(list(output_dir.glob("*.xlsx")), [])
            self.assertEqual(list(output_dir.glob("*.html")), [])

    def test_generate_symbol_stats_validation_failure_does_not_write_report(self) -> None:
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
                "symbol-stats",
                "--orders",
                str(bad_orders),
                "--market-events",
                str(MARKET_EVENTS),
                "--output-dir",
                str(output_dir),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Validation failed.", result.stdout)
            self.assertFalse((output_dir / SYMBOL_STATS_FILENAME).exists())

    def test_generate_shift_summary_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            command = (
                "generate-reports",
                "--report",
                "shift-summary",
                "--orders",
                str(ORDER_EVENTS),
                "--market-events",
                str(MARKET_EVENTS),
                "--output-dir",
                str(output_dir),
            )

            first = self.run_cli(*command)
            first_bytes = (output_dir / SHIFT_SUMMARY_FILENAME).read_bytes()
            second = self.run_cli(*command)
            second_bytes = (output_dir / SHIFT_SUMMARY_FILENAME).read_bytes()

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(first_bytes, second_bytes)

    def test_generate_shift_summary_validation_failure_does_not_write_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            bad_orders = tmp_path / "bad_orders.csv"
            output_dir = tmp_path / "outputs"
            with ORDER_EVENTS.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["client_order_id"] = rows[1]["client_order_id"]
            with bad_orders.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=ORDER_EVENT_HEADERS)
                writer.writeheader()
                writer.writerows(rows)

            result = self.run_cli(
                "generate-reports",
                "--report",
                "shift-summary",
                "--orders",
                str(bad_orders),
                "--market-events",
                str(MARKET_EVENTS),
                "--output-dir",
                str(output_dir),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Validation failed.", result.stdout)
            self.assertFalse((output_dir / SHIFT_SUMMARY_FILENAME).exists())

    def test_no_network_or_live_dependency(self) -> None:
        self.assertFalse(LIVE_INTEGRATIONS_ALLOWED)
        self.assertEqual(NETWORK_DEPENDENCIES, ())


if __name__ == "__main__":
    unittest.main()
