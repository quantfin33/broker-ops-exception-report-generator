"""Broker exception type detection for schema-valid static order rows."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


HIGH_LATENCY_THRESHOLD_MS = 2000

SEVERITY_BY_EXCEPTION_TYPE = {
    "bridge_failed_or_disconnected": "Critical",
    "transmitted_no_final_status": "Critical",
    "received_not_transmitted": "Critical",
    "rejected_without_reason": "Warning",
    "high_latency": "Warning",
    "pending_follow_up": "Warning",
}

DEFAULT_SEVERITY = "Info"

RECOMMENDED_ACTION_BY_EXCEPTION_TYPE = {
    "received_not_transmitted": (
        "Review platform queue/routing state and confirm whether the order should be "
        "transmitted, cancelled, or escalated."
    ),
    "transmitted_no_final_status": (
        "Check downstream execution/bridge response and follow up until a final fill, "
        "reject, cancel, fail, or expiry status is recorded."
    ),
    "rejected_without_reason": (
        "Investigate missing rejection reason and update the operational record with a "
        "clear rejection explanation."
    ),
    "bridge_failed_or_disconnected": (
        "Escalate bridge or liquidity-provider connectivity issue to "
        "platform/risk/technical support and monitor affected symbols."
    ),
    "high_latency": (
        "Review execution latency against operational thresholds and check whether the "
        "symbol, route, or bridge showed delays."
    ),
    "pending_follow_up": (
        "Carry forward to shift handover and confirm the order reaches a final status "
        "or is otherwise resolved."
    ),
}


@dataclass(frozen=True)
class BrokerException:
    """A detected broker operations exception type with deterministic triage metadata."""

    exception_type: str
    severity: str
    recommended_action: str
    event_id: str
    client_order_id: str
    server_order_id: str
    symbol: str
    status: str
    bridge_status: str
    detail: str


def detect_exceptions(order_path: str | Path) -> list[BrokerException]:
    """Detect broker exception types from a schema-valid static order CSV."""

    with Path(order_path).open(newline="", encoding="utf-8") as handle:
        return detect_exceptions_from_rows(csv.DictReader(handle))


def detect_exceptions_from_rows(rows: Iterable[dict[str, str]]) -> list[BrokerException]:
    """Detect broker exception types from order-event dictionaries."""

    exceptions: list[BrokerException] = []
    for row in rows:
        exceptions.extend(_detect_row_exceptions(row))
    return exceptions


def _detect_row_exceptions(row: dict[str, str]) -> list[BrokerException]:
    detected: list[BrokerException] = []
    status = _value(row, "status")
    bridge_status = _value(row, "bridge_status")
    received_time = _value(row, "order_received_time_utc")
    transmitted_time = _value(row, "order_transmitted_time_utc")
    final_time = _value(row, "final_status_time_utc")
    reject_reason = _value(row, "reject_reason")
    latency_ms = _parse_number(_value(row, "latency_ms"))

    if status in {"received", "pending_new"} and received_time and not transmitted_time:
        detected.append(
            _make_exception(
                row,
                "received_not_transmitted",
                "Order was received by the platform but has no transmission timestamp.",
            )
        )

    if status in {"transmitted", "new"} and transmitted_time and not final_time:
        detected.append(
            _make_exception(
                row,
                "transmitted_no_final_status",
                "Order was transmitted but has no final status timestamp.",
            )
        )

    if status == "rejected" and not reject_reason:
        detected.append(
            _make_exception(
                row,
                "rejected_without_reason",
                "Rejected order is missing a reject reason.",
            )
        )

    if bridge_status in {"failed", "disconnected"}:
        detected.append(
            _make_exception(
                row,
                "bridge_failed_or_disconnected",
                f"Bridge status is {bridge_status}.",
            )
        )

    if latency_ms is not None and latency_ms > HIGH_LATENCY_THRESHOLD_MS:
        detected.append(
            _make_exception(
                row,
                "high_latency",
                f"Latency {latency_ms:g} ms is above {HIGH_LATENCY_THRESHOLD_MS} ms.",
            )
        )

    if status in {"pending_new", "transmitted", "new"} and not final_time:
        detected.append(
            _make_exception(
                row,
                "pending_follow_up",
                "Order state is unresolved and has no final status timestamp.",
            )
        )

    return detected


def _make_exception(row: dict[str, str], exception_type: str, detail: str) -> BrokerException:
    return BrokerException(
        exception_type=exception_type,
        severity=classify_severity(exception_type),
        recommended_action=recommend_action(exception_type),
        event_id=_value(row, "event_id"),
        client_order_id=_value(row, "client_order_id"),
        server_order_id=_value(row, "server_order_id"),
        symbol=_value(row, "symbol"),
        status=_value(row, "status"),
        bridge_status=_value(row, "bridge_status"),
        detail=detail,
    )


def classify_severity(exception_type: str) -> str:
    """Return deterministic severity for an exception type."""

    return SEVERITY_BY_EXCEPTION_TYPE.get(exception_type, DEFAULT_SEVERITY)


def recommend_action(exception_type: str) -> str:
    """Return deterministic recommended action for a known exception type."""

    try:
        return RECOMMENDED_ACTION_BY_EXCEPTION_TYPE[exception_type]
    except KeyError as exc:
        raise ValueError(f"unknown exception type for recommended action: {exception_type}") from exc


def _parse_number(value: str) -> float | None:
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _value(row: dict[str, str], field_name: str) -> str:
    return (row.get(field_name) or "").strip()
