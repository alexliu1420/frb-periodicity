"""Stage 15 -- spectral envelope and chromaticity constraints.

Inputs:
    Curated qualitative summaries and literature anchors for band-limited
    spectra and chromatic activity windows.

Outputs:
    A printed table of spectral/chromaticity cautions and relevant references.

Pipeline role:
    Flags the tension between achromatic source-frame predictions and observed
    chromatic/band-limited behavior, requiring propagation-aware analysis before
    interpretation. Code license: MIT -- see LICENSE
    for details.
"""

import pandas as pd

from frb.literature import references_for_topic


BANDWIDTH_SUMMARY = pd.DataFrame(
    [
        {
            "source": "FRB 20121102A",
            "observed_behavior": "band-limited bursts and frequency-dependent activity-window behavior",
            "required_control": "separate intrinsic envelope from bandpass, scintillation, scattering, and selection",
        },
        {
            "source": "FRB 20180916B",
            "observed_behavior": "bursts detected over a wide frequency range with chromatic activity windows",
            "required_control": "test achromaticity only after DM correction and propagation modeling",
        },
    ]
)


def run_stage15() -> pd.DataFrame:
    print("--- Stage 15: Spectral Envelope and Chromaticity ---")
    print(BANDWIDTH_SUMMARY.to_string(index=False))
    print(
        "\nAssessment: the original plan predicted achromatic source behavior, while narrowband directed-beam "
        "predictions imply the opposite. This stage is currently a tension to resolve, not "
        "evidence for either interpretation."
    )
    print("\nRelevant references:")
    seen: set[str] = set()
    for tag in ("chromaticity", "subburst", "baseband"):
        for ref in references_for_topic(tag):
            if ref.key in seen:
                continue
            seen.add(ref.key)
            print(f"- {ref.title}: {ref.url}")
    return BANDWIDTH_SUMMARY


if __name__ == "__main__":
    run_stage15()
