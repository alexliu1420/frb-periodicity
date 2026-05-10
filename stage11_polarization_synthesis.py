"""Stage 11 -- polarization literature synthesis.

Inputs:
    Curated literature anchors from ``frb.literature`` and a compact summary of
    polarization behavior for key repeaters.

Outputs:
    A printed qualitative table and the relevant PA/RVM references.

Pipeline role:
    Frames polarization as a natural-comparator constraint rather than a
    standalone discriminator. Code license: MIT -- see LICENSE for details.
"""

import pandas as pd

from frb.literature import references_for_topic


POLARIZATION_SUMMARY = pd.DataFrame(
    [
        {
            "source": "FRB 20180916B",
            "summary": "high linear polarization; PA constrained on short timescales; periodic PA behavior reported",
            "interpretation": "strongly constrains simple precession, but rotational/natural models remain comparators",
        },
        {
            "source": "FRB 20121102A",
            "summary": "high linear polarization and extreme RM environment reported in literature",
            "interpretation": "requires RM-aware PA treatment; not a stand-alone engineered-beam discriminator",
        },
    ]
)


def run_stage11() -> pd.DataFrame:
    print("--- Stage 11: Polarization Synthesis ---")
    print(POLARIZATION_SUMMARY.to_string(index=False))
    print(
        "\nAssessment: flat or slowly varying PA can support a coherent-wavefront hypothesis, "
        "but it does not by itself eliminate magnetospheric or rotational natural models."
    )
    print("\nRelevant references:")
    seen: set[str] = set()
    for tag in ("polarization", "rvm"):
        for ref in references_for_topic(tag):
            if ref.key in seen:
                continue
            seen.add(ref.key)
            print(f"- {ref.title}: {ref.url}")
    return POLARIZATION_SUMMARY


if __name__ == "__main__":
    run_stage11()
