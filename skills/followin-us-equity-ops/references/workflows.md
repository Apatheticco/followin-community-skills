# Operating Workflows

## morning-brief

Goal: summarize the most important overnight information and today's decision calendar.

Collect:

1. `news` empty-query tradfi trending for the requested overnight window.
2. Entity-specific `news` searches for the top material events.
3. `metrics` market snapshots for major indices or ETFs and the affected tickers.
4. `metrics` US macro calendar and market-wide earnings calendar for today.
5. A small `signal(kol_call)` scan only when social activity materially changes the story.

Rank:

- Materiality: earnings, guidance, policy, macro, regulation, litigation, financing, M&A, and supply-chain changes outrank commentary.
- Breadth: market-wide and sector-wide transmission outranks isolated noise.
- Recency: use the requested overnight cutoff, not a vague “recent.”
- Verification: prefer events corroborated by multiple independent records.
- Price confirmation: use current `metrics`, not percentages quoted in articles or posts.

Publishable sections:

1. Market in one sentence.
2. Three to five overnight events: what happened, affected tickers, and why it matters.
3. Today's macro and earnings calendar with timezone.
4. Optional social-temperature line.
5. Data timestamp and informational-use disclaimer.

Do not force a fixed item count. Return fewer items when the evidence is thin.

## event-radar

Goal: preview events that can change expectations over the next 24 hours or seven days.

Collect:

1. `metrics(categories=["macro"])` with explicit US date bounds.
2. `metrics` market-wide earnings calendar with explicit date bounds.
3. For selected companies, `metrics` next-earnings dates, estimates, recent price behavior, and analyst context.
4. `news` verification for material dates or late changes when needed.

For each event, record:

- Event and exact timestamp in US Eastern and the user's timezone.
- Expected value or consensus when available.
- Previous value.
- Primary affected assets and transmission logic.
- What result would count as upside, baseline, or downside surprise.
- Refresh trigger and source timestamp.

Order by expected market impact, then time. Exclude low-impact calendar clutter unless the user asks for a full calendar.

## research-radar

Goal: find densely discussed tickers and turn scattered reports into comparable research.

Collect:

1. `metrics` research-report most-mentioned leaderboard for the requested window.
2. Drill into shortlisted tickers with `metrics(categories=["fundamentals"], keywords=[ticker], query="broker research reports and analyst price targets", verbosity="detail")`.
3. Pull current price in the same response or a separate `metrics` snapshot.
4. Add `news` or `signal` only when a current event or public strategy signal explains the research burst.

Shortlist using:

- Distinct institution count before raw mention count.
- Subject-report coverage before incidental mentions.
- Freshness and identifiable catalysts.
- Target-price coverage and dispersion.
- Bull and bear evidence availability.

Normalize targets with `scripts/normalize_price_targets.py`. Use the same listing and currency, keep the latest record per institution, and report:

- Distinct institution count.
- Low, median, and high target.
- Dispersion `(high - low) / median`.
- Median and range implied upside or downside versus the timestamped current price.
- Excluded records and reasons.

Output a leaderboard plus one independent research note per selected ticker. A research note must include thesis, catalysts, target distribution, bear case, open questions, and evidence dates.

## social-pulse

Goal: identify which US-equity tickers are attracting meaningful Twitter/X attention and what changed.

Collect:

1. `news(sources=["twitter"])` for broad discovery.
2. `signal(categories=["kol_call"])` for explicit public calls.
3. `twitter` for a named account, tweet thread, list, or exact search when raw context is required.
4. `metrics` to verify current price reaction.

Normalize:

- Deduplicate by tweet ID or source URL.
- Count unique authors separately from posts.
- Separate original posts, replies, retweets, and quoted commentary when possible.
- Separate explicit strategy signals from general opinion.
- Preserve direction, horizon, trigger, invalidation, and confidence only when explicitly stated.

Output:

- Hot-ticker table with unique authors, post direction, recency, and material catalyst.
- “What changed” timeline.
- Representative bull and bear evidence.
- Data-quality note covering sample size and coverage limits.

Never label discussion volume as buying pressure.

## strategy-signal

Goal: summarize public strategies from US-stock traders and analysts without turning them into automatic trade instructions.

Collect:

1. `signal(categories=["kol_call"])` for explicit calls.
2. `signal(categories=["trader_position"])` for observable public positions.
3. `twitter` for the original account or thread when context is incomplete.
4. `metrics` for current price, volatility, earnings dates, and analyst data.

Accept a post as a strategy signal only when at least two of these are explicit:

- Direction or action.
- Entry or trigger.
- Time horizon.
- Target or exit.
- Invalidation or stop.
- Position-size or risk statement.

For each accepted signal, show source, timestamp, ticker, direction, horizon, trigger, invalidation, current status, and original link. Mark all missing fields. Do not invent a stop or target.

Aggregate signals by unique author, not split rows. Report agreement as `x of n observed authors`, never as broad market consensus.

## signal-watchlist

Goal: maintain a pull-based inbox for new KOL calls.

1. Save requested symbols with `subscription(action="set")`.
2. Check unread counts with `subscription(action="list")`.
3. Fetch unread content with `signal(categories=["kol_call"])`.
4. Present the new items.
5. Acknowledge only after the items have been shown.

State clearly that this is an inbox checked on demand, not guaranteed server push.

## trade-desk

Goal: turn a researched thesis into a controlled broker workflow.

Read [trading-controls.md](trading-controls.md) before doing anything else. Followin supplies evidence and monitoring, not execution.

Stages:

1. Research packet: thesis, evidence, catalyst, invalidation, event risk, current price, liquidity, and data timestamp.
2. Draft ticket: account, symbol, side, quantity or notional, order type, price controls, time in force, and attached exits.
3. Pre-trade checks: buying power, position concentration, duplicate orders, market session, spread, earnings or macro risk, and maximum loss.
4. Explicit order-level confirmation.
5. Broker submission.
6. Broker status and position reconciliation.
7. Trade journal and monitoring triggers.

Without a connected broker tool, still run the Followin research and event-risk checks and create an incomplete draft ticket. Copy only order fields explicitly supplied by the user. Mark all other mutable fields `REQUIRED`, finish after stage 3, and label the result `INCOMPLETE / NOT_SUBMITTED`. Do not answer with only a generic inability statement, and do not use technical indicators to choose order parameters.
