# Data Model: Initial Asset Watchlist

## Entity: Asset Watchlist

Represents the versioned local allowlist of assets later ingestion features may monitor.

### Fields

- `watchlist_id`: Stable identifier for the watchlist. Required; expected value `asset-watchlist`.
- `version`: Version identifier for the watchlist content. Required; must change when governed content changes.
- `effective_date`: Date when the watchlist version becomes the active review baseline. Required; ISO date.
- `purpose`: Human-readable statement that the file is an allowlist for future monitoring scope. Required; must remain non-advisory.
- `assets`: Collection of watchlist entries. Required; exactly one active IPC entry in this feature.

### Relationships

- Contains one or more `Watchlist Entry` records, limited by this feature to exactly one active IPC record.
- Referenced by valid and invalid `Watchlist Sample` files for validation examples.

## Entity: Watchlist Entry

Represents the canonical IPC asset record.

### Fields

- `symbol`: Canonical local symbol. Required; must be `IPC`.
- `display_name`: Human-readable name. Required; must be `S&P/BMV IPC`.
- `market`: Market metadata object. Required.
- `asset_type`: Controlled vocabulary value. Required; must be `index`.
- `currency`: Standard currency code. Required; must be `MXN`.
- `active`: Boolean active status. Required; exactly one entry must be active for this feature.
- `notes`: Optional notes. Must not contain advisory language, live price values, target prices, ratings, or performance forecasts.
- `traceability`: Provenance and review context object. Required.

### Relationships

- Belongs to one `Asset Watchlist`.
- Uses one `Market Metadata` object.
- Uses one `Traceability Context` object.

## Entity: Market Metadata

Describes market context without performing an external lookup.

### Fields

- `venue`: Market venue name or abbreviation. Required; should identify BMV context.
- `country`: Market country or jurisdiction. Required; expected value `MX` or `Mexico` as defined by implementation contract.
- `index_family`: Optional human-readable index family context for IPC.

## Entity: Traceability Context

Explains why and how the IPC entry is included.

### Fields

- `source_reference`: Required reference category or documentation source used for reviewer traceability.
- `review_rationale`: Required non-advisory rationale for inclusion.
- `reviewed_by`: Optional maintainer or role identifier.
- `reviewed_at`: Optional review date.

## Entity: Validation Rule

Defines a stable check that reviewers and validation scripts can apply.

### Initial Rule IDs

- `WL-REQ-001`: Watchlist file must exist at `data/watchlists/asset-watchlist.json`.
- `WL-REQ-002`: Watchlist must include `watchlist_id`, `version`, `effective_date`, `purpose`, and `assets`.
- `WL-REQ-003`: Watchlist must contain exactly one active IPC entry.
- `WL-REQ-004`: IPC entry must use symbol `IPC` and display name `S&P/BMV IPC`.
- `WL-REQ-005`: IPC entry `asset_type` must be `index`.
- `WL-REQ-006`: IPC entry `currency` must be `MXN`.
- `WL-REQ-007`: IPC entry must include market metadata sufficient to identify BMV/Mexico context.
- `WL-REQ-008`: IPC entry must include traceability context.
- `WL-REQ-009`: Watchlist and samples must not include live prices, target prices, ratings, trading signals, recommendations, or performance forecasts.
- `WL-REQ-010`: Invalid watchlist samples must map to at least one rule ID in `docs/validation/sample-rule-mapping.md`.

## Entity: Watchlist Sample

Represents example watchlist data used for local review.

### Fields

- `sample_path`: Repository path to the sample file.
- `classification`: `valid` or `invalid`.
- `violated_rule_ids`: Required for invalid samples; empty or omitted for valid samples.
- `rationale`: Human-readable explanation of why the sample is valid or invalid.

## State Transitions

- `active: true`: The IPC entry is allowed for future monitoring scope.
- `active: false`: The entry is retained for traceability only and is not allowed for future monitoring.
- This feature requires exactly one active IPC entry; additional lifecycle states are deferred.
