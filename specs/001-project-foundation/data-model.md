# Data Model - Initial Project Foundation

## Entity: FoundationArtifact
- Description: Required baseline repository artifact used for contributor and maintainer alignment.
- Fields:
  - `path` (string, unique): repository-relative canonical location.
  - `type` (enum): `documentation` | `policy` | `contract` | `sample` | `validation-guide`.
  - `required_sections` (array[string]): minimum section headings required for acceptance.
  - `owner_role` (enum): `maintainer` | `contributor` | `future-agent`.
  - `review_status` (enum): `draft` | `reviewed` | `approved`.

## Entity: AssetEventContract
- Description: Canonical event contract specification for future producer/consumer interoperability.
- Required top-level fields:
  - `event_id` (string, non-empty, unique intent)
  - `event_type` (string, non-empty)
  - `schema_version` (string, semantic version format)
  - `occurred_at` (string, RFC3339 timestamp)
  - `source` (object)
  - `asset` (object)
  - `payload` (object)
- Required nested fields:
  - `source.name` (string, non-empty)
  - `source.category` (enum): `allowed` | `conditional` | `prohibited`
  - `asset.symbol` (string, non-empty)
  - `asset.market` (string, non-empty)

## Entity: AssetEventSample
- Description: Example event used to verify contract interpretation and review consistency.
- Fields:
  - `sample_id` (string)
  - `path` (string, unique)
  - `classification` (enum): `valid` | `invalid`
  - `violated_rule_ids` (array[string], required when `classification=invalid`)
  - `notes` (string)
- Cardinality constraints:
  - Minimum 2 samples where `classification=valid`
  - Minimum 3 samples where `classification=invalid`

## Entity: SourcePolicyRule
- Description: Rule describing source admissibility and obligations.
- Fields:
  - `source_name` (string)
  - `category` (enum): `allowed` | `conditional` | `prohibited`
  - `licensing_status` (string)
  - `attribution_requirements` (string)
  - `provenance_verifiability` (string)
  - `usage_constraints` (string)

## Relationships
- A `FoundationArtifact` may define or reference one `AssetEventContract`.
- An `AssetEventContract` is validated by many `AssetEventSample` records.
- A `SourcePolicyRule` constrains both `AssetEventContract.source.category` and sample acceptance rules.

## Validation and State Notes
- Artifact lifecycle: `draft -> reviewed -> approved`.
- Invalid sample acceptance requires at least one explicit rule reference.
- Foundation phase excludes runtime state transitions (no ingestion/execution states in scope).
