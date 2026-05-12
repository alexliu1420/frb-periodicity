# Changelog

## 0.2.0 - 2026-05-11

- Added the v0.2.0 manuscript at `paper/frb_periodicity_investigation.md`,
  derived from the v0.1.0 pipeline. The manuscript presents a directed-beam
  framework for periodic repeating FRBs, reports a two-source falsification
  of its passive (aberration-locked) sub-case under representative literature
  drift values for FRB 20180916B and FRB 20121102A, and reports the
  active-tracking variant as a non-discriminating kinematic-consistency
  result. A publication-ready PDF (`paper/frb_periodicity_investigation.pdf`)
  is built reproducibly from the markdown by `paper/build_paper.py`
  (pandoc + xelatex), and Figures 1 and 2 are regenerable from pipeline
  anchor data via `paper/figures/generate_figures.py`.
- Corrected the FRB 20121102A representative-drift observing-frequency tag
  in `frb/data.py`: `dfdt_frequency_mhz` was 600.0; updated to 1400.0 to
  match Hessels et al. 2019's reported L-band (1.1–1.7 GHz) context for
  the −3.9 MHz/ms value. v0.1.0's tag of 600 MHz was inconsistent with the
  source paper.
- Updated the Stage 5 cross-source scaling test to reflect the corrected
  frequency. Predicted cross-source ratio is now 0.267 (was 0.049 under
  the v0.1.0 tag); discrepancy factor is 7.3× (was 39.8×). The passive
  sub-case still fails the pre-declared 5× threshold — the change is a
  numerical refinement under correct f² normalization, not a change in
  the falsification conclusion.
- Re-pinned `tests/test_stage5.py` assertions to the corrected predicted
  ratio (0.267) and the new discrepancy bounds (5–10×). All tests pass.
- Refreshed `stage5_falsification_report.md` table and prose to match the
  corrected pipeline output, with explicit native-frequency columns.
- Clarified the `dfdt_status` provenance strings in `frb/data.py` for
  both anchor sources to mark the representative values as band-summary
  anchors rather than specific per-burst quotes.

## 0.1.0 - 2026-05-10

- Added a 16-stage reproducible FRB periodicity pipeline with shared constants,
  catalog validation, source assumptions, literature anchors, and tests.
- Added CHIME/FRB Catalog 2 download and Stage 3 summarization support.
- Added Stage 5 regression coverage for the passive orbital-aberration
  `P^(-4/3)` scaling result.
- Added structured provenance fields for period, drift, redshift, and host
  assumptions.
- Added runtime Stage 9 propagation/data-quality controls.
- Added publication-readiness files: `LICENSE`, `DATA_SOURCES.md`,
  `CITATION.md`, `CONTRIBUTING.md`, and dependency lockfile guidance.
- Initial public release under MIT (code) and CC BY 4.0 (documentation).
