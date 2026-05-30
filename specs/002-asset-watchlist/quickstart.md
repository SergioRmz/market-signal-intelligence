# Quickstart: Initial Asset Watchlist

## Purpose

Provide a local review path for the equity-primary Mexican market asset watchlist feature. Individual equity tickers are the primary monitoring targets; `S&P/BMV IPC` is reference benchmark context only.

## Expected Artifacts After Implementation

- `data/watchlists/asset-watchlist.json`
- `data/samples/watchlists/valid/asset-watchlist-valid-equities.json`
- `data/samples/watchlists/invalid/asset-watchlist-invalid-missing-required.json`
- `data/samples/watchlists/invalid/asset-watchlist-invalid-wrong-asset-type.json`
- `data/samples/watchlists/invalid/asset-watchlist-invalid-advisory-content.json`
- `docs/validation/asset-watchlist-validation.md`
- Updated `docs/validation/rule-ids.md`
- Updated `docs/validation/sample-rule-mapping.md`
- Updated `docs/foundation/artifact-manifest.md`

## Manual Review

1. Open `data/watchlists/asset-watchlist.json`.
2. Confirm the watchlist identifies at least five active equity monitoring targets.
3. Confirm each primary target uses `asset_type` `equity`, `asset_role` `monitoring_target`, and currency `MXN`.
4. Confirm `S&P/BMV IPC`, if present, uses `asset_type` `index` and `asset_role` `reference_benchmark`.
5. Confirm market metadata identifies BMV/Mexico context without requiring an external lookup.
6. Confirm traceability context explains inclusion without investment advice or trading signals.
7. Confirm no watchlist or sample file contains live prices, target prices, ratings, recommendations, portfolio guidance, or performance forecasts.

## Local Validation

Run from the repository root:

```bash
scripts/validation/check-asset-watchlist.sh
```

The command verifies required paths, JSON parseability, equity-primary constraints, benchmark role constraints, rule IDs, invalid sample mappings, and non-advisory content guardrails.

Expected output:

```text
PASS: Equity-primary asset watchlist and samples validated
```

## PR Evidence

Pull requests for this feature should include:

- Command executed.
- Pass/fail result.
- Current watchlist version.
- Active equity monitoring target count.
- Reference benchmark count.
- Valid sample count.
- Invalid sample count.
- Invalid sample to violated rule ID mapping.
- Confirmation that no runtime ingestion, external API, scraping, database, endpoint, streaming, dashboard, or AI behavior was introduced.

## Expected Outcome

Reviewers can reproduce validation from a clean clone in 10 minutes or less using repository-local instructions only.

## Validation Evidence

Command executed from repository root:

```bash
scripts/validation/check-asset-watchlist.sh
```

Result:

```text
PASS: Equity-primary asset watchlist and samples validated
```

Review summary:

- Current watchlist version: `2026.05.28`.
- Active equity monitoring targets: 5.
- Reference benchmark entries: 1.
- Valid watchlist samples: 1.
- Invalid watchlist samples: 3.
- Invalid samples map to `WL-REQ-002`, `WL-REQ-003`, `WL-REQ-005`, and `WL-REQ-009` in `docs/validation/sample-rule-mapping.md`.
- No runtime ingestion, external API, scraping, database, endpoint, streaming, dashboard, or AI behavior was introduced.
