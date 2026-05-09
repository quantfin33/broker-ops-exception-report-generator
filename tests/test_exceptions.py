from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from collections import Counter
from dataclasses import fields
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ORDER_EVENTS = ROOT / "data" / "sample_order_events.csv"
OUTPUTS = ROOT / "outputs"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from broker_ops_report.config import LIVE_INTEGRATIONS_ALLOWED, NETWORK_DEPENDENCIES
from broker_ops_report.exceptions import (
    BrokerException,
    classify_severity,
    detect_exceptions,
    recommend_action,
)


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
                self.assertIsInstance(exception.recommended_action, str)
                self.assertTrue(exception.recommended_action)
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

    def test_received_not_transmitted_recommended_action(self) -> None:
        self.assertEqual(
            recommend_action("received_not_transmitted"),
            (
                "Review platform queue/routing state and confirm whether the order should be "
                "transmitted, cancelled, or escalated."
            ),
        )

    def test_transmitted_no_final_status_recommended_action(self) -> None:
        self.assertEqual(
            recommend_action("transmitted_no_final_status"),
            (
                "Check downstream execution/bridge response and follow up until a final fill, "
                "reject, cancel, fail, or expiry status is recorded."
            ),
        )

    def test_rejected_without_reason_recommended_action(self) -> None:
        self.assertEqual(
            recommend_action("rejected_without_reason"),
            (
                "Investigate missing rejection reason and update the operational record with a "
                "clear rejection explanation."
            ),
        )

    def test_bridge_failed_or_disconnected_recommended_action(self) -> None:
        self.assertEqual(
            recommend_action("bridge_failed_or_disconnected"),
            (
                "Escalate bridge or liquidity-provider connectivity issue to "
                "platform/risk/technical support and monitor affected symbols."
            ),
        )

    def test_high_latency_recommended_action(self) -> None:
        self.assertEqual(
            recommend_action("high_latency"),
            (
                "Review execution latency against operational thresholds and check whether the "
                "symbol, route, or bridge showed delays."
            ),
        )

    def test_pending_follow_up_recommended_action(self) -> None:
        self.assertEqual(
            recommend_action("pending_follow_up"),
            (
                "Carry forward to shift handover and confirm the order reaches a final status "
                "or is otherwise resolved."
            ),
        )

    def test_unknown_exception_type_recommended_action_fails_clearly(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown exception type"):
            recommend_action("unknown_exception_type")

    def test_recommended_action_field_exists(self) -> None:
        field_names = {field.name for field in fields(BrokerException)}

        self.assertIn("recommended_action", field_names)

    def test_all_canonical_fixture_exceptions_include_recommended_action(self) -> None:
        self.assertGreater(len(self.exceptions), 0)
        for exception in self.exceptions:
            with self.subTest(exception=exception):
                self.assertTrue(exception.recommended_action)

    def test_total_canonical_fixture_exception_count_remains_14(self) -> None:
        self.assertEqual(len(self.exceptions), 14)

    def test_canonical_fixture_severity_counts_remain_stable(self) -> None:
        counts = Counter(exception.severity for exception in self.exceptions)

        self.assertEqual(counts["Critical"], 4)
        self.assertEqual(counts["Warning"], 10)
        self.assertEqual(counts["Info"], 0)

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
