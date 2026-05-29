# Foundation Artifact Manifest

## Purpose

Define exact required artifact paths and minimum sections for the initial project foundation.

## Required Artifacts

| Path | Type | Minimum Required Sections |
|------|------|---------------------------|
| `README.md` | Documentation | Purpose, Scope, Non-Goals, Disclaimer, Planned Stack, Methodology |
| `AGENTS.md` | Agent guidance | Repository Scope, Required Reading Order, Contribution Guardrails, Review Expectations |
| `docs/architecture/foundation-architecture.md` | Architecture | Purpose, Conceptual Boundaries, Data Flow, Repository Areas, Deferred Components |
| `docs/policies/allowed-sources.md` | Policy | Purpose, Categories, Decision Criteria, Attribution, Prohibited Sources |
| `contracts/events/asset-event.schema.json` | Contract | JSON Schema metadata, required fields, nested source and asset constraints |
| `data/samples/asset-events/valid/` | Samples | At least 2 valid JSON files |
| `data/samples/asset-events/invalid/` | Samples | At least 3 invalid JSON files |
| `data/watchlists/asset-watchlist.json` | Watchlist data | Version, effective date, purpose, at least 5 active equity monitoring targets, optional IPC benchmark, traceability |
| `contracts/watchlists/asset-watchlist.schema.json` | Contract | JSON Schema metadata, equity-primary constraints, optional IPC benchmark constraints, nested market and traceability constraints |
| `data/samples/watchlists/valid/` | Samples | At least 1 valid equity-primary watchlist JSON file |
| `data/samples/watchlists/invalid/` | Samples | At least 3 invalid equity-primary watchlist JSON files |
| `contracts/market-snapshots/raw-market-snapshot.schema.json` | Contract | JSON Schema metadata, raw snapshot required fields, source context, canonical asset reference, observed values, provenance |
| `contracts/market-snapshots/normalized-market-snapshot.schema.json` | Contract | JSON Schema metadata, normalized snapshot required fields, raw snapshot provenance link, canonical asset reference, observed values |
| `data/samples/market-snapshots/raw/valid/` | Samples | At least 2 valid raw snapshot JSON files using active canonical watchlist symbols |
| `data/samples/market-snapshots/raw/invalid/` | Samples | Invalid raw snapshot JSON files covering missing asset, inactive asset, malformed required fields, and prohibited content |
| `data/samples/market-snapshots/normalized/valid/` | Samples | At least 2 valid normalized snapshot JSON files linked to valid raw samples by `raw_snapshot_id` |
| `data/samples/market-snapshots/normalized/invalid/` | Samples | Invalid normalized snapshot JSON files covering missing raw provenance and canonical symbol violations |
| `docs/validation/event-contract-validation.md` | Validation guide | Purpose, Local Commands, Evidence Format, Failure Handling |
| `docs/validation/asset-watchlist-validation.md` | Validation guide | Purpose, Local Commands, Rule IDs, Evidence Format, Failure Handling, Guardrails |
| `docs/validation/market-snapshot-validation.md` | Validation guide | Purpose, Local Commands, Rule IDs, Evidence Format, Failure Handling, Guardrails |
| `scripts/validation/check-asset-watchlist.sh` | Local validation script | Path checks, JSON parse checks, equity-primary constraints, sample mappings, non-advisory guardrails |
| `scripts/validation/check-market-snapshots.sh` | Local validation script | Path checks, JSON parse checks, raw/normalized separation, active watchlist checks, provenance links, sample mappings, non-advisory guardrails |

## Review Rules

- Each artifact must be present before the feature is considered complete.
- Documentation artifacts must include all minimum required sections.
- Invalid samples must map to rule IDs in `docs/validation/sample-rule-mapping.md`.
- Runtime implementation files are not permitted in this foundation feature.
- Watchlist artifacts must not include live prices, ratings, rankings, recommendations, target prices, portfolio guidance, or performance forecasts.
- Market snapshot artifacts must remain static local samples and must not add external APIs, scraping, Kafka, database persistence, FastAPI endpoints, AWS automation, dashboard code, AI analysis, or live-feed behavior.
