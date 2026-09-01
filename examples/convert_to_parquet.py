"""
Convert CSV datasets to Parquet format for efficient querying.
Run this once before starting the Flask server.

Output:
  data/fleet_monthly_2020_2024.parquet  (~aggregated by month, flag, geartype)
  data/iuu_risk_all.parquet
  data/ais_disabling.parquet
  data/anchorages.parquet
"""

import os
import glob
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(BASE_DIR, "..", "datasets")
OUTPUT_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def convert_fleet_monthly():
    """
    Fleet-monthly: ~60 files x 1M rows = too large to load all at once.
    Strategy: read each file, aggregate to (year, month, flag, geartype) level,
    then combine. This shrinks 60M rows to ~100K summary rows.
    Also create a spatial version aggregated by (year, lat, lon) for the heatmap.
    """
    print("Converting fleet-monthly data...")

    # --- Aggregation 1: by year, month, flag, geartype (for bar/line charts) ---
    agg_list = []
    for year in range(2020, 2025):
        year_dir = os.path.join(DATASETS_DIR, "fleet-monthly", str(year))
        files = sorted(glob.glob(os.path.join(year_dir, "*.csv")))
        for f in files:
            print(f"  Reading {os.path.basename(f)}...")
            df = pd.read_csv(f)
            # Aggregate: sum hours/fishing_hours, sum mmsi_present by flag+geartype
            agg = df.groupby(["year", "month", "flag", "geartype"]).agg(
                hours=("hours", "sum"),
                fishing_hours=("fishing_hours", "sum"),
                mmsi_present=("mmsi_present", "sum"),
            ).reset_index()
            agg_list.append(agg)

    fleet_agg = pd.concat(agg_list, ignore_index=True)
    # Further aggregate in case of duplicate groupings across files
    fleet_agg = fleet_agg.groupby(["year", "month", "flag", "geartype"]).agg(
        hours=("hours", "sum"),
        fishing_hours=("fishing_hours", "sum"),
        mmsi_present=("mmsi_present", "sum"),
    ).reset_index()

    out_path = os.path.join(OUTPUT_DIR, "fleet_monthly_agg.parquet")
    fleet_agg.to_parquet(out_path, index=False)
    print(f"  Saved {out_path} ({len(fleet_agg)} rows)")

    # --- Aggregation 2: spatial heatmap (by year, lat_bin, lon_bin) ---
    # Use 1-degree bins for manageable heatmap data
    print("  Building spatial aggregation (1-degree grid)...")
    spatial_list = []
    for year in range(2020, 2025):
        year_dir = os.path.join(DATASETS_DIR, "fleet-monthly", str(year))
        files = sorted(glob.glob(os.path.join(year_dir, "*.csv")))
        for f in files:
            df = pd.read_csv(f, usecols=["cell_ll_lat", "cell_ll_lon", "fishing_hours"])
            # Bin to 1 degree
            df["lat"] = (df["cell_ll_lat"]).round(0).astype(int)
            df["lon"] = (df["cell_ll_lon"]).round(0).astype(int)
            agg = df.groupby(["lat", "lon"]).agg(
                fishing_hours=("fishing_hours", "sum")
            ).reset_index()
            agg["year"] = year
            spatial_list.append(agg)

    spatial_agg = pd.concat(spatial_list, ignore_index=True)
    spatial_agg = spatial_agg.groupby(["year", "lat", "lon"]).agg(
        fishing_hours=("fishing_hours", "sum")
    ).reset_index()

    out_path = os.path.join(OUTPUT_DIR, "fleet_spatial_1deg.parquet")
    spatial_agg.to_parquet(out_path, index=False)
    print(f"  Saved {out_path} ({len(spatial_agg)} rows)")

    # --- Aggregation 3: spatial detail (by year, lat, lon, flag, geartype) for click-to-inspect ---
    print("  Building spatial detail aggregation (1-degree, with flag+gear)...")
    detail_list = []
    for year in range(2020, 2025):
        year_dir = os.path.join(DATASETS_DIR, "fleet-monthly", str(year))
        files = sorted(glob.glob(os.path.join(year_dir, "*.csv")))
        for f in files:
            df = pd.read_csv(f, usecols=["cell_ll_lat", "cell_ll_lon", "flag", "geartype", "fishing_hours", "mmsi_present"])
            df["lat"] = (df["cell_ll_lat"]).round(0).astype(int)
            df["lon"] = (df["cell_ll_lon"]).round(0).astype(int)
            agg = df.groupby(["lat", "lon", "flag", "geartype"]).agg(
                fishing_hours=("fishing_hours", "sum"),
                mmsi_present=("mmsi_present", "sum"),
            ).reset_index()
            agg["year"] = year
            detail_list.append(agg)

    detail_agg = pd.concat(detail_list, ignore_index=True)
    detail_agg = detail_agg.groupby(["year", "lat", "lon", "flag", "geartype"]).agg(
        fishing_hours=("fishing_hours", "sum"),
        mmsi_present=("mmsi_present", "sum"),
    ).reset_index()

    out_path = os.path.join(OUTPUT_DIR, "fleet_spatial_detail.parquet")
    detail_agg.to_parquet(out_path, index=False)
    print(f"  Saved {out_path} ({len(detail_agg)} rows)")


def convert_iuu_risk():
    """Combine all IUU annual files into one Parquet."""
    print("Converting IUU risk data...")
    iuu_dir = os.path.join(DATASETS_DIR, "IUU-risk")
    files = sorted(glob.glob(os.path.join(iuu_dir, "*.csv")))

    dfs = []
    for f in files:
        print(f"  Reading {os.path.basename(f)}...")
        df = pd.read_csv(f, low_memory=False)
        dfs.append(df)

    iuu_all = pd.concat(dfs, ignore_index=True)
    out_path = os.path.join(OUTPUT_DIR, "iuu_risk_all.parquet")
    iuu_all.to_parquet(out_path, index=False)
    print(f"  Saved {out_path} ({len(iuu_all)} rows)")


def convert_ais_disabling():
    """Convert AIS disabling CSV to Parquet."""
    print("Converting AIS disabling data...")
    f = os.path.join(DATASETS_DIR, "ais_disabling_events.csv")
    df = pd.read_csv(f)
    out_path = os.path.join(OUTPUT_DIR, "ais_disabling.parquet")
    df.to_parquet(out_path, index=False)
    print(f"  Saved {out_path} ({len(df)} rows)")


def convert_anchorages():
    """Convert anchorages CSV to Parquet."""
    print("Converting anchorages data...")
    f = os.path.join(DATASETS_DIR, "named_anchorages_v2_pipe_v4_202607.csv")
    df = pd.read_csv(f)
    out_path = os.path.join(OUTPUT_DIR, "anchorages.parquet")
    df.to_parquet(out_path, index=False)
    print(f"  Saved {out_path} ({len(df)} rows)")


if __name__ == "__main__":
    convert_iuu_risk()
    convert_ais_disabling()
    convert_anchorages()
    convert_fleet_monthly()  # This one takes longest
    print("\nAll conversions complete!")
