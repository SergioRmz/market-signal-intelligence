"""Market source adapter boundary for controlled HTTP snapshot fetches."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from .controlled_http import ControlledHTTPResponse, SourceTimeoutError, fetch_json
from .models import AdapterFetchResult, FetchFailureClass, FetchOutcome, SourceMetadata

Fetcher = Callable[[str, float, str | None], ControlledHTTPResponse]


@dataclass(frozen=True)
class SourceAdapterConfig:
    """Local, non-secret configuration for one controlled HTTP endpoint."""

    endpoint_url: str
    source_name: str = "controlled-http-source-adapter"
    endpoint_label: str = "controlled-http-endpoint"
    timeout_seconds: float = 5.0
    credential_env_var: str | None = None
    watchlist_path: Path = Path("data/watchlists/asset-watchlist.json")

    @classmethod
    def from_environment(cls) -> "SourceAdapterConfig":
        return cls(
            endpoint_url=os.getenv("MSA_CONTROLLED_HTTP_URL", "https://controlled.example.local/market-snapshot"),
            source_name=os.getenv("MSA_SOURCE_NAME", "controlled-http-source-adapter"),
            endpoint_label=os.getenv("MSA_ENDPOINT_LABEL", "controlled-http-endpoint"),
            timeout_seconds=float(os.getenv("MSA_TIMEOUT_SECONDS", "5")),
            credential_env_var=os.getenv("MSA_CREDENTIAL_ENV_VAR") or None,
        )


class MarketSourceAdapter:
    """Fetch one ticker and adapt accepted payloads to the raw snapshot contract."""

    def __init__(self, config: SourceAdapterConfig, fetcher: Fetcher | None = None) -> None:
        self.config = config
        self._fetcher = fetcher or _default_fetcher

    def fetch_snapshot(self, requested_symbol: str) -> AdapterFetchResult:
        requested_at = _now()
        attempt_id = _attempt_id(requested_symbol, requested_at)
        symbol = requested_symbol.strip().upper()
        watchlist_entry = self._watchlist_entry(symbol)

        if watchlist_entry is None:
            return self._failed(
                attempt_id,
                requested_symbol,
                requested_at,
                FetchFailureClass.UNSUPPORTED_TICKER,
                "Ticker is not in the canonical active watchlist scope.",
            )
        if not watchlist_entry.get("active"):
            return self._failed(
                attempt_id,
                requested_symbol,
                requested_at,
                FetchFailureClass.INACTIVE_TICKER,
                "Ticker is present in the watchlist but inactive.",
                canonical_symbol=symbol,
            )

        credential = None
        if self.config.credential_env_var:
            credential = os.getenv(self.config.credential_env_var)
            if not credential:
                return self._failed(
                    attempt_id,
                    requested_symbol,
                    requested_at,
                    FetchFailureClass.CONFIGURATION_FAILURE,
                    "Required local credential environment configuration is missing.",
                    canonical_symbol=symbol,
                )

        try:
            response = self._fetcher(self.config.endpoint_url, self.config.timeout_seconds, credential)
        except SourceTimeoutError:
            return self._failed(
                attempt_id,
                requested_symbol,
                requested_at,
                FetchFailureClass.TIMEOUT,
                "Controlled source request exceeded the configured timeout.",
                canonical_symbol=symbol,
            )

        if response.status_code == 429:
            return self._failed(
                attempt_id,
                requested_symbol,
                requested_at,
                FetchFailureClass.RATE_LIMITED,
                "Controlled source returned a rate-limited response.",
                canonical_symbol=symbol,
                response=response,
            )
        if response.status_code == 404 or _payload_status(response.payload) == "not_found":
            return self._failed(
                attempt_id,
                requested_symbol,
                requested_at,
                FetchFailureClass.TICKER_NOT_FOUND,
                "Controlled source reported ticker not found.",
                canonical_symbol=symbol,
                response=response,
            )

        if not _valid_payload_shape(response.payload, symbol):
            return self._failed(
                attempt_id,
                requested_symbol,
                requested_at,
                FetchFailureClass.INVALID_RESPONSE_SHAPE,
                "Controlled source response is missing required market observation fields.",
                canonical_symbol=symbol,
                response=response,
            )

        raw_snapshot = self._adapt_raw_snapshot(attempt_id, symbol, response.payload)
        if not raw_snapshot_compatible(raw_snapshot, self.config.watchlist_path):
            return self._failed(
                attempt_id,
                requested_symbol,
                requested_at,
                FetchFailureClass.INVALID_RESPONSE_SHAPE,
                "Adapted raw snapshot does not satisfy existing market snapshot validation expectations.",
                canonical_symbol=symbol,
                response=response,
            )
        return AdapterFetchResult(
            attempt_id=attempt_id,
            requested_symbol=requested_symbol,
            canonical_symbol=symbol,
            timeout_seconds=self.config.timeout_seconds,
            source_metadata=self._metadata("accepted", requested_at, requested_symbol, response),
            outcome=FetchOutcome.ACCEPTED,
            raw_source_payload=response.payload,
            adapted_raw_snapshot=raw_snapshot,
        )

    def _adapt_raw_snapshot(self, attempt_id: str, symbol: str, payload: dict[str, Any]) -> dict[str, Any]:
        observed_at = str(payload["observed_at"])
        return {
            "raw_snapshot_id": f"raw-adapter-{symbol.lower()}-{_compact_timestamp(observed_at)}",
            "schema_version": "1.0.0",
            "source": {
                "name": self.config.source_name,
                "category": "local_sample",
                "reference": attempt_id,
            },
            "asset": {
                "symbol": symbol,
                "market": str(payload["market"]),
            },
            "observed_at": observed_at,
            "observed_values": {
                "last_price": float(payload["last_price"]),
                "currency": str(payload["currency"]),
                "volume": float(payload["volume"]),
            },
            "provenance": {
                "sample_origin": "Adapted from preserved controlled HTTP source payload fixture.",
                "review_notes": "Adapter output uses the existing raw market snapshot contract; normalization remains owned by the 003 pipeline.",
            },
            "notes": "Technical adapter sample for pipeline validation.",
        }

    def _watchlist_entry(self, symbol: str) -> dict[str, Any] | None:
        data = json.loads(self.config.watchlist_path.read_text())
        for asset in data.get("assets", []):
            if asset.get("symbol") == symbol:
                return asset
        return None

    def _failed(
        self,
        attempt_id: str,
        requested_symbol: str,
        requested_at: str,
        failure_class: FetchFailureClass,
        failure_message: str,
        *,
        canonical_symbol: str | None = None,
        response: ControlledHTTPResponse | None = None,
    ) -> AdapterFetchResult:
        return AdapterFetchResult(
            attempt_id=attempt_id,
            requested_symbol=requested_symbol,
            canonical_symbol=canonical_symbol,
            timeout_seconds=self.config.timeout_seconds,
            source_metadata=self._metadata(failure_class.value, requested_at, requested_symbol, response),
            outcome=FetchOutcome.FAILED,
            failure_class=failure_class,
            failure_message=failure_message,
            raw_source_payload=response.payload if response else None,
        )

    def _metadata(
        self,
        classification: str,
        requested_at: str,
        requested_symbol: str,
        response: ControlledHTTPResponse | None = None,
    ) -> SourceMetadata:
        return SourceMetadata(
            source_name=self.config.source_name,
            requested_symbol=requested_symbol,
            endpoint_label=self.config.endpoint_label,
            requested_at=requested_at,
            retrieved_at=response.retrieved_at if response else None,
            response_status=response.status_code if response else None,
            classification=classification,
            attribution="Controlled HTTP source fixture for deterministic adapter validation.",
        )


def _default_fetcher(endpoint_url: str, timeout_seconds: float, credential: str | None) -> ControlledHTTPResponse:
    return fetch_json(endpoint_url, timeout_seconds=timeout_seconds, credential=credential)


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _attempt_id(symbol: str, requested_at: str) -> str:
    safe_symbol = re.sub(r"[^A-Za-z0-9]+", "-", symbol.strip()).strip("-").lower() or "unknown"
    return f"source-attempt-{safe_symbol}-{_compact_timestamp(requested_at)}"


def _compact_timestamp(value: str) -> str:
    return value.replace("-", "").replace(":", "").replace("+00:00", "Z")


def _payload_status(payload: Any) -> str | None:
    if isinstance(payload, dict):
        status = payload.get("status")
        return str(status) if status is not None else None
    return None


def _valid_payload_shape(payload: Any, symbol: str) -> bool:
    if not isinstance(payload, dict):
        return False
    if str(payload.get("symbol", "")).upper() != symbol:
        return False
    if not isinstance(payload.get("market"), str) or not payload["market"]:
        return False
    if payload.get("currency") != "MXN":
        return False
    if not isinstance(payload.get("observed_at"), str):
        return False
    return _non_negative_number(payload.get("last_price")) and _non_negative_number(payload.get("volume"))


def _non_negative_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool) and value >= 0


def raw_snapshot_compatible(snapshot: dict[str, Any], watchlist_path: Path) -> bool:
    """Check adapter output against the existing raw snapshot validation expectations."""

    try:
        symbol = snapshot["asset"]["symbol"]
        observed_values = snapshot["observed_values"]
        provenance = snapshot["provenance"]
    except (KeyError, TypeError):
        return False
    if snapshot.get("source", {}).get("category") != "local_sample":
        return False
    if not isinstance(symbol, str) or not re.fullmatch(r"[A-Z0-9]+", symbol):
        return False
    if not isinstance(snapshot.get("observed_at"), str):
        return False
    if not _non_negative_number(observed_values.get("last_price")):
        return False
    if observed_values.get("currency") != "MXN":
        return False
    if not _non_negative_number(observed_values.get("volume")):
        return False
    if not provenance.get("sample_origin") or not provenance.get("review_notes"):
        return False

    watchlist = json.loads(watchlist_path.read_text())
    return any(asset.get("symbol") == symbol and asset.get("active") is True for asset in watchlist.get("assets", []))
