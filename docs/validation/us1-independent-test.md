# US1 Independent Test

## Goal

Confirm a maintainer can locate and review all required foundation artifacts from a clean clone.

## Steps

1. Run `scripts/validation/check-foundation-artifacts.sh`.
2. Open `README.md` and confirm purpose, scope, non-goals, disclaimer, planned stack, and methodology exist.
3. Open `AGENTS.md` and confirm agent guardrails and review expectations exist.
4. Open `docs/foundation/artifact-manifest.md` and confirm exact artifact paths are listed.

## Pass Criteria

- Required artifacts exist.
- Required sections are present.
- No runtime implementation files are required to understand the foundation.
