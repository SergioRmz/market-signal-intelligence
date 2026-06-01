# Research: Market Source Adapter

## Decision: Use a minimal internal Python adapter, not a service endpoint

**Rationale**: The constitution requires Python for data workflows, and the feature needs a replaceable source boundary without exposing FastAPI endpoints or adding deployment concerns. A small internal module keeps the first integration testable and avoids premature platform surface area.

**Alternatives considered**: FastAPI endpoint rejected because the spec forbids service endpoints; shell-only implementation rejected because HTTP behavior, timeout classification, credentials, and structured outcomes are easier to test and maintain in Python; framework-heavy client abstraction rejected as premature.

## Decision: Target Python 3.12 for the adapter workflow

**Rationale**: The local planning environment provides Python 3.12.3, and Python 3.12 is a stable current baseline for standard-library HTTP, configuration, dataclass, and unittest behavior. Pinning the minor version gives implementation tasks a reproducible target without over-constraining patch-level updates.

**Alternatives considered**: Python 3.11+ rejected because it is less precise for planning; pinning exactly to Python 3.12.3 rejected because patch-level pinning is unnecessary for this standard-library-only workflow unless later dependency evidence requires it.

## Decision: Reuse Bash 5.2+ and jq 1.7 validation tooling

**Rationale**: Existing repository validation is shell-based and already uses jq for JSON checks. Planning was validated locally with GNU Bash 5.2.21 and jq 1.7, so the adapter validation can extend the current pattern without adding package-manager dependencies.

**Alternatives considered**: Replacing shell validation with Python-only checks rejected because it would diverge from existing validation workflows; leaving jq and Bash unversioned rejected because clean-clone reproducibility depends on predictable validation behavior.

## Decision: One configurable controlled HTTP endpoint with fixture-backed validation

**Rationale**: Clarification selected one configurable controlled HTTP endpoint. Fixtures allow deterministic success and failure tests without depending on external source availability, network timing, credentials, or rate limits during routine validation.

**Alternatives considered**: Live external source rejected for clean-clone reproducibility risk; fixture-only source rejected because the feature must introduce an HTTP source boundary; multiple providers rejected by explicit scope.

## Decision: Default timeout is 5 seconds and configurable

**Rationale**: A fixed default prevents hanging fetches and gives tests a deterministic failure threshold, while configurability supports controlled validation scenarios.

**Alternatives considered**: No default rejected as ambiguous; 10 seconds rejected as slower for local validation; per-fixture-only timeout rejected because production-facing behavior would remain unclear.

## Decision: Credentials may be supplied only by local environment configuration

**Rationale**: The controlled endpoint may require credentials, but repository artifacts must remain safe. Local environment configuration avoids committed secrets and lets missing credentials be classified as configuration failure.

**Alternatives considered**: No credentials ever rejected because it may block a controlled endpoint; committed sample credentials rejected for security; live credentialed validation as a required clean-clone step rejected for reproducibility.

## Decision: Preserve provider payload and source metadata in an adapter fetch result

**Rationale**: Source payloads are unstable and must remain auditable. The adapter fetch result records the requested ticker, source name, status, retrieval timestamp, response classification, raw provider payload when received, and adapted raw market snapshot when accepted.

**Alternatives considered**: Storing only the adapted raw snapshot rejected because it loses provider evidence; storing only provider payload rejected because downstream validation needs the existing raw snapshot shape.

## Decision: Primary output is the adapted internal raw market snapshot

**Rationale**: The feature must prove end-to-end compatibility with existing 003 validation/normalization but must not own normalization. The adapter produces the existing raw market snapshot shape and reuses the existing validation/normalization flow when normalized artifacts are already present.

**Alternatives considered**: Provider-specific normalized schema rejected by clarification; duplicate normalization logic rejected by contract ownership; raw-only without compatibility proof rejected because the feature intent requires pipeline validation.

## Decision: BMV-first but not BMV-only adapter boundary

**Rationale**: Current acceptance is governed by the active canonical watchlist, which is BMV-focused today, but the adapter boundary must not hard-code BMV-only assumptions that block future governed non-BMV assets.

**Alternatives considered**: BMV-only implementation rejected by architectural clarification; broad multi-market support in this feature rejected because future non-BMV assets require governed watchlist and source-policy changes.

## Decision: Local validation extends existing snapshot validation instead of replacing it

**Rationale**: `scripts/validation/check-market-snapshots.sh` already validates raw/normalized snapshot contracts and samples. The adapter validation should verify adapter-specific scenarios, then call or document reuse of the existing snapshot validation path for accepted raw outputs.

**Alternatives considered**: Reimplementing snapshot validation rejected because it duplicates rules; skipping existing validation rejected because compatibility is a core success criterion.
