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

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"
shopt -s nullglob

RAW_SCHEMA="contracts/market-snapshots/raw-market-snapshot.schema.json"
NORMALIZED_SCHEMA="contracts/market-snapshots/normalized-market-snapshot.schema.json"
WATCHLIST="data/watchlists/asset-watchlist.json"
RAW_VALID_DIR="data/samples/market-snapshots/raw/valid"
RAW_INVALID_DIR="data/samples/market-snapshots/raw/invalid"
NORMALIZED_VALID_DIR="data/samples/market-snapshots/normalized/valid"
NORMALIZED_INVALID_DIR="data/samples/market-snapshots/normalized/invalid"
MAPPING="docs/validation/sample-rule-mapping.md"

require_file "$RAW_SCHEMA"
require_file "$NORMALIZED_SCHEMA"
require_file "$WATCHLIST"
require_file "$MAPPING"
require_dir "$RAW_VALID_DIR"
require_dir "$RAW_INVALID_DIR"
require_dir "$NORMALIZED_VALID_DIR"
require_dir "$NORMALIZED_INVALID_DIR"

require_json "$RAW_SCHEMA"
require_json "$NORMALIZED_SCHEMA"
require_json "$WATCHLIST"

contains_prohibited_content() {
  local path="$1"
  jq -e '
    tostring
    | test("(?i)(live[_ -]?feed|live[_ -]?price|target[_ -]?price|price target|\\bbuy\\b|\\bsell\\b|\\bhold\\b|recommendation|recommended|\\brating\\b|ranking|portfolio allocation|performance forecast|external api|scraping|kafka|fastapi|aws|artificial intelligence|\\bai\\b|database)")
  ' "$path" >/dev/null
}

active_watchlist_symbol() {
  local symbol="$1"
  jq -e --arg symbol "$symbol" '
    any(.assets[]; .symbol == $symbol and .active == true)
  ' "$WATCHLIST" >/dev/null
}

watchlist_role() {
  local symbol="$1"
  jq -r --arg symbol "$symbol" '.assets[] | select(.symbol == $symbol) | .asset_role' "$WATCHLIST" | head -n 1
}

is_rfc3339_like() {
  local value="$1"
  [[ "$value" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]]
}

raw_snapshot_structurally_valid() {
  local path="$1"
  jq -e '
    (.raw_snapshot_id | type == "string" and length > 0) and
    (.schema_version | type == "string" and length > 0) and
    (.source.name | type == "string" and length > 0) and
    (.source.category == "local_sample") and
    (.asset.symbol | type == "string" and test("^[A-Z0-9]+$")) and
    (.asset.market | type == "string" and length > 0) and
    (.observed_at | type == "string") and
    (.observed_values.last_price | type == "number" and . >= 0) and
    (.observed_values.currency == "MXN") and
    (.observed_values.volume | type == "number" and . >= 0) and
    (.provenance.sample_origin | type == "string" and length > 0) and
    (.provenance.review_notes | type == "string" and length > 0)
  ' "$path" >/dev/null 2>/dev/null
}

raw_snapshot_valid() {
  local path="$1"
  raw_snapshot_structurally_valid "$path" || return 1
  local observed_at symbol
  observed_at="$(jq -r '.observed_at' "$path")"
  is_rfc3339_like "$observed_at" || return 1
  symbol="$(jq -r '.asset.symbol' "$path")"
  active_watchlist_symbol "$symbol" || return 1
  contains_prohibited_content "$path" && return 1
  return 0
}

normalized_snapshot_structurally_valid() {
  local path="$1"
  jq -e '
    (.normalized_snapshot_id | type == "string" and length > 0) and
    (.schema_version | type == "string" and length > 0) and
    (.raw_snapshot_id | type == "string" and length > 0) and
    (.asset.symbol | type == "string" and test("^[A-Z0-9]+$")) and
    (.asset.market | type == "string" and length > 0) and
    (.asset.asset_role | type == "string" and (. == "monitoring_target" or . == "reference_benchmark")) and
    (.observed_at | type == "string") and
    (.normalized_at | type == "string") and
    (.observed_values.last_price | type == "number" and . >= 0) and
    (.observed_values.currency == "MXN") and
    (.observed_values.volume | type == "number" and . >= 0) and
    (.provenance.source_raw_snapshot_id | type == "string" and length > 0) and
    (.provenance.transformation_notes | type == "string" and length > 0) and
    (.provenance.source_raw_snapshot_id == .raw_snapshot_id)
  ' "$path" >/dev/null 2>/dev/null
}

normalized_snapshot_valid() {
  local path="$1"
  normalized_snapshot_structurally_valid "$path" || return 1
  local observed_at normalized_at symbol role raw_id
  observed_at="$(jq -r '.observed_at' "$path")"
  normalized_at="$(jq -r '.normalized_at' "$path")"
  is_rfc3339_like "$observed_at" || return 1
  is_rfc3339_like "$normalized_at" || return 1
  symbol="$(jq -r '.asset.symbol' "$path")"
  active_watchlist_symbol "$symbol" || return 1
  role="$(watchlist_role "$symbol")"
  [ "$(jq -r '.asset.asset_role' "$path")" = "$role" ] || return 1
  raw_id="$(jq -r '.raw_snapshot_id' "$path")"
  [ -n "${VALID_RAW_IDS[$raw_id]:-}" ] || return 1
  contains_prohibited_content "$path" && return 1
  return 0
}

mapping_exists() {
  local sample="$1"
  grep -F "| \`$sample\` |" "$MAPPING" >/dev/null
}

raw_valid_samples=("$RAW_VALID_DIR"/*.json)
[ "${#raw_valid_samples[@]}" -ge 2 ] || fail "Expected at least two valid raw samples in $RAW_VALID_DIR"

declare -A VALID_RAW_IDS
for sample in "${raw_valid_samples[@]}"; do
  require_json "$sample"
  raw_snapshot_valid "$sample" || fail "Valid raw sample failed validation: $sample"
  raw_id="$(jq -r '.raw_snapshot_id' "$sample")"
  [ -z "${VALID_RAW_IDS[$raw_id]:-}" ] || fail "Duplicate raw_snapshot_id in valid raw samples: $raw_id"
  VALID_RAW_IDS[$raw_id]="$sample"
done

normalized_valid_samples=("$NORMALIZED_VALID_DIR"/*.json)
[ "${#normalized_valid_samples[@]}" -ge 2 ] || fail "Expected at least two valid normalized samples in $NORMALIZED_VALID_DIR"
for sample in "${normalized_valid_samples[@]}"; do
  require_json "$sample"
  normalized_snapshot_valid "$sample" || fail "Valid normalized sample failed validation: $sample"
done

raw_invalid_samples=("$RAW_INVALID_DIR"/*.json)
normalized_invalid_samples=("$NORMALIZED_INVALID_DIR"/*.json)
invalid_total=$((${#raw_invalid_samples[@]} + ${#normalized_invalid_samples[@]}))
[ "$invalid_total" -ge 4 ] || fail "Expected at least four invalid snapshot samples"

for sample in "${raw_invalid_samples[@]}"; do
  require_json "$sample"
  if raw_snapshot_valid "$sample"; then
    fail "Invalid raw sample unexpectedly passed validation: $sample"
  fi
  mapping_exists "$sample" || fail "Invalid raw sample missing rule mapping: $sample"
done

for sample in "${normalized_invalid_samples[@]}"; do
  require_json "$sample"
  if normalized_snapshot_valid "$sample"; then
    fail "Invalid normalized sample unexpectedly passed validation: $sample"
  fi
  mapping_exists "$sample" || fail "Invalid normalized sample missing rule mapping: $sample"
done

pass "Local market snapshot contracts and samples validated"
