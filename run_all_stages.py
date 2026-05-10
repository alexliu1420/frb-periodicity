"""Run the reproducible, non-download stages of the pipeline.

Inputs:
    The local validated catalog file and curated source assumptions used by the
    individual stage modules.

Outputs:
    Prints each stage report in order. It does not write new analysis products
    beyond any outputs produced by the called stage functions.

Pipeline role:
    Provides a single command for replication and smoke testing after changes.
    Stage 1 downloads are intentionally excluded to keep this runner
    deterministic. Code license: MIT -- see LICENSE
    for details.
"""

import argparse

from stage2_orbital_mechanics import run_stage2_model
from stage3_full_catalog_pipeline import run_pipeline
from stage4_subburst_analysis import run_stage4
from stage5_scaling_test import run_stage5
from stage6_active_tracking import run_stage6
from stage7_energy_budget import run_stage7
from stage8_duty_cycle import run_stage8
from stage9_data_quality import run_stage9
from stage10_population_assessment import run_stage10
from stage11_polarization_synthesis import run_stage11
from stage12_target_mapping import run_stage12
from stage13_rvm_residuals import run_stage13
from stage14_control_group import run_stage14
from stage15_spectral_envelope import run_stage15
from stage16_rm_stability import run_stage16


def build_stages(catalog_path: str):
    """Build stage callables, injecting the selected catalog into Stage 3."""
    return (
        run_stage2_model,
        lambda: run_pipeline(catalog_path),
        run_stage4,
        run_stage5,
        run_stage6,
        run_stage7,
        run_stage8,
        run_stage9,
        run_stage10,
        run_stage11,
        run_stage12,
        run_stage13,
        run_stage14,
        run_stage15,
        run_stage16,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the non-download FRB periodicity stages.")
    parser.add_argument("--catalog", default="chimefrbcat1_data.csv", help="Catalog CSV path for Stage 3.")
    args = parser.parse_args()

    for stage in build_stages(args.catalog):
        print("\n" + "=" * 88)
        stage()
