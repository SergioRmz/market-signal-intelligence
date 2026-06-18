# Market Source Adapter Validation

## Purpose

Validate the first controlled market source adapter with deterministic local artifacts. The adapter accepts one active canonical watchlist symbol, preserves source evidence, adapts successful responses to the existing raw market snapshot shape, and classifies expected failures without adding production ingestion behavior.

## Local Commands

Run from repository root:

```bash
scripts/validation/check-market-source-adapter.sh
```

Expected completion output includes:

```text
PASS: Market source adapter artifacts validated
```

The script also calls existing market snapshot validation:

```bash
scripts/validation/check-market-snapshots.sh
```

## Rule IDs

- `MSA-REQ-001`: Required adapter artifacts exist and are traceable.
- `MSA-REQ-002`: Exactly one controlled HTTP source implementation is present.
- `MSA-REQ-003`: Timeout defaults to 5 seconds and remains configurable.
- `MSA-REQ-004`: Accepted fetches use active canonical watchlist symbols.
- `MSA-REQ-005`: Source payload and metadata are preserved.
- `MSA-REQ-006`: Accepted output uses the existing raw snapshot shape.
- `MSA-REQ-007`: Existing snapshot validation is reused; no provider-specific normalized schema is added.
- `MSA-REQ-008`: Timeout failures produce no accepted raw snapshot.
- `MSA-REQ-009`: Source response failures are classified and preserve response evidence when available.
- `MSA-REQ-010`: Watchlist and configuration failures produce no accepted raw snapshot.
- `MSA-REQ-011`: Credentials, tokens, and secrets are not committed.
- `MSA-REQ-012`: Content remains functional and technical, without signals, ratings, targets, or forecasts.

## Evidence Format

Pull request evidence should include:

- `python3 -m unittest discover tests` result.
- `scripts/validation/check-market-source-adapter.sh` result.
- `scripts/validation/check-market-snapshots.sh` result.
- Successful adapter fixture count.
- Failure evidence count by class.
- Confirmation that the accepted adapter raw snapshot uses an active canonical watchlist symbol.
- Confirmation that source metadata and raw payload evidence are preserved.
- Confirmation that no provider-specific normalized schema was added.

## Credential Handling

Credentials are optional and local-only. If a controlled endpoint requires credentials, configure only the environment variable name in `MSA_CREDENTIAL_ENV_VAR` and provide the credential value outside the repository. Missing credential values must classify as `configuration_failure` and must not produce an accepted raw snapshot.

## Guardrails

The adapter is BMV-first but not BMV-only: current acceptance is governed by active watchlist membership, not by hard-coded exchange exclusivity. The primary successful output is an adapted raw market snapshot; normalization remains owned by the existing 003 market snapshot pipeline.

This validation must not require Kafka, FastAPI endpoints, database persistence, AWS resources, dashboards, AI analysis, schedulers, multiple providers, scraping, or advisory outputs.
