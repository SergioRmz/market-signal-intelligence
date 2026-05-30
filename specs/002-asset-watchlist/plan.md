# Implementation Plan: Initial Asset Watchlist

**Branch**: `002-asset-watchlist` | **Date**: 2026-05-27 | **Spec**: `specs/002-asset-watchlist/spec.md`

**Input**: Feature specification from `specs/002-asset-watchlist/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Define an equity-primary Mexican market asset watchlist foundation so later ingestion features have a small, explicit, versioned allowlist before any live data behavior exists. The plan delivers a local JSON watchlist artifact path, design-time schema contract, sample-data expectations, validation rules, rule-ID mapping, and documentation updates while preserving non-advisory and no-runtime boundaries. `S&P/BMV IPC` may appear only as a reference benchmark, not as a replacement for individual equity monitoring targets.

## Technical Context

**Language/Version**: Markdown + JSON artifacts; JSON Schema Draft 2020-12 for design contract

**Primary Dependencies**: None beyond repository-local tooling and git

**Storage**: Filesystem only, version-controlled artifacts under `data/`, `docs/`, and `specs/`

**Testing**: Repository-local validation guidance and optional shell-based artifact checks; no deployed services or network access

**Target Platform**: Developer workstation from repository root

**Project Type**: Documentation/data-contract foundation package

**Performance Goals**: Maintainer can locate `data/watchlists/asset-watchlist.json` and identify active equity monitoring targets plus any benchmark entry in <=5 minutes; validation should be reproducible from a clean clone in <=10 minutes

**Constraints**: No live prices, scraping, external API calls, ingestion runtime, Kafka producers, FastAPI endpoints, databases, dashboard code, or AI analysis

**Scale/Scope**: 5-15 watchlist entries with at least 5 active individual equity monitoring targets; optional `IPC` entry is `index` + `reference_benchmark` only

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Non-advisory scope enforced: no buy/sell/hold or portfolio recommendations.
- [x] Traceability/reproducibility plan defined: data provenance, versioned inputs,
      deterministic parameters, and replay procedure.
- [x] Contract-first boundaries defined: API/event schemas, versioning, and
      compatibility expectations.
- [x] Evidence-backed AI controls defined (if AI used): source references,
      timestamps, model/provider metadata, confidence, latency, prompt version,
      and mandatory disclaimer. No AI outputs are included in this feature.
- [x] Simplicity gate passed: no RAG/agents/multi-provider orchestration or
      premature cloud complexity before deterministic pipeline foundations.

## Project Structure

### Documentation (this feature)

```text
specs/002-asset-watchlist/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── asset-watchlist.schema.json
├── checklists/
│   └── requirements.md
└── tasks.md              # Created later by /speckit.tasks
```

### Source Code (repository root)

```text
data/
├── watchlists/
│   └── asset-watchlist.json
└── samples/
    └── watchlists/
        ├── valid/
        │   └── asset-watchlist-valid-equities.json
        └── invalid/
            ├── asset-watchlist-invalid-missing-required.json
            ├── asset-watchlist-invalid-wrong-asset-type.json
            └── asset-watchlist-invalid-advisory-content.json

docs/
├── foundation/
│   └── artifact-manifest.md
└── validation/
    ├── asset-watchlist-validation.md
    ├── rule-ids.md
    └── sample-rule-mapping.md

scripts/
└── validation/
    └── check-asset-watchlist.sh
```

**Structure Decision**: Use repository-local data, samples, docs, and validation-script artifacts only. The canonical watchlist lives under `data/watchlists/` because it is future-service input data, while the design schema remains under the feature planning contracts directory until implementation tasks decide whether to promote a root-level contract artifact.

## Complexity Tracking

No constitution violations or complexity exceptions are required for this feature.
