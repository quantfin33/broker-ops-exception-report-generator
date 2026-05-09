# Broker Ops Static Data Schema

Last updated: 2026-05-08

## Purpose

This document defines the controlled static CSV fixtures for the Broker Operations Exception Report Generator.

The fixtures are synthetic and intentionally small. They exist to support later validation, exception-rule, reporting, and shift-handover tests. They are not broker exports, client records, platform logs, or live execution data.

## Files

- `data/sample_order_events.csv`: synthetic broker-style order/platform event rows.
- `data/sample_market_events.csv`: synthetic market-event awareness rows for later overlap checks.

## Timestamp Convention

All timestamps use UTC and ISO 8601-style text with a trailing `Z`, for example `2026-05-07T12:30:00Z`.

Some rows intentionally leave lifecycle timestamps blank so later validation and exception rules can detect incomplete order states.

## `sample_order_events.csv`

| Column | Expected type/format | Purpose |
| --- | --- | --- |
| `event_id` | string, unique fixture row id | Stable row identifier for tests and audit notes. |
| `client_order_id` | synthetic string | Client-side order id. Some rows intentionally duplicate this value. |
| `server_order_id` | synthetic string or blank | Server-side order id. Some rows intentionally duplicate or omit this value. |
| `timestamp_utc` | UTC timestamp text | Primary event timestamp. |
| `platform` | synthetic platform label | Demo source channel such as `demo_web`, `demo_mobile`, or `demo_desktop`. |
| `account_id_hash` | synthetic hash-like string | Fake account reference. No real account data is included. |
| `symbol` | instrument symbol or blank | Instrument under review. One row intentionally leaves this blank. |
| `asset_class` | string | Fixture asset class such as `fx`, `metal`, `crypto`, or `energy`. |
| `side` | `buy` or `sell` | Order side. |
| `order_type` | string | Demo order type such as `market` or `limit`. |
| `volume` | decimal number text | Synthetic order volume. |
| `requested_price` | decimal number text | Synthetic requested price. |
| `executed_price` | decimal number text or blank | Synthetic execution price where applicable. |
| `order_received_time_utc` | UTC timestamp text or blank | Time the broker/platform received the order. |
| `order_transmitted_time_utc` | UTC timestamp text or blank | Time the order was transmitted onward. |
| `final_status_time_utc` | UTC timestamp text or blank | Time the final status was observed. |
| `status` | allowed status string | Order lifecycle status. |
| `reject_reason` | string or blank | Rejection/failure/cancel/expiry reason where available. |
| `bridge_status` | allowed bridge status string | Synthetic route/bridge health status. |
| `route` | synthetic route label or blank | Fake route identifier. No broker server names are used. |
| `liquidity_provider` | synthetic provider label or blank | Fake liquidity-provider label. |
| `latency_ms` | integer number text | Synthetic lifecycle latency in milliseconds. |
| `slippage_points` | decimal number text or blank | Synthetic slippage amount where applicable. |
| `pnl_usd` | decimal number text | Synthetic sample P&L value. |

### Allowed `status` Values

- `received`
- `pending_new`
- `new`
- `transmitted`
- `partially_filled`
- `filled`
- `rejected`
- `failed`
- `cancelled`
- `expired`

### Allowed `bridge_status` Values

- `ok`
- `delayed`
- `failed`
- `disconnected`
- `not_applicable`

## Intentionally Imperfect Order Rows

These rows are deliberate fixture cases for later tests:

| Event id | Fixture purpose |
| --- | --- |
| `evt_0001` | Normal filled order. |
| `evt_0002` | Partially filled order and latency above 2,000 ms. |
| `evt_0003` | Received but not transmitted. |
| `evt_0004` | Transmitted but no final status. |
| `evt_0005` | Rejected with a clear reject reason. |
| `evt_0006` | Rejected without a reject reason. |
| `evt_0007` | Failed bridge status. |
| `evt_0008` | Disconnected bridge status. |
| `evt_0010` | Unresolved pending order. |
| `evt_0011` and `evt_0012` | Duplicate `client_order_id`. |
| `evt_0013` | Missing required field candidate: blank `symbol`. |
| `evt_0014` and `evt_0015` | Duplicate `server_order_id`. |
| `evt_0016` and `evt_0019` | Additional XAUUSD rejections for abnormal symbol activity candidates. |
| `evt_0001` through `evt_0006` | Market-event overlap candidates near the demo CPI event. |

## `sample_market_events.csv`

| Column | Expected type/format | Purpose |
| --- | --- | --- |
| `event_time_utc` | UTC timestamp text | Time of the synthetic market event. |
| `asset` | string | Asset or macro category. |
| `event_type` | string | Demo event category such as `macro_release` or `inventory_report`. |
| `headline` | string | Synthetic human-readable event headline. |
| `expected_impact` | string | Expected impact label such as `low`, `medium`, or `high`. |
| `related_symbols` | semicolon-separated string | Symbols that may be affected by the event. |

## Non-Claims

- Static sample data only.
- No real broker, client, server, platform, liquidity-provider, order, or account data.
- No credentials, secrets, private logs, browser sessions, app-support files, or `.env` data.
- No MT4/MT5 connection.
- No FIX venue connection.
- No broker bridge connection.
- No live execution, live monitoring, trading bot, or production risk-control behavior.
