# AssetEvent Contract Interface

## Scope
Defines the canonical baseline event contract interface for cross-service compatibility planning.

## Canonical Schema Path
- `contracts/events/asset-event.schema.json`

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
- `source.category` (`allowed` | `conditional` | `prohibited`)
- `asset.symbol`
- `asset.market`

## Compatibility Rules
- Schema changes must be versioned in `schema_version`.
- Removing required fields is considered breaking.
- Invalid samples must include explicit violated rule references.

## Validation Contract
- Validation must run from a clean clone using local commands only.
- Evidence must be included in PRs: command logs and invalid-sample rule mapping.
