# Contract Test Scenario: Required AssetEvent Fields

## Purpose

Document the required-field contract expectations for `AssetEvent` samples.

## Required Top-Level Fields

- `event_id`
- `event_type`
- `schema_version`
- `occurred_at`
- `source`
- `asset`
- `payload`

## Required Nested Fields

- `source.name`
- `source.category`
- `asset.symbol`
- `asset.market`

## Expected Results

- Valid samples include all required fields.
- Invalid samples omit or violate at least one documented rule ID.
