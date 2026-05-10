# Stage 4 Findings: Passive Orbital-Aberration Aperture Test

## Question

If a sub-burst drift rate is caused by a beam sweeping across the observer due
to passive orbital aberration, what effective aperture is required?

The simplified model uses:

```text
theta ~ lambda / D
df/dt = -f^2 D Omega / c
Omega = a_orb / c
```

## Result

For FRB 20180916B, using:

- `P = 16.35 d`
- `df/dt = -2.0 MHz/ms`
- `f = 600 MHz`
- circular orbit around a 1 solar-mass star

the required aperture is approximately `1.34e6 km`, close to a solar diameter
of `1.392e6 km`.

## Interpretation

This is an interesting one-source numerical coincidence under the adopted
assumptions. It is not evidence by itself. The same model makes a population
scaling prediction:

```text
|df/dt| proportional to P^(-4/3)
```

That scaling is tested in Stage 5 and fails for the current two-source
comparison using FRB 20180916B and FRB 20121102A.

## Required Controls

- Use DM-corrected, preferably coherent/baseband drift measurements.
- Attach uncertainty and observing frequency to every `df/dt` value.
- Check scattering and scintillation before interpreting sub-burst structure as
  source geometry.
- Compare against natural sub-burst slope laws and plasma models.

