# Followin MCP Tool Routing

Use the current tool schemas as the source of truth. Older client workarounds in legacy command files may no longer apply.

## Shared rules

- Set `asset_type="tradfi"` for US-equity work.
- Prefer canonical tickers in `keywords`.
- `metrics` and `signal` accept at most five keywords per call. Split larger lists.
- Pass array fields as arrays. Do not serialize `keywords`, `categories`, or `sources` into strings.
- Put the analytical angle in `query`; put symbols in `keywords`.
- Set explicit `time_range` or `date_from`/`date_to` when time matters.
- Inspect `meta.status`, `meta.warnings`, `meta.filters_applied`, timestamps, and totals before using results.
- Treat source timestamps as part of every factual claim. Do not mix stale and current observations into one snapshot.

## metrics

Use for prices, movers, history, technicals, macro data, earnings calendars, analyst ratings and targets, structured research reports, filings, and fundamentals.

Examples:

```json
{"categories":["market"],"asset_type":"tradfi","keywords":["SPY","QQQ","DIA","VIX"],"query":"live market snapshot","limit":10}
```

```json
{"categories":["macro"],"country":"US","query":"economic calendar","date_from":"2026-07-23","date_to":"2026-07-30","limit":50}
```

```json
{"categories":["fundamentals"],"asset_type":"tradfi","query":"most mentioned stocks in broker research reports","time_range":"7d","limit":10}
```

```json
{"categories":["fundamentals"],"asset_type":"tradfi","keywords":["NVDA"],"query":"broker research reports and analyst price targets","time_range":"30d","verbosity":"detail","limit":10}
```

For a research leaderboard, distinguish:

- `subject` evidence: the ticker is the report's research subject. Use this for formal target-price and rating statistics.
- `mention` evidence: the ticker appears in an industry or peer report. Use this for narrative context, not formal coverage counts.

## news

Use for broad event discovery, media commentary, indexed raw research documents, and curated Twitter content.

Examples:

```json
{"asset_type":"tradfi","query":"","time_range":"1d","sort_by":"hot","limit":20,"verbosity":"concise"}
```

```json
{"asset_type":"tradfi","query":"NVIDIA earnings","sources":["media","twitter"],"time_range":"1d","sort_by":"time","limit":20}
```

```json
{"asset_type":"tradfi","query":"NVDA","sources":["research"],"time_range":"30d","sort_by":"time","limit":20}
```

Empty-query trending is discovery, not verification. Verify material claims with a relevant entity search and current market data.

## signal

Use for public trade calls and positioning:

- `kol_call`: public finance-influencer calls.
- `trader_position`: public trader positions and rollups.
- `insider_trading`: Form 4 and congressional trades.
- `institutional`: 13F holdings and changes.

Examples:

```json
{"categories":["kol_call"],"asset_type":"tradfi","keywords":[],"time_range":"1d","limit":30,"verbosity":"concise"}
```

```json
{"categories":["kol_call"],"asset_type":"tradfi","keywords":["NVDA"],"query":"consensus","time_range":"7d","limit":30}
```

```json
{"categories":["trader_position"],"asset_type":"tradfi","keywords":["NVDA"],"sort_by":"amount","limit":20}
```

```json
{"categories":["insider_trading","institutional"],"asset_type":"tradfi","keywords":["NVDA"],"time_range":"90d","sort_by":"amount","limit":20}
```

Do not interpret tax withholding, option exercise, gifts, or in-kind transfers as discretionary open-market buying or selling. Preserve the transaction type and filing date.

## twitter

Use for a named account or raw tweet operation. Examples:

```json
{"action":"user_tweets","user_name":"example_handle","include_replies":false}
```

```json
{"action":"search","query":"$NVDA lang:en -is:retweet","query_type":"Latest","time_range":"1d"}
```

```json
{"action":"tweet_thread","tweet_id":"1234567890"}
```

Use `news(sources=["twitter"])` or `signal(kol_call)` for broad discovery. Use `twitter` when completeness for a named account or original-thread context matters.

## subscription

Use for a pull-based KOL-call watchlist:

```json
{"action":"set","category":"kol_call","items":[{"symbol":"NVDA","asset_type":"tradfi"}]}
```

```json
{"action":"list","category":"kol_call"}
```

When `list` reports unread items, fetch the actual posts with `signal(categories=["kol_call"], keywords=[...])`, then acknowledge only after presenting them.
