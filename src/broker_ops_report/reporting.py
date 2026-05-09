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


@dataclass(frozen=True)
class ExceptionLogResult:
    """Result from writing the Phase 4A exception log."""

    output_path: Path
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
