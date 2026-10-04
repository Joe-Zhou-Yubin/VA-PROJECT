# Tableau Data Dictionary

Five pre-cleaned CSVs for import into Tableau. All generated from `prep_tableau_data.py`.

Import in Tableau via: **Data → New Data Source → Text file** → select the CSV.

---

## Summary

| File | Rows | Size | Granularity | Use in Tableau |
|------|------|------|-------------|----------------|
| `fleet_by_flag_gear_month.csv` | 55,053 | 4.5 MB | flag × gear × month | Bar charts, line charts, stacked area, treemaps |
| `fleet_spatial_grid.csv` | 113,896 | 5.0 MB | 1° grid × year | Map (filled map / symbol map / density) |
| `iuu_risk_cleaned.csv` | ~1.8M | 255 MB | vessel × year | Scatter, parallel coords, filters, vessel lookup |
| `ais_disabling_cleaned.csv` | 55,368 | 9.0 MB | individual event | Map (point / line), bar, timeline |
| `anchorages_cleaned.csv` | 166,497 | 15.3 MB | individual port | Map (reference layer), filters |

---

## 1. fleet_by_flag_gear_month.csv

Monthly fishing effort aggregated by flag state and gear type. 2020–2024.

| Column | Type | Description | Tableau role |
|--------|------|-------------|-------------|
| `year` | int | Year | Dimension |
| `month` | int | Month (1–12) | Dimension |
| `flag` | string | Flag state (ISO3) | Dimension |
| `geartype` | string | Gear type (16 categories, see hierarchy) | Dimension |
| `total_hours` | float | Total AIS broadcast hours | Measure |
| `fishing_hours` | float | Hours detected as fishing | Measure |
| `vessel_count` | int | Sum of vessel-visits in the month | Measure |
| `date` | date | First of the month (YYYY-MM-DD) — use for time axis | Dimension (date) |
| `fishing_ratio` | float | fishing_hours / total_hours (0–1) | Measure |
| `flag_clean` | string | Same as flag but nulls replaced with "UNKNOWN" | Dimension |
| `gear_category` | string | Parent gear category (rolls up sub-types) | Dimension |

**Gear type hierarchy** (use `gear_category` for grouping, `geartype` for detail):

```
fishing (generic)
├── drifting_longlines
├── seiners
│   ├── purse_seines
│   │   ├── tuna_purse_seines
│   │   └── other_purse_seines
│   └── other_seines
├── trawlers
├── pole_and_line
├── trollers
├── fixed_gear
│   ├── pots_and_traps
│   ├── set_longlines
│   └── set_gillnets
├── dredge_fishing
└── squid_jigger
```

**Suggested Tableau sheets:**
- Top fishing nations (bar, by `flag`, SUM `fishing_hours`)
- Monthly trend (line, `date` on columns, SUM `fishing_hours` on rows)
- Gear composition (stacked bar or treemap, `gear_category` color)
- Flag × gear heatmap (cross-tab with color intensity)

---

## 2. fleet_spatial_grid.csv

Fishing effort on a 1-degree lat/lon grid, aggregated by year. For map visualizations.

| Column | Type | Description | Tableau role |
|--------|------|-------------|-------------|
| `year` | int | Year | Dimension / filter |
| `lat` | int | Lower-left latitude of grid cell | Dimension |
| `lon` | int | Lower-left longitude of grid cell | Dimension |
| `fishing_hours` | float | Total fishing hours in cell | Measure |
| `vessel_count` | int | Total vessel-visits in cell | Measure |
| `lat_center` | float | Center latitude (lat + 0.5) — **use this for maps** | Dimension (geographic) |
| `lon_center` | float | Center longitude (lon + 0.5) — **use this for maps** | Dimension (geographic) |
| `log_fishing_hours` | float | log₁₀(fishing_hours) — **use for color** | Measure |

**Tableau setup:**
1. Right-click `lat_center` → Geographic Role → Latitude
2. Right-click `lon_center` → Geographic Role → Longitude
3. Double-click both → map appears
4. Drag `log_fishing_hours` to Color (use sequential palette)
5. Drag `year` to Filters or Pages (for animation)

---

## 3. iuu_risk_cleaned.csv

Vessel-level IUU risk indicators across all years (2012–2025). One row per vessel per year.

| Column | Type | Description | Tableau role |
|--------|------|-------------|-------------|
| `mmsi` | int | Maritime Mobile Service Identity | Dimension |
| `year` | int | Year of observation | Dimension / filter |
| `vessel_class` | string | Gear/vessel type | Dimension |
| `is_fishing` | bool | Whether classified as fishing | Dimension |
| `ship_name` | string | Best available name (AIS or registry) | Dimension |
| `flag` | string | Best available flag (ISO3) | Dimension |
| `ais_imo` | string | IMO from AIS | Dimension |
| `registry_imo` | string | IMO from registries | Dimension |
| `ais_callsign` | string | Radio callsign from AIS | Dimension |
| `registry_callsign` | string | Radio callsign from registries | Dimension |
| `top_port` | string | Most-visited port | Dimension |
| `top_port_state` | string | Country of most-visited port | Dimension |
| `hours` | float | Total AIS hours | Measure |
| `active_hours` | float | Hours actively moving | Measure |
| `previously_iuu_listed` | int | 0/1 — previously on an RFMO IUU list | Dimension |
| `iuu_listed` | int | 0/1 — currently on an RFMO IUU list | Dimension |
| `number_encounters` | int | At-sea encounters with other vessels | Measure |
| `number_iuu_listed_encounters` | int | Encounters with IUU-listed vessels | Measure |
| `number_previously_iuu_listed_encounters` | int | Encounters with previously IUU-listed vessels | Measure |
| `number_forced_labor_encounters` | int | Encounters with forced-labor-linked vessels | Measure |
| `dist_to_iuu` | float | Network degrees of separation to IUU vessel | Measure |
| `dist_to_forced_labor` | float | Network degrees of separation to forced-labor vessel | Measure |
| `average_voyage_duration_hours` | float | Mean voyage length | Measure |
| `number_voyages` | int | Total voyages in the year | Measure |
| `gaps_count` | int | Number of AIS transmission gaps | Measure |
| `disabling_over_12_hours` | int | Suspected AIS disabling events (>12h) | Measure |
| `disabling_over_24_hours` | int | Suspected AIS disabling events (>24h) | Measure |
| `overlap_hours_multinames` | float | Hours broadcasting same MMSI as another vessel | Measure |
| `risk_score` | float | Composite weighted risk score | Measure |
| `risk_tier` | string | None / Low / Medium / High | Dimension |
| `has_disabling` | int | 0/1 — any disabling event | Dimension |
| `has_iuu_encounter` | int | 0/1 — any encounter with IUU vessel | Dimension |
| `has_forced_labor_encounter` | int | 0/1 — any forced-labor encounter | Dimension |
| `has_spoofing` | int | 0/1 — any identity spoofing | Dimension |

**Risk score formula:**
```
risk_score = disabling_12h × 1
           + disabling_24h × 2
           + iuu_encounters × 3
           + forced_labor_encounters × 3
           + previously_iuu_encounters × 2
           + min(spoofing_hours, 100) / 10
           + iuu_listed × 5
```

**Suggested Tableau sheets:**
- Risk scatter (disabling_over_12_hours vs. number_encounters, color by risk_tier)
- Flag risk comparison (bar chart of avg risk_score by flag)
- Vessel detail lookup (use mmsi as filter → show all fields)
- Year-over-year risk trend (line, by year for a specific vessel)

---

## 4. ais_disabling_cleaned.csv

Individual AIS disabling events from Welch et al. (2022). 2017–2019.

| Column | Type | Description | Tableau role |
|--------|------|-------------|-------------|
| `gap_id` | string | Unique event identifier | Dimension |
| `mmsi` | int | Vessel MMSI | Dimension |
| `vessel_class` | string | Vessel/gear type | Dimension |
| `flag` | string | Flag state (ISO3) or "UNKNOWN" | Dimension |
| `vessel_length_m` | float | Vessel length in meters | Measure |
| `vessel_tonnage_gt` | float | Gross tonnage | Measure |
| `gap_start_date` | date | Date signal was lost | Dimension (date) |
| `gap_start_year` | int | Year | Dimension |
| `gap_start_month` | int | Month | Dimension |
| `gap_start_lat` | float | Latitude where signal lost | Dimension (geographic) |
| `gap_start_lon` | float | Longitude where signal lost | Dimension (geographic) |
| `gap_start_dist_shore_km` | float | Distance from shore at gap start (km) | Measure |
| `gap_end_lat` | float | Latitude where signal returned | Dimension (geographic) |
| `gap_end_lon` | float | Longitude where signal returned | Dimension (geographic) |
| `gap_end_dist_shore_km` | float | Distance from shore at gap end (km) | Measure |
| `gap_hours` | float | Duration of the gap (hours) | Measure |
| `gap_severity` | string | 12-24h / 24-48h / 48-72h / 72h+ | Dimension |
| `displacement_lat` | float | Latitude change while dark | Measure |
| `displacement_lon` | float | Longitude change while dark | Measure |

**Tableau setup for map:**
1. Right-click `gap_start_lat` → Geographic Role → Latitude
2. Right-click `gap_start_lon` → Geographic Role → Longitude
3. Double-click both → map
4. Drag `gap_severity` to Color
5. Drag `gap_hours` to Size

---

## 5. anchorages_cleaned.csv

Global port/anchorage locations. Use as a reference layer or join key.

| Column | Type | Description | Tableau role |
|--------|------|-------------|-------------|
| `s2id` | string | S2 cell identifier | Dimension |
| `lat` | float | Latitude | Dimension (geographic) |
| `lon` | float | Longitude | Dimension (geographic) |
| `label` | string | Port name | Dimension |
| `sublabel` | string | Sub-location | Dimension |
| `label_source` | string | How the label was derived | Dimension |
| `iso3` | string | Country code (ISO3) | Dimension |
| `distance_from_shore_km` | float | Distance from shore (km) | Measure |
| `at_dock` | bool | Whether the anchorage is at a dock | Dimension |

---

## How to Join in Tableau

**Fleet → IUU Risk:** use `flag` (fleet) = `flag` (iuu risk), and `year` = `year`. This gives you fishing effort context alongside risk indicators per country per year.

**IUU Risk → Disabling:** use `mmsi` to link specific vessels to their disabling events.

**IUU Risk → Anchorages:** use `top_port` (iuu risk) = `label` (anchorages), or `top_port_state` = `iso3` for country-level joins.

---

*Generated by `prep_tableau_data.py` from raw Global Fishing Watch data.*
*Last updated: August 2026.*
