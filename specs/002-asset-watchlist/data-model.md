# Data Model: Initial Asset Watchlist

## Entity: Asset Watchlist

Represents the versioned local allowlist of assets later ingestion features may monitor.

### Fields

- `watchlist_id`: Stable identifier for the watchlist. Required; expected value `asset-watchlist`.
- `version`: Version identifier for the watchlist content. Required; must change when governed content changes.
- `effective_date`: Date when the watchlist version becomes the active review baseline. Required; ISO date.
- `purpose`: Human-readable statement that the file is an allowlist for future monitoring scope. Required; must remain non-advisory.
- `assets`: Collection of watchlist entries. Required; 5-15 entries with at least 5 active equity monitoring targets.

### Relationships

- Contains multiple `Watchlist Entry` records.
- Referenced by valid and invalid `Watchlist Sample` files for validation examples.

## Entity: Watchlist Entry

Represents an individual Mexican equity monitoring target or optional benchmark entry.

### Fields

- `symbol`: Canonical local symbol. Required; must be unique within the watchlist.
- `display_name`: Human-readable name. Required.
- `market`: Market metadata object. Required.
- `asset_type`: Controlled vocabulary value. Required; `equity` for monitoring targets, `index` only for optional IPC benchmark.
- `asset_role`: Controlled role value. Required; `monitoring_target` or `reference_benchmark`.
- `currency`: Standard currency code. Required; must be `MXN`.
- `active`: Boolean active status. Required.
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
- `country`: Market country or jurisdiction. Required; expected value `MX` or equivalent Mexico label defined by the contract.
- `exchange_symbol`: Optional exchange-specific identifier when different from local canonical symbol, such as `WALMEX*`.
- `index_membership`: Optional context indicating selection from a well-known S&P/BMV IPC constituent reference universe.
- `index_family`: Optional human-readable index family context for benchmark entries.

## Entity: Traceability Context

Explains why and how the entry is included.

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
- `WL-REQ-003`: Watchlist must include at least five active equity entries with `asset_role` set to `monitoring_target`.
- `WL-REQ-004`: Watchlist entry symbols must be non-empty, unique, canonical local identifiers.
- `WL-REQ-005`: Primary monitoring targets must use `asset_type` `equity`; `index` is allowed only for `IPC` as `reference_benchmark`.
- `WL-REQ-006`: Watchlist entries must use currency `MXN`.
- `WL-REQ-007`: Watchlist entries must include market metadata sufficient to identify BMV/Mexico context.
- `WL-REQ-008`: Watchlist entries must include traceability context.
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

- `active: true` and `asset_role: monitoring_target`: The equity is allowed for future monitoring scope.
- `active: true` and `asset_role: reference_benchmark`: The index is allowed only as benchmark/reference context.
- `active: false`: The entry is retained for traceability only and is not allowed for future monitoring.
- Additional lifecycle states are deferred.
