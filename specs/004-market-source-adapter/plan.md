# Implementation Plan: Market Source Adapter

**Branch**: `004-market-source-adapter` | **Date**: 2026-06-01 | **Spec**: `specs/004-market-source-adapter/spec.md`

**Input**: Feature specification from `specs/004-market-source-adapter/spec.md`

## Summary

Introduce the first controlled market data source adapter as a small internal Python data workflow. The adapter fetches one active watchlist ticker from one configurable controlled HTTP endpoint, preserves provider payload and source metadata, adapts successful responses into the existing raw market snapshot contract, and proves compatibility with the existing 003 validation/normalization flow without adding provider-specific normalized schemas, duplicated normalization logic, Kafka, FastAPI endpoints, databases, cloud resources, dashboards, AI, schedulers, or scraping.

## Technical Context

**Language/Version**: Python 3.12 for internal data workflow code, validated locally with Python 3.12.3; Markdown and JSON for contracts, fixtures, and documentation

**Primary Dependencies**: Python standard library only for initial HTTP client, configuration, fixture tests, and local validation; Bash 5.2+ and jq 1.7 for repository-local validation scripts; existing repository JSON contracts and shell validation scripts are reused

**Storage**: Filesystem only for version-controlled fixtures, sample outputs, validation evidence, and documentation; no database persistence

**Testing**: Python `unittest` for adapter behavior and fixture scenarios; existing `scripts/validation/check-market-snapshots.sh` for raw/normalized snapshot compatibility; planned local validation script for adapter evidence

**Target Platform**: Developer workstation from repository root, with deterministic validation runnable without production services; local planning validated on GNU Bash 5.2.21 and jq 1.7

**Project Type**: Internal data-workflow adapter plus repository-local contracts, fixtures, tests, and validation documentation

**Performance Goals**: Timeout defaults to 5 seconds and is configurable; clean-clone validation completes in <=10 minutes; maintainers can trace accepted raw snapshots to source metadata and payload in <=5 minutes

**Constraints**: One configurable controlled HTTP endpoint; one ticker per fetch; active canonical watchlist gate; credentials only via local environment configuration; no committed secrets; no provider-specific normalized schema; no duplicated normalization logic; no Kafka, FastAPI endpoints, database, AWS, dashboard, AI, scheduler, bulk harvesting, aggressive scraping, trading signals, ratings, targets, or recommendations

**Scale/Scope**: One initial adapter implementation, one successful fixture-backed fetch path, expected failure fixtures for timeout, rate limit, ticker not found, invalid response shape, unsupported ticker, inactive ticker, and missing credentials/configuration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Non-advisory scope enforced: no buy/sell/hold or portfolio recommendations. Adapter outputs and fixtures are technical observations only.
- [x] Traceability/reproducibility plan defined: source metadata, raw provider payload, request ticker, outcome classification, configured timeout, and fixture-backed validation are required.
- [x] Contract-first boundaries defined: existing raw/normalized market snapshot contracts remain stable; adapter boundary and fetch-result planning contracts are documented before implementation.
- [x] Evidence-backed AI controls defined (if AI used): no AI outputs are included in this feature.
- [x] Simplicity gate passed: no Kafka, AWS, RAG, agents, multi-provider orchestration, scheduler, FastAPI endpoint, database, dashboard, or aggressive scraping is introduced.

## Project Structure

### Documentation (this feature)

```text
specs/004-market-source-adapter/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── adapter-fetch-result.schema.json
│   └── market-source-adapter-boundary.md
├── checklists/
│   └── requirements.md
└── tasks.md              # Created later by /speckit.tasks
```

### Source Code (repository root)

```text
src/
└── market_signal_intelligence/
    └── sources/
        ├── __init__.py
        ├── adapter.py
        ├── controlled_http.py
        └── models.py

tests/
├── fixtures/
│   └── market-source-adapter/
│       ├── success-active-equity.json
│       ├── failure-rate-limited.json
│       ├── failure-ticker-not-found.json
│       └── failure-invalid-shape.json
└── unit/
    └── test_market_source_adapter.py

data/
└── samples/
    └── market-source-adapter/
        ├── source-payloads/
        ├── raw-snapshots/
        └── failures/

docs/
├── sources/
│   └── market-source-adapter.md
├── validation/
│   ├── market-source-adapter-validation.md
│   ├── rule-ids.md
│   └── sample-rule-mapping.md
└── foundation/
    └── artifact-manifest.md

scripts/
└── validation/
    └── check-market-source-adapter.sh

README.md      # Update only if project-wide usage guidance changes
AGENTS.md      # Update Speckit plan marker; update other guidance only if needed
```

**Structure Decision**: Add the first minimal internal Python source tree under `src/market_signal_intelligence/sources/` because this feature explicitly authorizes a replaceable adapter implementation, while keeping service endpoints, persistence, streaming, cloud, dashboard, and AI out of scope. Planning contracts live under the feature directory; root contracts for raw/normalized snapshots are reused rather than duplicated.

## Complexity Tracking

No constitution violations or complexity exceptions are required for this feature.

## Post-Design Constitution Check

- [x] Non-advisory scope remains enforced in research, data model, contracts, and quickstart.
- [x] Traceability/reproducibility remains covered through fetch attempts, source metadata, raw payload fixtures, deterministic failure classes, and validation evidence.
- [x] Contract-first boundaries remain stable: adapter fetch result is a boundary contract, while existing market snapshot schemas remain unchanged.
- [x] Evidence-backed AI controls remain not applicable because no AI output is introduced.
- [x] Simplicity gate remains passed: design excludes Kafka, AWS, FastAPI endpoints, databases, dashboards, AI, schedulers, and multi-provider behavior.
