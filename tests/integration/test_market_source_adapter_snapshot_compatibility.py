from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from market_signal_intelligence.sources.adapter import raw_snapshot_compatible  # noqa: E402


class MarketSourceAdapterSnapshotCompatibilityTest(unittest.TestCase):
    def test_adapter_raw_snapshot_sample_reuses_existing_raw_expectations(self) -> None:
        sample = json.loads(
            (ROOT / "data/samples/market-source-adapter/raw-snapshots/success-active-equity-raw-snapshot.json").read_text()
        )
        self.assertTrue(raw_snapshot_compatible(sample, ROOT / "data/watchlists/asset-watchlist.json"))

    def test_existing_normalized_artifacts_remain_the_only_normalization_flow(self) -> None:
        normalized_samples = list((ROOT / "data/samples/market-snapshots/normalized/valid").glob("*.json"))
        self.assertGreaterEqual(len(normalized_samples), 2)
        adapter_normalized_samples = list((ROOT / "data/samples/market-source-adapter").glob("**/*normalized*.json"))
        self.assertEqual([], adapter_normalized_samples)


if __name__ == "__main__":
    unittest.main()
