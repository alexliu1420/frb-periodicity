"""Stage 3 -- catalog repeater count and sample-size gate.

Inputs:
    A validated CHIME/FRB catalog CSV, defaulting to ``chimefrbcat1_data.csv``.
    Use ``python stage3_full_catalog_pipeline.py chimefrbcat2.csv`` after
    Stage 1 downloads Catalog 2.

Outputs:
    Printed catalog counts and a table of periodic/candidate-periodic sources
    tracked by this repository.

Pipeline role:
    Prevents population-level claims when the robust periodic-repeater sample is
    too small. This is the main n<5 guardrail for downstream interpretation.
    Code license: MIT -- see LICENSE for details.
"""

import argparse

import pandas as pd

from frb.catalog import (
    count_events_for_aliases,
    load_chime_catalog,
    named_repeater_event_count,
    named_repeater_source_count,
    repeater_counts,
    unique_event_count,
)
from frb.data import sources_with_periods


def run_pipeline(path: str = "chimefrbcat1_data.csv") -> pd.DataFrame:
    print("--- Stage 3: Catalog and Sample-Size Check ---")
    df = load_chime_catalog(path)
    # CHIME uses -9999 as a missing-value sentinel; the helper excludes it so
    # unknown one-off bursts are not counted as a repeating source.
    counts = repeater_counts(df)
    named_sources = named_repeater_source_count(df)
    unique_events = unique_event_count(df)
    named_repeater_events = named_repeater_event_count(df)
    periodic_sources = sources_with_periods(include_candidates=True)
    robust_periodic = sources_with_periods(include_candidates=False)

    print(f"Catalog rows: {len(df)}")
    print(f"Unique FRB events: {unique_events}")
    print(f"Named non-sentinel repeater labels: {named_sources}")
    print(f"Unique events associated with named repeaters: {named_repeater_events}")
    print(f"Named repeaters with at least two bursts in this catalog: {len(counts)}")
    print(f"Periodic/candidate-periodic sources tracked by this pipeline: {len(periodic_sources)}")
    print(f"Robust periodic sources tracked by this pipeline: {len(robust_periodic)}")

    rows = []
    for source in periodic_sources:
        rows.append(
            {
                "source": source.name,
                "period_days": source.period_days,
                "window_days": source.window_days,
                "duty_cycle": source.duty_cycle,
                "status": source.period_status,
                "period_reference": source.period_reference,
                "catalog_event_count": count_events_for_aliases(df, {source.name, *source.aliases}),
                "population_inference_allowed": False,
            }
        )

    results = pd.DataFrame(rows)
    print("\nTracked periodic sources:")
    print(results.to_string(index=False))
    print(
        "\nFalsification/status: n < 5, so population-level claims are descriptive only. "
        "This stage must not be used to claim statistical significance."
    )
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Stage 3 catalog/repeater summary.")
    parser.add_argument("catalog_path", nargs="?", default="chimefrbcat1_data.csv")
    args = parser.parse_args()
    run_pipeline(args.catalog_path)
