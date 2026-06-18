# Market Signal Intelligence Platform

Market Signal Intelligence Platform is a functional market intelligence system for multi-market assets, starting with BMV (Mexican Stock Exchange) and designed to extend to other governed markets.

## Purpose

The platform provides traceable, reproducible foundations for market data ingestion, event contracts, analysis workflows, and user-facing intelligence. This repository establishes the baseline documentation, governance, contracts, validation artifacts, and first controlled source adapter needed before runtime features are layered on top.

## Scope

This foundation includes:

- Repository purpose, scope, methodology, and governance.
- Agent and contributor guidance.
- Initial architecture documentation.
- Allowed sources policy for financial and macroeconomic data.
- Base `AssetEvent` JSON Schema contract.
- Valid and invalid `AssetEvent` samples.
- Initial equity-primary asset watchlist for BMV, designed for multi-market extension.
- Asset watchlist JSON Schema contract and samples.
- Local raw and normalized market snapshot contracts and samples.
- First controlled market source adapter boundary with deterministic fixtures and local validation.
- Lightweight local validation guidance.
- Documentation-first repository structure.

## Architecture Direction

The platform is multi-market by design. BMV is the first governed market; the adapter boundary, watchlist contracts, and snapshot pipeline do not hard-code BMV-only assumptions. Future governed markets are added through watchlist and source-policy extensions, not architectural rewrites.

## Non-Goals

This foundation phase does not implement:

- Live data ingestion or production scheduling.
- Kafka or event broker topology.
- AWS infrastructure or deployment automation.
- AI analysis, RAG, or autonomous agents.
- Dashboard runtime code.
- Trading execution, portfolio management, or personalized recommendations.

These are deferred to later phases where each is justified by a validated use case and built on top of the contracts and validation baseline established here.

## Planned Stack

Backend APIs and data workflows use Python with FastAPI. Dashboard and user-facing web interface uses Next.js. Event streaming, cloud deployment, and AI analysis are introduced incrementally as the pipeline baseline supports them.

## Methodology

Development follows specification-driven delivery:

1. Define scope and constraints in `specs/`.
2. Clarify ambiguity before planning.
3. Plan architecture and contracts before implementation.
4. Generate tasks by independently testable user story.
5. Validate artifacts locally and document PR evidence.

## Current Foundation Artifacts

- `AGENTS.md`
- `docs/foundation/artifact-manifest.md`
- `docs/architecture/foundation-architecture.md`
- `docs/policies/allowed-sources.md`
- `contracts/events/asset-event.schema.json`
- `data/samples/asset-events/valid/`
- `data/samples/asset-events/invalid/`
- `docs/validation/event-contract-validation.md`
- `data/watchlists/asset-watchlist.json`
- `contracts/watchlists/asset-watchlist.schema.json`
- `data/samples/watchlists/valid/`
- `data/samples/watchlists/invalid/`
- `docs/validation/asset-watchlist-validation.md`
- `scripts/validation/check-asset-watchlist.sh`
- `contracts/market-snapshots/raw-market-snapshot.schema.json`
- `contracts/market-snapshots/normalized-market-snapshot.schema.json`
- `data/samples/market-snapshots/raw/valid/`
- `data/samples/market-snapshots/raw/invalid/`
- `data/samples/market-snapshots/normalized/valid/`
- `data/samples/market-snapshots/normalized/invalid/`
- `docs/validation/market-snapshot-validation.md`
- `scripts/validation/check-market-snapshots.sh`
- `src/market_signal_intelligence/sources/`
- `tests/fixtures/market-source-adapter/`
- `data/samples/market-source-adapter/`
- `docs/sources/market-source-adapter.md`
- `docs/validation/market-source-adapter-validation.md`
- `scripts/validation/check-market-source-adapter.sh`

## Asset Watchlist

The initial watchlist defines individual BMV equity tickers allowed for monitoring. `S&P/BMV IPC` may appear only as a reference benchmark entry, not as a replacement for the equity monitoring targets. The watchlist schema supports multi-market extension: future markets are added through governed watchlist entries with their own venue and currency metadata, not through schema changes.

## Local Market Snapshots

Local market snapshot artifacts provide static raw and normalized examples for ingestion planning. Valid snapshots must use active canonical watchlist symbols, include `last_price`, `currency`, and `volume`, and preserve raw-to-normalized provenance through `raw_snapshot_id`.

## Market Source Adapter

The first market source adapter defines a controlled HTTP boundary for one snapshot request at a time. It accepts active canonical watchlist symbols, preserves source evidence, adapts successful responses to the existing raw snapshot shape, and reuses existing snapshot validation. The adapter is BMV-first but not BMV-only: current acceptance is governed by active watchlist membership, and the boundary does not hard-code exchange exclusivity.
