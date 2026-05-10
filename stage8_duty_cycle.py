"""Stage 8 -- duty-cycle visibility interpretation.

Inputs:
    Curated periodic/candidate-periodic sources with period and activity-window
    estimates.

Outputs:
    A printed table of duty cycles and equivalent visible-longitude angles.

Pipeline role:
    Evaluates whether activity-window fractions are compatible with a rotating
    visibility-window hypothesis, while preserving the n<5 limitation and
    heterogeneous-window caveat. Code license: MIT -- see LICENSE for details.
"""

import pandas as pd

from frb.data import PERIODIC_SOURCES
from frb.models import duty_cycle, kepler_period_days


def run_stage8() -> pd.DataFrame:
    print("--- Stage 8: Duty Cycle and Rotation-Window Interpretation ---")
    print("Hypothesis tested: activity window fraction could reflect visibility over a rotating platform.")

    rows = []
    for source in PERIODIC_SOURCES:
        if source.period_days is None or source.window_days is None:
            continue
        # Visible angle is a descriptive mapping: duty cycle times 360 degrees.
        # It is not by itself evidence for a rotating platform.
        duty, angle = duty_cycle(source.period_days, source.window_days)
        rows.append(
            {
                "source": source.name,
                "period_days": source.period_days,
                "window_days": source.window_days,
                "duty_cycle": duty,
                "visible_angle_deg": angle,
                "period_status": source.period_status,
                "period_reference": source.period_reference,
            }
        )

    results = pd.DataFrame(rows)
    print(results.to_string(index=False))
    print(f"\nReference: a fiducial 550 AU orbit around 1 solar mass has P = {kepler_period_days(550.0):.0f} days.")
    print(
        "Assessment: duty cycles of order 0.3-0.7 are compatible with a visibility-window idea, "
        "but the sample is too small and window definitions are heterogeneous. This is a hypothesis, not a proof."
    )
    return results


if __name__ == "__main__":
    run_stage8()
