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

---

### Story Point 0 (Prologue): "How the World Learned to Worry About Fishing"

**Format:** Static image or embedded chart (not a Tableau dashboard). Use `google_ngram_all_terms.png` or `google_ngram_iuu_focus.png` as a floating image on a blank story point, with text overlay.

**Image:** `attachments/google_ngram_all_terms.png` (3-panel faceted chart)

**What it shows:** Google Books Ngram frequency (1970–2019) of 9 fishing-related terms across published literature: books, academic papers, policy documents. Three panels separate the terms by scale and function.

**Panel A — Industry & Policy Terms:**
- "Aquaculture" dominates at 3+ ppm, peaking around 1995 then gradually declining. This reflects the 1980s–90s boom in fish farming research, when aquaculture was positioned as the solution to overfishing. The post-2000 decline doesn't mean aquaculture shrank; it means the literature moved from establishing the concept to assuming it.
- "Fisheries management" holds steady at ~0.5 ppm across the entire period, a backbone term in the literature.
- "Marine conservation" remains very low throughout, suggesting the conservation framing came later and never dominated the fisheries discourse.

**Panel B — Problem Recognition:**
- "Overfishing" and "bycatch" both peak sharply around 1996, aligning with the UN Fish Stocks Agreement (1995) and the FAO Code of Conduct for Responsible Fisheries. This was the era when the scale of the problem entered mainstream scientific consciousness.
- "Fish stocks" follows a similar trajectory but peaks slightly later (~1997), reflecting the stock-assessment science that followed the alarm.
- All three decline after 2000, not because the problems were solved, but because the discourse shifted from documenting the problem to debating responses.

**Panel C — IUU & Enforcement Terms:**
- "IUU fishing" barely existed in literature before 2001, then rose steadily after the FAO International Plan of Action on IUU Fishing (IPOA-IUU) was adopted that year. It peaks around 2004–2005 and plateaus.
- "Illegal fishing" follows a similar but slightly earlier curve, peaking around 2005.
- "Forced labour" (in the fishing context) is a declining legacy term with a different meaning in earlier decades. Its presence here is an artifact; the modern forced-labour-at-sea discourse is primarily post-2015 and lives in reports/news rather than books.
- Key policy milestones annotated: UN Fish Stocks Agreement (1995), FAO IPOA-IUU (2001), EU IUU Regulation (2009), Port State Measures Agreement entering force (2016).

**The narrative point:** IUU fishing is a concept that barely existed 25 years ago. The policy framework is young. The data we're about to show you covers a period (2020–2024) where the tools to detect IUU behaviour have only just become available at scale. We're looking at a problem the world has only recently learned to measure.

**Companion image (optional):** `google_ngram_iuu_focus.png` — a single-panel version with era shading (Discovery → Alarm → Action) that works well as a presentation opener. The shaded eras tell the story visually: the world spent 1970–1992 discovering the problem, 1992–2005 raising the alarm, and 2005–present building the response. Our project sits in the "Era of Action" — using the data tools that era produced.

**Transition → next:** "That's the literature. Now let's look at what's actually happening on the water."

---

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
| Bottom 20% | Sheet 24: GDELT News Volume | `gdelt_enriched` or `gdelt_monthly_by_query` |

**Caption:** "Do our risk scores match the experts and the media?"

**Key insight (left scatter):** If the trend line is positive with reasonable R², our GFW-derived composite risk score aligns with the independently published IUU Fishing Index (Poseidon/GI-TOC, 2025 edition — 152 coastal states scored 1–5). China confirmed as the highest-risk country at 3.60; Romania the lowest at 1.46. Outliers where the Index flags a country but our data doesn't (or vice versa) are analytically interesting — they may reflect enforcement gaps or data coverage differences.

**Key insight (right scatter):** Tests whether the IUU Index predicts AIS disabling behaviour specifically. A country with a high IUU Index score that also shows high disabling rates provides strong cross-validation. Countries with high IUU scores but low disabling may use other evasion methods (reflagging, transshipment) not captured by AIS gaps alone.

**Key insight (GDELT bottom panel):** The GDELT news corpus (1,539 articles, 2020–2024) provides a media-attention layer:

- *News volume by query group:* `iuu_fishing` queries dominate (905 articles), with visible spikes in late 2022 and late 2024 corresponding to WTO fisheries subsidies negotiations and major enforcement operations. `dark_fleet` barely registers (8 articles), confirming AIS disabling is a specialist topic that rarely reaches mainstream coverage.
- *Topic prevalence by year:* 2022 was the peak year for China-related IUU coverage (~140 articles), likely driven by the WTO fisheries subsidies debate and high-profile enforcement actions. IUU and enforcement coverage is more stable across years, suggesting a steady baseline of reporting rather than event-driven spikes.
- *China mention share:* Spiked to 31.2% of all IUU articles in 2022, then dropped to 5.1% by 2024. The decline doesn't indicate improvement — it indicates media attention shifted elsewhere. This is itself an insight: news coverage is a lagging, attention-driven indicator, not a real-time risk measure.
- *Topic co-occurrence:* "Seized" and "enforcement" correlate moderately (seizures are enforcement outcomes). "China" and "labor" show weak negative correlation, suggesting articles about China focus on fleet behaviour, while forced-labour coverage focuses on non-China contexts. "AIS" topics correlate loosely with everything — a niche cross-cutting term.
- *Precision caveat:* Title-level keyword matching produces false positives. A precision check sample (`gdelt_precision_check.csv`, 132 articles) is provided for hand-labelling. Reported precision should be included in the final report methodology.

**If presenting:** Show the GDELT news volume chart and note: "The world's attention to IUU fishing is growing, but it's uneven — dominated by English-language Western sources, and spiking around policy events rather than tracking actual risk geography. The news tells us what the world knows. Our AIS data tells us what's actually happening."

**Transition → next:** "Behind the data are real people."

---

### Story Point 9: "Voices from the Fleet"

**Dashboard 8**

| Position | Sheet | Data Source |
|----------|-------|-------------|
| Top-left | EJF Word Cloud (packed bubbles) | `ejf_word_freq` |
| Top-right | EJF Bigram Bar Chart | `ejf_bigram_freq` |
| Middle | Testimony Themes by Flag State | `ejf_testimonies` |
| Bottom-left | Sentiment by Flag | `ejf_testimonies` |
| Bottom-right | Testimonies by Year | `ejf_testimonies` |

**Caption:** "What 430 fishers told EJF about life on distant-water vessels"

**Chart-by-chart insights:**

**EJF Word Cloud / Top Bigrams:** "High seas" (141) and "jumbo squid" (134) anchor the domain context. "Chinese flagged" (93) and "forced labour" (91) are the 4th and 5th most common bigrams, confirming these two concepts are central to the EJF narrative. "Indonesian fisher" and "interview Indonesian" appearing in the top 25 reflects that the interviewees are predominantly Indonesian crew working on foreign-flagged vessels — they are the workers, not the operators. "Southwest Atlantic" and "Indian Ocean" locate the geographic focus. The colour coding separates abuse terms (red: forced labour, rights abuses, destructive fishing), IUU terms (orange: IUU fishing), and neutral domain terms (blue: high seas, squid fishing, fishing vessels).

**Themes by Flag State:** Chinese-flagged vessels lead every theme category (56 of 65 flagged testimonies). Wildlife is the dominant theme (24 mentions), likely reflecting shark finning and bycatch descriptions. Death (14) and violence (12) are both substantial. Conditions (14) and transshipment (9) complete the picture. Korean-flagged vessels appear disproportionately in violence and conditions relative to their small sample (4 testimonies, 2+ theme mentions each), suggesting concentrated severity. Taiwanese vessels appear mostly in wildlife and violence. Wages is comparatively low across all flags, suggesting the abuse described is more physical than financial.

**Sentiment Scatter:** Almost every testimony sits below zero (negative sentiment), as expected for abuse accounts. The main cluster (0–500 words, -5 to 0 sentiment) represents individual interview excerpts. Longer quotes that dip further negative (-3 to -5) are the more detailed, emotionally charged accounts. Bubble size (negative word count) makes the most disturbing testimonies visually prominent. Note: testimonies over 500 words are filtered out as they are likely entire report sections extracted as single quotes rather than individual statements.

**Testimonies by Year:** Chinese-flagged vessels dominate every year, ramping sharply from 2021 onward and peaking at ~19 in 2025. Taiwanese and Korean vessels only appear from 2023–2025, suggesting EJF expanded its investigation scope in recent cycles. The pre-2021 period (1–2 testimonies per year) is thin. Important caveat for narration: the growth reflects EJF's investigation intensity, not necessarily worsening conditions. But the consistency of themes across years suggests the conditions are structural, not episodic.

**The narrative point:** The AIS data shows us where vessels go and what they do. The risk indicators tell us who is suspicious. The news tells us what the world knows. And the testimonies tell us what the fishers experienced. Together, these four layers make the invisible visible. The shift from quantitative dashboards to human testimony is the strongest close to the presentation.

**Closing narration (to read aloud):** Pick one quote from `ejf_testimonies.csv` — suggested: *"When we refused to fish, we got scolded and physically abused. We were kicked and hit."* (Indonesian fisher, Chinese-flagged vessel, 2022). Read it over the dashboard. Then: "This is what the data looks like from the deck of a squid jigger."

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

1. **Open with the Ngram chart.** Show the 50-year arc of IUU as a concept before any AIS data. "This problem barely had a name 25 years ago."
2. **Then go to the map.** Everyone understands a world map. Let the audience orient before introducing risk metrics.
3. **Use the COVID dip** as a timestamp anchor. "See this dip in 2020? That's when the world locked down. Watch what happens after."
4. **Demo one vessel live.** Type an MMSI into Dashboard 5 during the presentation. Pick one with a dramatic risk profile in advance.
5. **Bridge with the news.** "The experts agree with our data [IUU Index scatter]. The media is paying attention [GDELT chart]. But the coverage is uneven and attention-driven."
6. **End with a quote.** Pull one EJF testimony and read it aloud over Dashboard 8. The shift from data to human voice is the strongest way to close.
7. **Keep each story point to 90 seconds.** 10 points × 90s = 15 minutes. That leaves room for Q&A in a 20-minute slot.

---

## File Checklist for Final Submission

| File | Location | Status |
|------|----------|--------|
| `GFW_IUU_Fishing_final.twbx` | `tableau/final/` | Build from this guide |
| `proposal.tex` + `sample-base.bib` | `tableau/final/` | Updated with feedback |
| **Attachments (charts)** | `tableau/final/attachments/` | |
| `google_ngram_all_terms.png` | attachments/ | 3-panel Ngram faceted chart |
| `google_ngram_iuu_focus.png` | attachments/ | Single-panel IUU focus with era shading |
| `gdelt_news_volume.png` | attachments/ | GDELT article volume over time |
| `gdelt_topics_by_year.png` | attachments/ | Topic prevalence grouped bars |
| `gdelt_china_and_cooccurrence.png` | attachments/ | China mention trend + correlation matrix |
| `ejf_themes_by_flag.png` | attachments/ | Testimony themes by vessel flag |
| `ejf_top_bigrams.png` | attachments/ | Top 25 bigrams colour-coded |
| `ejf_sentiment_scatter.png` | attachments/ | Sentiment vs quote length |
| `ejf_testimonies_by_year.png` | attachments/ | Testimonies over time by flag |
| `AIS Disabling Map.png` | attachments/ | Tableau AIS disabling map export |
| `Fleet Composition by Country.png` | attachments/ | Tableau fleet composition export |
| `Monthly Fishing Trend.png` | attachments/ | Tableau monthly trend export |
| **Tableau-ready CSVs** | `tableau/final/data/` | |
| `gdelt_enriched.csv` | data/ | 1,539 articles with domain + source country |
| `gdelt_monthly_by_query.csv` | data/ | Monthly article counts by query group |
| `gdelt_yearly_topics.csv` | data/ | Yearly topic flag aggregates |
| `gdelt_title_word_freq.csv` | data/ | Top 200 words from GDELT titles |
| `gdelt_precision_check.csv` | data/ | 132 articles sampled for hand-labelling |
| `google_ngram_iuu.csv` | data/ | 9 terms × 70 years (1950–2019) |
| `ejf_testimonies.csv` | data/ | 111 fisher testimonies with themes |
| `ejf_word_freq.csv` | data/ | 500 word frequencies |
| `ejf_bigram_freq.csv` | data/ | 300 bigram frequencies |
| `iuu_fishing_index.csv` | data/ | 70 country IUU Index scores |
| **Build guides** | `tableau/final/` | |
| `TABLEAU_BUILD.md` | tableau/final/ | Sheet-by-sheet build instructions |
| `STORY_FLOW.md` | tableau/final/ | This file |
| `text_viz.ipynb` | tableau/final/ | Jupyter notebook (generates all above) |
| `run_text_viz.py` | tableau/final/ | Script version of the notebook |

---

*Build the dashboards first, then assemble the Story in narrative order. The Story is what you present; the dashboards are what the audience explores afterward.*
