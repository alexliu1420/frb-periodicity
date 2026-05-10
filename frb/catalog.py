"""Catalog loading and validation helpers.

Inputs:
    CHIME/FRB-style CSV files or pandas DataFrames loaded from those files.

Outputs:
    Validated DataFrames and repeater-count summaries with CHIME missing-value
    sentinels excluded.

Pipeline role:
    Keeps data ingestion reproducible and prevents malformed downloads from
    entering the scientific stages. Code license: MIT -- see LICENSE for details.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

MISSING_SENTINEL = "-9999"

REQUIRED_CHIME_COLUMNS = {
    "tns_name",
    "repeater_name",
    "ra",
    "dec",
    "bonsai_dm",
    "mjd_400",
    "mjd_inf",
    "high_freq",
    "low_freq",
}


class CatalogValidationError(ValueError):
    """Raised when a downloaded file is not the expected CHIME catalog CSV."""


def load_chime_catalog(path: str | Path) -> pd.DataFrame:
    """Load and validate a CHIME catalog CSV."""
    path = Path(path)
    df = pd.read_csv(path, dtype={"repeater_name": "string"})
    # Schema validation is intentionally minimal but catches HTML downloads and
    # unrelated CSV files before later stages interpret them as catalog data.
    missing = REQUIRED_CHIME_COLUMNS.difference(df.columns)
    if missing:
        raise CatalogValidationError(
            f"{path} is not a valid CHIME catalog CSV; missing columns: {sorted(missing)}"
        )
    return df


def named_repeater_mask(df: pd.DataFrame) -> pd.Series:
    """Return a mask for rows with real repeater names, excluding sentinels."""
    if "repeater_name" not in df.columns:
        raise CatalogValidationError("Catalog is missing repeater_name.")
    as_text = df["repeater_name"].astype("string").str.strip()
    return as_text.notna() & ~as_text.isin({MISSING_SENTINEL, "-9999.0", ""})


def repeater_counts(df: pd.DataFrame, min_bursts: int = 2) -> pd.Series:
    """Return source counts for named repeaters, excluding CHIME missing sentinels."""
    # The public catalog uses -9999 for absent repeater names; counting that
    # sentinel would turn all non-repeaters into one artificial "source."
    named = df[named_repeater_mask(df)]
    counts = named["repeater_name"].value_counts()
    return counts[counts >= min_bursts]


def named_repeater_source_count(df: pd.DataFrame) -> int:
    """Return the number of distinct non-sentinel repeater labels."""
    named = df[named_repeater_mask(df)]
    return int(named["repeater_name"].nunique())


def event_identifier_column(df: pd.DataFrame) -> str:
    """Return the preferred column for counting unique FRB events."""
    if "event_id" in df.columns:
        return "event_id"
    return "tns_name"


def unique_event_count(df: pd.DataFrame) -> int:
    """Return unique event count, avoiding sub-burst/component double counting."""
    column = event_identifier_column(df)
    return int(df[column].astype("string").nunique())


def named_repeater_event_count(df: pd.DataFrame) -> int:
    """Return unique events associated with named repeaters."""
    column = event_identifier_column(df)
    named = df[named_repeater_mask(df)]
    return int(named[column].astype("string").nunique())


def count_events_for_aliases(df: pd.DataFrame, aliases: set[str]) -> int:
    """Count unique catalog events whose TNS or repeater name matches aliases."""
    normalized = {alias.replace(" ", "") for alias in aliases}
    tns = df["tns_name"].astype("string").str.replace(" ", "", regex=False)
    repeaters = df["repeater_name"].astype("string").str.replace(" ", "", regex=False)
    mask = tns.isin(normalized) | repeaters.isin(normalized)
    column = event_identifier_column(df)
    return int(df.loc[mask, column].astype("string").nunique())
