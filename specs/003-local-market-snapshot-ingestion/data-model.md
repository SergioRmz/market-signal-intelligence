# Data Model: Local Market Snapshot Ingestion

## Entity: Raw Market Snapshot

Represents a source-shaped local market observation preserved as a static sample input.

### Fields

- `raw_snapshot_id`: Stable local identifier for the raw sample. Required; unique across raw samples.
- `schema_version`: Contract version for raw snapshot shape. Required.
- `source`: Source context object. Required; must identify local sample provenance without external calls.
- `asset`: Asset identity object. Required; `symbol` must match the canonical watchlist `symbol`.
- `observed_at`: Observation timestamp. Required; must be valid and not malformed.
- `observed_values`: Observed market values object. Required; must include `last_price`, `currency`, and `volume`.
- `provenance`: Review and sample provenance object. Required; must identify that the data is static and local.
- `notes`: Optional non-advisory notes.

### Relationships

- References one active `Watchlist Entry` by canonical `symbol`.
- May have one corresponding `Normalized Market Snapshot` through `raw_snapshot_id`.
- Classified by `Snapshot Validation Rule` during local validation.

## Entity: Normalized Market Snapshot

Represents the canonical, watchlist-aligned form of an eligible raw snapshot.

### Fields

- `normalized_snapshot_id`: Stable local identifier for the normalized sample. Required; unique across normalized samples.
- `schema_version`: Contract version for normalized snapshot shape. Required.
- `raw_snapshot_id`: Identifier of the originating raw snapshot. Required; must match an existing valid raw sample.
- `asset`: Canonical asset identity object. Required; `symbol` must match the active watchlist `symbol`.
- `observed_at`: Normalized observation timestamp. Required.
- `normalized_at`: Timestamp or date-time indicating when the sample was normalized for review. Required for reproducibility metadata.
- `observed_values`: Canonical observed values object. Required; must include `last_price`, `currency`, and `volume`.
- `provenance`: Provenance object linking source context, raw snapshot, and deterministic transformation notes. Required.

### Relationships

- Derived from one `Raw Market Snapshot` through `raw_snapshot_id`.
- References one active `Watchlist Entry` by canonical `symbol`.
- Must not exist as valid output if the originating raw snapshot fails watchlist or required-field validation.

## Entity: Observed Values

Represents the minimal local market observation payload.

### Fields

- `last_price`: Static illustrative numeric market value. Required; must not be presented as live data or advice.
- `currency`: Currency code. Required; expected value `MXN` for Mexican equities and benchmark samples.
- `volume`: Static illustrative numeric volume. Required; may be zero for benchmark samples if documented as contextual.
- Additional fields: Optional only when static, local, non-advisory, and documented by the contract.

## Entity: Watchlist Entry Reference

Represents the eligibility gate from snapshot samples to the canonical watchlist.

### Rules

- The referenced `symbol` must exist in `data/watchlists/asset-watchlist.json`.
- The referenced entry must have `active` set to true.
- Individual equities are monitoring targets.
- `S&P/BMV IPC` may be accepted only as optional benchmark context and does not count toward equity coverage.
- Exchange symbol variants are invalid unless they are also the canonical watchlist `symbol`.

## Entity: Snapshot Sample Set

Represents grouped examples used to test validity and invalidity.

### Fields

- `sample_path`: Repository path to the sample file.
- `snapshot_kind`: `raw` or `normalized`.
- `classification`: `valid` or `invalid`.
- `violated_rule_ids`: Required for invalid samples.
- `rationale`: Human-readable explanation of sample classification.

## Entity: Snapshot Validation Rule

Defines a stable local validation rule.

### Initial Rule IDs

- `MS-REQ-001`: Raw and normalized snapshot contracts must exist and be documented.
- `MS-REQ-002`: Raw snapshots must include required identity, source, asset, timestamp, observed values, and provenance fields.
- `MS-REQ-003`: Normalized snapshots must include required identity, `raw_snapshot_id`, asset, timestamp, observed values, and provenance fields.
- `MS-REQ-004`: Snapshot `asset.symbol` must match a canonical active symbol in `data/watchlists/asset-watchlist.json`.
- `MS-REQ-005`: `S&P/BMV IPC` is optional benchmark context only and must not count toward equity snapshot coverage.
- `MS-REQ-006`: Snapshot observed values must include `last_price`, `currency`, and `volume`.
- `MS-REQ-007`: Normalized snapshots must reference an existing valid raw snapshot by `raw_snapshot_id`.
- `MS-REQ-008`: Invalid samples must map to at least one `MS-REQ-*` rule ID in `docs/validation/sample-rule-mapping.md`.
- `MS-REQ-009`: Snapshot artifacts must not include live-feed behavior, advisory language, target prices, ratings, rankings, recommendations, or performance forecasts.
- `MS-REQ-010`: Snapshot validation must be reproducible locally without network access or deployed services.

## State Transitions

- `raw sample valid`: Required fields pass, symbol is canonical and active, observed values are present, and content is non-advisory.
- `raw sample invalid`: Missing watchlist asset, inactive asset, malformed required field, missing observed value, prohibited content, or non-local/live-feed metadata.
- `normalized sample valid`: References a valid raw sample by `raw_snapshot_id` and preserves canonical watchlist identity.
- `normalized sample invalid`: Missing raw reference, references an invalid or missing raw sample, loses provenance, or violates canonical identity rules.

## Conditional Global Documentation Review

- `README.md`: Update only if implementation adds project-wide usage or validation instructions that are not adequately covered by feature-specific docs.
- `AGENTS.md`: Always update the Speckit current-plan marker during planning; update other guidance only if new project-wide agent constraints are introduced.
- Completion evidence must state whether each general document was updated or reviewed as not needing changes.
