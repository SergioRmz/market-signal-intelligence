# Contract: Market Source Adapter Boundary

## Purpose

Define the stable boundary between unstable controlled HTTP market source responses and the platform's existing raw market snapshot contract.

## Inputs

- `requested_symbol`: one candidate ticker symbol.
- `source_configuration`: non-secret local configuration for one controlled HTTP endpoint.
- `timeout_seconds`: optional configured timeout; defaults to `5`.
- `credential_reference`: optional local environment configuration reference when the controlled endpoint requires credentials.

## Preconditions

- `requested_symbol` must be checked against `data/watchlists/asset-watchlist.json`.
- Accepted symbols must be canonical and active.
- The adapter must use exactly one configured controlled HTTP endpoint in this feature.
- Missing required credentials must fail as configuration failure before an accepted raw snapshot can be produced.

## Accepted Output

When a fetch succeeds, the boundary returns an adapter fetch result with:

- `outcome`: `accepted`.
- Preserved `raw_source_payload`.
- Preserved `source_metadata`.
- `adapted_raw_snapshot` in the existing `contracts/market-snapshots/raw-market-snapshot.schema.json` shape.

The adapted raw market snapshot is the primary output of this feature.

## Failed Output

When a fetch fails, the boundary returns an adapter fetch result with:

- `outcome`: `failed`.
- `failure_class`: one of the documented failure classes.
- `failure_message`: non-secret diagnostic summary.
- `source_metadata` when available.
- `raw_source_payload` when a response was received.
- No accepted `adapted_raw_snapshot`.

## Failure Classes

- `timeout`
- `rate_limited`
- `ticker_not_found`
- `invalid_response_shape`
- `unsupported_ticker`
- `inactive_ticker`
- `configuration_failure`

## Compatibility Requirements

- Existing raw market snapshot schema remains unchanged.
- Existing normalized market snapshot schema remains unchanged.
- Existing 003 validation/normalization flow owns normalization.
- The adapter must not define provider-specific normalized schemas.
- The adapter must not duplicate normalization logic.

## Scope Guardrails

- No Kafka producers or consumers.
- No FastAPI endpoints.
- No database persistence.
- No AWS or cloud resources.
- No dashboard behavior.
- No AI analysis.
- No production scheduler.
- No multiple providers.
- No aggressive scraping.
- No trading signals, ratings, targets, or investment recommendations.
