"""Regression tests for the Stage 5 passive-scaling result.

Code license: MIT -- see LICENSE for details.
"""

import unittest

from stage5_scaling_test import build_scaling_results, compute_anchor_scaling_ratios, scaling_verdict


class Stage5ScalingTests(unittest.TestCase):
    def test_anchor_scaling_ratios_match_current_headline_result(self):
        results = build_scaling_results()
        ratios = compute_anchor_scaling_ratios(results)

        self.assertAlmostEqual(ratios["observed_ratio"], 1.95, places=2)
        self.assertAlmostEqual(ratios["predicted_ratio"], 0.049, places=3)
        self.assertGreater(ratios["discrepancy_factor"], 10.0)
        self.assertIn("fails", scaling_verdict(ratios["discrepancy_factor"]))


if __name__ == "__main__":
    unittest.main()
