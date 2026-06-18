# Quickstart: Local Market Snapshot Ingestion

## Purpose

Provide a local review path for raw and normalized market snapshot artifacts. This feature uses static sample files only and validates that snapshot assets exist as active canonical entries in `data/watchlists/asset-watchlist.json`.

## Expected Artifacts After Implementation

- `contracts/market-snapshots/raw-market-snapshot.schema.json`
- `contracts/market-snapshots/normalized-market-snapshot.schema.json`
- `data/samples/market-snapshots/raw/valid/`
- `data/samples/market-snapshots/raw/invalid/`
- `data/samples/market-snapshots/normalized/valid/`
- `data/samples/market-snapshots/normalized/invalid/`
- `docs/validation/market-snapshot-validation.md`
- Updated `docs/validation/rule-ids.md`
- Updated `docs/validation/sample-rule-mapping.md`
- Updated `docs/foundation/artifact-manifest.md`
- `scripts/validation/check-market-snapshots.sh`
- `README.md` and `AGENTS.md` updated only if project-wide guidance changes; otherwise completion evidence must state no update was needed

## Manual Review

1. Open the raw snapshot valid samples.
2. Confirm each raw sample includes `raw_snapshot_id`, source context, canonical `asset.symbol`, `observed_at`, `last_price`, `currency`, `volume`, and provenance.
3. Confirm each valid raw sample's `asset.symbol` exists in `data/watchlists/asset-watchlist.json` and has `active` set to true.
4. Open the normalized snapshot valid samples.
5. Confirm each normalized sample includes `raw_snapshot_id` and traces back to a valid raw sample.
6. Confirm normalized samples use the canonical watchlist `symbol` and do not use exchange symbol variants.
7. Confirm `S&P/BMV IPC`, if present, is treated only as optional benchmark context and does not count toward equity snapshot coverage.
8. Confirm invalid samples separately demonstrate missing asset, inactive asset, malformed required fields, and prohibited advisory or live-feed content.
9. Confirm no sample includes buy, sell, hold, rating, ranking, target price, portfolio allocation, recommendation, performance forecast, live-feed metadata, or runtime integration behavior.
10. Confirm `README.md` and `AGENTS.md` were reviewed and either updated where needed or documented as not needing changes.

## Local Validation

Run from the repository root after implementation:

```bash
scripts/validation/check-market-snapshots.sh
```

Expected output:

```text
PASS: Local market snapshot contracts and samples validated
```

The command should validate required paths, JSON parseability, raw/normalized separation, active watchlist symbols, canonical symbol usage, `raw_snapshot_id` provenance links, observed value fields, invalid sample mappings, and product boundary guardrails.

## PR Evidence

Pull requests for this feature should include:

- Command executed.
- Pass/fail result.
- Valid raw snapshot sample count.
- Valid normalized snapshot sample count.
- Invalid snapshot sample count.
- Active watchlist symbol checks performed.
- Invalid sample to violated `MS-REQ-*` rule ID mapping.
- Confirmation that normalized samples reference valid raw samples by `raw_snapshot_id`.
- Confirmation that `S&P/BMV IPC` is benchmark context only when present.
- Confirmation that no external API, scraping, Kafka, database, FastAPI, AWS, dashboard, AI, live-feed, or runtime ingestion behavior was introduced.
- Confirmation that `README.md` and `AGENTS.md` were updated if needed or explicitly reviewed as not needing changes.

## Expected Outcome

Reviewers can reproduce validation from a clean clone in 10 minutes or less using repository-local instructions only.

## Validation Evidence

Commands executed from repository root:

```bash
scripts/validation/check-market-snapshots.sh
scripts/validation/check-asset-watchlist.sh
```

Results:

```text
PASS: Local market snapshot contracts and samples validated
PASS: Equity-primary asset watchlist and samples validated
```

Review summary:

- Valid raw snapshot samples: 2.
- Valid normalized snapshot samples: 2.
- Invalid raw snapshot samples: 4.
- Invalid normalized snapshot samples: 2.
- Invalid samples map to `MS-REQ-002`, `MS-REQ-003`, `MS-REQ-004`, `MS-REQ-006`, `MS-REQ-007`, and `MS-REQ-009` in `docs/validation/sample-rule-mapping.md`.
- Valid normalized samples reference valid raw samples by `raw_snapshot_id`.
- `S&P/BMV IPC` remains benchmark context only and does not count toward equity snapshot coverage.
- `README.md` was updated because market snapshot artifacts and validation are now project-wide foundation artifacts.
- `AGENTS.md` was updated because agents must treat market snapshot contracts as boundaries and run market snapshot validation when those artifacts change.
- No runtime ingestion, external API, scraping, Kafka, database, FastAPI, AWS, dashboard, AI, or live-feed behavior was introduced.
