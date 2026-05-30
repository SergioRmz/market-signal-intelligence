# Implementation Plan: Local Market Snapshot Ingestion

**Branch**: `003-local-market-snapshot-ingestion` | **Date**: 2026-05-28 | **Spec**: `specs/003-local-market-snapshot-ingestion/spec.md`

**Input**: Feature specification from `specs/003-local-market-snapshot-ingestion/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Define a repository-local market snapshot ingestion baseline using static sample files, JSON Schema planning contracts, and lightweight validation guidance. The plan separates raw source-shaped snapshots from normalized watchlist-aligned snapshots, gates eligibility on active canonical watchlist symbols, preserves `S&P/BMV IPC` only as optional benchmark context, and explicitly excludes external APIs, scraping, Kafka, databases, FastAPI, AWS, AI, and live market integrations.

## Technical Context

**Language/Version**: Markdown + JSON artifacts; JSON Schema Draft 2020-12 for planning contracts; optional POSIX shell validation script in implementation

**Primary Dependencies**: None beyond repository-local tooling and git; validation must avoid network and deployed infrastructure

**Storage**: Filesystem only, version-controlled contracts, sample JSON files, validation docs, and optional local validation script

**Testing**: Repository-local validation guidance, sample classification, rule-ID mapping, and optional shell-based checks

**Target Platform**: Developer workstation from repository root

**Project Type**: Documentation/data-contract/sample-validation foundation package

**Performance Goals**: Maintainer can distinguish raw from normalized samples and trace valid normalized samples to raw sources in <=5 minutes; local validation reproducible from a clean clone in <=10 minutes

**Constraints**: No external APIs, scraping, Kafka, databases, FastAPI endpoints, AWS/cloud automation, dashboard code, AI analysis, live price fetching, or runtime ingestion behavior

**Scale/Scope**: At least 2 valid raw snapshot samples, 2 valid normalized snapshot samples, and 4 invalid snapshot samples covering missing asset, inactive asset, malformed required fields, and prohibited advisory/live-feed content

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
specs/003-local-market-snapshot-ingestion/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── raw-market-snapshot.schema.json
│   └── normalized-market-snapshot.schema.json
├── checklists/
│   └── requirements.md
└── tasks.md              # Created later by /speckit.tasks
```

### Source Code (repository root)
```text
contracts/
└── market-snapshots/
    ├── raw-market-snapshot.schema.json
    └── normalized-market-snapshot.schema.json

data/
└── samples/
    └── market-snapshots/
        ├── raw/
        │   ├── valid/
        │   └── invalid/
        └── normalized/
            ├── valid/
            └── invalid/

docs/
├── foundation/
│   └── artifact-manifest.md
└── validation/
    ├── market-snapshot-validation.md
    ├── rule-ids.md
    └── sample-rule-mapping.md

scripts/
└── validation/
    └── check-market-snapshots.sh

README.md      # Update only if project-wide usage guidance changes
AGENTS.md      # Update Speckit plan marker; update other guidance only if needed
```

**Structure Decision**: Use repository-local contracts, samples, validation docs, and an optional local validation script only. No runtime application code is introduced; root contracts may be created during implementation so future ingestion work has stable raw and normalized snapshot boundaries.

## Complexity Tracking

No constitution violations or complexity exceptions are required for this feature.
