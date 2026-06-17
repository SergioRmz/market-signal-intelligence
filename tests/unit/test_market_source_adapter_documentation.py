from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class MarketSourceAdapterDocumentationTest(unittest.TestCase):
    def test_source_docs_name_scope_and_exclusions(self) -> None:
        content = (ROOT / "docs/sources/market-source-adapter.md").read_text()
        self.assertIn("one controlled HTTP endpoint", content)
        self.assertIn("BMV-first but not BMV-only", content)
        self.assertIn("configuration_failure", content)
        self.assertIn("not investment advice", content)

    def test_samples_do_not_contain_prohibited_outputs(self) -> None:
        prohibited = [
            "target price",
            "price target",
            "trading signal",
            "rating",
            "ranking",
            "portfolio allocation",
            "performance forecast",
        ]
        for path in (ROOT / "data/samples/market-source-adapter").glob("**/*.json"):
            lowered = path.read_text().lower()
            for term in prohibited:
                self.assertNotIn(term, lowered, path.as_posix())


if __name__ == "__main__":
    unittest.main()
