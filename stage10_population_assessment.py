"""Stage 10 -- population assessment under the current sample-size limit.

Inputs:
    Curated periodic/candidate-periodic sources with period, activity-window,
    and host-environment summaries.

Outputs:
    A printed descriptive table and references relevant to candidate periodicity.

Pipeline role:
    Keeps the population-level conclusion honest: current n is too small for
    statistical inference, so this stage only records descriptive covariates for
    future expansion. Code license: MIT -- see LICENSE
    for details.
"""

import pandas as pd

from frb.data import PERIODIC_SOURCES
from frb.literature import references_for_topic
from frb.models import duty_cycle


def run_stage10() -> pd.DataFrame:
    print("--- Stage 10: Population Assessment Under n<5 Constraint ---")

    rows = []
    for source in PERIODIC_SOURCES:
        if source.period_days is None or source.window_days is None:
            continue
        # Duty cycle is retained as a descriptive statistic only; with n<5 it
        # cannot establish a population law.
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
                "host_reference": source.host_reference,
                "host_summary": source.host_summary,
            }
        )

    results = pd.DataFrame(rows)
    print(results.to_string(index=False))
    print("\nAssessment: with n=2 robust periodic sources plus one candidate, this is descriptive only.")
    print("Old stellar environments challenge young-core-collapse-only progenitor channels, but do not rule out natural old-population channels.")
    print("\nRelevant references:")
    for ref in references_for_topic("periodicity"):
        print(f"- {ref.title}: {ref.url}")
    return results


if __name__ == "__main__":
    run_stage10()
