"""Data models for controlled market source adapter attempts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class FetchOutcome(StrEnum):
    """Top-level adapter attempt outcome."""

    ACCEPTED = "accepted"
    FAILED = "failed"


class FetchFailureClass(StrEnum):
    """Controlled failure classifications for adapter attempts."""

    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    TICKER_NOT_FOUND = "ticker_not_found"
    INVALID_RESPONSE_SHAPE = "invalid_response_shape"
    UNSUPPORTED_TICKER = "unsupported_ticker"
    INACTIVE_TICKER = "inactive_ticker"
    CONFIGURATION_FAILURE = "configuration_failure"


@dataclass(frozen=True)
class SourceMetadata:
    """Non-secret provenance metadata for a source interaction."""

    source_name: str
    requested_at: str
    classification: str
    requested_symbol: str | None = None
    endpoint_label: str | None = None
    retrieved_at: str | None = None
    response_status: int | str | None = None
    attribution: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _without_none(
            {
                "source_name": self.source_name,
                "requested_symbol": self.requested_symbol,
                "endpoint_label": self.endpoint_label,
                "requested_at": self.requested_at,
                "retrieved_at": self.retrieved_at,
                "response_status": self.response_status,
                "classification": self.classification,
                "attribution": self.attribution,
            }
        )


@dataclass(frozen=True)
class AdapterFetchResult:
    """Boundary result for one controlled HTTP source fetch attempt."""

    attempt_id: str
    requested_symbol: str
    source_metadata: SourceMetadata
    outcome: FetchOutcome
    canonical_symbol: str | None = None
    timeout_seconds: float = 5.0
    failure_class: FetchFailureClass | None = None
    failure_message: str | None = None
    raw_source_payload: Any | None = None
    adapted_raw_snapshot: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return _without_none(
            {
                "attempt_id": self.attempt_id,
                "requested_symbol": self.requested_symbol,
                "canonical_symbol": self.canonical_symbol,
                "timeout_seconds": self.timeout_seconds,
                "source_metadata": self.source_metadata.to_dict(),
                "outcome": self.outcome.value,
                "failure_class": self.failure_class.value if self.failure_class else None,
                "failure_message": self.failure_message,
                "raw_source_payload": self.raw_source_payload,
                "adapted_raw_snapshot": self.adapted_raw_snapshot,
            }
        )


def _without_none(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}
