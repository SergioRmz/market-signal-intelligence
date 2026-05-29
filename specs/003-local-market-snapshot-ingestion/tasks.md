# Tasks: Local Market Snapshot Ingestion

**Input**: Design documents from `/specs/003-local-market-snapshot-ingestion/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Contract and validation tasks are included because this feature is contract-first, traceability-critical, and must be reproducible locally without runtime services.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create repository-local artifact locations for market snapshot contracts, samples, validation guidance, and local validation.

- [ ] T001 Create snapshot contract directory in `contracts/market-snapshots/`
- [ ] T002 Create raw snapshot sample directories in `data/samples/market-snapshots/raw/valid/` and `data/samples/market-snapshots/raw/invalid/`
- [ ] T003 Create normalized snapshot sample directories in `data/samples/market-snapshots/normalized/valid/` and `data/samples/market-snapshots/normalized/invalid/`
- [ ] T004 [P] Create market snapshot validation guide in `docs/validation/market-snapshot-validation.md`
- [ ] T005 [P] Create local snapshot validation script in `scripts/validation/check-market-snapshots.sh`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared contracts, rule IDs, manifest traceability, and base validation behavior before user-story sample work.

**CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T006 Copy raw planning contract from `specs/003-local-market-snapshot-ingestion/contracts/raw-market-snapshot.schema.json` to `contracts/market-snapshots/raw-market-snapshot.schema.json`
- [ ] T007 Copy normalized planning contract from `specs/003-local-market-snapshot-ingestion/contracts/normalized-market-snapshot.schema.json` to `contracts/market-snapshots/normalized-market-snapshot.schema.json`
- [ ] T008 Add `MS-REQ-001` through `MS-REQ-010` snapshot rule IDs to `docs/validation/rule-ids.md`
- [ ] T009 Add market snapshot artifact paths and minimum required sections to `docs/foundation/artifact-manifest.md`
- [ ] T010 Define local commands, rule IDs, evidence format, failure handling, and no-runtime guardrails in `docs/validation/market-snapshot-validation.md`
- [ ] T011 Implement required path checks and JSON parse checks in `scripts/validation/check-market-snapshots.sh`
- [ ] T012 Extend `scripts/validation/check-market-snapshots.sh` to reject prohibited advisory terms, live-feed fields, external API references, scraping references, Kafka references, database references, FastAPI references, AWS references, and AI references in `data/samples/market-snapshots/`

**Checkpoint**: Contracts, rule IDs, manifest entries, and baseline validation are ready.

---

## Phase 3: User Story 1 - Ingest Local Sample Snapshots (Priority: P1) MVP

**Goal**: Deliver valid and invalid raw snapshot samples that demonstrate local sample-only ingestion readiness and active watchlist gating.

**Independent Test**: A maintainer can review raw snapshot samples and confirm valid samples are static local inputs for active canonical watchlist symbols while invalid samples demonstrate rejected inputs.

### Tests for User Story 1

- [ ] T013 [P] [US1] Add raw snapshot contract review scenario in `specs/003-local-market-snapshot-ingestion/contracts/test-raw-market-snapshot.md`
- [ ] T014 [P] [US1] Add raw sample independent review checklist in `docs/validation/market-snapshot-validation.md`

### Implementation for User Story 1

- [ ] T015 [P] [US1] Create first valid raw equity snapshot sample in `data/samples/market-snapshots/raw/valid/raw-market-snapshot-valid-01-equity.json`
- [ ] T016 [P] [US1] Create second valid raw equity snapshot sample in `data/samples/market-snapshots/raw/valid/raw-market-snapshot-valid-02-equity.json`
- [ ] T017 [P] [US1] Create invalid raw snapshot for missing watchlist asset in `data/samples/market-snapshots/raw/invalid/raw-market-snapshot-invalid-01-missing-watchlist-asset.json`
- [ ] T018 [P] [US1] Create invalid raw snapshot for inactive watchlist asset in `data/samples/market-snapshots/raw/invalid/raw-market-snapshot-invalid-02-inactive-watchlist-asset.json`
- [ ] T019 [P] [US1] Create invalid raw snapshot for malformed required fields in `data/samples/market-snapshots/raw/invalid/raw-market-snapshot-invalid-03-malformed-required-fields.json`
- [ ] T020 [US1] Document raw snapshot invalid sample mappings in `docs/validation/sample-rule-mapping.md`
- [ ] T021 [US1] Extend `scripts/validation/check-market-snapshots.sh` to validate raw sample required fields, canonical symbol usage, active watchlist membership, and observed values in `data/samples/market-snapshots/raw/`

**Checkpoint**: US1 is independently testable through raw sample review and local validation.

---

## Phase 4: User Story 2 - Separate Raw and Normalized Snapshots (Priority: P2)

**Goal**: Deliver normalized snapshot samples that remain separate from raw snapshots and preserve a required `raw_snapshot_id` provenance link.

**Independent Test**: A reviewer can compare normalized samples to raw samples and confirm every valid normalized sample uses canonical watchlist identity and traces back to a valid raw sample by `raw_snapshot_id`.

### Tests for User Story 2

- [ ] T022 [P] [US2] Add normalized snapshot contract review scenario in `specs/003-local-market-snapshot-ingestion/contracts/test-normalized-market-snapshot.md`
- [ ] T023 [P] [US2] Add raw-to-normalized provenance review checklist in `docs/validation/market-snapshot-validation.md`

### Implementation for User Story 2

- [ ] T024 [P] [US2] Create first valid normalized equity snapshot sample in `data/samples/market-snapshots/normalized/valid/normalized-market-snapshot-valid-01-equity.json`
- [ ] T025 [P] [US2] Create second valid normalized equity snapshot sample in `data/samples/market-snapshots/normalized/valid/normalized-market-snapshot-valid-02-equity.json`
- [ ] T026 [P] [US2] Create invalid normalized snapshot missing raw provenance in `data/samples/market-snapshots/normalized/invalid/normalized-market-snapshot-invalid-01-missing-raw-snapshot-id.json`
- [ ] T027 [P] [US2] Create invalid normalized snapshot using exchange symbol variant in `data/samples/market-snapshots/normalized/invalid/normalized-market-snapshot-invalid-02-exchange-symbol-variant.json`
- [ ] T028 [US2] Document normalized snapshot invalid sample mappings in `docs/validation/sample-rule-mapping.md`
- [ ] T029 [US2] Extend `scripts/validation/check-market-snapshots.sh` to validate normalized sample required fields, canonical symbol usage, `raw_snapshot_id` links, and observed values in `data/samples/market-snapshots/normalized/`

**Checkpoint**: US2 is independently testable through raw/normalized comparison and provenance validation.

---

## Phase 5: User Story 3 - Validate Snapshot Readiness Locally (Priority: P3)

**Goal**: Provide lightweight local validation and review evidence so contributors can classify all snapshot samples without adding runtime integrations.

**Independent Test**: A contributor can run the local validation script and use repository-local guidance to classify valid and invalid snapshot samples with explicit `MS-REQ-*` rule mappings.

### Tests for User Story 3

- [ ] T030 [P] [US3] Add clean-clone validation runbook expectations to `specs/003-local-market-snapshot-ingestion/quickstart.md`
- [ ] T031 [P] [US3] Add validation evidence checklist and no-runtime scope checklist to `docs/validation/market-snapshot-validation.md`

### Implementation for User Story 3

- [ ] T032 [P] [US3] Create invalid raw snapshot with prohibited advisory or live-feed content in `data/samples/market-snapshots/raw/invalid/raw-market-snapshot-invalid-04-prohibited-content.json`
- [ ] T033 [US3] Add prohibited content invalid sample mapping to `docs/validation/sample-rule-mapping.md`
- [ ] T034 [US3] Extend `scripts/validation/check-market-snapshots.sh` to verify valid sample counts, invalid sample counts, and `MS-REQ-*` mappings in `docs/validation/sample-rule-mapping.md`
- [ ] T035 [US3] Extend `scripts/validation/check-market-snapshots.sh` to print `PASS: Local market snapshot contracts and samples validated` when all snapshot checks pass
- [ ] T036 [US3] Update `docs/validation/market-snapshot-validation.md` with final local validation command, expected output, evidence format, and failure handling

**Checkpoint**: US3 is independently testable through the local validation command and evidence checklist.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, documentation review, and reproducibility evidence across all stories.

- [ ] T037 [P] Update `specs/003-local-market-snapshot-ingestion/quickstart.md` with final validation evidence and sample counts
- [ ] T038 [P] Cross-check snapshot terminology across `contracts/market-snapshots/`, `docs/validation/market-snapshot-validation.md`, and `data/samples/market-snapshots/`
- [ ] T039 [P] Review `README.md` for project-wide snapshot usage or validation guidance needs and update `README.md` only if needed
- [ ] T040 [P] Review `AGENTS.md` for project-wide snapshot agent guidance needs and update `AGENTS.md` only if needed
- [ ] T041 Document README and AGENTS review outcome in `specs/003-local-market-snapshot-ingestion/quickstart.md`
- [ ] T042 Run `scripts/validation/check-market-snapshots.sh` from repository root and capture pass/fail evidence in `specs/003-local-market-snapshot-ingestion/quickstart.md`
- [ ] T043 Verify all new snapshot artifacts are listed in `docs/foundation/artifact-manifest.md` or justified by this task plan
- [ ] T044 Verify no runtime ingestion, external API, scraping, Kafka, database, FastAPI, AWS, dashboard, AI, or live-feed behavior was added and document the result in `specs/003-local-market-snapshot-ingestion/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies; starts immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1; blocks all user story work.
- **Phase 3 (US1)**: Depends on Phase 2; establishes MVP raw sample ingestion baseline.
- **Phase 4 (US2)**: Depends on Phase 2 and benefits from US1 raw samples for provenance links.
- **Phase 5 (US3)**: Depends on Phase 2 and validates artifacts from US1 and US2.
- **Phase 6 (Polish)**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational; no dependency on US2 or US3.
- **US2 (P2)**: Can start after Foundational, but valid normalized samples should reference raw samples created by US1.
- **US3 (P3)**: Can start after Foundational, but final validation depends on US1 and US2 sample sets.

### Within Each User Story

- Contract/review scenario tasks first.
- Sample artifacts next.
- Rule mapping and validation script tasks after sample artifacts.
- Checkpoint validation before moving to the next story.

### Parallel Opportunities

- T004 and T005 can run in parallel after directories exist.
- T013 and T014 can run in parallel for US1.
- T015 through T019 can run in parallel because they create separate files.
- T022 and T023 can run in parallel for US2.
- T024 through T027 can run in parallel because they create separate files.
- T030 and T031 can run in parallel for US3.
- T037 through T040 can run in parallel during polish because they touch separate files.

---

## Parallel Example: User Story 1

```bash
Task: "Add raw snapshot contract review scenario in specs/003-local-market-snapshot-ingestion/contracts/test-raw-market-snapshot.md"
Task: "Add raw sample independent review checklist in docs/validation/market-snapshot-validation.md"
Task: "Create first valid raw equity snapshot sample in data/samples/market-snapshots/raw/valid/raw-market-snapshot-valid-01-equity.json"
Task: "Create second valid raw equity snapshot sample in data/samples/market-snapshots/raw/valid/raw-market-snapshot-valid-02-equity.json"
Task: "Create missing asset invalid raw sample in data/samples/market-snapshots/raw/invalid/raw-market-snapshot-invalid-01-missing-watchlist-asset.json"
```

## Parallel Example: User Story 2

```bash
Task: "Add normalized snapshot contract review scenario in specs/003-local-market-snapshot-ingestion/contracts/test-normalized-market-snapshot.md"
Task: "Create first valid normalized equity snapshot sample in data/samples/market-snapshots/normalized/valid/normalized-market-snapshot-valid-01-equity.json"
Task: "Create second valid normalized equity snapshot sample in data/samples/market-snapshots/normalized/valid/normalized-market-snapshot-valid-02-equity.json"
Task: "Create missing raw provenance invalid normalized sample in data/samples/market-snapshots/normalized/invalid/normalized-market-snapshot-invalid-01-missing-raw-snapshot-id.json"
```

## Parallel Example: User Story 3

```bash
Task: "Add clean-clone validation runbook expectations to specs/003-local-market-snapshot-ingestion/quickstart.md"
Task: "Add validation evidence checklist and no-runtime scope checklist to docs/validation/market-snapshot-validation.md"
Task: "Create prohibited content invalid raw sample in data/samples/market-snapshots/raw/invalid/raw-market-snapshot-invalid-04-prohibited-content.json"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1) to deliver the raw local sample ingestion baseline.
3. Validate US1 independently using raw sample review and local checks.

### Incremental Delivery

1. Deliver setup and foundational contracts/rules.
2. Add US1 raw samples and active watchlist validation.
3. Add US2 normalized samples and `raw_snapshot_id` provenance validation.
4. Add US3 full local validation, invalid sample coverage, and evidence workflow.
5. Complete polish with conditional README/AGENTS review and quickstart evidence.

### Parallel Team Strategy

1. One contributor handles contracts and manifest updates while another prepares validation guidance.
2. After Foundational, split sample creation by story and file path.
3. Finish with one reviewer validating sample mappings, guardrails, and quickstart evidence.

---

## Notes

- All tasks are documentation, contract, sample data, validation guidance, or local validation scripting tasks only.
- Do not add runtime ingestion logic, external APIs, scraping, Kafka, databases, FastAPI endpoints, AWS resources, dashboard code, AI analysis, or live market data behavior.
- Invalid snapshot samples must map to explicit `MS-REQ-*` rule IDs in `docs/validation/sample-rule-mapping.md`.
- Local validation must remain reproducible from a clean clone without network access or deployed infrastructure.
