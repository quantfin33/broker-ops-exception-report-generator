"""Report writers for static broker operations outputs."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .exceptions import BrokerException, detect_exceptions
from .validation import ValidationResult, validate_inputs


ORDER_EXCEPTION_LOG_FILENAME = "order_exception_log.csv"

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
