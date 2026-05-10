"""Stage 1 -- data acquisition and catalog validation.

Inputs:
    Local CHIME/FRB catalog CSV files, primarily ``chimefrbcat1_data.csv``.
    With ``--download``, the script also attempts to fetch public CHIME/FRB
    catalog CSV endpoints.

Outputs:
    Prints schema-validation status. If ``--download`` is used, only validated
    CHIME-like CSV downloads replace local files.

Pipeline role:
    This is the ingest gate. Later stages assume catalog files have the required
    CHIME columns and are not HTML error pages or partial downloads. Code license: MIT -- see LICENSE for details.
"""

from pathlib import Path
import argparse

import pandas as pd
import requests

from frb.catalog import CatalogValidationError, REQUIRED_CHIME_COLUMNS, load_chime_catalog


# URLs verified 2026-05-10 against the official CHIME/FRB Public Database app
# bundle at www.chime-frb.ca/catalog and www.chime-frb.ca/catalog2.
DOWNLOADS = {
    "chimefrbcat1.csv": "https://storage.googleapis.com/chimefrb-dev.appspot.com/catalog1/chimefrbcat1.csv",
    "chimefrbcat2.csv": "https://storage.googleapis.com/chimefrb-dev.appspot.com/catalog2/chimefrbcat2.csv",
}


def download_and_validate(url: str, output_path: str) -> bool:
    """Download a catalog and keep it only if it validates as a CHIME-like CSV."""
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    # Write to a temporary file first so a bad download cannot overwrite a
    # previously validated catalog.
    path = Path(output_path)
    temp_path = path.with_suffix(path.suffix + ".download")
    temp_path.write_bytes(response.content)
    try:
        load_chime_catalog(temp_path)
    except (CatalogValidationError, pd.errors.ParserError) as exc:
        temp_path.unlink(missing_ok=True)
        print(f"Rejected {output_path}: {exc}")
        return False

    temp_path.replace(path)
    print(f"Validated {output_path}")
    return True


def validate_existing_catalog(path: str = "chimefrbcat1_data.csv") -> None:
    df = load_chime_catalog(path)
    print(f"{path}: {len(df)} rows, required columns present: {sorted(REQUIRED_CHIME_COLUMNS)}")


def download_chime_catalogs() -> None:
    for filename, url in DOWNLOADS.items():
        print(f"Downloading {filename}...")
        try:
            download_and_validate(url, filename)
        except Exception as exc:
            print(f"Download failed for {filename}: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and optionally download CHIME catalog files.")
    parser.add_argument("--download", action="store_true", help="Attempt network downloads after local validation.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    validate_existing_catalog()
    if args.download:
        download_chime_catalogs()
