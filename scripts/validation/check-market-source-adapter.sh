#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

pass() {
  printf 'PASS: %s\n' "$1"
}

require_file() {
  local path="$1"
  [ -f "$path" ] || fail "Missing required file: $path"
}

require_dir() {
  local path="$1"
  [ -d "$path" ] || fail "Missing required directory: $path"
}

require_json() {
  local path="$1"
  jq empty "$path" >/dev/null || fail "Invalid JSON: $path"
}

mapping_exists() {
  local sample="$1"
  grep -F "| \`$sample\` |" "docs/validation/sample-rule-mapping.md" >/dev/null
}

contains_secret_like_value() {
  local path="$1"
  jq -e '
    tostring
    | test("(?i)(bearer [A-Za-z0-9._-]{8,}|api[_ -]?key[\":= ][A-Za-z0-9._-]{8,}|password[\":= ][A-Za-z0-9._-]{8,}|secret[\":= ][A-Za-z0-9._-]{8,}|token[\":= ][A-Za-z0-9._-]{8,})")
  ' "$path" >/dev/null
}

contains_advisory_value() {
  local path="$1"
  jq -e '
    tostring
    | test("(?i)(target[_ -]?price|price target|\\bbuy\\b|\\bsell\\b|\\bhold\\b|trading signal|\\brating\\b|ranking|portfolio allocation|performance forecast)")
  ' "$path" >/dev/null
}

active_watchlist_symbol() {
  local symbol="$1"
  jq -e --arg symbol "$symbol" 'any(.assets[]; .symbol == $symbol and .active == true)' "data/watchlists/asset-watchlist.json" >/dev/null
}

raw_snapshot_valid() {
  local path="$1"
  jq -e '
    (.raw_snapshot_id | type == "string" and length > 0) and
    (.schema_version | type == "string" and length > 0) and
    (.source.name | type == "string" and length > 0) and
    (.source.category == "local_sample") and
    (.source.reference | type == "string" and length > 0) and
    (.asset.symbol | type == "string" and test("^[A-Z0-9]+$")) and
    (.asset.market | type == "string" and length > 0) and
    (.observed_at | type == "string" and test("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")) and
    (.observed_values.last_price | type == "number" and . >= 0) and
    (.observed_values.currency == "MXN") and
    (.observed_values.volume | type == "number" and . >= 0) and
    (.provenance.sample_origin | type == "string" and length > 0) and
    (.provenance.review_notes | type == "string" and length > 0)
  ' "$path" >/dev/null
}

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"
shopt -s nullglob globstar

required_files=(
  "src/market_signal_intelligence/__init__.py"
  "src/market_signal_intelligence/sources/__init__.py"
  "src/market_signal_intelligence/sources/adapter.py"
  "src/market_signal_intelligence/sources/controlled_http.py"
  "src/market_signal_intelligence/sources/models.py"
  "specs/004-market-source-adapter/contracts/adapter-fetch-result.schema.json"
  "docs/sources/market-source-adapter.md"
  "docs/validation/market-source-adapter-validation.md"
  "docs/validation/rule-ids.md"
  "docs/validation/sample-rule-mapping.md"
  "docs/foundation/artifact-manifest.md"
  "data/watchlists/asset-watchlist.json"
)

required_dirs=(
  "tests/fixtures/market-source-adapter"
  "data/samples/market-source-adapter/source-payloads"
  "data/samples/market-source-adapter/raw-snapshots"
  "data/samples/market-source-adapter/failures"
)

for path in "${required_files[@]}"; do
  require_file "$path"
done
for path in "${required_dirs[@]}"; do
  require_dir "$path"
done

for path in \
  specs/004-market-source-adapter/contracts/*.json \
  tests/fixtures/market-source-adapter/*.json \
  data/samples/market-source-adapter/source-payloads/*.json \
  data/samples/market-source-adapter/raw-snapshots/*.json \
  data/samples/market-source-adapter/failures/*.json; do
  require_json "$path"
  contains_secret_like_value "$path" && fail "Secret-like value found in JSON artifact: $path"
  contains_advisory_value "$path" && fail "Advisory-like content found in JSON artifact: $path"
done

for rule in MSA-REQ-{001..012}; do
  grep -F "\`$rule\`" "docs/validation/rule-ids.md" >/dev/null || fail "Missing rule ID: $rule"
done

success_payloads=(data/samples/market-source-adapter/source-payloads/*.json)
[ "${#success_payloads[@]}" -eq 1 ] || fail "Expected exactly one preserved successful source payload sample"

raw_snapshots=(data/samples/market-source-adapter/raw-snapshots/*.json)
[ "${#raw_snapshots[@]}" -eq 1 ] || fail "Expected exactly one adapter raw snapshot sample"
for sample in "${raw_snapshots[@]}"; do
  raw_snapshot_valid "$sample" || fail "Adapter raw snapshot sample failed compatibility checks: $sample"
  symbol="$(jq -r '.asset.symbol' "$sample")"
  active_watchlist_symbol "$symbol" || fail "Adapter raw snapshot does not use active canonical watchlist symbol: $sample"
done

expected_failures=(timeout rate_limited ticker_not_found invalid_response_shape unsupported_ticker inactive_ticker configuration_failure)
for failure_class in "${expected_failures[@]}"; do
  matches=(data/samples/market-source-adapter/failures/*.json)
  found=0
  for sample in "${matches[@]}"; do
    if [ "$(jq -r '.failure_class' "$sample")" = "$failure_class" ]; then
      found=1
      [ "$(jq -r '.outcome' "$sample")" = "failed" ] || fail "Failure sample outcome is not failed: $sample"
      [ "$(jq -r '.source_metadata.classification' "$sample")" = "$failure_class" ] || fail "Failure sample metadata classification mismatch: $sample"
      if jq -e 'has("adapted_raw_snapshot")' "$sample" >/dev/null; then
        fail "Failure sample contains accepted raw snapshot: $sample"
      fi
      mapping_exists "$sample" || fail "Failure sample missing rule mapping: $sample"
    fi
  done
  [ "$found" -eq 1 ] || fail "Missing failure evidence sample for class: $failure_class"
done

provider_normalized=(specs/004-market-source-adapter/contracts/**/*normalized*.schema.json)
[ "${#provider_normalized[@]}" -eq 0 ] || fail "Provider-specific normalized schema found under adapter contracts"
for schema in contracts/**/*normalized*.schema.json; do
  [ "$schema" = "contracts/market-snapshots/normalized-market-snapshot.schema.json" ] || fail "Unexpected normalized schema artifact: $schema"
done

scripts/validation/check-market-snapshots.sh >/dev/null

pass "Market source adapter artifacts validated"
