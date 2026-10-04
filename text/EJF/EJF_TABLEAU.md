# EJF Text Visualization — Tableau Guide

Step-by-step instructions for building text-based visualizations from the EJF fisher testimony data.

## Data Files

| File | Rows | Load via |
|------|------|---------|
| `ejf_word_freq.csv` | 500 | Data → Text file |
| `ejf_bigram_freq.csv` | 300 | Data → Text file |
| `ejf_testimonies.csv` | 111 | Data → Text file |
| `ejf_statistics.csv` | 834 | Data → Text file |

---

## Sheet 1: Word Cloud (Word Frequency)

**Data source:** `ejf_word_freq.csv`

Tableau doesn't have a native word cloud. Two approaches:

### Option A — Use the built-in Packed Bubble as a proxy

1. Drag `word` → **Label** on Marks
2. Drag `count` → **Size** on Marks
3. Drag `count` → **Color** → sequential blue or orange palette
4. Mark type should auto-switch to **Packed Bubbles** (or select it manually)
5. Each bubble is a word, sized and colored by frequency

### Option B — Use a Tableau Extension

1. Go to the Marks card dropdown → look for **Word Cloud** under Viz Extensions (Tableau 2024.3+)
2. If available: drag `word` → the extension's text field, `count` → size
3. If not available: install from Tableau Exchange → search "Word Cloud"

### Option C — Export to external tool

1. The CSV is already ready — upload `ejf_word_freq.csv` to https://wordart.com or https://www.wordclouds.com
2. Map `word` → text, `count` → weight
3. Export as image → embed in your dashboard as a floating image

**Rename:** "EJF Word Cloud"

---

## Sheet 2: Bigram Bar Chart (Top Phrases)

**Data source:** `ejf_bigram_freq.csv`

1. Drag `bigram` → **Rows**
2. Drag `count` → **Columns**
3. Sort descending
4. Drag `bigram` → **Filters → Top → Top 25 by count**
5. Drag `count` → **Color** → sequential orange
6. Drag `count` → **Label**

Reveals the dominant phrases: "high seas", "jumbo squid", "distant water", "chinese flagged", "forced labour", etc.

**Rename:** "Top Phrases in EJF Reports"

---

## Sheet 3: Testimony Theme Distribution (Stacked Bar)

**Data source:** `ejf_testimonies.csv`

1. Drag `vessel_flag` → **Columns** (discrete)
2. Create a calculated field `Total Themes`:
   ```
   [theme_violence] + [theme_wildlife] + [theme_death] + [theme_wages] + [theme_conditions] + [theme_transshipment]
   ```
3. Better approach — use **Measure Names / Measure Values**:
   - Drag `Measure Names` → **Rows**
   - Filter `Measure Names` to keep only: `theme_violence`, `theme_wildlife`, `theme_death`, `theme_wages`, `theme_conditions`, `theme_transshipment`
   - Drag `Measure Values` → **Columns** (auto-sums the 0/1 flags = count of testimonies mentioning each theme)
   - Drag `Measure Names` → **Color**
4. Sort by total descending

This shows: "Chinese-flagged vessels have the most violence mentions, Taiwanese have the most wildlife mentions" etc.

**Color assignments:**
- `theme_violence` → Red
- `theme_wildlife` → Green
- `theme_death` → Dark red / black
- `theme_wages` → Orange
- `theme_conditions` → Blue
- `theme_transshipment` → Purple

**Rename:** "Testimony Themes by Flag State"

---

## Sheet 4: Testimony Sentiment by Vessel Flag (Box Plot or Bar)

**Data source:** `ejf_testimonies.csv`

1. Drag `vessel_flag` → **Columns**
2. Drag `sentiment_score` → **Rows**
3. Drag `quote` → **Detail** (one mark per testimony)
4. Mark type → **Circle**
5. Drag `sentiment_score` → **Color** → diverging palette (red-blue, centered at 0)
6. Drag `theme_violence` → **Size** (violent quotes appear larger)

**For a box plot alternative:**
1. Same axes
2. Click **Analytics pane** → drag **Box Plot** onto the chart
3. Shows median, quartiles, outliers per flag state

Most quotes will have negative sentiment (these are abuse testimonies). The interesting comparison is whether Chinese-flagged vessels have more extreme negative scores than Korean or Taiwanese.

**Rename:** "Testimony Sentiment by Flag"

---

## Sheet 5: Testimony Count by Year (Bar)

**Data source:** `ejf_testimonies.csv`

1. Drag `year` → **Columns** (discrete)
2. Drag `quote` → **Rows** → right-click → **Measure → Count**
3. Drag `vessel_flag` → **Color**

Shows when the interviews were conducted — most cluster in 2022–2025.

**Note:** Filter out rows where `year` is empty (some extracted quotes lack a date attribution).

**Rename:** "Testimonies by Year"

---

## Sheet 6: Violence vs. Wildlife (Scatter — per testimony)

**Data source:** `ejf_testimonies.csv`

1. Drag `neg_word_count` → **Columns**
2. Drag `word_count` → **Rows**
3. Drag `vessel_flag` → **Color**
4. Drag `quote` → **Detail**
5. Drag `theme_violence` → **Shape** (1 = filled circle, 0 = open circle)
6. Drag the quote text or a substring → **Tooltip**

Longer quotes with more negative words are in the top-right — the most detailed and disturbing accounts.

**Rename:** "Testimony Intensity"

---

## Sheet 7: Statistics by Category (Treemap)

**Data source:** `ejf_statistics.csv`

1. Mark type → **Treemap** (or Square + Color + Size)
2. Drag `category` → **Color**
3. Drag `statement` → **Detail** (one box per statistic)
4. Drag COUNT → **Size** (or just leave equal-sized)
5. Drag `statement` → **Tooltip**

Shows the distribution of numeric claims across categories: how many stats are about human_rights vs. environment vs. fleet_operations.

**Rename:** "Report Statistics by Topic"

---

## Dashboard: "Voices from the Fleet"

**Size:** 1400 × 900

| Position | Sheet | Size |
|----------|-------|------|
| Top-left (40%) | Sheet 1: Word Cloud (packed bubbles) | |
| Top-right (40%) | Sheet 2: Bigram Bar Chart | |
| Middle (30%) | Sheet 3: Theme Distribution by Flag | Full width |
| Bottom-left (30%) | Sheet 4: Sentiment by Flag | |
| Bottom-right (30%) | Sheet 5: Testimonies by Year | |

**Interactivity:**
1. Click the theme bar chart → funnel → **Use as Filter** → clicking "Chinese" filters the word cloud and sentiment chart to Chinese-flagged vessels only
2. Add a `vessel_flag` filter at the top as a dropdown

**Title:** "Voices from the Fleet: What 430 Fishers Told EJF About Life on Distant-Water Vessels"

---

## Dashboard: "Behind the Numbers"

A second dashboard focusing on the statistics and contextualizing the AIS data:

| Position | Sheet |
|----------|-------|
| Left (50%) | Sheet 7: Statistics Treemap |
| Right-top (25%) | Sheet 6: Testimony Intensity Scatter |
| Right-bottom (25%) | Sheet 5: Testimonies by Year |

**Title:** "Behind the Numbers: Mapping the Human Cost of Illegal Fishing"

---

## Data Cleaning Tips

### Filtering noisy testimonies

Some extracted quotes are long regulatory text, not actual fisher interviews. To filter:

1. In `ejf_testimonies.csv`, add a filter: `source = "manual"` to show only the verified hand-picked quotes
2. Or filter by `word_count < 100` to keep only shorter, punchier quotes
3. Or filter by any `theme_*` flag = 1 to keep only quotes that mention a specific theme

### Renaming vessel flags for display

Create an alias or calculated field:
```
IF [vessel_flag] = "Chinese" THEN "China 🇨🇳"
ELSEIF [vessel_flag] = "Korean" THEN "South Korea 🇰🇷"
ELSEIF [vessel_flag] = "Taiwanese" THEN "Taiwan 🇹🇼"
ELSE [vessel_flag]
END
```

---

## Script Files (for reproduction)

| Script | Purpose |
|--------|---------|
| `extract_ejf.py` | Main extraction: PDF → 5 CSVs |
| `run_extract.py` | Wrapper to run extraction with proper paths |

To re-run after updating PDFs:
```bash
cd Project/text/EJF
python extract_ejf.py
```
