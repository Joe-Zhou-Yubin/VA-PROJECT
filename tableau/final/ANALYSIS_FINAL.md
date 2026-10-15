# Final website analysis and dashboard guide

Final structure agreed on 15 October 2026: **six website analyses, five dashboards, and three standalone worksheets**. This file is the current analysis plan and supersedes conflicting allocations in WEBSITE_STORYBOARD.md and DASHBOARD_RECOMMENDATION.md.

A standalone worksheet is embedded directly within the relevant analysis section. It does not require another dashboard or another numbered analysis. Retain the existing native EJF word showcase.

## The story and reading order

**Where fishing happens -> which fleets operate -> how country risks differ -> what an individual vessel's history shows -> what external evidence adds -> what people experienced.**

| Analysis | Website title | Views in reading order |
|---|---|---|
| 01 | Where Does the World Fish? | Dashboard 1: global map with its existing year-comparison mode |
| 02 | Fleet DNA: How the Top 20 Flag States Fish | Dashboard 2: ranking, gear composition, monthly trend |
| 03 | Country Risk Patterns | Dashboard 3, then standalone Risk Tier Distribution |
| 04 | Going Dark: From Offshore Patterns to a Vessel | Standalone Disabling Distance from Shore, then Dashboard 4 |
| 05 | External Assessments and World News | Dashboard 5: external Index comparison, then retrieved news |
| 06 | Voices from the Fleet | Existing word showcase, then standalone Testimony Themes by Flag State |

The Problem, What we found, and Why it matters paragraphs below are draft website copy. Numerical findings refer to the supplied workbook's packaged data and the stated period; they do not automatically update when readers change filters. Label them as reference findings or update the text to match a saved view. Dashboard interactions still require testing in the final workbook.

## Shared presentation rules

- Use one dashboard title, short chart titles, and readable legends. Worksheet tab names can stay unchanged.
- Keep the existing right-hand control panels. Do not rearrange them solely for consistency with an older guide.
- Use plain labels: Flag state, Fishing hours, Assessed vessels, Event year, and Gap duration. A flag state is a registration country, not necessarily an owner, fishing location, or crew nationality.
- No dashboard footers are required. Put source coverage and methodology in the website text or a shared methodology section.
- Risk indicators support investigation; they do not establish illegal fishing. Unknown information is not an assessed zero-risk result.
- Preview at the actual website embed width. Use additional height rather than shrinking labels. Remove horizontal scrolling, clipped titles, and ### numerical labels wherever possible.
- The country group for Analyses 2 and 3 should be the same Top 20 flag states by fishing hours for the chosen ranking year, with identical exclusions. Selections for detail are subsets of that group. Do not rank each risk chart independently using another metric.
- Start country comparisons at 2024. A country missing risk data remains a documented gap; do not silently substitute a different country. This matching of country lists is a remaining setup check, not something confirmed by screenshots.
- Separate embedded views do not automatically share selections. A standalone sheet's country group and period must be configured explicitly. EJF and event data retain their own appropriate populations.

---

## Analysis 01 - Where Does the World Fish?

### Views

**Dashboard title:** Where Does the World Fish?

| Existing worksheet | Role |
|---|---|
| Global Fishing Effort Map | Location and intensity of observed fishing over the selected period |
| Fishing Effort by Year (Small Multiples) | Comparison of spatial patterns between years |

### Dashboard instructions

1. Keep the existing Fishing Map View dropdown: Selected period / Compare years. Show one map view at a time, using the full map area.
2. Keep the Year range slider for the selected-period map. Label it **Fishing period**. Several selected years combine their fishing hours.
3. Keep 2020-2024 visible in the comparison mode; the selected-period slider must not restrict it.
4. Use small marks and save a full-world extent. Keep raw fishing hours in tooltips.
5. Check that map colour uses `LOG(1 + SUM([fishing_hours]), 10)`, not a sum of precomputed logarithms. Use a common colour scale across the comparison year panes.

**Reader instruction:** Choose a fishing period, or switch to Compare years to explore changes in the same locations.

**Check:** both modes fill the available area; comparison panes are readable; the period slider affects only the selected-period map.

### The Problem

Fishing takes place across a vast ocean, but its distribution is uneven. Before examining risk, we need to understand where observed activity is concentrated and whether those concentrations change over time.

### What we found

The map shows dense concentrations of observed fishing around several coastal and offshore regions, including waters around East and Southeast Asia and Europe. The yearly comparison allows readers to distinguish recurring concentrations from changes between 2020 and 2024. These are patterns in the observed dataset, rather than a complete census of all fishing.

### Why it matters

This establishes the geographic context for monitoring. A fishing hotspot indicates activity and exposure; it does not by itself indicate illegal fishing.

**Transition:** Where activity occurs is only the beginning. Which fleets account for it, and how do they fish?

---

## Analysis 02 - Fleet DNA: How the Top 20 Flag States Fish

### Views

**Dashboard title:** Fleet DNA: How the Top 20 Flag States Fish

| Existing worksheet | Displayed chart title | Position |
|---|---|---|
| Top 20 Fishing Nations | Top 20 Flag States by Fishing Hours | Upper left |
| Fleet Composition by Country | Gear Composition by Flag State | Upper right |
| Monthly Fishing Trend | Monthly Fishing Trend | Full width below |

### Dashboard instructions

1. Show the same 20 flag states in both upper charts, ordered by fishing hours. Allow enough height to keep their rows readable and aligned.
2. Label the existing Year control **Ranking year**. Apply it to the two upper charts only. Keep monthly history at 2020-2024.
3. Restore all countries within the Top 20 restriction, then hide the visible country checkbox card. Keep the underlying Top 20 set/filter active.
4. Configure a Select filter action from the ranking to Monthly Fishing Trend, matching Flag Clean only. Allow multiple selections. On clearing, exclude all values and retain the instruction text.
5. Configure a Select highlight action from the ranking to Fleet Composition, matching Flag Clean only.
6. Keep gear colours consistent and replace underscored labels with readable aliases. Verify what the generic fishing category means before renaming it.
7. Identify selected flags in the trend title or legend. Remove overlapping event annotations; discuss sourced historical context in the website prose without implying causation.

**Reader instruction:** Click a flag state to view its monthly trend. Ctrl+click to compare several.

**Check:** a click filters the trend and highlights the matching gear bar while the ranking retains all 20. Ranking year changes the upper charts, not the history period.

### The Problem

Similar levels of fishing activity can arise from very different fleet structures. Country totals alone conceal differences in fishing gear, seasonality, and changes over time.

### What we found

In the supplied 2024 extract, Chinese-flagged vessels account for approximately 52.4 million fishing hours, compared with 6.9 million for Vietnam and 5.4 million for South Korea. Gear composition also differs: trawlers account for approximately 60.4% of Chinese-flagged fishing hours, while drifting longlines account for approximately 55.8% of Taiwanese-flagged hours. The monthly view lets readers inspect how selected fleets' activity changes across 2020-2024.

### Why it matters

Fleet scale and fishing methods provide context for interpreting risk. A large fleet may accumulate more events simply because it operates more extensively; monitoring priorities should consider those differences.

**Transition:** Fishing volume describes activity. The next analysis asks whether country risk patterns follow the same ordering.

---

## Analysis 03 - Country Risk Patterns

### Views

**Dashboard title:** Country Risk Patterns

| Existing worksheet | Purpose |
|---|---|
| Fishing vs Risk Bubble | Compare fishing activity with average assessed-vessel risk |
| Risk Indicator Heatmap | Compare individual recorded indicators across flag states |
| Risk Trend by Country | Examine country risk histories |
| Flag-vs-Port-State | Examine recorded flag-state and top-port-state associations |

**Standalone after the dashboard:** Risk Tier Distribution.

The standalone chart shows the proportions of assessed vessels in each tier over 2020-2024. It complements the country averages; it is not a separate vessel-indicator dashboard.

### Dashboard and standalone instructions

1. Keep these four existing dashboard sheets. Give the heatmap and port matrix full-width rows if the current layout clips their labels. The bubble and trends may occupy the upper row.
2. Keep the existing Year filter for country snapshots. Apply it to the bubble and heatmap. Keep risk history at 2020-2024. Explicitly match the port matrix's year because it uses a different source.
3. Use the agreed country group consistently. Within that group, bubble selections can filter the heatmap, history, and port matrix through Flag-to-Flag mappings. Do not pass Year in this action.
4. Use AVG of the country average-risk field. Label the bubble size **Assessed vessels**. Investigate the visible negative-value indicator before using a logarithmic axis; do not silently hide an unexplained record.
5. For the current heatmap's mixed counts and hours, use separate legends/scales per measure and retain exact values in tooltips. Colours compare countries within each column, not equivalent severity across columns.
6. Use one colour for trend lines and a common vertical scale across country panes. Remove disabling-event totals from line colour.
7. Replace ### in the port matrix with readable abbreviated counts or tooltip-only values. Keep its numerical meaning explicit: distinct assessed MMSIs with that recorded association.
8. For standalone Risk Tier Distribution, use the same country group and assessed-vessel population. Each year's stacked bar totals 100%; include all risk tiers, including None. Explain None as no recorded scored indicators, not confirmed safe.

**Reader instruction:** Select country bubbles to compare their indicators and histories. Then inspect the risk-tier distribution to see what the averages conceal.

**Check:** the country group is consistent, snapshot years match, history retains all five years, and no chart quietly switches between fishing-only and all-assessed populations.

### The Problem

A country with more fishing activity does not necessarily have the highest average risk. Country averages can also hide the number of vessels with elevated indicators and the kinds of behaviour contributing to those scores.

### What we found

The supplied 2024 country summary illustrates this distinction. China has an average assessed-vessel risk score of 0.585, compared with 1.238 for Taiwan and 1.213 for Spain, despite China's much larger fishing total. The same summary records 115 high-risk vessels for China, 101 for Taiwan, and 50 for Spain, across very different assessed-vessel populations. Read these counts alongside averages and tier proportions rather than treating any single measure as a complete ranking.

These figures refer to the current country-summary population, which includes non-fishing vessels. They must not be described as fishing-only statistics unless the aggregates are rebuilt accordingly.

### Why it matters

Combining scale, indicator types, history, and tier proportions gives a more defensible basis for prioritizing investigation. Flag/port differences provide operational context but do not, by themselves, prove ownership concealment or misconduct.

**Transition:** Country-level patterns narrow the questions. The next analysis follows tracking gaps from an offshore distribution to an individual vessel's history.

---

## Analysis 04 - Going Dark: From Offshore Patterns to a Vessel

### Views

**First:** standalone Disabling Distance from Shore.

**Then dashboard title:** Going Dark: A Vessel Deep Dive.

| Existing worksheet | Position and purpose |
|---|---|
| AIS Disabling Map | Full-width upper map; select a recorded event |
| Vessel Risk Profile | Below map; inspect the selected MMSI's recorded indicators |
| Vessel Activity Timeline | Beside or below profile; inspect its available history |

### Dashboard and standalone instructions

1. Present the histogram first, with the axis labelled **Gap-start distance from shore (km)**. Describe it as the distribution of recorded events in this extract.
2. Keep event filters on the map only: Event year, Flag state, and Gap duration. The disabling extract covers 2017-2019. Do not apply this event period to vessel history.
3. Use small map symbols so extreme gap durations do not obscure other events. Review the largest durations before interpreting them; keep exact duration in tooltips.
4. Place Selected MMSI directly above the lower charts and display the vessel identity in their titles.
5. Use a Select parameter action from AIS Disabling Map to Selected MMSI. Source field: MMSI Text, with no aggregation; keep the current value on clearing. MMSI Text must be on Detail in the map and match the parameter's text type.
6. Preserve the existing selected-MMSI filters in the profile and timeline. Retain their available historical years.
7. Widen indicator labels, use integer formatting for event counts, and distinguish hours from counts. Use separate heatmap row scales where units differ. Keep the timeline's hours and voyages axes separately labelled.
8. The standalone histogram and dashboard are separate embeds; their selections do not synchronize automatically. Give the histogram an explicit reference period.

**Reader instruction:** Explore the offshore distribution, then click one event on the map to inspect that vessel's profile and history.

**Check:** changing gap duration actually changes map events; clicking an event changes Selected MMSI and both lower charts; event filters do not truncate vessel history. No matching profile means unavailable matching data, not no risk.

### The Problem

Tracking gaps reduce visibility into vessel movements. Their location and duration can identify questions for investigation, but a gap alone does not reveal why tracking stopped or what happened during it.

### What we found

The supplied 2017-2019 extract contains 55,368 distinct events associated with 5,269 MMSIs. Median event duration is approximately 23.5 hours, and median gap-start distance from shore is approximately 413 km. These describe the full extract, not a filtered map selection. The map-to-profile interaction then reveals which recorded indicators and activity years are available for an individual vessel.

The source excludes near-shore gaps under its selection criteria. This offshore distribution is therefore not representative of every tracking gap, and distance from shore is not distance from an EEZ boundary.

### Why it matters

An individual vessel's history helps turn a broad geographic pattern into a specific, traceable investigation. Temporal matching matters: later risk information should not be presented as proof of what happened during an earlier event.

**Transition:** Internal indicators suggest where to look. External assessments and reporting help examine how those signals fit a wider picture.

---

## Analysis 05 - External Assessments and World News

### Views

**Dashboard title:** External Assessments and World News.

| Existing worksheet | Displayed title | Position |
|---|---|---|
| IUU Index Validation | Country Risk Compared with the 2025 IUU Fishing Index | Full-width upper chart |
| IUU News Volume Over Time | Retrieved IUU-Related News Over Time | Full-width lower chart |

### Dashboard instructions

1. Keep one shared **Year** control, limited to 2020-2024. Use a single-year dropdown, default 2024, to avoid mixing annual risk summaries without an explicit aggregation method.
2. Map Year between country_summary and gdelt_iuu_news_clean through the existing cross-source filter setup. Apply the filter to these two sheets only. Keep the country-code mapping to the external Index unchanged.
3. Keep the Index year fixed and labelled as 2025. The shared filter changes AIS risk and retrieved-news years, not the Index edition.
4. Keep monthly detail in the news chart, using the actual date field as a continuous monthly axis. Prefer bars to lines across sparse retrieved months. Missing collection months are not observed zeros.
5. Label the scatter's risk axis **Average vessel risk score** and any reference/trend line by its actual meaning. Keep sample size and the assessed-vessel population visible in tooltips.
6. Clean up news-query names and keep their legend near the news chart. Query categories describe the retrieval process; they are not a validated classification of offences.
7. Do not add a country-to-news action: the current news extract has no reliable country/vessel link for that purpose.

**Reader instruction:** Choose a year to compare its AIS-derived country risk and retrieved news. The external country assessment remains the 2025 Index.

**Check:** selecting 2024 removes records from other years in both charts. In particular, verify that January 2025 news records do not remain. Country joins, missing matches, and any minimum-sample rule must be checked before reporting correlations.

### The Problem

A behavioural risk score is one perspective, not an independent determination of illegality. External country assessments and public reporting provide additional context, but their scope and coverage differ from vessel tracking data.

### What we found

The dashboard compares annual AIS-derived country risk with a fixed 2025 external assessment; the two measures describe different populations and concepts. A quantified agreement result has not yet been validated for the final displayed sample, so this comparison should not be presented as proof that the risk score is accurate.

The supplied news extract contains 1,534 distinct retrieved URLs dated within 2020-2024. Coverage is concentrated in selected months, with gaps between retrieval periods. It therefore shows the captured reporting rather than a complete annual measure of worldwide IUU news attention.

### Why it matters

External comparison can reveal agreement, disagreement, and questions about measurement. News provides context, but sparse coverage cannot establish annual growth in media attention or identify geographic monitoring blind spots without additional data.

**Transition:** Scores and headlines still do not tell us what people experienced aboard vessels. The final analysis adds those human accounts.

---

## Analysis 06 - Voices from the Fleet

### Views

**No new dashboard.**

1. Retain the existing native website word showcase representing EJF Word Count.
2. Embed the existing standalone **Testimony Themes by Flag State** worksheet.

**Displayed chart title:** Themes in EJF Passages by Vessel Flag.

### Standalone instructions

1. Keep readable theme names and label the numerical axis **Extracted passages mentioning a theme**.
2. Retain all available flag groups, including Unknown. Do not apply the fishing Top 20 group to this different sample.
3. Use the same count scale across flag panes. Keep sample sizes available in tooltips or website text.
4. If showing a Vessel Flag filter, apply it only to this worksheet and start with all groups selected. No dashboard actions are required.
5. Keep word frequency distinct from testimony themes: report vocabulary is not a count of respondents or incidents. Do not embed a duplicate EJF Word Count treemap.
6. Verify any displayed quotation against its original report and provide its report/page reference in the website text.

**Reader instruction:** Explore recurring report vocabulary, then compare themes in the extracted passages while checking each flag group's sample size.

**Check:** Unknown remains visible; counts refer to passages; the chart does not claim to represent 430 independently coded respondents.

### The Problem

Tracking data cannot directly describe working conditions, violence, pay, or other experiences aboard vessels. Understanding fishing risk also requires evidence from people and reports, with careful attention to how that evidence was collected.

### What we found

The supplied extraction contains 111 passages: 56 assigned to Chinese vessel flags, 5 Taiwanese, 4 Korean, and 46 with unknown flags. Its existing theme coding marks wildlife in 40 passages, conditions in 26, death in 24, violence in 19, transshipment in 13, and wages in 11. A passage can have more than one theme. These are counts from the extracted and coded sample, not independently verified incident totals or national prevalence estimates.

### Why it matters

These passages add human and environmental context that vessel tracks cannot establish. Their uneven sampling means the analysis should illuminate reported experiences rather than rank national fleets by abuse rates.

**Closing message:** Use the application to identify patterns, compare evidence, and ask better investigative questions. None of the individual views alone determines that a vessel or country has committed an offence.

---

## Final publishing checklist

- Five dashboard views and three standalone worksheet views: **eight Tableau embeds across six website analyses**. The native word showcase is additional website content, not another Tableau embed.
- No separate Vessel Risk Indicators dashboard and no assumed IUU Risk Scatter worksheet. Neither is part of this final plan.
- Disabling Seasonality and other unused worksheets remain supporting workbook material; they are not extra required website sections.
- Verify filter scope, default selections, click actions, colour legends, and the actual embed dimensions before publishing.
- Keep sources and methodology together on the website. Consult [Analysis evidence notes](ANALYSIS_EVIDENCE_NOTES.md) for coverage and interpretation limits.
- The supplied workbook and later screenshots may reflect different saved states. Recheck the reference findings if data or calculations change; this document does not certify that the current dashboard implementation has passed those checks.
