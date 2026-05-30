# Asset Watchlist Validation

## Purpose

Define local validation rules and review evidence for the equity-primary Mexican market asset watchlist. Individual equity entries are the primary monitoring targets; `S&P/BMV IPC` may appear only as a reference benchmark index.

## Local Commands

Run from the repository root:

```bash
scripts/validation/check-asset-watchlist.sh
```

The command validates the canonical watchlist, valid samples, invalid sample mappings, and non-advisory scope guardrails without network access or deployed services.

## Rule IDs

- `WL-REQ-001`: Watchlist file must exist at `data/watchlists/asset-watchlist.json`.
- `WL-REQ-002`: Watchlist must include `watchlist_id`, `version`, `effective_date`, `purpose`, and `assets`.
- `WL-REQ-003`: Watchlist must include at least five active equity entries with `asset_role` set to `monitoring_target`.
- `WL-REQ-004`: Watchlist entry symbols must be non-empty, unique, canonical local identifiers.
- `WL-REQ-005`: Primary monitoring targets must use `asset_type` `equity`; `index` is allowed only for `IPC` as `reference_benchmark`.
- `WL-REQ-006`: Watchlist entries must use currency `MXN`.
- `WL-REQ-007`: Watchlist entries must include market metadata sufficient to identify BMV/Mexico context.
- `WL-REQ-008`: Watchlist entries must include traceability context.
- `WL-REQ-009`: Watchlist and samples must not include live prices, target prices, ratings, trading signals, recommendations, or performance forecasts.
- `WL-REQ-010`: Invalid watchlist samples must map to at least one rule ID in `docs/validation/sample-rule-mapping.md`.

## Equity Baseline Manual Review

Reviewers must confirm `data/watchlists/asset-watchlist.json` satisfies these baseline checks:

- The file exists and is valid JSON.
- `watchlist_id` is `asset-watchlist`.
- `version`, `effective_date`, and `purpose` are present and non-empty.
- `assets` contains at least five active individual equity monitoring targets.
- Each primary monitoring target uses `asset_type` `equity` and `asset_role` `monitoring_target`.
- Each entry uses currency `MXN`.
- Market metadata identifies BMV/Mexico context and preserves exchange symbols where useful.
- Traceability includes source reference and non-advisory review rationale.
- `IPC` appears only as a reference benchmark with `asset_type` `index` and `asset_role` `reference_benchmark`.
- No index entry replaces or reduces the individual equity monitoring targets.

## Sample Expectations

- Valid samples under `data/samples/watchlists/valid/` must pass the same equity-primary structural checks as the canonical watchlist.
- Invalid samples under `data/samples/watchlists/invalid/` must remain parseable JSON but fail at least one `WL-REQ-*` rule.
- Every invalid watchlist sample must be listed in `docs/validation/sample-rule-mapping.md` with at least one violated rule ID.

## Non-Advisory Content Scan

The local validation script rejects watchlist and sample JSON when it finds prohibited terms or fields associated with live prices, target prices, ratings, rankings, trading signals, recommendations, portfolio allocation, or performance forecasts.

Reviewers must also confirm the artifacts do not imply that any equity or index inclusion is a buy, sell, hold, allocation, ranking, or forecasting decision. Watchlist inclusion only defines allowed future monitoring scope.

## Traceability Review

Each watchlist entry must include traceability context with:

- A source reference that identifies the public issuer/listing, IPC constituent reference category, or benchmark reference basis used for review.
- A review rationale that explains why the asset is in scope without making performance claims.
- Optional reviewer and review date metadata when available.

Traceability must be sufficient for maintainers and future ingestion service owners to understand the source context without fetching live market data.

## Scope Guardrail Checklist

Before approving watchlist changes, reviewers must confirm this feature introduced none of the following:

- Live price fetching.
- Website scraping.
- External API calls.
- Kafka producers or streaming topology.
- FastAPI endpoints or service runtime behavior.
- Database schemas, migrations, or persistence code.
- Dashboard code.
- AI analysis, RAG workflows, or autonomous agents.

Allowed changes are limited to documentation, contracts, sample data, validation guidance, repository-local watchlist artifacts, and local validation scripting.

## Evidence Format

Pull requests must include:

- Command executed.
- Pass/fail result.
- Current watchlist version.
- Active equity monitoring target count.
- Reference benchmark count.
- Valid watchlist sample count.
- Invalid watchlist sample count.
- Invalid sample to violated rule ID mapping.
- Confirmation that no runtime ingestion, external API, scraping, database, endpoint, streaming, dashboard, or AI behavior was introduced.

## Failure Handling

- Missing watchlist artifact: create `data/watchlists/asset-watchlist.json` or update the governing spec.
- Invalid JSON: fix the watchlist or sample file.
- Equity-primary constraint failure: update the artifact so individual equities remain the primary monitoring targets.
- Invalid sample without rule mapping: update `docs/validation/sample-rule-mapping.md`.
- Advisory or live-price content: remove prohibited language or data fields.

## Guardrails

- Validation must not fetch live prices, scrape websites, call external APIs, connect to databases, create service endpoints, produce streaming events, run dashboard code, or invoke AI analysis.
- Watchlist artifacts are educational and technical scope controls only; they are not investment advice, trading signals, ratings, rankings, or recommendations.
