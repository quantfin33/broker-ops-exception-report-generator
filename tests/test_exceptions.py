from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from dataclasses import fields
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ORDER_EVENTS = ROOT / "data" / "sample_order_events.csv"
OUTPUTS = ROOT / "outputs"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from broker_ops_report.config import LIVE_INTEGRATIONS_ALLOWED, NETWORK_DEPENDENCIES
from broker_ops_report.exceptions import BrokerException, classify_severity, detect_exceptions


class BrokerExceptionDetectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.before_outputs = self._output_files()
        self.exceptions = detect_exceptions(ORDER_EVENTS)

    def _output_files(self) -> set[str]:
        return {path.name for path in OUTPUTS.iterdir() if path.is_file()}

    def exception_types(self) -> set[str]:
        return {exception.exception_type for exception in self.exceptions}

    def test_canonical_fixture_detects_received_not_transmitted(self) -> None:
        self.assertIn("received_not_transmitted", self.exception_types())

    def test_canonical_fixture_detects_transmitted_no_final_status(self) -> None:
        self.assertIn("transmitted_no_final_status", self.exception_types())

    def test_canonical_fixture_detects_rejected_without_reason(self) -> None:
        self.assertIn("rejected_without_reason", self.exception_types())

    def test_canonical_fixture_detects_bridge_failed_or_disconnected(self) -> None:
        self.assertIn("bridge_failed_or_disconnected", self.exception_types())

    def test_canonical_fixture_detects_high_latency(self) -> None:
        self.assertIn("high_latency", self.exception_types())

    def test_canonical_fixture_detects_pending_follow_up(self) -> None:
        self.assertIn("pending_follow_up", self.exception_types())

    def test_detected_exceptions_include_required_context(self) -> None:
        self.assertGreater(len(self.exceptions), 0)
        for exception in self.exceptions:
            with self.subTest(exception=exception):
                self.assertIsInstance(exception.severity, str)
                self.assertTrue(exception.severity)
                self.assertIsInstance(exception.event_id, str)
                self.assertTrue(exception.event_id)
                self.assertIsInstance(exception.symbol, str)
                self.assertTrue(exception.symbol)
                self.assertIsInstance(exception.status, str)
                self.assertTrue(exception.status)
                self.assertIsInstance(exception.bridge_status, str)
                self.assertTrue(exception.bridge_status)
                self.assertIsInstance(exception.detail, str)
                self.assertTrue(exception.detail)

    def test_received_not_transmitted_severity_is_critical(self) -> None:
        self.assertEqual(classify_severity("received_not_transmitted"), "Critical")

    def test_transmitted_no_final_status_severity_is_critical(self) -> None:
        self.assertEqual(classify_severity("transmitted_no_final_status"), "Critical")

    def test_bridge_failed_or_disconnected_severity_is_critical(self) -> None:
        self.assertEqual(classify_severity("bridge_failed_or_disconnected"), "Critical")

    def test_rejected_without_reason_severity_is_warning(self) -> None:
        self.assertEqual(classify_severity("rejected_without_reason"), "Warning")

    def test_high_latency_severity_is_warning(self) -> None:
        self.assertEqual(classify_severity("high_latency"), "Warning")

    def test_pending_follow_up_severity_is_warning(self) -> None:
        self.assertEqual(classify_severity("pending_follow_up"), "Warning")

    def test_unknown_exception_type_severity_defaults_to_info(self) -> None:
        self.assertEqual(classify_severity("unknown_exception_type"), "Info")

    def test_all_canonical_fixture_exceptions_include_severity(self) -> None:
        self.assertGreater(len(self.exceptions), 0)
        for exception in self.exceptions:
            with self.subTest(exception=exception):
                self.assertIn(exception.severity, {"Critical", "Warning", "Info"})

    def test_severity_field_exists(self) -> None:
        field_names = {field.name for field in fields(BrokerException)}

        self.assertIn("severity", field_names)

    def test_no_recommended_action_field_exists_yet(self) -> None:
        field_names = {field.name for field in fields(BrokerException)}

        self.assertNotIn("recommended_action", field_names)

    def test_exception_detection_does_not_write_output_files(self) -> None:
        after_outputs = self._output_files()

        self.assertEqual(after_outputs, self.before_outputs)

    def test_no_network_or_live_dependency(self) -> None:
        self.assertFalse(LIVE_INTEGRATIONS_ALLOWED)
        self.assertEqual(NETWORK_DEPENDENCIES, ())

    def test_detection_can_read_temporary_static_csv_without_network(self) -> None:
        with ORDER_EVENTS.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
            headers = list(rows[0].keys())

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_orders = Path(tmpdir) / "orders.csv"
            with temp_orders.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows[:3])

            detected = detect_exceptions(temp_orders)

        self.assertIn(
            "received_not_transmitted",
            {exception.exception_type for exception in detected},
        )


if __name__ == "__main__":
    unittest.main()
