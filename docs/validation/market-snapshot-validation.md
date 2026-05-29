# Market Snapshot Validation

## Purpose

Define local validation rules and review evidence for raw and normalized market snapshot artifacts. This feature uses static repository samples only and validates assets against `data/watchlists/asset-watchlist.json`.

## Local Commands

Run from the repository root:

```bash
scripts/validation/check-market-snapshots.sh
```

The command validates snapshot contracts, raw samples, normalized samples, active watchlist membership, invalid sample mappings, and non-advisory scope guardrails without network access or deployed services.

## Rule IDs

- `MS-REQ-001`: Raw and normalized snapshot contracts must exist and be documented.
- `MS-REQ-002`: Raw snapshots must include required identity, source, asset, timestamp, observed values, and provenance fields.
- `MS-REQ-003`: Normalized snapshots must include required identity, `raw_snapshot_id`, asset, timestamp, observed values, and provenance fields.
- `MS-REQ-004`: Snapshot `asset.symbol` must match a canonical active symbol in `data/watchlists/asset-watchlist.json`.
- `MS-REQ-005`: `S&P/BMV IPC` is optional benchmark context only and must not count toward equity snapshot coverage.
- `MS-REQ-006`: Snapshot observed values must include `last_price`, `currency`, and `volume`.
- `MS-REQ-007`: Normalized snapshots must reference an existing valid raw snapshot by `raw_snapshot_id`.
- `MS-REQ-008`: Invalid samples must map to at least one `MS-REQ-*` rule ID in `docs/validation/sample-rule-mapping.md`.
- `MS-REQ-009`: Snapshot artifacts must not include live-feed behavior, advisory language, target prices, ratings, rankings, recommendations, or performance forecasts.
- `MS-REQ-010`: Snapshot validation must be reproducible locally without network access or deployed services.

## Raw Snapshot Review

Reviewers must confirm valid raw samples under `data/samples/market-snapshots/raw/valid/` satisfy these checks:

- Each file is valid JSON.
- Each sample includes `raw_snapshot_id`, `schema_version`, `source`, `asset`, `observed_at`, `observed_values`, and `provenance`.
- `source.category` is `local_sample`.
- `asset.symbol` is the canonical symbol from `data/watchlists/asset-watchlist.json`.
- The watchlist entry for `asset.symbol` exists and has `active` set to true.
- `observed_values` includes `last_price`, `currency`, and `volume`.
- `currency` is `MXN`.
- No sample includes advisory language, target prices, ratings, rankings, live-feed metadata, or runtime integration behavior.

## Normalized Snapshot Review

Reviewers must confirm valid normalized samples under `data/samples/market-snapshots/normalized/valid/` satisfy these checks:

- Each file is valid JSON.
- Each sample includes `normalized_snapshot_id`, `schema_version`, `raw_snapshot_id`, `asset`, `observed_at`, `normalized_at`, `observed_values`, and `provenance`.
- `raw_snapshot_id` matches a valid raw sample.
- `provenance.source_raw_snapshot_id` matches `raw_snapshot_id`.
- `asset.symbol` remains the canonical watchlist symbol.
- `observed_values` includes `last_price`, `currency`, and `volume`.
- Raw and normalized samples remain separate files.

## Benchmark Review

`S&P/BMV IPC` may appear only as optional benchmark context. It must use canonical symbol `IPC`, role `reference_benchmark`, and must not count toward required individual equity snapshot coverage.

## Sample Expectations

- Valid raw samples must include at least two active equity examples.
- Valid normalized samples must include at least two active equity examples linked to valid raw samples by `raw_snapshot_id`.
- Invalid samples must separately cover missing watchlist asset, inactive watchlist asset, malformed required fields, missing raw provenance, exchange symbol variant, and prohibited content.
- Every invalid sample must be listed in `docs/validation/sample-rule-mapping.md` with at least one `MS-REQ-*` rule ID.

## Non-Advisory Content Scan

The local validation script rejects valid samples when it finds prohibited terms or fields associated with live feeds, target prices, ratings, rankings, trading signals, recommendations, portfolio allocation, or performance forecasts.

Reviewers must also confirm that static sample values are educational and technical examples only. They are not live prices, advice, signals, ratings, rankings, or performance forecasts.

## Scope Guardrail Checklist

Before approving snapshot changes, reviewers must confirm this feature introduced none of the following:

- External API calls.
- Website scraping.
- Kafka producers or streaming topology.
- Database schemas, migrations, connections, or persistence code.
- FastAPI endpoints or service runtime behavior.
- AWS or cloud automation.
- Dashboard code.
- AI analysis, RAG workflows, or autonomous agents.
- Live market data fetching or live-feed metadata in valid samples.

Allowed changes are limited to documentation, contracts, sample data, validation guidance, repository-local artifacts, and local validation scripting.

## Evidence Format

Pull requests must include:

- Command executed.
- Pass/fail result.
- Valid raw snapshot sample count.
- Valid normalized snapshot sample count.
- Invalid snapshot sample count.
- Active watchlist symbol checks performed.
- Invalid sample to violated `MS-REQ-*` rule ID mapping.
- Confirmation that normalized samples reference valid raw samples by `raw_snapshot_id`.
- Confirmation that `S&P/BMV IPC` is benchmark context only when present.
- Confirmation that no runtime ingestion, external API, scraping, Kafka, database, FastAPI, AWS, dashboard, AI, or live-feed behavior was introduced.
- Confirmation that `README.md` and `AGENTS.md` were updated if needed or explicitly reviewed as not needing changes.

## Failure Handling

- Missing contract or sample path: create the missing artifact or update the governing spec and tasks.
- Invalid JSON: fix the sample or contract file.
- Missing or inactive watchlist symbol: update the sample to use an active canonical symbol or update the watchlist through review.
- Missing observed values: include `last_price`, `currency`, and `volume`.
- Missing raw provenance: add a `raw_snapshot_id` that matches a valid raw sample.
- Invalid sample without rule mapping: update `docs/validation/sample-rule-mapping.md`.
- Advisory or live-feed content in valid samples: remove prohibited fields or move the example to invalid samples with rule mapping.

## Guardrails

- Validation must not fetch live prices, scrape websites, call external APIs, connect to databases, create service endpoints, produce streaming events, run dashboard code, or invoke AI analysis.
- Snapshot artifacts are educational and technical sample data only; they are not investment advice, trading signals, ratings, rankings, recommendations, or forecasts.
