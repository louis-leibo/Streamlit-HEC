from typing import Tuple

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def load_gps(
    file_path: str = "data/players_data/marc_cucurella/CFC GPS Data.csv",
    encoding: str = "ISO-8859-1",
    season: str = "2023/2024",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load GPS CSV, parse dates, filter by season, derive HR zone seconds and helpers.

    Returns the full dataframe and an "active" subset where distance > 0.

    Args:
        file_path: Path to the GPS data CSV file.
        encoding: File encoding used to read the CSV.
        season: Season label to filter the dataset (e.g., "2023/2024").

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: (full_df, active_df)
    """
    df = pd.read_csv(file_path, encoding=encoding)

    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df = df[df["season"] == season]
    # Define heart rate zone columns
    hr_columns = [
        "hr_zone_1_hms",
        "hr_zone_2_hms",
        "hr_zone_3_hms",
        "hr_zone_4_hms",
        "hr_zone_5_hms",
    ]

    for col in hr_columns:
        df[f"{col}_seconds"] = df[col].apply(
            lambda x: (
                sum(
                    int(part) * (60**i)
                    for i, part in enumerate(reversed(str(x).split(":")))
                )
                if pd.notna(x) and x != "00:00:00"
                else 0
            )
        )

    # Add useful derived columns for analysis
    df["is_match_day"] = df["md_plus_code"] == 0
    df["week_num"] = ((df["date"] - df["date"].min()).dt.days // 7) + 1
    df["day_name"] = df["date"].dt.day_name()

    df_active = df[df["distance"] > 0].copy()

    return df, df_active


def load_physical_capabilities(
    file_path: str = "data/players_data/marc_cucurella/CFC Physical Capability Data.csv",
    season: str = "2023/2024",
) -> pd.DataFrame:
    """Load physical capabilities CSV, parse dates, coerce benchmarkPct, and filter by season.

    Args:
        file_path: Path to the physical capabilities CSV file.
        season: Season window used to filter testDate.

    Returns:
        DataFrame sorted by testDate within the selected season.
    """
    df = pd.read_csv(file_path)

    df["testDate"] = pd.to_datetime(df["testDate"], format="%d/%m/%Y")
    df["benchmarkPct"] = pd.to_numeric(df["benchmarkPct"], errors="coerce")

    if season == "2023/2024":
        df = df.loc[
            (df["testDate"] >= pd.to_datetime("01/07/2023", format="%d/%m/%Y"))
            & (df["testDate"] <= pd.to_datetime("30/06/2024", format="%d/%m/%Y"))
        ]
    elif season == "2024/2025":
        df = df.loc[
            df["testDate"] >= pd.to_datetime("01/07/2024", format="%d/%m/%Y")
        ]
    df = df.sort_values("testDate")

    return df


def load_recovery_status(
    file_path: str = "data/players_data/marc_cucurella/CFC Recovery status Data.csv",
    season: str = "2023/2024",
) -> pd.DataFrame:
    """Load recovery CSV, filter by season, parse dates, and derive helper columns.

    Adds ISO week, month name, metric_type classification, and a base_metric name.

    Args:
        file_path: Path to the recovery status CSV file.
        season: Season label to filter the dataset (e.g., "2023/2024").

    Returns:
        Preprocessed DataFrame sorted by sessionDate.
    """
    df = pd.read_csv(file_path)
    df = df[df["seasonName"] == season]

    # Convert date strings to datetime objects
    df["sessionDate"] = pd.to_datetime(df["sessionDate"], format="%d/%m/%Y")

    df = df.sort_values("sessionDate")

    df = df.dropna(subset=["value"])

    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Add temporal grouping columns for analysis
    df["week"] = df["sessionDate"].dt.isocalendar().week
    df["month"] = df["sessionDate"].dt.month_name()

    # Extract and categorize different metric types
    df["metric_type"] = df["metric"].apply(
        lambda x: (
            "completeness"
            if "completeness" in x
            else ("composite" if "composite" in x else "score")
        )
    )

    # Clean up metric names by removing type suffixes
    df["base_metric"] = df["metric"].apply(
        lambda x: x.replace("_baseline_completeness", "")
        .replace("_baseline_composite", "")
        .replace("_baseline_score", "")
    )

    return df


def load_priority(path: str, encoding: str = "ISO-8859-1") -> pd.DataFrame:
    """Load a CSV with the given encoding and return it as a DataFrame.

    Args:
        path: Filesystem path to the CSV file.
        encoding: Text encoding to use when reading the file.

    Returns:
        Raw DataFrame read from the CSV.
    """
    df = pd.read_csv(path, encoding=encoding)
    return df
