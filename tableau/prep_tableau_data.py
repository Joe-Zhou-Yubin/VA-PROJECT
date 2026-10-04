"""
Prepare clean, Tableau-ready CSVs from the raw GFW datasets.

Output goes to tableau/data/:
  1. fleet_by_flag_gear_month.csv    — monthly fishing hours by flag + gear (~50K rows)
  2. fleet_spatial_grid.csv          — 1° grid fishing effort by year (~200K rows)
  3. iuu_risk_cleaned.csv            — vessel-level IUU risk, all years, nulls handled (~1.8M rows)
  4. ais_disabling_cleaned.csv       — disabling events with derived fields (~55K rows)
  5. anchorages_cleaned.csv          — global ports/anchorages (~166K rows)

Run from the tableau/ folder:
    python prep_tableau_data.py
"""

import os
import glob
import pandas as pd
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(SCRIPT_DIR, "..", "datasets")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "data")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 1. Fleet by flag + gear + month
#    Aggregates ~60M rows down to ~50K for Tableau
# ============================================================
def build_fleet_summary():
    print("=== 1/5  Fleet by flag + gear + month ===")
    chunks = []
    for year in range(2020, 2025):
        year_dir = os.path.join(DATASETS_DIR, "fleet-monthly", str(year))
        files = sorted(glob.glob(os.path.join(year_dir, "*.csv")))
        for f in files:
            print(f"  Reading {os.path.basename(f)}...")
            df = pd.read_csv(f)
            agg = df.groupby(["year", "month", "flag", "geartype"]).agg(
                total_hours=("hours", "sum"),
                fishing_hours=("fishing_hours", "sum"),
                vessel_count=("mmsi_present", "sum"),
            ).reset_index()
            chunks.append(agg)

    result = pd.concat(chunks, ignore_index=True)
    result = result.groupby(["year", "month", "flag", "geartype"]).agg(
        total_hours=("total_hours", "sum"),
        fishing_hours=("fishing_hours", "sum"),
        vessel_count=("vessel_count", "sum"),
    ).reset_index()

    # Add a proper date column for Tableau time axis
    result["date"] = pd.to_datetime(
        result["year"].astype(str) + "-" + result["month"].astype(str).str.zfill(2) + "-01"
    )

    # Compute fishing ratio
    result["fishing_ratio"] = (
        result["fishing_hours"] / result["total_hours"].replace(0, np.nan)
    ).round(4)

    # Clean unknown flags
    result["flag_clean"] = result["flag"].fillna("UNKNOWN")

    # Gear type hierarchy for Tableau grouping
    gear_parent = {
        "tuna_purse_seines": "seiners",
        "other_purse_seines": "seiners",
        "purse_seines": "seiners",
        "other_seines": "seiners",
        "pots_and_traps": "fixed_gear",
        "set_longlines": "fixed_gear",
        "set_gillnets": "fixed_gear",
    }
    result["gear_category"] = result["geartype"].map(gear_parent).fillna(result["geartype"])

    out = os.path.join(OUTPUT_DIR, "fleet_by_flag_gear_month.csv")
    result.to_csv(out, index=False)
    print(f"  Saved {out} ({len(result):,} rows)\n")


# ============================================================
# 2. Spatial grid (1-degree)
#    For map visualizations in Tableau
# ============================================================
def build_spatial_grid():
    print("=== 2/5  Spatial grid (1 degree) ===")
    chunks = []
    for year in range(2020, 2025):
        year_dir = os.path.join(DATASETS_DIR, "fleet-monthly", str(year))
        files = sorted(glob.glob(os.path.join(year_dir, "*.csv")))
        for f in files:
            print(f"  Reading {os.path.basename(f)}...")
            df = pd.read_csv(f, usecols=[
                "year", "month", "cell_ll_lat", "cell_ll_lon",
                "flag", "geartype", "fishing_hours", "mmsi_present"
            ])
            # Bin to 1 degree
            df["lat"] = df["cell_ll_lat"].round(0).astype(int)
            df["lon"] = df["cell_ll_lon"].round(0).astype(int)

            agg = df.groupby(["year", "lat", "lon"]).agg(
                fishing_hours=("fishing_hours", "sum"),
                vessel_count=("mmsi_present", "sum"),
            ).reset_index()
            chunks.append(agg)

    result = pd.concat(chunks, ignore_index=True)
    result = result.groupby(["year", "lat", "lon"]).agg(
        fishing_hours=("fishing_hours", "sum"),
        vessel_count=("vessel_count", "sum"),
    ).reset_index()

    # Center of grid cell (Tableau plots points at center)
    result["lat_center"] = result["lat"] + 0.5
    result["lon_center"] = result["lon"] + 0.5

    # Drop zero-fishing cells
    result = result[result["fishing_hours"] > 0]

    # Log scale bucket for Tableau color
    result["log_fishing_hours"] = np.log10(result["fishing_hours"].clip(lower=1)).round(2)

    out = os.path.join(OUTPUT_DIR, "fleet_spatial_grid.csv")
    result.to_csv(out, index=False)
    print(f"  Saved {out} ({len(result):,} rows)\n")


# ============================================================
# 3. IUU Risk — cleaned
#    Fills nulls, adds composite risk score, cleans flags
# ============================================================
def build_iuu_risk():
    print("=== 3/5  IUU Risk cleaned ===")
    iuu_dir = os.path.join(DATASETS_DIR, "IUU-risk")
    files = sorted(glob.glob(os.path.join(iuu_dir, "*.csv")))

    dfs = []
    for f in files:
        print(f"  Reading {os.path.basename(f)}...")
        df = pd.read_csv(f, low_memory=False)
        dfs.append(df)

    result = pd.concat(dfs, ignore_index=True)

    # Fill numeric nulls with 0
    numeric_cols = [
        "hours", "positions", "active_hours", "active_positions",
        "previously_iuu_listed", "iuu_listed",
        "number_encounters", "number_forced_labor_encounters",
        "number_iuu_listed_encounters", "number_previously_iuu_listed_encounters",
        "dist_to_forced_labor", "dist_to_iuu",
        "average_voyage_duration_hours", "number_voyages",
        "gaps_count", "disabling_over_12_hours", "disabling_over_24_hours",
        "overlap_hours_multinames",
    ]
    for col in numeric_cols:
        if col in result.columns:
            result[col] = result[col].fillna(0)

    # Unified ship name
    result["ship_name"] = result["ais_shipname"].fillna(result["registry_shipname"]).fillna("")

    # Unified flag
    result["flag"] = result["best_flag"].fillna(result["ais_flag"]).fillna(result["registry_flag"]).fillna("UNKNOWN")

    # Composite risk score (transparent weighted sum)
    result["risk_score"] = (
        result["disabling_over_12_hours"] * 1
        + result["disabling_over_24_hours"] * 2
        + result["number_iuu_listed_encounters"] * 3
        + result["number_forced_labor_encounters"] * 3
        + result["number_previously_iuu_listed_encounters"] * 2
        + result["overlap_hours_multinames"].clip(upper=100) / 10
        + result["iuu_listed"] * 5
    ).round(2)

    # Risk tier for Tableau color
    result["risk_tier"] = pd.cut(
        result["risk_score"],
        bins=[-0.01, 0, 5, 15, float("inf")],
        labels=["None", "Low", "Medium", "High"],
    )

    # Has any suspicious behavior flag
    result["has_disabling"] = (result["disabling_over_12_hours"] > 0).astype(int)
    result["has_iuu_encounter"] = (result["number_iuu_listed_encounters"] > 0).astype(int)
    result["has_forced_labor_encounter"] = (result["number_forced_labor_encounters"] > 0).astype(int)
    result["has_spoofing"] = (result["overlap_hours_multinames"] > 0).astype(int)

    # Select clean columns for Tableau
    keep_cols = [
        "mmsi", "year", "vessel_class", "is_fishing",
        "ship_name", "flag",
        "ais_imo", "registry_imo",
        "ais_callsign", "registry_callsign",
        "top_port", "top_port_state",
        "hours", "active_hours",
        "previously_iuu_listed", "iuu_listed",
        "number_encounters",
        "number_iuu_listed_encounters",
        "number_previously_iuu_listed_encounters",
        "number_forced_labor_encounters",
        "dist_to_iuu", "dist_to_forced_labor",
        "average_voyage_duration_hours", "number_voyages",
        "gaps_count", "disabling_over_12_hours", "disabling_over_24_hours",
        "overlap_hours_multinames",
        "risk_score", "risk_tier",
        "has_disabling", "has_iuu_encounter",
        "has_forced_labor_encounter", "has_spoofing",
    ]
    result = result[[c for c in keep_cols if c in result.columns]]

    out = os.path.join(OUTPUT_DIR, "iuu_risk_cleaned.csv")
    result.to_csv(out, index=False)
    print(f"  Saved {out} ({len(result):,} rows)\n")


# ============================================================
# 4. AIS Disabling — cleaned with derived fields
# ============================================================
def build_disabling():
    print("=== 4/5  AIS Disabling cleaned ===")
    f = os.path.join(DATASETS_DIR, "ais_disabling_events.csv")
    df = pd.read_csv(f)

    # Parse timestamps
    df["gap_start_timestamp"] = pd.to_datetime(df["gap_start_timestamp"], utc=True)
    df["gap_end_timestamp"] = pd.to_datetime(df["gap_end_timestamp"], utc=True)

    # Derived fields
    df["gap_start_date"] = df["gap_start_timestamp"].dt.date
    df["gap_start_year"] = df["gap_start_timestamp"].dt.year
    df["gap_start_month"] = df["gap_start_timestamp"].dt.month

    # Distance from shore in km (more readable)
    df["gap_start_dist_shore_km"] = (df["gap_start_distance_from_shore_m"] / 1000).round(1)
    df["gap_end_dist_shore_km"] = (df["gap_end_distance_from_shore_m"] / 1000).round(1)

    # Displacement (how far the vessel moved while dark)
    df["displacement_lat"] = (df["gap_end_lat"] - df["gap_start_lat"]).round(4)
    df["displacement_lon"] = (df["gap_end_lon"] - df["gap_start_lon"]).round(4)

    # Gap severity bucket
    df["gap_severity"] = pd.cut(
        df["gap_hours"],
        bins=[0, 12, 24, 48, 72, float("inf")],
        labels=["12-24h", "24-48h", "48-72h", "72h+", "72h++"],
        right=True,
    )
    # Fix: the cut above doesn't handle the ranges cleanly, let me redo
    df["gap_severity"] = "12-24h"
    df.loc[df["gap_hours"] >= 24, "gap_severity"] = "24-48h"
    df.loc[df["gap_hours"] >= 48, "gap_severity"] = "48-72h"
    df.loc[df["gap_hours"] >= 72, "gap_severity"] = "72h+"

    # Clean flag
    df["flag"] = df["flag"].fillna("UNKNOWN")

    # Round coords for cleaner display
    df["gap_start_lat"] = df["gap_start_lat"].round(4)
    df["gap_start_lon"] = df["gap_start_lon"].round(4)
    df["gap_end_lat"] = df["gap_end_lat"].round(4)
    df["gap_end_lon"] = df["gap_end_lon"].round(4)
    df["gap_hours"] = df["gap_hours"].round(2)

    keep_cols = [
        "gap_id", "mmsi", "vessel_class", "flag",
        "vessel_length_m", "vessel_tonnage_gt",
        "gap_start_date", "gap_start_year", "gap_start_month",
        "gap_start_lat", "gap_start_lon", "gap_start_dist_shore_km",
        "gap_end_lat", "gap_end_lon", "gap_end_dist_shore_km",
        "gap_hours", "gap_severity",
        "displacement_lat", "displacement_lon",
    ]
    df = df[keep_cols]

    out = os.path.join(OUTPUT_DIR, "ais_disabling_cleaned.csv")
    df.to_csv(out, index=False)
    print(f"  Saved {out} ({len(df):,} rows)\n")


# ============================================================
# 5. Anchorages — cleaned
# ============================================================
def build_anchorages():
    print("=== 5/5  Anchorages cleaned ===")
    f = os.path.join(DATASETS_DIR, "named_anchorages_v2_pipe_v4_202607.csv")
    df = pd.read_csv(f)

    # Clean
    df["label"] = df["label"].fillna("Unknown")
    df["sublabel"] = df["sublabel"].fillna("")
    df["iso3"] = df["iso3"].fillna("UNKNOWN")
    df["distance_from_shore_km"] = (df["distance_from_shore_m"].fillna(0) / 1000).round(2)

    keep_cols = [
        "s2id", "lat", "lon", "label", "sublabel",
        "label_source", "iso3", "distance_from_shore_km",
        "at_dock",
    ]
    df = df[[c for c in keep_cols if c in df.columns]]

    out = os.path.join(OUTPUT_DIR, "anchorages_cleaned.csv")
    df.to_csv(out, index=False)
    print(f"  Saved {out} ({len(df):,} rows)\n")


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("Preparing Tableau-ready datasets...\n")

    # Small ones first (fast)
    build_iuu_risk()
    build_disabling()
    build_anchorages()

    # Large ones (fleet monthly — slower)
    build_fleet_summary()
    build_spatial_grid()

    print("=" * 50)
    print("All done! Files are in tableau/data/")
    print("Open them in Tableau via Data > Text File.")
