import io
import textwrap
from pathlib import Path

import pandas as pd

from src.data_preprocessing import (
    load_gps,
    load_physical_capabilities,
    load_recovery_status,
)


def write(tmp_path: Path, rel: str, content: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


def test_load_gps_parses_dates_and_filters_season(tmp_path: Path, monkeypatch):
    csv_path = write(
        tmp_path,
        "data/players_data/marc_cucurella/CFC GPS Data.csv",
        """
        date,season,md_plus_code,distance,hr_zone_1_hms,hr_zone_2_hms,hr_zone_3_hms,hr_zone_4_hms,hr_zone_5_hms
        01/08/2023,2023/2024,0,5000,00:10:00,00:05:00,00:02:00,00:01:00,00:00:30
        01/08/2024,2024/2025,1,0,00:00:00,00:00:00,00:00:00,00:00:00,00:00:00
        """,
    )

    df, df_active = load_gps(str(csv_path), season="2023/2024")

    assert len(df) == 1  # filtered to season
    assert pd.api.types.is_datetime64_any_dtype(df["date"])  # parsed
    # derived columns
    assert {"is_match_day", "week_num", "day_name"}.issubset(df.columns)
    # hr zone seconds computed
    for z in range(1, 6):
        assert f"hr_zone_{z}_hms_seconds" in df.columns
    # active filter based on distance > 0
    assert len(df_active) == 1


def test_load_physical_capabilities_filters_and_sorts(tmp_path: Path):
    csv_path = write(
        tmp_path,
        "data/players_data/marc_cucurella/CFC Physical Capability Data.csv",
        """
        testDate,benchmarkPct,movement
        01/07/2023,50,Jump
        30/06/2024,60,Sprint
        01/07/2024,70,Agility
        """,
    )

    df_2324 = load_physical_capabilities(str(csv_path), season="2023/2024")
    assert (df_2324["testDate"].min().strftime("%d/%m/%Y")) == "01/07/2023"
    assert (df_2324["testDate"].max().strftime("%d/%m/%Y")) == "30/06/2024"
    assert df_2324.iloc[0]["benchmarkPct"] == 50

    df_2425 = load_physical_capabilities(str(csv_path), season="2024/2025")
    assert df_2425["testDate"].min().strftime("%d/%m/%Y") == "01/07/2024"


def test_load_recovery_status_filters_season_and_derives_columns(tmp_path: Path):
    csv_path = write(
        tmp_path,
        "data/players_data/marc_cucurella/CFC Recovery status Data.csv",
        """
        sessionDate,seasonName,metric,value
        01/08/2023,2023/2024,sleep_baseline_score,7
        02/08/2023,2023/2024,sleep_baseline_completeness,1
        03/08/2024,2024/2025,nutrition_baseline_composite,0.8
        """,
    )

    df = load_recovery_status(str(csv_path), season="2023/2024")

    assert len(df) == 2  # filtered to season
    assert pd.api.types.is_datetime64_any_dtype(df["sessionDate"])  # parsed
    # derived columns present
    for col in ["week", "month", "metric_type", "base_metric"]:
        assert col in df.columns