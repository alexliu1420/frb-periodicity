"""Stage 2 -- broad Keplerian orbital-period bounds.

Inputs:
    Curated source assumptions from ``frb.data``: source redshifts and reported
    activity periods.

Outputs:
    A printed table and ``stage2_results.csv`` containing observed-frame period
    bounds for broad circular orbits.

Pipeline role:
    Establishes that simple orbital-period consistency is too broad to be
    discriminating, motivating the tighter Stage 4/5 drift-scaling tests. Code
    license: MIT -- see LICENSE for details.
"""

import pandas as pd

from frb.data import PERIODIC_SOURCES
from frb.models import observed_orbital_period_range


def run_stage2_model() -> pd.DataFrame:
    print("Running Stage 2: Keplerian Period Bounds")
    print("Assumption: circular orbits around a 1 solar-mass star, 0.1-50 AU.")

    rows = []
    for source in PERIODIC_SOURCES:
        if source.redshift is None:
            continue
        # Keplerian rest-frame bounds are multiplied by (1 + z) inside the
        # helper, because the reported activity period is observed at Earth.
        min_days, max_days = observed_orbital_period_range(source.redshift)
        observed = source.period_days
        is_consistent = observed is not None and min_days <= observed <= max_days
        rows.append(
            {
                "source_id": source.name,
                "period_status": source.period_status,
                "period_reference": source.period_reference,
                "z": source.redshift,
                "redshift_reference": source.redshift_reference,
                "observed_period_days": observed,
                "predicted_min_days": min_days,
                "predicted_max_days": max_days,
                "is_consistent": is_consistent,
                "interpretation": "non-discriminating broad bound" if is_consistent else "outside adopted broad bound",
            }
        )

    results = pd.DataFrame(rows)
    print(results.to_string(index=False))
    results.to_csv("stage2_results.csv", index=False)
    print("\nAssessment: these bounds are too broad to support the hypothesis by themselves.")
    return results


if __name__ == "__main__":
    run_stage2_model()
