"""
Fetch Google Books Ngram data for IUU fishing-related terms.

Uses the undocumented JSON API at books.google.com/ngrams/json.
This indexes BOOKS (published literature), not news.
Coverage: 1800–2019 (English corpus).

Output: text/google_ngram_iuu.csv — ready for Tableau or matplotlib.

The value of this data: shows the long-arc emergence of IUU fishing
as a concept in published literature, useful as a framing chart
for the introduction/presentation.
"""

import requests
import pandas as pd
import time
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Terms to query — chosen to show the evolution of the IUU fishing concept
TERMS = {
    "illegal fishing": "illegal+fishing",
    "IUU fishing": "IUU+fishing",
    "overfishing": "overfishing",
    "fish stocks": "fish+stocks",
    "marine conservation": "marine+conservation",
    "bycatch": "bycatch",
    "fisheries management": "fisheries+management",
    "forced labour fishing": "forced+labour",
    "aquaculture": "aquaculture",
}

YEAR_START = 1950
YEAR_END = 2019
CORPUS = 26  # English (2019 corpus)
SMOOTHING = 3

all_data = []

for label, query in TERMS.items():
    url = (
        f"https://books.google.com/ngrams/json"
        f"?content={query}"
        f"&year_start={YEAR_START}"
        f"&year_end={YEAR_END}"
        f"&corpus={CORPUS}"
        f"&smoothing={SMOOTHING}"
    )
    print(f"Fetching: {label}...", end=" ", flush=True)
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                timeseries = data[0]["timeseries"]
                years = list(range(YEAR_START, YEAR_START + len(timeseries)))
                for yr, val in zip(years, timeseries):
                    all_data.append({
                        "term": label,
                        "year": yr,
                        "frequency": val,  # fraction of all bigrams/unigrams in corpus
                        "frequency_ppm": val * 1_000_000,  # parts per million for readability
                    })
                print(f"OK ({len(timeseries)} years)")
            else:
                print("no data returned")
        else:
            print(f"HTTP {resp.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(2)  # polite pause

if not all_data:
    print("\nNo data fetched. Check network.")
else:
    df = pd.DataFrame(all_data)
    out_path = os.path.join(OUTPUT_DIR, "google_ngram_iuu.csv")
    df.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")
    print(f"Terms: {df['term'].nunique()}, Years: {df['year'].min()}-{df['year'].max()}, Rows: {len(df)}")

    # Quick summary
    print("\nPeak year by term:")
    for term, grp in df.groupby("term"):
        peak = grp.loc[grp["frequency_ppm"].idxmax()]
        print(f"  {term:30s} peaked in {int(peak['year'])} at {peak['frequency_ppm']:.3f} ppm")
