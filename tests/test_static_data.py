from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORDER_EVENTS = ROOT / "data" / "sample_order_events.csv"
MARKET_EVENTS = ROOT / "data" / "sample_market_events.csv"

ORDER_HEADERS = [
    "event_id",
    "client_order_id",
    "server_order_id",
    "timestamp_utc",
    "platform",
    "account_id_hash",
    "symbol",
    "asset_class",
    "side",
    "order_type",
    "volume",
    "requested_price",
    "executed_price",
    "order_received_time_utc",
    "order_transmitted_time_utc",
    "final_status_time_utc",
    "status",
    "reject_reason",
    "bridge_status",
    "route",
    "liquidity_provider",
    "latency_ms",
    "slippage_points",
    "pnl_usd",
]

MARKET_EVENT_HEADERS = [
    "event_time_utc",
    "asset",
    "event_type",
    "headline",
    "expected_impact",
    "related_symbols",
]

REQUIRED_EVENT_IDS = {
    "evt_0001",
    "evt_0002",
    "evt_0003",
    "evt_0004",
    "evt_0005",
    "evt_0006",
    "evt_0007",
    "evt_0008",
    "evt_0010",
    "evt_0011",
    "evt_0012",
    "evt_0013",
    "evt_0014",
    "evt_0015",
    "evt_0016",
    "evt_0019",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class StaticDataFixtureTests(unittest.TestCase):
    def test_csv_files_exist(self) -> None:
        self.assertTrue(ORDER_EVENTS.is_file())
        self.assertTrue(MARKET_EVENTS.is_file())

    def test_expected_headers_are_present(self) -> None:
        with ORDER_EVENTS.open(newline="", encoding="utf-8") as handle:
            self.assertEqual(next(csv.reader(handle)), ORDER_HEADERS)
        with MARKET_EVENTS.open(newline="", encoding="utf-8") as handle:
            self.assertEqual(next(csv.reader(handle)), MARKET_EVENT_HEADERS)

    def test_expected_sample_rows_are_present(self) -> None:
        rows = read_csv(ORDER_EVENTS)
        event_ids = {row["event_id"] for row in rows}

        self.assertTrue(REQUIRED_EVENT_IDS.issubset(event_ids))
        self.assertGreaterEqual(sum(row["symbol"] == "XAUUSD" for row in rows), 6)
        self.assertTrue(any(row["bridge_status"] == "failed" for row in rows))
        self.assertTrue(any(row["bridge_status"] == "disconnected" for row in rows))
        self.assertTrue(any(int(row["latency_ms"] or "0") > 2000 for row in rows))

    def test_market_event_rows_are_present(self) -> None:
        rows = read_csv(MARKET_EVENTS)
        self.assertGreaterEqual(len(rows), 3)
        self.assertTrue(any("XAUUSD" in row["related_symbols"] for row in rows))
        self.assertTrue(any(row["expected_impact"] == "high" for row in rows))

    def test_no_obvious_secrets_or_private_account_values(self) -> None:
        combined_text = ORDER_EVENTS.read_text(encoding="utf-8") + MARKET_EVENTS.read_text(
            encoding="utf-8"
        )
        forbidden_patterns = [
            r"(?i)api[_-]?key",
            r"(?i)secret",
            r"(?i)password",
            r"(?i)bearer\s+",
            r"(?i)token",
            r"(?i)\.env",
            r"\b\d{8,}\b",
        ]

        for pattern in forbidden_patterns:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, combined_text))

    def test_no_network_or_live_dependency_in_fixture_tests(self) -> None:
        import broker_ops_report.config as config

        self.assertFalse(config.LIVE_INTEGRATIONS_ALLOWED)
        self.assertEqual(config.NETWORK_DEPENDENCIES, ())


if __name__ == "__main__":
    unittest.main()
