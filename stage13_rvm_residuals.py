"""Stage 13 -- RVM fitting demonstration.

Inputs:
    Synthetic polarization-angle arrays generated inside the script.

Outputs:
    A printed table of RVM fit statistics for flat and RVM-like synthetic cases.

Pipeline role:
    Demonstrates the fitting machinery without claiming source-level
    significance. Real publication claims require RM-corrected burst PA data,
    uncertainties, priors, and natural-model comparison. Code license: MIT --
    see LICENSE for details.
"""

import numpy as np
import pandas as pd

from frb.literature import references_for_topic
from frb.models import fit_rvm_to_pa, rvm_model


def run_stage13() -> pd.DataFrame:
    print("--- Stage 13: RVM Fit Demonstration ---")
    print("This stage demonstrates the fitting machinery on synthetic data.")
    print("Publication-level claims require real PA arrays, RM correction, and model priors.")

    # Synthetic phase grid across a narrow burst window. Real data should use
    # observed pulse phase/time samples after RM correction.
    phases = np.linspace(-0.1, 0.1, 100)
    pa_error = np.full_like(phases, 0.05)

    synthetic_cases = {
        "flat_pa": np.zeros_like(phases),
        "typical_rvm_pa": rvm_model(phases, np.radians(45.0), np.radians(50.0), 0.0, 0.0),
    }

    rows = []
    for name, observed_pa in synthetic_cases.items():
        # The fit optimizes RVM geometry instead of comparing against one
        # arbitrary "typical" geometry, avoiding the earlier false rejection.
        fit = fit_rvm_to_pa(phases, observed_pa, pa_error)
        alpha, zeta, psi0, phi0 = fit.fitted_parameters
        rows.append(
            {
                "case": name,
                "chi_squared": fit.chi_squared,
                "dof": fit.dof,
                "reduced_chi_squared": fit.reduced_chi_squared,
                "alpha_deg": np.degrees(alpha),
                "zeta_deg": np.degrees(zeta),
                "note": fit.note,
            }
        )

    results = pd.DataFrame(rows)
    print(results.to_string(index=False))
    print(
        "\nAssessment: a flat PA can be fit by special RVM geometries, so the key scientific question is "
        "not whether one arbitrary RVM curve fails. The question is whether real PA data prefer one "
        "model class after accounting for priors and alternatives."
    )
    print("\nRelevant references:")
    for ref in references_for_topic("rvm"):
        print(f"- {ref.title}: {ref.url}")
    return results


if __name__ == "__main__":
    run_stage13()
