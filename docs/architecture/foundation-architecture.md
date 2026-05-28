# Foundation Architecture

## Purpose

Describe the initial repository architecture needed before runtime platform features are implemented.

## Conceptual Boundaries

- **Documentation boundary**: project scope, methodology, source rules, and review guidance.
- **Contract boundary**: `AssetEvent` schema and sample payloads.
- **Watchlist boundary**: equity-primary asset allowlist contract and sample payloads for future monitoring scope.
- **Validation boundary**: local checks and PR evidence for contracts and samples.
- **Future runtime boundary**: backend, dashboard, ingestion, event streaming, cloud, and AI features remain deferred.

## Data Flow

In this phase, data flow is conceptual only:

1. Future source data is governed by `docs/policies/allowed-sources.md`.
2. Future monitored assets must be allowed by `data/watchlists/asset-watchlist.json`.
3. Future events must conform to `contracts/events/asset-event.schema.json`.
4. Sample events and watchlists document expected valid and invalid shapes.
5. Local validation confirms contract and sample consistency.

## Repository Areas

- `docs/`: architecture, policy, foundation, and validation documentation.
- `contracts/`: event and watchlist contract definitions.
- `data/samples/`: non-production sample payloads.
- `data/watchlists/`: versioned repository-local watchlist artifacts.
- `specs/`: specification-driven development artifacts.
- `scripts/validation/`: local validation helper scripts only.

## Deferred Components

The following remain out of scope for this feature: ingestion jobs, Kafka, AWS, AI analysis, RAG, autonomous agents, dashboard runtime, and deployment automation.
