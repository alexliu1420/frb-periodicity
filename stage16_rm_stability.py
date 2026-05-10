"""Stage 16 -- rotation-measure stability and magneto-ionic environment.

Inputs:
    Curated qualitative RM summaries and literature anchors for key repeaters
    and RM-variability comparators.

Outputs:
    A printed table describing RM behavior and model impact.

Pipeline role:
    Treats RM behavior as a quantitative environmental diagnostic rather than a
    one-source knockout argument against natural models. Code license: MIT --
    see LICENSE for details.
"""

import pandas as pd

from frb.literature import references_for_topic


RM_SUMMARY = pd.DataFrame(
    [
        {
            "source": "FRB 20180916B",
            "rm_behavior": "reported stochastic and secular evolution; not a single permanently stable value",
            "model_impact": "constrains dense/turbulent propagation scenarios but does not falsify all binary models",
        },
        {
            "source": "FRB 20121102A",
            "rm_behavior": "extreme and time-variable RM environment reported in literature",
            "model_impact": "strong natural comparator for magnetized local environments",
        },
        {
            "source": "FRB 20220529",
            "rm_behavior": "reported as possible binary/RM-periodicity candidate",
            "model_impact": "shows RM periodicity is a live natural-model diagnostic",
        },
    ]
)


def run_stage16() -> pd.DataFrame:
    print("--- Stage 16: RM Stability and Magneto-Ionic Environment ---")
    print(RM_SUMMARY.to_string(index=False))
    print(
        "\nAssessment: RM behavior should be modeled quantitatively across phase and epoch. "
        "Stable or slowly varying RM can constrain some wind models, but it is not a standalone "
        "falsification of natural explanations."
    )
    print("\nRelevant references:")
    for ref in references_for_topic("rm"):
        print(f"- {ref.title}: {ref.url}")
    return RM_SUMMARY


if __name__ == "__main__":
    run_stage16()
