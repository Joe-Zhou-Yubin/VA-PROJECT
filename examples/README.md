# GFW Fishing Visualization Examples

Interactive visualizations of Global Fishing Watch data using Flask + Leaflet/D3/Chart.js.

## Setup

```bash
# 1. Install dependencies (if not already installed)
pip install -r requirements.txt

# 2. Convert CSVs to Parquet (run once, takes 5-10 minutes)
python convert_to_parquet.py

# 3. Start the Flask server
python app.py

# 4. Open http://localhost:5000 in your browser
```

## Architecture

```
examples/
├── app.py                  # Flask backend (API endpoints)
├── convert_to_parquet.py   # One-time CSV → Parquet conversion
├── requirements.txt
├── data/                   # Generated Parquet files (after conversion)
│   ├── fleet_monthly_agg.parquet
│   ├── fleet_spatial_1deg.parquet
│   ├── iuu_risk_all.parquet
│   ├── ais_disabling.parquet
│   └── anchorages.parquet
└── static/                 # Frontend HTML pages
    ├── index.html          # Dashboard home page
    ├── heatmap.html        # Leaflet heatmap of fishing effort
    ├── disabling_map.html  # AIS disabling events map
    ├── trends.html         # Chart.js bar/line/doughnut charts
    └── iuu_risk.html       # D3.js parallel coordinates
```

## Visualizations

| Page | Library | Chart Type | Data |
|------|---------|-----------|------|
| Heatmap | Leaflet + leaflet.heat | Heatmap on map | Fleet spatial effort |
| AIS Disabling | Leaflet | Point + arc map | Disabling events |
| Trends | Chart.js | Bar, doughnut, line | Fleet aggregates |
| IUU Risk | D3.js | Parallel coordinates + table | IUU risk indicators |

## API Endpoints

- `GET /api/fleet/by_flag?year=2024&n=15` — Top fishing nations
- `GET /api/fleet/by_gear?year=2024` — Effort by gear type
- `GET /api/fleet/trend?flag=CHN` — Monthly trend
- `GET /api/fleet/heatmap?year=2024` — Spatial data for heatmap
- `GET /api/iuu/top_risk?year=2024&n=50` — Highest risk vessels
- `GET /api/iuu/by_flag?year=2024&n=20` — Risk by flag state
- `GET /api/disabling/events?min_hours=24&flag=CHN` — Disabling events
- `GET /api/disabling/by_flag?n=15` — Disabling by country
- `GET /api/anchorages?iso3=SGP` — Port locations

## Notes

- The Parquet conversion aggregates the ~60M row fleet dataset to manageable sizes
- Fleet spatial uses 1-degree bins (~111km) for the heatmap
- IUU risk composite score is a simple weighted sum (not official)
- All maps use CARTO dark basemap tiles (no API key needed)
