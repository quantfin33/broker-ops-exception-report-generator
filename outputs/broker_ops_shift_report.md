# Broker Operations Shift Report

## Input files used

- Orders: `data/sample_order_events.csv`
- Market events: `data/sample_market_events.csv`

## Order activity summary

- Order rows: 20
- Market-event rows: 5
- Symbols monitored: 6
- Filled orders: 7
- Rejected orders: 4
- Failed orders: 2
- Pending/open orders: 5

## Exception summary

- Total exceptions: 14
- received_not_transmitted: 1
- transmitted_no_final_status: 1
- rejected_without_reason: 1
- bridge_failed_or_disconnected: 2
- high_latency: 7
- pending_follow_up: 2

## Severity breakdown

- Critical: 4
- Warning: 10
- Info: 0

## Items requiring review

- Warning `high_latency` on `XAUUSD` event `evt_0002`: Latency 2040 ms is above 2000 ms. Action: Review execution latency against operational thresholds and check whether the symbol, route, or bridge showed delays.
- Critical `received_not_transmitted` on `XAUUSD` event `evt_0003`: Order was received by the platform but has no transmission timestamp. Action: Review platform queue/routing state and confirm whether the order should be transmitted, cancelled, or escalated.
- Critical `transmitted_no_final_status` on `BTCUSD` event `evt_0004`: Order was transmitted but has no final status timestamp. Action: Check downstream execution/bridge response and follow up until a final fill, reject, cancel, fail, or expiry status is recorded.
- Warning `pending_follow_up` on `BTCUSD` event `evt_0004`: Order state is unresolved and has no final status timestamp. Action: Carry forward to shift handover and confirm the order reaches a final status or is otherwise resolved.
- Warning `rejected_without_reason` on `XAUUSD` event `evt_0006`: Rejected order is missing a reject reason. Action: Investigate missing rejection reason and update the operational record with a clear rejection explanation.
- Critical `bridge_failed_or_disconnected` on `USOIL` event `evt_0007`: Bridge status is failed. Action: Escalate bridge or liquidity-provider connectivity issue to platform/risk/technical support and monitor affected symbols.
- Warning `high_latency` on `USOIL` event `evt_0007`: Latency 3020 ms is above 2000 ms. Action: Review execution latency against operational thresholds and check whether the symbol, route, or bridge showed delays.
- Critical `bridge_failed_or_disconnected` on `BTCUSD` event `evt_0008`: Bridge status is disconnected. Action: Escalate bridge or liquidity-provider connectivity issue to platform/risk/technical support and monitor affected symbols.
- Warning `high_latency` on `BTCUSD` event `evt_0008`: Latency 4300 ms is above 2000 ms. Action: Review execution latency against operational thresholds and check whether the symbol, route, or bridge showed delays.
- Warning `high_latency` on `USDJPY` event `evt_0009`: Latency 3250 ms is above 2000 ms. Action: Review execution latency against operational thresholds and check whether the symbol, route, or bridge showed delays.
- Warning `pending_follow_up` on `XAUUSD` event `evt_0010`: Order state is unresolved and has no final status timestamp. Action: Carry forward to shift handover and confirm the order reaches a final status or is otherwise resolved.
- Warning `high_latency` on `XAUUSD` event `evt_0016`: Latency 2500 ms is above 2000 ms. Action: Review execution latency against operational thresholds and check whether the symbol, route, or bridge showed delays.
- Warning `high_latency` on `USOIL` event `evt_0017`: Latency 60000 ms is above 2000 ms. Action: Review execution latency against operational thresholds and check whether the symbol, route, or bridge showed delays.
- Warning `high_latency` on `EURUSD` event `evt_0018`: Latency 300000 ms is above 2000 ms. Action: Review execution latency against operational thresholds and check whether the symbol, route, or bridge showed delays.

## By-symbol summary

| Symbol | Asset class | Orders | Exceptions | Critical | Warning | Avg latency ms | P&L USD |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BTCUSD | crypto | 2 | 4 | 2 | 2 | 2150 | 0 |
| EURUSD | fx | 6 | 1 | 0 | 1 | 50288.333333 | 28.4 |
| GBPUSD | fx | 1 | 0 | 0 | 0 | 410 | 3.25 |
| USDJPY | fx | 1 | 1 | 0 | 1 | 3250 | 18.7 |
| USOIL | energy | 2 | 3 | 1 | 2 | 31510 | 0 |
| XAUUSD | metal | 8 | 5 | 1 | 4 | 873.75 | 63.4 |

## Shift handover notes

- Carry forward unresolved exception items: 4
- Critical exceptions requiring immediate review: 4
- Confirm pending/open orders reach a final status or are otherwise resolved.
- Review symbols with concentrated exceptions using the by-symbol summary.

## Limitations / non-claims

- Static sample data only.
- No real client/account data.
- No live broker connection.
- No MT4/MT5 admin access.
- No execution or trading bot.
