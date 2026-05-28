# Foundation Documentation Index

This directory indexes foundation artifacts for the initial repository baseline.

## Core Foundation Documents

- `docs/foundation/artifact-manifest.md` defines required artifacts and minimum sections.
- `docs/foundation/scaffolding-boundaries.md` defines what scaffolding is allowed without becoming runtime implementation.
- `docs/architecture/foundation-architecture.md` describes conceptual architecture boundaries.
- `docs/policies/allowed-sources.md` defines source policy categories.
- `docs/validation/event-contract-validation.md` defines lightweight validation expectations.
- `docs/validation/asset-watchlist-validation.md` defines lightweight asset watchlist validation expectations.

## Contract Artifacts

- `contracts/events/asset-event.schema.json` defines the base event schema.
- `data/samples/asset-events/valid/` contains valid examples.
- `data/samples/asset-events/invalid/` contains invalid examples.

## Watchlist Artifacts

- `data/watchlists/asset-watchlist.json` defines the equity-primary asset allowlist for future monitoring scope.
- `contracts/watchlists/asset-watchlist.schema.json` defines the watchlist contract.
- `data/samples/watchlists/valid/` contains valid watchlist examples.
- `data/samples/watchlists/invalid/` contains invalid watchlist examples.
- `scripts/validation/check-asset-watchlist.sh` validates the watchlist, samples, and rule mappings locally.
