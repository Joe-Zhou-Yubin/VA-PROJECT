# Beneath the Waves — Global Fishing Watch Visual Analytics

**IS428 Visual Analytics for Business Intelligence · Group Project**

An interactive visual analytics dashboard that reveals **where the world fishes**, **who fishes where**, and **which vessels display suspicious behavior indicative of illegal, unreported, and unregulated (IUU) fishing**. Built with Python, Flask, Leaflet, D3.js, and Chart.js using open data from Global Fishing Watch.

<p align="center">
  <a href="examples/">→ Live examples</a> ·
  <a href="DRAFT.md">→ Report draft</a> ·
  <a href="datasets/SUMMARY.md">→ Dataset docs</a> ·
  <a href="TEXT_SOURCES.md">→ Complementary sources</a>
</p>

---

## Repo Structure

```
Project/
├── README.md              # this file
├── DRAFT.md               # draft of the final group report
├── TEXT_SOURCES.md        # curated list of news sources and complementary datasets
├── datasets/              # raw source data (git-ignored — see download instructions)
│   ├── SUMMARY.md         # dataset schemas and documentation
│   ├── ais_disabling_events.csv        (ignored)
│   ├── named_anchorages_v2*.csv        (ignored)
│   ├── fleet-monthly/                  (60 monthly CSVs — ignored)
│   │   ├── README-fleet-v3.txt
│   │   ├── README-fishing-vessels-v3.txt
│   │   └── fleet-monthly-v3.schema.json
│   └── IUU-risk/                       (14 annual CSVs — ignored)
└── examples/              # working dashboard implementation
    ├── app.py             # Flask backend, 15+ REST endpoints
    ├── convert_to_parquet.py   # one-time CSV → Parquet ETL
    ├── requirements.txt
    ├── README.md          # dev/run instructions
    ├── data/              # generated Parquet files (ignored)
    └── static/            # 8 visualization pages
        ├── index.html
        ├── heatmap.html
        ├── disabling_map.html
        ├── country_map.html
        ├── trends.html
        ├── iuu_risk.html
        ├── sunburst.html
        ├── vessel_profile.html
        └── bar_race.html
```

## The Eight Visualizations

| # | Page | Category | Libraries | What it shows |
|---|------|----------|-----------|---------------|
| 1 | Fishing Effort Heatmap | Geographic | Leaflet + leaflet.heat | Global fishing intensity with click-to-inspect grid cells |
| 2 | AIS Disabling Map | Geographic | Leaflet + MarkerCluster | Where vessels "go dark" — clustered by severity |
| 3 | Country Choropleth | Geographic | Leaflet + GeoJSON | World map, toggle between fishing / disabling / IUU metrics |
| 4 | Trends & Rankings | Analytical | Chart.js | Bar, doughnut, and line charts of fleet aggregates |
| 5 | IUU Risk Profiles | Analytical | D3 v7 | Parallel coordinates + sortable risk table |
| 6 | Fleet Composition Sunburst | Analytical | D3 v7 | Zoomable flag → gear hierarchy |
| 7 | Vessel Profile Search | Interactive | D3 radar + Chart.js | Search by MMSI/name; radar + multi-year timeline |
| 8 | Bar Chart Race | Interactive | D3 v7 | Animated monthly ranking of top fishing nations |

## Quick Start

Requires Python 3.10+ and ~10 GB of free disk for raw datasets.

```bash
# 1. Clone the repo
git clone https://github.com/Joe-Zhou-Yubin/VA-PROJECT.git
cd VA-PROJECT

# 2. Install dependencies
pip install -r examples/requirements.txt

# 3. Download raw datasets from Global Fishing Watch
#    (See datasets/SUMMARY.md for exact files and destinations)
#    Register free at https://globalfishingwatch.org, then use the Data Download Portal.
#    Datasets required:
#    - AIS Apparent Fishing Effort v3 (fleet-monthly, 2020-2024)
#    - IUU Fishing Risk Insights
#    - Welch et al. (2022) AIS Disabling Events
#    - Anchorages

# 4. Convert CSVs to Parquet (one-time, 5-10 minutes)
cd examples
python convert_to_parquet.py

# 5. Start the Flask server
python app.py

# 6. Open http://localhost:5000
```

## Data Sources

All data is licensed **CC BY-NC 4.0** and courtesy of [Global Fishing Watch](https://globalfishingwatch.org/).

| Dataset | Coverage | Files | Rows |
|---------|----------|-------|------|
| AIS Apparent Fishing Effort v3 | 2020–2024 | 60 monthly CSVs | ~60M |
| IUU Fishing Risk Insights v1 | 2012–2025 | 14 annual CSVs | ~1.8M |
| AIS Disabling Events (Welch et al. 2022) | 2017–2019 | 1 CSV | 55,369 |
| Named Anchorages | Jul 2026 snapshot | 1 CSV | 166,498 |

Full column-level documentation in [datasets/SUMMARY.md](datasets/SUMMARY.md).

## Team

_[Fill in team member names]_

## Attribution & License

- **Data:** Global Fishing Watch, licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). See [globalfishingwatch.org/terms-of-use](https://globalfishingwatch.org/terms-of-use/).
- **Code:** MIT (for the visualization app in `examples/`).
- **Basemap tiles:** OpenStreetMap contributors, styled by CARTO.
- **World boundaries GeoJSON:** [johan/world.geo.json](https://github.com/johan/world.geo.json).

## References

Kroodsma, D.A. et al. (2018). Tracking the global footprint of fisheries. *Science*, 361(6378).
Welch, H. et al. (2022). Hotspots of unseen fishing vessels. *Science Advances*.
Paolo, F.S. et al. (2024). Satellite mapping reveals extensive industrial activity at sea. *Nature*, 625.
Global Fishing Watch (2025). *Global AIS-based Apparent Fishing Effort Dataset, Version 3.0*. https://doi.org/10.5281/zenodo.14982712

See [DRAFT.md](DRAFT.md) for the full report and [TEXT_SOURCES.md](TEXT_SOURCES.md) for a curated list of complementary datasets and news sources.
