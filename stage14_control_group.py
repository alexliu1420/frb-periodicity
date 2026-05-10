"""Stage 14 -- non-periodic repeater active-tracking sensitivity examples.

Inputs:
    Curated non-periodic or unconfirmed-period repeater examples with rough
    representative drift rates.

Outputs:
    A printed table of active-tracking transverse velocities at several
    fiducial distances.

Pipeline role:
    Shows how the active-tracking mapping behaves for control-like sources. It
    is a sensitivity check, not evidence that the model is universal. Code license: MIT -- see LICENSE for details.
"""

import pandas as pd

from frb.data import CONTROL_SOURCES
from frb.models import active_tracking_result


def run_stage14() -> pd.DataFrame:
    print("--- Stage 14: Non-Periodic Repeater Sensitivity Examples ---")
    print("Purpose: show what velocities are implied by the active-tracking mapping for non-periodic repeaters.")
    print("Caution: because the mapping accepts any df/dt, this is not a proof of universality.")
    print("The velocity scale is linear in the adopted distance; 550 AU is only the reference normalization.")

    rows = []
    for source in CONTROL_SOURCES:
        if source.dfdt_mhz_ms is None or source.dfdt_frequency_mhz is None:
            continue
        # Any df/dt can be inverted into an Omega in this model; this is why the
        # stage is labeled a sensitivity example rather than a discriminator.
        result_100 = active_tracking_result(source.dfdt_mhz_ms, source.dfdt_frequency_mhz, focal_distance_au=100.0)
        result_550 = active_tracking_result(source.dfdt_mhz_ms, source.dfdt_frequency_mhz, focal_distance_au=550.0)
        result_1000 = active_tracking_result(source.dfdt_mhz_ms, source.dfdt_frequency_mhz, focal_distance_au=1000.0)
        rows.append(
            {
                "source": source.name,
                "frequency_mhz": source.dfdt_frequency_mhz,
                "obs_dfdt_mhz_ms": source.dfdt_mhz_ms,
                "dfdt_reference": source.dfdt_reference,
                "v_transverse_100au_km_s": result_100.transverse_velocity_km_s,
                "v_transverse_550au_km_s": result_550.transverse_velocity_km_s,
                "v_transverse_1000au_km_s": result_1000.transverse_velocity_km_s,
                "data_status": source.dfdt_status,
            }
        )

    results = pd.DataFrame(rows)
    print(results.to_string(index=False))
    print(
        "\nAssessment: these examples remain within a broad plausible speed range, but a robust test "
        "needs a pre-declared velocity prior and burst-level uncertainties."
    )
    return results


if __name__ == "__main__":
    run_stage14()
