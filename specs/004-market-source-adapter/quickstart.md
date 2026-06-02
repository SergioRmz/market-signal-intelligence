# Quickstart: Market Source Adapter

## Purpose

Validate the first controlled market source adapter from a clean checkout without production services, databases, Kafka, AWS, dashboard code, AI tools, schedulers, multiple providers, or aggressive scraping.

## Prerequisites

- Repository checkout on branch `004-market-source-adapter`.
- Python 3.12 available on the developer workstation; planning was validated locally with Python 3.12.3.
- Bash 5.2+ available for repository-local validation scripts; planning was validated locally with GNU Bash 5.2.21.
- jq 1.7 available for JSON validation in existing shell scripts; planning was validated locally with jq 1.7.
- Optional local environment variables only if the controlled endpoint scenario requires credentials.

## Expected Artifacts After Implementation

- `src/market_signal_intelligence/sources/` contains the adapter boundary and controlled HTTP implementation.
- `tests/unit/`, `tests/integration/`, and `tests/contract/` cover success paths, failure classes, contract boundaries, documentation guardrails, and snapshot compatibility.
- `tests/fixtures/market-source-adapter/` contains deterministic provider responses.
- `data/samples/market-source-adapter/` contains preserved payload, adapted raw snapshot, and failure evidence samples.
- `docs/sources/market-source-adapter.md` documents source limitations and usage constraints.
- `docs/validation/market-source-adapter-validation.md` documents local evidence and failure handling.
- `scripts/validation/check-market-source-adapter.sh` validates adapter artifacts and reuses existing snapshot validation.

## Local Validation Flow

Run from repository root:

```bash
scripts/validation/check-market-source-adapter.sh
```

The adapter validation must confirm:

- Active canonical watchlist symbols are accepted only when source response shape is valid.
- Unsupported and inactive tickers are rejected without accepted raw snapshots.
- Timeout uses the 5-second default unless a scenario documents a configured timeout.
- Rate-limited, ticker-not-found, invalid-shape, and missing-credential scenarios fail with documented classifications.
- Raw source payload and source metadata are preserved when a response is received.
- Credentials are never committed or printed in evidence.
- Adapted raw snapshots pass existing raw market snapshot validation.
- Existing 003 normalization flow is reused when normalized artifacts already exist.
- No provider-specific normalized schema or duplicate normalization logic is introduced.

Then run existing snapshot validation:

```bash
scripts/validation/check-market-snapshots.sh
```

## Evidence Format

Pull request evidence should include:

- Commands executed.
- Pass/fail result for adapter validation.
- Pass/fail result for existing market snapshot validation.
- Successful fetch fixture count.
- Failure fixture count by class.
- Confirmation that accepted raw snapshots use active canonical watchlist symbols.
- Confirmation that source metadata and raw provider payload are preserved.
- Confirmation that timeout default is 5 seconds and configurable.
- Confirmation that missing credentials fail safely without exposing secrets.
- Confirmation that no provider-specific normalized schema or duplicate normalization logic was added.
- Confirmation that `README.md` and `AGENTS.md` were updated if needed or explicitly reviewed as not needing changes.

## Scope Guardrails

This feature must not add:

- Kafka producers or consumers.
- FastAPI endpoints.
- Database persistence.
- AWS or cloud resources.
- Dashboard work.
- AI analysis, RAG workflows, or autonomous agents.
- Trading signals, ratings, targets, recommendations, or forecasts.
- Multiple source providers.
- Production scheduler.
- Aggressive scraping.

## README And AGENTS Review

`README.md` was updated with the adapter artifact paths and a concise market source adapter section because this feature adds a limited repository-local adapter boundary. `AGENTS.md` was updated to clarify that feature 004 authorizes only the controlled adapter boundary, not production ingestion services, schedulers, persistence, service endpoints, multiple providers, or cloud resources.

## Validation Evidence

Final local validation from repository root:

```bash
python3 -m unittest discover tests
```

Observed result: `Ran 18 tests` and `OK`.

```bash
scripts/validation/check-market-source-adapter.sh
```

Observed result: `PASS: Market source adapter artifacts validated`.

```bash
scripts/validation/check-market-snapshots.sh
```

Observed result: `PASS: Local market snapshot contracts and samples validated`.

```bash
scripts/validation/check-foundation-artifacts.sh
```

Observed result: `PASS foundation artifacts and samples validated`.

## Scope Review Result

Completion review confirms this feature added no Kafka topology, FastAPI endpoints, database persistence, AWS resources, dashboard behavior, AI analysis, RAG workflows, autonomous agents, production scheduler, bulk ingestion, aggressive scraping, multiple providers, trading signals, ratings, rankings, target prices, recommendations, or performance forecasts.

## Expected Completion Signal

Implementation is complete when adapter tests pass, adapter validation passes, existing market snapshot validation passes, task checkboxes are updated, and the validation evidence above is included in review notes.
