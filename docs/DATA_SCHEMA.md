# Broker Ops Static Data Schema

Last updated: 2026-05-09

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
| `client_order_id` | synthetic string | Client-side order id. Duplicate examples are covered by temporary validation test fixtures, not the primary sample CSV. |
| `server_order_id` | synthetic string or blank | Server-side order id. Blank values are allowed for pre-transmission rows. Duplicate examples are covered by temporary validation test fixtures. |
| `timestamp_utc` | UTC timestamp text | Primary event timestamp. |
| `platform` | synthetic platform label | Demo source channel such as `demo_web`, `demo_mobile`, or `demo_desktop`. |
| `account_id_hash` | synthetic hash-like string | Fake account reference. No real account data is included. |
| `symbol` | instrument symbol | Instrument under review. Blank symbols are covered by temporary validation test fixtures, not the primary sample CSV. |
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

## Lifecycle Consistency Notes

The primary order-events CSV is expected to pass structural lifecycle validation.

- `received` and `pending_new` are pre-transmission states.
- `transmitted`, `new`, `partially_filled`, `filled`, `rejected`, `failed`, `cancelled`, and `expired` require `order_received_time_utc` and `order_transmitted_time_utc`.
- `partially_filled`, `filled`, `rejected`, `failed`, `cancelled`, and `expired` require `final_status_time_utc`.
- `partially_filled` and `filled` require `executed_price`.
- `rejected`, `cancelled`, and `expired` may have a blank `executed_price`.
- `order_transmitted_time_utc` must not be earlier than `order_received_time_utc`.
- `final_status_time_utc` must not be earlier than `order_received_time_utc` or `order_transmitted_time_utc`.

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
| `evt_0011` and `evt_0012` | Structurally valid XAUUSD rows retained after duplicate client-order coverage moved to temporary validation test fixtures. |
| `evt_0013` | Structurally valid EURUSD row retained after missing-field coverage moved to temporary validation test fixtures. |
| `evt_0014` and `evt_0015` | Structurally valid EURUSD rows retained after duplicate server-order coverage moved to temporary validation test fixtures. |
| `evt_0016` and `evt_0019` | Additional XAUUSD rejections for abnormal symbol activity candidates. |
| `evt_0001` through `evt_0006` | Market-event overlap candidates near the demo CPI event. |

## Phase 3C Exception Type Definitions

Phase 3C detects broker exception types from schema-valid static order rows only. Phase 3D adds deterministic severity classification for those same exception types. Phase 3E adds deterministic recommended actions. The project still does not aggregate by symbol, match market events, or generate report files.

| Exception type | Severity | Recommended action | Deterministic rule |
| --- | --- | --- | --- |
| `received_not_transmitted` | `Critical` | Review platform queue/routing state and confirm whether the order should be transmitted, cancelled, or escalated. | `status` is `received` or `pending_new`, `order_received_time_utc` is present, and `order_transmitted_time_utc` is blank. |
| `transmitted_no_final_status` | `Critical` | Check downstream execution/bridge response and follow up until a final fill, reject, cancel, fail, or expiry status is recorded. | `status` is `transmitted` or `new`, `order_transmitted_time_utc` is present, and `final_status_time_utc` is blank. |
| `bridge_failed_or_disconnected` | `Critical` | Escalate bridge or liquidity-provider connectivity issue to platform/risk/technical support and monitor affected symbols. | `bridge_status` is `failed` or `disconnected`. |
| `rejected_without_reason` | `Warning` | Investigate missing rejection reason and update the operational record with a clear rejection explanation. | `status` is `rejected` and `reject_reason` is blank. |
| `high_latency` | `Warning` | Review execution latency against operational thresholds and check whether the symbol, route, or bridge showed delays. | `latency_ms` is numeric and greater than `2000`. |
| `pending_follow_up` | `Warning` | Carry forward to shift handover and confirm the order reaches a final status or is otherwise resolved. | `status` is `pending_new`, `transmitted`, or `new`, and `final_status_time_utc` is blank. |

## `sample_market_events.csv`

| Column | Expected type/format | Purpose |
| --- | --- | --- |
| `event_time_utc` | UTC timestamp text | Time of the synthetic market event. |
| `asset` | string | Asset or macro category. |
| `event_type` | string | Demo event category such as `macro_release` or `inventory_report`. |
| `headline` | string | Synthetic human-readable event headline. |
| `expected_impact` | string | Expected impact label such as `low`, `medium`, or `high`. |
| `related_symbols` | semicolon-separated string | Symbols that may be affected by the event. |

## Phase 4A `order_exception_log.csv`

Phase 4A writes `outputs/order_exception_log.csv` only. It is generated from validated static inputs and existing internal exception records. It does not generate a JSON summary, by-symbol statistics, Markdown report, Excel workbook, market-event overlap, duplicate-ID exception reporting, or missing-field exception reporting.

Sequencing note: Phase 3C through Phase 3E define the core exception object pipeline. Duplicate IDs and missing required fields remain validation failures, not exception-log rows. Abnormal symbol activity is deferred to later by-symbol statistics work, and market-event overlap is deferred to later enrichment. Phase 4A can depend on the existing exception objects, but its output remains local work-in-progress until the Phase 3F tracker cleanup is locked.

| Column | Source |
| --- | --- |
| `exception_type` | Internal broker exception type. |
| `severity` | Deterministic severity classification. |
| `event_id` | Source order-event row id. |
| `client_order_id` | Source synthetic client order id. |
| `server_order_id` | Source synthetic server order id, if present. |
| `symbol` | Source symbol. |
| `status` | Source lifecycle status. |
| `bridge_status` | Source bridge status. |
| `detail` | Deterministic exception detail text. |
| `recommended_action` | Deterministic operations follow-up text. |

## Non-Claims

- Static sample data only.
- No real broker, client, server, platform, liquidity-provider, order, or account data.
- No credentials, secrets, private logs, browser sessions, app-support files, or `.env` data.
- No MT4/MT5 connection.
- No FIX venue connection.
- No broker bridge connection.
- No live execution, live monitoring, trading bot, or production risk-control behavior.
