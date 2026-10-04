"""
Fetch IUU fishing news articles from GDELT DOC 2.0 API.

Key fixes for rate limiting:
  - User-Agent header (GDELT blocks requests without one)
  - Exponential backoff: 60s → 120s → 240s on 429, max 5 retries per request
  - 5-second pause between every successful request
  - Progress saved after each query so you can resume if interrupted

Targets English-language articles on:
  - Illegal fishing
  - IUU fishing
  - Forced labor in fishing
  - Vessel seizures / enforcement
  - Dark fleet / AIS disabling
  - Illegal vessels

Output: Project/text/gdelt/gdelt_iuu_news_clean.csv
"""

import os
import time
import json
import requests
import pandas as pd
from io import StringIO
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gdelt")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Progress file — tracks which query+window combos are done
PROGRESS_FILE = os.path.join(OUTPUT_DIR, "_progress.json")

API_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"

# Browser-like User-Agent (GDELT blocks bare requests)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Search queries — all English-only
QUERIES = {
    "illegal_fishing": '"illegal fishing" sourcelang:english',
    "iuu_fishing": '"IUU fishing" sourcelang:english',
    "forced_labor_fishing": '("forced labor" OR "forced labour" OR "slave labor") fishing vessel sourcelang:english',
    "vessel_seized": '("vessel seized" OR "vessel apprehended" OR "boat seized") fishing sourcelang:english',
    "dark_fleet": '("dark fleet" OR "dark vessel" OR "AIS disabled" OR "AIS disabling") fishing sourcelang:english',
    "illegal_vessel": '("illegal vessel" OR "illegal trawler" OR "poaching vessel") sourcelang:english',
}

# Quarterly time windows 2020-2024
TIME_WINDOWS = []
for year in range(2020, 2025):
    quarters = [
        (f"{year}0101000000", f"{year}0401000000", f"{year}-Q1"),
        (f"{year}0401000000", f"{year}0701000000", f"{year}-Q2"),
        (f"{year}0701000000", f"{year}1001000000", f"{year}-Q3"),
        (f"{year}1001000000", f"{year}1231235959", f"{year}-Q4"),
    ]
    TIME_WINDOWS.extend(quarters)


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"completed": [], "partial_results": []}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def fetch_with_retry(query, start_dt, end_dt, max_retries=5):
    """
    Fetch articles with exponential backoff on rate limits.
    Retries: 60s, 120s, 240s, 480s, 960s before giving up.
    """
    params = {
        "query": query,
        "mode": "artlist",
        "maxrecords": 250,
        "format": "csv",
        "sort": "datedesc",
        "startdatetime": start_dt,
        "enddatetime": end_dt,
    }

    for attempt in range(max_retries):
        try:
            resp = requests.get(API_BASE, params=params, headers=HEADERS, timeout=30)

            if resp.status_code == 200:
                if len(resp.text.strip()) < 50:
                    return pd.DataFrame()
                return pd.read_csv(StringIO(resp.text))

            elif resp.status_code == 429:
                wait = 60 * (2 ** attempt)  # 60, 120, 240, 480, 960 seconds
                print(f"\n    429 Rate limited. Attempt {attempt+1}/{max_retries}. Waiting {wait}s...", end=" ", flush=True)
                time.sleep(wait)
                print("Retrying...", end=" ", flush=True)

            else:
                print(f"\n    HTTP {resp.status_code}", end=" ", flush=True)
                wait = 30 * (2 ** attempt)
                time.sleep(wait)

        except requests.exceptions.Timeout:
            print(f"\n    Timeout. Attempt {attempt+1}/{max_retries}.", end=" ", flush=True)
            time.sleep(30 * (2 ** attempt))

        except Exception as e:
            print(f"\n    Error: {e}", end=" ", flush=True)
            time.sleep(30)

    print(f"\n    FAILED after {max_retries} retries.", flush=True)
    return pd.DataFrame()


def main():
    progress = load_progress()
    completed_keys = set(progress["completed"])

    # Load any partial results from previous runs
    partial_file = os.path.join(OUTPUT_DIR, "gdelt_iuu_news_raw.csv")
    if os.path.exists(partial_file) and len(completed_keys) > 0:
        existing = pd.read_csv(partial_file, low_memory=False)
        all_dfs = [existing]
        print(f"Resuming: {len(completed_keys)} queries already done, {len(existing)} articles loaded.\n")
    else:
        all_dfs = []

    total_queries = len(QUERIES) * len(TIME_WINDOWS)
    done = len(completed_keys)
    new_articles = 0

    for query_name, query_str in QUERIES.items():
        print(f"\n=== Query: {query_name} ===")

        for start_dt, end_dt, period_label in TIME_WINDOWS:
            key = f"{query_name}|{period_label}"

            if key in completed_keys:
                done_display = list(completed_keys).index(key) + 1 if key in completed_keys else "?"
                continue  # Skip already-completed

            done += 1
            print(f"  [{done}/{total_queries}] {period_label}...", end=" ", flush=True)

            df = fetch_with_retry(query_str, start_dt, end_dt)

            if not df.empty:
                df["query_name"] = query_name
                df["period"] = period_label
                all_dfs.append(df)
                new_articles += len(df)
                print(f"{len(df)} articles", flush=True)
            else:
                print("0 articles", flush=True)

            # Mark as done
            completed_keys.add(key)
            progress["completed"] = list(completed_keys)
            save_progress(progress)

            # Polite pause between successful requests
            time.sleep(5)

    if not all_dfs:
        print("\nNo articles fetched at all. Check network or try later.")
        return

    # Combine
    combined = pd.concat(all_dfs, ignore_index=True)
    print(f"\nTotal raw articles: {len(combined)}")

    # Standardize columns
    combined.columns = [c.strip().lower() for c in combined.columns]

    # Deduplicate
    if "url" in combined.columns:
        before = len(combined)
        combined = combined.drop_duplicates(subset="url")
        print(f"After dedup: {len(combined)} (removed {before - len(combined)} dupes)")

    # Parse date
    date_col = "seendate" if "seendate" in combined.columns else "date"
    if date_col in combined.columns:
        combined["date"] = pd.to_datetime(combined[date_col], errors="coerce")
        combined["year"] = combined["date"].dt.year
        combined["month"] = combined["date"].dt.month
        combined["year_month"] = combined["date"].dt.to_period("M").astype(str)

    # Topic flags
    if "title" in combined.columns:
        combined["title"] = combined["title"].fillna("")
        t = combined["title"].str.lower()

        combined["topic_iuu"] = t.str.contains(r"iuu|illegal.*fish|unlawful.*fish|poach", na=False).astype(int)
        combined["topic_seized"] = t.str.contains(r"seize|apprehend|intercept|arrest|detain|caught|confiscat", na=False).astype(int)
        combined["topic_labor"] = t.str.contains(r"forced labor|forced labour|slave|traffick|abuse|exploit", na=False).astype(int)
        combined["topic_china"] = t.str.contains(r"china|chinese|beijing", na=False).astype(int)
        combined["topic_ais"] = t.str.contains(r"\bais\b|tracking|dark.*vessel|dark.*fleet|transponder|go.*dark", na=False).astype(int)
        combined["topic_subsidy"] = t.str.contains(r"subsid|wto|incentiv", na=False).astype(int)
        combined["topic_enforcement"] = t.str.contains(r"coast guard|navy|patrol|enforce|fine|penalty|prison|prosecut", na=False).astype(int)

    # Save raw
    combined.to_csv(partial_file, index=False)
    print(f"\nSaved raw: {partial_file}")

    # Save clean version
    keep_cols = [c for c in [
        "title", "url", "date", "year", "month", "year_month",
        "domain", "language", "sourcecountry",
        "query_name",
        "topic_iuu", "topic_seized", "topic_labor",
        "topic_china", "topic_ais", "topic_subsidy", "topic_enforcement",
    ] if c in combined.columns]

    clean = combined[keep_cols].copy()
    clean_path = os.path.join(OUTPUT_DIR, "gdelt_iuu_news_clean.csv")
    clean.to_csv(clean_path, index=False)
    print(f"Saved clean: {clean_path} ({len(clean)} articles)")

    # Summary
    print("\n=== Summary ===")
    if "year" in clean.columns:
        print("Articles by year:")
        print(clean.groupby("year").size().to_string())
    print(f"\nBy query:")
    if "query_name" in clean.columns:
        print(clean.groupby("query_name").size().to_string())
    print(f"\nTopic flags:")
    for col in [c for c in clean.columns if c.startswith("topic_")]:
        print(f"  {col}: {clean[col].sum()}")

    # Clean up progress file on full completion
    if done >= total_queries:
        print("\nAll queries completed!")
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)


if __name__ == "__main__":
    main()
