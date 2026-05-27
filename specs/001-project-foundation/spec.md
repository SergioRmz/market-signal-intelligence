# Feature Specification: Initial Project Foundation

**Feature Branch**: `001-project-foundation`

**Created**: 2026-05-26

**Status**: Draft

**Input**: User description: "Before creating this specification, read and follow: .specify/memory/constitution.md, existing repository structure, and existing skills under .opencode/skills if relevant. Create the specification for the initial project foundation of BMV Signal Intelligence Platform, including repository documentation, source policy, base AssetEvent contract and samples, validation approach, and repository structure; exclude application implementation and advanced platform components."

## Clarifications

### Session 2026-05-26

- Q: Should artifact paths and minimum sections be flexible or explicitly fixed in this feature? -> A: Define an explicit artifact manifest with exact repository paths and minimum required sections per artifact.
- Q: How should required AssetEvent fields be defined in this iteration? -> A: Define exact names for minimum required fields shared by all AssetEvent records.
- Q: What minimum valid/invalid AssetEvent sample set is required? -> A: Require 2 valid samples and 3 invalid samples, each invalid mapped to explicit violated rule(s).
- Q: Which source policy categories should be mandatory? -> A: Use three categories: `allowed`, `conditional`, and `prohibited`.
- Q: What does "lightweight validation approach" mean for this feature? -> A: Local command-based validation with PR evidence, without external infrastructure or deployed services.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Establish Foundation Baseline (Priority: P1)

As a maintainer, I need a complete and explicit repository foundation package so new contributors and future agents can start work with shared scope, rules, and artifacts before any implementation begins.

**Why this priority**: Without this baseline, downstream features risk violating scope boundaries, data governance rules, and contract consistency.

**Independent Test**: Can be fully tested by reviewing the repository and confirming all required foundation artifacts exist with complete sections and no implementation code added.

**Acceptance Scenarios**:

1. **Given** a new clone of the repository, **When** a maintainer reviews root and docs folders, **Then** they find README, AGENTS guidance, architecture overview, source policy, AssetEvent schema, examples, and validation approach documentation.
2. **Given** the foundation artifacts, **When** a contributor reads them in order, **Then** they can explain project purpose, non-goals, constraints, and expected contribution workflow without external clarification.

---

### User Story 2 - Safeguard Scope Before Build (Priority: P2)

As a contributor, I need explicit exclusions and boundaries so I do not introduce ingestion, streaming infrastructure, AI analysis, cloud deployment, or dashboard implementation too early.

**Why this priority**: Clear boundaries prevent premature complexity and maintain compliance with the constitution's foundation-first principle.

**Independent Test**: Can be tested by verifying the specification includes non-goals and requirements that explicitly prohibit implementation of excluded subsystems in this feature.

**Acceptance Scenarios**:

1. **Given** the feature specification, **When** a contributor plans tasks, **Then** the plan excludes application logic and excluded platform components.
2. **Given** a pull request for this feature, **When** a reviewer checks changed files, **Then** changes are limited to foundational documentation, contracts, examples, and structure setup.

---

### User Story 3 - Enable Contract-First Collaboration (Priority: P3)

As a future agent or service owner, I need a base AssetEvent contract, valid/invalid samples, and a lightweight validation approach to align future event producers and consumers from day one.

**Why this priority**: Early contract alignment reduces future integration ambiguity and lowers risk of incompatible event evolution.

**Independent Test**: Can be tested by checking that the base contract is documented as a JSON Schema with required fields, versioning intent, and sample payloads that clearly pass or fail against stated rules.

**Acceptance Scenarios**:

1. **Given** the contract and sample set, **When** a reviewer evaluates each sample against the documented rules, **Then** each example is unambiguously categorized as valid or invalid.
2. **Given** the validation approach document, **When** a contributor prepares future contracts, **Then** they can follow a repeatable process for schema checks without introducing heavy infrastructure.

---

### Edge Cases

- What happens when a required foundation artifact is missing or incomplete at review time?
- How does the process handle data sources that are commonly referenced but prohibited by licensing or unverifiable provenance?
- What happens when a sample event appears valid structurally but violates business constraints such as unsupported source, asset identifier format, or timestamp quality?
- How is contract evolution handled when a proposed change breaks compatibility with earlier sample payloads?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The repository MUST include a foundation README that defines project purpose, in-scope outcomes, out-of-scope outcomes, non-investment-advice disclaimer, planned stack overview, and development methodology.
- **FR-002**: The repository MUST include an AGENTS guidance document defining how coding agents should operate in this repository, including scope safeguards, review expectations, and artifact update responsibilities.
- **FR-003**: The repository MUST include initial architecture documentation that identifies major bounded areas, intended data and control flow at a conceptual level, and the responsibilities of each repository area.
- **FR-004**: The repository MUST include an allowed sources policy for financial and macroeconomic data that defines approval criteria, prohibited source characteristics, attribution expectations, and provenance requirements.
- **FR-005**: The repository MUST define a base AssetEvent contract in JSON Schema form, including required identity, timing, source, and payload metadata fields, plus schema version identification.
- **FR-006**: The repository MUST include both valid and invalid AssetEvent sample files, with each invalid sample mapped to at least one explicit rule violation.
- **FR-007**: The foundation MUST define a lightweight event-contract validation approach that maintainers and contributors can execute during routine development without specialized platform infrastructure.
- **FR-008**: The repository MUST establish a documented directory structure covering specification-driven development assets, opencode skills/commands, backend area, dashboard area, service boundaries, contracts, data samples, infrastructure placeholders, and architecture/documentation space.
- **FR-009**: The feature deliverables MUST contain no application runtime implementation for ingestion, event streaming topology, AI analysis, cloud deployment automation, RAG workflows, or dashboard application behavior.
- **FR-010**: All foundation artifacts MUST be written to support maintainers, contributors, and future agents by emphasizing intent, responsibilities, governance constraints, and handoff clarity.
- **FR-011**: The foundation documentation MUST preserve constitution alignment by explicitly reinforcing educational/non-advisory scope, traceability expectations, contract-first behavior, and foundation-first sequencing.
- **FR-012**: The specification MUST define an explicit artifact manifest with exact expected paths and minimum required sections for each artifact.
- **FR-013**: The artifact manifest MUST include at least these paths: `README.md`, `AGENTS.md`, `docs/architecture/foundation-architecture.md`, `docs/policies/allowed-sources.md`, `contracts/events/asset-event.schema.json`, `data/samples/asset-events/valid/`, `data/samples/asset-events/invalid/`, and `docs/validation/event-contract-validation.md`.
- **FR-014**: The base AssetEvent schema MUST define these minimum required fields with exact names for every event: `event_id`, `event_type`, `schema_version`, `occurred_at`, `source`, `asset`, and `payload`.
- **FR-015**: The `asset` object in the base AssetEvent schema MUST require `symbol` and `market`; the `source` object MUST require `name` and `category`.
- **FR-016**: The sample set MUST include at least 2 valid AssetEvent JSON files under `data/samples/asset-events/valid/`.
- **FR-017**: The sample set MUST include at least 3 invalid AssetEvent JSON files under `data/samples/asset-events/invalid/`, and each invalid file MUST be traceable to explicit violated rule(s) documented in the validation approach artifact.
- **FR-018**: The allowed sources policy MUST classify each source into exactly one category: `allowed`, `conditional`, or `prohibited`.
- **FR-019**: The allowed sources policy MUST define minimum decision criteria per category, including licensing status, attribution requirements, provenance verifiability, and usage constraints.
- **FR-020**: The lightweight validation approach MUST be executable locally from the repository workspace using simple command(s) and MUST NOT require deployed services, cloud resources, event brokers, or runtime application components.
- **FR-021**: The feature review process MUST include validation evidence in pull requests, documenting executed validation command(s), pass/fail result per contract/sample set, and references to violating rule IDs for invalid samples.

### Key Entities *(include if feature involves data)*

- **Foundation Artifact**: A required repository baseline document or contract asset (README, AGENTS guidance, architecture document, source policy, schema, sample set, validation guide) with ownership and review intent.
- **AssetEvent Contract**: The canonical event definition used as the shared boundary for future producers/consumers, including schema version, source provenance fields, temporal metadata, asset identifiers, and event payload envelope.
- **AssetEvent Sample**: A concrete event example classified as valid or invalid, used to verify contract interpretation and reviewer consistency.
- **Source Policy Rule**: A decision rule defining whether a financial or macroeconomic source is allowed, conditionally allowed, or disallowed based on licensing, provenance, and reproducibility criteria.
- **Repository Structure Map**: A documented set of top-level and nested directories that allocates future work into stable areas while remaining implementation-light in this phase.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of required foundation artifacts listed in this specification are present and reviewable in a single pull request for this feature.
- **SC-002**: At least 90% of first-time contributors can correctly identify scope, non-goals, and next-step contribution path from repository documentation within 10 minutes of reading.
- **SC-003**: Reviewers can classify 100% of provided AssetEvent samples as valid or invalid with no ambiguity and consistent rationale.
- **SC-004**: 100% of proposed changes in this feature are limited to foundational documents, contracts, sample data, and directory scaffolding, with zero runtime feature behavior introduced.
- **SC-005**: The foundation package passes maintainer readiness review in one cycle or fewer minor revisions, indicating clear guidance for subsequent planning and task generation phases.
- **SC-006**: Reviewers can verify 100% of invalid sample files map to at least one documented violated contract rule without interpretation ambiguity.
- **SC-007**: Reviewers can reproduce contract/sample validation from a clean clone in 10 minutes or less using only repository-local instructions and commands.

## Assumptions

- Maintainers will treat this feature as a prerequisite gate and will not approve implementation features until this foundation is merged.
- Initial artifact language will prioritize clarity for mixed audiences (maintainers, contributors, future agents) rather than legal or regulatory final wording.
- Source policy will start with explicit inclusion/exclusion criteria and can evolve through governance without changing the feature's no-implementation boundary.
- The first AssetEvent schema version is intentionally minimal but complete enough to anchor future compatibility and validation discussions.
- Repository structure may include placeholders for future subsystems, but those placeholders will not contain executable feature logic in this phase.
