# Research: Initial Asset Watchlist

## Decision: IPC-Only Initial Scope

**Decision**: The initial watchlist contains exactly one active entry for symbol `IPC`, display name `S&P/BMV IPC`.

**Rationale**: A single IPC entry satisfies the clarified scope, minimizes ambiguity, and creates a stable allowlist boundary before any ingestion implementation. It prevents accidental expansion into individual equities, ETFs, FIBRAs, or broad index universes.

**Alternatives considered**: A multi-asset BMV list was rejected because it expands scope beyond the user's clarified first vertical. Vendor-specific symbols such as `^MXX` or `MEXBOL` were rejected as canonical local identifiers because they can imply dependency on a specific external data provider.

## Decision: JSON Watchlist Artifact

**Decision**: Store the local watchlist at `data/watchlists/asset-watchlist.json`.

**Rationale**: JSON is simple, deterministic, reviewable, and directly consumable by future ingestion services without introducing runtime behavior. The path separates governed data artifacts from documentation and feature planning outputs.

**Alternatives considered**: Markdown was rejected because it is less suitable for future machine validation. A root `contracts/` path was deferred because this feature creates a local allowlist artifact, while the design schema remains in `specs/002-asset-watchlist/contracts/` until implementation planning promotes a repository-wide contract.

## Decision: Design Contract Uses JSON Schema Draft 2020-12

**Decision**: Define the planning contract as `specs/002-asset-watchlist/contracts/asset-watchlist.schema.json` using JSON Schema Draft 2020-12.

**Rationale**: The foundation feature already uses JSON Schema Draft 2020-12 for event contracts, so this keeps validation conventions consistent while remaining documentation/data-contract-only.

**Alternatives considered**: Informal prose-only validation was rejected because it weakens contract-first collaboration. A database schema was rejected because the feature explicitly forbids database implementation.

## Decision: IPC Currency Code Is MXN

**Decision**: The IPC entry uses currency code `MXN`, with notes allowed to clarify that index observations are expressed in points.

**Rationale**: The spec requires a standard currency code and the IPC is tied to the Mexican market context. Distinguishing currency metadata from future observation units avoids using non-standard or omitted currency values.

**Alternatives considered**: `XXX` and omitted currency were rejected because they would complicate validation and conflict with the required currency field.

## Decision: Validation Remains Local and Non-Networked

**Decision**: Validation rules, rule IDs, samples, and optional shell checks run locally without deployed services, APIs, scraping, or live market data.

**Rationale**: This satisfies reproducibility, foundation-first delivery, and the explicit no-runtime constraints. It also lets reviewers verify validity from a clean clone.

**Alternatives considered**: External lookup validation and live data confirmation were rejected because they violate the feature's prohibition on external APIs, scraping, and live price behavior.
