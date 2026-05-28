# Allowed Sources Policy

## Purpose

Define how financial and macroeconomic data sources are classified before they are used by future features.

## Categories

- `allowed`: Source has acceptable licensing, attribution terms, provenance, and usage constraints for the intended educational/technical use.
- `conditional`: Source may be used only when documented conditions are satisfied, such as attribution, rate limits, non-commercial restrictions, or manual approval.
- `prohibited`: Source must not be used due to unclear licensing, unverifiable provenance, scraping restrictions, redistribution limits, or conflicts with project scope.

## Decision Criteria

Each source decision must document:

- Licensing status.
- Attribution requirements.
- Provenance verifiability.
- Usage constraints.
- Jurisdictional or redistribution concerns.

## Attribution

Any accepted source must preserve attribution details in future provenance metadata and related documentation.

## Prohibited Sources

Do not use sources with unclear rights, unverifiable origin, terms that prohibit the planned use, or content that cannot be reproduced or audited.

## Initial Source Policy Table

| Source | Category | Licensing Status | Attribution | Provenance | Usage Constraints |
|--------|----------|------------------|-------------|------------|-------------------|
| Official public regulatory/economic data portals | conditional | Verify per source | Required when specified | High if source URL and retrieval date are recorded | Use only within published terms |
| Unlicensed reposts or scraped mirrors | prohibited | Unclear | Unreliable | Low | Do not use |
