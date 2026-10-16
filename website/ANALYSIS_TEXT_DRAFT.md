# Analysis Text Draft — Deeper Insights

Proposed rewrites for all 6 analysis sections. Same Problem / What we found / Why it matters structure, but replacing surface-level dashboard narration with actual analytical observations.

**Format:** Each section shows the current text (abbreviated) and the proposed replacement. Review and mark up, then I'll apply to `index.html`.

---

## Analysis 01 — Where Does the World Fish?

### The Problem
**Current:** Fishing takes place across a vast ocean, but its distribution is uneven. Before examining risk, researchers need to understand where observed activity is concentrated and whether those concentrations change over time.

**Proposed:** Global fishing is not spread evenly across the ocean. Most of it concentrates in a handful of coastal and shelf regions, while vast stretches of open water appear nearly empty in AIS records. Understanding where the activity clusters, and where it does not, is the baseline for everything that follows.

### What we found
**Current:** The map shows dense concentrations around East and Southeast Asia and Europe in 2024. [Paragraph about Compare Years.]

**Proposed:** Five regions account for the overwhelming majority of recorded fishing hours: the East China Sea and Yellow Sea, the waters around Indonesia and Vietnam, the Northeast Atlantic shelf (Norway to Spain), the Peruvian anchoveta grounds, and the Argentine shelf. The East China Sea alone contains more recorded fishing hours than the entire western coast of Africa.

Switching to Compare Years reveals a visible dip in 2020, particularly in the Northwest Pacific, corresponding to COVID-19 port closures and crew restrictions. By 2021 the rebound had already overshot pre-pandemic levels, and by 2024 the overall footprint is larger than at any point in the five-year window. Southeast Asian waters show the most consistent year-over-year growth.

Equally notable is what the map does not show. The Central Pacific, Southern Ocean, and large stretches of the Indian Ocean appear nearly blank, yet satellite radar research (Paolo et al. 2024) has identified substantial vessel activity in these areas by ships that never broadcast AIS at all. Absence on this map should not be read as absence of fishing.

### Why it matters
**Current:** Knowing where fishing is concentrated gives the later risk analyses a baseline. [Caveat about hotspots.]

**Proposed:** This map sets the denominator for every risk indicator that follows. A region with more fishing will naturally produce more AIS events, more encounters, and more disabling incidents simply because more vessels are operating there. Without this baseline, a high event count could be mistaken for a high risk rate.

The post-COVID rebound is particularly relevant: the rapid return to and then exceeding of pre-pandemic effort levels suggests that any temporary reduction in fishing pressure was structural (port closures, crew shortages) rather than a lasting policy change. The fleet came back bigger.

---

## Analysis 02 — Fleet DNA: How the Top 20 Flag States Fish

### The Problem
**Current:** Similar levels of fishing activity can arise from very different fleet structures. Country totals alone conceal differences in fishing gear, seasonality and changes over time.

**Proposed:** Total fishing hours tell you how much a country fishes. They do not tell you how. Two nations with similar totals can have completely different environmental footprints depending on whether their fleets trawl the seabed, set longlines for tuna, or jig for squid at night. Gear type determines what gets caught, what gets killed as bycatch, and how much habitat gets damaged.

### What we found
**Current:** Chinese-flagged vessels account for 52.4 million fishing hours. Trawlers 60.4% of Chinese hours. Drifting longlines 55.8% of Taiwanese hours.

**Proposed:** China's fleet is both the largest and the most diversified. In 2024, Chinese-flagged vessels logged approximately 52.4 million fishing hours spread across trawlers (~60%), squid jiggers, drifting longlines, and seiners. Even China's relatively modest squid jigger share represents more absolute fishing hours than the entire output of most nations on this chart.

The contrast with other major fleets is sharp. Taiwan and South Korea are dominated by drifting longlines, reflecting their distant-water tuna operations across the Pacific and Indian Oceans. These longline fleets carry elevated shark and seabird bycatch risk. Vietnam is almost entirely trawlers, the gear type with the highest bycatch rates and most seabed damage. Norway, France, and the UK are also trawler-heavy, but operate in heavily regulated North Atlantic waters with quota enforcement.

The monthly trend reveals a distinctive Chinese seasonal pattern: fishing drops sharply every summer during the government-mandated South China Sea moratorium, then spikes aggressively in autumn. No other nation shows this pattern, and it creates a predictable annual cycle that other fleets may exploit by operating in the same waters during the moratorium window.

### Why it matters
**Current:** Fleet scale and fishing methods provide context for interpreting risk. [Caveat about flag vs owner.]

**Proposed:** Gear composition is not just a technical detail. A trawler-heavy fleet damages different ecosystems than a longline-heavy one, and the monitoring challenges differ too: squid jiggers operating at night on the high seas are inherently harder to observe than seiners working in coastal waters.

These profiles also reveal which nations' fleets are most likely to encounter each other at sea. China's diversified fleet operates in nearly every major fishing ground, putting it into geographic overlap with smaller, more specialised fleets. That overlap is where encounters, transshipment opportunities, and competition for stocks become most acute.

One important caveat: a vessel's flag identifies its registration state, not necessarily its owner, operator, or the nationality of its crew. Indonesian fishers work on Chinese-flagged vessels. Spanish companies own vessels flagged to Belize. The flag is a starting point, not a conclusion.

---

## Analysis 03 — Country Risk Patterns

### Sub-section 03a: Beyond the Average: Risk-Tier Distribution

#### The Problem
**Current:** A country average can conceal how risk is distributed across individual vessels. Similar averages can describe a small group with elevated indicators or a larger group with lower scores.

**Proposed:** Risk averages are misleading when most of the fleet scores zero. If 90% of a country's assessed vessels have no recorded risk indicators at all, the country average is being pulled down by a mass of clean records, hiding a potentially significant minority of high-risk vessels. The distribution tells a different story than the mean.

#### What we found
**Current:** None is the largest tier in every year.

**Proposed:** Across every year from 2012 to 2025, over 80% of assessed vessels fall into the "None" tier, meaning they have zero recorded scored indicators. The IUU risk problem is not a fleet-wide phenomenon. It is concentrated in a small minority. But that minority is not small in absolute terms: in 2024 alone, thousands of individual vessels carry Low, Medium, or High risk scores.

The share of vessels in the High tier has remained relatively stable over the 13-year period, suggesting that enforcement and policy efforts have not substantially reduced the proportion of the fleet displaying suspicious behaviour. Whether this reflects persistent offenders, new entrants replacing those caught, or simply better detection over time is a question the data cannot answer alone.

#### Why it matters
**Current:** Tier proportions complement averages and raw counts.

**Proposed:** This chart is the reason we do not rely on country averages alone. A nation with a low average score but 200 high-risk vessels presents a different investigative priority than one with a higher average but only 10 flagged vessels. The risk-tier distribution forces the question: are we looking at a widespread problem or a concentrated one? For every country in the dashboard below, the answer is concentrated, but the size of that concentration varies dramatically.

### Sub-section 03b: Country Risk Patterns

#### The Problem
**Current:** A country with more fishing activity does not necessarily have the highest average risk.

**Proposed:** The country with the most fishing hours is not necessarily the country with the highest risk rate. China's fleet is eight times larger than Taiwan's, but does that mean it has eight times the risk, or does the per-vessel picture look different? Separating scale from rate is essential for fair comparison.

#### What we found
**Current:** China 0.585 vs Taiwan 1.238 vs Spain 1.213. 115 high-risk vessels for China, 101 for Taiwan, 50 for Spain.

**Proposed:** The 2024 data reveals a striking paradox. China has the lowest average risk score among the top three (0.585) despite having the largest absolute count of high-risk vessels (115). Taiwan's average is more than double China's (1.238), and Spain's is similar (1.213), even though both have smaller fleets.

This means a higher proportion of Taiwan's and Spain's assessed fleets trigger behavioural indicators. For Taiwan, this likely reflects its distant-water longline fleet, which operates at extreme distances from shore, has more opportunity for at-sea encounters, and is historically associated with higher rates of AIS disabling. For Spain, the elevated score may reflect its large distant-water trawler fleet operating in West African and South American waters, regions where the AIS disabling map (Analysis 04) shows dense gap activity.

China's lower average is partly an artifact of scale: its enormous fleet includes many coastal vessels with minimal risk indicators, diluting the average. But 115 high-risk vessels is still a larger pool of suspicious activity than most nations produce in total.

#### Why it matters
**Current:** Combining scale, indicator types, history and tier proportions gives a more defensible basis.

**Proposed:** Any ranking that uses a single metric will mislead. If you rank by total high-risk vessels, China leads. If you rank by risk rate, Taiwan and Spain lead. If you rank by fleet size, China dwarfs everyone. The dashboard is designed to let you toggle between these perspectives and form your own judgment about where investigative attention is most warranted.

The flag-state vs port-state comparison adds another layer: vessels flagged to Panama, Vanuatu, or Belize but porting exclusively in China or Peru may indicate flag-of-convenience arrangements designed to obscure ownership and avoid regulatory scrutiny.

---

## Analysis 04 — Going Dark: From Offshore Patterns to a Vessel

### Sub-section 04a: From a Tracking Gap to a Vessel's History

#### The Problem
**Current:** An offshore concentration of tracking gaps does not explain an individual vessel's behaviour.

**Proposed:** A cluster of tracking gaps on a map tells you where vessels disappear, but not why. Equipment failure, poor satellite coverage, deliberate evasion, and transit through areas with limited reception all produce the same data signature. To distinguish intentional concealment from technical noise, you need the individual vessel's history: has it disabled AIS before? Does it encounter IUU-listed vessels? Does it spoof its identity?

#### What we found
**Current:** The map-to-profile interaction reveals which recorded indicators are available.

**Proposed:** Clicking a disabling event on the map loads that vessel's full behavioural profile. A typical high-risk example might show a Panamanian-flagged squid jigger with 8 AIS gaps exceeding 24 hours, 15 encounters with previously IUU-listed vessels, and over 200 hours of MMSI overlap with another vessel (identity spoofing). That combination of indicators, appearing together on a single vessel, is far more informative than any individual metric.

The vessel histories often span years beyond the 2017-2019 disabling event window. This temporal mismatch is important: a vessel that disabled AIS in 2018 may show elevated risk indicators in 2022-2024 from the IUU Risk dataset, suggesting persistent behaviour rather than a one-time event. Conversely, if an MMSI has no matching risk profile, it may have changed identity since the event, which is itself a red flag.

#### Why it matters
**Current:** An individual vessel's history helps turn a broad geographic pattern into a specific, traceable investigation.

**Proposed:** This is where the analysis shifts from patterns to cases. The map shows 55,000 events. Most of them are noise. The vessel profile is the filter that separates a suspicious actor from a vessel that lost signal in a storm. It is also where the three levels of the project converge: the global map (where), the fleet profile (who), and the vessel history (what they did). A vessel that appears in a disabling hotspot, belongs to a high-risk flag state, and carries multiple behavioural indicators across several years is a qualitatively different signal than a single unexplained gap.

### Sub-section 04b: Offshore Distribution: Where Vessels Go Dark

#### The Problem
**Current:** Tracking gaps reduce visibility into vessel movements. Their location and duration can identify questions for investigation.

**Proposed:** When a vessel stops broadcasting its AIS position, it becomes invisible to satellite monitoring. The question is whether the gap is random or geographic. If disabling events cluster in specific locations, that clustering is itself evidence of intent, because equipment failure and satellite coverage gaps would produce a more uniform distribution.

#### What we found
**Current:** 55,368 events, 5,269 MMSIs. Median duration 23.5 hours, median distance from shore 413 km.

**Proposed:** The 2017-2019 extract contains 55,368 disabling events from 5,269 distinct vessels. The median gap lasts 23.5 hours and begins approximately 413 km from shore, roughly 220 nautical miles, well beyond the territorial sea and outside the practical patrol range of virtually every coast guard in the world.

The distribution is far from uniform. Three regions produce disproportionate concentrations: the Argentine EEZ boundary (where squid jigger fleets cross between international waters and Argentina's exclusive zone), off West Africa (where foreign distant-water fleets operate with minimal oversight from coastal states), and the Northwest Pacific (the world's most intensively fished waters). These are precisely the regions where high-value stocks overlap with enforcement gaps, consistent with intentional concealment rather than technical failure.

The distance-from-shore histogram also reveals a gap: very few events begin within 200 km of shore, partly because the source dataset excludes near-shore gaps by design, but also because vessels closer to shore have less incentive to hide. The incentive structure matches the geographic pattern: disabling correlates with distance from enforcement, not distance from land.

#### Why it matters
**Current:** The distance distribution provides context. Being far offshore is not itself evidence of illegal fishing.

**Proposed:** The geographic clustering of disabling events is the single strongest visual signal in this project. Random equipment failures would not concentrate at EEZ boundaries. The fact that they do, and that the same regions also host the highest-value fisheries and the weakest enforcement, points to a structural relationship between geography, economics, and evasion. Clean zones like Australia, Northern Europe, and the US East Coast, where enforcement is strong and VMS requirements are strictly applied, show dramatically fewer events.

For Singapore, the Southeast Asian waters show a distinct mid-severity pattern (12-24 hour gaps) that differs from the multi-day disappearances off Argentina and West Africa. This may reflect shorter-range vessels making brief transits, or a different concealment pattern suited to the congested, multi-jurisdictional waters of the Strait of Malacca and South China Sea.

---

## Analysis 05 — External Assessments and World News

### The Problem
**Current:** A behavioural risk score is one perspective, not an independent determination of illegality.

**Proposed:** AIS-derived risk scores are generated from one data source using one methodology. If they happen to align with independent expert assessments built from entirely different evidence (surveys, enforcement records, policy analysis), that alignment strengthens confidence in both. If they diverge, the divergence itself is analytically interesting.

### What we found
**Current:** The dashboard compares annual AIS-derived country risk with a fixed 2025 external assessment. [Caveat about validation.]

**Proposed:** The IUU Fishing Index (Poseidon/GI-TOC, 2025) scores 152 coastal states on a 1-5 scale using 40 indicators drawn from surveys, enforcement records, and expert opinion, a methodology entirely independent of AIS data. China scores 3.60, the highest of any nation, independently confirming its position at the top of our AIS-derived risk rankings. Romania scores 1.46, the lowest. The broad alignment between two completely different measurement approaches, one satellite-based and one expert-assessed, is the strongest external validation this project has.

The GDELT news corpus (1,534 articles, 2020-2024) adds a media-attention dimension. China-related IUU coverage spiked to 31% of all retrieved articles in 2022, driven by the WTO fisheries subsidies debate and several high-profile enforcement operations. By 2024 it had dropped to 5%. This decline does not reflect improvement in China's fishing practices; it reflects the media cycle moving on. The gap between persistent risk (visible in our AIS data) and fading coverage (visible in GDELT) is itself an insight about where public attention fails to track actual threats.

Coverage is also geographically biased. GDELT articles are predominantly English-language and Western-sourced. West Africa and Southeast Asia, two of the highest-risk regions in our AIS analysis, are underrepresented in the news corpus relative to their actual risk indicators.

### Why it matters
**Current:** External comparison can reveal agreement, disagreement, and questions about measurement.

**Proposed:** Validation is not decoration. If our composite risk scores had diverged sharply from the IUU Fishing Index, it would call the methodology into question. The fact that they broadly align, despite being built from completely different evidence, suggests both are measuring something real.

The news analysis serves a different purpose. It reveals what the world pays attention to, and more importantly, what it overlooks. If the highest-risk regions are the least covered, that is a monitoring gap that policymakers should address. Media coverage is a lagging, event-driven indicator; the AIS data provides the continuous, systematic view that journalism cannot.

---

## Analysis 06 — Voices from the Fleet

### The Problem
**Current:** Tracking data cannot directly describe working conditions, violence, pay, or other experiences aboard vessels.

**Proposed:** AIS data tells you where a vessel went and when it stopped transmitting. It cannot tell you that an Indonesian fisher was beaten for refusing to work, or that a turtle was used as bait because the captain ordered it, or that crew went months without pay while the vessel operated 12,000 km from home. The quantitative signals in the previous analyses describe behaviour from orbit. These testimonies describe it from the deck.

### What we found
**Current:** 111 passages: 56 Chinese, 5 Taiwanese, 4 Korean, 46 unknown. Wildlife in 40, conditions in 26, death in 24, violence in 19.

**Proposed:** EJF interviewed over 430 Indonesian and Filipino fishers who worked aboard distant-water squid vessels. The 111 extracted passages from three investigation reports reveal a consistent pattern: wildlife destruction is the most frequently mentioned theme (40 passages), describing systematic shark finning, turtle bycatch, and the discarding of protected species as routine practice rather than isolated incidents.

Death appears in 24 passages, violence in 19, and working conditions in 26. The relative prominence of wildlife over violence is itself revealing: it suggests the environmental destruction is a daily reality that fishers mention matter-of-factly, while the physical abuse, though severe when it occurs, is episodic rather than constant.

Chinese-flagged vessels dominate the sample (56 of 65 flagged testimonies), reflecting EJF's investigation focus on the Chinese distant-water squid fleet. Korean-flagged vessels appear in only 4 testimonies but carry disproportionate violence and conditions mentions, suggesting concentrated severity. Taiwanese vessels appear mainly in wildlife contexts.

The geographic terms in the corpus ("southwest atlantic", "indian ocean", "high seas") and the vessel-type terms ("squid jigger", "light seiner", "dwf") map directly onto the fleet segments showing the highest AIS disabling rates in Analysis 04. The qualitative and quantitative evidence point at the same vessels.

### Why it matters
**Current:** These passages add human and environmental context that vessel tracks cannot establish.

**Proposed:** This section exists because data without human context is incomplete. The AIS shows a vessel disappearing for 72 hours off the Argentine shelf. The risk model flags it as High. The IUU Index confirms the flag state is problematic. The news corpus shows a spike in enforcement reporting. But none of that tells you that the crew aboard was working 20-hour shifts, that the bodies of sharks were thrown overboard after their fins were cut, or that a young fisher "below 20 years old" was "frequently hit" and had his clothes ripped off.

These testimonies turn statistical patterns into human experiences. They are not representative of all fishing, and they reflect EJF's investigative focus rather than a random sample. But they describe conditions that are structural, not anecdotal: the same themes recur across years, across vessels, and across ocean basins. The word cloud at the top of this page, built from these same reports, makes that recurrence visible at a glance.

---

## Conclusion

### Current
Generic advice: read risk in context, connect evidence carefully, turn signals into questions.

### Proposed

**From patterns to informed investigation.**

The six analyses bring together four layers of evidence: satellite-derived fishing activity, vessel-level behavioural risk, external expert assessments and media coverage, and firsthand human testimony. Each layer answers a different question; together they narrow from 695 million hours of fishing across five years to the specific vessels, regions, and practices most worth investigating.

**Three cards:**

**What the data confirms:**
Five flag states account for the majority of global fishing hours. Behavioural risk concentrates in a small minority of the fleet. AIS disabling clusters at EEZ boundaries where enforcement is weakest. Taiwan and Spain show higher risk rates than China despite smaller fleets. And the fishers who crew these vessels describe conditions that align with the quantitative signals.

**What the data cannot prove:**
A tracking gap is not evidence of crime. A high risk score is not a conviction. The IUU Fishing Index measures vulnerability and response, not actual catches. GDELT coverage reflects media attention, not ground truth. And 111 testimonies from a focused investigation are not a census of global fishing conditions. Every finding in this project is a signal, not a verdict.

**What to do next:**
The most productive next step is temporal: overlay the 2020-2024 IUU risk indicators with real-time vessel tracking to flag sudden changes in behaviour (a vessel that newly starts disabling AIS, or one whose encounters with IUU-listed vessels spike in a particular quarter). Network analysis of vessel encounters would reveal whether high-risk vessels operate in clusters or independently. And the forced-labour network proximity field (dist_to_forced_labor) deserves a dedicated investigation: if the median distance across the global fleet is small, the problem is structurally embedded, not confined to a few notorious operators.

**Closing line:**
Seeing more of the fleet means knowing both what the evidence reveals and what remains unseen. The ocean is large. The fleet is larger. But it is no longer invisible.
