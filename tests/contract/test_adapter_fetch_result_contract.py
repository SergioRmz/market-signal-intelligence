from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from market_signal_intelligence.sources.models import (  # noqa: E402
    AdapterFetchResult,
    FetchFailureClass,
    FetchOutcome,
    SourceMetadata,
)


class AdapterFetchResultContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = json.loads(
            (ROOT / "specs/004-market-source-adapter/contracts/adapter-fetch-result.schema.json").read_text()
        )

    def test_schema_exposes_expected_failure_classes(self) -> None:
        expected = {
            "timeout",
            "rate_limited",
            "ticker_not_found",
            "invalid_response_shape",
            "unsupported_ticker",
            "inactive_ticker",
            "configuration_failure",
        }
        self.assertEqual(expected, set(self.schema["properties"]["failure_class"]["enum"]))

    def test_success_result_matches_contract_boundary(self) -> None:
        result = AdapterFetchResult(
            attempt_id="source-attempt-amxl-20260601T150000Z",
            requested_symbol="AMXL",
            canonical_symbol="AMXL",
            timeout_seconds=5,
            source_metadata=SourceMetadata(
                source_name="controlled-http-source-adapter",
                endpoint_label="controlled-http-endpoint",
                requested_at="2026-06-01T15:00:00Z",
                retrieved_at="2026-06-01T15:00:01Z",
                response_status=200,
                classification="accepted",
            ),
            outcome=FetchOutcome.ACCEPTED,
            raw_source_payload={"symbol": "AMXL"},
            adapted_raw_snapshot={"raw_snapshot_id": "raw-adapter-amxl-20260601T150000Z"},
        ).to_dict()

        self.assertEqual("accepted", result["outcome"])
        self.assertIn("raw_source_payload", result)
        self.assertIn("adapted_raw_snapshot", result)
        self.assertNotIn("failure_class", result)

    def test_failure_result_matches_contract_boundary(self) -> None:
        result = AdapterFetchResult(
            attempt_id="source-attempt-amxl-timeout",
            requested_symbol="AMXL",
            canonical_symbol="AMXL",
            timeout_seconds=5,
            source_metadata=SourceMetadata(
                source_name="controlled-http-source-adapter",
                endpoint_label="controlled-http-endpoint",
                requested_at="2026-06-01T15:00:00Z",
                classification="timeout",
            ),
            outcome=FetchOutcome.FAILED,
            failure_class=FetchFailureClass.TIMEOUT,
            failure_message="Controlled source request exceeded the configured timeout.",
        ).to_dict()

        self.assertEqual("failed", result["outcome"])
        self.assertEqual("timeout", result["failure_class"])
        self.assertIn("failure_message", result)
        self.assertNotIn("adapted_raw_snapshot", result)


if __name__ == "__main__":
    unittest.main()
