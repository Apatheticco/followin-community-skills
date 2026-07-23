# Output Contracts

Return an operating packet with four blocks. Keep internal blocks visually separate from publishable copy.

## 1. Publishable

Write channel-ready copy in the requested language and format. If unspecified, use concise Chinese plain text.

Requirements:

- Put the `as_of` timestamp and timezone near the title.
- Lead with the decision-relevant conclusion.
- Explain why each event matters in plain language.
- Include both supporting and conflicting evidence when material.
- Avoid “must buy,” “guaranteed,” and similar certainty language.
- Include an informational-use disclaimer for external market content.

## 2. Evidence ledger

Use one row per material claim:

| Claim | Source type | Source or URL | Published at | Data as of | Status |
|---|---|---|---|---|---|
| Concise claim | Followin metrics/news/signal/twitter | Original URL or dataset label | Timestamp | Timestamp | verified / single-source / stale / conflicting |

Do not publish the ledger by default, but always keep it in the response for the operator unless the user asks for copy only.

## 3. Editor notes

List:

- Items excluded and why.
- Data gaps, stale fields, and small samples.
- Conflicts between price, news, research, and social evidence.
- Claims requiring manual review before publication.
- Whether supplemental non-Followin sources were used.

## 4. Next refresh

Specify a concrete trigger, such as:

- `08:30 Asia/Shanghai`
- `30 minutes before US market open`
- `after CPI release`
- `when the company files an 8-K`
- `when unread KOL-call count changes`

## Trade packet

Replace the publishable block with:

1. `Research summary`
2. `Draft order ticket`
3. `Pre-trade checks`
4. `Approval state`
5. `Broker result`
6. `Position reconciliation`
7. `Monitoring and exit triggers`

Use this draft state machine:

- `INCOMPLETE`: one or more mutable order fields are missing.
- `AWAITING_CONFIRMATION`: every field is complete and broker pre-trade checks passed.
- `SUBMITTED`, `PARTIALLY_FILLED`, `FILLED`, `CANCELED`, or `REJECTED`: only from broker responses.

Without a broker tool, the highest possible state is `INCOMPLETE / NOT_SUBMITTED`.

Use this minimum ticket. Copy only user-specified values; keep every other mutable field exactly `REQUIRED`.

```yaml
draft_status: INCOMPLETE
execution_status: NOT_SUBMITTED
broker: REQUIRED
account_id: REQUIRED
symbol: USER_VALUE_OR_REQUIRED
side: USER_VALUE_OR_REQUIRED
quantity_or_notional: USER_VALUE_OR_REQUIRED
order_type: REQUIRED
limit_price: REQUIRED_IF_LIMIT
stop_price: REQUIRED_IF_STOP
time_in_force: REQUIRED
trading_session: REQUIRED
maximum_intended_loss: REQUIRED
attached_exits: REQUIRED_OR_NONE_AS_SPECIFIED_BY_USER
```

Do not generate a client order ID, entry, stop, target, or “recommended cash” value for an incomplete ticket.
