# Sample Rule Mapping

## Invalid Samples

| Sample | Violated Rule IDs | Rationale |
|--------|-------------------|-----------|
| `data/samples/asset-events/invalid/asset-event-invalid-01-missing-required.json` | `AE-REQ-001` | Missing required `event_id`. |
| `data/samples/asset-events/invalid/asset-event-invalid-02-bad-source-category.json` | `AE-REQ-006`, `SRC-001` | `source.category` is not one of the accepted policy categories. |
| `data/samples/asset-events/invalid/asset-event-invalid-03-invalid-timestamp.json` | `AE-REQ-004` | `occurred_at` is not an RFC3339 timestamp. |
