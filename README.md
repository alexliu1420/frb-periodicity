# FRB Periodicity Investigation: A Falsifiable Directed-Beam Test Pipeline

Alex Liu, 2026

This repository tests whether periodic repeating fast radio bursts contain
geometric or kinematic regularities that can be compared against a directed-beam
launch-window model. The goal is not to assume an engineered origin. The goal is
to build a reproducible, falsifiable pipeline that remains consistent with
existing FRB literature and stays testable against future data.

The present contribution is a transparent computational test framework and a
limited negative result for one passive model. It is not a claim that FRBs are
engineered, that natural models are ruled out, or that the negative result for
the passive model generalizes beyond the two anchor sources currently tested.

## Current Scientific Status

The current result is negative:

- A passive orbital-aberration directed-beam model predicts
  `|df/dt| proportional to P^(-4/3)` at fixed observing frequency and aperture.
- FRB 20180916B gives an interesting one-source aperture coincidence under this
  model.
- FRB 20121102A departs from the same scaling under the adopted representative
  drift values.

Therefore, the passive orbital-aberration model fails the current two-source
comparison under the stated assumptions.

This conclusion is conditional. It uses representative literature drift values
for the two current Stage 5 anchor sources, not a uniform burst-level reanalysis
of all bursts. Publication-grade inference requires the propagation and
measurement controls listed below.

The active-tracking model remains a hypothesis:

- Mapping observed drift rates to beam sweep rates gives transverse speeds that
  are within plausible kinematic limits under the adopted aperture and fiducial
  550 AU distance assumptions.
- This is not yet a discriminating test, because the model currently maps nearly
  any drift rate to some velocity.
- It needs pre-declared velocity priors, burst-level uncertainty, frequency
  scaling, and rejection conditions.

Population-level claims are not allowed at the current sample size. The pipeline
tracks two robust periodic repeaters plus one candidate/possible source,
FRB 20240209A. That is too small for population inference.

## Role of CHIME/FRB Catalog 2

CHIME/FRB Catalog 2 is used here to update catalog-scale repeater context and
to exercise the pipeline on a larger public data release. It does not by itself
add a new Stage 5 anchor source.

Stage 5 requires a curated tuple for each source: activity period, drift rate,
observing frequency, and provenance. Catalog 2 provides burst detections and
metadata, but periodicity claims and burst-level drift measurements require
separate analysis. Future periodic repeaters can be added through `frb/data.py`
and the provenance workflow in `CONTRIBUTING.md` once suitable measurements are
published or independently derived.

## License

Code: MIT License.
Documentation and written materials: CC BY 4.0.
Data: CHIME/FRB Collaboration -- see DATA_SOURCES.md for attribution.

See LICENSE for full terms.

## Repository Structure

For the headline result, read [stage5_falsification_report.md](stage5_falsification_report.md).
For the propagation/data-quality gate, read [stage9_data_quality.md](stage9_data_quality.md).
For the assumptions required to add future sources, read [CONTRIBUTING.md](CONTRIBUTING.md).

- `frb/`: shared constants, source assumptions, catalog validation, literature
  anchors, and physical models.
- `stage1_data_acquisition.py`: validates local CHIME catalog data and rejects
  bad downloads.
- `stage2_orbital_mechanics.py`: broad Keplerian period bounds.
- `stage3_full_catalog_pipeline.py`: catalog/repeater counting and sample-size
  gate.
- `stage4_subburst_analysis.py`: passive beam-sweep aperture calculation.
- `stage5_scaling_test.py`: `P^(-4/3)` falsification test.
- `stage6_active_tracking.py`: active-tracking kinematic consistency check.
- `stage7_energy_budget.py`: beaming-sensitive energy calculation.
- `stage8_duty_cycle.py`: duty-cycle visibility interpretation.
- `stage9_data_quality.py` / `stage9_data_quality.md`: propagation and
  measurement controls.
- `stage10_population_assessment.py` through `stage16_rm_stability.py`:
  population, host, polarization, spectral, and RM comparators.
- `docs/`: methodology and literature review.
- `tests/`: unit tests for the shared equations.
- `run_all_stages.py`: runs the non-download stages.

## Reproducibility

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Reproducing the published numerical anchors: use `python -m pip install -r requirements-lock.txt` to install the exact dependency versions used to compute the Stage 5 falsification ratios and test anchors. `requirements.txt` carries looser floors for general development.

Run equation tests:

```bash
python -m unittest discover
```

Run the non-download pipeline stages:

```bash
python run_all_stages.py
```

Stage 1 performs network downloads and should be run separately:

```bash
python stage1_data_acquisition.py --download
```

To summarize CHIME/FRB Catalog 2 after download:

```bash
python stage3_full_catalog_pipeline.py chimefrbcat2.csv
```

## Required Scientific Controls

Any publication-grade extension must record, for each burst-level measurement:

- DM correction method
- observing frequency and bandwidth
- `df/dt` uncertainty
- scattering/scintillation context
- RM correction for polarization angles
- source and activity-window provenance

Sub-burst structure cannot be attributed to beam sweep until propagation effects
and natural drift laws have been compared. Achromaticity claims apply only after
DM correction and propagation modeling.

## External Literature

The repo explicitly engages prior work on directed-beam interpretations of
FRBs, periodic repeaters, chromatic activity windows, sub-burst drift laws,
polarization/RVM behavior, and RM variability. See
[docs/literature_review.md](docs/literature_review.md).

## Claim Discipline

This repository should use publication-safe language:

- "consistent with"
- "fails under these assumptions"
- "not currently discriminating"
- "candidate-level"
- "requires burst-level data"

It should not use advocacy language such as "proves," "kills," "checkmate," or
"consensus collapsed." The useful contribution is a transparent test framework,
including negative results.
