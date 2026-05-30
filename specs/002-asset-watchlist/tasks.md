# Tasks: Initial Asset Watchlist

**Input**: Design documents from `/specs/002-asset-watchlist/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Contract and validation tasks are included because this feature is contract-first, traceability-critical, and must be reproducible locally without runtime services.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create artifact locations and establish the implementation surface for the equity-primary watchlist.

- [X] T001 Create watchlist and sample directories in `data/watchlists/`, `data/samples/watchlists/valid/`, and `data/samples/watchlists/invalid/`
- [X] T002 [P] Create watchlist validation guide in `docs/validation/asset-watchlist-validation.md`
- [X] T003 [P] Create validation script in `scripts/validation/check-asset-watchlist.sh`
- [X] T004 [P] Create root watchlist contract directory in `contracts/watchlists/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define shared contract, rule IDs, and manifest traceability before user-story implementation.

- [X] T005 Copy and adapt design schema from `specs/002-asset-watchlist/contracts/asset-watchlist.schema.json` into `contracts/watchlists/asset-watchlist.schema.json`
- [X] T006 Add watchlist artifact paths and minimum required sections to `docs/foundation/artifact-manifest.md`
- [X] T007 Add `WL-REQ-001` through `WL-REQ-010` watchlist rule IDs to `docs/validation/rule-ids.md`
- [X] T008 Define local validation commands, evidence format, and failure handling in `docs/validation/asset-watchlist-validation.md`
- [X] T009 Implement JSON syntax, path presence, equity-primary checks, and benchmark role checks in `scripts/validation/check-asset-watchlist.sh`

---

## Phase 3: User Story 1 - Establish Allowed Asset Baseline (Priority: P1) MVP

**Goal**: Deliver the canonical local Mexican equity watchlist artifact so future ingestion scope has governed individual monitoring targets.

**Independent Test**: From a clean checkout, a maintainer can open `data/watchlists/asset-watchlist.json` and identify the watchlist version, at least five active equity monitoring targets, any `IPC` reference benchmark, market metadata, and traceability context without external services.

### Tests for User Story 1

- [X] T010 [P] [US1] Add equity baseline manual review checklist to `docs/validation/asset-watchlist-validation.md`
- [X] T011 [P] [US1] Add contract validation scenario for equity-primary entries in `specs/002-asset-watchlist/contracts/test-watchlist-entries.md`

### Implementation for User Story 1

- [X] T012 [US1] Create canonical equity-primary watchlist artifact in `data/watchlists/asset-watchlist.json`
- [X] T013 [US1] Ensure `data/watchlists/asset-watchlist.json` contains `watchlist_id`, `version`, `effective_date`, `purpose`, and at least five active equity entries
- [X] T014 [US1] Ensure equity entries in `data/watchlists/asset-watchlist.json` use `asset_type` `equity`, `asset_role` `monitoring_target`, currency `MXN`, and BMV/Mexico metadata
- [X] T015 [US1] Add source reference and non-advisory review rationale in each `traceability` object of `data/watchlists/asset-watchlist.json`
- [X] T016 [US1] Ensure `IPC` in `data/watchlists/asset-watchlist.json` is only `asset_type` `index` and `asset_role` `reference_benchmark`

---

## Phase 4: User Story 2 - Validate Watchlist Changes (Priority: P2)

**Goal**: Provide validation rules and samples so contributors can identify valid and invalid watchlist changes locally.

**Independent Test**: A reviewer can use `docs/validation/asset-watchlist-validation.md`, the sample files, and `scripts/validation/check-asset-watchlist.sh` to classify valid and invalid samples with explicit rule IDs.

### Tests for User Story 2

- [X] T017 [P] [US2] Add valid sample expectation to `docs/validation/asset-watchlist-validation.md`
- [X] T018 [P] [US2] Add invalid sample rule-mapping expectation to `docs/validation/asset-watchlist-validation.md`

### Implementation for User Story 2

- [X] T019 [P] [US2] Create valid equity-primary sample in `data/samples/watchlists/valid/asset-watchlist-valid-equities.json`
- [X] T020 [P] [US2] Create missing-required-field invalid sample in `data/samples/watchlists/invalid/asset-watchlist-invalid-missing-required.json`
- [X] T021 [P] [US2] Create wrong-asset-type invalid sample in `data/samples/watchlists/invalid/asset-watchlist-invalid-wrong-asset-type.json`
- [X] T022 [P] [US2] Create advisory-content invalid sample in `data/samples/watchlists/invalid/asset-watchlist-invalid-advisory-content.json`
- [X] T023 [US2] Add watchlist invalid sample mappings to `docs/validation/sample-rule-mapping.md`
- [X] T024 [US2] Extend `scripts/validation/check-asset-watchlist.sh` to verify valid sample pass conditions in `data/samples/watchlists/valid/`
- [X] T025 [US2] Extend `scripts/validation/check-asset-watchlist.sh` to verify invalid sample failures and rule mappings in `data/samples/watchlists/invalid/`

---

## Phase 5: User Story 3 - Preserve Non-Advisory Traceability (Priority: P3)

**Goal**: Ensure the watchlist, samples, and validation guidance preserve traceability and cannot be mistaken for advice, live market data, or runtime ingestion behavior.

**Independent Test**: A reviewer can inspect the watchlist artifacts and run local validation to confirm source traceability, non-advisory language, and absence of live prices, ratings, recommendations, external API behavior, database work, endpoints, streaming, dashboard code, or AI analysis.

### Tests for User Story 3

- [X] T026 [P] [US3] Add non-advisory content scan expectations to `docs/validation/asset-watchlist-validation.md`
- [X] T027 [P] [US3] Add scope guardrail review checklist for watchlist artifacts in `docs/validation/asset-watchlist-validation.md`

### Implementation for User Story 3

- [X] T028 [US3] Extend `scripts/validation/check-asset-watchlist.sh` to reject prohibited advisory phrases and live-price fields in `data/watchlists/asset-watchlist.json`
- [X] T029 [US3] Extend `scripts/validation/check-asset-watchlist.sh` to reject prohibited advisory phrases and live-price fields in `data/samples/watchlists/`
- [X] T030 [US3] Document traceability review requirements for equity and benchmark source references in `docs/validation/asset-watchlist-validation.md`
- [X] T031 [US3] Document explicit no-runtime exclusions for this feature in `docs/validation/asset-watchlist-validation.md`

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, reproducibility, and review readiness across all stories.

- [X] T032 [P] Update `specs/002-asset-watchlist/quickstart.md` with final validation command output expectations
- [X] T033 [P] Cross-check equity and benchmark terminology across `data/watchlists/asset-watchlist.json`, `docs/validation/asset-watchlist-validation.md`, and `contracts/watchlists/asset-watchlist.schema.json`
- [X] T034 Run `scripts/validation/check-asset-watchlist.sh` from repository root and capture pass/fail evidence in `specs/002-asset-watchlist/quickstart.md`
- [X] T035 Verify all new watchlist artifacts are listed in `docs/foundation/artifact-manifest.md` or justified by this task plan
- [X] T036 Verify no runtime application behavior was added and document the review result in `specs/002-asset-watchlist/quickstart.md`

---

## Phase 7: Domain Scope Correction

**Purpose**: Correct the domain ambiguity that previously treated the IPC index as the sole monitoring target.

- [X] T037 Update feature specification to make individual Mexican equities the primary monitoring targets in `specs/002-asset-watchlist/spec.md`
- [X] T038 Update plan, research, and data model to describe equity-primary scope in `specs/002-asset-watchlist/plan.md`, `specs/002-asset-watchlist/research.md`, and `specs/002-asset-watchlist/data-model.md`
- [X] T039 Update canonical watchlist with multiple equity monitoring targets and optional IPC benchmark in `data/watchlists/asset-watchlist.json`
- [X] T040 Update schema and validation script for equity-primary constraints in `contracts/watchlists/asset-watchlist.schema.json` and `scripts/validation/check-asset-watchlist.sh`
- [X] T041 Update samples, rule mappings, manifest, quickstart, and validation guide for corrected scope in `data/samples/watchlists/`, `docs/validation/`, `docs/foundation/artifact-manifest.md`, and `specs/002-asset-watchlist/quickstart.md`

---

## Dependencies & Execution Order

- Phase 1 precedes Phase 2.
- Phase 2 blocks all user story work.
- US1 is the MVP and establishes the canonical watchlist.
- US2 validates samples and rule mappings after shared rules exist.
- US3 confirms traceability and no-runtime guardrails.
- Phase 7 corrects the domain interpretation while staying within the same feature scope.

## Implementation Strategy

### MVP First

Complete Phase 1, Phase 2, and US1 so the repository has a concrete equity-primary allowlist.

### Incremental Delivery

Add samples and validation after the canonical watchlist, then finish with non-advisory and no-runtime checks.

## Notes

- All tasks are documentation, contract, sample data, validation guidance, or local validation scripting tasks only.
- Do not add live price fetching, scraping, external API calls, ingestion runtime, Kafka producers, FastAPI endpoints, databases, dashboard code, or AI analysis.
- Invalid watchlist samples must map to explicit `WL-REQ-*` rule IDs in `docs/validation/sample-rule-mapping.md`.
- Local validation must remain reproducible from a clean clone without network access or deployed infrastructure.
