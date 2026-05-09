from __future__ import annotations

import csv
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ORDER_EVENTS = ROOT / "data" / "sample_order_events.csv"
MARKET_EVENTS = ROOT / "data" / "sample_market_events.csv"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from broker_ops_report.schema import MARKET_EVENT_HEADERS, ORDER_EVENT_HEADERS
from broker_ops_report.validation import validate_inputs


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


class CsvValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.order_rows = read_rows(ORDER_EVENTS)
        self.market_rows = read_rows(MARKET_EVENTS)

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

    def assert_validation_fails_with(self, result, expected_text: str) -> None:
        self.assertFalse(result.ok)
        formatted = "\n".join(issue.format() for issue in result.issues)
        self.assertIn(expected_text, formatted)

    def test_valid_fixture_files_pass(self) -> None:
        result = validate_inputs(ORDER_EVENTS, MARKET_EVENTS)

        self.assertTrue(result.ok, [issue.format() for issue in result.issues])
        self.assertEqual(result.order_rows, 20)
        self.assertEqual(result.market_event_rows, 5)

    def test_missing_required_order_column_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_orders = Path(tmpdir) / "bad_orders.csv"
            headers = [header for header in ORDER_EVENT_HEADERS if header != "status"]
            rows = [{key: value for key, value in self.order_rows[0].items() if key != "status"}]
            write_rows(bad_orders, headers, rows)

            result = validate_inputs(bad_orders, MARKET_EVENTS)

        self.assert_validation_fails_with(result, "required header is missing")
        self.assert_validation_fails_with(result, "status")

    def test_invalid_status_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_orders = Path(tmpdir) / "bad_orders.csv"
            rows = [dict(self.order_rows[0], status="done")]
            write_rows(bad_orders, ORDER_EVENT_HEADERS, rows)

            result = validate_inputs(bad_orders, MARKET_EVENTS)

        self.assert_validation_fails_with(result, "invalid value 'done'")

    def test_invalid_bridge_status_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_orders = Path(tmpdir) / "bad_orders.csv"
            rows = [dict(self.order_rows[0], bridge_status="unstable")]
            write_rows(bad_orders, ORDER_EVENT_HEADERS, rows)

            result = validate_inputs(bad_orders, MARKET_EVENTS)

        self.assert_validation_fails_with(result, "invalid value 'unstable'")

    def test_missing_core_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_orders = Path(tmpdir) / "bad_orders.csv"
            rows = [dict(self.order_rows[0], symbol="")]
            write_rows(bad_orders, ORDER_EVENT_HEADERS, rows)

            result = validate_inputs(bad_orders, MARKET_EVENTS)

        self.assert_validation_fails_with(result, "required field is blank")
        self.assert_validation_fails_with(result, "symbol")

    def test_invalid_timestamp_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_orders = Path(tmpdir) / "bad_orders.csv"
            rows = [dict(self.order_rows[0], timestamp_utc="2026-05-07 12:28:10")]
            write_rows(bad_orders, ORDER_EVENT_HEADERS, rows)

            result = validate_inputs(bad_orders, MARKET_EVENTS)

        self.assert_validation_fails_with(result, "timestamp must be UTC ISO-style")

    def test_invalid_numeric_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_orders = Path(tmpdir) / "bad_orders.csv"
            rows = [dict(self.order_rows[0], latency_ms="slow")]
            write_rows(bad_orders, ORDER_EVENT_HEADERS, rows)

            result = validate_inputs(bad_orders, MARKET_EVENTS)

        self.assert_validation_fails_with(result, "numeric field could not be parsed")

    def test_missing_market_event_column_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_market_events = Path(tmpdir) / "bad_market_events.csv"
            headers = [header for header in MARKET_EVENT_HEADERS if header != "related_symbols"]
            rows = [
                {key: value for key, value in self.market_rows[0].items() if key != "related_symbols"}
            ]
            write_rows(bad_market_events, headers, rows)

            result = validate_inputs(ORDER_EVENTS, bad_market_events)

        self.assert_validation_fails_with(result, "required header is missing")
        self.assert_validation_fails_with(result, "related_symbols")

    def test_missing_input_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            missing_orders = Path(tmpdir) / "missing_orders.csv"

            result = validate_inputs(missing_orders, MARKET_EVENTS)

        self.assert_validation_fails_with(result, "CSV file does not exist")

    def test_validate_inputs_cli_returns_zero_for_current_fixtures(self) -> None:
        result = self.run_cli(
            "validate-inputs",
            "--orders",
            str(ORDER_EVENTS),
            "--market-events",
            str(MARKET_EVENTS),
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validation successful.", result.stdout)

    def test_validate_inputs_cli_returns_nonzero_for_bad_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_orders = Path(tmpdir) / "bad_orders.csv"
            rows = [dict(self.order_rows[0], status="bad_status")]
            write_rows(bad_orders, ORDER_EVENT_HEADERS, rows)

            result = self.run_cli(
                "validate-inputs",
                "--orders",
                str(bad_orders),
                "--market-events",
                str(MARKET_EVENTS),
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Validation failed.", result.stdout)
        self.assertIn("bad_status", result.stdout)

    def test_no_network_or_live_dependency(self) -> None:
        import broker_ops_report.config as config

        self.assertFalse(config.LIVE_INTEGRATIONS_ALLOWED)
        self.assertEqual(config.NETWORK_DEPENDENCIES, ())


if __name__ == "__main__":
    unittest.main()
