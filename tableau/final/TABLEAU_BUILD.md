# Final Tableau Build Guide

Updated build plan incorporating professor feedback. Builds on `../TABLEAU.md` (the original 18-sheet guide). This document covers **only what is new or changed**.

Refer to `../TABLEAU.md` for the full step-by-step on the original 18 sheets and 6 dashboards. Everything there still applies — this file adds to it.

---

## New Data Sources to Add

### 9. IUU Fishing Index (External Validation)

**File:** `../../datasets/iuu_fishing_index.csv`  
**Rows:** 70 countries  
**Rename in Tableau:** "IUU Fishing Index"

| Column | Type | Description |
|--------|------|-------------|
| `iso3` | string | ISO3 country code — **join key to `flag` in other sources** |
| `country` | string | Country name |
| `iuu_score_2025` | float | IUU Fishing Index overall score (1 = best, 5 = worst) |
| `iuu_score_2023` | float | Previous edition score |
| `region` | string | Geographic region |
| `score_change` | float | 2025 minus 2023 (negative = improvement) |
| `risk_tier` | string | Very Low / Low / Medium / High / Very High |

**Join:** Blend or relationship with `country_summary.csv` on `iso3` = `flag`.

### 10. GDELT News Articles (when available)

**File:** `../../text/GDELT/gdelt_iuu_news_clean.csv`  
**Rename:** "GDELT News"

Key columns: `title`, `date`, `year`, `month`, `year_month`, `sourcecountry`, `query_name`, `topic_iuu`, `topic_seized`, `topic_labor`, `topic_china`, `topic_ais`, `topic_subsidy`, `topic_enforcement`

### 11. EJF Fisher Testimonies

**File:** `../../text/EJF/ejf_testimonies.csv` (111 rows)  
**File:** `../../text/EJF/ejf_word_freq.csv` (500 rows)  
**File:** `../../text/EJF/ejf_bigram_freq.csv` (300 rows)  
**Rename:** "EJF Testimonies", "EJF Words", "EJF Bigrams"

See `../../text/EJF/EJF_TABLEAU.md` for full build instructions on the 7 EJF sheets.

---

## New Sheets (3 from Feedback + 2 from IUU Index + GDELT)

All sheet numbers continue from the original 18.

---

### Sheet 19: Flag-vs-Port-State Matrix

**Purpose:** Surface flags of convenience — vessels flagged to one country but operating entirely from another's ports.  
**Data source:** `iuu_risk_cleaned.csv`  
**Why:** Professor feedback — "flag-state vs port-state matrix to surface flags of convenience"

1. Drag `flag` → **Rows** (this is `best_flag`, the vessel's registered country)
2. Drag `top_port_state` → **Columns** (where the vessel actually docks)
3. Drag `mmsi` → **Text** → right-click → **Measure → Count Distinct**
4. Drag `mmsi` (CNTD) → **Color** → sequential orange-red
5. Mark type → **Square** (creates a heatmap matrix)
6. Filter `flag` and `top_port_state` to Top 20 each by vessel count (otherwise too many countries)
7. Drag `year` → **Filters** → 2024
8. Right-click Color legend → **Edit Colors** → check **Use Full Color Range**

**What to look for:** Off-diagonal concentrations. If Panama-flagged vessels all port in Peru, or Vanuatu-flagged vessels port in China, that's classic flag-shopping. The diagonal (flag = port state) is normal; everything off-diagonal is worth investigating.

**Rename:** "Flag vs Port State"

---

### Sheet 20: Yearly Small-Multiples Heatmap

**Purpose:** Show how fishing effort shifts geographically over 2020–2024 — the trend view GFW's own map cannot show.  
**Data source:** `fleet_spatial_grid.csv`  
**Why:** Professor feedback — "yearly small multiples of the heat map"

1. Drag `lon_center` → **Columns**
2. Drag `lat_center` → **Rows**
3. Drag `year` → **Columns** (discrete, placed BEFORE lon_center)
   - This creates 5 maps side by side (one per year)
4. Drag `log_fishing_hours` → **Color** → sequential Orange-Red
5. Mark type → **Square** (renders faster than circles for 100K+ marks)
6. Reduce mark size to minimum (Size slider all the way left)
7. **Map → Map Layers → Style: Dark** → uncheck all layers
8. Fix the color range: **Color → Edit Colors → Advanced → check "Start" and "End"** → set identical values across all 5 years so colors are comparable

**Key insight:** You should see the 2020 map noticeably lighter (COVID dip), then 2021+ rebounding and possibly shifting geographically (e.g. more Southeast Asian activity in later years).

**Rename:** "Fishing Effort by Year (Small Multiples)"

---

### Sheet 21: Per-Vessel Gantt Timeline

**Purpose:** Show a selected vessel's year-by-year history of gaps, encounters, and voyages as a visual timeline.  
**Data source:** `iuu_risk_cleaned.csv`  
**Why:** Professor feedback — "per-vessel timeline (a Gantt of gaps and encounters)"

1. Use the same `Selected MMSI` parameter and `Is Selected` filter from Sheet 15
2. Drag `year` → **Columns** (discrete)
3. Create calculated fields:
   ```
   [Disabling Bar] = [disabling_over_12_hours]
   [Encounter Bar] = [number_encounters]
   [Voyage Bar] = [number_voyages]
   ```
4. Drag `Measure Names` → **Rows** → filter to: Disabling Bar, Encounter Bar, Voyage Bar
5. Drag `Measure Values` → **Columns**
6. Mark type → **Bar**
7. Drag `Measure Names` → **Color**:
   - Disabling Bar → Red
   - Encounter Bar → Orange
   - Voyage Bar → Blue
8. Drag `risk_score` → **Tooltip**

This creates a grouped bar chart per year showing the three activity types side-by-side — a simplified Gantt. Each year's bars tell you: how many voyages, how many encounters, how many times the vessel disabled AIS.

**Alternative (true Gantt):** If the dataset had individual event dates (not just annual counts), we could build a proper Gantt. With annual aggregates, the grouped bar is the cleanest representation.

**Rename:** "Vessel Activity Gantt"

---

### Sheet 22: IUU Index Validation Scatter

**Purpose:** External validation — do our GFW-derived country risk scores correlate with the independently published IUU Fishing Index?  
**Data source:** Blend `country_summary.csv` with `iuu_fishing_index.csv` on `flag` = `iso3`  
**Why:** Professor feedback — "use the IUU Fishing Index as an external validation target"

**Setup the blend:**
1. Primary: `country_summary.csv`
2. **Data → Edit Relationships** → link `flag` (country_summary) to `iso3` (IUU Fishing Index)

**Build the chart:**
1. Drag `avg_risk_score` (from country_summary) → **Columns**
2. Drag `iuu_score_2025` (from IUU Fishing Index, will show as orange pill) → **Rows**
3. Drag `flag` → **Detail**
4. Drag `flag` → **Label** (or just top 10)
5. Drag `fishing_hours` → **Size** (bigger bubbles = bigger fleets)
6. Drag `region` (from IUU Index) → **Color**
7. Add trend line: **Analytics → Trend Line → Linear**
8. Add R² annotation: right-click trend line → **Describe Trend Line** → note R²
9. Drag `year` → Filters → 2024

**What to look for:** A positive correlation (up-right trend) means our GFW-derived scores align with the expert-assessed IUU Index — validating our composite risk metric. Outliers (high on one axis, low on the other) are analytically interesting — they suggest countries that either evade detection or are overrepresented in expert assessments.

**Rename:** "IUU Index Validation"

---

### Sheet 23: IUU Index vs Disabling Rate

**Purpose:** Second validation angle — does a country's IUU Index score predict its AIS disabling rate?  
**Data source:** Same blend as Sheet 22

1. Drag `iuu_score_2025` → **Columns**
2. Drag `pct_vessels_with_disabling` (from country_summary) → **Rows**
3. Drag `flag` → **Detail** and **Label**
4. Drag `total_disabling_12h` → **Size**
5. Drag `region` → **Color**
6. Add trend line
7. Filter year → 2024

**Rename:** "IUU Index vs Disabling Rate"

---

### Sheet 24: GDELT News Volume Over Time (when data available)

**Data source:** `gdelt_iuu_news_clean.csv`

1. Drag `year_month` → **Columns** (or `date` as continuous month)
2. Drag `url` → **Rows** → CNTD (count distinct = article count)
3. Drag `query_name` → **Color** (lines by topic group)
4. Mark type → **Line**

**Rename:** "IUU News Volume Over Time"

---

### Sheet 25: GDELT News by Source Country (when data available)

**Data source:** `gdelt_iuu_news_clean.csv`

1. Drag `sourcecountry` → **Rows**
2. Drag `url` → **Columns** → CNTD
3. Sort descending, filter Top 20
4. Drag `topic_iuu` (SUM) → **Color**

**Rename:** "News Coverage by Country"

---

## Updated Dashboard Plan (8 Dashboards)

The original 6 dashboards remain. Add 2 new ones.

### Dashboard 7: "Validation & External Evidence" (NEW)

**Story point:** Do our findings hold up against independent data?

| Position | Sheet |
|----------|-------|
| Top-left (40%) | Sheet 22: IUU Index Validation Scatter |
| Top-right (40%) | Sheet 23: IUU Index vs Disabling Rate |
| Bottom (20%) | Sheet 24: GDELT News Volume (or text summary if GDELT not ready) |

**Title:** "External Validation: Do Our Risk Scores Match the Experts?"

### Dashboard 8: "Voices from the Fleet" (NEW — from EJF data)

See `../../text/EJF/EJF_TABLEAU.md` for the full build.

| Position | Sheet |
|----------|-------|
| Top-left | EJF Word Cloud (packed bubbles) |
| Top-right | EJF Bigram Bar Chart |
| Middle | Testimony Themes by Flag State |
| Bottom-left | Sentiment by Flag |
| Bottom-right | Testimonies by Year |

**Title:** "Voices from the Fleet: What 430 Fishers Told EJF"

---

## Updated Sheet Assignments

### Sheets added to EXISTING dashboards:

| New Sheet | Add to Dashboard |
|-----------|-----------------|
| Sheet 19: Flag vs Port State | Dashboard 3 (Risk Landscape) — add as a tab or replace Sheet 9 |
| Sheet 20: Yearly Small Multiples | Dashboard 1 (Where Does the World Fish?) — add as a second tab |
| Sheet 21: Vessel Activity Gantt | Dashboard 5 (Vessel Deep Dive) — add below the existing sheets |

---

## Total Final Count

| Item | Count |
|------|-------|
| Data sources | 11 (5 original + 3 joined + IUU Index + GDELT + EJF) |
| Sheets | 25 (18 original + 7 new) |
| Dashboards | 8 (6 original + 2 new) |
| Story points | 8 |

---

*This guide extends `../TABLEAU.md`. Read that first, then apply these additions.*
