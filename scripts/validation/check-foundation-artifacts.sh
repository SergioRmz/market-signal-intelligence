#!/usr/bin/env bash
set -euo pipefail

required_paths=(
  "README.md"
  "AGENTS.md"
  "docs/architecture/foundation-architecture.md"
  "docs/policies/allowed-sources.md"
  "contracts/events/asset-event.schema.json"
  "data/samples/asset-events/valid"
  "data/samples/asset-events/invalid"
  "docs/validation/event-contract-validation.md"
  "docs/validation/rule-ids.md"
  "docs/validation/sample-rule-mapping.md"
)

for path in "${required_paths[@]}"; do
  if [ ! -e "$path" ]; then
    echo "FAIL missing required path: $path" >&2
    exit 1
  fi
done

valid_count=$(find data/samples/asset-events/valid -type f -name '*.json' | wc -l | tr -d ' ')
invalid_count=$(find data/samples/asset-events/invalid -type f -name '*.json' | wc -l | tr -d ' ')

if [ "$valid_count" -lt 2 ]; then
  echo "FAIL expected at least 2 valid samples, found $valid_count" >&2
  exit 1
fi

if [ "$invalid_count" -lt 3 ]; then
  echo "FAIL expected at least 3 invalid samples, found $invalid_count" >&2
  exit 1
fi

python3 - <<'PY'
import json
import re
from pathlib import Path

required = {"event_id", "event_type", "schema_version", "occurred_at", "source", "asset", "payload"}
categories = {"allowed", "conditional", "prohibited"}
timestamp = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

def load(path):
    with path.open() as fh:
        return json.load(fh)

schema = load(Path("contracts/events/asset-event.schema.json"))
if set(schema.get("required", [])) != required:
    raise SystemExit("FAIL schema required fields do not match foundation contract")

for path in Path("data/samples/asset-events/valid").glob("*.json"):
    doc = load(path)
    missing = required - set(doc)
    if missing:
        raise SystemExit(f"FAIL valid sample {path} missing {sorted(missing)}")
    if doc["source"].get("category") not in categories:
        raise SystemExit(f"FAIL valid sample {path} has invalid source category")
    if not timestamp.match(doc["occurred_at"]):
        raise SystemExit(f"FAIL valid sample {path} has invalid occurred_at")

mapping = Path("docs/validation/sample-rule-mapping.md").read_text()
for path in Path("data/samples/asset-events/invalid").glob("*.json"):
    load(path)
    if str(path) not in mapping:
        raise SystemExit(f"FAIL invalid sample {path} missing rule mapping")

print("PASS foundation artifacts and samples validated")
PY
