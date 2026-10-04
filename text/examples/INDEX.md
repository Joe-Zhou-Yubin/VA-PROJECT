# Text Sources — Index

8 example sources fetched and annotated. Each file includes a summary, key findings, and explicit connections to our Tableau sheets and datasets.

## Files

| # | File | Source Type | What It Explains |
|---|------|-----------|-----------------|
| 01 | `01_tmt_iuu_vessel_list.md` | Structured database | The official RFMO blacklist — who gets formally listed and why. Join key for our IUU risk data. |
| 02 | `02_ejf_global_squid_report_2026.md` | NGO investigation | Forced labor + IUU in squid fleets. Explains our `forced_labor_encounters` field and the SWA/NWIO disabling hotspots. |
| 03 | `03_ejf_southwest_atlantic_squid.md` | Regional investigation | "Mile 201" off Argentina — why our disabling map has a cluster there. Chinese fishing hours up 85% in 5 years. |
| 04 | `04_noaa_2026_biennial_report.md` | US government report | Which countries the US formally identifies for IUU. Validates our country-level risk rankings. |
| 05 | `05_australia_enforcement_2026.md` | Enforcement news | 21 vessels seized in 2026, 190 fishers prosecuted. Real-world enforcement outcomes in our disabling hotspot near Torres Strait. |
| 06 | `06_seasonal_fishing_effort_paper.md` | Academic paper | Peer-reviewed proof that China's moratorium is the dominant seasonal signal in all AIS data. Explains Sheet 3 V-shaped dips. |
| 07 | `07_mongabay_enforcement_gap.md` | Environmental journalism | The gap between MPA designation and actual enforcement. Frames our project's entire motivation. |
| 08 | `08_china_subsidies_fleet_expansion.md` | Multi-source synthesis | China's $1.8B/year fishing subsidies, moratorium dates, WTO deal, fleet expansion. Explains the upward trend in our data. |

## How These Map to Tableau Sheets

| Tableau Sheet | Sources That Explain Its Patterns |
|---------------|----------------------------------|
| Sheet 1 (Global Fishing Map) | 07 (enforcement gap), 08 (fleet expansion) |
| Sheet 2 (Top Fishing Nations) | 04 (NOAA identified nations), 08 (subsidy-driven dominance) |
| Sheet 3 (Monthly Trend) | **06** (seasonal paper — directly explains V-dips), **08** (moratorium dates + subsidies) |
| Sheet 5 (Fleet Composition) | 02 (squid fleet is key gear type), 08 (China fleet composition) |
| Sheet 7 (Country Risk Ranking) | 04 (NOAA formal identifications validate our rankings) |
| Sheet 8 (IUU Risk Scatter) | 01 (TMT list = ground truth for which vessels are officially IUU), 02 (forced labor indicators) |
| Sheet 11 (Disabling Map) | **03** (SWA hotspot = Mile 201 squid fleet), **05** (Torres Strait enforcement), 07 (dark vessels) |
| Sheet 12 (Disabling by Flag) | 04 (NOAA identified flags), 05 (Indonesia dominates Torres Strait apprehensions) |
| Sheet 15 (Vessel Profile) | 01 (cross-reference individual vessels against TMT list), 02 (forced labor context) |
| Sheet 17 (Bubble Chart) | 08 (China = largest bubble because of subsidies, not just productive waters) |

## Suggested Use in the Report

### Introduction / Motivation
- 07 (enforcement gap) — sets the stage
- 08 (subsidies) — explains why the problem is getting worse, not better

### Related Works
- 06 (seasonal paper) — uses the same GFW dataset, directly citable
- 01 (TMT list) — established enforcement infrastructure

### Visual Analysis Results
- 03 + 05 — explain specific geographic hotspots visible in the disabling map
- 02 — explains the forced labor and transshipment patterns in the IUU risk data

### Conclusion
- 04 (NOAA report) — validates our findings against official government identifications
- 07 — reinforces why tools like our dashboard are needed
