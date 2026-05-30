# Contract Scenario: Normalized Market Snapshot

## Purpose

Verify normalized market snapshot samples remain separate from raw samples and preserve deterministic provenance through `raw_snapshot_id`.

## Required Checks

- Valid normalized samples include `normalized_snapshot_id`, `schema_version`, `raw_snapshot_id`, `asset`, `observed_at`, `normalized_at`, `observed_values`, and `provenance`.
- `raw_snapshot_id` matches a valid raw snapshot sample.
- `provenance.source_raw_snapshot_id` matches `raw_snapshot_id`.
- `asset.symbol` remains canonical and active in the watchlist.
- Invalid normalized samples demonstrate missing raw provenance and exchange symbol variant rejection.

## Expected Outcome

The local validation command accepts valid normalized samples and rejects invalid normalized samples with explicit `MS-REQ-*` mappings.
