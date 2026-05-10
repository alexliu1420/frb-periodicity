"""Regression tests for Stage 2 reference output.

Code license: MIT -- see LICENSE for details.
"""

import unittest
from contextlib import redirect_stdout
from io import StringIO

from stage2_orbital_mechanics import run_stage2_model


class Stage2OutputTests(unittest.TestCase):
    def test_stage2_reference_output_columns_and_consistency(self):
        with redirect_stdout(StringIO()):
            results = run_stage2_model()
        expected_columns = {
            "source_id",
            "period_status",
            "period_reference",
            "z",
            "redshift_reference",
            "observed_period_days",
            "predicted_min_days",
            "predicted_max_days",
            "is_consistent",
            "interpretation",
        }
        self.assertEqual(set(results.columns), expected_columns)
        self.assertEqual(len(results), 3)
        self.assertTrue(results["is_consistent"].all())


if __name__ == "__main__":
    unittest.main()
