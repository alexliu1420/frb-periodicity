"""Stage 9 -- data-quality and propagation controls.

Inputs:
    The publication-control checklist maintained in ``stage9_data_quality.md``
    and literature anchors for sub-burst drift and baseband measurement.

Outputs:
    A printed checklist of required controls before interpreting drift,
    achromaticity, polarization angle, or scintillation-sensitive structure.

Pipeline role:
    Makes the propagation gate visible in ``run_all_stages.py``. It does not
    transform data; it prevents downstream stages from being read as
    publication-grade until burst-level controls are satisfied. Code license: MIT -- see LICENSE for details.
"""

from frb.literature import references_for_topic


CONTROLS = (
    "Apply and document DM correction before frequency-dependent analysis.",
    "Restrict achromaticity claims to post-DM-correction, propagation-modeled data.",
    "Record observing frequency, bandwidth, df/dt uncertainty, and burst provenance.",
    "Check scattering and scintillation timescales before assigning sub-burst structure to beam sweep.",
    "Correct polarization angles for RM before RVM or flat-PA interpretation.",
    "Carry the n<5 sample-size gate (currently 2 robust periodic sources plus 1 candidate) into every population-level statement.",
)


def run_stage9() -> tuple[str, ...]:
    print("--- Stage 9: Data Quality and Propagation Controls ---")
    for control in CONTROLS:
        print(f"- {control}")
    print(
        "\nAssessment: stages using representative df/dt or qualitative PA/RM summaries are "
        "exploratory until these controls are applied to burst-level measurements."
    )
    print("\nRelevant references:")
    seen: set[str] = set()
    for tag in ("stage9", "subburst", "baseband"):
        for ref in references_for_topic(tag):
            if ref.key in seen:
                continue
            seen.add(ref.key)
            print(f"- {ref.title}: {ref.url}")
    return CONTROLS


if __name__ == "__main__":
    run_stage9()
