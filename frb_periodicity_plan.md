# FRB Periodicity Investigation Plan

This file preserves the project intent while updating the scientific standard
for publication-quality work.

## Objective

Build a reproducible pipeline that tests whether periodic repeating FRBs show
geometric or kinematic regularities that can be compared against a directed-beam
launch-window model and against natural FRB models.

The pipeline must be able to return negative, ambiguous, or positive results.
It must not be written as an advocacy document.

## Model Classes

1. **Broad Keplerian consistency**
   - Test whether observed periods fall within plausible orbital-period ranges.
   - Current status: too broad to be discriminating.

2. **Passive orbital-aberration directed-beam model**
   - Test whether `df/dt` is coupled to the macroscopic activity period through
     orbital aberration.
   - Prediction: `|df/dt| proportional to P^(-4/3)` at fixed observing
     frequency and aperture.
   - Current status: fails for FRB 20180916B versus FRB 20121102A under the
     adopted representative drift values.

3. **Active-tracking model**
   - Test whether `df/dt` can be mapped to an active beam sweep decoupled from
     the macroscopic period.
   - Current status: numerically plausible velocities under assumptions, but
     not yet discriminating.
   - The velocity scale is proportional to the adopted distance; 550 AU is a
     fiducial normalization, not a derived extragalactic lens geometry.

4. **Natural comparators**
   - Precession, rotation, binary modulation, magnetospheric emission,
     plasma/radius-to-frequency mapping, scattering, scintillation, and local
     magneto-ionic environments.

## Required Data For New Sources

- source name and aliases
- redshift and host environment, if known
- activity period and window, with publication source and confidence
- burst-level `df/dt` with uncertainty
- observing frequency/band
- DM correction method
- scattering/scintillation context
- RM and PA correction status
- whether the source is robust periodic, candidate periodic, or non-periodic

## Falsification Conditions

The passive orbital-aberration model is weakened or falsified if:

- `df/dt` does not follow `P^(-4/3)` under fixed aperture assumptions
- required apertures vary by orders of magnitude without an independent reason
- observed drift is better explained by known natural drift laws

The active-tracking model is weakened or falsified if:

- inferred transverse speeds fall outside a pre-declared plausible range
- frequency scaling differs from the declared beam-sweep law
- burst-to-burst drift distributions cannot be reproduced
- propagation-corrected sub-burst morphology matches natural models without
  residual geometric structure

Population-level claims require more than the current sample. With fewer than
five robust periodic repeaters, the pipeline may report descriptive statistics
only.

## Propagation Controls

All source-intrinsic claims require propagation-aware treatment:

- frequency drift must be measured after DM correction
- PA claims require RM correction
- sub-burst interpretation requires scattering/scintillation checks
- activity-window chromaticity must be handled explicitly

## Publication Standard

Use careful claim language:

- "is consistent with"
- "fails under these assumptions"
- "requires additional data"
- "not currently discriminating"

Avoid:

- "proves"
- "kills"
- "checkmate"
- "consensus collapsed"

The contribution of this repository is the transparent test framework, including
the negative result for the passive model and the explicit open tests for any
surviving active-tracking hypothesis.
