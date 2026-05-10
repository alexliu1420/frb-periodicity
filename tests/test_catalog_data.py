"""Tests for catalog validation and curated source selectors.

Code license: MIT -- see LICENSE for details.
"""

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from frb.catalog import (
    CatalogValidationError,
    REQUIRED_CHIME_COLUMNS,
    count_events_for_aliases,
    load_chime_catalog,
    named_repeater_event_count,
    repeater_counts,
    unique_event_count,
)
from frb.data import all_sources, sources_with_dfdt
from frb.literature import REFERENCES


class CatalogValidationTests(unittest.TestCase):
    def write_temp_file(self, content: str) -> Path:
        handle = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        with handle:
            handle.write(content)
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        return Path(handle.name)

    def test_load_chime_catalog_rejects_html(self):
        path = self.write_temp_file("<html><body>not a csv</body></html>")
        with self.assertRaises(CatalogValidationError):
            load_chime_catalog(path)

    def test_load_chime_catalog_rejects_missing_columns(self):
        columns = sorted(REQUIRED_CHIME_COLUMNS - {"low_freq"})
        path = self.write_temp_file(",".join(columns) + "\n" + ",".join("1" for _ in columns))
        with self.assertRaises(CatalogValidationError):
            load_chime_catalog(path)

    def test_repeater_counts_excludes_string_and_numeric_sentinel(self):
        df = pd.DataFrame(
            {
                "repeater_name": ["-9999", -9999, -9999.0, "FRB_TEST", "FRB_TEST"],
                "tns_name": ["a", "b", "c", "d", "e"],
                "event_id": [1, 2, 3, 4, 5],
            }
        )
        counts = repeater_counts(df)
        self.assertNotIn("-9999", counts.index.astype(str).tolist())
        self.assertEqual(counts.loc["FRB_TEST"], 2)

    def test_event_counts_use_event_id_when_available(self):
        df = pd.DataFrame(
            {
                "tns_name": ["FRB_A", "FRB_A", "FRB_B"],
                "event_id": [10, 10, 11],
                "repeater_name": ["FRB_TEST", "FRB_TEST", pd.NA],
            }
        )
        self.assertEqual(unique_event_count(df), 2)
        self.assertEqual(named_repeater_event_count(df), 1)
        self.assertEqual(count_events_for_aliases(df, {"FRB_TEST"}), 1)

    def test_sources_with_dfdt_returns_curated_pair(self):
        names = [source.name for source in sources_with_dfdt()]
        self.assertEqual(names, ["FRB 20180916B", "FRB 20121102A"])

    def test_sources_have_structured_provenance_when_values_are_present(self):
        reference_keys = {ref.key for ref in REFERENCES}
        self.assertEqual(len(reference_keys), len(REFERENCES))
        for source in all_sources():
            self.assertIsNotNone(source.host_reference, source.name)
            self.assertIn(source.host_reference, reference_keys)
            if source.period_days is not None:
                self.assertIsNotNone(source.period_reference, source.name)
                self.assertIn(source.period_reference, reference_keys)
            if source.redshift is not None:
                self.assertIsNotNone(source.redshift_reference, source.name)
                self.assertIn(source.redshift_reference, reference_keys)
            if source.dfdt_mhz_ms is not None:
                self.assertIsNotNone(source.dfdt_reference, source.name)
                self.assertIn(source.dfdt_reference, reference_keys)


if __name__ == "__main__":
    unittest.main()
