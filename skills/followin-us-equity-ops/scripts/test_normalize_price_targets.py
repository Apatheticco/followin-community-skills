#!/usr/bin/env python3

import unittest

from normalize_price_targets import normalize


class NormalizePriceTargetsTest(unittest.TestCase):
    def test_deduplicates_and_excludes_mixed_evidence(self):
        result = normalize({
            "as_of": "2026-07-23T08:00:00Z",
            "current_price": 100,
            "current_currency": "USD",
            "targets": [
                {"institution": "Alpha", "target": 110, "currency": "USD", "published_at": "2026-07-01", "report_type": "subject"},
                {"institution": "Alpha", "target": 120, "currency": "USD", "published_at": "2026-07-20", "report_type": "subject"},
                {"institution": "Beta", "target": 80, "currency": "USD", "published_at": "2026-07-18", "report_type": "subject"},
                {"institution": "Context Only", "target": 200, "currency": "USD", "published_at": "2026-07-19", "report_type": "mention"},
                {"institution": "Foreign", "target": 140, "currency": "EUR", "published_at": "2026-07-19", "report_type": "subject"},
            ],
        })

        self.assertEqual(result["institution_count"], 2)
        self.assertEqual(result["target_low"], 80.0)
        self.assertEqual(result["target_median"], 100.0)
        self.assertEqual(result["target_high"], 120.0)
        self.assertEqual(result["upside_to_median_pct"], 0.0)
        self.assertEqual(len(result["excluded"]), 3)

    def test_rejects_empty_valid_set(self):
        with self.assertRaisesRegex(ValueError, "no valid"):
            normalize({
                "current_price": 100,
                "current_currency": "USD",
                "targets": [
                    {"institution": "Alpha", "target": 120, "currency": "EUR", "report_type": "subject"},
                ],
            })


if __name__ == "__main__":
    unittest.main()
