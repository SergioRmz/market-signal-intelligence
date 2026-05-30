# Research: Initial Asset Watchlist

## Decision: Equity-Primary Initial Scope

**Decision**: The initial watchlist contains individual Mexican equity monitoring targets selected from well-known S&P/BMV IPC constituent reference context where identifiers are clear. `S&P/BMV IPC` may appear only as a benchmark entry with `asset_type` `index` and `asset_role` `reference_benchmark`.

**Rationale**: The feature is intended to govern future monitoring of specific market assets/tickers, not just the benchmark index. Equity-first scope gives ingestion features actionable symbols while keeping the benchmark available for context.

**Alternatives considered**: IPC-only scope was rejected because it replaces the individual asset allowlist with a benchmark. A broad BMV universe was rejected because it expands beyond a small, explicit initial list.

## Decision: JSON Watchlist Artifact

**Decision**: Store the local watchlist at `data/watchlists/asset-watchlist.json`.

**Rationale**: JSON is simple, deterministic, reviewable, and directly consumable by future ingestion services without introducing runtime behavior. The path separates governed data artifacts from documentation and feature planning outputs.

**Alternatives considered**: Markdown was rejected because it is less suitable for future machine validation. A database schema was rejected because the feature explicitly forbids database implementation.

## Decision: Design Contract Uses JSON Schema Draft 2020-12

**Decision**: Define the planning contract as `specs/002-asset-watchlist/contracts/asset-watchlist.schema.json` and the root contract as `contracts/watchlists/asset-watchlist.schema.json` using JSON Schema Draft 2020-12.

**Rationale**: The foundation feature already uses JSON Schema Draft 2020-12 for event contracts, so this keeps validation conventions consistent while remaining documentation/data-contract-only.

**Alternatives considered**: Informal prose-only validation was rejected because it weakens contract-first collaboration.

## Decision: Currency Code Is MXN

**Decision**: All watchlist entries use currency code `MXN`, with notes allowed to clarify that index benchmark observations are expressed in points.

**Rationale**: The watchlist is for Mexican market assets, and a required standard currency code keeps future ingestion contracts deterministic.

**Alternatives considered**: `XXX` and omitted currency were rejected because they would complicate validation and conflict with the required currency field.

## Decision: Validation Remains Local and Non-Networked

**Decision**: Validation rules, rule IDs, samples, and optional shell checks run locally without deployed services, APIs, scraping, or live market data.

**Rationale**: This satisfies reproducibility, foundation-first delivery, and the explicit no-runtime constraints. It also lets reviewers verify validity from a clean clone.

**Alternatives considered**: External lookup validation and live data confirmation were rejected because they violate the feature's prohibition on external APIs, scraping, and live price behavior.
