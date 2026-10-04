# Story Flow & Dashboard Formation Guide

How the 8 dashboards connect into a single Tableau Story. Follow this when assembling the final `.twbx`.

---

## The Narrative Arc

The story answers one question at increasing depth: **"What is happening on the world's oceans, and should we be worried?"**

```
ACT 1: SCALE            ACT 2: SUSPICION           ACT 3: EVIDENCE
"How big is this?"      "Who's doing what?"        "Can we prove it?"

 Dashboard 1             Dashboard 3                Dashboard 7
 Where the world         The risk landscape         External validation
 fishes                                            
                         Dashboard 4                Dashboard 8
 Dashboard 2             Going dark                 Voices from the fleet
 Fleet DNA                                         
                         Dashboard 5
                         Vessel deep dive
                        
                         Dashboard 6
                         The bigger picture
```

The viewer starts with the familiar (a world map) and ends with human testimony. Each dashboard raises a question that the next one answers.

---

## Story Point Sequence

Build this in Tableau: **New Story → Size 1400×900 → add each dashboard as a story point in order.**

### Story Point 1: "Where Does the World Fish?"

**Dashboard 1**

| Position | Sheet | Data Source |
|----------|-------|-------------|
| Top 60% | Sheet 1: Global Fishing Map | `fleet_spatial_grid` |
| Bottom-left 20% | Sheet 2: Top 20 Fishing Nations | `fleet_with_risk` |
| Bottom-right 20% | Sheet 3: Monthly Fishing Trend | `fleet_with_risk` |

**Caption:** "695 million hours of AIS-observed fishing across 2020–2024"

**Key insight to annotate:** China accounts for more fishing hours than the next 10 nations combined. Fishing dipped visibly in early 2020 (COVID) then rebounded above pre-pandemic levels.

**Filter:** Year selector at top (dropdown). Map → Use as Filter on the bar chart and line chart.

**Transition question → next point:** "But where is the fishing concentrated, and has that shifted?"

---

### Story Point 2: "How Fishing Has Shifted (2020–2024)"

**Dashboard 1 (second tab)** or standalone

| Position | Sheet |
|----------|-------|
| Full width | Sheet 20: Yearly Small-Multiples Heatmap |

**Caption:** "Five years side by side: fishing effort by location"

**Key insight:** The 2020 panel is visibly lighter than 2021–2024. Southeast Asian waters show growing intensity year over year. The Northwest Pacific and Argentine shelf remain consistently hot.

**Transition → next:** "Now we know where the world fishes. But who fishes, and with what gear?"

---

### Story Point 3: "Fleet DNA: How Each Nation Fishes"

**Dashboard 2**

| Position | Sheet | Data Source |
|----------|-------|-------------|
| Left 50% | Sheet 5: Fleet Composition by Country | `fleet_with_risk` |
| Top-right 25% | Sheet 4: Gear Type Treemap | `fleet_with_risk` |
| Bottom-right 25% | Sheet 6: Fishing Efficiency Scatter | `country_summary` |

**Caption:** "Fleet composition reveals national fishing strategies"

**Key insight:** China is diversified (squid jiggers, longlines, trawlers, seiners). Peru is almost 100% purse seiners. Vietnam is trawler-heavy, implying high bycatch. Even a small proportional share of China's fleet exceeds the entire output of most countries.

**Filter:** Click a country in the stacked bar → treemap and scatter update.

**Transition → next:** "Some of these fleets carry elevated risk. How do we measure suspicion?"

---

### Story Point 4: "The Risk Landscape"

**Dashboard 3**

| Position | Sheet | Data Source |
|----------|-------|-------------|
| Top-left 35% | Sheet 8: IUU Risk Scatter | `iuu_risk_cleaned` |
| Top-right 35% | Sheet 19: Flag vs Port State Matrix | `iuu_risk_cleaned` |
| Bottom-left 30% | Sheet 9: Risk Indicator Heatmap | `country_summary` |

**Caption:** "11 behavioural indicators flag suspicious vessels"

**Key insight (scatter):** The top-risk vessels combine multiple red flags: AIS disabling + identity spoofing + IUU-listed encounters. Most of the fleet sits at zero risk (pre-filtered out).

**Key insight (matrix):** Off-diagonal cells reveal flag-of-convenience patterns: vessels flagged to Panama or Vanuatu but porting in Peru or China. The diagonal is normal (flag = port state); everything off-diagonal warrants investigation.

**Filter:** Risk score minimum filter (exclude zero-risk vessels). Year filter.

**Transition → next:** "The most dramatic form of evasion: vessels turning off their tracking entirely."

---

### Story Point 5: "Going Dark: Where Vessels Disappear"

**Dashboard 4**

| Position | Sheet | Data Source |
|----------|-------|-------------|
| Left 55% | Sheet 11: Disabling Map (Enriched) | `disabling_enriched` |
| Top-right 15% | Sheet 12: Disabling by Flag + Risk | `disabling_enriched` |
| Mid-right 15% | Sheet 13: Distance from Shore | `disabling_enriched` |
| Bottom-right 15% | Sheet 14: Disabling Seasonality | `disabling_enriched` |

**Caption:** "55,000 times vessels turned off their AIS tracking (2017–2019)"

**Key insight (map):** Disabling clusters at EEZ boundaries: Argentine shelf, West Africa, Northwest Pacific. Clean zones (Australia, Northern Europe, US East Coast) correlate with strong enforcement.

**Key insight (histogram):** Most disabling happens 100–400 km from shore, beyond coast guard patrol range.

**Key insight (seasonality):** Peaks align with high-value species migration seasons.

**Temporal note for narration:** These events are from 2017–2019 (Welch et al. dataset). For 2020–2024 disabling analysis, we use the vessel-level `disabling_over_12_hours` column from the IUU Risk dataset shown in Dashboard 3.

**Filter:** Severity filter + risk tier filter. Click flag in bar chart → map highlights.

**Transition → next:** "Can we investigate an individual vessel?"

---

### Story Point 6: "Vessel Investigation"

**Dashboard 5**

| Position | Sheet | Data Source |
|----------|-------|-------------|
| Top 10% | MMSI parameter input | (parameter control) |
| Middle-left 30% | Sheet 15: Vessel Risk Profile | `iuu_risk_cleaned` |
| Middle-right 30% | Sheet 16: Vessel Activity Timeline | `iuu_risk_cleaned` |
| Bottom 30% | Sheet 21: Vessel Activity Gantt | `iuu_risk_cleaned` |

**Caption:** "Enter an MMSI to see a vessel's full behavioural history"

**How to demo:** Pre-load the parameter with the highest-risk MMSI from the 2024 data. The heatmap shows which years had the most disabling/encounters, the timeline shows hours at sea, the Gantt shows year-by-year activity breakdown.

**Suggested demo vessel:** Find in `iuu_risk_cleaned.csv` the vessel with the highest `risk_score` in 2024. Note its MMSI, flag, name, top port.

**Transition → next:** "Zooming out: how do all these countries compare, and is the situation improving?"

---

### Story Point 7: "The Bigger Picture: Countries Over Time"

**Dashboard 6**

| Position | Sheet | Data Source |
|----------|-------|-------------|
| Top 50% | Sheet 17: Fishing vs Risk Bubble | `country_summary` |
| Bottom 50% | Sheet 18: Risk Trend by Country | `country_summary` |

**Caption:** "How risk profiles evolve across nations and years"

**Key insight (bubble):** China is the largest bubble and sits high on the risk axis. European nations cluster low-left (small fleets, low risk). Panama is interesting: moderate fleet size but elevated risk.

**Key insight (small multiples):** Some nations show improving trends (declining risk score). Others are flat or worsening.

**Interactivity:** Year on Pages shelf for the bubble chart → play button animates across 2020–2024.

**Transition → next:** "Do our findings hold up against independent assessments?"

---

### Story Point 8: "External Validation"

**Dashboard 7**

| Position | Sheet | Data Source |
|----------|-------|-------------|
| Top-left 40% | Sheet 22: IUU Index Validation Scatter | `country_summary` + `iuu_fishing_index` |
| Top-right 40% | Sheet 23: IUU Index vs Disabling Rate | `country_summary` + `iuu_fishing_index` |
| Bottom 20% | Sheet 24: GDELT News Volume (or text annotation) | `gdelt_iuu_news_clean` |

**Caption:** "Do our risk scores match the experts and the media?"

**Key insight (left scatter):** If the trend line is positive with reasonable R², our GFW-derived composite risk score aligns with the independently published IUU Fishing Index. Outliers are countries the Index flags but our data doesn't (or vice versa), interesting in either direction.

**Key insight (right scatter):** Tests whether the IUU Index predicts disabling behaviour specifically.

**Key insight (bottom):** GDELT news volume shows IUU coverage increasing over 2020–2024, but may be geographically biased toward Western/English sources.

**If GDELT data is not ready:** Replace Sheet 24 with a text box summarising the intended analysis and noting it as future work.

**Transition → next (optional final point):** "Behind the data are real people."

---

### Story Point 9 (Optional): "Voices from the Fleet"

**Dashboard 8**

| Position | Sheet | Data Source |
|----------|-------|-------------|
| Top-left | EJF Word Cloud (packed bubbles) | `ejf_word_freq` |
| Top-right | EJF Bigram Bar Chart | `ejf_bigram_freq` |
| Middle | Testimony Themes by Flag State | `ejf_testimonies` |
| Bottom-left | Sentiment by Flag | `ejf_testimonies` |
| Bottom-right | Testimonies by Year | `ejf_testimonies` |

**Caption:** "What 430 fishers told EJF about life on distant-water vessels"

**Key insight:** Chinese-flagged vessels dominate violence mentions. The most common bigrams are "high seas", "forced labour", "distant water". This qualitative layer gives human context to the quantitative risk indicators.

**Closing narration:** "The AIS data shows us where vessels go and what they do. The risk indicators tell us who is suspicious. The news tells us what the world knows. And the testimonies tell us what the fishers experienced. Together, these four layers make the invisible visible."

---

## Dashboard Action Wiring (Summary)

Set these up in each dashboard via **Dashboard → Actions**.

| Dashboard | Action Type | Source Sheet | Target Sheet | Trigger | Field |
|-----------|-------------|--------------|--------------|---------|-------|
| 1 | Filter | Global Fishing Map | Top Nations + Trend | Select | (lat, lon region) |
| 2 | Filter | Fleet Composition | Treemap + Scatter | Select | flag_clean |
| 3 | Highlight | Risk Scatter | Risk Heatmap | Hover | flag |
| 3 | Highlight | Flag vs Port Matrix | Risk Scatter | Select | flag |
| 4 | Filter | Disabling by Flag | Disabling Map | Select | flag |
| 4 | Highlight | Disabling Map | Disabling by Flag | Hover | flag |
| 5 | (Parameter) | MMSI input | All 3 sheets | Type | Selected MMSI |
| 6 | Filter | Bubble Chart | Risk Trend | Select | flag |
| 7 | Highlight | IUU Index Scatter | IUU vs Disabling | Hover | flag |

---

## Colour Semantics (Consistent Across All Dashboards)

| Meaning | Hex | Usage |
|---------|-----|-------|
| Fishing activity (neutral) | `#4fc3f7` | Bars, lines, areas for fishing hours |
| High risk / danger | `#ff4444` | High risk tier, 72h+ disabling, violence theme |
| Medium risk / warning | `#ffaa00` | Medium risk tier, 24–48h disabling |
| Low risk | `#66bb6a` | Low risk tier, good performers |
| No data / baseline | `#78909c` | Zero risk, unknown flags |
| Map background | `#112240` | Dark theme base |
| Text on dark | `#e0e0e0` | All labels and titles |

---

## Presentation Tips

1. **Start with the map.** Everyone understands a world map. Let the audience orient before introducing risk metrics.
2. **Use the COVID dip** as a timestamp anchor. "See this dip in 2020? That's when the world locked down. Watch what happens after."
3. **Demo one vessel live.** Type an MMSI into Dashboard 5 during the presentation. Pick one with a dramatic risk profile in advance.
4. **End with a quote.** Pull one EJF testimony and read it aloud over Dashboard 8. The shift from data to human voice is the strongest way to close.
5. **Keep each story point to 2 minutes.** 8 points × 2 min = 16 minutes. That leaves room for Q&A in a 20-minute slot.

---

## File Checklist for Final Submission

| File | Location | Status |
|------|----------|--------|
| `GFW_IUU_Fishing_final.twbx` | `tableau/final/` | Build from this guide |
| `proposal.tex` + `sample-base.bib` | `tableau/final/` | Updated with feedback |
| `attachments/*.png` | `tableau/final/attachments/` | Figures for the report |
| `TABLEAU_BUILD.md` | `tableau/final/` | Sheet-by-sheet build instructions |
| `STORY_FLOW.md` | `tableau/final/` | This file |
| `iuu_fishing_index.csv` | `datasets/` | External validation data |
| `ejf_*.csv` | `text/EJF/` | Fisher testimony data |
| `gdelt_iuu_news_clean.csv` | `text/GDELT/` | News data (when complete) |

---

*Build the dashboards first, then assemble the Story in narrative order. The Story is what you present; the dashboards are what the audience explores afterward.*
