<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan:
specs/004-market-source-adapter/plan.md
<!-- SPECKIT END -->

# Agent Instructions

## Repository Scope

This repository is the BMV Signal Intelligence Platform foundation. Work in this phase is limited to documentation, contracts, sample data, validation guidance, repository scaffolding, and the feature-004 controlled source adapter boundary authorized by `specs/004-market-source-adapter/plan.md`.

Do not add production runtime behavior in this feature. Specifically, do not implement ingestion services, Kafka topology, AWS deployment automation, AI analysis, RAG workflows, autonomous agents, dashboards, schedulers, persistence, multiple providers, or service endpoints.

## Required Reading Order

1. `.specify/memory/constitution.md`
2. `specs/001-project-foundation/spec.md`
3. `specs/001-project-foundation/plan.md`
4. `specs/001-project-foundation/tasks.md`
5. `specs/002-asset-watchlist/spec.md`
6. `specs/002-asset-watchlist/plan.md`
7. `specs/002-asset-watchlist/tasks.md`
8. `specs/003-local-market-snapshot-ingestion/spec.md`
9. `specs/003-local-market-snapshot-ingestion/plan.md`
10. `specs/003-local-market-snapshot-ingestion/tasks.md`
11. `docs/foundation/artifact-manifest.md`

## Contribution Guardrails

- Keep all financial content educational and non-advisory.
- Preserve traceability for source policies, contracts, and samples.
- Treat `contracts/events/asset-event.schema.json` as the contract boundary for future event work.
- Treat `contracts/watchlists/asset-watchlist.schema.json` as the contract boundary for future asset watchlist work.
- Treat `contracts/market-snapshots/raw-market-snapshot.schema.json` and `contracts/market-snapshots/normalized-market-snapshot.schema.json` as the contract boundaries for future local market snapshot work.
- Preserve the equity-primary watchlist rule: individual Mexican equities are monitoring targets; `S&P/BMV IPC` is reference benchmark context only.
- Preserve the raw/normalized snapshot split and require active canonical watchlist symbols for valid snapshot samples.
- Treat `src/market_signal_intelligence/sources/` as the limited controlled source adapter boundary for feature 004; keep it one-source, fixture-backed, non-scheduled, and raw-snapshot-primary.
- Update validation evidence when contract or sample files change.
- Keep scaffolding empty or documentation-only unless a future feature explicitly authorizes runtime code.

## Review Expectations

- Confirm every changed artifact is listed in `docs/foundation/artifact-manifest.md` or justified by a task.
- Confirm invalid samples map to rule IDs in `docs/validation/sample-rule-mapping.md`.
- Confirm local validation instructions in `docs/validation/event-contract-validation.md` remain reproducible from a clean clone.
- Confirm local validation instructions in `docs/validation/asset-watchlist-validation.md` remain reproducible from a clean clone when watchlist artifacts change.
- Confirm local validation instructions in `docs/validation/market-snapshot-validation.md` remain reproducible from a clean clone when snapshot artifacts change.
- Confirm local validation instructions in `docs/validation/market-source-adapter-validation.md` remain reproducible from a clean clone when adapter artifacts change.
- Run `scripts/validation/check-asset-watchlist.sh` when watchlist contracts, samples, validation docs, or watchlist data change.
- Run `scripts/validation/check-market-snapshots.sh` when market snapshot contracts, samples, validation docs, or watchlist-gated snapshot behavior change.
- Run `scripts/validation/check-market-source-adapter.sh` when source adapter code, fixtures, samples, validation docs, or adapter contract artifacts change.
