# IS428 Group Project — Draft

## Beneath the Waves: Visualizing Global Fishing Activity and Illegal Fishing Risk

**Team:** _[Group Name / Members]_
**Module:** IS428 Visual Analytics for Business Intelligence
**Semester:** AY2026 · Term 1

---

## Abstract

Illegal, Unreported, and Unregulated (IUU) fishing costs the global economy an estimated USD 10–23 billion annually and threatens marine ecosystems, food security, and coastal communities. Because most fishing occurs beyond public view on the high seas, monitoring is difficult and enforcement patchy. This project uses Automatic Identification System (AIS) data published by Global Fishing Watch (GFW) to build an interactive visual analytics dashboard that reveals **where the world fishes**, **who fishes where**, and **which vessels display suspicious behavior indicative of IUU activity**. We combine 60 months of gridded fishing effort data with GFW's new vessel-level IUU Risk Insights dataset (released June 2026) and the Welch et al. (2022) AIS disabling hotspots to build eight coordinated visualizations spanning maps, hierarchical charts, animated rankings, and vessel-level profiles.

---

## 1. Introduction / Problem Statement

Roughly **80% of world trade** and virtually all commercial seafood catches move across the ocean, yet public visibility of that activity is thin. Coastal nations depend on fishing for jobs and protein, but fisheries are being depleted faster than they can recover — a problem worsened by IUU practices such as:

- Vessels turning off their AIS to hide their location ("going dark")
- Encounters at sea between suspicious vessels for illicit transshipment
- Identity spoofing (multiple vessels broadcasting the same MMSI)
- Fleets operating with links to forced labour

**Core questions our visualization aims to answer:**

1. **Where** is fishing effort concentrated across the world's oceans, and **how** has it shifted over 2020–2024?
2. **Which nations** dominate the global fishing fleet, and **what gear types** do they operate?
3. **Where and when** do vessels disable AIS ("go dark"), and **which flag states** account for the most disabling events?
4. **Which individual vessels** display the highest composite IUU risk profile based on observable behavior?
5. **How** does behavior differ between countries, gear types, and years?

## 2. Motivation

**Why should we care?**

- **Environmental:** Overfishing has already collapsed one-third of global fish stocks. IUU fishing accounts for roughly 1 in every 5 wild-caught fish sold on the market.
- **Economic:** Estimated USD 10–23 billion in losses annually. Small island developing states and low-income coastal nations bear a disproportionate share.
- **Human rights:** Forced labour and human trafficking have been documented on distant-water fishing fleets.
- **Regional relevance:** Singapore is a major port state, ship registry, and transshipment hub. Understanding vessel behavior in the region has direct policy relevance.

**Who benefits from this analysis?**

| Stakeholder | Use Case |
|-------------|----------|
| Fisheries regulators (e.g. RFMOs) | Prioritize enforcement patrols and targeted inspections |
| Port state control | Screen incoming vessels for risk before granting entry |
| NGOs & journalists | Investigate suspicious fleet behavior and specific vessels |
| Policy makers | Evaluate the impact of fisheries agreements and sanctions |
| Researchers | Explore behavioral patterns in the AIS data at scale |

## 3. Related Works

### Existing Visualizations

- **[Global Fishing Watch Map](https://globalfishingwatch.org/map)** — the reference platform for visualizing AIS-based fishing activity. Powerful but geared toward analysts already familiar with the domain; the interface prioritizes exploration over narrative.
- **[Global Maritime Traffic](https://globalmaritimetraffic.org/)** — vessel density visualization. Covers all vessel types (not fishing-focused) and lacks IUU risk overlays.
- **[OECD AIS Vessel Tracking Dashboard](https://www.oecd.org/en/data/dashboards/monitoring-maritime-trade-the-oecd-ais-vessel-tracking-dashboard.html)** — trade-focused view of maritime traffic. Not fishing-specific.
- **[Ocean Mind](https://www.oceanmind.global/)** — commercial platform combining AIS + satellite radar for enforcement. Not publicly accessible.

### Academic Work

- **Kroodsma et al. (2018)**, "Tracking the global footprint of fisheries", _Science_ — foundational paper introducing the GFW fishing detection model.
- **Welch et al. (2022)**, "Hotspots of unseen fishing vessels", _Science Advances_ — behind our AIS disabling events dataset. Identified 55K+ suspicious gaps between 2017–2019.
- **Paolo et al. (2024)**, _Nature_ — used satellite radar to reveal ~75% of industrial fishing vessels do not appear in public tracking.

### How our approach differs

Existing platforms are either domain-expert tools (GFW map) or single-purpose reports. Our project prioritizes **narrative-driven exploration**: a coordinated set of eight complementary views that a non-expert can navigate from a global overview down to a single vessel's history. We also incorporate GFW's brand-new (June 2026) **IUU Risk Insights dataset** which, to our knowledge, has not yet appeared in student or public dashboards.

---

## 4. Datasets, Tools and Resources

### Data Sources — Global Fishing Watch

All data is licensed CC BY-NC 4.0 and downloaded from the [GFW Data Portal](https://globalfishingwatch.org/datasets-and-code/).

| Dataset | Coverage | Size | Rows |
|---------|----------|------|------|
| AIS Apparent Fishing Effort v3 (fleet-monthly) | 2020–2024 | ~600 MB (60 CSVs) | ~60M |
| IUU Fishing Risk Insights v1 | 2012–2025 | ~246 MB (14 CSVs) | ~1.8M |
| AIS Disabling Events (Welch et al. 2022) | 2017–2019 | ~11 MB | 55,369 |
| Named Anchorages (Jul 2026) | Global snapshot | ~18 MB | 166,498 |

Key data attributes we leverage:

- **Fishing effort:** date, grid cell (0.1°), ISO3 flag, gear type, fishing hours, hours, vessel count
- **IUU Risk:** 33 fields per vessel including AIS disabling counts (12h/24h), IUU-listed encounters, forced-labour encounters, network proximity to known offenders, identity spoofing hours, voyage duration, top port
- **Disabling events:** MMSI, gap start/end coordinates & timestamps, distance from shore, gap duration

Additional supporting data:

- **[johan/world.geo.json](https://github.com/johan/world.geo.json)** — country boundary GeoJSON for choropleth (ISO3-keyed)
- **[CARTO dark basemap](https://carto.com/)** — no-key tile provider for maps

### Data Preprocessing

The raw fleet-monthly dataset is ~60M rows across 60 CSVs — too large for direct use in a browser. We built a Python conversion script that produces three aggregated Parquet files:

1. `fleet_monthly_agg.parquet` — (year, month, flag, geartype) totals (~100K rows)
2. `fleet_spatial_1deg.parquet` — (year, lat, lon) 1° grid for the heatmap
3. `fleet_spatial_detail.parquet` — (year, lat, lon, flag, geartype) for click-to-inspect

Small datasets (IUU risk, disabling, anchorages) are converted to Parquet unchanged for fast querying.

### Tools and Justification

| Layer | Tool | Why |
|-------|------|-----|
| Data storage | **Apache Parquet** | Columnar format, 10x smaller than CSV, fast filtered reads |
| Data processing | **Python + pandas + pyarrow** | Familiar, mature ecosystem for tabular ETL |
| Backend server | **Flask** | Lightweight, easy REST API, integrates cleanly with pandas |
| Base maps | **Leaflet + leaflet.heat + MarkerCluster** | Open source, no API key, works with CARTO dark tiles |
| Choropleth colour scaling | **D3 scaleSequentialLog** | Handles skewed distributions (fishing hours span orders of magnitude) |
| Analytical charts | **Chart.js** | Fast standard charts (bar/line/donut) with minimal boilerplate |
| Custom / bespoke charts | **D3.js v7** | Sunburst, parallel coordinates, radar, bar chart race — no library equivalent |

**Why not just Tableau?** Tableau does not support all our chart types natively (parallel coordinates, zoomable sunburst, animated bar chart race). Building on the web also gives us fine-grained control over interactivity and enables future embedding on a website.

---

## 5. Tasks

We identified nine analytical tasks the dashboard must support:

| # | Task | Visualization |
|---|------|---------------|
| T1 | Overview of global fishing activity | Fishing Effort Heatmap |
| T2 | Compare fishing intensity by country | Country Choropleth |
| T3 | Identify high-risk vessels | IUU Risk Profiles (Parallel Coords) |
| T4 | Investigate individual vessel history | Vessel Profile Search |
| T5 | Detect suspicious "dark" activity locations | AIS Disabling Map |
| T6 | Understand fleet composition | Fleet Composition Sunburst |
| T7 | Observe how rankings shift over time | Bar Chart Race |
| T8 | Trend analysis and cross-metric comparison | Trends & Rankings Dashboard |
| T9 | Provide contextual reference data (ports) | Anchorages integration |

Each task follows Shneiderman's mantra: **overview first, zoom and filter, details on demand**.

---

## 6. Method

### 6.1 System Architecture

```
┌─────────────────────────┐
│  Raw GFW CSVs (~5 GB)  │
└───────────┬─────────────┘
            │  convert_to_parquet.py
            ▼
┌─────────────────────────┐
│  Aggregated Parquet     │  ← ~800 MB, columnar
│  files (5 tables)       │
└───────────┬─────────────┘
            │  pandas queries on load
            ▼
┌─────────────────────────┐         ┌──────────────────┐
│  Flask REST API (app.py)│ ◄─JSON─►│ HTML/JS frontend │
│  - Lazy caches parquet  │         │ - Leaflet, D3,   │
│  - 15+ endpoints        │         │   Chart.js       │
└─────────────────────────┘         └──────────────────┘
```

### 6.2 Major Challenges & Solutions

**Challenge 1: Data volume**
60M rows of fishing effort data cannot be loaded into a browser or served row-by-row.
_Solution:_ Precompute three aggregation levels (fleet-monthly totals, 1° spatial grid, 1° spatial with flag/gear detail). Cache Parquet files in server memory on first read.

**Challenge 2: Skewed distributions**
Fishing hours by country range from tens of hours (small nations) to tens of millions (China). Linear color scales wash out most countries.
_Solution:_ Use **logarithmic color scale** (`d3.scaleSequentialLog`) for choropleth. All comparative charts sort descending to highlight top contributors.

**Challenge 3: Rendering large point sets**
55K disabling events overwhelm Leaflet with per-marker rendering.
_Solution:_ Adopted **Leaflet.markercluster** to aggregate points at low zoom and expand them on interaction. Added `parseFloat` + `isNaN` guards (naive truthy checks failed at latitude/longitude of exactly 0).

**Challenge 4: Composite risk scoring**
The IUU Risk Insights dataset provides 11 indicators but no single score.
_Solution:_ Built a transparent weighted sum where the two most severe indicators (currently IUU-listed, forced labour encounters) contribute 3× weight each; disabling events contribute 1–2×, spoofing is scaled by hours. We treat this score as a **screening signal** rather than definitive evidence, mirroring GFW's own caveats.

**Challenge 5: Country boundary matching**
GeoJSON files use various country code schemes.
_Solution:_ Chose [johan/world.geo.json](https://github.com/johan/world.geo.json) because its `id` field uses ISO3 codes matching GFW's `flag` field directly.

### 6.3 Design Decisions

- **Dark colour theme** — matches the ocean subject matter and reduces eye strain during long exploration sessions. Also improves visibility of heatmap gradients.
- **Coordinated colour semantics** across all pages:
  - Blue (`#4fc3f7`) = neutral / information
  - Red / orange (`#ff6b6b`, `#ff8800`) = risk / disabling / IUU
  - Amber (`#ffaa00`) = warnings / gap trajectories
- **Consistent navigation** — every page has a "Back to home" link fixed top-left; the landing page groups the eight visualizations into three semantic sections (Geographic, Analytical, Interactive).

---

## 7. Visual Analysis Results & Discussions

### 7.1 Geographic Explorations

**Fishing Effort Heatmap.** The dominant fishing zones globally are:
- The East China Sea and Yellow Sea (China, South Korea, Japan)
- The Grand Banks (northwest Atlantic)
- The Northeast Atlantic (Norway, Iceland, UK)
- The Peruvian anchoveta grounds
- Southeast Asian waters (Indonesia, Vietnam, Philippines)

Clicking any cell reveals a detailed flag/gear breakdown — for example, clicking a cell in the Yellow Sea shows dozens of Chinese trawlers and squid jiggers dominating that grid square.

**Country Choropleth.** Toggling between metrics reveals striking contrasts:
- **Fishing hours (2024):** China dwarfs all others (~200M hours), followed by Taiwan, Spain, and South Korea.
- **AIS disabling events:** The distribution is very different — Portugal (`PRT`), Panama (`PAN`), and several West African flags appear high in the list, hinting at flag-of-convenience patterns.
- **IUU-listed encounters (2024):** Concentrated among distant-water fleets fishing in others' EEZs.

**AIS Disabling Map.** Clusters of "dark" activity concentrate near:
- The Argentinian EEZ boundary (squid fleets)
- Off West Africa (near Guinea-Bissau, Mauritania)
- The North Pacific transition zone
- Approaches to Antarctica

These are precisely the areas where high-value species live and enforcement is thin — a strong signal that AIS disabling correlates with high-risk fishing zones.

### 7.2 Analytical Dashboards

**IUU Risk Profiles (Parallel Coordinates).** The top 50 highest-risk vessels in 2024 show a consistent pattern: many high scorers combine identity spoofing (>50 hours of dual-MMSI overlap) with frequent AIS gaps, but few appear on formal IUU lists — supporting the argument that behavioral indicators catch risk that formal lists miss.

**Fleet Composition Sunburst.** Nations' fleet profiles are strikingly different:
- **China:** Diverse — squid jiggers (~30%), trawlers (~30%), drifting longlines, purse seiners
- **Japan / Korea:** Dominated by longlines and purse seines (tuna fisheries)
- **Norway:** Almost entirely trawlers and seiners (bottom fisheries)
- **Peru:** Nearly 100% purse seiners (anchoveta reduction fishery)

**Trends & Rankings.** Global fishing effort dipped in early 2020 (COVID-19) then rebounded above pre-pandemic levels by 2022. Trawlers remain the single largest gear category by hours.

### 7.3 Interactive Deep Dives

**Vessel Profile Search.** Illustrative example: querying the top-risk vessel in 2024 reveals a Panamanian-flagged squid jigger with 8 AIS gaps over 24h, 15 encounters with previously IUU-listed vessels, and 200+ hours of MMSI overlap with another vessel — every red flag simultaneously.

**Bar Chart Race.** Playing the animation, we see:
- China's fishing hours climb steadily
- South Korea and Taiwan swap positions frequently
- Spain remains the top European fleet
- The 2020 COVID dip and the 2022 fuel-price shock are visible as brief plateaus

---

## 8. Conclusion & Future Work

### Key Findings

1. **Fishing is highly concentrated:** ~5 nations account for the majority of global effort.
2. **Fleet composition varies dramatically:** Beyond hours, _how_ a country fishes reveals its economic and ecological posture.
3. **Behavioral risk indicators are informative:** Vessels can be flagged as high-risk long before they appear on formal IUU lists.
4. **AIS disabling has geographic patterns:** Suspicious gaps cluster near EEZ boundaries and enforcement-thin waters.
5. **Regional relevance:** Southeast Asia (relevant to Singapore) shows substantial dark activity — a policy opportunity for a port state.

### Challenges Faced

- Volume of raw AIS data required significant preprocessing and aggregation strategy
- No official composite risk score, so we built our own (transparently, with limitations noted)
- Country boundary matching across data sources
- Rendering performance for large point sets

### Future Work

- **Add temporal animation to the heatmap** — currently the heat map is a per-year snapshot; a play-through of monthly frames would surface seasonal patterns.
- **Integrate satellite radar data** (Paolo et al. 2024) — reveal "hidden" vessels not broadcasting AIS at all.
- **Network graph of vessel encounters** — force-directed layout of vessels linked by at-sea encounters, colour by IUU-listing status.
- **Alerting layer** — flag when a vessel's risk score jumps year-over-year.
- **Case study integration** — deep-dive tabs for specific investigations (e.g., squid jiggers on the Argentinian shelf).
- **Sankey diagram** for flag-of-registration → top port state flows (data endpoint is already implemented in the backend).

---

## 9. Team Contributions

_[To be filled in]_

| Member | Responsibilities |
|--------|------------------|
| _Name_ | Data pipeline, Parquet conversion, Flask backend |
| _Name_ | Geographic visualizations (heatmap, choropleth, disabling map) |
| _Name_ | Analytical dashboards (trends, sunburst, parallel coords) |
| _Name_ | Interactive drilldowns (vessel profile, bar chart race) |
| _Name_ | Design system, landing page, integration testing, presentation |

---

## 10. References

1. Global Fishing Watch. (2025). *Global AIS-based Apparent Fishing Effort Dataset, Version 3.0*. https://doi.org/10.5281/zenodo.14982712
2. Global Fishing Watch. (2026). *IUU Fishing Risk Insights, Version 1*. https://globalfishingwatch.org/datasets-and-code
3. Kroodsma, D.A. et al. (2018). Tracking the global footprint of fisheries. *Science*, 361(6378).
4. Welch, H. et al. (2022). Hotspots of unseen fishing vessels. *Science Advances*.
5. Paolo, F.S. et al. (2024). Satellite mapping reveals extensive industrial activity at sea. *Nature*, 625.
6. FAO. (2024). *The State of World Fisheries and Aquaculture 2024*.
7. Sumaila, U.R. et al. (2020). Illicit trade in marine fish catch and its effects on ecosystems and people worldwide. *Science Advances*, 6(9).
8. Shneiderman, B. (1996). The eyes have it: a task by data type taxonomy for information visualizations. *IEEE Symposium on Visual Languages*.

---

## Appendix A — Project Repository Structure

```
Project/
├── DRAFT.md                          # this file
├── datasets/                         # raw + parquet-ready data
│   ├── SUMMARY.md                    # dataset documentation
│   ├── ais_disabling_events.csv
│   ├── named_anchorages_v2_pipe_v4_202607.csv
│   ├── fleet-monthly/ (60 monthly CSVs, 5 years)
│   └── IUU-risk/ (14 annual CSVs)
└── examples/                         # working dashboard implementation
    ├── app.py                        # Flask backend, 15+ API endpoints
    ├── convert_to_parquet.py         # ETL script
    ├── data/                         # generated Parquet files
    ├── requirements.txt
    ├── README.md
    └── static/                       # 8 visualization pages
        ├── index.html                # Landing page
        ├── heatmap.html              # Leaflet + heat
        ├── disabling_map.html        # Leaflet + clusters
        ├── country_map.html          # Leaflet choropleth
        ├── trends.html               # Chart.js panels
        ├── iuu_risk.html             # D3 parallel coordinates
        ├── sunburst.html             # D3 zoomable sunburst
        ├── vessel_profile.html       # D3 radar + Chart.js timeline
        └── bar_race.html             # D3 animated bar chart race
```

## Appendix B — How to Run

```bash
cd Project/examples
pip install -r requirements.txt
python convert_to_parquet.py       # one-time, ~10 min
python app.py                      # http://localhost:5000
```
