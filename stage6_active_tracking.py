"""Stage 6 -- active-tracking kinematic consistency check.

Inputs:
    Curated sources with representative drift rates and observing frequencies.

Outputs:
    A printed table mapping each ``df/dt`` value to angular sweep rate and
    transverse velocity at several fiducial distances, including 550 AU.

Pipeline role:
    Tests whether an active beam-sweep interpretation is kinematically plausible
    after the passive orbital-aberration model fails. This stage is explicitly
    not a proof because the mapping is underconstrained. Code license: MIT --
    see LICENSE for details.
"""

import pandas as pd

from frb.data import sources_with_dfdt
from frb.models import active_tracking_result


def run_stage6() -> pd.DataFrame:
    print("--- Stage 6: Active Tracking Kinematic Consistency Check ---")
    print("Hypothesis tested: df/dt is caused by active beam tracking, decoupled from the activity period.")
    print("Important: this maps an observed drift to a velocity; it is not by itself a discriminating proof.")
    print("The transverse velocity scales linearly with the adopted distance; 550 AU is a fiducial normalization.")

    rows = []
    for source in sources_with_dfdt():
        # Active tracking inverts the same beam-width relation as Stage 4, but
        # Omega is no longer tied to the macroscopic activity period.
        result_100 = active_tracking_result(source.dfdt_mhz_ms, source.dfdt_frequency_mhz, focal_distance_au=100.0)
        result_550 = active_tracking_result(source.dfdt_mhz_ms, source.dfdt_frequency_mhz, focal_distance_au=550.0)
        result_1000 = active_tracking_result(source.dfdt_mhz_ms, source.dfdt_frequency_mhz, focal_distance_au=1000.0)
        rows.append(
            {
                "source": source.name,
                "obs_dfdt_mhz_ms": source.dfdt_mhz_ms,
                "dfdt_reference": source.dfdt_reference,
                "frequency_mhz": source.dfdt_frequency_mhz,
                "omega_track_rad_s": result_550.sweep_rate_rad_s,
                "v_transverse_100au_km_s": result_100.transverse_velocity_km_s,
                "v_transverse_550au_km_s": result_550.transverse_velocity_km_s,
                "v_transverse_1000au_km_s": result_1000.transverse_velocity_km_s,
                "data_status": source.dfdt_status,
            }
        )

    results = pd.DataFrame(rows)
    print(results.to_string(index=False))
    print(
        "\nAssessment: inferred velocities are within plausible kinematic limits under these assumptions, but the model remains "
        "underconstrained until it predicts drift distributions or rejects some measured bursts."
    )
    return results


if __name__ == "__main__":
    run_stage6()
