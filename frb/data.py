"""Curated source metadata with uncertainty notes.

The values here are deliberately compact and traceable. They are not intended to
replace a literature database; they are the assumptions used by the stage
scripts. Any new FRB added to the pipeline should enter here with a status note.

Inputs:
    Literature-derived source metadata maintained manually in this file.

Outputs:
    Immutable dataclass records and helper selectors for periodic, control, and
    drift-bearing sources.

Pipeline role:
    Makes the scientific assumptions explicit and auditable. Code license: MIT -- see LICENSE for details.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceAssumption:
    name: str
    aliases: tuple[str, ...]
    redshift: float | None
    period_days: float | None
    window_days: float | None
    period_status: str
    dfdt_mhz_ms: float | None
    dfdt_frequency_mhz: float | None
    dfdt_status: str
    host_summary: str
    notes: str
    period_reference: str | None = None
    dfdt_reference: str | None = None
    redshift_reference: str | None = None
    host_reference: str | None = None

    @property
    def duty_cycle(self) -> float | None:
        # Duty cycle is undefined when either the period or activity window is
        # unknown; callers use None to keep candidate data out of hard claims.
        if self.period_days is None or self.window_days is None:
            return None
        if self.period_days == 0:
            return None
        return self.window_days / self.period_days


PERIODIC_SOURCES: tuple[SourceAssumption, ...] = (
    SourceAssumption(
        name="FRB 20180916B",
        aliases=("FRB 180916.B", "FRB20180916B"),
        redshift=0.0337,
        period_days=16.35,
        window_days=5.0,
        period_status="robust periodic activity window",
        dfdt_mhz_ms=-2.0,
        dfdt_frequency_mhz=600.0,
        dfdt_status="representative literature value; must be replaced by burst-level baseband measurements for inference",
        host_summary="near a star-forming region in a nearby spiral galaxy",
        notes="Use as the best current anchor for periodic-window tests, but avoid treating one drift value as universal.",
        period_reference="chime_2020_frb20180916b_periodicity",
        dfdt_reference="pleunis_2021_chime_morphology",
        redshift_reference="marcote_2020_frb20180916b_host",
        host_reference="marcote_2020_frb20180916b_host",
    ),
    SourceAssumption(
        name="FRB 20121102A",
        aliases=("FRB 121102A", "FRB20121102A"),
        redshift=0.19273,
        period_days=157.0,
        window_days=90.0,
        period_status="reported long activity cycle; window estimate varies across analyses",
        dfdt_mhz_ms=-3.9,
        dfdt_frequency_mhz=600.0,
        dfdt_status="representative value normalized for the exploratory scaling test; not a source-wide constant",
        host_summary="dwarf star-forming host; complex magneto-ionic environment",
        notes="Window duration is a major sensitivity for duty-cycle claims.",
        period_reference="rajwade_2020_frb121102_periodicity",
        dfdt_reference="hessels_2019_frb121102_drift",
        redshift_reference="tendulkar_2017_frb121102_host",
        host_reference="tendulkar_2017_frb121102_host",
    ),
    SourceAssumption(
        name="FRB 20240209A",
        aliases=("FRB20240209A",),
        redshift=0.1384,
        period_days=126.0,
        window_days=88.0,
        period_status="possible periodicity; treat as candidate until independently confirmed",
        dfdt_mhz_ms=None,
        dfdt_frequency_mhz=None,
        dfdt_status="no curated drift value in this pipeline",
        host_summary="quiescent elliptical / old stellar population environment",
        notes="Useful for future tests, not for current population significance.",
        period_reference="frb20240209a_periodicity_2025",
        redshift_reference="frb20240209a_periodicity_2025",
        host_reference="frb20240209a_periodicity_2025",
    ),
)


CONTROL_SOURCES: tuple[SourceAssumption, ...] = (
    SourceAssumption(
        name="FRB 20190520B",
        aliases=("FRB20190520B",),
        redshift=0.241,
        period_days=None,
        window_days=None,
        period_status="no confirmed macroscopic period",
        dfdt_mhz_ms=-10.0,
        dfdt_frequency_mhz=1250.0,
        dfdt_status="rough literature-scale value; use only as a sensitivity example",
        host_summary="highly active repeater with complex local environment",
        notes="Do not use as evidence for universal active tracking without burst-level checks.",
        dfdt_reference="frb20190520b_burst_comparison_2023",
        redshift_reference="niu_2022_frb20190520b_host",
        host_reference="niu_2022_frb20190520b_host",
    ),
    SourceAssumption(
        name="FRB 20201124A",
        aliases=("FRB20201124A",),
        redshift=None,
        period_days=None,
        window_days=None,
        period_status="no stable long-term period in this pipeline",
        dfdt_mhz_ms=-3.0,
        dfdt_frequency_mhz=600.0,
        dfdt_status="rough representative value",
        host_summary="active repeater with strong polarization/RM literature",
        notes="Useful natural-comparator source for RM and polarization variability.",
        dfdt_reference="xu_2022_frb20201124a_magnetized_site",
        host_reference="xu_2022_frb20201124a_magnetized_site",
    ),
    SourceAssumption(
        name="FRB 20190417A",
        aliases=("FRB20190417A",),
        redshift=None,
        period_days=None,
        window_days=None,
        period_status="sparse repeater in CHIME Catalog 1",
        dfdt_mhz_ms=-1.5,
        dfdt_frequency_mhz=600.0,
        dfdt_status="rough representative value",
        host_summary="limited public constraints in this pipeline",
        notes="Sensitivity example only.",
        dfdt_reference="chime_2021_catalog1",
        host_reference="chime_2021_catalog1",
    ),
)


def sources_with_periods(include_candidates: bool = True) -> list[SourceAssumption]:
    sources = [source for source in PERIODIC_SOURCES if source.period_days is not None]
    if include_candidates:
        return sources
    return [source for source in sources if "possible" not in source.period_status.lower()]


def sources_with_dfdt() -> list[SourceAssumption]:
    return [source for source in PERIODIC_SOURCES if source.dfdt_mhz_ms is not None]


def all_sources() -> tuple[SourceAssumption, ...]:
    return PERIODIC_SOURCES + CONTROL_SOURCES
