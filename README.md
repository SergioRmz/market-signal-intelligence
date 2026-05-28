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
- Lightweight local validation guidance.
- Documentation-first repository structure.

## Non-Goals

This feature does not implement:

- Data ingestion logic.
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
