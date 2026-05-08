"""Project constants for the Phase 1 CLI scaffold."""

from __future__ import annotations

PROJECT_NAME = "Broker Operations Exception Report Generator"
__version__ = "0.1.0"

DEFAULT_ORDER_EVENTS_PATH = "data/sample_order_events.csv"
DEFAULT_MARKET_EVENTS_PATH = "data/sample_market_events.csv"
DEFAULT_OUTPUT_DIR = "outputs"

LIVE_INTEGRATIONS_ALLOWED = False
NETWORK_DEPENDENCIES: tuple[str, ...] = ()

NO_LIVE_INTEGRATIONS_MESSAGE = (
    "Static demo boundary: no live broker, MT4/MT5, FIX, exchange, bridge, "
    "Binance, Telegram, TradingView, account, or credential dependency is used."
)
