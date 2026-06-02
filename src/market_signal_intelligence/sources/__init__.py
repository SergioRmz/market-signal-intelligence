"""Controlled market source adapter boundary."""

from .adapter import MarketSourceAdapter, SourceAdapterConfig, raw_snapshot_compatible
from .models import FetchFailureClass, FetchOutcome

__all__ = [
    "FetchFailureClass",
    "FetchOutcome",
    "MarketSourceAdapter",
    "SourceAdapterConfig",
    "raw_snapshot_compatible",
]
