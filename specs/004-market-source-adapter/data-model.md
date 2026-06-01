# Data Model: Market Source Adapter

## Market Source Adapter

Represents the replaceable boundary for requesting one ticker from one configured controlled HTTP source.

**Fields**:

- `source_name`: stable source identifier for provenance.
- `endpoint_base_url`: configured controlled HTTP endpoint location; not committed with secrets.
- `timeout_seconds`: configurable timeout, default `5`.
- `credential_reference`: optional local environment configuration reference; never stores credential values.
- `supported_failure_classes`: controlled set of expected failure classifications.

**Relationships**:

- Produces one `Source Fetch Attempt` per requested ticker.
- Emits an `Adapter-Produced Raw Market Snapshot` only for accepted attempts.
- Depends on the canonical asset watchlist for eligibility.

**Validation Rules**:

- Exactly one source implementation is allowed in this feature.
- Must request one ticker at a time.
- Must not schedule, poll in bulk, scrape aggressively, or add service endpoints.
- Must not hard-code BMV-only assumptions beyond current watchlist-gated acceptance.

## Source Fetch Attempt

Represents one request/response evaluation for a candidate ticker.

**Fields**:

- `attempt_id`: unique identifier for the attempt.
- `requested_symbol`: candidate ticker provided by the caller.
- `canonical_symbol`: active watchlist symbol after eligibility validation, when available.
- `source_name`: source identifier.
- `requested_at`: timestamp when the fetch attempt begins.
- `retrieved_at`: timestamp when a response is received, when available.
- `timeout_seconds`: timeout used for the attempt.
- `response_status`: source response status when available.
- `outcome`: `accepted` or `failed`.
- `failure_class`: one of `timeout`, `rate_limited`, `ticker_not_found`, `invalid_response_shape`, `unsupported_ticker`, `inactive_ticker`, or `configuration_failure` when failed.
- `failure_message`: non-secret diagnostic summary for failed attempts.
- `raw_source_payload`: preserved provider-shaped payload or error body when received.
- `source_metadata`: provenance context for the source interaction.
- `adapted_raw_snapshot`: existing raw market snapshot shape when accepted.

**Relationships**:

- May include one `Raw Source Payload`.
- May include one `Adapter-Produced Raw Market Snapshot`.
- References one watchlist entry only when the ticker is active and canonical.

**Validation Rules**:

- Missing local credentials classify as `configuration_failure`.
- Timeout classifies as `timeout` and produces no accepted raw snapshot.
- Rate-limited source response classifies as `rate_limited` and produces no accepted raw snapshot.
- Unknown source ticker classifies as `ticker_not_found` and preserves response evidence when available.
- Invalid provider response shape classifies as `invalid_response_shape` and preserves response evidence.
- Unsupported or inactive watchlist ticker fails before accepted raw snapshot creation.

## Raw Source Payload

Represents the provider-shaped data returned by the controlled HTTP endpoint.

**Fields**:

- `payload_body`: original parsed response body or retained error payload.
- `content_type`: response content type when available.
- `received_status`: response status code or source status when available.
- `captured_at`: timestamp when the payload was captured.

**Validation Rules**:

- Must be preserved for every received source response, including rejected source-shape and ticker-not-found responses.
- Must not contain committed credentials or secrets.
- Must not include advisory language, ratings, targets, recommendations, or trading signals in accepted scenarios.

## Source Metadata

Represents audit context for the source interaction.

**Fields**:

- `source_name`: source identifier.
- `requested_symbol`: requested ticker.
- `endpoint_label`: non-secret endpoint descriptor.
- `retrieved_at`: response retrieval timestamp when available.
- `response_status`: source status when available.
- `classification`: accepted or failure classification.
- `attribution`: source attribution or usage note when applicable.

**Validation Rules**:

- Must be present for every attempted fetch.
- Must not expose credentials.
- Must provide enough context to reproduce acceptance or rejection decisions from fixtures.

## Adapter-Produced Raw Market Snapshot

Represents the accepted internal raw snapshot produced from a valid source response.

**Fields**:

- Existing fields from `contracts/market-snapshots/raw-market-snapshot.schema.json`.
- `source` fields identify the adapter/source context without changing the raw snapshot contract.
- `asset.symbol` uses the active canonical watchlist symbol.
- `observed_values` includes `last_price`, `currency`, and `volume`.
- `provenance` links back to the source fetch attempt and source payload evidence.

**Validation Rules**:

- Must pass existing raw market snapshot validation.
- Must be the primary output of a successful adapter fetch.
- Must prove compatibility with existing 003 normalization flow when normalized artifacts already exist.
- Must not create or require a provider-specific normalized schema.

## Fetch Failure Classification

Controlled vocabulary for failed attempts.

**Values**:

- `timeout`
- `rate_limited`
- `ticker_not_found`
- `invalid_response_shape`
- `unsupported_ticker`
- `inactive_ticker`
- `configuration_failure`

**State Transitions**:

1. `requested` → `watchlist_rejected` for unsupported or inactive tickers.
2. `requested` → `configuration_failed` for missing required local configuration or credentials.
3. `requested` → `source_failed` for timeout, rate limit, ticker not found, or invalid response shape.
4. `requested` → `accepted` only after active watchlist validation, valid source shape, required observed values, source metadata preservation, and raw snapshot validation.
