# Datasets Summary

All data sourced from [Global Fishing Watch](https://globalfishingwatch.org/datasets-and-code/) (free account required for download).

**Project focus:** Visualizing global fishing activity, identifying suspicious vessel behavior, and mapping IUU (Illegal, Unreported, Unregulated) fishing risk.

---

## 1. Fleet-Monthly Fishing Effort

**Folder:** `fleet-monthly/`  
**Source:** AIS Apparent Fishing Effort v3.0 (March 2025 release)  
**Coverage:** 2020–2024 (5 years)  
**Structure:** 12 monthly CSV files per year (60 files total)  
**Rows per file:** ~1M (994K in Jan 2020 → 1.08M in Jan 2024)  
**Total estimated rows:** ~60M across all files  
**Grid resolution:** 0.1 degrees (~11 km at equator)

### Columns (10 fields)

| Column | Type | Description |
|--------|------|-------------|
| `date` | DATE | First day of the month (YYYY-MM-DD) |
| `year` | INT | Year |
| `month` | INT | Month (1–12) |
| `cell_ll_lat` | FLOAT | Latitude of grid cell lower-left corner (WGS84) |
| `cell_ll_lon` | FLOAT | Longitude of grid cell lower-left corner (WGS84) |
| `flag` | STRING | Flag state (ISO3 code, e.g. CHN, ESP, TWN) |
| `geartype` | STRING | Gear type classification (see below) |
| `hours` | FLOAT | Total AIS broadcast hours in grid cell |
| `fishing_hours` | FLOAT | Hours detected as fishing by ML model |
| `mmsi_present` | INT | Number of unique vessels in the grid cell |

### Gear Types (hierarchical)

- `fishing` (generic)
  - `drifting_longlines`
  - `seiners` → `purse_seines` → `tuna_purse_seines`, `other_purse_seines`
  - `seiners` → `other_seines`
  - `trawlers`
  - `pole_and_line`
  - `trollers`
  - `fixed_gear` → `pots_and_traps`, `set_longlines`, `set_gillnets`
  - `dredge_fishing`
  - `squid_jigger`

### File naming

```
fleet-monthly-csvs-10-v3-{YYYY}-{MM}-01.csv
```

---

## 2. IUU Fishing Risk Insights

**Folder:** `IUU-risk/`  
**Source:** IUU Fishing Risk Insights v1 (June 2026 release)  
**Coverage:** 2012–2025 (14 years, annual)  
**Rows per file:** ~131K (2020) → ~165K (2024)  
**Total estimated rows:** ~1.8M across all files  
**Granularity:** Per vessel (MMSI) per year

### Columns (33 fields)

| Column | Type | Description |
|--------|------|-------------|
| `mmsi` | INT | Maritime Mobile Service Identity (vessel ID) |
| `year` | INT | Year of observation |
| `vessel_class` | STRING | Gear type / vessel classification |
| `is_fishing` | BOOL | Whether vessel is classified as fishing |
| `ais_shipname` | STRING | Ship name broadcast via AIS |
| `registry_shipname` | STRING | Ship name from registries |
| `ais_imo` | STRING | IMO number from AIS |
| `registry_imo` | STRING | IMO number from registries |
| `ais_callsign` | STRING | Radio callsign from AIS |
| `registry_callsign` | STRING | Radio callsign from registries |
| `best_flag` | STRING | Best-determined flag state |
| `ais_flag` | STRING | Flag from AIS MID |
| `registry_flag` | STRING | Flag from vessel registries |
| `top_port` | STRING | Most visited port |
| `top_port_state` | STRING | Country of most visited port |
| `hours` | FLOAT | Total AIS hours |
| `positions` | INT | Total AIS positions recorded |
| `active_hours` | FLOAT | Hours actively moving |
| `active_positions` | INT | Positions while actively moving |
| `previously_iuu_listed` | INT | Whether previously on RFMO IUU list |
| `iuu_listed` | INT | Whether currently on RFMO IUU list |
| `number_encounters` | INT | Total at-sea encounters with other vessels |
| `number_forced_labor_encounters` | INT | Encounters with forced-labor-linked vessels |
| `number_iuu_listed_encounters` | INT | Encounters with currently IUU-listed vessels |
| `number_previously_iuu_listed_encounters` | INT | Encounters with previously IUU-listed vessels |
| `dist_to_forced_labor` | FLOAT | Network degrees of separation to forced-labor vessel |
| `dist_to_iuu` | FLOAT | Network degrees of separation to IUU-listed vessel |
| `average_voyage_duration_hours` | FLOAT | Mean voyage length |
| `number_voyages` | INT | Total voyages in the year |
| `gaps_count` | INT | Number of AIS gaps |
| `disabling_over_12_hours` | INT | Suspected AIS disabling events (>12 hrs) |
| `disabling_over_24_hours` | INT | Suspected AIS disabling events (>24 hrs) |
| `overlap_hours_multinames` | FLOAT | Hours broadcasting same MMSI as another vessel (identity spoofing) |

### File naming

```
{YYYY}_iuu_insights_v1_pipe4.csv
```

> Note: The 2021 file has a typo in the filename (`2021_iuu_insights_v1_pipe4..csv` — double dot).

---

## 3. AIS Disabling Events (Welch et al. 2022)

**File:** `ais_disabling_events.csv`  
**Source:** Welch et al. (2022), "Hotspots of unseen fishing vessels", Science Advances  
**Coverage:** 2017–2019  
**Rows:** 55,369 events  
**Granularity:** Individual disabling event (one gap = one row)

### Columns (15 fields)

| Column | Type | Description |
|--------|------|-------------|
| `gap_id` | STRING | Unique event identifier (hash) |
| `mmsi` | INT | Vessel MMSI |
| `vessel_class` | STRING | Vessel/gear type |
| `flag` | STRING | Flag state (ISO3) |
| `vessel_length_m` | FLOAT | Vessel length in meters |
| `vessel_tonnage_gt` | FLOAT | Gross tonnage |
| `gap_start_timestamp` | DATETIME | When AIS signal was lost |
| `gap_start_lat` | FLOAT | Latitude where signal was lost |
| `gap_start_lon` | FLOAT | Longitude where signal was lost |
| `gap_start_distance_from_shore_m` | FLOAT | Distance from shore at gap start (meters) |
| `gap_end_timestamp` | DATETIME | When AIS signal returned |
| `gap_end_lat` | FLOAT | Latitude where signal returned |
| `gap_end_lon` | FLOAT | Longitude where signal returned |
| `gap_end_distance_from_shore_m` | FLOAT | Distance from shore at gap end (meters) |
| `gap_hours` | FLOAT | Duration of the gap in hours |

> Only includes gaps >50 nautical miles from shore with sufficient satellite AIS reception.

---

## 4. Anchorages (Port Locations)

**File:** `named_anchorages_v2_pipe_v4_202607.csv`  
**Source:** Global Fishing Watch Anchorages Database  
**Coverage:** Global, updated July 2026  
**Rows:** 166,498 anchorage points  
**Granularity:** Individual anchorage location

### Columns (10 fields)

| Column | Type | Description |
|--------|------|-------------|
| `s2id` | STRING | S2 cell identifier (Google S2 geometry) |
| `lat` | FLOAT | Latitude |
| `lon` | FLOAT | Longitude |
| `label` | STRING | Port/anchorage name |
| `sublabel` | STRING | Sub-location name |
| `label_source` | STRING | How the label was determined |
| `iso3` | STRING | Country code (ISO3) |
| `distance_from_shore_m` | FLOAT | Distance from shore in meters |
| `drift_radius` | FLOAT | Typical drift radius at anchorage |
| `at_dock` | BOOL | Whether anchorage is at a dock |

---

## Dataset Relationships

```
Fleet-Monthly ──(flag, geartype)──► aggregated fishing effort by location
       │
       │ can join on mmsi (if using mmsi-daily variant)
       ▼
IUU Risk Insights ──(mmsi)──► per-vessel risk profile
       │
       │ mmsi links disabling events to risk profiles
       ▼
AIS Disabling Events ──(lat/lon)──► where vessels "go dark"
       │
       │ port visits contextualize vessel behavior
       ▼
Anchorages ──(lat/lon, iso3)──► global port reference
```

**Key join fields:**
- `mmsi` — links IUU Risk ↔ AIS Disabling (and mmsi-daily fishing effort if downloaded)
- `flag` / `best_flag` — compare fleet effort by country against IUU risk by country
- `lat/lon` — spatial joins across all datasets
- `vessel_class` / `geartype` — gear type analysis across datasets

---

## Size Summary

| Dataset | Files | Compressed | Est. Uncompressed |
|---------|-------|-----------|-------------------|
| Fleet-Monthly (2020–2024) | 60 CSVs | ~600 MB (ZIPs) | ~3–4 GB |
| IUU Risk Insights (2012–2025) | 14 CSVs | — | ~246 MB |
| AIS Disabling Events | 1 CSV | — | ~11 MB |
| Anchorages | 1 CSV | — | ~18 MB |
| **Total** | **76 files** | | **~4 GB** |

---

## Citation

Global Fishing Watch. 2025. *Global AIS-based Apparent Fishing Effort Dataset, Version 3.0*.  
https://doi.org/10.5281/zenodo.14982712

Welch et al. (2022). "Hotspots of unseen fishing vessels." *Science Advances*.

---

## License

CC BY-NC 4.0 — Non-Commercial Use Only.  
See [GFW Terms of Use](https://globalfishingwatch.org/terms-of-use/).
