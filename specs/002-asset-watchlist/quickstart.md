# Quickstart: Initial Asset Watchlist

## Purpose

Provide a local review path for the IPC-only asset watchlist feature before implementation tasks begin.

## Expected Artifacts After Implementation

- `data/watchlists/asset-watchlist.json`
- `data/samples/watchlists/valid/asset-watchlist-valid-ipc.json`
- `data/samples/watchlists/invalid/asset-watchlist-invalid-missing-required.json`
- `data/samples/watchlists/invalid/asset-watchlist-invalid-wrong-asset-type.json`
- `data/samples/watchlists/invalid/asset-watchlist-invalid-advisory-content.json`
- `docs/validation/asset-watchlist-validation.md`
- Updated `docs/validation/rule-ids.md`
- Updated `docs/validation/sample-rule-mapping.md`
- Updated `docs/foundation/artifact-manifest.md`

## Manual Review

1. Open `data/watchlists/asset-watchlist.json`.
2. Confirm the watchlist identifies exactly one active entry.
3. Confirm the entry uses symbol `IPC`, display name `S&P/BMV IPC`, asset type `index`, and currency `MXN`.
4. Confirm market metadata identifies BMV/Mexico context without requiring an external lookup.
5. Confirm traceability context explains inclusion without investment advice or trading signals.
6. Confirm no watchlist or sample file contains live prices, target prices, ratings, recommendations, portfolio guidance, or performance forecasts.

## Local Validation

Run from the repository root after implementation tasks create the validation script:

```bash
scripts/validation/check-asset-watchlist.sh
```

The command should verify required paths, JSON parseability, IPC-only constraints, rule IDs, invalid sample mappings, and non-advisory content guardrails.

## PR Evidence

Pull requests for this feature should include:

- Command executed.
- Pass/fail result.
- Current watchlist version.
- Count of active entries.
- Valid sample count.
- Invalid sample count.
- Invalid sample to violated rule ID mapping.
- Confirmation that no runtime ingestion, external API, scraping, database, endpoint, streaming, dashboard, or AI behavior was introduced.

## Expected Outcome

Reviewers can reproduce validation from a clean clone in 10 minutes or less using repository-local instructions only.
