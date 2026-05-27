# Phase 0 Research - Initial Project Foundation

## Decision 1: Contract expression format
- Decision: Use JSON Schema Draft 2020-12 as the normative AssetEvent contract format.
- Rationale: Widely understood, tooling-neutral, and suitable for local validation without runtime services.
- Alternatives considered: OpenAPI component-only schema (less direct for event payloads), ad-hoc markdown contract (less machine-verifiable).

## Decision 2: Minimum AssetEvent core fields
- Decision: Enforce `event_id`, `event_type`, `schema_version`, `occurred_at`, `source`, `asset`, and `payload` as required top-level fields.
- Rationale: Provides identity, temporal traceability, versioning, provenance, and business envelope needed for downstream compatibility.
- Alternatives considered: Flexible optional field sets (higher ambiguity), per-event-type required lists at this stage (premature complexity).

## Decision 3: Source policy categorization
- Decision: Classify data sources as `allowed`, `conditional`, or `prohibited`.
- Rationale: Balanced governance granularity for licensing/provenance while keeping review simple.
- Alternatives considered: Binary allow/deny (insufficient nuance), multi-dimensional matrix (too complex for foundation phase).

## Decision 4: Lightweight validation definition
- Decision: Define lightweight validation as repository-local command execution plus PR evidence, without external infrastructure.
- Rationale: Meets reproducibility requirements and avoids violating foundation-first constraints.
- Alternatives considered: Manual-only checks (too subjective), CI-only enforcement from day one (extra setup overhead).

## Decision 5: Contract sample set baseline
- Decision: Require at least 2 valid and 3 invalid AssetEvent samples, with explicit violated rule mapping for each invalid sample.
- Rationale: Creates objective acceptance coverage for positive and negative cases with manageable effort.
- Alternatives considered: 1+1 samples (insufficient breadth), large sample suites (not proportional for initial phase).
