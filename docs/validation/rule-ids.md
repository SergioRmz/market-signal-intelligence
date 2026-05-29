# Validation Rule IDs

## Contract Rules

- `AE-REQ-001`: `event_id` is required and must be a non-empty string.
- `AE-REQ-002`: `event_type` is required and must be a non-empty string.
- `AE-REQ-003`: `schema_version` is required and must identify the schema version.
- `AE-REQ-004`: `occurred_at` is required and must be an RFC3339 timestamp.
- `AE-REQ-005`: `source.name` is required and must be a non-empty string.
- `AE-REQ-006`: `source.category` must be one of `allowed`, `conditional`, or `prohibited`.
- `AE-REQ-007`: `asset.symbol` is required and must be a non-empty string.
- `AE-REQ-008`: `asset.market` is required and must be a non-empty string.
- `AE-REQ-009`: `payload` is required and must be an object.

## Policy Rules

- `SRC-001`: Source category must be documented in the allowed sources policy.
- `SRC-002`: Conditional sources must document usage constraints.
- `SRC-003`: Prohibited sources must not appear in valid samples.

## Review Rules

- `REV-001`: PR validation evidence must include commands executed and pass/fail result.
- `REV-002`: Each invalid sample must map to at least one rule ID.

## Watchlist Rules

- `WL-REQ-001`: Watchlist file must exist at `data/watchlists/asset-watchlist.json`.
- `WL-REQ-002`: Watchlist must include `watchlist_id`, `version`, `effective_date`, `purpose`, and `assets`.
- `WL-REQ-003`: Watchlist must include at least five active equity entries with `asset_role` set to `monitoring_target`.
- `WL-REQ-004`: Watchlist entry symbols must be non-empty, unique, canonical local identifiers.
- `WL-REQ-005`: Primary monitoring targets must use `asset_type` `equity`; `index` is allowed only for `IPC` as `reference_benchmark`.
- `WL-REQ-006`: Watchlist entries must use currency `MXN`.
- `WL-REQ-007`: Watchlist entries must include market metadata sufficient to identify BMV/Mexico context.
- `WL-REQ-008`: Watchlist entries must include traceability context.
- `WL-REQ-009`: Watchlist and samples must not include live prices, target prices, ratings, trading signals, recommendations, or performance forecasts.
- `WL-REQ-010`: Invalid watchlist samples must map to at least one rule ID in `docs/validation/sample-rule-mapping.md`.

## Market Snapshot Rules

- `MS-REQ-001`: Raw and normalized snapshot contracts must exist and be documented.
- `MS-REQ-002`: Raw snapshots must include required identity, source, asset, timestamp, observed values, and provenance fields.
- `MS-REQ-003`: Normalized snapshots must include required identity, `raw_snapshot_id`, asset, timestamp, observed values, and provenance fields.
- `MS-REQ-004`: Snapshot `asset.symbol` must match a canonical active symbol in `data/watchlists/asset-watchlist.json`.
- `MS-REQ-005`: `S&P/BMV IPC` is optional benchmark context only and must not count toward equity snapshot coverage.
- `MS-REQ-006`: Snapshot observed values must include `last_price`, `currency`, and `volume`.
- `MS-REQ-007`: Normalized snapshots must reference an existing valid raw snapshot by `raw_snapshot_id`.
- `MS-REQ-008`: Invalid samples must map to at least one `MS-REQ-*` rule ID in `docs/validation/sample-rule-mapping.md`.
- `MS-REQ-009`: Snapshot artifacts must not include live-feed behavior, advisory language, target prices, ratings, rankings, recommendations, or performance forecasts.
- `MS-REQ-010`: Snapshot validation must be reproducible locally without network access or deployed services.
