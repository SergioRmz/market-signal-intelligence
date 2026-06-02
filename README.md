# BMV Signal Intelligence Platform

BMV Signal Intelligence Platform is an educational and technical market intelligence project focused on Mexican equities and related macroeconomic context.

## Purpose

The platform will provide traceable, reproducible foundations for future market data ingestion, event contracts, analysis workflows, and user-facing intelligence. This repository phase establishes the baseline documentation, governance, contracts, and validation artifacts needed before runtime features are implemented.

## Scope

This foundation feature includes:

- Repository purpose, scope, non-goals, and methodology.
- Agent and contributor guidance.
- Initial architecture documentation.
- Allowed sources policy for financial and macroeconomic data.
- Base `AssetEvent` JSON Schema contract.
- Valid and invalid `AssetEvent` samples.
- Initial equity-primary asset watchlist for allowed future monitoring scope.
- Asset watchlist JSON Schema contract and samples.
- Local raw and normalized market snapshot contracts and samples.
- First controlled market source adapter boundary with deterministic fixtures and local validation.
- Lightweight local validation guidance.
- Documentation-first repository structure.

## Non-Goals

This feature does not implement:

- Data ingestion logic.
- Production market data ingestion, scheduling, or bulk harvesting.
- Kafka or event broker topology.
- AWS infrastructure or deployment automation.
- AI analysis, RAG, autonomous agents, or prompt orchestration.
- Dashboard runtime code.
- Trading, portfolio, or recommendation functionality.

## Disclaimer

This project is for educational and technical market intelligence purposes only. It does not provide investment advice, portfolio allocation guidance, or buy/sell/hold recommendations.

## Planned Stack

Future backend APIs and data workflows are expected to use Python with FastAPI. Future dashboard work is expected to use Next.js. Event streaming, cloud deployment, and AI analysis are intentionally deferred until deterministic foundations are validated.

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

The initial watchlist defines individual Mexican equity tickers allowed for future monitoring. `S&P/BMV IPC` may appear only as a reference benchmark entry, not as a replacement for the equity monitoring targets. The watchlist is a scope-control artifact and does not include live prices, rankings, recommendations, or trading signals.

## Local Market Snapshots

Local market snapshot artifacts provide static raw and normalized examples for future ingestion planning. Valid snapshots must use active canonical watchlist symbols, include `last_price`, `currency`, and `volume`, and preserve raw-to-normalized provenance through `raw_snapshot_id`. These artifacts are sample data only and do not fetch live prices, call external APIs, scrape websites, stream events, store data in a database, expose service endpoints, or perform AI analysis.

## Market Source Adapter

The first market source adapter defines a narrow controlled HTTP boundary for one snapshot request at a time. It is BMV-first but not BMV-only, accepts only active canonical watchlist symbols, preserves non-secret source evidence, adapts successful responses to the existing raw snapshot shape, and reuses existing snapshot validation. It does not add production ingestion, schedulers, service endpoints, persistence, multiple providers, scraping, advisory outputs, or normalized provider-specific schemas.
