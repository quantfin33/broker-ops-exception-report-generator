"""Schema constants for static broker operations CSV fixtures."""

from __future__ import annotations

ORDER_EVENT_HEADERS = [
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

REQUIRED_ORDER_CORE_FIELDS = [
    "event_id",
    "client_order_id",
    "timestamp_utc",
    "platform",
    "symbol",
    "status",
    "bridge_status",
]

REQUIRED_MARKET_EVENT_FIELDS = [
    "event_time_utc",
    "related_symbols",
]

ORDER_TIMESTAMP_FIELDS = [
    "timestamp_utc",
    "order_received_time_utc",
    "order_transmitted_time_utc",
    "final_status_time_utc",
]

MARKET_EVENT_TIMESTAMP_FIELDS = [
    "event_time_utc",
]

ORDER_NUMERIC_FIELDS = [
    "volume",
    "requested_price",
    "executed_price",
    "latency_ms",
    "slippage_points",
    "pnl_usd",
]

ALLOWED_STATUSES = {
    "received",
    "pending_new",
    "new",
    "transmitted",
    "partially_filled",
    "filled",
    "rejected",
    "failed",
    "cancelled",
    "expired",
}

ALLOWED_BRIDGE_STATUSES = {
    "ok",
    "delayed",
    "failed",
    "disconnected",
    "not_applicable",
}

SECRET_SCAN_PATTERNS = [
    r"api[_-]?key",
    r"secret",
    r"password",
    r"bearer\s+",
    r"token",
    r"\.env",
]
