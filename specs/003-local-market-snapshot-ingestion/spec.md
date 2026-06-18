# Feature Specification: Local Market Snapshot Ingestion

**Feature Branch**: `003-local-market-snapshot-ingestion`

**Created**: 2026-05-28

**Status**: Draft

**Input**: User description: "Crea la spec 003-local-market-snapshot-ingestion. Debe implementar una base local de ingesta usando archivos sample. Debe validar que el activo exista y este activo en la watchlist. Debe separar raw snapshot de normalized snapshot. Debe incluir samples validos e invalidos. Debe agregar validaciones ligeras. No debe agregar APIs externas, scraping, Kafka, base de datos, FastAPI, AWS ni IA."

## Clarifications

### Session 2026-05-28

- Q: How should snapshots handle `S&P/BMV IPC` relative to active equity monitoring targets? → A: Accept active equities and allow `IPC` only as an optional benchmark; `IPC` does not count toward equity minimums.
- Q: Should raw snapshots accept exchange symbol variants or only canonical watchlist symbols? → A: Raw snapshots must use only the canonical watchlist `symbol`; exchange variants are invalid.
- Q: What minimum observed market fields should valid snapshot samples include? → A: Require `last_price`, `currency`, and `volume`; other market fields are optional.
- Q: Must invalid samples cover missing asset and inactive asset as separate failures? → A: Invalid samples must cover both missing asset and inactive asset as separate failures.
- Q: How should normalized snapshots reference their source raw sample? → A: Each normalized snapshot must reference a required `raw_snapshot_id` from its source raw sample.
- Q: What general project documentation must be updated before completion? → A: Review `README.md` and `AGENTS.md`, and update them if and only if project-wide usage, validation, scope, or agent guidance changes.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ingest Local Sample Snapshots (Priority: P1)

As a maintainer, I need a repository-local market snapshot ingestion baseline using sample files so future ingestion work can be reviewed against deterministic inputs before any external market data integration exists.

**Why this priority**: The platform needs a reproducible local baseline before introducing live feeds, services, infrastructure, or automated market integrations.

**Independent Test**: Can be fully tested by reviewing the local snapshot sample set and confirming valid samples represent accepted candidate inputs while invalid samples demonstrate rejected conditions without requiring network access or deployed services.

**Acceptance Scenarios**:

1. **Given** a repository checkout with local market snapshot samples, **When** a maintainer reviews the valid raw snapshot samples, **Then** each sample contains enough source, timing, asset, and observed-value context to be evaluated locally.
2. **Given** a valid raw snapshot sample for an allowed asset, **When** the local ingestion baseline is reviewed, **Then** the sample is accepted as eligible for normalization only if its asset exists in the canonical watchlist and is active.
3. **Given** an invalid raw snapshot sample, **When** a reviewer compares it to the documented validation rules, **Then** the sample has an explicit failure reason and at least one mapped rule ID.

---

### User Story 2 - Separate Raw and Normalized Snapshots (Priority: P2)

As a future ingestion service owner, I need raw market snapshots and normalized market snapshots represented as distinct artifacts so provenance is preserved while downstream consumers can rely on a clean canonical form.

**Why this priority**: Separating raw observations from normalized records preserves traceability and prevents future consumers from mistaking source-shaped inputs for curated platform-ready data.

**Independent Test**: Can be tested by comparing raw and normalized sample sets and confirming raw samples preserve source-facing fields while normalized samples use a canonical, watchlist-aligned structure with provenance back to the raw input.

**Acceptance Scenarios**:

1. **Given** a raw sample and its normalized counterpart, **When** a reviewer compares them, **Then** the normalized snapshot references the originating raw snapshot and retains source provenance without overwriting the raw sample.
2. **Given** normalized snapshot samples, **When** a reviewer checks asset identity, timing, and value fields, **Then** each normalized sample uses canonical watchlist asset symbols and a consistent snapshot timestamp representation.
3. **Given** a raw sample that cannot be normalized because the asset is missing or inactive in the watchlist, **When** validation guidance is applied, **Then** no valid normalized sample is produced for that rejected input.

---

### User Story 3 - Validate Snapshot Readiness Locally (Priority: P3)

As a contributor or future agent, I need lightweight local validation rules and samples so I can verify snapshot artifacts without adding external APIs, scraping, streaming, databases, service endpoints, cloud resources, or AI analysis.

**Why this priority**: Lightweight validation keeps the feature foundation-first while giving reviewers repeatable evidence for contract, sample, watchlist, and guardrails.

**Independent Test**: Can be tested by following repository-local validation guidance and confirming valid samples pass, invalid samples fail for documented rule IDs, and all reviewed assets are checked against the active watchlist.

**Acceptance Scenarios**:

1. **Given** the snapshot validation rules, **When** a contributor evaluates all provided samples, **Then** valid samples and invalid samples are classified consistently using only repository-local artifacts.
2. **Given** an asset symbol that is not in `data/watchlists/asset-watchlist.json`, **When** a sample references that symbol, **Then** the sample is rejected as out of scope for local ingestion.
3. **Given** a watchlist entry with `active` set to false, **When** a sample references that asset, **Then** the sample is rejected until a reviewed watchlist change makes the asset active.
4. **Given** the feature deliverables, **When** a reviewer checks scope, **Then** they find no live price fetching, website scraping, external API calls, streaming producers, service endpoints, database persistence, cloud deployment, or AI behavior.

---

### Edge Cases

- What happens when a raw snapshot references `S&P/BMV IPC` without the required active equity snapshot coverage?
- What happens when a raw snapshot uses an exchange symbol variant instead of the canonical local watchlist `symbol`?
- How is a raw snapshot handled when required timing, source, asset, or observed-value fields are missing?
- What happens when a normalized snapshot exists without a corresponding raw snapshot reference?
- How are stale, future-dated, or malformed snapshot timestamps identified during local validation?
- What happens when a sample includes advisory language, rankings, target prices, live-price feed metadata, or performance predictions?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The feature MUST define a local market snapshot ingestion baseline based only on repository sample files and documentation, without live or external data acquisition.
- **FR-002**: The feature MUST define raw market snapshot artifacts that preserve source-facing observation details, including source context, asset identity, observation timing, observed values, and provenance metadata.
- **FR-003**: The feature MUST define normalized market snapshot artifacts that are separate from raw snapshots and use canonical watchlist-aligned asset identity, normalized timing, normalized observed-value fields, and a required `raw_snapshot_id` provenance reference back to the raw snapshot.
- **FR-004**: Raw snapshot samples and normalized snapshot samples MUST be stored as distinct sample sets so reviewers can evaluate source preservation and normalized output independently.
- **FR-005**: A raw snapshot MUST be eligible for normalization only when its asset symbol exists in `data/watchlists/asset-watchlist.json` and the corresponding watchlist entry has `active` set to true.
- **FR-006**: A snapshot referencing an asset that is missing from the watchlist MUST be classified as invalid for this local ingestion baseline.
- **FR-007**: A snapshot referencing an inactive watchlist asset MUST be classified as invalid for this local ingestion baseline.
- **FR-008**: The feature MUST preserve the equity-primary watchlist rule: individual Mexican equities are monitoring targets, while active `S&P/BMV IPC` snapshots MAY be accepted only as optional benchmark context and MUST NOT replace or count toward required equity snapshot coverage.
- **FR-009**: Raw and normalized snapshots MUST use the canonical `symbol` value from `data/watchlists/asset-watchlist.json`; samples using exchange symbol variants instead of the canonical local symbol MUST be classified as invalid.
- **FR-010**: The feature MUST include at least two valid raw snapshot samples and at least two valid normalized snapshot samples that demonstrate successful local snapshot acceptance and normalization readiness.
- **FR-011**: The feature MUST include invalid snapshot samples demonstrating distinct failures, including separate examples for a missing watchlist asset and an inactive watchlist asset, plus malformed required fields and prohibited advisory or live-feed content.
- **FR-012**: Each invalid snapshot sample MUST map to at least one stable validation rule ID documented in repository validation guidance.
- **FR-013**: Valid raw and normalized snapshot samples MUST include observed values for `last_price`, `currency`, and `volume`; other market observation fields MAY be included only when they remain static, local, and .
- **FR-014**: The feature MUST define lightweight validation rules for required fields, raw-to-normalized separation, watchlist existence, active status, canonical symbol usage, timestamp quality, observed-value shape, required `raw_snapshot_id` provenance linkage, and prohibited non-local behavior.
- **FR-015**: The local validation guidance MUST be reproducible from a clean repository checkout without network access, deployed services, event brokers, database connections, service endpoints, cloud resources, or AI tools.
- **FR-016**: The feature MUST document validation evidence expected from reviewers, including reviewed sample counts, pass/fail classification, active-watchlist checks, invalid sample rule mappings, and scope-guardrail confirmation.
- **FR-017**: The feature MUST NOT add external APIs, website scraping, Kafka or streaming topology, database persistence, FastAPI or service endpoints, AWS or cloud automation, dashboard behavior, AI analysis, RAG workflows, autonomous agents, or live price fetching.
- **FR-018**: Snapshot artifacts MUST NOT include buy, sell, hold, rating, ranking, target price, portfolio allocation, recommendation, or performance forecast language.
- **FR-019**: Snapshot artifacts MUST remain functional and technical examples for local validation and MUST NOT imply personalized financial advice or trading signals.
- **FR-020**: The feature MUST update governed artifact traceability so new snapshot contracts, samples, validation guidance, and local validation artifacts are discoverable by maintainers.
- **FR-021**: Before completion, the feature MUST review `README.md` and `AGENTS.md` and update them if and only if snapshot ingestion artifacts introduce project-wide usage instructions, validation workflow changes, contributor guidance, scope boundaries, or agent operating constraints not already covered.
- **FR-022**: Future ingestion work MUST be able to use the raw and normalized snapshot definitions as contract boundaries without relying on external lookup behavior introduced by this feature.

### Key Entities *(include if feature involves data)*

- **Raw Market Snapshot**: A local sample representation of a source-shaped market observation, preserving source context, original asset identifier, observation timestamp, required `last_price`, `currency`, and `volume` observed values, a `raw_snapshot_id`, and provenance needed for reproducibility.
- **Normalized Market Snapshot**: A canonical sample representation derived from an eligible raw snapshot, using active watchlist asset identity, normalized timing, required `last_price`, `currency`, and `volume` observed values, and a required `raw_snapshot_id` reference back to the raw snapshot.
- **Snapshot Sample Set**: The grouped valid and invalid raw or normalized examples used by reviewers to verify interpretation of snapshot validation rules.
- **Active Watchlist Asset**: A watchlist entry in `data/watchlists/asset-watchlist.json` whose symbol exists and whose `active` value permits local ingestion baseline evaluation.
- **Snapshot Validation Rule**: A stable rule with an identifier used to classify raw and normalized snapshot samples, explain invalid examples, and support review evidence.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of valid snapshot samples reference assets that exist in the canonical watchlist and are active at review time.
- **SC-002**: Reviewers can classify 100% of provided snapshot samples as valid or invalid with no ambiguity using repository-local validation rules.
- **SC-003**: 100% of invalid snapshot samples map to at least one documented validation rule ID.
- **SC-004**: A maintainer can distinguish raw snapshot samples from normalized snapshot samples and trace each valid normalized sample back to its raw source in under 5 minutes.
- **SC-005**: Local validation evidence can be reproduced from a clean repository checkout in 10 minutes or less without network access or deployed infrastructure.
- **SC-006**: 0 feature deliverables introduce external APIs, scraping, Kafka, databases, FastAPI endpoints, AWS resources, AI analysis, live price fetching, or other runtime market-data integrations.
- **SC-007**: At least 90% of maintainers reviewing the feature can explain the raw-vs-normalized boundary, active-watchlist gate, and product boundary within 10 minutes using only repository-local artifacts.
- **SC-008**: Completion review confirms `README.md` and `AGENTS.md` were either updated with required project-wide guidance or explicitly documented as not needing changes.

## Assumptions

- The initial snapshot ingestion baseline is a local contract and sample-data foundation, not a production ingestion service.
- The canonical watchlist at `data/watchlists/asset-watchlist.json` remains the source of truth for determining whether a sample asset is allowed and active.
- Raw snapshots may preserve source-shaped field names or values, while normalized snapshots use canonical platform terminology defined by this feature.
- Lightweight validation may include repository-local commands or manual review guidance, but it must not depend on external services or network calls.
- Sample market values are illustrative, static, and ; they do not represent live prices, recommendations, or performance forecasts.
- General project documentation updates are conditional; they are required only when the feature introduces information that maintainers, contributors, or agents need outside feature-specific artifacts.
