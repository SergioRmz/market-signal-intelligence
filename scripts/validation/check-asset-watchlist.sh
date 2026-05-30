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

WATCHLIST="data/watchlists/asset-watchlist.json"
VALID_DIR="data/samples/watchlists/valid"
INVALID_DIR="data/samples/watchlists/invalid"
MAPPING="docs/validation/sample-rule-mapping.md"
SCHEMA="contracts/watchlists/asset-watchlist.schema.json"

contains_prohibited_content() {
  local path="$1"
  jq -e '
    tostring
    | test("(?i)(live[_ -]?price|target[_ -]?price|\\bbuy\\b|\\bsell\\b|\\bhold\\b|recommendation|recommended|\\brating\\b|ranking|portfolio allocation|performance forecast|price target)")
  ' "$path" >/dev/null
}

is_valid_watchlist() {
  local path="$1"
  jq -e '
    .watchlist_id == "asset-watchlist" and
    (.version | type == "string" and length > 0) and
    (.effective_date | type == "string" and test("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")) and
    (.purpose | type == "string" and length > 0) and
    (.assets | type == "array" and length >= 5 and length <= 15) and
    ([.assets[].symbol] | unique | length) == ([.assets[].symbol] | length) and
    ([.assets[] | select(.active == true and .asset_type == "equity" and .asset_role == "monitoring_target")] | length) >= 5 and
    ([.assets[] | select(.asset_type == "index")] | length) <= 1 and
    all(.assets[];
      (.symbol | type == "string" and test("^[A-Z0-9]+$")) and
      (.display_name | type == "string" and length > 0) and
      (.currency == "MXN") and
      (.active | type == "boolean") and
      (.market.venue | type == "string" and length > 0) and
      (.market.country | type == "string" and length > 0) and
      (.traceability.source_reference | type == "string" and length > 0) and
      (.traceability.review_rationale | type == "string" and length > 0) and
      (
        (.asset_type == "equity" and .asset_role == "monitoring_target" and .symbol != "IPC") or
        (.asset_type == "index" and .asset_role == "reference_benchmark" and .symbol == "IPC" and .display_name == "S&P/BMV IPC")
      )
    )
  ' "$path" >/dev/null 2>/dev/null
}

assert_valid_watchlist() {
  local path="$1"
  is_valid_watchlist "$path" || fail "Watchlist does not satisfy equity-primary constraints: $path"
}

require_file "$WATCHLIST"
require_dir "$VALID_DIR"
require_dir "$INVALID_DIR"
require_file "$MAPPING"
require_file "$SCHEMA"
require_json "$WATCHLIST"
require_json "$SCHEMA"

assert_valid_watchlist "$WATCHLIST"
if contains_prohibited_content "$WATCHLIST"; then
  fail "Prohibited advisory or live-price content found in $WATCHLIST"
fi

valid_samples=("$VALID_DIR"/*.json)
[ "${#valid_samples[@]}" -ge 1 ] || fail "Expected at least one valid watchlist sample in $VALID_DIR"
for sample in "${valid_samples[@]}"; do
  require_json "$sample"
  assert_valid_watchlist "$sample"
  if contains_prohibited_content "$sample"; then
    fail "Prohibited advisory or live-price content found in valid sample: $sample"
  fi
done

invalid_samples=("$INVALID_DIR"/*.json)
[ "${#invalid_samples[@]}" -ge 3 ] || fail "Expected at least three invalid watchlist samples in $INVALID_DIR"
for sample in "${invalid_samples[@]}"; do
  require_json "$sample"
  if is_valid_watchlist "$sample" && ! contains_prohibited_content "$sample"; then
    fail "Invalid sample unexpectedly passed watchlist validation: $sample"
  fi
  if ! grep -F "| \`$sample\` |" "$MAPPING" >/dev/null; then
    fail "Invalid sample missing rule mapping: $sample"
  fi
done

pass "Equity-primary asset watchlist and samples validated"
