"""Structural validation for static broker operations CSV fixtures."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .schema import (
    ALLOWED_BRIDGE_STATUSES,
    ALLOWED_STATUSES,
    EXECUTED_PRICE_REQUIRED_STATUSES,
    FINAL_STATUS_REQUIRED_STATUSES,
    MARKET_EVENT_HEADERS,
    MARKET_EVENT_TIMESTAMP_FIELDS,
    ORDER_EVENT_HEADERS,
    ORDER_NUMERIC_FIELDS,
    ORDER_TIMESTAMP_FIELDS,
    PRE_TRANSMISSION_STATUSES,
    REQUIRED_MARKET_EVENT_FIELDS,
    REQUIRED_ORDER_CORE_FIELDS,
    SECRET_SCAN_PATTERNS,
    TRANSMISSION_REQUIRED_STATUSES,
)


@dataclass(frozen=True)
class ValidationIssue:
    """A single CSV validation error."""

    file: str
    message: str
    row_number: int | None = None
    column: str | None = None

    def format(self) -> str:
        location = self.file
        if self.row_number is not None:
            location += f":row {self.row_number}"
        if self.column:
            location += f":{self.column}"
        return f"{location} - {self.message}"


@dataclass
class ValidationResult:
    """Validation result with row counts and collected errors."""

    order_rows: int = 0
    market_event_rows: int = 0
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues


def validate_inputs(order_path: str | Path, market_events_path: str | Path) -> ValidationResult:
    """Validate static order-event and market-event CSV inputs."""

    result = ValidationResult()
    order_file = Path(order_path)
    market_file = Path(market_events_path)

    order_rows = _read_csv(order_file, "orders", result)
    market_rows = _read_csv(market_file, "market-events", result)

    if order_rows is not None:
        result.order_rows = len(order_rows)
        _validate_order_rows(order_file, order_rows, result)
        _validate_duplicate_order_ids(order_file, order_rows, result)
    if market_rows is not None:
        result.market_event_rows = len(market_rows)
        _validate_market_event_rows(market_file, market_rows, result)

    _scan_for_secret_patterns(order_file, result)
    _scan_for_secret_patterns(market_file, result)
    return result


def _read_csv(
    path: Path,
    label: str,
    result: ValidationResult,
) -> list[dict[str, str]] | None:
    if not path.is_file():
        result.issues.append(ValidationIssue(str(path), f"{label} CSV file does not exist"))
        return None

    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                result.issues.append(ValidationIssue(str(path), f"{label} CSV has no header row"))
                return None
            _validate_headers(path, reader.fieldnames, _expected_headers_for(label), result)
            return list(reader)
    except csv.Error as exc:
        result.issues.append(ValidationIssue(str(path), f"CSV parse error: {exc}"))
    except OSError as exc:
        result.issues.append(ValidationIssue(str(path), f"could not read file: {exc}"))
    return None


def _expected_headers_for(label: str) -> list[str]:
    if label == "orders":
        return ORDER_EVENT_HEADERS
    return MARKET_EVENT_HEADERS


def _validate_headers(
    path: Path,
    fieldnames: list[str],
    expected_headers: list[str],
    result: ValidationResult,
) -> None:
    for index, header in enumerate(fieldnames, start=1):
        if not header or not header.strip():
            result.issues.append(
                ValidationIssue(str(path), f"empty header name at position {index}")
            )

    missing = [header for header in expected_headers if header not in fieldnames]
    for header in missing:
        result.issues.append(ValidationIssue(str(path), "required header is missing", column=header))


def _validate_order_rows(
    path: Path,
    rows: list[dict[str, str]],
    result: ValidationResult,
) -> None:
    for row_number, row in _numbered_rows(rows):
        _validate_required_fields(path, row, row_number, REQUIRED_ORDER_CORE_FIELDS, result)
        _validate_allowed_value(path, row, row_number, "status", ALLOWED_STATUSES, result)
        _validate_allowed_value(
            path,
            row,
            row_number,
            "bridge_status",
            ALLOWED_BRIDGE_STATUSES,
            result,
        )
        _validate_timestamp_fields(path, row, row_number, ORDER_TIMESTAMP_FIELDS, result)
        _validate_numeric_fields(path, row, row_number, ORDER_NUMERIC_FIELDS, result)
        _validate_lifecycle_consistency(path, row, row_number, result)


def _validate_market_event_rows(
    path: Path,
    rows: list[dict[str, str]],
    result: ValidationResult,
) -> None:
    for row_number, row in _numbered_rows(rows):
        _validate_required_fields(path, row, row_number, REQUIRED_MARKET_EVENT_FIELDS, result)
        _validate_timestamp_fields(path, row, row_number, MARKET_EVENT_TIMESTAMP_FIELDS, result)


def _validate_duplicate_order_ids(
    path: Path,
    rows: list[dict[str, str]],
    result: ValidationResult,
) -> None:
    for field_name in ("client_order_id", "server_order_id"):
        seen: dict[str, list[tuple[int, str]]] = {}
        for row_number, row in _numbered_rows(rows):
            value = _value(row, field_name)
            if not value:
                continue
            seen.setdefault(value, []).append((row_number, _value(row, "event_id") or "<missing>"))

        for value, locations in seen.items():
            if len(locations) < 2:
                continue
            formatted_locations = ", ".join(
                f"row {row_number} ({event_id})" for row_number, event_id in locations
            )
            result.issues.append(
                ValidationIssue(
                    str(path),
                    f"duplicate {field_name} {value!r} appears in {formatted_locations}",
                    column=field_name,
                )
            )


def _numbered_rows(rows: Iterable[dict[str, str]]) -> Iterable[tuple[int, dict[str, str]]]:
    # CSV row 1 is the header, so data rows start on line 2.
    for row_number, row in enumerate(rows, start=2):
        yield row_number, row


def _validate_required_fields(
    path: Path,
    row: dict[str, str],
    row_number: int,
    fields: list[str],
    result: ValidationResult,
) -> None:
    for field_name in fields:
        if not _value(row, field_name):
            result.issues.append(
                ValidationIssue(
                    str(path),
                    "required field is blank",
                    row_number=row_number,
                    column=field_name,
                )
            )


def _validate_allowed_value(
    path: Path,
    row: dict[str, str],
    row_number: int,
    field_name: str,
    allowed_values: set[str],
    result: ValidationResult,
) -> None:
    value = _value(row, field_name)
    if value and value not in allowed_values:
        result.issues.append(
            ValidationIssue(
                str(path),
                f"invalid value {value!r}; allowed values are {', '.join(sorted(allowed_values))}",
                row_number=row_number,
                column=field_name,
            )
        )


def _validate_timestamp_fields(
    path: Path,
    row: dict[str, str],
    row_number: int,
    fields: list[str],
    result: ValidationResult,
) -> None:
    for field_name in fields:
        value = _value(row, field_name)
        if value and not _is_utc_timestamp(value):
            result.issues.append(
                ValidationIssue(
                    str(path),
                    "timestamp must be UTC ISO-style text ending in Z",
                    row_number=row_number,
                    column=field_name,
                )
            )


def _validate_numeric_fields(
    path: Path,
    row: dict[str, str],
    row_number: int,
    fields: list[str],
    result: ValidationResult,
) -> None:
    for field_name in fields:
        value = _value(row, field_name)
        if value:
            try:
                float(value)
            except ValueError:
                result.issues.append(
                    ValidationIssue(
                        str(path),
                        f"numeric field could not be parsed: {value!r}",
                        row_number=row_number,
                        column=field_name,
                    )
                )


def _validate_lifecycle_consistency(
    path: Path,
    row: dict[str, str],
    row_number: int,
    result: ValidationResult,
) -> None:
    status = _value(row, "status")
    received_time = _value(row, "order_received_time_utc")
    transmitted_time = _value(row, "order_transmitted_time_utc")
    final_time = _value(row, "final_status_time_utc")
    executed_price = _value(row, "executed_price")

    if status in PRE_TRANSMISSION_STATUSES | TRANSMISSION_REQUIRED_STATUSES and not received_time:
        _add_lifecycle_issue(
            path,
            row_number,
            "order_received_time_utc",
            f"status {status!r} requires order_received_time_utc",
            result,
        )
    if status in TRANSMISSION_REQUIRED_STATUSES and not transmitted_time:
        _add_lifecycle_issue(
            path,
            row_number,
            "order_transmitted_time_utc",
            f"status {status!r} requires order_transmitted_time_utc",
            result,
        )
    if status in FINAL_STATUS_REQUIRED_STATUSES and not final_time:
        _add_lifecycle_issue(
            path,
            row_number,
            "final_status_time_utc",
            f"status {status!r} requires final_status_time_utc",
            result,
        )
    if status in EXECUTED_PRICE_REQUIRED_STATUSES and not executed_price:
        _add_lifecycle_issue(
            path,
            row_number,
            "executed_price",
            f"status {status!r} requires executed_price",
            result,
        )

    parsed_received = _parse_utc_timestamp(received_time)
    parsed_transmitted = _parse_utc_timestamp(transmitted_time)
    parsed_final = _parse_utc_timestamp(final_time)

    if parsed_received and parsed_transmitted and parsed_transmitted < parsed_received:
        _add_lifecycle_issue(
            path,
            row_number,
            "order_transmitted_time_utc",
            "order_transmitted_time_utc cannot be earlier than order_received_time_utc",
            result,
        )
    if parsed_received and parsed_final and parsed_final < parsed_received:
        _add_lifecycle_issue(
            path,
            row_number,
            "final_status_time_utc",
            "final_status_time_utc cannot be earlier than order_received_time_utc",
            result,
        )
    if parsed_transmitted and parsed_final and parsed_final < parsed_transmitted:
        _add_lifecycle_issue(
            path,
            row_number,
            "final_status_time_utc",
            "final_status_time_utc cannot be earlier than order_transmitted_time_utc",
            result,
        )


def _add_lifecycle_issue(
    path: Path,
    row_number: int,
    field_name: str,
    message: str,
    result: ValidationResult,
) -> None:
    result.issues.append(
        ValidationIssue(
            str(path),
            message,
            row_number=row_number,
            column=field_name,
        )
    )


def _is_utc_timestamp(value: str) -> bool:
    return _parse_utc_timestamp(value) is not None


def _parse_utc_timestamp(value: str) -> datetime | None:
    if not value:
        return None
    if not value.endswith("Z"):
        return None
    normalized = value[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _scan_for_secret_patterns(path: Path, result: ValidationResult) -> None:
    if not path.is_file():
        return
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        result.issues.append(ValidationIssue(str(path), f"could not scan file: {exc}"))
        return

    for pattern in SECRET_SCAN_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            result.issues.append(
                ValidationIssue(str(path), f"possible secret/live credential pattern found: {pattern}")
            )


def _value(row: dict[str, str], field_name: str) -> str:
    return (row.get(field_name) or "").strip()
