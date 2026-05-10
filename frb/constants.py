"""Physical constants and unit conversions used across the pipeline.

Inputs:
    Astropy's physical constants package.

Outputs:
    Repository-wide constants in SI or explicitly named astrophysical units,
    plus small conversion helpers for drift-rate units.

Pipeline role:
    Prevents silent inconsistencies in speed-of-light, AU, solar-luminosity, and
    MHz/ms conversions across stages. Code license: MIT -- see LICENSE for details.
"""

from astropy import constants as const

C_M_S = const.c.value
G_M3_KG_S2 = const.G.value
M_SUN_KG = const.M_sun.value
L_SUN_ERG_S = const.L_sun.to("erg/s").value
AU_M = const.au.value

SECONDS_PER_DAY = 86400.0
DAYS_PER_YEAR = 365.25

SOLAR_DIAMETER_M = 1.392e9
# Solar gravitational-lens focal distance used only as a fiducial scale.
# The passive Stage 4/5 calculation does not implement gravitational-lensing
# physics; active-tracking velocities scale linearly with this reference value.
FIDUCIAL_FOCAL_DISTANCE_AU = 550.0


def mhz_per_ms_to_hz_per_s(value: float) -> float:
    """Convert MHz/ms to Hz/s."""
    # 1 MHz/ms = 1e6 Hz / 1e-3 s = 1e9 Hz/s.
    return value * 1e9


def hz_per_s_to_mhz_per_ms(value: float) -> float:
    """Convert Hz/s to MHz/ms."""
    return value / 1e9
