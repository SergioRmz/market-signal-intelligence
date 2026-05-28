# Validation Rule IDs

## Contract Rules

- `AE-REQ-001`: `event_id` is required and must be a non-empty string.
- `AE-REQ-002`: `event_type` is required and must be a non-empty string.
- `AE-REQ-003`: `schema_version` is required and must identify the schema version.
- `AE-REQ-004`: `occurred_at` is required and must be an RFC3339 timestamp.
- `AE-REQ-005`: `source.name` is required and must be a non-empty string.
- `AE-REQ-006`: `source.category` must be one of `allowed`, `conditional`, or `prohibited`.
- `AE-REQ-007`: `asset.symbol` is required and must be a non-empty string.
- `AE-REQ-008`: `asset.market` is required and must be a non-empty string.
- `AE-REQ-009`: `payload` is required and must be an object.

## Policy Rules

- `SRC-001`: Source category must be documented in the allowed sources policy.
- `SRC-002`: Conditional sources must document usage constraints.
- `SRC-003`: Prohibited sources must not appear in valid samples.

## Review Rules

- `REV-001`: PR validation evidence must include commands executed and pass/fail result.
- `REV-002`: Each invalid sample must map to at least one rule ID.
