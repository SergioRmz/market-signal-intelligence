# Tasks: Initial Project Foundation

**Input**: Design documents from `/specs/001-project-foundation/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Contract and integration tests are REQUIRED for constitution-critical work (event contracts and reproducibility validation workflow).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create baseline directories and anchor files used by all stories.

- [x] T001 Create foundation directories in `docs/architecture/`, `docs/policies/`, `docs/validation/`, `contracts/events/`, `data/samples/asset-events/valid/`, and `data/samples/asset-events/invalid/`
- [x] T002 Create initial root docs stubs in `README.md` and `AGENTS.md` aligned with current spec context
- [x] T003 [P] Create foundation spec support index in `docs/foundation/README.md` referencing governed artifact paths

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define shared contract, governance, and validation baselines before story-specific completion.

**CRITICAL**: No user story can be considered complete before this phase is done.

- [x] T004 Define artifact manifest with required sections in `docs/foundation/artifact-manifest.md`
- [x] T005 [P] Define architecture baseline sections in `docs/architecture/foundation-architecture.md`
- [x] T006 [P] Define allowed source categories and criteria in `docs/policies/allowed-sources.md`
- [x] T007 Define base AssetEvent JSON Schema with required fields in `contracts/events/asset-event.schema.json`
- [x] T008 Define lightweight validation procedure and evidence format in `docs/validation/event-contract-validation.md`
- [x] T009 [P] Create rule ID registry for contract/policy violations in `docs/validation/rule-ids.md`

**Checkpoint**: Shared foundation and contract guardrails are defined.

---

## Phase 3: User Story 1 - Establish Foundation Baseline (Priority: P1) 🎯 MVP

**Goal**: Deliver complete, readable baseline artifacts for maintainers and contributors.

**Independent Test**: From a clean clone, a reviewer can locate all required artifact paths and verify each has required sections without external context.

### Tests for User Story 1 (REQUIRED) ⚠️

- [x] T010 [P] [US1] Add artifact-presence check script in `scripts/validation/check-foundation-artifacts.sh`
- [x] T011 [P] [US1] Add integration review checklist for onboarding flow in `docs/validation/us1-independent-test.md`

### Implementation for User Story 1

- [x] T012 [US1] Complete project purpose, scope, non-goals, disclaimer, planned stack, and methodology in `README.md`
- [x] T013 [US1] Complete agent operating guidance in `AGENTS.md`
- [x] T014 [US1] Complete artifact manifest section requirements in `docs/foundation/artifact-manifest.md`
- [x] T015 [US1] Add maintainer review procedure for baseline acceptance in `docs/validation/us1-review-procedure.md`

**Checkpoint**: US1 is independently testable and reviewable.

---

## Phase 4: User Story 2 - Safeguard Scope Before Build (Priority: P2)

**Goal**: Enforce explicit non-goals and prevent premature runtime implementation.

**Independent Test**: Reviewer can apply a documented guardrail checklist and reject any out-of-scope runtime additions.

### Tests for User Story 2 (REQUIRED) ⚠️

- [x] T016 [P] [US2] Add scope-guardrail validation checklist in `docs/validation/us2-scope-guardrail-checklist.md`
- [x] T017 [P] [US2] Add prohibited-change examples and expected review outcomes in `docs/validation/us2-negative-scenarios.md`

### Implementation for User Story 2

- [x] T018 [US2] Document explicit out-of-scope implementation boundaries in `README.md`
- [x] T019 [US2] Document contributor enforcement process for non-goals in `AGENTS.md`
- [x] T020 [US2] Document scaffolding-allowed vs runtime-not-allowed matrix in `docs/foundation/scaffolding-boundaries.md`
- [x] T021 [US2] Add PR evidence template for scope-compliance confirmation in `.github/pull_request_template.md`

**Checkpoint**: US2 independently prevents scope drift.

---

## Phase 5: User Story 3 - Enable Contract-First Collaboration (Priority: P3)

**Goal**: Establish contract-first event schema, sample set, and reproducible local validation.

**Independent Test**: Reviewer can validate sample classification (2 valid, 3 invalid) against schema and documented violated rules using local instructions.

### Tests for User Story 3 (REQUIRED) ⚠️

- [x] T022 [P] [US3] Add contract test scenario document for required AssetEvent fields in `specs/001-project-foundation/contracts/test-required-fields.md`
- [x] T023 [P] [US3] Add integration validation runbook for clean-clone execution in `specs/001-project-foundation/contracts/test-validation-runbook.md`
- [x] T024 [P] [US3] Add reproducibility verification checklist in `docs/validation/us3-reproducibility-checklist.md`

### Implementation for User Story 3

- [x] T025 [US3] Finalize required top-level and nested fields in `contracts/events/asset-event.schema.json`
- [x] T026 [P] [US3] Create first valid sample in `data/samples/asset-events/valid/asset-event-valid-01.json`
- [x] T027 [P] [US3] Create second valid sample in `data/samples/asset-events/valid/asset-event-valid-02.json`
- [x] T028 [P] [US3] Create first invalid sample with rule mapping in `data/samples/asset-events/invalid/asset-event-invalid-01-missing-required.json`
- [x] T029 [P] [US3] Create second invalid sample with rule mapping in `data/samples/asset-events/invalid/asset-event-invalid-02-bad-source-category.json`
- [x] T030 [P] [US3] Create third invalid sample with rule mapping in `data/samples/asset-events/invalid/asset-event-invalid-03-invalid-timestamp.json`
- [x] T031 [US3] Document per-sample violated rule IDs in `docs/validation/sample-rule-mapping.md`
- [x] T032 [US3] Finalize lightweight local validation commands and PR evidence steps in `docs/validation/event-contract-validation.md`

**Checkpoint**: US3 independently provides contract-first collaboration baseline.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, traceability, and review readiness across all stories.

- [x] T033 [P] Cross-check terminology consistency across `README.md`, `AGENTS.md`, `docs/`, `contracts/`, and `specs/001-project-foundation/`
- [x] T034 [P] Verify all required artifact sections from `docs/foundation/artifact-manifest.md` are complete
- [x] T035 Run end-to-end quickstart validation and capture final evidence in `specs/001-project-foundation/quickstart.md`
- [x] T036 Prepare final reviewer handoff notes in `docs/validation/foundation-review-handoff.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: starts immediately
- **Phase 2 (Foundational)**: depends on Phase 1
- **Phase 3-5 (User Stories)**: depend on Phase 2 completion
- **Phase 6 (Polish)**: depends on completion of desired user stories

### User Story Dependencies

- **US1 (P1)**: starts after Foundational and defines MVP baseline
- **US2 (P2)**: starts after Foundational; independent from US1 outputs except shared docs
- **US3 (P3)**: starts after Foundational; depends on base schema/policy artifacts from Phase 2

### Within Each User Story

- Validation/test tasks first
- Documentation/contract implementation next
- Evidence and handoff tasks last

### Parallel Opportunities

- Phase 1: T003 parallel with T001/T002 after directories exist
- Phase 2: T005, T006, T009 parallel
- US1: T010 and T011 parallel; T012 and T013 parallel
- US2: T016 and T017 parallel; T018 and T019 parallel
- US3: T022/T023/T024 parallel; T026-T030 parallel sample creation
- Phase 6: T033 and T034 parallel

---

## Parallel Example: User Story 3

```bash
# Parallel test docs
Task: "Add contract test scenario document in specs/001-project-foundation/contracts/test-required-fields.md"
Task: "Add integration validation runbook in specs/001-project-foundation/contracts/test-validation-runbook.md"
Task: "Add reproducibility checklist in docs/validation/us3-reproducibility-checklist.md"

# Parallel sample creation
Task: "Create valid sample 01 in data/samples/asset-events/valid/asset-event-valid-01.json"
Task: "Create valid sample 02 in data/samples/asset-events/valid/asset-event-valid-02.json"
Task: "Create invalid samples 01-03 in data/samples/asset-events/invalid/"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1).
3. Validate US1 independently using T010-T011.

### Incremental Delivery

1. Deliver US1 baseline artifacts.
2. Add US2 guardrails and enforcement docs.
3. Add US3 contract + samples + validation evidence flow.
4. Finish with Phase 6 polish.

### Parallel Team Strategy

1. One contributor handles Phase 2 architecture/policy while another defines validation/rule IDs.
2. After Phase 2, split by story owner (US1, US2, US3).
3. Merge with Phase 6 consistency pass.

---

## Notes

- All tasks follow required checklist format: `- [ ] T### [P] [US#] Description with file path`.
- No runtime application code is included in this task plan.
- Contract/integration validation tasks are included due to constitution-critical scope.
