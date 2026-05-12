# Stage 5 Report: Passive Directed-Beam Scaling Test

<!-- Numbers below correspond to v0.1.0; regenerate if frb/models.py or frb/data.py change. -->

## Hypothesis Tested

This stage tests only the passive orbital-aberration directed-beam model:

- fixed stellar-sized effective aperture
- circular Keplerian orbit
- comparable stellar masses
- sub-burst drift caused by passive orbital aberration

Under those assumptions:

```text
|df/dt| proportional to D f^2 Omega
Omega = a_orb / c
a_orb proportional to M^(1/3) P^(-4/3)
```

The model predicts both the period scaling and the `f^2` frequency scaling
simultaneously. The two anchor sources used here are reported at different
observing frequencies (FRB 20180916B in CHIME band; FRB 20121102A at Hessels
et al. 2019's L-band), so the test combines the period scaling and the
frequency scaling jointly through the predicted `df/dt` values.

## Result

Using representative values at their native observing frequencies:

| Source | Period | Observed df/dt | At freq | Predicted df/dt |
| --- | ---: | ---: | ---: | ---: |
| FRB 20180916B | 16.35 d | -2.0 MHz/ms | 600 MHz | -2.08 MHz/ms |
| FRB 20121102A | 157.0 d | -3.9 MHz/ms | 1400 MHz | -0.555 MHz/ms |

The predicted ratio (with the model's own `f^2 P^(-4/3)` dependence carrying
both the period and frequency scaling) is 0.267. The observed ratio is 1.95.
The discrepancy factor is approximately 7.3, above the data-derived failure
threshold of 5.

## Assessment

The passive orbital-aberration model fails this two-source comparison under its
own assumptions. This is a useful negative result.

This does not falsify every possible directed-beam model. In particular, it does
not test an active-tracking model where the sub-burst drift is decoupled from the
macroscopic activity period. That model requires separate falsification
conditions and is currently underconstrained.

## Controls Needed Before Publication

- Replace representative `df/dt` values with burst-level measurements and
  uncertainties.
- The `f^2` normalization implicit in the predicted ratio is the model's own
  prediction; verifying that the natural sub-burst slope-law literature
  supports `f^alpha` with alpha close to 2 over the relevant frequency range
  is a load-bearing literature check.
- Document DM correction method.
- Compare against natural sub-burst drift laws.
