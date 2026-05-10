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
|df/dt| proportional to D Omega
Omega = a_orb / c
a_orb proportional to M^(1/3) P^(-4/3)
```

At fixed aperture and observing frequency, this gives:

```text
|df/dt| proportional to P^(-4/3)
```

## Result

Using representative values:

| Source | Period | Observed df/dt | Predicted df/dt |
| --- | ---: | ---: | ---: |
| FRB 20180916B | 16.35 d | -2.0 MHz/ms | -2.08 MHz/ms |
| FRB 20121102A | 157.0 d | -3.9 MHz/ms | -0.10 MHz/ms |

The longer-period source has a larger representative drift magnitude, while the
passive model predicts a much smaller one.

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
- Normalize or model observing-frequency dependence.
- Document DM correction method.
- Compare against natural sub-burst drift laws.
