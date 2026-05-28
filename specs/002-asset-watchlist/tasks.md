# Tasks: Initial Asset Watchlist

**Input**: Design documents from `/specs/002-asset-watchlist/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Contract and validation tasks are included because this feature is contract-first, traceability-critical, and must be reproducible locally without runtime services.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create artifact locations and establish the implementation surface for the IPC-only watchlist.

- [ ] T001 Create watchlist and sample directories in `data/watchlists/`, `data/samples/watchlists/valid/`, and `data/samples/watchlists/invalid/`
- [ ] T002 [P] Create watchlist validation guide stub in `docs/validation/asset-watchlist-validation.md`
- [ ] T003 [P] Create validation script stub in `scripts/validation/check-asset-watchlist.sh`
- [ ] T004 [P] Create root watchlist contract directory in `contracts/watchlists/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define shared contract, rule IDs, and manifest traceability before user-story implementation.

**CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T005 Copy and adapt design schema from `specs/002-asset-watchlist/contracts/asset-watchlist.schema.json` into `contracts/watchlists/asset-watchlist.schema.json`
- [ ] T006 Add watchlist artifact paths and minimum required sections to `docs/foundation/artifact-manifest.md`
- [ ] T007 Add `WL-REQ-001` through `WL-REQ-010` watchlist rule IDs to `docs/validation/rule-ids.md`
- [ ] T008 Define local validation commands, evidence format, and failure handling in `docs/validation/asset-watchlist-validation.md`
- [ ] T009 Implement JSON syntax, path presence, and IPC-only structural checks in `scripts/validation/check-asset-watchlist.sh`

**Checkpoint**: Watchlist contract, rule IDs, manifest traceability, and validation entry point are defined.

---

## Phase 3: User Story 1 - Establish Allowed Asset Baseline (Priority: P1) MVP

**Goal**: Deliver the canonical local IPC watchlist artifact so future ingestion scope has one governed active asset.

**Independent Test**: From a clean checkout, a maintainer can open `data/watchlists/asset-watchlist.json` and identify the watchlist version, active `IPC` entry, display name `S&P/BMV IPC`, asset type `index`, currency `MXN`, market metadata, and traceability context without external services.

### Tests for User Story 1

- [ ] T010 [P] [US1] Add IPC baseline manual review checklist to `docs/validation/asset-watchlist-validation.md`
- [ ] T011 [P] [US1] Add contract validation scenario for the canonical IPC entry in `specs/002-asset-watchlist/contracts/test-ipc-entry.md`

### Implementation for User Story 1

- [ ] T012 [US1] Create canonical IPC watchlist artifact in `data/watchlists/asset-watchlist.json`
- [ ] T013 [US1] Ensure `data/watchlists/asset-watchlist.json` contains `watchlist_id`, `version`, `effective_date`, `purpose`, and exactly one active `IPC` asset entry
- [ ] T014 [US1] Ensure the `IPC` entry in `data/watchlists/asset-watchlist.json` uses display name `S&P/BMV IPC`, asset type `index`, currency `MXN`, and BMV/Mexico market metadata
- [ ] T015 [US1] Add source reference and non-advisory review rationale in the `traceability` object of `data/watchlists/asset-watchlist.json`
- [ ] T016 [US1] Extend `scripts/validation/check-asset-watchlist.sh` to verify the canonical active `IPC` entry in `data/watchlists/asset-watchlist.json`

**Checkpoint**: US1 is independently reviewable as the minimal watchlist MVP.

---

## Phase 4: User Story 2 - Validate Watchlist Changes (Priority: P2)

**Goal**: Provide validation rules and samples so contributors can identify valid and invalid watchlist changes locally.

**Independent Test**: A reviewer can use `docs/validation/asset-watchlist-validation.md`, the sample files, and `scripts/validation/check-asset-watchlist.sh` to classify valid and invalid samples with explicit rule IDs.

### Tests for User Story 2

- [ ] T017 [P] [US2] Add valid sample expectation to `docs/validation/asset-watchlist-validation.md`
- [ ] T018 [P] [US2] Add invalid sample rule-mapping expectation to `docs/validation/asset-watchlist-validation.md`

### Implementation for User Story 2

- [ ] T019 [P] [US2] Create valid IPC sample in `data/samples/watchlists/valid/asset-watchlist-valid-ipc.json`
- [ ] T020 [P] [US2] Create missing-required-field invalid sample in `data/samples/watchlists/invalid/asset-watchlist-invalid-missing-required.json`
- [ ] T021 [P] [US2] Create wrong-asset-type invalid sample in `data/samples/watchlists/invalid/asset-watchlist-invalid-wrong-asset-type.json`
- [ ] T022 [P] [US2] Create advisory-content invalid sample in `data/samples/watchlists/invalid/asset-watchlist-invalid-advisory-content.json`
- [ ] T023 [US2] Add watchlist invalid sample mappings to `docs/validation/sample-rule-mapping.md`
- [ ] T024 [US2] Extend `scripts/validation/check-asset-watchlist.sh` to verify valid sample pass conditions in `data/samples/watchlists/valid/`
- [ ] T025 [US2] Extend `scripts/validation/check-asset-watchlist.sh` to verify invalid sample failures and rule mappings in `data/samples/watchlists/invalid/`

**Checkpoint**: US2 is independently testable through samples and rule-ID mappings.

---

## Phase 5: User Story 3 - Preserve Non-Advisory Traceability (Priority: P3)

**Goal**: Ensure the watchlist, samples, and validation guidance preserve traceability and cannot be mistaken for advice, live market data, or runtime ingestion behavior.

**Independent Test**: A reviewer can inspect the watchlist artifacts and run local validation to confirm source traceability, non-advisory language, and absence of live prices, ratings, recommendations, external API behavior, database work, endpoints, streaming, dashboard code, or AI analysis.

### Tests for User Story 3

- [ ] T026 [P] [US3] Add non-advisory content scan expectations to `docs/validation/asset-watchlist-validation.md`
- [ ] T027 [P] [US3] Add scope guardrail review checklist for watchlist artifacts in `docs/validation/asset-watchlist-validation.md`

### Implementation for User Story 3

- [ ] T028 [US3] Extend `scripts/validation/check-asset-watchlist.sh` to reject prohibited advisory phrases and live-price fields in `data/watchlists/asset-watchlist.json`
- [ ] T029 [US3] Extend `scripts/validation/check-asset-watchlist.sh` to reject prohibited advisory phrases and live-price fields in `data/samples/watchlists/`
- [ ] T030 [US3] Document traceability review requirements for IPC source references in `docs/validation/asset-watchlist-validation.md`
- [ ] T031 [US3] Document explicit no-runtime exclusions for this feature in `docs/validation/asset-watchlist-validation.md`

**Checkpoint**: US3 independently enforces non-advisory, traceable, no-runtime delivery boundaries.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, reproducibility, and review readiness across all stories.

- [ ] T032 [P] Update `specs/002-asset-watchlist/quickstart.md` with final validation command output expectations
- [ ] T033 [P] Cross-check IPC terminology across `data/watchlists/asset-watchlist.json`, `docs/validation/asset-watchlist-validation.md`, and `contracts/watchlists/asset-watchlist.schema.json`
- [ ] T034 Run `scripts/validation/check-asset-watchlist.sh` from repository root and capture pass/fail evidence in `specs/002-asset-watchlist/quickstart.md`
- [ ] T035 Verify all new watchlist artifacts are listed in `docs/foundation/artifact-manifest.md` or justified by this task plan
- [ ] T036 Verify no runtime application behavior was added and document the review result in `specs/002-asset-watchlist/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: starts immediately.
- **Phase 2 (Foundational)**: depends on Phase 1 and blocks all user stories.
- **Phase 3 (US1)**: depends on Phase 2 and is the MVP.
- **Phase 4 (US2)**: depends on Phase 2; can start after shared validation rules exist, but benefits from US1 canonical artifact.
- **Phase 5 (US3)**: depends on Phase 2; can run after US1 and US2 artifacts exist for complete scope scanning.
- **Phase 6 (Polish)**: depends on desired user stories being complete.

### User Story Dependencies

- **US1 (P1)**: no dependency on other user stories after Foundational.
- **US2 (P2)**: uses rule IDs and validation docs from Foundational; sample validation references US1 constraints.
- **US3 (P3)**: uses watchlist and sample artifacts from US1 and US2 for complete non-advisory checks.

### Within Each User Story

- Validation expectations before implementation changes.
- Canonical artifact before script checks that validate it.
- Samples before invalid sample mapping validation.
- Documentation updates before final quickstart evidence.

### Parallel Opportunities

- T002, T003, and T004 can run in parallel after T001.
- T006 and T007 can run in parallel with T005.
- T010 and T011 can run in parallel for US1.
- T019, T020, T021, and T022 can run in parallel for US2 after validation rules exist.
- T026 and T027 can run in parallel for US3.
- T032 and T033 can run in parallel during polish.

---

## Parallel Example: User Story 2

```bash
Task: "Create valid IPC sample in data/samples/watchlists/valid/asset-watchlist-valid-ipc.json"
Task: "Create missing-required-field invalid sample in data/samples/watchlists/invalid/asset-watchlist-invalid-missing-required.json"
Task: "Create wrong-asset-type invalid sample in data/samples/watchlists/invalid/asset-watchlist-invalid-wrong-asset-type.json"
Task: "Create advisory-content invalid sample in data/samples/watchlists/invalid/asset-watchlist-invalid-advisory-content.json"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 for the canonical IPC watchlist artifact.
3. Validate that `data/watchlists/asset-watchlist.json` has exactly one active `IPC` entry with required metadata and traceability.
4. Stop and review before expanding validation samples.

### Incremental Delivery

1. Deliver setup and foundational contract/rule infrastructure.
2. Deliver US1 canonical IPC watchlist artifact.
3. Deliver US2 validation samples and rule mappings.
4. Deliver US3 non-advisory and no-runtime guardrails.
5. Finish with quickstart evidence and manifest consistency checks.

### Parallel Team Strategy

1. One contributor prepares contract/rule documentation while another prepares validation script scaffolding.
2. After Foundational, one contributor completes US1, another drafts sample files for US2, and another drafts US3 guardrail documentation.
3. Merge through Phase 6 validation and terminology consistency checks.

---

## Notes

- All tasks are documentation, contract, sample data, validation guidance, or local validation scripting tasks only.
- Do not add live price fetching, scraping, external API calls, ingestion runtime, Kafka producers, FastAPI endpoints, databases, dashboard code, or AI analysis.
- Invalid watchlist samples must map to explicit `WL-REQ-*` rule IDs in `docs/validation/sample-rule-mapping.md`.
- Local validation must remain reproducible from a clean clone without network access or deployed infrastructure.
