# Feature Specification: Initial Asset Watchlist

**Feature Branch**: `002-asset-watchlist`

**Created**: 2026-05-27

**Status**: Draft

**Input**: User description: "Create the initial asset watchlist feature for BMV Signal Intelligence Platform. The goal is to define a small, explicit, versioned list of Mexican market assets that the system is allowed to monitor in later ingestion features. This feature must create a local watchlist artifact with ticker symbols, display names, market metadata, asset type, currency, active status, and optional notes. It must include validation rules and sample data, but it must not fetch live prices, scrape websites, call external APIs, create Kafka producers, create FastAPI endpoints, create a database, or implement AI analysis. The feature must align with the constitution: traceability first, no investment advice, no trading signals, no premature runtime implementation, and contract-first collaboration. The output should be understandable for maintainers, future agents, and future ingestion services."

## Clarifications

### Session 2026-05-27

- Q: Where should the local watchlist artifact be stored? -> A: `data/watchlists/asset-watchlist.json`

### Session 2026-05-28

- Q: Should the first watchlist monitor only the S&P/BMV IPC index? -> A: No; individual Mexican equity tickers are the primary monitoring targets. `S&P/BMV IPC` may be included only as a reference benchmark of type `index`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Establish Allowed Asset Baseline (Priority: P1)

As a maintainer, I need a small, explicit, versioned watchlist of individual Mexican market assets so future ingestion work has a governed list of equity tickers it is allowed to monitor.

**Why this priority**: The platform cannot safely plan ingestion without a clear allowlist that defines asset scope, provenance, and non-advisory boundaries.

**Independent Test**: Can be fully tested by reviewing the watchlist artifact and confirming every listed asset includes required metadata, version context, active status, role, and traceability fields without requiring external services.

**Acceptance Scenarios**:

1. **Given** a repository checkout, **When** a maintainer opens the asset watchlist artifact, **Then** they can identify the watchlist version, active individual equity monitoring targets, optional reference benchmark, and whether each entry is active or inactive.
2. **Given** a listed equity, **When** a maintainer reviews its entry, **Then** they find ticker symbol, display name, market metadata, asset type `equity`, currency `MXN`, active status, monitoring role, traceability, and any applicable notes.
3. **Given** an asset not present in the watchlist, **When** a future ingestion feature evaluates monitoring scope, **Then** the asset is treated as not allowed until a reviewed watchlist change adds it.

---

### User Story 2 - Validate Watchlist Changes (Priority: P2)

As a contributor or future agent, I need explicit validation rules and examples so I can propose watchlist changes without introducing malformed entries, ambiguous identifiers, benchmark-only substitutions, or out-of-scope assets.

**Why this priority**: Validation rules make the watchlist reproducible and reviewable before any runtime service depends on it.

**Independent Test**: Can be tested by checking the validation guidance and sample data, then confirming valid samples satisfy every rule and invalid samples map to specific rule IDs.

**Acceptance Scenarios**:

1. **Given** the validation rules, **When** a contributor reviews a proposed watchlist entry, **Then** they can determine whether the entry is valid using only repository-local guidance.
2. **Given** invalid sample data, **When** a reviewer compares each sample to the validation rules, **Then** each invalid sample has at least one explicit violated rule ID.
3. **Given** duplicate symbols, unsupported asset metadata, or an index replacing equity entries, **When** validation guidance is applied, **Then** the issue is detected before the watchlist is accepted.

---

### User Story 3 - Preserve Non-Advisory Traceability (Priority: P3)

As a reviewer, I need the watchlist to explain its provenance and boundaries so it cannot be mistaken for investment advice, trading signals, or an automated market data integration.

**Why this priority**: The constitution requires traceability, educational scope, and foundation-first delivery; the watchlist must not imply recommendations or runtime behavior.

**Independent Test**: Can be tested by reviewing the watchlist, samples, and validation guidance for source references, change rationale, non-advisory language, and absence of live data behavior.

**Acceptance Scenarios**:

1. **Given** a watchlist entry, **When** a reviewer checks traceability, **Then** the entry includes enough provenance context to understand why the asset is listed without relying on live market data.
2. **Given** the watchlist and samples, **When** a reviewer searches for recommendation language, **Then** there are no buy, sell, hold, portfolio allocation, ranking, or price-target statements.
3. **Given** the feature deliverables, **When** a reviewer checks scope, **Then** they find no live price fetching, website scraping, external API calls, streaming producers, service endpoints, databases, or AI analysis behavior.

---

### Edge Cases

- What happens when two entries use the same ticker symbol with different display names or metadata?
- How is an asset represented when it is no longer intended for monitoring but remains in the versioned watchlist history?
- What happens when an asset has a commonly used informal ticker that conflicts with the official market identifier?
- How is `S&P/BMV IPC` represented as a reference benchmark without replacing individual equity monitoring targets?
- What happens when sample data is structurally valid but includes recommendation language, live price fields, or untraceable notes?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The feature MUST define the local asset watchlist artifact at `data/watchlists/asset-watchlist.json` and identify individual Mexican equity tickers as the primary assets allowed for monitoring by later ingestion features.
- **FR-002**: The watchlist artifact MUST include an explicit version identifier, review date or effective date, and a brief purpose statement describing it as an allowlist for future monitoring scope.
- **FR-003**: Each watchlist entry MUST include ticker symbol, display name, market metadata, asset type, asset role, currency, active status, and optional notes.
- **FR-004**: Market metadata for each entry MUST include enough information for reviewers and future ingestion services to distinguish the market venue and country or jurisdiction without consulting external systems.
- **FR-005**: Asset type values MUST use a documented controlled vocabulary limited to `equity` for primary monitoring targets and `index` only for an optional `S&P/BMV IPC` reference benchmark.
- **FR-006**: Each watchlist entry MUST use currency code `MXN`; notes MAY clarify that index benchmark observations are expressed as points rather than tradable currency amounts.
- **FR-007**: Active status MUST clearly indicate whether an asset is currently allowed for future monitoring or retained only for traceability/history.
- **FR-008**: The initial watchlist MUST remain small and explicit, containing at least 5 and no more than 15 assets, with at least 5 active individual equity monitoring targets.
- **FR-009**: The watchlist MUST include traceability context for each entry, including a source reference category, review rationale, or note sufficient for maintainers to understand why the asset is listed.
- **FR-010**: The feature MUST define validation rules covering required fields, ticker symbol uniqueness, controlled vocabularies, equity-primary role constraints, currency value, active status, traceability, and prohibited advisory or live-price content.
- **FR-011**: The validation rules MUST assign stable rule IDs so review findings and invalid samples can reference exact violations.
- **FR-012**: The feature MUST include sample watchlist data with at least one valid sample set and at least three invalid examples that demonstrate distinct validation failures.
- **FR-013**: Each invalid sample MUST map to at least one documented validation rule ID.
- **FR-014**: The watchlist and samples MUST NOT include live prices, target prices, ratings, trading signals, buy/sell/hold language, portfolio allocation guidance, or performance predictions.
- **FR-015**: The feature MUST NOT fetch live prices, scrape websites, call external APIs, create streaming producers, create service endpoints, create a database, implement automated ingestion, or implement AI analysis.
- **FR-016**: Future ingestion services MUST be able to determine whether a candidate asset is allowed by checking `data/watchlists/asset-watchlist.json`, asset role, and active status without relying on external lookup behavior from this feature.
- **FR-017**: The feature documentation MUST explain how maintainers should review additions, removals, or status changes while preserving traceability and non-advisory scope.
- **FR-018**: The feature deliverables MUST be understandable to maintainers, future agents, and future ingestion service owners without requiring platform runtime knowledge.
- **FR-019**: Any changed repository artifacts introduced for this feature MUST be traceable through a manifest or feature-specific documentation that identifies their purpose and expected review criteria.
- **FR-020**: If `S&P/BMV IPC` is included, it MUST use asset type `index`, asset role `reference_benchmark`, and MUST NOT count toward the minimum number of equity monitoring targets.

### Key Entities *(include if feature involves data)*

- **Asset Watchlist**: The versioned allowlist stored at `data/watchlists/asset-watchlist.json` that defines which individual Mexican equity assets later features may monitor, plus optional benchmark context.
- **Watchlist Entry**: A single asset record with symbol, display name, market metadata, asset type, asset role, currency, active status, traceability context, and optional notes.
- **Market Metadata**: Descriptive market context that distinguishes venue, country or jurisdiction, exchange symbol, and related identifier information needed to avoid ambiguity.
- **Validation Rule**: A documented requirement with a stable rule ID used to judge watchlist and sample correctness.
- **Watchlist Sample**: Example data classified as valid or invalid to demonstrate correct interpretation of the watchlist rules.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of watchlist entries include all required fields: ticker symbol, display name, market metadata, asset type, asset role, currency, and active status.
- **SC-002**: A maintainer can locate `data/watchlists/asset-watchlist.json` and identify all active equity monitoring targets plus any benchmark entry within 5 minutes from a clean repository checkout.
- **SC-003**: Reviewers can classify 100% of provided watchlist samples as valid or invalid with no ambiguity using the documented validation rules.
- **SC-004**: 100% of invalid samples map to at least one explicit validation rule ID.
- **SC-005**: A future ingestion service owner can evaluate a mixed set of 20 candidate assets against the watchlist with 100% consistent allow/not-allowed outcomes across two independent reviewers.
- **SC-006**: 0 feature deliverables introduce live data fetching, scraping, external API calls, streaming producers, service endpoints, database persistence, trading advice, or AI analysis behavior.
- **SC-007**: At least 90% of maintainers reviewing the feature can explain its purpose, scope boundaries, and change-review process within 10 minutes using only repository-local artifacts.

## Assumptions

- The initial watchlist is a governance artifact for future monitoring scope, not a statement that any asset is attractive, risky, recommended, or forecast to perform in any way.
- The first watchlist favors well-known Mexican equities with clear BMV identifiers, using S&P/BMV IPC constituent membership only as reference context for selection.
- Active status and asset role are sufficient for this phase to distinguish current monitoring targets from reference benchmarks and historical entries.
- Validation can be defined as repository-local rules and samples in this phase; automated enforcement remains local and does not require live market data.
- Later ingestion features will treat the watchlist as an input contract and will not infer permission to monitor unlisted assets.
