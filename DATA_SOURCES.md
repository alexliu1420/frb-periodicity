# Data Sources

This repository uses public Fast Radio Burst catalog data released by the
CHIME/FRB Collaboration for independent scientific analysis.

## CHIME/FRB Catalog Attribution

Catalog data should be credited to the CHIME/FRB Collaboration. Users should
consult the original CHIME/FRB public database and associated data-release
papers for official metadata, usage guidance, and release terms.

Primary catalog portal:

- https://www.chime-frb.ca/catalog
- https://www.chime-frb.ca/catalog2

Public database:

- https://www.chime-frb.ca/

Direct public CSV downloads used by Stage 1:

- Catalog 1: https://storage.googleapis.com/chimefrb-dev.appspot.com/catalog1/chimefrbcat1.csv
- Catalog 2: https://storage.googleapis.com/chimefrb-dev.appspot.com/catalog2/chimefrbcat2.csv

These URLs were verified on 2026-05-10 against the official CHIME/FRB Public
Database web application at https://www.chime-frb.ca/catalog and
https://www.chime-frb.ca/catalog2.

## Catalog CSV Files

- `chimefrbcat1_data.csv` — committed local working CSV corresponding to
  CHIME/FRB Catalog 1 data used by the current reproducible pipeline stages.
- `chimefrbcat1.csv` — expected raw download filename for CHIME/FRB Catalog 1
  if generated locally by Stage 1; this file is not committed by default.
- `chimefrbcat2.csv` — expected raw download filename for CHIME/FRB Catalog 2
  if generated locally by Stage 1; this file is not committed by default.
- `catalog1.csv` and `repeaters.csv` — legacy/raw catalog filenames that may be
  produced during manual data acquisition or earlier exploratory work; these
  files are not committed by default.
- Related CSV files generated from CHIME/FRB data should be treated as derived
  catalog products and attributed to the CHIME/FRB Collaboration.

`stage2_results.csv` is a generated reference output from this repository's
curated source assumptions, not a CHIME/FRB catalog release.

## Use Statement

The catalog data are used here for independent scientific analysis of repeating
FRB periodicity and burst-structure hypotheses. The CSV data are not licensed
under the repository's MIT code license or CC BY 4.0 documentation license.
Users should refer to the CHIME/FRB Collaboration's original data release
terms.
