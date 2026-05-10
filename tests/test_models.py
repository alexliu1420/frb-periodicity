"""Unit tests for core FRB periodicity model calculations.

Inputs:
    No external data files. Tests use fixed numerical anchors from the shared
    model functions.

Outputs:
    Standard unittest pass/fail results.

Pipeline role:
    Guards the physics calculations against accidental changes during future
    public-release maintenance. Code license: MIT -- see LICENSE for details.
"""

import unittest

from frb.constants import SOLAR_DIAMETER_M, hz_per_s_to_mhz_per_ms, mhz_per_ms_to_hz_per_s
from frb.models import active_tracking_result, energy_budget, kepler_period_days, passive_aberration_result


class ModelTests(unittest.TestCase):
    def test_unit_conversion(self):
        self.assertEqual(mhz_per_ms_to_hz_per_s(1.0), 1e9)
        self.assertEqual(hz_per_s_to_mhz_per_ms(1e9), 1.0)

    def test_kepler_earth_orbit(self):
        self.assertAlmostEqual(kepler_period_days(1.0, 1.0), 365.25, places=6)

    def test_passive_aberration_frb20180916b_anchor(self):
        result = passive_aberration_result(16.35, -2.0, 600.0, SOLAR_DIAMETER_M)
        self.assertAlmostEqual(result.orbital_velocity_km_s, 83.885, places=3)
        self.assertAlmostEqual(result.required_aperture_km, 1.33824e6, delta=2e3)
        self.assertAlmostEqual(result.predicted_dfdt_mhz_ms, -2.0803, places=3)

    def test_active_tracking_anchor(self):
        result = active_tracking_result(-2.0, 600.0)
        self.assertAlmostEqual(result.transverse_velocity_km_s, 98.446, places=3)

    def test_energy_budget_anchor(self):
        result = energy_budget(1e38, 2.0, 600.0)
        self.assertAlmostEqual(result.beaming_fraction, 8.05268e-21, delta=1e-25)
        self.assertAlmostEqual(result.true_power_l_sun, 1.0518e-13, delta=1e-17)


if __name__ == "__main__":
    unittest.main()
