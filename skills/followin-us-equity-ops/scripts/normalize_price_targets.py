#!/usr/bin/env python3
"""Normalize same-listing analyst price targets into comparable statistics."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_date(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        try:
            parsed = datetime.strptime(text[:10], "%Y-%m-%d")
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) and parsed > 0 else None


def round_or_none(value: float | None, digits: int = 2) -> float | None:
    return None if value is None else round(value, digits)


def normalize(payload: dict[str, Any]) -> dict[str, Any]:
    currency = str(payload.get("current_currency") or "").upper()
    current_price = number(payload.get("current_price"))
    raw_targets = payload.get("targets")
    if not currency:
        raise ValueError("current_currency is required")
    if current_price is None:
        raise ValueError("current_price must be a positive number")
    if not isinstance(raw_targets, list):
        raise ValueError("targets must be an array")

    excluded: list[dict[str, Any]] = []
    latest_by_institution: dict[str, dict[str, Any]] = {}

    for index, row in enumerate(raw_targets):
        if not isinstance(row, dict):
            excluded.append({"index": index, "reason": "not_an_object"})
            continue
        institution = str(row.get("institution") or "").strip()
        target = number(row.get("target"))
        row_currency = str(row.get("currency") or "").upper()
        report_type = str(row.get("report_type") or "subject").lower()
        published_at = parse_date(row.get("published_at"))

        if not institution:
            excluded.append({"index": index, "reason": "missing_institution"})
            continue
        if target is None:
            excluded.append({"index": index, "institution": institution, "reason": "invalid_target"})
            continue
        if row_currency != currency:
            excluded.append({"index": index, "institution": institution, "reason": "currency_mismatch"})
            continue
        if report_type != "subject":
            excluded.append({"index": index, "institution": institution, "reason": "not_subject_research"})
            continue

        candidate = {
            "institution": institution,
            "target": target,
            "currency": row_currency,
            "published_at": published_at.isoformat() if published_at else None,
            "_published_at": published_at,
            "_index": index,
        }
        previous = latest_by_institution.get(institution.casefold())
        previous_key = (
            previous.get("_published_at") or datetime.min.replace(tzinfo=timezone.utc),
            previous.get("_index", -1),
        ) if previous else None
        candidate_key = (
            published_at or datetime.min.replace(tzinfo=timezone.utc),
            index,
        )
        if previous is None or candidate_key >= previous_key:
            if previous is not None:
                excluded.append({
                    "index": previous["_index"],
                    "institution": previous["institution"],
                    "reason": "superseded_by_newer_target",
                })
            latest_by_institution[institution.casefold()] = candidate
        else:
            excluded.append({"index": index, "institution": institution, "reason": "older_duplicate"})

    included = sorted(
        latest_by_institution.values(),
        key=lambda row: (row["_published_at"] or datetime.min.replace(tzinfo=timezone.utc), row["institution"]),
        reverse=True,
    )
    values = [row["target"] for row in included]
    if not values:
        raise ValueError("no valid same-currency subject targets remain")

    low = min(values)
    median = statistics.median(values)
    high = max(values)
    dispersion = ((high - low) / median * 100) if median else None

    for row in included:
        row.pop("_published_at", None)
        row.pop("_index", None)

    return {
        "as_of": payload.get("as_of"),
        "currency": currency,
        "current_price": current_price,
        "institution_count": len(values),
        "target_low": round_or_none(low),
        "target_median": round_or_none(median),
        "target_high": round_or_none(high),
        "dispersion_pct": round_or_none(dispersion),
        "upside_to_low_pct": round_or_none((low / current_price - 1) * 100),
        "upside_to_median_pct": round_or_none((median / current_price - 1) * 100),
        "upside_to_high_pct": round_or_none((high / current_price - 1) * 100),
        "included": included,
        "excluded": excluded,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSON input file, or - for stdin")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    try:
        if args.input == "-":
            payload = json.load(sys.stdin)
        else:
            payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        result = normalize(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
