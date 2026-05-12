"""Regression tests for the Stage 5 passive-scaling result.

Code license: MIT -- see LICENSE for details.
"""

import unittest

from stage5_scaling_test import build_scaling_results, compute_anchor_scaling_ratios, scaling_verdict


class Stage5ScalingTests(unittest.TestCase):
    def test_anchor_scaling_ratios_match_current_headline_result(self):
        # The anchor sources are tagged at their native observing frequencies:
        # FRB 20180916B at 600 MHz (CHIME), FRB 20121102A at 1400 MHz (Hessels
        # 2019 L-band). The predicted-ratio carries the model's intrinsic f^2
        # scaling, so the discrepancy factor is the frequency-normalized test
        # outcome even though raw observed values are at different bands.
        results = build_scaling_results()
        ratios = compute_anchor_scaling_ratios(results)

        self.assertAlmostEqual(ratios["observed_ratio"], 1.95, places=2)
        self.assertAlmostEqual(ratios["predicted_ratio"], 0.267, places=3)
        self.assertGreater(ratios["discrepancy_factor"], 5.0)
        self.assertLess(ratios["discrepancy_factor"], 10.0)
        self.assertIn("fails", scaling_verdict(ratios["discrepancy_factor"]))


if __name__ == "__main__":
    unittest.main()
