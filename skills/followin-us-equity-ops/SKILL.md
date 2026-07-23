---
name: followin-us-equity-ops
description: Turn Followin MCP market data, news, research, Twitter/X activity, and public trading signals into an editorial operating workflow for US equities. Use for daily morning briefs, important-event previews, research-report heat maps and normalized analyst targets, Twitter hot-ticker monitoring, public trader or analyst strategy-signal summaries, watchlists, and broker-assisted live-trading workflows.
---

# Followin US Equity Operations

Use Followin MCP as the evidence layer and this skill as the operating layer. Produce a complete operating packet instead of forwarding raw MCP rows.

## Route the request

Choose one primary workflow. Read the matching section in [workflows.md](references/workflows.md) before calling tools.

| User intent | Workflow |
|---|---|
| 昨夜重要消息、早报、晨报、盘前简报 | `morning-brief` |
| 重要事件、财报日历、宏观预告、本周看点 | `event-radar` |
| 研报密集标的、目标价、机构分歧、研究笔记 | `research-radar` |
| 推特热门标的、讨论变化、社媒热度 | `social-pulse` |
| 美股交易员、分析师公开策略、喊单、仓位信号 | `strategy-signal` |
| 盯盘、提醒、订阅某标的公开喊单 | `signal-watchlist` |
| 下单、实盘交易、仓位调整、止损止盈 | `trade-desk` |

Combine workflows only when the requested deliverable genuinely needs them. For example, a morning brief may use a small social pulse, but it must not silently expand into full single-stock research.

## Run the operating loop

1. Set `as_of`, timezone, lookback window, asset scope, output locale, and channel. Default to the user's timezone, US equities, and the user's language.
2. Read [tool-routing.md](references/tool-routing.md). Call the smallest set of Followin tools that can answer the request.
3. Normalize entities, timestamps, duplicate posts, research-report roles, target prices, and source provenance before drawing conclusions.
4. Rank items by decision relevance, not raw row count. Prefer material, recent, multi-source events over noisy price moves.
5. Build the output using [output-contracts.md](references/output-contracts.md). Always separate publishable copy from internal evidence and editor notes.
6. Check `meta.warnings`, missing fields, source timestamps, and contradictory evidence. State data gaps instead of filling them from memory.
7. Return a refresh trigger: a time, event, price level, or new-source condition that would justify rerunning the workflow.

## Apply evidence rules

- Use `metrics` for every current price, market move, calendar value, fundamental datapoint, analyst rating, target, and structured research-report claim.
- Use `news` for event discovery, commentary, raw indexed research documents, and broad Twitter content discovery.
- Use `signal` for KOL calls, public trader positions, insider or congressional trades, and 13F holdings.
- Use `twitter` only for raw operations on a named account, a specific tweet, list, community, or trend endpoint.
- Use `subscription` for saved KOL-call watchlists and unread counts.
- Mark Followin-derived evidence as Followin MCP. Label any supplemental public source separately.
- Treat one post as one source even when it mentions several tickers. Deduplicate by original URL or tweet ID before counting authors or posts.
- Never turn a small or unknown sample into “market consensus.” Report the sample size and the observed direction.
- Keep observation, inference, and proposed action visibly distinct.

## Handle target prices

For standardized target-price statistics, use only ticker-subject research or analyst records in the same currency and listing. Deduplicate institutions by their latest observation, then run:

```bash
python3 scripts/normalize_price_targets.py --input targets.json
```

Do not convert currencies without an explicit FX source and timestamp. When a record count is unavailable, say so rather than estimating it from unrelated fields.

## Guard live trading

Read [trading-controls.md](references/trading-controls.md) for any trade-related request.

Followin MCP does not place broker orders. Use it to form and monitor a thesis. Use a separately connected broker or execution tool for orders.

Never claim that an order was placed, accepted, filled, canceled, or rejected without a broker response. Before any order-changing action, show the exact account, symbol, side, quantity or notional, order type, limit or stop, time in force, estimated exposure, and risk controls, then obtain explicit order-level confirmation. After submission, fetch order status and positions and return the broker IDs.

If no purpose-built broker tool is available, do not search browser tabs or attempt website trading. Do not stop at a generic refusal. Use Followin to complete the timestamped research and event-risk checks, copy only user-specified order fields, mark every other mutable field as `REQUIRED`, and return `INCOMPLETE / NOT_SUBMITTED`. Technical analysis may inform the research summary but must never auto-populate order type, entry, limit, stop, target, time in force, session, or risk budget.
