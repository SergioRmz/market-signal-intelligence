# Feature Specification: Market Source Adapter

**Feature Branch**: `004-market-source-adapter`

**Created**: 2026-05-31

**Status**: Draft

**Input**: User description: "Add the first controlled external market data source integration for BMV Signal Intelligence Platform. Introduce a small, replaceable market data source adapter that can fetch a market snapshot for an active watchlist ticker from an external source, preserve raw source data, convert it into the existing raw market snapshot shape, validate it through the existing snapshot pipeline, and produce deterministic testable outputs. External sources are unstable. Internal contracts must remain stable. Must include a source adapter boundary, one initial implementation for a single external or controlled HTTP source, explicit HTTP timeout handling, expected failure handling, raw source payload and metadata preservation, active asset watchlist validation, reuse of existing local snapshot validation/normalization where applicable, fixtures or tests for successful and failed fetch scenarios, and minimal documentation. Must not include Kafka, FastAPI endpoints, database persistence, AWS resources, dashboard work, AI analysis, trading signals, ratings, targets, investment recommendations, multiple providers, production scheduler, or aggressive scraping. Before finalizing the spec, incorporate this architectural clarification: the platform is BMV-first but not BMV-only."

## Clarifications

### Session 2026-06-01

- Q: What should the initial source type be for the first adapter integration? → A: One configurable controlled HTTP endpoint, with fixture-backed validation required.
- Q: What should the HTTP timeout expectation be for the initial adapter? → A: Timeout must default to 5 seconds and be configurable.
- Q: What credential posture should the initial controlled HTTP endpoint use? → A: Credentials may be required, but only via local environment configuration.
- Q: Should the adapter produce normalized snapshots directly? → A: Primary output is the adapted internal raw market snapshot; successful fetches must prove compatibility by reusing the existing 003 validation/normalization flow when existing normalized snapshot artifacts are available. No provider-specific normalized schema or duplicate normalization logic.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Fetch Controlled Snapshot For Active Ticker (Priority: P1)

As a maintainer, I need a controlled market data source adapter that can request one snapshot for an active watchlist ticker so the platform can take the first step beyond local sample files without weakening internal contracts.

**Why this priority**: The platform needs a narrow, testable external-source boundary before any broader ingestion, scheduling, streaming, persistence, or user-facing integration is considered.

**Independent Test**: Can be fully tested by using a deterministic successful source response for an active watchlist ticker and confirming the accepted result preserves the source payload, source metadata, and a valid raw market snapshot representation.

**Acceptance Scenarios**:

1. **Given** an active equity ticker in the canonical watchlist and a controlled successful source response from the configured HTTP endpoint, **When** a single snapshot fetch is requested, **Then** the result includes the preserved source payload, source metadata, and an accepted raw market snapshot shaped for existing snapshot validation.
2. **Given** an inactive or unsupported ticker, **When** a snapshot fetch is requested, **Then** the request is rejected before producing a raw market snapshot and the rejection identifies watchlist eligibility as the reason.
3. **Given** a successful source response whose market values are accepted, **When** the result is reviewed, **Then** it contains no recommendation, rating, target price, trading signal, portfolio guidance, or investment advice language.

---

### User Story 2 - Preserve Stable Internal Snapshot Contracts (Priority: P2)

As a future ingestion service owner, I need source-specific data to be isolated from existing raw and normalized snapshot contracts so a source change or future approved market expansion does not force downstream contract changes.

**Why this priority**: External sources are unstable; preserving the existing raw/normalized split protects downstream consumers and keeps contract evolution deliberate while recognizing the platform is BMV-first but not BMV-only.

**Independent Test**: Can be tested by comparing the source payload to the produced raw market snapshot and confirming source-specific fields remain preserved as source data while the platform-facing snapshot follows the existing raw snapshot contract and remains eligible for existing normalization checks.

**Acceptance Scenarios**:

1. **Given** a source response with provider-specific field names, **When** it is accepted, **Then** the original source response remains available for traceability and the produced raw snapshot uses the platform's raw snapshot shape.
2. **Given** a raw snapshot produced by the adapter, **When** existing local snapshot validation is applied, **Then** the snapshot passes or fails using the same rules as local raw snapshot samples.
3. **Given** a valid raw snapshot produced by the adapter, **When** compatibility is reviewed, **Then** the existing 003 validation and normalization flow can be reused to produce the normalized snapshot artifact when that artifact already exists in the project.
4. **Given** a future approved watchlist asset outside BMV scope, **When** the adapter boundary is reviewed, **Then** the boundary does not require BMV-specific assumptions beyond the currently active governed watchlist and source-policy checks.

---

### User Story 3 - Classify Expected Source Failures (Priority: P3)

As a contributor or future agent, I need deterministic success and failure fixtures so expected source problems are handled consistently and can be reviewed without relying on a live market source during development.

**Why this priority**: Source failures are common and must be predictable before the platform depends on any external market data behavior.

**Independent Test**: Can be tested by running fixture-backed scenarios for timeout, rate-limited response, ticker not found, invalid response shape, unsupported ticker, and inactive ticker, then confirming each produces a clear non-advisory failure result and no accepted raw snapshot.

**Acceptance Scenarios**:

1. **Given** a source request that exceeds the configured waiting limit, **When** the fetch is evaluated, **Then** it is classified as a timeout and no raw market snapshot is accepted.
2. **Given** a source response indicating rate limiting, **When** the fetch is evaluated, **Then** it is classified as rate limited and no retry loop, scheduler, or accepted raw market snapshot is produced.
3. **Given** a source response for an unknown ticker or an invalid response shape, **When** the fetch is evaluated, **Then** the result is rejected with the appropriate failure reason and the raw source evidence is retained when available.

---

### User Story 4 - Document Source Limits And Usage Constraints (Priority: P4)

As a reviewer, I need concise documentation of the initial source's limitations, allowed use, and non-goals so the integration cannot be mistaken for production market coverage, scraping, advice, or a multi-provider strategy.

**Why this priority**: Controlled documentation keeps the first source adapter aligned with source policy, traceability, and foundation-first delivery.

**Independent Test**: Can be tested by reviewing the source documentation and confirming it names the single allowed source mode, required attribution/provenance metadata, expected failure modes, and excluded behavior.

**Acceptance Scenarios**:

1. **Given** the source documentation, **When** a maintainer reviews allowed usage, **Then** they can identify the single supported source, its limitations, and the exact constraints for non-advisory, non-scheduled, non-scraping use.
2. **Given** a proposed change that adds another provider or production scheduler, **When** the feature scope is reviewed, **Then** the change is rejected as outside this feature.
3. **Given** the adapter changes project-wide usage, validation, scope, or agent guidance, **When** the feature is completed, **Then** the relevant project documentation such as `README.md` or `AGENTS.md` is updated; otherwise the review documents that no project-wide documentation change was needed.

### Edge Cases

- What happens when the requested ticker is present in the watchlist but not active?
- What happens when the requested ticker uses an exchange alias instead of the canonical watchlist symbol?
- What happens when the HTTP source does not respond before the configurable timeout, which defaults to 5 seconds?
- What happens when the source returns a rate-limited response with no usable market payload?
- What happens when the source reports that a ticker is not found?
- What happens when the source returns a successful status but the payload lacks required market observation fields?
- What happens when the source payload contains extra fields, advisory wording, ratings, target prices, or trading signals?
- What happens when source metadata is incomplete, such as missing retrieval timestamp, source name, or source response status?
- What happens when the source adapter introduces project-wide usage or agent guidance that is not yet reflected in `README.md` or `AGENTS.md`?
- What happens when a future governed watchlist includes an approved non-BMV asset while the first integration remains BMV-first?
- What happens when the controlled HTTP endpoint requires credentials but local environment configuration is missing?
- What happens when a successful external fetch produces a valid raw snapshot but no existing normalized snapshot artifact is available for compatibility proof?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The feature MUST define a stable source adapter boundary that separates external market source behavior from internal raw and normalized market snapshot contracts.
- **FR-002**: The feature MUST include exactly one initial source implementation for one configurable controlled HTTP endpoint.
- **FR-003**: The feature MUST support requesting one market snapshot at a time for a candidate ticker and MUST NOT introduce production scheduling, background polling, bulk harvesting, or aggressive scraping.
- **FR-004**: The feature MUST validate the candidate ticker against `data/watchlists/asset-watchlist.json` before accepting any market snapshot result.
- **FR-005**: The feature MUST accept snapshot results only for canonical watchlist symbols whose entries are active at evaluation time.
- **FR-006**: The feature MUST reject unsupported, missing, inactive, or alias-based tickers without producing an accepted raw market snapshot.
- **FR-007**: The adapter boundary MUST reflect that the platform is BMV-first but not BMV-only, meaning this first integration MAY focus on active BMV watchlist assets but MUST NOT hard-code BMV-only assumptions that would block future governed non-BMV assets.
- **FR-008**: Any future non-BMV asset support MUST remain outside this feature unless the asset is first added through governed watchlist and source-policy changes.
- **FR-009**: The feature MUST preserve the complete raw source payload for every source response that is received, including responses that are rejected for source shape or ticker-not-found reasons.
- **FR-010**: The feature MUST preserve source metadata for each attempted fetch, including source name, retrieval timestamp, requested ticker, response classification, and source response status when available.
- **FR-011**: The feature MUST transform accepted source responses into the existing raw market snapshot shape defined by `contracts/market-snapshots/raw-market-snapshot.schema.json` without changing that internal contract, and this adapted raw market snapshot is the feature's primary output.
- **FR-012**: Accepted raw market snapshots produced by the adapter MUST prove compatibility with the existing 003 market snapshot validation and normalization flow, including producing or matching the normalized snapshot artifact only when that artifact already exists in the project.
- **FR-013**: The feature MUST apply an explicit HTTP timeout that defaults to 5 seconds and can be configured for controlled validation scenarios.
- **FR-014**: The feature MUST explicitly handle HTTP timeout outcomes and classify them as failed fetches with no accepted raw market snapshot.
- **FR-015**: The feature MUST explicitly handle rate-limited source responses and classify them as failed fetches with no accepted raw market snapshot.
- **FR-016**: The feature MUST explicitly handle ticker-not-found source responses and classify them as failed fetches with no accepted raw market snapshot.
- **FR-017**: The feature MUST explicitly handle invalid source response shape and classify it as a failed fetch with no accepted raw market snapshot.
- **FR-018**: The feature MUST provide deterministic fixture-backed validation scenarios for one successful fetch and for each expected failure class: timeout, rate limited response, ticker not found, invalid response shape, unsupported ticker, and inactive ticker.
- **FR-019**: If the controlled HTTP endpoint requires credentials, the feature MUST allow credentials only through local environment configuration and MUST NOT commit credentials, tokens, secrets, or credential-bearing fixtures.
- **FR-020**: Missing local credentials MUST be classified as a configuration failure and MUST NOT produce an accepted raw market snapshot.
- **FR-021**: The feature MUST NOT create a provider-specific normalized schema or duplicate normalization logic; normalization remains owned by the existing 003 market snapshot pipeline.
- **FR-022**: The feature MUST document the initial source's usage constraints, limitations, attribution or provenance expectations, expected failure modes, credential posture, replacement boundary, and BMV-first but not BMV-only architectural scope.
- **FR-023**: The feature MUST update governed artifact traceability so any source adapter boundary, source documentation, fixtures, validation evidence, and test artifacts are discoverable by maintainers.
- **FR-024**: Before completion, the feature MUST review project documentation, including `README.md` and `AGENTS.md`, and update it if the adapter introduces project-wide usage instructions, validation workflow changes, scope boundaries, market-scope guidance, or agent operating guidance not already covered.
- **FR-025**: If project documentation does not require updates, the feature MUST document that review outcome in feature-specific completion evidence.
- **FR-026**: The feature MUST NOT add Kafka producers or consumers, FastAPI endpoints, database persistence, AWS resources, dashboard work, AI analysis, RAG workflows, autonomous agents, multiple source providers, production schedulers, bulk ingestion, or aggressive scraping.
- **FR-027**: The feature MUST NOT produce trading signals, buy/sell/hold language, ratings, rankings, price targets, portfolio allocation guidance, investment recommendations, or performance forecasts.
- **FR-028**: The feature MUST keep all market data content educational and technical, and any reviewer-facing documentation MUST reinforce that snapshots are not investment advice.

### Key Entities *(include if feature involves data)*

- **Market Source Adapter**: The replaceable boundary that accepts a candidate ticker, interacts with one configured source, classifies outcomes, preserves source evidence, avoids BMV-only coupling, and emits an accepted raw market snapshot only when validation succeeds.
- **Source Fetch Attempt**: A single request for one ticker, including requested ticker, source metadata, retrieval timestamp, outcome classification, and any raw source payload or failure evidence.
- **Raw Source Payload**: The source-shaped response body or error evidence retained for traceability before any platform snapshot conversion.
- **Source Metadata**: Context about where and when the payload was retrieved, including source name, requested ticker, response status, retrieval timestamp, and failure classification when applicable.
- **Adapter-Produced Raw Market Snapshot**: A raw market snapshot created from an accepted source payload that follows the existing raw market snapshot contract and can be evaluated by existing local validation.
- **Fetch Failure Classification**: A controlled outcome category for expected failures such as timeout, rate limited, ticker not found, invalid response shape, unsupported ticker, or inactive ticker.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of successful fixture-backed fetch scenarios for active watchlist tickers produce an accepted raw market snapshot that passes existing raw snapshot validation.
- **SC-002**: 100% of expected failure scenarios are classified into the documented failure categories with no accepted raw market snapshot produced.
- **SC-003**: 100% of received source responses retain raw source payload evidence and source metadata sufficient for a reviewer to reproduce the acceptance or rejection decision.
- **SC-004**: A maintainer can trace an accepted adapter-produced raw snapshot back to the requested ticker, source metadata, and preserved source payload in under 5 minutes.
- **SC-005**: 100% of timeout fixtures classify the fetch as failed when the source exceeds the 5-second default timeout or a documented configured timeout.
- **SC-006**: 100% of credential-required scenarios fail safely when local environment configuration is missing, with no accepted raw market snapshot and no credential value exposed in output evidence.
- **SC-007**: 100% of successful fetch scenarios demonstrate compatibility with the existing 003 validation and normalization flow without adding provider-specific normalized contracts or duplicate normalization logic.
- **SC-008**: A contributor can run deterministic success and failure checks from a clean repository checkout in 10 minutes or less without production scheduling, databases, event brokers, cloud resources, dashboards, or AI tools.
- **SC-009**: 0 feature deliverables change the existing raw or normalized market snapshot contract boundaries unless a separate governed contract-change task explicitly approves it.
- **SC-010**: 0 feature deliverables add Kafka, FastAPI endpoints, database persistence, AWS resources, dashboard behavior, AI analysis, trading signals, ratings, targets, recommendations, multiple providers, or aggressive scraping.
- **SC-011**: Completion review confirms the adapter boundary is documented as BMV-first but not BMV-only, with current acceptance still governed by active watchlist membership.
- **SC-012**: Completion review confirms `README.md` and `AGENTS.md` were either updated with required project-wide guidance or explicitly documented as not needing changes.
- **SC-013**: At least 90% of reviewers can explain the adapter boundary, source limitations, watchlist gate, BMV-first market scope, and raw/normalized preservation model within 10 minutes using repository-local artifacts.

## Assumptions

- The first source is one configurable controlled HTTP endpoint, and fixture-backed validation is required so success and failure behavior can be exercised without broad market coverage or scraping.
- The default HTTP timeout is 5 seconds unless a controlled validation scenario documents a different configured timeout.
- If source credentials are needed, they are provided only through local environment configuration and never committed to repository artifacts.
- The initial source adapter is a narrow foundation for future ingestion work, not a production-grade feed, scheduler, monitoring service, or multi-provider abstraction.
- Normalization remains owned by the existing 003 market snapshot pipeline; this feature proves compatibility with it rather than creating provider-specific normalization behavior.
- The platform is BMV-first but not BMV-only; this feature starts from active governed BMV watchlist assets while preserving a boundary that can support future approved non-BMV assets through later governed changes.
- Existing watchlist and market snapshot contracts remain the internal source of truth; this feature adapts external source data to those contracts rather than redefining them.
- Timeout, rate-limit, not-found, invalid-shape, unsupported-ticker, and inactive-ticker outcomes are sufficient expected failure categories for the first controlled source integration.
- Market values retrieved or represented through fixtures are technical observations only and are not recommendations, ratings, signals, targets, or investment advice.
- Project-wide documentation updates are conditional; they are required only when this feature adds guidance that maintainers, contributors, or agents need outside feature-specific artifacts.
