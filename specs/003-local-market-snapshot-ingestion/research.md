# Research: Local Market Snapshot Ingestion

## Decision: Local Sample-Only Ingestion Baseline

**Decision**: Represent ingestion readiness through static repository sample files, documentation, contracts, and local validation guidance only.

**Rationale**: The feature's purpose is to establish deterministic inputs and validation expectations before any live or external market data behavior exists. Static samples keep the workflow reproducible from a clean clone and satisfy the foundation-first constraint.

**Alternatives considered**: External API pulls, scraping, Kafka messages, service endpoints, databases, and cloud storage were rejected because they are explicitly out of scope.

## Decision: Separate Raw and Normalized Snapshot Contracts

**Decision**: Define separate raw and normalized market snapshot planning contracts under `specs/003-local-market-snapshot-ingestion/contracts/`, with implementation tasks expected to promote stable root contracts under `contracts/market-snapshots/`.

**Rationale**: Raw snapshots preserve source-shaped observations, while normalized snapshots provide a canonical watchlist-aligned representation for future consumers. Separate contracts prevent accidental overwrites and make provenance review explicit.

**Alternatives considered**: A single combined snapshot contract was rejected because it blurs source preservation with normalized output. Prose-only contracts were rejected because they weaken contract-first review.

## Decision: Active Watchlist Gate

**Decision**: Valid raw and normalized samples must reference canonical symbols that exist in `data/watchlists/asset-watchlist.json` and have `active` set to true.

**Rationale**: The watchlist is the governed allowlist for future monitoring scope. Gating snapshot eligibility on active entries prevents accidental expansion to unreviewed or retired assets.

**Alternatives considered**: Accepting any BMV-looking symbol was rejected because it bypasses the watchlist. Allowing inactive entries was rejected because inactive status means retained for traceability only.

## Decision: Canonical Symbols Only

**Decision**: Raw and normalized samples must use the canonical watchlist `symbol`; exchange symbol variants are invalid in this baseline.

**Rationale**: Canonical-only symbols keep local validation deterministic and avoid requiring external lookup, alias resolution, or source-specific mapping logic.

**Alternatives considered**: Allowing `market.exchange_symbol` variants was rejected because it introduces normalization decisions better deferred until runtime ingestion is authorized.

## Decision: Optional IPC Benchmark Context

**Decision**: Active `S&P/BMV IPC` snapshots may be accepted only as optional benchmark context and do not count toward required equity snapshot coverage.

**Rationale**: This preserves the equity-primary watchlist rule while allowing benchmark samples to demonstrate contextual snapshot handling.

**Alternatives considered**: Rejecting all IPC snapshots was considered but would make benchmark context unavailable. Counting IPC as a monitoring target was rejected because it conflicts with the equity-primary scope.

## Decision: Minimal Observed Value Shape

**Decision**: Valid raw and normalized snapshot samples require `last_price`, `currency`, and `volume`; other market observation fields are optional when static, local, and non-advisory.

**Rationale**: These fields are enough to test basic value normalization while avoiding unnecessary OHLC complexity for a local foundation feature.

**Alternatives considered**: Requiring only `last_price` was rejected as too weak for market snapshot validation. Full OHLCV was rejected as unnecessary scope expansion.

## Decision: `raw_snapshot_id` Provenance Link

**Decision**: Each raw snapshot has a `raw_snapshot_id`, and each normalized snapshot must reference the originating raw sample through `raw_snapshot_id`.

**Rationale**: A stable identifier gives reviewers a simple, testable provenance link without databases, generated IDs, or runtime services.

**Alternatives considered**: Referencing only file paths was rejected because file organization may change. Optional provenance was rejected because traceability is constitution-critical.

## Decision: Invalid Sample Coverage

**Decision**: Invalid samples must separately cover missing watchlist asset, inactive watchlist asset, malformed required fields, and prohibited advisory or live-feed content.

**Rationale**: Separate failures make validation expectations unambiguous and prevent implementations from covering only one watchlist gate.

**Alternatives considered**: Combining missing and inactive cases was rejected because it weakens test coverage of distinct rules.

## Decision: Conditional General Documentation Updates

**Decision**: `README.md` and `AGENTS.md` must be reviewed before completion and updated only if snapshot artifacts introduce project-wide usage, validation, scope, or agent guidance not already covered.

**Rationale**: This keeps global documentation accurate without forcing noisy changes when feature-specific docs are sufficient. The Speckit plan marker in `AGENTS.md` is updated as part of planning context.

**Alternatives considered**: Always updating global docs was rejected because it can create redundant documentation. Never updating them was rejected because project-wide guidance may become stale.
