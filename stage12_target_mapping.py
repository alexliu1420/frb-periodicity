"""Stage 12 -- host and local-environment mapping.

Inputs:
    A curated table of host/local-environment summaries for the tracked
    periodic or candidate-periodic repeaters.

Outputs:
    A printed table of environments, scientific uses, and cautions.

Pipeline role:
    Records environmental covariates for future tests while avoiding unsupported
    inferences about target destinations or intent. Code license: MIT -- see
    LICENSE for details.
"""

import pandas as pd


TARGET_ENVIRONMENTS = pd.DataFrame(
    [
        {
            "source": "FRB 20121102A",
            "environment": "dwarf star-forming host; compact local environment",
            "scientific_use": "tests whether source environment correlates with period, RM, and drift behavior",
            "caution": "do not infer target destination without an independent geometric observable",
        },
        {
            "source": "FRB 20180916B",
            "environment": "near a star-forming region in a nearby spiral galaxy",
            "scientific_use": "nearby benchmark for high-quality timing, polarization, and propagation checks",
            "caution": "offset/environment are compatible with multiple progenitor channels",
        },
        {
            "source": "FRB 20240209A",
            "environment": "old stellar population / quiescent elliptical context",
            "scientific_use": "candidate test of delayed or old-population progenitor channels",
            "caution": "periodicity is candidate-level and natural old-population channels remain viable",
        },
    ]
)


def run_stage12() -> pd.DataFrame:
    print("--- Stage 12: Host and Local-Environment Mapping ---")
    print(TARGET_ENVIRONMENTS.to_string(index=False))
    print(
        "\nAssessment: environments are important covariates for source modeling. "
        "They should be used to define tests, not to infer logistical intent."
    )
    return TARGET_ENVIRONMENTS


if __name__ == "__main__":
    run_stage12()
