# Market Source Adapter

## Purpose

The market source adapter is the first controlled boundary for fetching one market snapshot from one configurable HTTP source and adapting accepted responses to the existing raw market snapshot shape.

## Supported Source Mode

This feature supports exactly one controlled HTTP endpoint configured locally. Fixture-backed tests and samples provide deterministic validation without depending on an unstable live source during review.

## BMV-First Scope

The platform is BMV-first but not BMV-only. This adapter currently accepts only active canonical symbols governed by `data/watchlists/asset-watchlist.json`; it does not hard-code a permanent BMV-only boundary that would block future governed market expansion.

## Credential Posture

Credentials are optional and local-only. If needed, the repository may store the environment variable name, but credential values must remain outside committed files. Missing required local credential configuration is classified as `configuration_failure`.

## Preserved Evidence

Each fetch attempt records non-secret source metadata. When a source response is received, the parsed raw source payload is preserved for traceability, including rejected rate-limited, ticker-not-found, and invalid-shape responses.

## Failure Modes

Expected failure classifications are:

- `timeout`
- `rate_limited`
- `ticker_not_found`
- `invalid_response_shape`
- `unsupported_ticker`
- `inactive_ticker`
- `configuration_failure`

Failed attempts do not produce accepted raw market snapshots.

## Exclusions

This adapter does not add Kafka, service endpoints, database persistence, AWS resources, dashboards, AI analysis, schedulers, multiple providers, bulk ingestion, scraping, ratings, rankings, target prices, trading signals, recommendations, or performance forecasts. It is educational and technical only, not investment advice.
