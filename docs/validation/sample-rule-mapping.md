# Sample Rule Mapping

## Invalid Samples

| Sample | Violated Rule IDs | Rationale |
|--------|-------------------|-----------|
| `data/samples/asset-events/invalid/asset-event-invalid-01-missing-required.json` | `AE-REQ-001` | Missing required `event_id`. |
| `data/samples/asset-events/invalid/asset-event-invalid-02-bad-source-category.json` | `AE-REQ-006`, `SRC-001` | `source.category` is not one of the accepted policy categories. |
| `data/samples/asset-events/invalid/asset-event-invalid-03-invalid-timestamp.json` | `AE-REQ-004` | `occurred_at` is not an RFC3339 timestamp. |
| `data/samples/watchlists/invalid/asset-watchlist-invalid-missing-required.json` | `WL-REQ-002` | Missing required `effective_date`. |
| `data/samples/watchlists/invalid/asset-watchlist-invalid-wrong-asset-type.json` | `WL-REQ-003`, `WL-REQ-005` | A primary monitoring target is incorrectly typed as an index and the sample lacks the required active equity target count. |
| `data/samples/watchlists/invalid/asset-watchlist-invalid-advisory-content.json` | `WL-REQ-009` | Contains prohibited advisory language. |
| `data/samples/market-snapshots/raw/invalid/raw-market-snapshot-invalid-01-missing-watchlist-asset.json` | `MS-REQ-004` | Raw snapshot references a symbol that is not present in the canonical watchlist. |
| `data/samples/market-snapshots/raw/invalid/raw-market-snapshot-invalid-02-inactive-watchlist-asset.json` | `MS-REQ-004` | Raw snapshot references a watchlist symbol whose `active` status is false. |
| `data/samples/market-snapshots/raw/invalid/raw-market-snapshot-invalid-03-malformed-required-fields.json` | `MS-REQ-002`, `MS-REQ-006` | Raw snapshot has malformed timing and is missing a required observed value. |
| `data/samples/market-snapshots/raw/invalid/raw-market-snapshot-invalid-04-prohibited-content.json` | `MS-REQ-009` | Raw snapshot contains prohibited advisory or live-feed content. |
| `data/samples/market-snapshots/normalized/invalid/normalized-market-snapshot-invalid-01-missing-raw-snapshot-id.json` | `MS-REQ-003`, `MS-REQ-007` | Normalized snapshot omits the required raw snapshot provenance link. |
| `data/samples/market-snapshots/normalized/invalid/normalized-market-snapshot-invalid-02-exchange-symbol-variant.json` | `MS-REQ-004` | Normalized snapshot uses an exchange symbol variant instead of the canonical watchlist symbol. |
