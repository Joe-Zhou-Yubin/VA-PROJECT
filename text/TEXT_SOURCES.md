# Text Sources & Complementary Datasets for the IUU Fishing Project

A curated list of news sources, IUU vessel blacklists, complementary datasets, and contextual data layers that can be combined with the Global Fishing Watch data already in this project.

Grouped by usefulness. Every link has been surfaced from a public source and can be independently verified.

---

## 1. Authoritative IUU Vessel Lists

These are **join-ready blacklists** — connect them to `iuu_risk_all.parquet` via `mmsi` / `imo` / `callsign` to flag known offenders in your visualizations.

| Source | Description | Format | Link |
|--------|-------------|--------|------|
| **TMT Combined IUU Vessel List** | Consolidated real-time list of all RFMO-blacklisted vessels. Includes photos, last known AIS position, historical operators. Downloadable in Excel. | Web + Excel | https://iuu-vessels.org/ |
| **TMT — Our Tools page** | Landing page with all TMT-maintained public tools | Web | https://www.tm-tracking.org/combined-iuu-vessel-list |
| **ISSF IMO/UVI Tuna Vessel List** | Every tuna fishing vessel with an IMO number, cross-referenced against IUU lists | Public downloads | https://www.iss-foundation.org/fishery-goals-and-resources/our-priorities/illegal-fishing-prevention/ |
| **NOAA Biennial IUU Report to Congress** | Every 2 years, US names specific countries and vessels engaged in IUU. Historical PDF archive. | PDF | https://www.fisheries.noaa.gov/international/international-affairs/report-iuu-fishing-bycatch-and-shark-catch |
| **Interpol Purple Notices (fisheries)** | Public alerts on specific vessels changing names or flags to evade detection | Web listings | https://www.interpol.int/en/Crimes/Environmental-crime/Fisheries-related-crimes |
| **EU IUU Yellow Card system** | Trading partners flagged by EU for IUU shortcomings | News feed | https://ec.europa.eu/newsroom/mare/items/topic/331 |
| **NOAA Port Denials list** | Countries whose vessels are denied entry to US ports due to IUU findings | Web | https://www.fisheries.noaa.gov/international-affairs/port-denials-under-moratorium-protection-act |

**Recommended for our project:** the **TMT Combined IUU List**. Download the Excel, join on `imo` or `mmsi`, add an "IUU-listed" badge on the vessel profile page.

---

## 2. News Sources for Illegal Vessel Movements

### Structured News Databases (queryable)

| Source | Description | Query capability |
|--------|-------------|------------------|
| **GDELT Project** | 100+ languages of world news, indexed and georeferenced, updated every 15 min. Free. | Web search + BigQuery + CSV downloads. Good for "IUU fishing" + country + date queries. |
| **GDELT Analysis Service** | Point-and-click web UI to explore GDELT | Web tool |
| **GDELT DOC 2.0 API** | JSON REST API for the same data, no authentication required | Keyword + date filtering |

Links:
- https://www.gdeltproject.org/
- https://analysis.gdeltproject.org/
- https://gdelt.github.io/

Example GDELT news API call:
```
https://api.gdeltproject.org/api/v2/doc/doc?query=%22illegal%20fishing%22%20china&format=json
```

### Official Enforcement News Feeds

| Source | Description | Format | Link |
|--------|-------------|--------|------|
| **NOAA Fisheries** | US enforcement releases (patrols, seizures, sanctions) | Web + RSS | https://www.fisheries.noaa.gov/news |
| **Australian Border Force** | Frequent illegal fishing seizure reports; very active in Northern Territory | Web | https://www.abf.gov.au/newsroom-subsite/Pages/Newsroom.aspx |
| **Fisheries and Oceans Canada** | North Pacific patrol reports | RSS | https://www.canada.ca/en/fisheries-oceans/news.html |
| **INTERPOL News** | Global fisheries crime operations | Web | https://www.interpol.int/en/News-and-Events/News |
| **US State Department — IUU** | US policy positions and country actions on IUU | Web | https://www.state.gov/illegal-unreported-and-unregulated-fishing |

### NGO Investigative Reports (rich narrative content)

| Source | Description | Link |
|--------|-------------|------|
| **Environmental Justice Foundation (EJF)** | Long-form investigations linking IUU fishing with forced labor. Country-specific PDF downloads (Thailand, Indonesia, Vietnam, Senegal). | https://ejfoundation.org/reports |
| **Oceana** | Runs the IUU Tracker; publishes campaign reports | https://usa.oceana.org/reports/ |
| **Global Fishing Watch news & stories** | Case studies and platform releases | https://globalfishingwatch.org/stories-and-updates/ |
| **Mongabay** | Independent environmental journalism, strong fisheries coverage | https://news.mongabay.com/list/fisheries/ |

### Maritime Trade Press (for context)

| Source | Format | Link |
|--------|--------|------|
| **MarineLink** | Web + RSS | https://www.marinelink.com/feeds |
| **The Maritime Executive** | Web | https://www.maritime-executive.com/ |
| **TradeWinds** | Paywalled but headlines free | https://www.tradewindsnews.com/ |
| **National Geographic — Environment** | Feature journalism (INTERPOL fisheries crime story) | https://www.nationalgeographic.com/environment/article/interpol-illegal-fishing-detectives |

---

## 3. Datasets on Hugging Face

Most maritime datasets on HF are **image-based (SAR / satellite)** rather than event/news-based, but useful for augmentation if extending toward computer vision:

| Dataset | Type | Link |
|---------|------|------|
| **ConnorLuckettDSTG/SARFish** | SAR imagery labeled for ship detection, classification, length regression | https://huggingface.co/datasets/ConnorLuckettDSTG/SARFish |
| **opensar-insight/vessel-detection-dataset** | 15 SAR scenes with ocean wind conditions | https://huggingface.co/datasets/opensar-insight/vessel-detection-dataset |
| **hanchong/maritime-vessel-dataset** | Maritime vessel dataset (gated, needs access approval) | https://huggingface.co/datasets/hanchong/maritime-vessel-dataset |
| **SEA-AI/SeaClips** | Maritime obstacle detection video clips | https://huggingface.co/datasets/SEA-AI/SeaClips |
| **TobinH/FMUKF_dataset** | 1000 parameterizations of a 6-DOF containership model | https://huggingface.co/datasets/TobinH/FMUKF_dataset |
| **alimkacar/argus-maritime-yolo11l** | Pre-trained YOLO model for maritime object detection | https://huggingface.co/alimkacar/argus-maritime-yolo11l |

**Verdict:** HF is limited for our tabular use case. SARFish is the most on-topic (IUU imagery). Consider only if we extend to computer vision.

---

## 4. Datasets on Kaggle and GitHub

| Source | Description | Link |
|--------|-------------|------|
| **Kaggle — GFW datasets** | Older mirrors of GFW data + community notebooks | Search "global fishing watch" on https://www.kaggle.com/datasets |
| **AIS Vessel Traffic (US Coast Guard / MarineCadastre)** | US territorial waters AIS; higher resolution than GFW globally | https://github.com/ocm-marinecadastre/ais-vessel-traffic (data at https://marinecadastre.gov/accessais/) |
| **Ushant AIS Dataset** | 18K vessel trajectories, 7M+ GPS observations off the French coast | https://github.com/rtavenar/ushant_ais |
| **Piraeus AIS Dataset** | 2.5 years of AIS around the port of Piraeus, Greece | https://pmc.ncbi.nlm.nih.gov/articles/PMC8749179/ |
| **geetakingle/Detecting-Illegal-Fishing** | GitHub project: anomaly detection on GFW data using semi-supervised learning | https://github.com/geetakingle/Detecting-Illegal-Fishing |
| **eyesofworld/Maritime-Monitoring** | Curated dataset links and papers on AIS-based maritime monitoring | https://github.com/eyesofworld/Maritime-Monitoring |
| **ABDULSABOOR1995/Vessel-Anomaly-Behaviour-Detection** | AIS anomaly detection | https://github.com/ABDULSABOOR1995/Vessel-s-Anomaly-Behaviour-Detection |
| **DanielAmigo/trajectory-based-ship-classification** | Trajectory-based fishing ship classification (paper + code) | https://github.com/DanielAmigo/trajectory-based-ship-classification |
| **GlobalFishingWatch/vessel-classification** | Official GFW vessel classification code | https://github.com/GlobalFishingWatch/vessel-classification |
| **GlobalFishingWatch/paper-longline-ais-sar-matching** | Repo behind the longline SAR paper | https://github.com/GlobalFishingWatch/paper-longline-ais-sar-matching |

---

## 5. Contextual Geographic Layers

Layer these onto our maps to add spatial context and support the "who's fishing where they shouldn't be" narrative.

| Source | Description | Format | Link |
|--------|-------------|--------|------|
| **MarineRegions EEZ boundaries** | Exclusive Economic Zones polygons for every coastal country | GeoJSON, Shapefile | https://www.marineregions.org/downloads.php |
| **FAO Major Fishing Areas** | Global fishing zone polygons used in FAO statistics | Downloadable | https://www.fao.org/fishery/en/area/search |
| **Marine Protected Areas (MPA Atlas)** | Global no-fishing and restricted zones | Web + downloads | https://mpatlas.org/ |
| **World Port Index (WPI)** | Global port database, complements GFW anchorages | Downloadable | https://msi.nga.mil/Publications/WPI |
| **Natural Earth** | Country boundaries, physical features, populated places | Shapefile, GeoJSON | https://www.naturalearthdata.com/ |
| **johan/world.geo.json** | Already used in the country choropleth (ISO3-keyed) | GeoJSON | https://github.com/johan/world.geo.json |

---

## 6. Academic Papers (for related works section)

Key papers to cite when writing about the IUU fishing landscape:

| Paper | Year | Topic | Link |
|-------|------|-------|------|
| Kroodsma et al. — *Tracking the global footprint of fisheries* | 2018, Science | Foundational GFW paper | https://science.sciencemag.org/content/359/6378/904 |
| Welch et al. — *Hotspots of unseen fishing vessels* | 2022, Science Advances | AIS disabling events (our dataset) | https://www.science.org/doi/10.1126/sciadv.abq2109 |
| Paolo et al. — *Satellite mapping reveals extensive industrial activity at sea* | 2024, Nature | SAR-detected "hidden" vessels | https://www.nature.com/articles/s41586-023-06825-8 |
| Park et al. — *Tracking elusive and shifting identities of the global fishing fleet* | 2023, Science Advances | Reflagging patterns and hidden ownership | https://www.science.org/doi/10.1126/sciadv.abp8200 |
| Nature Comm 2022 — *Revealing global risks of labor abuse and IUU fishing* | 2022 | Links between forced labor and IUU | https://www.nature.com/articles/s41467-022-28916-2 |
| arXiv 2606.18181 — *Tracking IUU, Seafood Fraud, and Labor Abuse through LLM-driven Information Extraction* | 2025 | Modern LLM approach | http://arxiv.org/abs/2606.18181v1 |
| MDPI Water 2025 — *Improving International Cooperation Frameworks for Combating IUU Fishing* | 2025 | Policy analysis | https://www.mdpi.com/2073-4441/17/17/2518 |

---

## 7. Recommended Additions for the Project (Priority Order)

If you want to strengthen the story on top of what we already have:

### High priority

1. **TMT Combined IUU List** — highest ROI. Adds "officially blacklisted" flag to any vessel that appears in both datasets. Join key: `imo`, fallback to `mmsi`.
2. **GDELT news overlay** — add a side panel to the AIS Disabling Map that pulls recent news mentions when a vessel or flag state is selected. Live investigative context.
3. **MarineRegions EEZ Boundaries** — overlay onto the fishing heatmap so viewers can see when country A's vessels fish in country B's waters (strong IUU signal).

### Medium priority

4. **NOAA Biennial Report countries** — highlight nations formally identified by the US for IUU. Small hardcoded list.
5. **EJF forced labor reports** — pull country-specific findings into the story text of the country choropleth.

### Low priority (for extended work)

6. **SARFish satellite imagery** — reveal vessels not broadcasting AIS at all (dark fleet). Requires computer vision.
7. **MPA Atlas overlays** — highlight fishing hours inside marine protected areas as a specific illegal-fishing indicator.

---

## 8. Quick Verification Links (single click each to sanity-check)

- TMT: https://iuu-vessels.org/
- GDELT search: https://analysis.gdeltproject.org/
- NOAA IUU reports: https://www.fisheries.noaa.gov/international/international-affairs/report-iuu-fishing-bycatch-and-shark-catch
- MarineRegions EEZ: https://www.marineregions.org/eez.php
- EJF reports index: https://ejfoundation.org/reports
- SARFish: https://huggingface.co/datasets/ConnorLuckettDSTG/SARFish
- Mongabay Fisheries: https://news.mongabay.com/list/fisheries/
- Global Fishing Watch stories: https://globalfishingwatch.org/stories-and-updates/

---

*Last updated: August 2026*
*Sources gathered via web search during project scoping. Verify freshness before final report.*
