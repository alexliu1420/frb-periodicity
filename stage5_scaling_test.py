"""Stage 5 -- passive directed-beam P^(-4/3) scaling test.

Inputs:
    Curated periodic sources with representative ``df/dt`` values.

Outputs:
    A printed comparison of observed drift rates, predicted passive drift
    rates, and required apertures.

Pipeline role:
    Provides the key negative result for the passive orbital-aberration model:
    at fixed aperture and frequency, Keplerian acceleration predicts
    ``|df/dt| proportional to P^(-4/3)``. The verdict threshold below treats a
    factor-of-five disagreement between observed and predicted drift-ratio
    scaling as a failure under the stated assumptions. Code license: MIT -- see
    LICENSE for details.
"""

import pandas as pd

from frb.constants import SOLAR_DIAMETER_M
from frb.data import sources_with_dfdt
from frb.models import passive_aberration_result


ANCHOR_SOURCES = ("FRB 20180916B", "FRB 20121102A")
SCALING_FAILURE_FACTOR = 5.0


def build_scaling_results() -> pd.DataFrame:
    """Return passive-aberration predictions for sources with curated drift rates."""
    rows = []
    for source in sources_with_dfdt():
        # Reuse the same passive-aberration model as Stage 4 so the cross-source
        # scaling test is exactly tied to the one-source aperture calculation.
        result = passive_aberration_result(
            period_days=source.period_days,
            dfdt_mhz_ms=source.dfdt_mhz_ms,
            frequency_mhz=source.dfdt_frequency_mhz,
            aperture_m=SOLAR_DIAMETER_M,
        )
        rows.append(
            {
                "source": source.name,
                "period_days": source.period_days,
                "obs_dfdt_mhz_ms": source.dfdt_mhz_ms,
                "dfdt_reference": source.dfdt_reference,
                "pred_dfdt_mhz_ms": result.predicted_dfdt_mhz_ms,
                "required_aperture_km": result.required_aperture_km,
            }
        )

    return pd.DataFrame(rows)


def compute_anchor_scaling_ratios(results: pd.DataFrame) -> dict[str, float]:
    """Compute Stage 5 ratios for the named anchor-source comparison."""
    by_source = results.set_index("source", drop=False)
    missing = [source for source in ANCHOR_SOURCES if source not in by_source.index]
    if missing:
        raise ValueError(f"Stage 5 anchor source(s) missing from results: {missing}")

    first = by_source.loc[ANCHOR_SOURCES[0]]
    second = by_source.loc[ANCHOR_SOURCES[1]]
    observed_ratio = abs(second["obs_dfdt_mhz_ms"] / first["obs_dfdt_mhz_ms"])
    predicted_ratio = abs(second["pred_dfdt_mhz_ms"] / first["pred_dfdt_mhz_ms"])
    return {
        "period_ratio": second["period_days"] / first["period_days"],
        "observed_ratio": observed_ratio,
        "predicted_ratio": predicted_ratio,
        "discrepancy_factor": observed_ratio / predicted_ratio,
    }


def scaling_verdict(discrepancy_factor: float) -> str:
    """Return a data-derived verdict for the passive scaling comparison."""
    if discrepancy_factor >= SCALING_FAILURE_FACTOR or discrepancy_factor <= 1.0 / SCALING_FAILURE_FACTOR:
        magnitude = max(discrepancy_factor, 1.0 / discrepancy_factor)
        return f"fails by factor {magnitude:.1f} under these assumptions"
    return f"is consistent within factor {discrepancy_factor:.1f} under these assumptions"


def run_stage5() -> pd.DataFrame:
    print("--- Stage 5: Passive Directed-Beam P^(-4/3) Scaling Test ---")
    print("Hypothesis tested: fixed stellar-sized aperture, passive orbital aberration, comparable stellar masses.")

    results = build_scaling_results()
    print(results.to_string(index=False))

    ratios = compute_anchor_scaling_ratios(results)
    # The named 20180916B-vs-20121102A comparison is the direct P^(-4/3)
    # falsification check for the passive model.
    print(f"\nRatios using anchor sources {ANCHOR_SOURCES[0]} and {ANCHOR_SOURCES[1]}:")
    print(f"Period ratio: {ratios['period_ratio']:.2f}")
    print(f"Observed |df/dt| ratio: {ratios['observed_ratio']:.2f}")
    print(f"Predicted |df/dt| ratio: {ratios['predicted_ratio']:.3f}")

    print(
        f"\nAssessment: the passive orbital-aberration directed-beam model "
        f"{scaling_verdict(ratios['discrepancy_factor'])}. This does not test active tracking."
    )
    print(
        "Caveat: this conclusion uses representative df/dt values from frb/data.py. "
        "Stage 9 controls--DM correction, frequency normalization, and burst-level "
        "uncertainties--are required before publication-grade falsification."
    )
    return results


if __name__ == "__main__":
    run_stage5()
