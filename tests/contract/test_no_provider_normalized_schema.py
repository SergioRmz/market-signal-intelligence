from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class NoProviderNormalizedSchemaTest(unittest.TestCase):
    def test_adapter_does_not_add_provider_specific_normalized_schema(self) -> None:
        adapter_schemas = list((ROOT / "specs/004-market-source-adapter/contracts").glob("**/*normalized*.schema.json"))
        self.assertEqual([], adapter_schemas)

    def test_only_existing_platform_normalized_schema_is_present(self) -> None:
        schemas = sorted(path.relative_to(ROOT).as_posix() for path in (ROOT / "contracts").glob("**/*normalized*.schema.json"))
        self.assertEqual(["contracts/market-snapshots/normalized-market-snapshot.schema.json"], schemas)


if __name__ == "__main__":
    unittest.main()
