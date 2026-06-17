from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from market_signal_intelligence.sources.adapter import MarketSourceAdapter, SourceAdapterConfig  # noqa: E402
from market_signal_intelligence.sources.controlled_http import ControlledHTTPResponse  # noqa: E402
from market_signal_intelligence.sources.models import FetchOutcome  # noqa: E402


class MarketSourceAdapterSuccessTest(unittest.TestCase):
    def test_active_watchlist_ticker_accepts_successful_payload(self) -> None:
        payload = json.loads((ROOT / "tests/fixtures/market-source-adapter/success-active-equity.json").read_text())

        def fetcher(_url: str, timeout: float, credential: str | None) -> ControlledHTTPResponse:
            self.assertEqual(5, timeout)
            self.assertIsNone(credential)
            return ControlledHTTPResponse(200, payload, "2026-06-01T15:00:01Z", "application/json")

        adapter = MarketSourceAdapter(
            SourceAdapterConfig(endpoint_url="https://controlled.example.local/market-snapshot"),
            fetcher=fetcher,
        )
        result = adapter.fetch_snapshot("AMXL")

        self.assertEqual(FetchOutcome.ACCEPTED, result.outcome)
        self.assertEqual("AMXL", result.canonical_symbol)
        self.assertEqual(payload, result.raw_source_payload)
        self.assertIsNotNone(result.adapted_raw_snapshot)
        self.assertEqual("AMXL", result.adapted_raw_snapshot["asset"]["symbol"])
        self.assertEqual("local_sample", result.adapted_raw_snapshot["source"]["category"])
        self.assertEqual(result.attempt_id, result.adapted_raw_snapshot["source"]["reference"])


if __name__ == "__main__":
    unittest.main()
