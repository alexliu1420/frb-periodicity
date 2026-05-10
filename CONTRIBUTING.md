# Contributing

This repository is intended to remain reproducible and scientifically cautious
as new FRB data become public. New sources should be added through the curated
metadata layer first, then promoted into stage-level claims only after the
quality controls below are satisfied.

## Adding a New FRB

Add a `SourceAssumption` entry in `frb/data.py`:

```python
SourceAssumption(
    name="FRB YYYYMMDDX",
    aliases=("FRBYYYYMMDDX",),
    redshift=None,
    period_days=None,
    window_days=None,
    period_status="candidate, robust, or no confirmed period",
    dfdt_mhz_ms=None,
    dfdt_frequency_mhz=None,
    dfdt_status="burst-level, representative, rough, or unavailable",
    host_summary="short host/environment summary",
    notes="limits on how this source may be interpreted",
    period_reference=None,
    dfdt_reference=None,
    redshift_reference=None,
    host_reference=None,
)
```

Use reference keys from `frb/literature.py`. Add a new `Reference(...)` there
when the period, drift, redshift, or host value comes from a paper that is not
already listed.

## Minimum Evidence Checklist

- Period or activity window has a primary reference and a stated confidence
  level.
- `df/dt` values include observing frequency, uncertainty, and whether they are
  burst-level measurements or representative literature values.
- DM correction is documented before frequency-dependent analysis.
- Scattering and scintillation timescales are checked before assigning
  sub-burst structure to beam sweep.
- PA data are RM-corrected before RVM or flat-PA interpretation.
- Population-level claims remain disabled until the robust periodic sample is
  large enough for inference.

## Tests to Update

When the curated drift-bearing set changes, update
`tests/test_catalog_data.py::test_sources_with_dfdt_returns_curated_pair`.

When a new headline scaling comparison is introduced, add or update a Stage 5
regression test in `tests/test_stage5.py`.

Run:

```bash
python -m unittest discover
python run_all_stages.py
```

To use CHIME/FRB Catalog 2 locally after Stage 1 download:

```bash
python run_all_stages.py --catalog chimefrbcat2.csv
```
