# Tableau Step-by-Step Guide

Complete walkthrough for loading data, configuring joins, and building each visualization sheet for the IUU Fishing project.

---

## Part 1 — Setting Up the Workbook

### 1.1 Create a New Workbook

1. Open Tableau Desktop
2. **File → New** (or Ctrl+N)
3. Save as `GFW_IUU_Fishing.twbx` inside the `Project/tableau/` folder

### 1.2 Connect to the First Data Source (Fleet Monthly)

1. Click **Data → New Data Source** (or on the start page, click "Text file" under "Connect")
2. Navigate to `Project/tableau/data/`
3. Select `fleet_by_flag_gear_month.csv`
4. Tableau opens the Data Source tab showing a preview
5. Verify:
   - `date` is recognized as a Date type (blue calendar icon). If not, click the type icon on the column header → change to **Date**
   - `flag`, `geartype`, `gear_category` are Strings
   - `fishing_hours`, `total_hours`, `vessel_count` are Numbers

### 1.3 Connect the Remaining Data Sources

Repeat for each file — each becomes its own data source in the workbook:

| Step | File | Name it |
|------|------|---------|
| 2 | `fleet_spatial_grid.csv` | Fleet Spatial |
| 3 | `iuu_risk_cleaned.csv` | IUU Risk |
| 4 | `ais_disabling_cleaned.csv` | AIS Disabling |
| 5 | `anchorages_cleaned.csv` | Anchorages |

For each:
1. **Data → New Data Source → Text file** → pick the CSV
2. Once loaded, right-click the data source name at the top of the Data pane → **Rename** to the short name above

### 1.4 Fix Geographic Roles

**For Fleet Spatial:**
1. Go to the Data Source tab for Fleet Spatial
2. Click the type icon on `lat_center` → change to **Number (decimal)**
3. Right-click `lat_center` in the data pane → **Geographic Role → Latitude**
4. Right-click `lon_center` → **Geographic Role → Longitude**

**For AIS Disabling:**
1. Right-click `gap_start_lat` → **Geographic Role → Latitude**
2. Right-click `gap_start_lon` → **Geographic Role → Longitude**
3. Right-click `gap_end_lat` → **Geographic Role → Latitude**
4. Right-click `gap_end_lon` → **Geographic Role → Longitude**

**For Anchorages:**
1. Right-click `lat` → **Geographic Role → Latitude**
2. Right-click `lon` → **Geographic Role → Longitude**

### 1.5 Fix Data Types (if needed)

Tableau usually auto-detects correctly, but double-check:

| Data source | Column | Should be |
|-------------|--------|-----------|
| Fleet Monthly | `date` | Date |
| Fleet Monthly | `year`, `month` | Number (whole) |
| IUU Risk | `mmsi` | String (not number — leading zeros matter) |
| IUU Risk | `iuu_listed`, `previously_iuu_listed` | Number (whole) |
| IUU Risk | `risk_tier` | String |
| AIS Disabling | `gap_start_date` | Date |
| AIS Disabling | `mmsi` | String |

To change: click the type icon above the column name in the Data Source tab → pick the correct type.

---

## Part 2 — Data Sources (Pre-Joined, No Tableau Joins Needed)

All joins have been done externally by `join_tables.py`. Each CSV is a **flat table** — just connect via **Data → Text file** and start building.

### Your 8 data sources

| # | File | Location | Rows | Purpose |
|---|------|----------|------|---------|
| 1 | `fleet_with_risk.csv` | `data/joined/` | 55,053 | Fleet effort by flag×gear×month **+ country risk stats** |
| 2 | `fleet_spatial_grid.csv` | `data/` | 113,896 | 1° lat/lon grid for map heatmaps |
| 3 | `country_summary.csv` | `data/joined/` | 3,226 | One row per flag×year, fleet + IUU risk aggregates |
| 4 | `iuu_risk_cleaned.csv` | `data/` | ~1.8M | Vessel-level risk indicators (all years) |
| 5 | `disabling_enriched.csv` | `data/joined/` | 55,368 | Disabling events **+ vessel risk info, name, port** |
| 6 | `anchorages_cleaned.csv` | `data/` | 166,497 | Global ports/anchorages |
| 7 | `fleet_by_flag_gear_month.csv` | `data/` | 55,053 | Fleet effort (standalone, no risk columns) |
| 8 | `ais_disabling_cleaned.csv` | `data/` | 55,368 | Disabling events (standalone, no risk columns) |

**Primary files for most sheets:** `fleet_with_risk`, `country_summary`, `disabling_enriched`, and `iuu_risk_cleaned`. The others are backups or reference layers.

### Connect each one

For each file you plan to use:
1. **Data → New Data Source → Text file** → navigate to `tableau/data/` or `tableau/data/joined/`
2. Select the CSV → Tableau opens the Data Source tab
3. Right-click the data source name at top → **Rename** to a short name (e.g. "Fleet+Risk", "Country Summary")
4. Fix geographic roles and types as described in Part 1.4 and 1.5 above

No relationships or joins to configure. Each file stands alone.

---

## Part 3 — Building the Visualizations (18 Sheets)

Organized into the story narrative: **Overview → Who's Fishing → What Gear → Where's the Risk → Going Dark → Vessel Deep Dives → Time & Change**

---

### SECTION A: The Big Picture

---

### Sheet 1: Global Fishing Effort Map

**Data source:** `fleet_spatial_grid.csv`

1. Double-click `lat_center` and `lon_center` → map appears
2. Change mark type to **Circle** (or **Square** for a grid look)
3. Drag `log_fishing_hours` → **Color** on Marks
4. Click **Color → Edit Colors** → sequential palette **Orange-Red**
   - Check **Stepped Color** with 6 steps for cleaner bands
5. Drag `fishing_hours` → **Size** (optional, makes hot cells larger)
6. Drag `fishing_hours` and `vessel_count` → **Tooltip**
7. Drag `year` → **Filters** → select 2024 → right-click → **Show Filter**
8. **Map → Map Layers → Style: Dark** → uncheck Land Cover, check Coastline

**Tooltip template:**
```
Fishing Hours: <SUM(fishing_hours)>
Vessel Visits: <SUM(vessel_count)>
Location: <lat_center>, <lon_center>
```

**Rename:** "Global Fishing Map"

---

### Sheet 2: Top 20 Fishing Nations (Horizontal Bar)

**Data source:** `fleet_with_risk.csv`

1. Drag `flag_clean` → **Rows**
2. Drag `fishing_hours` → **Columns** (auto-sums)
3. Sort descending (toolbar ↓ button)
4. Drag `flag_clean` → **Filters → Top tab → By field → Top 20 by SUM(fishing_hours)**
5. Drag `country_avg_risk` → **Color** on Marks
   - Click **Color → Edit Colors** → diverging palette **Red-Blue Diverging**, reversed so red = high risk
6. Drag `country_pct_vessels_disabling` → **Tooltip**
7. Drag `year` → **Filters** → select 2024 → Show Filter
8. Right-click axis → Format → Numbers → abbreviate (K, M)

**Tooltip:**
```
<flag_clean>
Fishing Hours: <SUM(fishing_hours)>
Avg Risk Score: <AVG(country_avg_risk)>
% Vessels Disabling: <AVG(country_pct_vessels_disabling)>%
```

**Rename:** "Top Fishing Nations"

---

### Sheet 3: Monthly Fishing Trend (Line Chart)

**Data source:** `fleet_with_risk.csv`

1. Drag `date` → **Columns** → right-click pill → **Exact Date** (continuous)
2. Drag `fishing_hours` → **Rows**
3. Mark type auto-switches to Line
4. For global trend: leave as-is (single line)
5. For per-country: drag `flag_clean` → **Color** → filter to **Top 5 by SUM(fishing_hours)**

**Add COVID annotation:**
6. Right-click X-axis → **Add Reference Line → Line → Constant: 2020-03-15** → label "COVID-19" → dashed gray

**Rename:** "Monthly Fishing Trend"

---

### SECTION B: Fleet Composition

---

### Sheet 4: Gear Type Treemap

**Data source:** `fleet_with_risk.csv`

1. Mark type → **Treemap** (select from dropdown, or it auto-detects)
2. Drag `gear_category` → **Color**
3. Drag `fishing_hours` → **Size**
4. Drag `geartype` → **Label**
5. Drag `fishing_hours` → **Label** (hold Ctrl to add second label)
6. Drag `year` → Filters → 2024

**Rename:** "Gear Type Treemap"

---

### Sheet 5: Gear Composition by Country (Stacked Bar, Normalized)

**Data source:** `fleet_with_risk.csv`

1. Drag `flag_clean` → **Rows** → filter Top 15 by SUM(fishing_hours)
2. Drag `fishing_hours` → **Columns**
3. Drag `gear_category` → **Color**
4. Right-click axis → **Quick Table Calculation → Percent of Total** → Compute Using: Table (across)
   - This converts raw hours to % of each country's total
5. Sort by total fishing hours descending

This reveals which countries rely on trawlers vs. longlines vs. purse seines — structurally different fishing profiles.

**Rename:** "Fleet Composition by Country"

---

### Sheet 6: Fishing Efficiency Scatter (Hours vs. Fishing Ratio)

**Data source:** `country_summary.csv`

1. Drag `fishing_hours` → **Columns**
2. Drag `fishing_ratio` → **Rows**
3. Drag `flag` → **Detail** on Marks (one dot per country)
4. Drag `iuu_vessel_count` → **Size**
5. Drag `avg_risk_score` → **Color** → sequential red
6. Drag `flag`, `fishing_hours`, `fishing_ratio`, `avg_risk_score` → **Tooltip**
7. Drag `year` → Filters → 2024

Highlights which nations have large fleets that spend a higher proportion of time actually fishing (efficient) vs. transit/idle.

**Add trend line:** Analytics pane → drag **Trend Line** onto chart → Linear

**Rename:** "Fishing Efficiency by Country"

---

### SECTION C: Risk & Suspicion

---

### Sheet 7: Country Risk Ranking (Horizontal Bar + Dual Axis)

**Data source:** `country_summary.csv`

1. Drag `flag` → **Rows** → filter Top 20 by SUM(total_disabling_12h)
2. Drag `total_disabling_12h` → **Columns**
3. Drag `total_iuu_encounters` → **Columns** (second pill — creates second axis)
4. Right-click secondary axis → **Dual Axis** → then **Synchronize Axis**
5. On Marks card:
   - First measure tab (disabling): mark type **Bar**, color red
   - Second measure tab (IUU encounters): mark type **Circle**, color orange
6. Drag `year` → Filters → 2024
7. Sort by total_disabling_12h descending

**Rename:** "Country Risk Ranking"

---

### Sheet 8: IUU Risk Scatter (Disabling vs. Encounters)

**Data source:** `iuu_risk_cleaned.csv`

1. Drag `disabling_over_12_hours` → **Columns**
2. Drag `number_encounters` → **Rows**
3. Drag `risk_tier` → **Color** → assign: None = light gray, Low = blue, Medium = orange, High = red
4. Drag `risk_score` → **Size**
5. Drag `mmsi` → **Detail** (one dot per vessel)
6. Drag `ship_name`, `flag`, `vessel_class`, `risk_score` → **Tooltip**
7. Drag `year` → **Filters** → 2024 → Show Filter
8. **Critical:** Drag `risk_score` → **Filters** → At least 1 (excludes the 90%+ of vessels with zero risk, otherwise chart is a blob)

**Rename:** "IUU Risk Scatter"

---

### Sheet 9: Risk Heatmap by Flag × Indicator (Highlight Table)

**Data source:** `country_summary.csv`

1. Drag `flag` → **Rows** → filter Top 15 by `avg_risk_score`
2. Create a calculated field for each indicator you want to show:
   - Or simpler: drag `Measure Names` → **Columns** → filter to keep: `total_disabling_12h`, `total_iuu_encounters`, `total_forced_labor_encounters`, `total_spoofing_hours`, `high_risk_vessels`
3. Drag `Measure Values` → **Color** → sequential red
4. Drag `Measure Values` → **Label**
5. Mark type → **Square** (makes a heatmap grid)
6. Drag `year` → Filters → 2024

Each cell shows how a country scores on each indicator — instantly reveals who triggers what.

**Rename:** "Risk Indicator Heatmap"

---

### Sheet 10: Risk Tier Distribution (Stacked Bar)

**Data source:** `iuu_risk_cleaned.csv`

1. Drag `year` → **Columns** (discrete)
2. Drag `mmsi` → **Rows** → right-click → **Measure → Count Distinct**
3. Drag `risk_tier` → **Color** → assign: None = gray, Low = blue, Medium = orange, High = red
4. Right-click axis → **Quick Table Calculation → Percent of Total** → Compute Using: Table (down)

Shows the proportion of the global fleet that falls into each risk tier year over year — is it getting better or worse?

**Rename:** "Risk Tier Distribution"

---

### SECTION D: Where Vessels Go Dark

---

### Sheet 11: AIS Disabling Map (Enriched)

**Data source:** `disabling_enriched.csv`

1. Double-click `gap_start_lat` and `gap_start_lon` → map appears
2. Drag `gap_severity` → **Color** → assign severity-to-color:
   - 12-24h: `#ffd93d` (yellow)
   - 24-48h: `#f97316` (orange)
   - 48-72h: `#ef4444` (red)
   - 72h+: `#991b1b` (dark red)
3. Drag `gap_hours` → **Size**
4. Drag `ship_name`, `flag`, `risk_tier`, `risk_score`, `gap_hours`, `gap_start_dist_shore_km` → **Tooltip**
5. Click **Color** → reduce opacity to **50%**
6. **Map → Map Layers → Style: Dark**
7. Drag `gap_severity` → Filters → Show Filter
8. Drag `risk_tier` → Filters → Show Filter

**Tooltip:**
```
<ship_name> (<flag>)
Risk: <risk_tier> (score: <risk_score>)
Gap: <gap_hours> hours
Distance from shore: <gap_start_dist_shore_km> km
IUU encounters: <number_iuu_listed_encounters>
```

**Rename:** "Disabling Map (Enriched)"

---

### Sheet 12: Disabling by Flag + Risk (Stacked Bar)

**Data source:** `disabling_enriched.csv`

1. Drag `flag` → **Rows**
2. Drag `gap_id` → **Columns** → right-click → **Measure → Count Distinct**
3. Sort descending → filter Top 20
4. Drag `risk_tier` → **Color** (stacks bars by risk tier instead of severity)
5. Drag AVG(`gap_hours`) and AVG(`risk_score`) → **Tooltip**

This answers: "Which countries' vessels go dark, and of those, how many are already flagged as high-risk?"

**Rename:** "Disabling by Flag + Risk"

---

### Sheet 13: Disabling Distance from Shore (Histogram)

**Data source:** `disabling_enriched.csv`

1. Drag `gap_start_dist_shore_km` → **Columns** → right-click → **Create Bins → Bin Size: 50** (creates 50km bins)
2. Drag the new binned field → **Columns**
3. Drag `gap_id` → **Rows** → CNTD
4. Drag `gap_severity` → **Color**

Reveals that most disabling events happen 100-400km from shore — far enough that coast guard patrols can't easily reach.

**Rename:** "Disabling Distance from Shore"

---

### Sheet 14: Disabling Seasonality (Calendar Heatmap)

**Data source:** `disabling_enriched.csv`

1. Drag `gap_start_year` → **Columns**
2. Drag `gap_start_month` → **Rows** (discrete)
3. Drag `gap_id` → **Color** → CNTD → sequential orange
4. Drag `gap_id` → **Label** → CNTD
5. Mark type → **Square**

Shows whether disabling is seasonal (spoiler: it often peaks during migration seasons of high-value species).

**Rename:** "Disabling Seasonality"

---

### SECTION E: Vessel Deep Dives

---

### Sheet 15: Vessel Risk Profile (Highlight Table)

**Data source:** `iuu_risk_cleaned.csv`

1. Create parameter: right-click Data pane → **Create Parameter**
   - Name: `Selected MMSI`
   - Data type: **String**
   - Allowable values: **All**
2. Create calculated field `Is Selected`:
   ```
   STR([mmsi]) = [Selected MMSI]
   ```
3. Drag `Is Selected` → **Filters** → select True
4. Drag `year` → **Columns** (discrete)
5. Drag `Measure Names` → **Rows** → filter to:
   - `disabling_over_12_hours`, `disabling_over_24_hours`, `number_encounters`, `number_iuu_listed_encounters`, `number_forced_labor_encounters`, `overlap_hours_multinames`, `gaps_count`
6. Drag `Measure Values` → **Color** (sequential red) and **Label**
7. Mark type → **Square**
8. Right-click the `Selected MMSI` parameter → **Show Parameter**

Displays a vessel's risk indicators over time as a heatmap grid — each row is an indicator, each column a year.

**Rename:** "Vessel Risk Profile"

---

### Sheet 16: Vessel Activity Timeline (Dual-Axis Line)

**Data source:** `iuu_risk_cleaned.csv`

1. Use the same `Is Selected` filter from Sheet 15
2. Drag `year` → **Columns** (continuous)
3. Drag `hours` → **Rows** (left axis)
4. Drag `number_voyages` → **Rows** (second pill)
5. Right-click second axis → **Dual Axis → Synchronize** (or leave unsync'd if scales differ)
6. First axis: mark type **Area**, color blue, fill opacity 30%
7. Second axis: mark type **Line**, color orange, weight 2

Shows hours at sea vs. number of voyages over the years for the selected vessel.

**Rename:** "Vessel Activity Timeline"

---

### SECTION F: Country Comparison & Change Over Time

---

### Sheet 17: Fishing vs. Risk Bubble Chart

**Data source:** `country_summary.csv`

1. Drag `fishing_hours` → **Columns** (log axis recommended: right-click axis → Edit Axis → check **Logarithmic**)
2. Drag `avg_risk_score` → **Rows**
3. Drag `iuu_vessel_count` → **Size**
4. Drag `flag` → **Detail** and **Label** (one bubble per country)
5. Drag `pct_vessels_with_disabling` → **Color** → sequential red
6. Drag `year` → **Filters** → 2024
7. Drag `year` → **Pages** shelf for animation across years (play button appears)

This is the "Gapminder-style" view — each bubble is a country, sized by fleet size, positioned by fishing effort (x) vs. risk (y), colored by AIS disabling prevalence.

**Rename:** "Fishing vs. Risk Bubble"

---

### Sheet 18: Year-over-Year Risk Trend (Small Multiples)

**Data source:** `country_summary.csv`

1. Drag `year` → **Columns** (continuous)
2. Drag `avg_risk_score` → **Rows**
3. Drag `flag` → **Rows** (first position, before avg_risk_score) → filter to 6-8 interesting countries (e.g. CHN, TWN, ESP, RUS, KOR, PAN, IDN, JPN)
4. Each country gets its own row — a "small multiples" layout
5. Mark type → **Line**
6. Drag `total_disabling_12h` → **Color** → sequential red → makes the line redder in years with more disabling

Shows risk trajectories side-by-side for key nations.

**Rename:** "Risk Trend by Country"

---

## Part 4 — Building Dashboards (6 Dashboards)

Each dashboard tells a chapter of the story. Together they form a **Tableau Story**.

All dashboards: **New Dashboard → Size: 1400 × 900** (or 1920 × 1080 for presentations)

---

### Dashboard 1: "Where Does the World Fish?"

**Story point:** Establish the baseline — global fishing is massive and concentrated.

| Position | Sheet | Size |
|----------|-------|------|
| Top (60%) | Sheet 1: Global Fishing Map | Full width |
| Bottom-left (20%) | Sheet 2: Top Fishing Nations | Half width |
| Bottom-right (20%) | Sheet 3: Monthly Fishing Trend | Half width |

**Interactivity:**
1. Click the map → funnel icon → **Use as Filter** (click a region → bars and trend update)
2. Add `year` filter at top (Floating text box + filter control)

**Title:** "Where Does the World Fish? 695 Million Hours of Fishing Activity (2020–2024)"

---

### Dashboard 2: "Who Fishes — And How?"

**Story point:** Not all fleets are equal. Countries use fundamentally different gear types, revealing economic and ecological differences.

| Position | Sheet | Size |
|----------|-------|------|
| Left (50%) | Sheet 5: Fleet Composition by Country | Full height |
| Top-right (25%) | Sheet 4: Gear Type Treemap | |
| Bottom-right (25%) | Sheet 6: Fishing Efficiency Scatter | |

**Interactivity:**
1. Stacked bar → Use as Filter → clicking a country updates the treemap and scatter
2. Add `year` filter at top

**Title:** "Fleet DNA: How Each Nation Fishes"

---

### Dashboard 3: "The Risk Landscape"

**Story point:** Shift from "where they fish" to "who's suspicious." Introduce the IUU risk framework.

| Position | Sheet | Size |
|----------|-------|------|
| Top-left (40%) | Sheet 8: IUU Risk Scatter | |
| Top-right (40%) | Sheet 9: Risk Indicator Heatmap | |
| Bottom (20%) | Sheet 10: Risk Tier Distribution | Full width |

**Interactivity:**
1. Scatter → Use as Filter → click a dot → heatmap highlights that country
2. Year filter at top

**Title:** "Behavioral Risk Indicators: What Makes a Vessel Suspicious?"

---

### Dashboard 4: "Going Dark — Where Vessels Disappear"

**Story point:** The most dramatic finding — showing where and when AIS tracking drops off.

| Position | Sheet | Size |
|----------|-------|------|
| Left (55%) | Sheet 11: Disabling Map (Enriched) | Full height |
| Top-right (15%) | Sheet 12: Disabling by Flag + Risk | |
| Mid-right (15%) | Sheet 13: Distance from Shore Histogram | |
| Bottom-right (15%) | Sheet 14: Disabling Seasonality | |

**Interactivity:**
1. Bar chart → Use as Filter → click a flag → map highlights those events
2. Severity filter and Risk Tier filter at top
3. Dashboard Action: hovering on the map → highlight the same flag in the bar chart
   - **Dashboard → Actions → Add Action → Highlight → Source: Disabling Map → Target: Disabling by Flag → Run on: Hover**

**Title:** "Going Dark: 55,000 Times Vessels Turned Off Tracking"

---

### Dashboard 5: "Vessel Deep Dive"

**Story point:** Let the viewer investigate any individual vessel by MMSI.

| Position | Sheet | Size |
|----------|-------|------|
| Top (10%) | Parameter input for `Selected MMSI` | Banner |
| Middle-left (45%) | Sheet 15: Vessel Risk Profile (highlight table) | |
| Middle-right (45%) | Sheet 16: Vessel Activity Timeline | |
| Bottom (30%) | Text box with vessel metadata (auto-updates via tooltip or Sheet 7 filtered to one country) | |

**Setup:**
1. Show the `Selected MMSI` parameter (right-click → Show Parameter)
2. Both sheets use the same `Is Selected` filter — they update together

**Title:** "Vessel Investigation: Enter an MMSI to See Its Full History"

---

### Dashboard 6: "The Bigger Picture — Countries & Change"

**Story point:** Zoom out again — compare countries holistically and show change over time.

| Position | Sheet | Size |
|----------|-------|------|
| Top (50%) | Sheet 17: Fishing vs. Risk Bubble Chart | Full width |
| Bottom (50%) | Sheet 18: Risk Trend by Country (Small Multiples) | Full width |

**Interactivity:**
1. Bubble chart → Use as Filter → click a country → small multiples highlights that row
2. Add **Pages** shelf on the bubble chart with `year` → enables play/pause animation
3. Year filter at top

**Title:** "The Bigger Picture: How Nations Compare and Change Over Time"

---

## Part 5 — Assembling the Tableau Story

A **Story** in Tableau is a sequence of dashboards presented like a slide deck — ideal for the presentation.

### 5.1 Create the Story

1. Click **New Story** icon (bottom tab bar, next to New Dashboard)
2. Set size to match your dashboards (1400 × 900)
3. On the left pane, you'll see all your dashboards listed

### 5.2 Add Story Points (in narrative order)

| # | Dashboard | Caption for the story point tab |
|---|-----------|-------------------------------|
| 1 | Where Does the World Fish? | "695 million hours of AIS-observed fishing across 5 years" |
| 2 | Who Fishes — And How? | "Fleet composition reveals national strategies" |
| 3 | The Risk Landscape | "11 behavioral indicators flag suspicious vessels" |
| 4 | Going Dark | "55,000 times vessels turned off their tracking" |
| 5 | Vessel Deep Dive | "Investigating individual vessel histories" |
| 6 | The Bigger Picture | "How risk profiles evolve across nations and years" |

For each:
1. Drag the dashboard from the left pane → drop into the story canvas
2. Click the **caption bar** above → type the caption text
3. Click **New story point** (button top-left, or Blank tab at top) → add the next dashboard

### 5.3 Add Annotations to Story Points

For each story point you can add explanatory text:

1. Click the dashboard within the story
2. Add a **Text** object (drag from the Objects panel at bottom)
3. Position it as a floating annotation
4. Type a key insight, e.g.:
   - Story point 1: "China accounts for more fishing hours than the next 10 nations combined"
   - Story point 4: "Most disabling occurs 100-400km from shore — beyond coast guard range"

---

## Part 6 — Final Polish

### 6.1 Consistent Color Palette

Apply these everywhere:

| Semantic meaning | Hex | Where |
|-----------------|-----|-------|
| Neutral / fishing | `#4fc3f7` (light blue) | Fishing hours bars, fleet lines |
| Risk / danger | `#ff4444` (red) | High risk tier, disabling 72h+ |
| Warning / medium | `#ffaa00` (amber) | Medium risk, disabling 24-48h |
| Low risk | `#4fc3f7` (blue) | Low risk tier |
| No data / none | `#78909c` (gray) | Zero risk, unknown flags |
| Gear: trawlers | `#e63946` | Consistent across treemap and stacked bars |
| Gear: seiners | `#457b9d` | |
| Gear: longlines | `#f4a261` | |
| Gear: fixed gear | `#2a9d8f` | |

Set in each sheet: **Color → Edit Colors → select item → enter custom hex**

### 6.2 Dark Theme

1. **Format → Workbook Theme** → select a dark theme if available
2. Or manually per sheet: **Format → Shading → Worksheet** → `#112240`
3. **Format → Font → Worksheet** → all text white/light gray
4. **Map → Map Layers → Style: Dark**

### 6.3 Tooltips

Always customize tooltips. Click **Tooltip** on Marks → **Edit** → use HTML-like formatting:

```
<b><flag></b>
Fishing Hours: <SUM(fishing_hours)>
Vessels: <SUM(vessel_count)>
Avg Risk: <AVG(country_avg_risk)>
```

### 6.4 Titles and Captions

Every sheet:
- **Title:** double-click title bar → descriptive title
- **Caption:** Worksheet → Show Caption → data source attribution (e.g. "Source: Global Fishing Watch AIS data, 2020-2024")

### 6.5 Export / Publish

| Method | Use case |
|--------|----------|
| **File → Export as Image** (PNG) | Screenshots for the report |
| **File → Package Workbook** (.twbx) | Portable file with data embedded |
| **File → Save to Tableau Public** | Online sharing (free, requires account) |
| **Dashboard → Export → PowerPoint** | Slides for the Week 13 presentation |

---

## Quick Reference — Marks Card

| Drop target | What it does |
|---|---|
| Color | Colors marks by that field |
| Size | Scales mark size by that measure |
| Label | Shows text on marks |
| Detail | Adds granularity without visual encoding |
| Tooltip | Shows on hover only |
| Shape | Changes mark shapes (shape mark type only) |
| Pages | Creates animation / playback control |

## Quick Reference — Filter Interactions

**Make a chart filter other sheets on the same dashboard:**
1. Click the sheet on the dashboard
2. Click the **funnel icon** (top-right border of the sheet)
3. Select **Use as Filter**

**Limit which sheets are affected:**
1. **Dashboard → Actions → Add Action → Filter**
2. Set Source sheet, Target sheet(s), and clearing behavior

**Highlight instead of filter (gentler):**
1. **Dashboard → Actions → Add Action → Highlight**
2. Choose Source, Target, and which fields to highlight on

---

## Sheet → Data Source Cheat Sheet

| Sheet | Data Source |
|-------|-----------|
| 1 Global Fishing Map | `fleet_spatial_grid` |
| 2 Top Fishing Nations | `fleet_with_risk` |
| 3 Monthly Fishing Trend | `fleet_with_risk` |
| 4 Gear Type Treemap | `fleet_with_risk` |
| 5 Fleet Composition by Country | `fleet_with_risk` |
| 6 Fishing Efficiency Scatter | `country_summary` |
| 7 Country Risk Ranking | `country_summary` |
| 8 IUU Risk Scatter | `iuu_risk_cleaned` |
| 9 Risk Indicator Heatmap | `country_summary` |
| 10 Risk Tier Distribution | `iuu_risk_cleaned` |
| 11 Disabling Map (Enriched) | `disabling_enriched` |
| 12 Disabling by Flag + Risk | `disabling_enriched` |
| 13 Distance from Shore Histogram | `disabling_enriched` |
| 14 Disabling Seasonality | `disabling_enriched` |
| 15 Vessel Risk Profile | `iuu_risk_cleaned` |
| 16 Vessel Activity Timeline | `iuu_risk_cleaned` |
| 17 Fishing vs. Risk Bubble | `country_summary` |
| 18 Risk Trend by Country | `country_summary` |

---

*This guide assumes Tableau Desktop 2024.1+. Minor UI differences may exist in earlier/later versions.*
