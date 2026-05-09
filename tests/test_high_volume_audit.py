from __future__ import annotations

import csv
import json
import os
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from broker_ops_report.config import LIVE_INTEGRATIONS_ALLOWED, NETWORK_DEPENDENCIES
from broker_ops_report.exceptions import detect_exceptions
from broker_ops_report.reporting import (
    SHIFT_REPORT_FILENAME,
    SHIFT_SUMMARY_FILENAME,
    SYMBOL_STATS_FILENAME,
    write_broker_ops_shift_report,
    write_broker_ops_shift_summary,
    write_by_symbol_trading_stats,
    write_order_exception_log,
)
from broker_ops_report.schema import MARKET_EVENT_HEADERS, ORDER_EVENT_HEADERS
from broker_ops_report.validation import validate_inputs


class HighVolumeSyntheticAuditTests(unittest.TestCase):
    def test_pipeline_audits_hundreds_of_synthetic_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            order_path = tmp_path / "synthetic_orders.csv"
            market_path = tmp_path / "synthetic_market_events.csv"
            output_dir = tmp_path / "outputs"

            _write_csv(order_path, ORDER_EVENT_HEADERS, _build_order_rows(batch_count=100))
            _write_csv(market_path, MARKET_EVENT_HEADERS, _build_market_event_rows())

            validation = validate_inputs(order_path, market_path)
            self.assertTrue(validation.ok, [issue.format() for issue in validation.issues])
            self.assertEqual(validation.order_rows, 600)
            self.assertEqual(validation.market_event_rows, 2)

            exceptions = detect_exceptions(order_path)
            severity_counts = Counter(exception.severity for exception in exceptions)
            self.assertEqual(len(exceptions), 700)
            self.assertEqual(severity_counts["Critical"], 300)
            self.assertEqual(severity_counts["Warning"], 400)
            self.assertEqual(severity_counts["Info"], 0)

            exception_log = write_order_exception_log(order_path, market_path, output_dir)
            shift_summary = write_broker_ops_shift_summary(order_path, market_path, output_dir)
            symbol_stats = write_by_symbol_trading_stats(order_path, market_path, output_dir)
            shift_report = write_broker_ops_shift_report(order_path, market_path, output_dir)

            self.assertTrue(exception_log.validation.ok)
            self.assertTrue(shift_summary.validation.ok)
            self.assertTrue(symbol_stats.validation.ok)
            self.assertTrue(shift_report.validation.ok)
            self.assertEqual(exception_log.exception_count, 700)
            self.assertEqual(shift_summary.exception_count, 700)
            self.assertEqual(symbol_stats.order_count, 600)
            self.assertEqual(symbol_stats.exception_count, 700)
            self.assertEqual(shift_report.exception_count, 700)

            with exception_log.output_path.open(newline="", encoding="utf-8") as handle:
                exception_rows = list(csv.DictReader(handle))
            self.assertEqual(len(exception_rows), 700)

            summary = json.loads((output_dir / SHIFT_SUMMARY_FILENAME).read_text(encoding="utf-8"))
            self.assertEqual(summary["exception_summary"]["total_exceptions"], 700)
            self.assertEqual(summary["severity_breakdown"], {"Critical": 300, "Warning": 400, "Info": 0})

            with (output_dir / SYMBOL_STATS_FILENAME).open(newline="", encoding="utf-8") as handle:
                symbol_rows = list(csv.DictReader(handle))
            self.assertEqual(sum(int(row["total_orders"]) for row in symbol_rows), 600)
            self.assertEqual(sum(int(row["exception_count"]) for row in symbol_rows), 700)
            self.assertTrue((output_dir / SHIFT_REPORT_FILENAME).is_file())
            self.assertEqual(list(output_dir.glob("*.xlsx")), [])
            self.assertEqual(list(output_dir.glob("*.html")), [])

            self.assertFalse(LIVE_INTEGRATIONS_ALLOWED)
            self.assertEqual(NETWORK_DEPENDENCIES, ())

    def test_streaming_batches_audit_flowing_synthetic_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            market_path = tmp_path / "synthetic_market_events.csv"
            cumulative_order_path = tmp_path / "cumulative_stream_orders.csv"
            _write_csv(market_path, MARKET_EVENT_HEADERS, _build_market_event_rows())

            cumulative_rows: list[dict[str, str]] = []
            cumulative_severity_counts: Counter[str] = Counter()
            cumulative_exception_count = 0

            for batch_index in range(10):
                batch_rows = _build_streaming_batch_rows(batch_index)
                cumulative_rows.extend(batch_rows)
                batch_order_path = tmp_path / f"stream_batch_{batch_index:02d}.csv"
                batch_output_dir = tmp_path / "stream_outputs" / f"batch_{batch_index:02d}"
                _write_csv(batch_order_path, ORDER_EVENT_HEADERS, batch_rows)

                validation = validate_inputs(batch_order_path, market_path)
                self.assertTrue(validation.ok, [issue.format() for issue in validation.issues])
                self.assertEqual(validation.order_rows, 100)

                batch_exceptions = detect_exceptions(batch_order_path)
                batch_severity_counts = Counter(exception.severity for exception in batch_exceptions)
                self.assertEqual(len(batch_exceptions), 110)
                self.assertEqual(batch_severity_counts["Critical"], 45)
                self.assertEqual(batch_severity_counts["Warning"], 65)
                self.assertEqual(batch_severity_counts["Info"], 0)
                cumulative_exception_count += len(batch_exceptions)
                cumulative_severity_counts.update(batch_severity_counts)

                exception_log = write_order_exception_log(batch_order_path, market_path, batch_output_dir)
                shift_summary = write_broker_ops_shift_summary(batch_order_path, market_path, batch_output_dir)
                symbol_stats = write_by_symbol_trading_stats(batch_order_path, market_path, batch_output_dir)
                shift_report = write_broker_ops_shift_report(batch_order_path, market_path, batch_output_dir)

                self.assertEqual(exception_log.exception_count, 110)
                self.assertEqual(shift_summary.exception_count, 110)
                self.assertEqual(symbol_stats.order_count, 100)
                self.assertEqual(symbol_stats.exception_count, 110)
                self.assertEqual(shift_report.exception_count, 110)

                with exception_log.output_path.open(newline="", encoding="utf-8") as handle:
                    exception_rows = list(csv.DictReader(handle))
                self.assertEqual(len(exception_rows), 110)

                summary = json.loads((batch_output_dir / SHIFT_SUMMARY_FILENAME).read_text(encoding="utf-8"))
                self.assertEqual(summary["exception_summary"]["total_exceptions"], 110)
                self.assertEqual(summary["severity_breakdown"], {"Critical": 45, "Warning": 65, "Info": 0})

                with (batch_output_dir / SYMBOL_STATS_FILENAME).open(newline="", encoding="utf-8") as handle:
                    symbol_rows = list(csv.DictReader(handle))
                self.assertEqual(sum(int(row["total_orders"]) for row in symbol_rows), 100)
                self.assertEqual(sum(int(row["exception_count"]) for row in symbol_rows), 110)
                self.assertTrue((batch_output_dir / SHIFT_REPORT_FILENAME).is_file())
                self.assertEqual(list(batch_output_dir.glob("*.xlsx")), [])
                self.assertEqual(list(batch_output_dir.glob("*.html")), [])

            _write_csv(cumulative_order_path, ORDER_EVENT_HEADERS, cumulative_rows)
            cumulative_validation = validate_inputs(cumulative_order_path, market_path)
            self.assertTrue(cumulative_validation.ok, [issue.format() for issue in cumulative_validation.issues])
            self.assertEqual(cumulative_validation.order_rows, 1000)

            cumulative_exceptions = detect_exceptions(cumulative_order_path)
            self.assertEqual(len(cumulative_rows), 1000)
            self.assertEqual(cumulative_exception_count, 1100)
            self.assertEqual(len(cumulative_exceptions), 1100)
            self.assertEqual(cumulative_severity_counts["Critical"], 450)
            self.assertEqual(cumulative_severity_counts["Warning"], 650)
            self.assertEqual(cumulative_severity_counts["Info"], 0)
            self.assertFalse(LIVE_INTEGRATIONS_ALLOWED)
            self.assertEqual(NETWORK_DEPENDENCIES, ())


def _write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def _build_market_event_rows() -> list[dict[str, str]]:
    return [
        {
            "event_time_utc": "2026-05-07T12:30:00Z",
            "asset": "USD",
            "event_type": "macro_release",
            "headline": "Synthetic macro release monitoring window",
            "expected_impact": "high",
            "related_symbols": "EURUSD;XAUUSD;USDJPY",
        },
        {
            "event_time_utc": "2026-05-07T15:00:00Z",
            "asset": "crypto",
            "event_type": "market_stress",
            "headline": "Synthetic crypto volatility monitoring window",
            "expected_impact": "medium",
            "related_symbols": "BTCUSD",
        },
    ]


def _build_order_rows(batch_count: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for batch in range(batch_count):
        base = batch * 6
        rows.extend(
            [
                _order_row(base + 1, "EURUSD", "fx", "filled", "ok", "120", executed=True, final=True),
                _order_row(
                    base + 2,
                    "XAUUSD",
                    "metal",
                    "received",
                    "not_applicable",
                    "0",
                    transmitted=False,
                    final=False,
                ),
                _order_row(
                    base + 3,
                    "BTCUSD",
                    "crypto",
                    "transmitted",
                    "delayed",
                    "500",
                    final=False,
                ),
                _order_row(
                    base + 4,
                    "XAUUSD",
                    "metal",
                    "rejected",
                    "ok",
                    "320",
                    executed=False,
                    final=True,
                    reject_reason="",
                ),
                _order_row(
                    base + 5,
                    "USOIL",
                    "energy",
                    "failed",
                    "failed",
                    "3500",
                    executed=False,
                    final=True,
                    reject_reason="downstream timeout",
                ),
                _order_row(base + 6, "USDJPY", "fx", "filled", "ok", "4500", executed=True, final=True),
            ]
        )
    return rows


def _build_streaming_batch_rows(batch_index: int) -> list[dict[str, str]]:
    start = batch_index * 100
    rows: list[dict[str, str]] = []
    rows.extend(
        _order_row(start + index, "EURUSD", "fx", "filled", "ok", "120", executed=True, final=True)
        for index in range(1, 21)
    )
    rows.extend(
        _order_row(
            start + index,
            "XAUUSD",
            "metal",
            "received",
            "not_applicable",
            "0",
            transmitted=False,
            final=False,
        )
        for index in range(21, 36)
    )
    rows.extend(
        _order_row(
            start + index,
            "BTCUSD",
            "crypto",
            "transmitted",
            "delayed",
            "500",
            final=False,
        )
        for index in range(36, 51)
    )
    rows.extend(
        _order_row(
            start + index,
            "XAUUSD",
            "metal",
            "rejected",
            "ok",
            "320",
            executed=False,
            final=True,
            reject_reason="",
        )
        for index in range(51, 66)
    )
    rows.extend(
        _order_row(
            start + index,
            "USOIL",
            "energy",
            "failed",
            "failed",
            "3500",
            executed=False,
            final=True,
            reject_reason="downstream timeout",
        )
        for index in range(66, 81)
    )
    rows.extend(
        _order_row(start + index, "USDJPY", "fx", "filled", "ok", "4500", executed=True, final=True)
        for index in range(81, 101)
    )
    return rows


def _order_row(
    sequence: int,
    symbol: str,
    asset_class: str,
    status: str,
    bridge_status: str,
    latency_ms: str,
    *,
    transmitted: bool = True,
    final: bool = True,
    executed: bool = False,
    reject_reason: str = "",
) -> dict[str, str]:
    timestamp = f"2026-05-07T12:{sequence % 60:02d}:00Z"
    received_time = timestamp
    transmitted_time = f"2026-05-07T12:{sequence % 60:02d}:01Z" if transmitted else ""
    final_time = f"2026-05-07T12:{sequence % 60:02d}:02Z" if final else ""
    executed_price = _price_for(symbol) if executed else ""
    server_order_id = f"sv_hv_{sequence:05d}" if transmitted else ""

    return {
        "event_id": f"evt_hv_{sequence:05d}",
        "client_order_id": f"cl_hv_{sequence:05d}",
        "server_order_id": server_order_id,
        "timestamp_utc": timestamp,
        "platform": "demo_platform",
        "account_id_hash": f"acct_demo_{sequence % 17:02d}",
        "symbol": symbol,
        "asset_class": asset_class,
        "side": "buy" if sequence % 2 else "sell",
        "order_type": "market",
        "volume": "1.0",
        "requested_price": _price_for(symbol),
        "executed_price": executed_price,
        "order_received_time_utc": received_time,
        "order_transmitted_time_utc": transmitted_time,
        "final_status_time_utc": final_time,
        "status": status,
        "reject_reason": reject_reason,
        "bridge_status": bridge_status,
        "route": "demo_route",
        "liquidity_provider": "demo_lp",
        "latency_ms": latency_ms,
        "slippage_points": "0.1" if executed else "",
        "pnl_usd": "1.25" if executed else "0",
    }


def _price_for(symbol: str) -> str:
    prices = {
        "EURUSD": "1.0850",
        "XAUUSD": "2350.00",
        "BTCUSD": "64000.00",
        "USOIL": "78.50",
        "USDJPY": "155.25",
    }
    return prices[symbol]


if __name__ == "__main__":
    unittest.main()
