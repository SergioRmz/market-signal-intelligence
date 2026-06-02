from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from market_signal_intelligence.sources.adapter import MarketSourceAdapter, SourceAdapterConfig  # noqa: E402
from market_signal_intelligence.sources.controlled_http import ControlledHTTPResponse, SourceTimeoutError  # noqa: E402
from market_signal_intelligence.sources.models import FetchFailureClass, FetchOutcome  # noqa: E402


class MarketSourceAdapterFailureTest(unittest.TestCase):
    def adapter_with_response(self, status_code: int, fixture: str) -> MarketSourceAdapter:
        payload = json.loads((ROOT / f"tests/fixtures/market-source-adapter/{fixture}").read_text())

        def fetcher(_url: str, _timeout: float, _credential: str | None) -> ControlledHTTPResponse:
            return ControlledHTTPResponse(status_code, payload, "2026-06-01T15:00:01Z", "application/json")

        return MarketSourceAdapter(SourceAdapterConfig(endpoint_url="https://controlled.example.local/market-snapshot"), fetcher)

    def assert_failed(self, result, failure_class: FetchFailureClass) -> None:
        self.assertEqual(FetchOutcome.FAILED, result.outcome)
        self.assertEqual(failure_class, result.failure_class)
        self.assertIsNone(result.adapted_raw_snapshot)
        self.assertEqual(failure_class.value, result.source_metadata.classification)

    def test_timeout_classification(self) -> None:
        def fetcher(_url: str, _timeout: float, _credential: str | None) -> ControlledHTTPResponse:
            raise SourceTimeoutError("timeout")

        adapter = MarketSourceAdapter(SourceAdapterConfig(endpoint_url="https://controlled.example.local/market-snapshot"), fetcher)
        self.assert_failed(adapter.fetch_snapshot("AMXL"), FetchFailureClass.TIMEOUT)

    def test_rate_limited_classification_preserves_payload(self) -> None:
        result = self.adapter_with_response(429, "failure-rate-limited.json").fetch_snapshot("AMXL")
        self.assert_failed(result, FetchFailureClass.RATE_LIMITED)
        self.assertEqual("rate_limited", result.raw_source_payload["status"])

    def test_ticker_not_found_classification_preserves_payload(self) -> None:
        result = self.adapter_with_response(404, "failure-ticker-not-found.json").fetch_snapshot("AMXL")
        self.assert_failed(result, FetchFailureClass.TICKER_NOT_FOUND)
        self.assertEqual("not_found", result.raw_source_payload["status"])

    def test_invalid_shape_classification_preserves_payload(self) -> None:
        result = self.adapter_with_response(200, "failure-invalid-shape.json").fetch_snapshot("AMXL")
        self.assert_failed(result, FetchFailureClass.INVALID_RESPONSE_SHAPE)
        self.assertNotIn("last_price", result.raw_source_payload)

    def test_unsupported_ticker_fails_before_source_fetch(self) -> None:
        def fetcher(_url: str, _timeout: float, _credential: str | None) -> ControlledHTTPResponse:
            self.fail("unsupported ticker should not call source")

        adapter = MarketSourceAdapter(SourceAdapterConfig(endpoint_url="https://controlled.example.local/market-snapshot"), fetcher)
        self.assert_failed(adapter.fetch_snapshot("XYZ"), FetchFailureClass.UNSUPPORTED_TICKER)

    def test_inactive_ticker_fails_before_source_fetch(self) -> None:
        def fetcher(_url: str, _timeout: float, _credential: str | None) -> ControlledHTTPResponse:
            self.fail("inactive ticker should not call source")

        adapter = MarketSourceAdapter(SourceAdapterConfig(endpoint_url="https://controlled.example.local/market-snapshot"), fetcher)
        result = adapter.fetch_snapshot("KOFUBL")
        self.assert_failed(result, FetchFailureClass.INACTIVE_TICKER)
        self.assertEqual("KOFUBL", result.canonical_symbol)

    def test_missing_credential_classification(self) -> None:
        os.environ.pop("MSA_TEST_CREDENTIAL", None)

        def fetcher(_url: str, _timeout: float, _credential: str | None) -> ControlledHTTPResponse:
            self.fail("missing credential should not call source")

        adapter = MarketSourceAdapter(
            SourceAdapterConfig(
                endpoint_url="https://controlled.example.local/market-snapshot",
                credential_env_var="MSA_TEST_CREDENTIAL",
            ),
            fetcher,
        )
        self.assert_failed(adapter.fetch_snapshot("AMXL"), FetchFailureClass.CONFIGURATION_FAILURE)


if __name__ == "__main__":
    unittest.main()
