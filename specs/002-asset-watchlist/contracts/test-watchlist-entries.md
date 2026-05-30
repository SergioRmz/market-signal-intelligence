# Contract Test Scenario: Equity-Primary Watchlist Entries

## Purpose

Verify that the canonical watchlist artifact satisfies the equity-primary contract before any future ingestion feature consumes it.

## Scenario

1. Open `data/watchlists/asset-watchlist.json`.
2. Confirm the top-level fields `watchlist_id`, `version`, `effective_date`, `purpose`, and `assets` exist.
3. Confirm `assets` contains between 5 and 15 entries.
4. Confirm at least five active entries use `asset_type: equity` and `asset_role: monitoring_target`.
5. Confirm every entry has a unique canonical `symbol`.
6. Confirm every entry uses currency `MXN`.
7. Confirm market metadata identifies BMV and Mexico context.
8. Confirm traceability includes `source_reference` and `review_rationale`.
9. If `IPC` appears, confirm it uses `asset_type: index` and `asset_role: reference_benchmark`.
10. Confirm no live prices, target prices, ratings, trading signals, recommendations, portfolio guidance, or performance forecasts appear.

## Expected Result

The canonical watchlist passes local validation with:

```bash
scripts/validation/check-asset-watchlist.sh
```
