# Scientific Methodology

Documentation license: CC BY 4.0 -- see LICENSE for details.

The repository now separates four model classes:

1. **Broad Keplerian consistency**
   - Tests whether observed periods fall inside broad orbital-period bounds.
   - Expected outcome: non-discriminating unless the bounds are narrowed.

2. **Passive orbital-aberration directed-beam model**
   - Assumes fixed stellar-sized aperture and passive orbital aberration.
   - Predicts `|df/dt| proportional to P^(-4/3)` at fixed observing frequency.
   - Current status: fails for FRB 20180916B versus FRB 20121102A under the
     adopted representative drift values.

3. **Active-tracking beam model**
   - Treats sub-burst drift as an active angular sweep decoupled from the
     macroscopic activity period.
   - Current status: inferred transverse speeds are within plausible kinematic
     limits under the adopted assumptions, but the model is underconstrained.
   - The reported transverse velocity scales linearly with the adopted
     distance; 550 AU is a fiducial normalization, not a derived extragalactic
     lens geometry.
   - Required falsification conditions: pre-declared velocity prior,
     frequency-scaling prediction, burst-to-burst drift distribution, and cases
     that would be rejected.

4. **Natural comparator models**
   - Magnetospheric/RVM behavior, precession, binary modulation, local
     magneto-ionic environments, scattering, scintillation, and selection
     effects.
   - These must be addressed stage by stage.

## Minimum Evidence Standard

For any new source, the pipeline should record:

- source name and aliases
- redshift/host environment, if known
- period and activity-window provenance
- whether periodicity is robust or candidate-level
- burst-level `df/dt`, observing frequency, uncertainty, and dedispersion method
- scattering/scintillation context
- RM and PA correction status

## Claim Language

Allowed:

- "is consistent with"
- "fails under these assumptions"
- "is not currently discriminating"
- "requires burst-level data"
- "defines a future falsification test"

Avoid:

- "proves"
- "kills"
- "checkmate"
- "natural consensus has collapsed"
- "perfectly predicts"
