"""
Pre-join datasets externally so Tableau gets flat files with zero join config.

Input:  tableau/data/ (the 5 cleaned CSVs from prep_tableau_data.py)
Output: tableau/data/joined/ (3 ready-to-use flat files)

  1. country_summary.csv     — flag × year: fleet effort + IUU risk aggregates
  2. disabling_enriched.csv  — each disabling event enriched with vessel risk info
  3. fleet_with_risk.csv     — flag × year × gear: fleet effort + country-level risk

Run:
    python join_tables.py
"""

import os
import pandas as pd
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
OUT_DIR = os.path.join(DATA_DIR, "joined")

os.makedirs(OUT_DIR, exist_ok=True)


def build_country_summary():
    """
    One row per flag × year.
    Combines fleet fishing effort totals with IUU risk aggregates for that country.
    """
    print("=== 1/3  Country Summary (flag × year) ===")

    # Fleet side: aggregate across gear types
    fleet = pd.read_csv(os.path.join(DATA_DIR, "fleet_by_flag_gear_month.csv"))
    fleet_agg = (
        fleet.groupby(["year", "flag"])
        .agg(
            total_hours=("total_hours", "sum"),
            fishing_hours=("fishing_hours", "sum"),
            vessel_visits=("vessel_count", "sum"),
            gear_types_active=("geartype", "nunique"),
        )
        .reset_index()
    )
    fleet_agg["fishing_ratio"] = (
        fleet_agg["fishing_hours"] / fleet_agg["total_hours"].replace(0, np.nan)
    ).round(4)

    # IUU side: aggregate per flag × year
    iuu = pd.read_csv(
        os.path.join(DATA_DIR, "iuu_risk_cleaned.csv"),
        usecols=[
            "mmsi", "year", "flag", "risk_score", "risk_tier",
            "disabling_over_12_hours", "disabling_over_24_hours",
            "number_encounters", "number_iuu_listed_encounters",
            "number_forced_labor_encounters", "overlap_hours_multinames",
            "has_disabling", "has_iuu_encounter", "has_forced_labor_encounter", "has_spoofing",
        ],
        low_memory=False,
    )
    iuu_agg = (
        iuu.groupby(["year", "flag"])
        .agg(
            iuu_vessel_count=("mmsi", "nunique"),
            avg_risk_score=("risk_score", "mean"),
            max_risk_score=("risk_score", "max"),
            total_disabling_12h=("disabling_over_12_hours", "sum"),
            total_disabling_24h=("disabling_over_24_hours", "sum"),
            total_encounters=("number_encounters", "sum"),
            total_iuu_encounters=("number_iuu_listed_encounters", "sum"),
            total_forced_labor_encounters=("number_forced_labor_encounters", "sum"),
            total_spoofing_hours=("overlap_hours_multinames", "sum"),
            vessels_with_disabling=("has_disabling", "sum"),
            vessels_with_iuu_encounter=("has_iuu_encounter", "sum"),
            vessels_with_forced_labor=("has_forced_labor_encounter", "sum"),
            vessels_with_spoofing=("has_spoofing", "sum"),
            high_risk_vessels=("risk_score", lambda x: (x > 15).sum()),
            medium_risk_vessels=("risk_score", lambda x: ((x > 5) & (x <= 15)).sum()),
        )
        .reset_index()
    )
    iuu_agg["avg_risk_score"] = iuu_agg["avg_risk_score"].round(3)
    iuu_agg["pct_vessels_with_disabling"] = (
        iuu_agg["vessels_with_disabling"] / iuu_agg["iuu_vessel_count"].replace(0, np.nan) * 100
    ).round(2)

    # Merge
    merged = fleet_agg.merge(iuu_agg, on=["year", "flag"], how="outer")
    merged = merged.fillna(0)

    # Sort
    merged = merged.sort_values(["year", "fishing_hours"], ascending=[True, False])

    out = os.path.join(OUT_DIR, "country_summary.csv")
    merged.to_csv(out, index=False)
    print(f"  Saved {out} ({len(merged):,} rows)\n")


def build_disabling_enriched():
    """
    Each disabling event joined with the vessel's IUU risk profile for that year.
    If no IUU match (different year range), uses the closest available year.
    """
    print("=== 2/3  Disabling Enriched ===")

    disabling = pd.read_csv(os.path.join(DATA_DIR, "ais_disabling_cleaned.csv"))

    # Load just the columns we need from IUU for the join
    iuu = pd.read_csv(
        os.path.join(DATA_DIR, "iuu_risk_cleaned.csv"),
        usecols=[
            "mmsi", "year", "vessel_class", "flag", "ship_name",
            "risk_score", "risk_tier",
            "number_encounters", "number_iuu_listed_encounters",
            "number_forced_labor_encounters",
            "iuu_listed", "previously_iuu_listed",
            "top_port", "top_port_state",
        ],
        low_memory=False,
    )

    # Disabling data is 2017-2019, IUU data covers 2012-2025
    # Try exact year match first
    disabling["mmsi"] = disabling["mmsi"].astype(int)
    iuu["mmsi"] = iuu["mmsi"].astype(int)

    merged = disabling.merge(
        iuu,
        left_on=["mmsi", "gap_start_year"],
        right_on=["mmsi", "year"],
        how="left",
        suffixes=("", "_iuu"),
    )

    # For unmatched rows, try nearest year from IUU
    unmatched_mask = merged["risk_score"].isna()
    if unmatched_mask.sum() > 0:
        unmatched_mmsis = merged.loc[unmatched_mask, "mmsi"].unique()
        # Get the latest IUU record for each unmatched mmsi
        iuu_latest = (
            iuu[iuu["mmsi"].isin(unmatched_mmsis)]
            .sort_values("year", ascending=False)
            .drop_duplicates(subset="mmsi")
        )
        # Fill in the blanks
        for col in iuu_latest.columns:
            if col in ["mmsi", "year"]:
                continue
            if col in merged.columns and col + "_iuu" not in merged.columns:
                continue
            target_col = col if col not in merged.columns else col + "_iuu"
            if target_col in merged.columns:
                fill = iuu_latest.set_index("mmsi")[col]
                merged.loc[unmatched_mask, target_col] = (
                    merged.loc[unmatched_mask, "mmsi"].map(fill)
                )

    # Clean up: use disabling's own flag/vessel_class if IUU didn't match
    if "flag_iuu" in merged.columns:
        merged["flag"] = merged["flag"].fillna(merged["flag_iuu"])
        merged.drop(columns=["flag_iuu"], inplace=True, errors="ignore")
    if "vessel_class_iuu" in merged.columns:
        merged.drop(columns=["vessel_class_iuu"], inplace=True, errors="ignore")

    merged["risk_score"] = merged["risk_score"].fillna(0)
    merged["risk_tier"] = merged["risk_tier"].fillna("Unknown")
    merged["ship_name"] = merged["ship_name"].fillna("")

    # Drop the redundant year column from IUU
    merged.drop(columns=["year"], inplace=True, errors="ignore")

    out = os.path.join(OUT_DIR, "disabling_enriched.csv")
    merged.to_csv(out, index=False)
    print(f"  Saved {out} ({len(merged):,} rows)\n")


def build_fleet_with_risk():
    """
    Fleet monthly data (flag × year × gear × month) enriched with
    country-level IUU risk summary. Lets you color fleet bars by risk
    without needing a separate data source.
    """
    print("=== 3/3  Fleet with Country Risk ===")

    fleet = pd.read_csv(os.path.join(DATA_DIR, "fleet_by_flag_gear_month.csv"))

    # Build country-year risk summary from IUU
    iuu = pd.read_csv(
        os.path.join(DATA_DIR, "iuu_risk_cleaned.csv"),
        usecols=[
            "mmsi", "year", "flag", "risk_score",
            "disabling_over_12_hours", "number_iuu_listed_encounters",
            "number_forced_labor_encounters", "has_disabling",
        ],
        low_memory=False,
    )
    country_risk = (
        iuu.groupby(["year", "flag"])
        .agg(
            country_avg_risk=("risk_score", "mean"),
            country_max_risk=("risk_score", "max"),
            country_total_disabling=("disabling_over_12_hours", "sum"),
            country_total_iuu_encounters=("number_iuu_listed_encounters", "sum"),
            country_total_fl_encounters=("number_forced_labor_encounters", "sum"),
            country_pct_vessels_disabling=("has_disabling", "mean"),
        )
        .reset_index()
    )
    country_risk["country_avg_risk"] = country_risk["country_avg_risk"].round(3)
    country_risk["country_pct_vessels_disabling"] = (
        country_risk["country_pct_vessels_disabling"] * 100
    ).round(2)

    # Merge onto fleet
    merged = fleet.merge(country_risk, on=["year", "flag"], how="left")
    merged = merged.fillna(0)

    out = os.path.join(OUT_DIR, "fleet_with_risk.csv")
    merged.to_csv(out, index=False)
    print(f"  Saved {out} ({len(merged):,} rows)\n")


if __name__ == "__main__":
    print("Building pre-joined Tableau tables...\n")
    build_country_summary()
    build_disabling_enriched()
    build_fleet_with_risk()
    print("=" * 50)
    print("Done! Files in tableau/data/joined/")
    print("Load these directly in Tableau — no joins needed.")
