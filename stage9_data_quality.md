# Stage 9: Data Quality and Propagation Controls

This stage is a gatekeeper for all downstream physical interpretation. A burst
feature should not be attributed to source geometry, engineered tracking, or
natural magnetospheric physics until propagation and instrumental effects have
been controlled.

## Required Controls

1. **Dispersion correction before frequency-dependent analysis**
   - Sub-burst drift rates must come from DM-corrected data.
   - Coherent/baseband measurements are preferred.
   - If only intensity data are available, the drift value should be marked as
     low-confidence and excluded from model-selection claims.

2. **Scattering and scintillation checks**
   - Millisecond substructure can be distorted by scattering and scintillation.
   - Each source should carry a scattering time or scintillation bandwidth when
     available.
   - Features shorter than the relevant propagation timescale must be flagged.

3. **Primary beam and bandpass response**
   - CHIME beam response and observing band can imprint spectral structure.
   - Band-limited spectra are not automatically source-intrinsic.

4. **RM and PA correction**
   - Polarization-angle claims require RM correction.
   - RM variability itself should be treated as a diagnostic, not as a single
     static number.

## Literature Anchors

- CHIME/FRB baseband morphology work shows that high-time-resolution baseband
  data can reveal microstructure and scattering that lower-resolution pipelines
  miss: https://arxiv.org/abs/2408.13215
- Sub-burst drift laws exist in natural/phenomenological models and must be
  compared directly against any beam-sweep law: https://arxiv.org/abs/2308.11729
- Periodic repeater activity windows are chromatic, so achromaticity claims must
  be restricted to properly corrected source-frame burst morphology:
  https://arxiv.org/abs/2507.04609

## Current Status

The current repository uses representative literature values for several stages.
Those values are suitable for exploratory calculations, but not yet sufficient
for source-level inference. A publication-ready version must attach provenance,
uncertainty, observing frequency, dedispersion method, and scattering/RM context
to every burst-level measurement.
