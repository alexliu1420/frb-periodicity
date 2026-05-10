"""Stage 4 -- passive orbital-aberration beam-sweep aperture test.

Inputs:
    Curated periodic sources with representative drift rates from ``frb.data``.

Outputs:
    A printed table of orbital velocity, orbital acceleration, aberration sweep
    rate, and required aperture for each source.

Pipeline role:
    Tests whether a passive beam sweep tied to the activity period can reproduce
    observed ``df/dt`` values. This sets up the stricter population scaling test
    in Stage 5. Code license: MIT -- see LICENSE for details.
"""

import pandas as pd

from frb.constants import SOLAR_DIAMETER_M
from frb.data import sources_with_dfdt
from frb.models import passive_aberration_result


def run_stage4() -> pd.DataFrame:
    print("--- Stage 4: Passive Orbital-Aberration Beam Sweep ---")
    print("Assumption: df/dt is produced by orbital aberration and theta ~ lambda / D.")
    print("Propagation requirement: use only DM-corrected, preferably baseband/coherently dedispersed drift measurements.")

    rows = []
    for source in sources_with_dfdt():
        # The helper implements theta ~ lambda / D and df/dt = -f^2 D Omega / c,
        # with Omega taken to be the orbital-aberration rate a_orb / c.
        result = passive_aberration_result(
            period_days=source.period_days,
            dfdt_mhz_ms=source.dfdt_mhz_ms,
            frequency_mhz=source.dfdt_frequency_mhz,
            aperture_m=SOLAR_DIAMETER_M,
        )
        rows.append(
            {
                "source": source.name,
                "period_days": source.period_days,
                "obs_dfdt_mhz_ms": source.dfdt_mhz_ms,
                "dfdt_reference": source.dfdt_reference,
                "frequency_mhz": source.dfdt_frequency_mhz,
                "v_orb_km_s": result.orbital_velocity_km_s,
                "a_orb_m_s2": result.orbital_acceleration_m_s2,
                "omega_aberration_rad_s": result.sweep_rate_rad_s,
                "required_aperture_km": result.required_aperture_km,
                "solar_diameter_ratio": result.required_aperture_km / (SOLAR_DIAMETER_M / 1000.0),
            }
        )

    results = pd.DataFrame(rows)
    print(results.to_string(index=False))
    print(
        "\nAssessment: the FRB 20180916B aperture coincidence is reproduced under these assumptions, "
        "but this one-source match is not evidence without the Stage 5 scaling test."
    )
    return results


if __name__ == "__main__":
    run_stage4()
