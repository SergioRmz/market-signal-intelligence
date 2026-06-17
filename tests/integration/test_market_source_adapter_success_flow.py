from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from market_signal_intelligence.sources.adapter import (  # noqa: E402
    MarketSourceAdapter,
    SourceAdapterConfig,
    raw_snapshot_compatible,
)
from market_signal_intelligence.sources.controlled_http import ControlledHTTPResponse  # noqa: E402
from market_signal_intelligence.sources.models import FetchOutcome  # noqa: E402


class MarketSourceAdapterSuccessFlowTest(unittest.TestCase):
    def test_success_flow_produces_compatible_raw_snapshot(self) -> None:
        payload = json.loads((ROOT / "tests/fixtures/market-source-adapter/success-active-equity.json").read_text())

        def fetcher(_url: str, _timeout: float, _credential: str | None) -> ControlledHTTPResponse:
            return ControlledHTTPResponse(200, payload, "2026-06-01T15:00:01Z", "application/json")

        adapter = MarketSourceAdapter(SourceAdapterConfig(endpoint_url="https://controlled.example.local/market-snapshot"), fetcher)
        result = adapter.fetch_snapshot("AMXL")

        self.assertEqual(FetchOutcome.ACCEPTED, result.outcome)
        self.assertTrue(raw_snapshot_compatible(result.adapted_raw_snapshot, ROOT / "data/watchlists/asset-watchlist.json"))
        self.assertEqual(payload, result.raw_source_payload)
        self.assertEqual("accepted", result.source_metadata.classification)


if __name__ == "__main__":
    unittest.main()
