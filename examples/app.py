"""
Flask backend serving aggregated data from Parquet files.

Run:
    python app.py

Then open http://localhost:5000 in your browser.
"""

import os
import pandas as pd
from flask import Flask, jsonify, send_from_directory, request

app = Flask(__name__, static_folder="static")

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# ---------- Lazy-loaded data caches ----------
_cache = {}


def load_parquet(name):
    """Load a parquet file and cache it in memory."""
    if name not in _cache:
        path = os.path.join(DATA_DIR, name)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"{name} not found. Run convert_to_parquet.py first."
            )
        _cache[name] = pd.read_parquet(path)
    return _cache[name]


# ---------- Static file serving ----------

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)


# ---------- API: Fleet Monthly ----------

@app.route("/api/fleet/by_flag")
def fleet_by_flag():
    """Top N fishing nations by total fishing hours, optionally filtered by year."""
    df = load_parquet("fleet_monthly_agg.parquet")
    year = request.args.get("year", type=int)
    n = request.args.get("n", default=20, type=int)

    if year:
        df = df[df["year"] == year]

    top = (
        df.groupby("flag")
        .agg(fishing_hours=("fishing_hours", "sum"))
        .reset_index()
        .sort_values("fishing_hours", ascending=False)
        .head(n)
    )
    return jsonify(top.to_dict(orient="records"))


@app.route("/api/fleet/by_gear")
def fleet_by_gear():
    """Fishing hours by gear type, optionally filtered by year."""
    df = load_parquet("fleet_monthly_agg.parquet")
    year = request.args.get("year", type=int)

    if year:
        df = df[df["year"] == year]

    agg = (
        df.groupby("geartype")
        .agg(fishing_hours=("fishing_hours", "sum"))
        .reset_index()
        .sort_values("fishing_hours", ascending=False)
    )
    return jsonify(agg.to_dict(orient="records"))


@app.route("/api/fleet/trend")
def fleet_trend():
    """Monthly fishing hours trend, optionally filtered by flag."""
    df = load_parquet("fleet_monthly_agg.parquet")
    flag = request.args.get("flag")

    if flag:
        df = df[df["flag"] == flag.upper()]

    trend = (
        df.groupby(["year", "month"])
        .agg(fishing_hours=("fishing_hours", "sum"))
        .reset_index()
        .sort_values(["year", "month"])
    )
    trend["date"] = trend.apply(
        lambda r: f"{int(r['year'])}-{int(r['month']):02d}", axis=1
    )
    return jsonify(trend[["date", "fishing_hours"]].to_dict(orient="records"))


@app.route("/api/fleet/heatmap")
def fleet_heatmap():
    """Spatial fishing effort for heatmap. Returns lat, lon, fishing_hours."""
    df = load_parquet("fleet_spatial_1deg.parquet")
    year = request.args.get("year", default=2024, type=int)
    resolution = request.args.get("res", default="1deg", type=str)

    if resolution == "tenth" and "fleet_spatial_tenth.parquet" in os.listdir(DATA_DIR):
        df = load_parquet("fleet_spatial_tenth.parquet")

    filtered = df[df["year"] == year]
    # Only return cells with meaningful fishing
    min_hours = 10 if resolution == "1deg" else 1
    filtered = filtered[filtered["fishing_hours"] > min_hours]

    result = filtered[["lat", "lon", "fishing_hours"]].to_dict(orient="records")
    return jsonify(result)


@app.route("/api/fleet/cell_detail")
def fleet_cell_detail():
    """Get breakdown of a specific grid cell (by flag + gear) for click-to-inspect."""
    df = load_parquet("fleet_monthly_agg.parquet")
    year = request.args.get("year", default=2024, type=int)
    # For cell detail we use the spatial-with-detail parquet if available
    detail_path = os.path.join(DATA_DIR, "fleet_spatial_detail.parquet")
    if os.path.exists(detail_path):
        detail_df = load_parquet("fleet_spatial_detail.parquet")
        lat = request.args.get("lat", type=float)
        lon = request.args.get("lon", type=float)
        if lat is None or lon is None:
            return jsonify({"error": "lat and lon required"}), 400

        # Find matching cell (1-degree bin)
        cell = detail_df[
            (detail_df["year"] == year) &
            (detail_df["lat"] == int(round(lat))) &
            (detail_df["lon"] == int(round(lon)))
        ]
        result = cell.to_dict(orient="records")
        return jsonify(result)

    # Fallback: return top flags/gears for the whole year
    return jsonify({"error": "Detail data not available. Re-run convert_to_parquet.py"}), 404


# ---------- API: IUU Risk ----------

@app.route("/api/iuu/top_risk")
def iuu_top_risk():
    """Top N vessels by composite risk score for a given year."""
    df = load_parquet("iuu_risk_all.parquet")
    year = request.args.get("year", default=2024, type=int)
    n = request.args.get("n", default=50, type=int)

    filtered = df[df["year"] == year].copy()

    # Simple composite risk: sum of binary risk indicators
    filtered["risk_score"] = (
        filtered["disabling_over_12_hours"].fillna(0)
        + filtered["disabling_over_24_hours"].fillna(0) * 2
        + filtered["number_iuu_listed_encounters"].fillna(0) * 3
        + filtered["number_forced_labor_encounters"].fillna(0) * 3
        + filtered["number_previously_iuu_listed_encounters"].fillna(0) * 2
        + filtered["overlap_hours_multinames"].fillna(0).clip(upper=100) / 10
        + filtered["iuu_listed"].fillna(0) * 5
    )

    top = filtered.nlargest(n, "risk_score")
    cols = [
        "mmsi", "vessel_class", "best_flag", "ais_shipname",
        "number_encounters", "number_iuu_listed_encounters",
        "number_forced_labor_encounters", "disabling_over_12_hours",
        "disabling_over_24_hours", "overlap_hours_multinames",
        "average_voyage_duration_hours", "number_voyages",
        "dist_to_iuu", "dist_to_forced_labor", "risk_score",
    ]
    available_cols = [c for c in cols if c in top.columns]
    return jsonify(top[available_cols].fillna(0).to_dict(orient="records"))


@app.route("/api/iuu/by_flag")
def iuu_by_flag():
    """Aggregate IUU risk indicators by flag state."""
    df = load_parquet("iuu_risk_all.parquet")
    year = request.args.get("year", default=2024, type=int)
    n = request.args.get("n", default=20, type=int)

    filtered = df[df["year"] == year]

    agg = (
        filtered.groupby("best_flag")
        .agg(
            vessel_count=("mmsi", "count"),
            total_disabling_12h=("disabling_over_12_hours", "sum"),
            total_disabling_24h=("disabling_over_24_hours", "sum"),
            total_iuu_encounters=("number_iuu_listed_encounters", "sum"),
            total_forced_labor_encounters=("number_forced_labor_encounters", "sum"),
            avg_voyage_duration=("average_voyage_duration_hours", "mean"),
        )
        .reset_index()
        .sort_values("total_disabling_12h", ascending=False)
        .head(n)
    )
    return jsonify(agg.fillna(0).to_dict(orient="records"))


@app.route("/api/iuu/profile/<int:mmsi>")
def iuu_vessel_profile(mmsi):
    """Get risk profile for a specific vessel across all years."""
    df = load_parquet("iuu_risk_all.parquet")
    vessel = df[df["mmsi"] == mmsi].sort_values("year")
    if vessel.empty:
        return jsonify({"error": "Vessel not found"}), 404
    return jsonify(vessel.fillna(0).to_dict(orient="records"))


# ---------- API: AIS Disabling ----------

@app.route("/api/disabling/events")
def disabling_events():
    """AIS disabling events, optionally filtered by flag or min gap hours."""
    df = load_parquet("ais_disabling.parquet")
    flag = request.args.get("flag")
    min_hours = request.args.get("min_hours", default=12, type=float)
    limit = request.args.get("limit", default=5000, type=int)

    filtered = df[df["gap_hours"] >= min_hours]
    if flag:
        filtered = filtered[filtered["flag"] == flag.upper()]

    # Return a sample if too many
    if len(filtered) > limit:
        filtered = filtered.sample(n=limit, random_state=42)

    cols = [
        "gap_id", "mmsi", "vessel_class", "flag",
        "gap_start_lat", "gap_start_lon",
        "gap_end_lat", "gap_end_lon",
        "gap_hours", "gap_start_distance_from_shore_m",
    ]
    return jsonify(filtered[cols].to_dict(orient="records"))


@app.route("/api/disabling/by_flag")
def disabling_by_flag():
    """Count disabling events by flag state."""
    df = load_parquet("ais_disabling.parquet")
    n = request.args.get("n", default=20, type=int)

    agg = (
        df.groupby("flag")
        .agg(
            event_count=("gap_id", "count"),
            avg_gap_hours=("gap_hours", "mean"),
            total_gap_hours=("gap_hours", "sum"),
        )
        .reset_index()
        .sort_values("event_count", ascending=False)
        .head(n)
    )
    return jsonify(agg.to_dict(orient="records"))


# ---------- API: Anchorages ----------

@app.route("/api/anchorages")
def anchorages():
    """Get anchorages, optionally filtered by country."""
    df = load_parquet("anchorages.parquet")
    iso3 = request.args.get("iso3")
    limit = request.args.get("limit", default=1000, type=int)

    if iso3:
        df = df[df["iso3"] == iso3.upper()]

    if len(df) > limit:
        df = df.sample(n=limit, random_state=42)

    cols = ["lat", "lon", "label", "sublabel", "iso3", "at_dock"]
    available_cols = [c for c in cols if c in df.columns]
    return jsonify(df[available_cols].to_dict(orient="records"))


if __name__ == "__main__":
    print("Starting GFW Visualization Server...")
    print("Open http://localhost:5000 in your browser")
    print("Make sure you've run convert_to_parquet.py first!")
    app.run(debug=True, port=5000)


# ---------- API: Country Choropleth ----------

@app.route("/api/fleet/choropleth")
def fleet_choropleth():
    """Total fishing hours per country for choropleth. Filter by year."""
    df = load_parquet("fleet_monthly_agg.parquet")
    year = request.args.get("year", type=int)
    metric = request.args.get("metric", default="fishing_hours")

    if year:
        df = df[df["year"] == year]

    # Aggregate by flag; exclude UNKNOWN
    df = df[~df["flag"].str.startswith("UNKNOWN", na=False)]

    agg = (
        df.groupby("flag")
        .agg(
            fishing_hours=("fishing_hours", "sum"),
            vessel_hours=("hours", "sum"),
            vessel_count=("mmsi_present", "sum"),
        )
        .reset_index()
    )
    return jsonify(agg.to_dict(orient="records"))


@app.route("/api/disabling/choropleth")
def disabling_choropleth():
    """Disabling events per country for choropleth."""
    df = load_parquet("ais_disabling.parquet")

    agg = (
        df.dropna(subset=["flag"])
        .groupby("flag")
        .agg(
            event_count=("gap_id", "count"),
            total_gap_hours=("gap_hours", "sum"),
            avg_gap_hours=("gap_hours", "mean"),
        )
        .reset_index()
    )
    return jsonify(agg.to_dict(orient="records"))


@app.route("/api/iuu/choropleth")
def iuu_choropleth():
    """IUU risk aggregates per country for choropleth."""
    df = load_parquet("iuu_risk_all.parquet")
    year = request.args.get("year", default=2024, type=int)

    filtered = df[df["year"] == year].copy()
    filtered = filtered[~filtered["best_flag"].astype(str).str.startswith("UNKNOWN")]
    filtered = filtered.dropna(subset=["best_flag"])

    agg = (
        filtered.groupby("best_flag")
        .agg(
            vessel_count=("mmsi", "count"),
            total_disabling=("disabling_over_12_hours", "sum"),
            total_iuu_encounters=("number_iuu_listed_encounters", "sum"),
            total_forced_labor_encounters=("number_forced_labor_encounters", "sum"),
        )
        .reset_index()
        .rename(columns={"best_flag": "flag"})
    )
    return jsonify(agg.fillna(0).to_dict(orient="records"))


# ---------- API: Vessel Search & Profile ----------

@app.route("/api/iuu/search")
def iuu_search():
    """Search vessels by MMSI (exact) or shipname (partial)."""
    df = load_parquet("iuu_risk_all.parquet")
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])

    # Try MMSI (numeric)
    matches = pd.DataFrame()
    if q.isdigit():
        matches = df[df["mmsi"] == int(q)]

    # If no MMSI match, search by shipname
    if matches.empty:
        q_upper = q.upper()
        name_match = df[
            df["ais_shipname"].astype(str).str.upper().str.contains(q_upper, na=False)
            | df["registry_shipname"].astype(str).str.upper().str.contains(q_upper, na=False)
        ]
        matches = name_match

    if matches.empty:
        return jsonify([])

    # Get unique vessels, take most recent year
    unique = (
        matches.sort_values("year", ascending=False)
        .drop_duplicates(subset="mmsi")
        .head(20)
    )
    cols = ["mmsi", "vessel_class", "best_flag", "ais_shipname",
            "registry_shipname", "top_port", "top_port_state", "year"]
    return jsonify(unique[cols].fillna("").to_dict(orient="records"))


@app.route("/api/iuu/vessel/<int:mmsi>")
def iuu_vessel_full(mmsi):
    """Full vessel history across all years."""
    df = load_parquet("iuu_risk_all.parquet")
    vessel = df[df["mmsi"] == mmsi].sort_values("year")
    if vessel.empty:
        return jsonify({"error": "Vessel not found"}), 404
    return jsonify(vessel.fillna(0).to_dict(orient="records"))


# ---------- API: Sunburst (Hierarchical) ----------

@app.route("/api/fleet/sunburst")
def fleet_sunburst():
    """Hierarchical data: flag -> gear -> fishing_hours."""
    df = load_parquet("fleet_monthly_agg.parquet")
    year = request.args.get("year", default=2024, type=int)
    min_hours = request.args.get("min_hours", default=5000, type=float)
    top_n_flags = request.args.get("top_n", default=20, type=int)

    filtered = df[df["year"] == year]
    filtered = filtered[~filtered["flag"].str.startswith("UNKNOWN", na=False)]

    # Top N flags by fishing hours
    top_flags = (
        filtered.groupby("flag")["fishing_hours"].sum()
        .nlargest(top_n_flags)
        .index.tolist()
    )
    filtered = filtered[filtered["flag"].isin(top_flags)]

    # Aggregate by flag + gear
    agg = (
        filtered.groupby(["flag", "geartype"])
        .agg(fishing_hours=("fishing_hours", "sum"))
        .reset_index()
    )
    agg = agg[agg["fishing_hours"] >= min_hours]

    # Build hierarchical structure: root -> flag -> gear
    root = {"name": "Global", "children": []}
    for flag in top_flags:
        flag_data = agg[agg["flag"] == flag]
        if flag_data.empty:
            continue
        flag_node = {
            "name": flag,
            "children": [
                {"name": row["geartype"], "value": float(row["fishing_hours"])}
                for _, row in flag_data.iterrows()
            ],
        }
        root["children"].append(flag_node)
    return jsonify(root)


# ---------- API: Bar Chart Race (Monthly Ranking) ----------

@app.route("/api/fleet/race")
def fleet_race():
    """Monthly cumulative fishing hours by flag for bar chart race."""
    df = load_parquet("fleet_monthly_agg.parquet")
    top_n = request.args.get("top_n", default=15, type=int)

    df = df[~df["flag"].str.startswith("UNKNOWN", na=False)]

    # Find top N flags overall
    top_flags = (
        df.groupby("flag")["fishing_hours"].sum()
        .nlargest(top_n).index.tolist()
    )
    filtered = df[df["flag"].isin(top_flags)]

    # Aggregate to year-month by flag
    monthly = (
        filtered.groupby(["year", "month", "flag"])
        .agg(fishing_hours=("fishing_hours", "sum"))
        .reset_index()
    )
    monthly["date"] = monthly.apply(
        lambda r: f"{int(r['year'])}-{int(r['month']):02d}", axis=1
    )

    # Pivot: rows = months, cols = flags
    dates = sorted(monthly["date"].unique())
    result = []
    for d in dates:
        month_data = monthly[monthly["date"] == d]
        entry = {"date": d, "flags": []}
        for flag in top_flags:
            row = month_data[month_data["flag"] == flag]
            hours = float(row["fishing_hours"].iloc[0]) if not row.empty else 0.0
            entry["flags"].append({"flag": flag, "hours": hours})
        entry["flags"].sort(key=lambda x: x["hours"], reverse=True)
        result.append(entry)

    return jsonify(result)


# ---------- API: Port Flow (Sankey) ----------

@app.route("/api/iuu/port_flow")
def iuu_port_flow():
    """Flag state -> top port state flow for Sankey diagram."""
    df = load_parquet("iuu_risk_all.parquet")
    year = request.args.get("year", default=2024, type=int)
    n = request.args.get("n", default=20, type=int)

    filtered = df[df["year"] == year]
    filtered = filtered.dropna(subset=["best_flag", "top_port_state"])
    filtered = filtered[
        (~filtered["best_flag"].astype(str).str.startswith("UNKNOWN"))
        & (filtered["top_port_state"].astype(str).str.len() > 0)
    ]

    # Count vessels flowing from flag -> port state
    flow = (
        filtered.groupby(["best_flag", "top_port_state"])
        .size()
        .reset_index(name="vessel_count")
        .sort_values("vessel_count", ascending=False)
        .head(n * 3)  # allow more edges since many countries
    )

    return jsonify(flow.rename(
        columns={"best_flag": "source", "top_port_state": "target"}
    ).to_dict(orient="records"))


# ---------- API: Fleet Composition Comparison ----------

@app.route("/api/fleet/composition")
def fleet_composition():
    """Gear composition for top N flags. Optional flags param comma-separated."""
    df = load_parquet("fleet_monthly_agg.parquet")
    year = request.args.get("year", default=2024, type=int)
    top_n = request.args.get("top_n", default=15, type=int)
    flags_param = request.args.get("flags")

    filtered = df[df["year"] == year]
    filtered = filtered[~filtered["flag"].str.startswith("UNKNOWN", na=False)]

    if flags_param:
        selected_flags = [f.strip().upper() for f in flags_param.split(",")]
    else:
        selected_flags = (
            filtered.groupby("flag")["fishing_hours"].sum()
            .nlargest(top_n).index.tolist()
        )

    filtered = filtered[filtered["flag"].isin(selected_flags)]

    agg = (
        filtered.groupby(["flag", "geartype"])
        .agg(fishing_hours=("fishing_hours", "sum"))
        .reset_index()
    )
    return jsonify(agg.to_dict(orient="records"))
