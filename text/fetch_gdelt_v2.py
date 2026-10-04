"""
GDELT DOC 2.0 fetcher v2 — slow and steady.

Key changes from v1:
  - Yearly windows instead of quarterly (30 requests instead of 120)
  - 10-second pause between requests (2x the minimum)
  - 90-second backoff on 429, doubling each retry
  - Saves after EVERY successful request so nothing is lost
  - Outputs both raw and clean CSVs

Run:  python fetch_gdelt_v2.py
Output: Project/text/GDELT/gdelt_iuu_news_raw.csv
        Project/text/GDELT/gdelt_iuu_news_clean.csv
"""

import os, time, json, requests, pandas as pd
from io import StringIO

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GDELT")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PROGRESS_FILE = os.path.join(OUTPUT_DIR, "_progress_v2.json")
RAW_FILE = os.path.join(OUTPUT_DIR, "gdelt_iuu_news_raw.csv")
CLEAN_FILE = os.path.join(OUTPUT_DIR, "gdelt_iuu_news_clean.csv")

API_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

PAUSE_BETWEEN = 10   # seconds between requests (2x the stated minimum)
BACKOFF_START = 90   # first retry wait on 429

QUERIES = {
    "illegal_fishing": '"illegal fishing" sourcelang:english',
    "iuu_fishing": '"IUU fishing" sourcelang:english',
    "forced_labor_fishing": '("forced labor" OR "forced labour") fishing vessel sourcelang:english',
    "vessel_seized": '("vessel seized" OR "boat seized") fishing sourcelang:english',
    "dark_fleet": '("dark fleet" OR "dark vessel" OR "AIS disabling") fishing sourcelang:english',
    "illegal_vessel": '("illegal vessel" OR "illegal trawler" OR "poaching vessel") sourcelang:english',
}

# Yearly windows — only 5 per query = 30 total requests
TIME_WINDOWS = []
for year in range(2020, 2025):
    TIME_WINDOWS.append((
        f"{year}0101000000",
        f"{year}1231235959",
        str(year),
    ))


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"completed": []}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def fetch_one(query, start_dt, end_dt, max_retries=4):
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
                wait = BACKOFF_START * (2 ** attempt)
                print(f"\n  429 rate limited. Waiting {wait}s (attempt {attempt+1}/{max_retries})...", flush=True)
                time.sleep(wait)
            else:
                print(f"\n  HTTP {resp.status_code}. Waiting 30s...", flush=True)
                time.sleep(30)
        except Exception as e:
            print(f"\n  Error: {e}. Waiting 30s...", flush=True)
            time.sleep(30)
    print(f"  FAILED after {max_retries} retries.", flush=True)
    return pd.DataFrame()


def build_clean(combined):
    combined.columns = [c.strip().lower() for c in combined.columns]

    if "url" in combined.columns:
        combined = combined.drop_duplicates(subset="url")

    date_col = "seendate" if "seendate" in combined.columns else "date"
    if date_col in combined.columns:
        combined["date"] = pd.to_datetime(combined[date_col], errors="coerce")
        combined["year"] = combined["date"].dt.year
        combined["month"] = combined["date"].dt.month
        combined["year_month"] = combined["date"].dt.to_period("M").astype(str)

    if "title" in combined.columns:
        combined["title"] = combined["title"].fillna("")
        t = combined["title"].str.lower()
        combined["topic_iuu"] = t.str.contains(r"iuu|illegal.*fish|unlawful.*fish|poach", na=False).astype(int)
        combined["topic_seized"] = t.str.contains(r"seize|apprehend|intercept|arrest|detain|caught|confiscat", na=False).astype(int)
        combined["topic_labor"] = t.str.contains(r"forced labor|forced labour|slave|traffick|abuse|exploit", na=False).astype(int)
        combined["topic_china"] = t.str.contains(r"china|chinese|beijing", na=False).astype(int)
        combined["topic_ais"] = t.str.contains(r"\bais\b|tracking|dark.*vessel|dark.*fleet|transponder", na=False).astype(int)
        combined["topic_subsidy"] = t.str.contains(r"subsid|wto|incentiv", na=False).astype(int)
        combined["topic_enforcement"] = t.str.contains(r"coast guard|navy|patrol|enforce|fine|penalty|prison|prosecut", na=False).astype(int)

    return combined


def main():
    progress = load_progress()
    completed_keys = set(progress["completed"])

    # Load existing raw results if resuming
    all_dfs = []
    if os.path.exists(RAW_FILE) and completed_keys:
        existing = pd.read_csv(RAW_FILE, low_memory=False)
        all_dfs.append(existing)
        print(f"Resuming: {len(completed_keys)} done, {len(existing)} articles loaded.\n")

    total = len(QUERIES) * len(TIME_WINDOWS)
    done = len(completed_keys)

    for query_name, query_str in QUERIES.items():
        print(f"\n=== {query_name} ===")
        for start_dt, end_dt, label in TIME_WINDOWS:
            key = f"{query_name}|{label}"
            if key in completed_keys:
                continue

            done += 1
            print(f"  [{done}/{total}] {label}...", end=" ", flush=True)

            df = fetch_one(query_str, start_dt, end_dt)

            if not df.empty:
                df["query_name"] = query_name
                df["period"] = label
                all_dfs.append(df)
                print(f"{len(df)} articles", flush=True)
            else:
                print("0 articles", flush=True)

            # Save progress immediately
            completed_keys.add(key)
            progress["completed"] = list(completed_keys)
            save_progress(progress)

            # Save raw CSV after every request
            if all_dfs:
                raw = pd.concat(all_dfs, ignore_index=True)
                raw.to_csv(RAW_FILE, index=False)

            # Pause
            print(f"    (waiting {PAUSE_BETWEEN}s...)", flush=True)
            time.sleep(PAUSE_BETWEEN)

    if not all_dfs:
        print("\nNo articles fetched.")
        return

    # Final combine + clean
    combined = pd.concat(all_dfs, ignore_index=True)
    combined.to_csv(RAW_FILE, index=False)
    print(f"\nRaw: {RAW_FILE} ({len(combined)} rows)")

    clean = build_clean(combined.copy())
    keep = [c for c in [
        "title", "url", "date", "year", "month", "year_month",
        "domain", "language", "sourcecountry", "query_name",
        "topic_iuu", "topic_seized", "topic_labor",
        "topic_china", "topic_ais", "topic_subsidy", "topic_enforcement",
    ] if c in clean.columns]
    clean[keep].to_csv(CLEAN_FILE, index=False)
    print(f"Clean: {CLEAN_FILE} ({len(clean[keep])} rows after dedup)")

    # Summary
    print("\n=== Summary ===")
    if "year" in clean.columns:
        print(clean.groupby("year").size().to_string())
    print(f"\nBy query: {clean.groupby('query_name').size().to_string()}")
    for col in [c for c in clean.columns if c.startswith("topic_")]:
        print(f"  {col}: {clean[col].sum()}")

    if done >= total and os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("\nAll done!")


if __name__ == "__main__":
    main()
