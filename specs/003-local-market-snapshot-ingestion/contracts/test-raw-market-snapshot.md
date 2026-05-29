# Contract Scenario: Raw Market Snapshot

## Purpose

Verify raw market snapshot samples preserve source-shaped local observations while remaining eligible only when the asset symbol is canonical and active in `data/watchlists/asset-watchlist.json`.

## Required Checks

- Valid raw samples include `raw_snapshot_id`, `schema_version`, `source`, `asset`, `observed_at`, `observed_values`, and `provenance`.
- `source.category` is `local_sample`.
- `asset.symbol` is a canonical watchlist symbol and does not use exchange symbol variants.
- `observed_values` includes `last_price`, `currency`, and `volume`.
- Invalid raw samples demonstrate missing watchlist asset, inactive watchlist asset, malformed required fields, and prohibited content.

## Expected Outcome

The local validation command accepts valid raw samples and rejects invalid raw samples with explicit `MS-REQ-*` mappings.
