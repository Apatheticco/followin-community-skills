# Trading Controls

Treat trade execution as a separate control plane from research and content operations.

## Tool boundary

- Followin MCP: evidence, quotes, fundamentals, events, research, public calls, and monitoring.
- Purpose-built broker or execution tool: accounts, buying power, orders, fills, positions, and cancellations.
- User: final authority for every live order or order change.

Never treat a public trader position, KOL call, analyst target, or social trend as authorization to trade.

Do not inspect browser tabs, log into a brokerage website, or type orders through general browser automation unless the user explicitly requested that exact interface and the environment provides an approved trading workflow. A generic browser is not a broker tool.

The absence of a broker tool is a capability boundary, not a reason to abandon the workflow. Continue through research, draft, and pre-trade data checks; mark broker-only checks as unavailable and return `INCOMPLETE / NOT_SUBMITTED`.

## Draft the order

Collect:

- Broker and account identifier.
- Symbol and instrument type.
- Buy or sell.
- Quantity or notional.
- Market, limit, stop, stop-limit, or bracket.
- Limit and stop prices.
- Time in force.
- Regular-hours or extended-hours eligibility.
- Maximum intended loss and portfolio concentration after the order.
- Thesis, catalyst, invalidation, and planned review time.

If the user has not specified a required field, write `REQUIRED` and ask before submission. Do not infer account, order type, entry, limit, stop, target, time in force, trading session, share size, risk budget, or exit plan. Do not translate technical indicators into order parameters.

State rules:

- Use `INCOMPLETE` while any mutable order field is `REQUIRED`.
- Use `AWAITING_CONFIRMATION` only after all fields are explicitly supplied and broker pre-trade checks pass.
- Never use `READY_FOR_BROKER` as a substitute for missing user decisions.

## Run pre-trade checks

Use the broker tool to verify:

- Account, buying power, permissions, and current positions.
- Open or duplicate orders.
- Estimated exposure and concentration.
- Market session and instrument tradability.
- Bid, ask, spread, and liquidity when available.
- Short availability and borrow constraints for short sales.

Use Followin to verify:

- Current timestamped quote.
- Near-term earnings, macro, or corporate events.
- Thesis evidence and contradictory evidence.

## Confirm

Immediately before submission, show one confirmation block containing every mutable order field and estimated exposure. Require explicit confirmation for that exact order.

A prior statement such as “you can trade for me” is not confirmation for a later ticket. Any change to symbol, side, quantity, price, order type, account, or time in force requires a new confirmation.

## Submit and reconcile

After confirmation:

1. Submit once.
2. Record the broker order ID and broker timestamp.
3. Fetch order status.
4. Fetch positions and open orders.
5. Report fill quantity, average price, remaining quantity, fees when available, and final status.

On timeout or ambiguous response, query the broker before retrying. Do not blindly resubmit.

## Amend, cancel, and exit

Treat replace, cancel, close, stop, and take-profit actions as live order changes. Show the exact action and require confirmation unless the user has just explicitly requested that exact action with all fields.

Do not claim that monitoring is automatic unless a real automation or broker-native order is active.
