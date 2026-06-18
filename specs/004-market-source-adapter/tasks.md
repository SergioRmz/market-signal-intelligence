# Tasks: Market Source Adapter

**Input**: Design documents from `/specs/004-market-source-adapter/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Contract, unit, integration, and validation tasks are included because the feature requires fixture-backed scenarios, active watchlist gating, source metadata preservation, and compatibility with the existing market snapshot validation/normalization flow.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the adapter implementation, test, fixture, sample, and documentation locations used by all stories.

- [X] T001 Create source adapter package directories in `src/market_signal_intelligence/sources/` and `src/market_signal_intelligence/__init__.py`
- [X] T002 Create test directories in `tests/unit/`, `tests/integration/`, `tests/contract/`, and `tests/fixtures/market-source-adapter/`
- [X] T003 Create adapter sample directories in `data/samples/market-source-adapter/source-payloads/`, `data/samples/market-source-adapter/raw-snapshots/`, and `data/samples/market-source-adapter/failures/`
- [X] T004 [P] Create source documentation directory in `docs/sources/`
- [X] T005 [P] Create adapter validation script placeholder in `scripts/validation/check-market-source-adapter.sh`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared contracts, models, rule IDs, configuration rules, and validation baseline before story-specific behavior.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T006 Define package exports in `src/market_signal_intelligence/sources/__init__.py`
- [X] T007 Implement adapter data models and failure classification enum in `src/market_signal_intelligence/sources/models.py`
- [X] T008 Implement local environment configuration loader with 5-second default timeout in `src/market_signal_intelligence/sources/adapter.py`
- [X] T009 [P] Add adapter fetch result contract test in `tests/contract/test_adapter_fetch_result_contract.py`
- [X] T010 [P] Add `MSA-REQ-001` through `MSA-REQ-012` source adapter rule IDs to `docs/validation/rule-ids.md`
- [X] T011 Add adapter artifact paths and minimum review criteria to `docs/foundation/artifact-manifest.md`
- [X] T012 Create adapter validation guide with local command, rule IDs, evidence format, credential handling, and guardrails in `docs/validation/market-source-adapter-validation.md`
- [X] T013 Implement required path, JSON parse, no-secret, and no-prohibited-content checks in `scripts/validation/check-market-source-adapter.sh`
- [X] T014 Make `scripts/validation/check-market-source-adapter.sh` executable and document expected PASS output in `docs/validation/market-source-adapter-validation.md`

**Checkpoint**: Adapter contracts, shared models, rule IDs, and validation baseline are ready.

---

## Phase 3: User Story 1 - Fetch Controlled Snapshot For Active Ticker (Priority: P1) MVP

**Goal**: Fetch one active canonical watchlist ticker from the configured controlled HTTP endpoint and produce an accepted internal raw market snapshot with preserved source payload and metadata.

**Independent Test**: Run the success fixture path and confirm the result preserves provider payload, source metadata, and an adapted raw market snapshot that passes existing raw snapshot validation.

### Tests for User Story 1

- [X] T015 [P] [US1] Create successful active equity source fixture in `tests/fixtures/market-source-adapter/success-active-equity.json`
- [X] T016 [P] [US1] Add unit test for active watchlist ticker acceptance in `tests/unit/test_market_source_adapter_success.py`
- [X] T017 [P] [US1] Add integration test for adapted raw snapshot validation in `tests/integration/test_market_source_adapter_success_flow.py`

### Implementation for User Story 1

- [X] T018 [US1] Implement active canonical watchlist lookup in `src/market_signal_intelligence/sources/adapter.py`
- [X] T019 [US1] Implement controlled HTTP fetch wrapper with configurable timeout in `src/market_signal_intelligence/sources/controlled_http.py`
- [X] T020 [US1] Implement successful provider payload adaptation to existing raw market snapshot shape in `src/market_signal_intelligence/sources/adapter.py`
- [X] T021 [US1] Add preserved successful source payload sample in `data/samples/market-source-adapter/source-payloads/success-active-equity.json`
- [X] T022 [US1] Add accepted adapted raw snapshot sample in `data/samples/market-source-adapter/raw-snapshots/success-active-equity-raw-snapshot.json`
- [X] T023 [US1] Extend `scripts/validation/check-market-source-adapter.sh` to validate successful fixture count, source metadata, raw payload preservation, and adapted raw snapshot sample

**Checkpoint**: US1 is independently testable as the MVP adapter fetch path.

---

## Phase 4: User Story 2 - Preserve Stable Internal Snapshot Contracts (Priority: P2)

**Goal**: Prove adapter output remains compatible with existing raw and normalized snapshot contracts without provider-specific normalized schema or duplicated normalization logic.

**Independent Test**: Run compatibility checks and confirm the adapter-produced raw snapshot uses existing raw snapshot validation and existing 003 normalization flow when normalized artifacts already exist.

### Tests for User Story 2

- [X] T024 [P] [US2] Add integration test for existing market snapshot validation reuse in `tests/integration/test_market_source_adapter_snapshot_compatibility.py`
- [X] T025 [P] [US2] Add test that rejects provider-specific normalized schema files in `tests/contract/test_no_provider_normalized_schema.py`

### Implementation for User Story 2

- [X] T026 [US2] Implement raw snapshot compatibility helper that invokes existing validation expectations in `src/market_signal_intelligence/sources/adapter.py`
- [X] T027 [US2] Extend adapter provenance fields to link adapted raw snapshots to source attempt and payload evidence in `src/market_signal_intelligence/sources/adapter.py`
- [X] T028 [US2] Extend `scripts/validation/check-market-source-adapter.sh` to call `scripts/validation/check-market-snapshots.sh` after adapter-specific validation
- [X] T029 [US2] Add validation check rejecting provider-specific normalized schema artifacts under `contracts/` and `specs/004-market-source-adapter/contracts/` in `scripts/validation/check-market-source-adapter.sh`
- [X] T030 [US2] Document raw-primary output and existing 003 normalization ownership in `docs/validation/market-source-adapter-validation.md`

**Checkpoint**: US2 confirms stable internal contracts and existing normalization ownership.

---

## Phase 5: User Story 3 - Classify Expected Source Failures (Priority: P3)

**Goal**: Provide deterministic failure handling for timeout, rate limiting, ticker not found, invalid response shape, unsupported ticker, inactive ticker, and missing credentials.

**Independent Test**: Run fixture-backed failure scenarios and confirm each produces the expected failure classification, preserves source evidence when available, and produces no accepted raw snapshot.

### Tests for User Story 3

- [X] T031 [P] [US3] Create rate-limited source fixture in `tests/fixtures/market-source-adapter/failure-rate-limited.json`
- [X] T032 [P] [US3] Create ticker-not-found source fixture in `tests/fixtures/market-source-adapter/failure-ticker-not-found.json`
- [X] T033 [P] [US3] Create invalid response shape fixture in `tests/fixtures/market-source-adapter/failure-invalid-shape.json`
- [X] T034 [P] [US3] Add unit tests for timeout and rate-limited classification in `tests/unit/test_market_source_adapter_failures.py`
- [X] T035 [US3] Add unit tests for ticker-not-found and invalid-shape classification in `tests/unit/test_market_source_adapter_failures.py`
- [X] T036 [US3] Add unit tests for unsupported, inactive, and missing-credential classification in `tests/unit/test_market_source_adapter_failures.py`

### Implementation for User Story 3

- [X] T037 [US3] Implement timeout and rate-limited failure classification in `src/market_signal_intelligence/sources/controlled_http.py`
- [X] T038 [US3] Implement ticker-not-found and invalid-response-shape classification in `src/market_signal_intelligence/sources/adapter.py`
- [X] T039 [US3] Implement unsupported ticker, inactive ticker, and missing-credential configuration failure classification in `src/market_signal_intelligence/sources/adapter.py`
- [X] T040 [US3] Add failure evidence samples in `data/samples/market-source-adapter/failures/`
- [X] T041 [US3] Add adapter invalid sample mappings to `docs/validation/sample-rule-mapping.md`
- [X] T042 [US3] Extend `scripts/validation/check-market-source-adapter.sh` to verify each failure class and rule mapping

**Checkpoint**: US3 failure scenarios are deterministic and independently reviewable.

---

## Phase 6: User Story 4 - Document Source Limits And Usage Constraints (Priority: P4)

**Goal**: Document the single controlled source mode, limitations, credential posture, BMV-first but not BMV-only scope, and excluded production behaviors.

**Independent Test**: Review source documentation and confirm it names the single supported source mode, expected failure modes, attribution/provenance expectations, credential constraints, and excluded behaviors.

### Tests for User Story 4

- [X] T043 [P] [US4] Add documentation guardrail test for prohibited provider, scheduler, advisory, and secret content in `tests/unit/test_market_source_adapter_documentation.py`

### Implementation for User Story 4

- [X] T044 [US4] Create source limitations and usage constraints documentation in `docs/sources/market-source-adapter.md`
- [X] T045 [US4] Document BMV-first but not BMV-only adapter scope in `docs/sources/market-source-adapter.md`
- [X] T046 [US4] Document local credential configuration and no-secret evidence requirements in `docs/sources/market-source-adapter.md`
- [X] T047 [US4] Review `README.md` for project-wide adapter usage guidance and update it only if needed
- [X] T048 [US4] Review `AGENTS.md` for project-wide adapter agent guidance and update it only if needed
- [X] T049 [US4] Document README and AGENTS review outcome in `specs/004-market-source-adapter/quickstart.md`

**Checkpoint**: US4 documentation explains source limits, usage constraints, and no-goals.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, reproducibility evidence, and scope guardrail verification across all stories.

- [X] T050 [P] Cross-check adapter terminology across `specs/004-market-source-adapter/`, `docs/sources/market-source-adapter.md`, `docs/validation/market-source-adapter-validation.md`, and `src/market_signal_intelligence/sources/`
- [X] T051 [P] Verify all new adapter artifacts are listed in `docs/foundation/artifact-manifest.md` or justified by this task plan
- [X] T052 Run Python unit and integration tests from repository root with `python3 -m unittest discover tests`
- [X] T053 Run adapter validation from repository root with `scripts/validation/check-market-source-adapter.sh`
- [X] T054 Run existing market snapshot validation from repository root with `scripts/validation/check-market-snapshots.sh`
- [X] T055 Capture final validation evidence and command outputs in `specs/004-market-source-adapter/quickstart.md`
- [X] T056 Verify no Kafka, FastAPI endpoints, database persistence, AWS resources, dashboard work, AI analysis, multiple providers, scheduler, aggressive scraping, advisory language, ratings, targets, or recommendations were added and document result in `specs/004-market-source-adapter/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies; starts immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1; blocks all user story work.
- **Phase 3 (US1)**: Depends on Foundational; establishes MVP success path.
- **Phase 4 (US2)**: Depends on Foundational and benefits from US1 raw output samples.
- **Phase 5 (US3)**: Depends on Foundational; can proceed after shared adapter models exist.
- **Phase 6 (US4)**: Depends on Foundational; can proceed in parallel with US1-US3 after source behavior is stable enough to document.
- **Phase 7 (Polish)**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 (P1)**: MVP and no dependency on other user stories after Foundational.
- **US2 (P2)**: Requires adapter-produced raw snapshot behavior from US1 for full compatibility proof.
- **US3 (P3)**: Independent failure behavior after Foundational, but final validation should include US1 success fixtures.
- **US4 (P4)**: Documentation can start after Foundational and must be finalized after US1-US3 behavior is confirmed.

### Within Each User Story

- Write tests and fixtures first.
- Implement models/helpers before adapter behavior that depends on them.
- Add validation script checks after samples and implementation exist.
- Complete each checkpoint before treating the story as done.

### Parallel Opportunities

- T004 and T005 can run in parallel with source/test directory setup.
- T009 and T010 can run in parallel after shared paths exist.
- T015, T016, and T017 can run in parallel for US1.
- T024 and T025 can run in parallel for US2.
- T031 through T034 can run in parallel for US3 because they touch separate fixtures or an initial failure-test section.
- T050 and T051 can run in parallel during polish.

---

## Parallel Example: User Story 1

```bash
Task: "Create successful active equity source fixture in tests/fixtures/market-source-adapter/success-active-equity.json"
Task: "Add unit test for active watchlist ticker acceptance in tests/unit/test_market_source_adapter_success.py"
Task: "Add integration test for adapted raw snapshot validation in tests/integration/test_market_source_adapter_success_flow.py"
```

## Parallel Example: User Story 2

```bash
Task: "Add integration test for existing market snapshot validation reuse in tests/integration/test_market_source_adapter_snapshot_compatibility.py"
Task: "Add test that rejects provider-specific normalized schema files in tests/contract/test_no_provider_normalized_schema.py"
```

## Parallel Example: User Story 3

```bash
Task: "Create rate-limited source fixture in tests/fixtures/market-source-adapter/failure-rate-limited.json"
Task: "Create ticker-not-found source fixture in tests/fixtures/market-source-adapter/failure-ticker-not-found.json"
Task: "Create invalid response shape fixture in tests/fixtures/market-source-adapter/failure-invalid-shape.json"
Task: "Add unit tests for timeout and rate-limited classification in tests/unit/test_market_source_adapter_failures.py"
```

## Parallel Example: User Story 4

```bash
Task: "Add documentation guardrail test for prohibited provider, scheduler, advisory, and secret content in tests/unit/test_market_source_adapter_documentation.py"
Task: "Create source limitations and usage constraints documentation in docs/sources/market-source-adapter.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1) to deliver one successful controlled HTTP fetch path for an active watchlist ticker.
3. Validate US1 independently with unit, integration, and adapter validation checks.

### Incremental Delivery

1. Deliver setup and foundational models/contracts/rules.
2. Add US1 success path and adapted raw snapshot output.
3. Add US2 existing snapshot pipeline compatibility proof.
4. Add US3 deterministic failure classifications.
5. Add US4 source limitations and usage documentation.
6. Complete polish with full validation evidence and scope guardrail checks.

### Parallel Team Strategy

1. One contributor creates shared adapter models and validation docs while another prepares fixtures and contract tests.
2. After Foundational, split work by story: success path, compatibility proof, failure handling, and documentation.
3. Final reviewer runs validation scripts, checks artifact manifest coverage, and confirms no forbidden runtime/platform behavior was added.

---

## Notes

- All tasks use Python 3.12, Bash 5.2+, jq 1.7, and Python standard library only unless a later governed change explicitly approves another dependency.
- Do not add FastAPI endpoints, database persistence, Kafka, AWS resources, dashboards, AI analysis, multiple providers, production schedulers, or aggressive scraping.
- Do not create provider-specific normalized schemas or duplicate normalization logic.
- Keep all market values and source examples technical, technical, and .
- Invalid adapter samples must map to `MSA-REQ-*` rule IDs in `docs/validation/sample-rule-mapping.md`.
