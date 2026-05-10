"""Primary literature anchors that the pipeline must engage.

Inputs:
    Manually curated primary-source references relevant to periodicity,
    polarization, RM, chromaticity, sub-burst drift, and directed-beam or
    related technosignature interpretations.

Outputs:
    Immutable reference records used by stages and documentation.

Pipeline role:
    Ensures the public repository acknowledges related work and natural
    comparators rather than presenting results in isolation. Code license: MIT -- see LICENSE for details.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Reference:
    key: str
    title: str
    url: str
    relevance: str
    tags: tuple[str, ...] = ()


def references_for_topic(tag: str) -> tuple[Reference, ...]:
    """Return references tagged for a scientific topic or stage."""
    return tuple(ref for ref in REFERENCES if tag in ref.tags)


REFERENCES: tuple[Reference, ...] = (
    Reference(
        key="lingam_loeb_2017_lightsails",
        title="Fast Radio Bursts from Extragalactic Light Sails",
        url="https://arxiv.org/abs/1701.01109",
        relevance="Prior directed-energy / light-sail interpretation; cite to clarify novelty.",
        tags=("technosignature", "directed_energy"),
    ),
    Reference(
        key="tendulkar_2017_frb121102_host",
        title="The Host Galaxy and Redshift of the Repeating Fast Radio Burst FRB 121102",
        url="https://arxiv.org/abs/1701.01100",
        relevance="Primary host/redshift reference for FRB 20121102A / FRB 121102.",
        tags=("host", "redshift", "frb20121102a"),
    ),
    Reference(
        key="hessels_2019_frb121102_drift",
        title="FRB 121102 Bursts Show Complex Time-Frequency Structure",
        url="https://arxiv.org/abs/1811.10748",
        relevance="Primary sub-burst drift and DM-structure reference for FRB 20121102A.",
        tags=("dfdt", "subburst", "frb20121102a", "stage5"),
    ),
    Reference(
        key="cordes_chatterjee_2019_frb_review",
        title="Fast Radio Bursts: An Extragalactic Enigma",
        url="https://arxiv.org/abs/1906.05878",
        relevance="Standard FRB review covering phenomenology, source models, host galaxies, and propagation.",
        tags=("review", "natural_comparator"),
    ),
    Reference(
        key="marcote_2020_frb20180916b_host",
        title="A repeating fast radio burst source localised to a nearby spiral galaxy",
        url="https://arxiv.org/abs/2001.02222",
        relevance="Primary localization, redshift, and host-environment reference for FRB 20180916B.",
        tags=("host", "redshift", "frb20180916b"),
    ),
    Reference(
        key="chime_2020_frb20180916b_periodicity",
        title="Periodic activity from a fast radio burst source",
        url="https://arxiv.org/abs/2001.10275",
        relevance="Discovery of the 16.35 day activity period and 5 day active window in FRB 20180916B.",
        tags=("periodicity", "frb20180916b", "stage3", "stage8"),
    ),
    Reference(
        key="ioka_zhang_2020_binary_comb",
        title="A Binary Comb Model for Periodic Fast Radio Bursts",
        url="https://arxiv.org/abs/2002.08297",
        relevance="Primary binary/natural periodicity comparator for FRB activity cycles.",
        tags=("natural_comparator", "binary", "periodicity"),
    ),
    Reference(
        key="lyutikov_barkov_giannios_2020_ob_binary",
        title="FRB-periodicity: mild pulsars in tight O/B-star binaries",
        url="https://arxiv.org/abs/2002.01920",
        relevance="Binary wind/absorption comparator for periodic activity windows.",
        tags=("natural_comparator", "binary", "periodicity"),
    ),
    Reference(
        key="rajwade_2020_frb121102_periodicity",
        title="Possible periodic activity in the repeating FRB 121102",
        url="https://arxiv.org/abs/2003.03596",
        relevance="Primary reported 157 day activity-cycle reference for FRB 20121102A / FRB 121102.",
        tags=("periodicity", "frb20121102a", "stage3", "stage8"),
    ),
    Reference(
        key="levin_2020_precessing_magnetar",
        title="Precessing flaring magnetar as a source of repeating FRB 180916.J0158+65",
        url="https://arxiv.org/abs/2002.04595",
        relevance="Primary precessing-magnetar comparator for FRB 20180916B periodic activity.",
        tags=("natural_comparator", "precession", "polarization", "periodicity"),
    ),
    Reference(
        key="beniamini_2020_ultralong_magnetars",
        title="Periodicity in recurrent fast radio bursts and the origin of ultra long period magnetars",
        url="https://arxiv.org/abs/2003.12509",
        relevance="Natural ultra-long-period magnetar comparator for periodic repeating FRBs.",
        tags=("natural_comparator", "magnetar", "periodicity"),
    ),
    Reference(
        key="lyutikov_popov_2020_magnetosphere",
        title="Fast Radio Bursts from reconnection events in magnetar magnetospheres",
        url="https://arxiv.org/abs/2005.05093",
        relevance="Magnetospheric natural-model counterpoint to engineered-beam interpretations.",
        tags=("natural_comparator", "magnetosphere"),
    ),
    Reference(
        key="pastor_marazuela_2021_low_frequency_chromatic",
        title="Chromatic periodic activity down to 120 MHz in a Fast Radio Burst",
        url="https://arxiv.org/abs/2012.08348",
        relevance="Original low-frequency/chromatic activity-window constraint for FRB 20180916B.",
        tags=("chromaticity", "frb20180916b", "stage15"),
    ),
    Reference(
        key="chime_2021_catalog1",
        title="The First CHIME/FRB Fast Radio Burst Catalog",
        url="https://arxiv.org/abs/2106.04352",
        relevance="Primary data-release paper for the Catalog 1 CSV used by the default pipeline.",
        tags=("catalog", "data", "stage3"),
    ),
    Reference(
        key="pleunis_2021_chime_morphology",
        title="Fast Radio Burst Morphology in the First CHIME/FRB Catalog",
        url="https://arxiv.org/abs/2106.04356",
        relevance="CHIME morphology and drift-law comparator for beam-sweep interpretations.",
        tags=("dfdt", "subburst", "morphology", "stage5", "stage9"),
    ),
    Reference(
        key="petroff_2022_frb_review",
        title="Fast radio bursts at the dawn of the 2020s",
        url="https://link.springer.com/article/10.1007/s00159-022-00139-w",
        relevance="Comprehensive FRB review for field context and model landscape.",
        tags=("review", "natural_comparator"),
    ),
    Reference(
        key="niu_2022_frb20190520b_host",
        title="A repeating fast radio burst associated with a persistent radio source",
        url="https://arxiv.org/abs/2110.07418",
        relevance="Primary localization, host, persistent-source, and redshift reference for FRB 20190520B.",
        tags=("host", "redshift", "frb20190520b", "control"),
    ),
    Reference(
        key="xu_2022_frb20201124a_magnetized_site",
        title="A fast radio burst source at a complex magnetised site in a barred galaxy",
        url="https://arxiv.org/abs/2111.11764",
        relevance="FAST burst and magnetized-environment reference for FRB 20201124A.",
        tags=("host", "dfdt", "rm", "frb20201124a", "control"),
    ),
    Reference(
        key="anna_thomas_2023_frb20190520b_rm",
        title="Magnetic field reversal in the turbulent environment around a repeating fast radio burst",
        url="https://arxiv.org/abs/2202.11112",
        relevance="RM and magneto-ionic environment reference for FRB 20190520B.",
        tags=("rm", "frb20190520b", "control"),
    ),
    Reference(
        key="frb20190520b_burst_comparison_2023",
        title="Comparison of Burst Properties between FRB 20190520B and FRB 20121102A",
        url="https://arxiv.org/abs/2305.02595",
        relevance="Burst-property context for FRB 20190520B used as a control-source sensitivity example.",
        tags=("dfdt", "subburst", "frb20190520b", "control"),
    ),
    Reference(
        key="frb20240209a_periodicity_2025",
        title="A Possible Four-Month Periodicity in the Activity of FRB 20240209A",
        url="https://arxiv.org/abs/2502.11215",
        relevance="Treat 126 day periodicity as candidate/possible, not a settled population point.",
        tags=("periodicity", "frb20240209a", "stage3", "stage8"),
    ),
    Reference(
        key="chime_frb_catalog2_2026",
        title="The Second CHIME/FRB Catalog of Fast Radio Bursts",
        url="https://arxiv.org/abs/2601.09399",
        relevance="Catalog 2 expands public CHIME data to 4539 unique FRB events and 83 repeater sources.",
        tags=("catalog", "data", "stage3"),
    ),
    Reference(
        key="chromatic_activity_windows_2026",
        title="Chromatic Activity Windows of Periodic FRB Repeaters",
        url="https://arxiv.org/abs/2507.04609",
        relevance="Activity windows are chromatic; achromatic claims must be restricted and tested after propagation correction.",
        tags=("chromaticity", "stage15"),
    ),
    Reference(
        key="pa_frb20180916b_2025",
        title="Polarization angle behavior of FRB 20180916B",
        url="https://arxiv.org/abs/2507.07651",
        relevance="Flat/limited short-timescale PA constrains precession but does not eliminate all natural rotational models.",
        tags=("polarization", "rvm", "frb20180916b", "stage11", "stage13"),
    ),
    Reference(
        key="rvm_repeaters_2025",
        title="Rotating-vector-model-like PA swings in repeating FRBs",
        url="https://arxiv.org/abs/2504.00391",
        relevance="RVM comparisons require fitted models and real PA data; flat PA is not a universal natural-model rejection.",
        tags=("polarization", "rvm", "stage11", "stage13"),
    ),
    Reference(
        key="rm_frb20180916b_2024",
        title="Time evolution of rotation measure in FRB 20180916B",
        url="https://arxiv.org/abs/2409.12584",
        relevance="RM is not simply stable at one value; there is stochastic and secular evolution.",
        tags=("rm", "frb20180916b", "stage16"),
    ),
    Reference(
        key="rm_frb20220529_2025",
        title="Possible periodic rotation-measure evolution in FRB 20220529",
        url="https://arxiv.org/abs/2505.10463",
        relevance="Binary/wind and magneto-ionic natural comparators remain active research programs.",
        tags=("rm", "binary", "stage16"),
    ),
    Reference(
        key="rm_flare_search_2026",
        title="Search for rotation-measure flares in repeating FRBs",
        url="https://arxiv.org/abs/2604.20814",
        relevance="RM variability is a diagnostic to model, not a one-source knockout argument.",
        tags=("rm", "stage16"),
    ),
    Reference(
        key="subburst_slope_law_2023",
        title="Sub-burst slope law across repeating FRBs",
        url="https://arxiv.org/abs/2308.11729",
        relevance="Natural/phenomenological models can also produce frequency-squared-like drift scaling.",
        tags=("dfdt", "subburst", "stage5", "stage9"),
    ),
    Reference(
        key="chime_baseband_morphology_2024",
        title="CHIME/FRB baseband morphology catalog",
        url="https://arxiv.org/abs/2408.13215",
        relevance="Use baseband/coherent data and scattering checks before interpreting substructure.",
        tags=("baseband", "subburst", "stage9"),
    ),
)
