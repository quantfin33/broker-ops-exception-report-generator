"""Report writers for static broker operations outputs."""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from .exceptions import BrokerException, detect_exceptions
from .validation import ValidationResult, validate_inputs


ORDER_EXCEPTION_LOG_FILENAME = "order_exception_log.csv"
SHIFT_SUMMARY_FILENAME = "broker_ops_shift_summary.json"
SYMBOL_STATS_FILENAME = "by_symbol_trading_stats.csv"

SEVERITY_ORDER = ("Critical", "Warning", "Info")
EXCEPTION_TYPE_ORDER = (
    "received_not_transmitted",
    "transmitted_no_final_status",
    "rejected_without_reason",
    "bridge_failed_or_disconnected",
    "high_latency",
    "pending_follow_up",
)
UNRESOLVED_EXCEPTION_TYPES = (
    "received_not_transmitted",
    "transmitted_no_final_status",
    "pending_follow_up",
)
PENDING_OR_OPEN_STATUSES = {"received", "pending_new", "new", "transmitted", "partially_filled"}

ORDER_EXCEPTION_LOG_HEADERS = [
    "exception_type",
    "severity",
    "event_id",
    "client_order_id",
    "server_order_id",
    "symbol",
    "status",
    "bridge_status",
    "detail",
    "recommended_action",
]

SYMBOL_STATS_HEADERS = [
    "symbol",
    "asset_class",
    "total_orders",
    "filled_orders",
    "rejected_orders",
    "failed_orders",
    "pending_or_open_orders",
    "total_volume",
    "average_latency_ms",
    "max_latency_ms",
    "total_pnl_usd",
    "exception_count",
    "critical_exception_count",
    "warning_exception_count",
]


@dataclass(frozen=True)
class ExceptionLogResult:
    """Result from writing the Phase 4A exception log."""

    output_path: Path
    exception_count: int
    validation: ValidationResult


@dataclass(frozen=True)
class SymbolStatsResult:
    """Result from writing the Phase 4C by-symbol trading stats CSV."""

    output_path: Path
    symbol_count: int
    order_count: int
    exception_count: int
    validation: ValidationResult


@dataclass(frozen=True)
class ShiftSummaryResult:
    """Result from writing the Phase 4B shift summary JSON."""

    output_path: Path
    exception_count: int
    order_count: int
    market_event_count: int
    validation: ValidationResult


def write_order_exception_log(
    order_path: str | Path,
    market_events_path: str | Path,
    output_dir: str | Path,
) -> ExceptionLogResult:
    """Validate inputs and write only the Phase 4A order exception log CSV."""

    validation = validate_inputs(order_path, market_events_path)
    output_path = Path(output_dir) / ORDER_EXCEPTION_LOG_FILENAME
    if not validation.ok:
        return ExceptionLogResult(output_path=output_path, exception_count=0, validation=validation)

    exceptions = detect_exceptions(order_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _write_exception_log_csv(output_path, exceptions)
    return ExceptionLogResult(
        output_path=output_path,
        exception_count=len(exceptions),
        validation=validation,
    )


def write_by_symbol_trading_stats(
    order_path: str | Path,
    market_events_path: str | Path,
    output_dir: str | Path,
) -> SymbolStatsResult:
    """Validate inputs and write only the Phase 4C by-symbol stats CSV."""

    validation = validate_inputs(order_path, market_events_path)
    output_path = Path(output_dir) / SYMBOL_STATS_FILENAME
    if not validation.ok:
        return SymbolStatsResult(
            output_path=output_path,
            symbol_count=0,
            order_count=0,
            exception_count=0,
            validation=validation,
        )

    order_rows = _read_csv_rows(order_path)
    exceptions = detect_exceptions(order_path)
    stats_rows = _build_symbol_stats_rows(order_rows, exceptions)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SYMBOL_STATS_HEADERS)
        writer.writeheader()
        writer.writerows(stats_rows)

    return SymbolStatsResult(
        output_path=output_path,
        symbol_count=len(stats_rows),
        order_count=len(order_rows),
        exception_count=len(exceptions),
        validation=validation,
    )


def write_broker_ops_shift_summary(
    order_path: str | Path,
    market_events_path: str | Path,
    output_dir: str | Path,
) -> ShiftSummaryResult:
    """Validate inputs and write only the Phase 4B shift summary JSON."""

    validation = validate_inputs(order_path, market_events_path)
    output_path = Path(output_dir) / SHIFT_SUMMARY_FILENAME
    if not validation.ok:
        return ShiftSummaryResult(
            output_path=output_path,
            exception_count=0,
            order_count=0,
            market_event_count=0,
            validation=validation,
        )

    order_rows = _read_csv_rows(order_path)
    market_event_rows = _read_csv_rows(market_events_path)
    exceptions = detect_exceptions(order_path)
    summary = _build_shift_summary(
        order_path=order_path,
        market_events_path=market_events_path,
        output_dir=output_dir,
        output_path=output_path,
        validation=validation,
        order_rows=order_rows,
        market_event_rows=market_event_rows,
        exceptions=exceptions,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")

    return ShiftSummaryResult(
        output_path=output_path,
        exception_count=len(exceptions),
        order_count=len(order_rows),
        market_event_count=len(market_event_rows),
        validation=validation,
    )


def _write_exception_log_csv(output_path: Path, exceptions: list[BrokerException]) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ORDER_EXCEPTION_LOG_HEADERS)
        writer.writeheader()
        for exception in exceptions:
            writer.writerow(
                {
                    "exception_type": exception.exception_type,
                    "severity": exception.severity,
                    "event_id": exception.event_id,
                    "client_order_id": exception.client_order_id,
                    "server_order_id": exception.server_order_id,
                    "symbol": exception.symbol,
                    "status": exception.status,
                    "bridge_status": exception.bridge_status,
                    "detail": exception.detail,
                    "recommended_action": exception.recommended_action,
                }
            )


def _build_symbol_stats_rows(
    order_rows: list[dict[str, str]],
    exceptions: list[BrokerException],
) -> list[dict[str, str]]:
    rows_by_symbol: dict[str, list[dict[str, str]]] = {}
    for row in order_rows:
        symbol = _value(row, "symbol")
        rows_by_symbol.setdefault(symbol, []).append(row)

    exceptions_by_symbol: dict[str, list[BrokerException]] = {}
    for exception in exceptions:
        exceptions_by_symbol.setdefault(exception.symbol, []).append(exception)

    output_rows: list[dict[str, str]] = []
    for symbol in sorted(rows_by_symbol):
        symbol_rows = rows_by_symbol[symbol]
        symbol_exceptions = exceptions_by_symbol.get(symbol, [])
        severity_counts = Counter(exception.severity for exception in symbol_exceptions)
        latency_values = [_parse_number(_value(row, "latency_ms")) for row in symbol_rows]
        numeric_latencies = [value for value in latency_values if value is not None]

        output_rows.append(
            {
                "symbol": symbol,
                "asset_class": _first_nonblank(symbol_rows, "asset_class"),
                "total_orders": str(len(symbol_rows)),
                "filled_orders": str(_count_status(symbol_rows, "filled")),
                "rejected_orders": str(_count_status(symbol_rows, "rejected")),
                "failed_orders": str(_count_status(symbol_rows, "failed")),
                "pending_or_open_orders": str(_count_pending_or_open(symbol_rows)),
                "total_volume": _format_number(
                    sum(_parse_number(_value(row, "volume")) or 0.0 for row in symbol_rows)
                ),
                "average_latency_ms": _format_number(
                    sum(numeric_latencies) / len(numeric_latencies) if numeric_latencies else 0.0
                ),
                "max_latency_ms": _format_number(max(numeric_latencies) if numeric_latencies else 0.0),
                "total_pnl_usd": _format_number(
                    sum(_parse_number(_value(row, "pnl_usd")) or 0.0 for row in symbol_rows)
                ),
                "exception_count": str(len(symbol_exceptions)),
                "critical_exception_count": str(severity_counts.get("Critical", 0)),
                "warning_exception_count": str(severity_counts.get("Warning", 0)),
            }
        )
    return output_rows


def _build_shift_summary(
    *,
    order_path: str | Path,
    market_events_path: str | Path,
    output_dir: str | Path,
    output_path: Path,
    validation: ValidationResult,
    order_rows: list[dict[str, str]],
    market_event_rows: list[dict[str, str]],
    exceptions: list[BrokerException],
) -> dict[str, object]:
    severity_breakdown = _breakdown(
        (exception.severity for exception in exceptions),
        SEVERITY_ORDER,
    )
    exception_type_breakdown = _breakdown(
        (exception.exception_type for exception in exceptions),
        EXCEPTION_TYPE_ORDER,
    )
    unresolved_items = [
        {
            "event_id": exception.event_id,
            "exception_type": exception.exception_type,
            "severity": exception.severity,
            "symbol": exception.symbol,
            "status": exception.status,
            "detail": exception.detail,
            "recommended_action": exception.recommended_action,
        }
        for exception in exceptions
        if exception.exception_type in UNRESOLVED_EXCEPTION_TYPES
    ]

    return {
        "project_name": "Broker Operations Exception Report Generator",
        "generated_at_utc": "2026-05-09T00:00:00Z",
        "input_files": {
            "orders": str(order_path),
            "market_events": str(market_events_path),
        },
        "validation_summary": {
            "validation_passed": validation.ok,
            "validation_error_count": len(validation.issues),
            "duplicate_id_failures": _count_validation_issues(validation, "duplicate"),
            "missing_required_field_failures": _count_validation_issues(
                validation,
                "required field is blank",
            ),
            "note": (
                "Duplicate IDs and missing required fields are validation failures, "
                "not exception-log rows."
            ),
        },
        "order_summary": {
            "total_order_rows": len(order_rows),
            "total_market_event_rows": len(market_event_rows),
            "symbols_count": _distinct_count(order_rows, "symbol"),
            "routes_count": _distinct_count(order_rows, "route"),
            "liquidity_providers_count": _distinct_count(order_rows, "liquidity_provider"),
        },
        "exception_summary": {
            "total_exceptions": len(exceptions),
            "severity_breakdown": severity_breakdown,
            "exception_type_breakdown": exception_type_breakdown,
            "highest_severity_present": _highest_severity_present(severity_breakdown),
            "unresolved_exception_count": len(unresolved_items),
        },
        "severity_breakdown": severity_breakdown,
        "exception_type_breakdown": exception_type_breakdown,
        "unresolved_items": unresolved_items,
        "output_files": {
            "order_exception_log": str(Path(output_dir) / ORDER_EXCEPTION_LOG_FILENAME),
            "shift_summary": str(output_path),
        },
        "non_claims": [
            "Static broker operations reporting demo only.",
            "Does not perform live trading.",
            "Does not integrate with broker APIs.",
            "Does not integrate with MT4/MT5.",
            "Does not perform live monitoring.",
            "Does not prove broker administrator access.",
            "Not investment or trading advice.",
        ],
    }


def _read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _breakdown(values, expected_order: tuple[str, ...]) -> dict[str, int]:
    counts = Counter(values)
    return {key: counts.get(key, 0) for key in expected_order}


def _distinct_count(rows: list[dict[str, str]], field_name: str) -> int:
    values = {(row.get(field_name) or "").strip() for row in rows}
    values.discard("")
    return len(values)


def _highest_severity_present(severity_breakdown: dict[str, int]) -> str | None:
    for severity in SEVERITY_ORDER:
        if severity_breakdown[severity]:
            return severity
    return None


def _count_validation_issues(validation: ValidationResult, text: str) -> int:
    return sum(1 for issue in validation.issues if text in issue.message)


def _count_status(rows: list[dict[str, str]], status: str) -> int:
    return sum(1 for row in rows if _value(row, "status") == status)


def _count_pending_or_open(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if _value(row, "status") in PENDING_OR_OPEN_STATUSES)


def _first_nonblank(rows: list[dict[str, str]], field_name: str) -> str:
    for row in rows:
        value = _value(row, field_name)
        if value:
            return value
    return ""


def _parse_number(value: str) -> float | None:
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _format_number(value: float) -> str:
    return f"{value:.6f}".rstrip("0").rstrip(".")


def _value(row: dict[str, str], field_name: str) -> str:
    return (row.get(field_name) or "").strip()
