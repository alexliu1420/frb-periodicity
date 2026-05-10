"""Stage 7 -- beaming and energy-budget sensitivity.

Inputs:
    Representative isotropic-equivalent burst energies and durations.

Outputs:
    A printed table with beam divergence, beaming fraction, true energy, and
    true power in solar-luminosity units under the adopted aperture assumption.

Pipeline role:
    Shows how strongly inferred energetics depend on beaming assumptions. It
    does not establish the beaming mechanism. Code license: MIT -- see LICENSE for details.
"""

import numpy as np
import pandas as pd

from frb.models import energy_budget


ENERGY_EXAMPLES = pd.DataFrame(
    [
        {"source": "FRB 20180916B", "isotropic_energy_erg": 1e38, "duration_ms": 2.0},
        {"source": "FRB 20121102A", "isotropic_energy_erg": 1e39, "duration_ms": 2.0},
    ]
)


def run_stage7() -> pd.DataFrame:
    print("--- Stage 7: Beaming and Energy Budget Sensitivity ---")
    print("Assumption: diffraction-limited circular aperture with D equal to the solar diameter at 600 MHz.")
    print("Numbers use a single 600 MHz reference frequency; beaming fraction rescales as (f_ref / f)^2.")
    print("Caution: this is an aperture assumption, not an established gravitational-lens transfer calculation.")

    rows = []
    for _, row in ENERGY_EXAMPLES.iterrows():
        # The helper computes theta ~ lambda / D, solid angle ~ pi(theta/2)^2,
        # then scales isotropic-equivalent energy by Omega_beam / 4pi.
        result = energy_budget(row["isotropic_energy_erg"], row["duration_ms"])
        rows.append(
            {
                "source": row["source"],
                "log10_e_iso_erg": np.log10(row["isotropic_energy_erg"]),
                "beam_divergence_rad": result.beam_divergence_rad,
                "beaming_fraction": result.beaming_fraction,
                "log10_e_true_erg": np.log10(result.true_energy_erg),
                "p_true_l_sun": result.true_power_l_sun,
            }
        )

    results = pd.DataFrame(rows)
    print(results.to_string(index=False))
    print(
        "\nAssessment: under the adopted collimation assumption, required true powers are about "
        "10^-13 to 10^-12 L_sun for these examples. This demonstrates energetic sensitivity "
        "to beaming assumptions; it does not establish the beaming mechanism."
    )
    return results


if __name__ == "__main__":
    run_stage7()
