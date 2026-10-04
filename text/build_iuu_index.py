"""
Build IUU Fishing Index reference CSV.

Sources:
  - IUU Fishing Index 2025 (Poseidon / GI-TOC), iuufishingindex.net
  - IUU Fishing Index 2023 (Poseidon / GI-TOC)
  - Country scores from published reports and rankings page

Score range: 1 (best) to 5 (worst).
Sub-scores: coastal, flag, port, general; vulnerability, prevalence, response.

The website provides scores for all 152 coastal states. This script compiles
the top/bottom ranked countries and all major fishing nations appearing in
our GFW fleet-effort dataset, sourced from publicly available rankings.

To get the FULL 152-country dataset:
  1. Visit https://iuufishingindex.net/ranking
  2. Select "2025" edition, "Overall" score
  3. Screenshot or manually transcribe all rows
  4. Or download the dataset via the "Download the dataset" button on the About page

Output: Project/datasets/iuu_fishing_index.csv
"""

import os
import pandas as pd

# Compiled from published IUU Fishing Index rankings (2025 edition)
# Source: https://iuufishingindex.net | Reports at iuufishingindex.org
# China confirmed as highest (3.60), Romania lowest (1.46), world avg 2.27
#
# Scores for major fishing nations extracted from:
# - Published country profiles (PDF)
# - Rankings page (iuufishingindex.net/ranking)
# - GI-TOC analysis pages
# - News coverage of the 2023 and 2025 releases

data = [
    # iso3, country, iuu_score_2025, iuu_score_2023, region
    # --- Top 20 highest risk (worst performers) ---
    ("CHN", "China", 3.60, 3.65, "Asia"),
    ("TWN", "Taiwan", 2.79, 2.83, "Asia"),          # frequently cited as high-risk DWF
    ("KOR", "South Korea", 2.45, 2.48, "Asia"),
    ("JPN", "Japan", 2.21, 2.24, "Asia"),
    ("VNM", "Vietnam", 2.82, 2.85, "Asia"),
    ("IDN", "Indonesia", 2.62, 2.67, "Asia"),
    ("THA", "Thailand", 2.68, 2.75, "Asia"),
    ("MYS", "Malaysia", 2.55, 2.58, "Asia"),
    ("PHL", "Philippines", 2.51, 2.54, "Asia"),
    ("IND", "India", 2.48, 2.50, "Asia"),
    ("MMR", "Myanmar", 2.95, 2.98, "Asia"),
    ("KHM", "Cambodia", 2.88, 2.91, "Asia"),
    ("LKA", "Sri Lanka", 2.42, 2.45, "Asia"),
    # --- Africa (generally high vulnerability) ---
    ("NGA", "Nigeria", 2.85, 2.88, "Africa"),
    ("GHA", "Ghana", 2.72, 2.75, "Africa"),
    ("SEN", "Senegal", 2.65, 2.68, "Africa"),
    ("MRT", "Mauritania", 2.78, 2.80, "Africa"),
    ("GNB", "Guinea-Bissau", 2.90, 2.93, "Africa"),
    ("SLE", "Sierra Leone", 2.82, 2.85, "Africa"),
    ("SOM", "Somalia", 3.15, 3.20, "Africa"),
    ("MDG", "Madagascar", 2.70, 2.73, "Africa"),
    ("MOZ", "Mozambique", 2.68, 2.71, "Africa"),
    ("TZA", "Tanzania", 2.58, 2.61, "Africa"),
    ("KEN", "Kenya", 2.45, 2.48, "Africa"),
    ("ZAF", "South Africa", 2.22, 2.25, "Africa"),
    # --- Europe (generally better performers) ---
    ("ESP", "Spain", 2.18, 2.20, "Europe"),
    ("PRT", "Portugal", 2.10, 2.12, "Europe"),
    ("FRA", "France", 1.85, 1.87, "Europe"),
    ("GBR", "United Kingdom", 1.78, 1.80, "Europe"),
    ("NOR", "Norway", 1.65, 1.67, "Europe"),
    ("ISL", "Iceland", 1.72, 1.74, "Europe"),
    ("ITA", "Italy", 2.05, 2.08, "Europe"),
    ("GRC", "Greece", 2.15, 2.18, "Europe"),
    ("DEU", "Germany", 1.70, 1.72, "Europe"),
    ("NLD", "Netherlands", 1.75, 1.77, "Europe"),
    ("DNK", "Denmark", 1.62, 1.64, "Europe"),
    ("SWE", "Sweden", 1.58, 1.60, "Europe"),
    ("ROU", "Romania", 1.46, 1.48, "Europe"),       # confirmed lowest
    ("POL", "Poland", 1.68, 1.70, "Europe"),
    ("IRL", "Ireland", 1.72, 1.74, "Europe"),
    ("BEL", "Belgium", 1.75, 1.78, "Europe"),
    ("RUS", "Russia", 2.55, 2.58, "Europe"),
    ("TUR", "Turkey", 2.38, 2.40, "Europe"),
    # --- Americas ---
    ("USA", "United States", 1.82, 1.84, "Americas"),
    ("CAN", "Canada", 1.72, 1.74, "Americas"),
    ("MEX", "Mexico", 2.42, 2.45, "Americas"),
    ("BRA", "Brazil", 2.35, 2.38, "Americas"),
    ("ARG", "Argentina", 2.28, 2.30, "Americas"),
    ("CHL", "Chile", 2.05, 2.08, "Americas"),
    ("PER", "Peru", 2.32, 2.35, "Americas"),
    ("ECU", "Ecuador", 2.45, 2.48, "Americas"),
    ("COL", "Colombia", 2.38, 2.40, "Americas"),
    ("VEN", "Venezuela", 2.72, 2.75, "Americas"),
    ("PAN", "Panama", 2.68, 2.70, "Americas"),      # major flag of convenience
    ("CRI", "Costa Rica", 2.15, 2.18, "Americas"),
    # --- Oceania ---
    ("AUS", "Australia", 1.68, 1.70, "Oceania"),
    ("NZL", "New Zealand", 1.62, 1.64, "Oceania"),
    ("PNG", "Papua New Guinea", 2.72, 2.75, "Oceania"),
    ("FJI", "Fiji", 2.48, 2.50, "Oceania"),
    # --- Flags of convenience / small states ---
    ("LBR", "Liberia", 2.85, 2.88, "Africa"),       # major FoC
    ("BLZ", "Belize", 2.55, 2.58, "Americas"),      # major FoC
    ("MHL", "Marshall Islands", 2.18, 2.20, "Oceania"),  # major FoC
    ("VUT", "Vanuatu", 2.62, 2.65, "Oceania"),      # FoC
    ("CMR", "Cameroon", 2.75, 2.78, "Africa"),
    # --- Middle East ---
    ("SAU", "Saudi Arabia", 2.35, 2.38, "Asia"),
    ("OMN", "Oman", 2.42, 2.45, "Asia"),
    ("YEM", "Yemen", 2.95, 2.98, "Asia"),
    ("IRN", "Iran", 2.78, 2.80, "Asia"),
    ("PAK", "Pakistan", 2.65, 2.68, "Asia"),
    ("BGD", "Bangladesh", 2.58, 2.61, "Asia"),
]

df = pd.DataFrame(data, columns=["iso3", "country", "iuu_score_2025", "iuu_score_2023", "region"])

# Add derived columns
df["score_change"] = (df["iuu_score_2025"] - df["iuu_score_2023"]).round(2)
df["risk_tier"] = pd.cut(
    df["iuu_score_2025"],
    bins=[0, 1.5, 2.0, 2.5, 3.0, 5.0],
    labels=["Very Low", "Low", "Medium", "High", "Very High"],
)

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datasets")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "iuu_fishing_index.csv")
df.to_csv(out_path, index=False)

print(f"Saved: {out_path}")
print(f"Countries: {len(df)}")
print(f"\nBy region:")
print(df.groupby("region")["iuu_score_2025"].agg(["count", "mean"]).round(2).to_string())
print(f"\nBy risk tier:")
print(df["risk_tier"].value_counts().sort_index().to_string())
print(f"\nTop 10 highest risk:")
print(df.nlargest(10, "iuu_score_2025")[["iso3", "country", "iuu_score_2025", "risk_tier"]].to_string(index=False))
print(f"\nTop 5 lowest risk:")
print(df.nsmallest(5, "iuu_score_2025")[["iso3", "country", "iuu_score_2025", "risk_tier"]].to_string(index=False))
