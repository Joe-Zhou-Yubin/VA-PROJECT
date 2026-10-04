# How to Access & Clean the Two Tier 1 Text Sources

Step-by-step guide for getting GDELT news articles and EJF fisher testimonies into a format ready for text visualization (word clouds, sentiment, topic analysis).

---

## Source 1: GDELT News Articles

### What you get
- Hundreds/thousands of news article records mentioning IUU fishing
- Each record has: **title**, **URL**, **date**, **tone** (sentiment score -100 to +100), **source domain**, **source country**, **language**
- Covers 2017–present, updated every 15 minutes

### Method A: GDELT DOC 2.0 Web Interface (Easiest — no code)

**Step 1:** Go to https://api.gdeltproject.org/api/v2/doc/doc

**Step 2:** Build your query URL directly in the browser. Format:

```
https://api.gdeltproject.org/api/v2/doc/doc?query=SEARCH_TERMS&mode=artlist&maxrecords=250&format=csv&sort=datedesc&startdatetime=YYYYMMDDHHMMSS&enddatetime=YYYYMMDDHHMMSS
```

**Step 3:** Run these queries (click each link or paste into browser):

**Query 1 — "Illegal fishing" articles (most recent 250):**
```
https://api.gdeltproject.org/api/v2/doc/doc?query=%22illegal%20fishing%22&mode=artlist&maxrecords=250&format=csv&sort=datedesc
```

**Query 2 — "IUU fishing" articles:**
```
https://api.gdeltproject.org/api/v2/doc/doc?query=%22IUU%20fishing%22&mode=artlist&maxrecords=250&format=csv&sort=datedesc
```

**Query 3 — "AIS" + "fishing vessel" articles:**
```
https://api.gdeltproject.org/api/v2/doc/doc?query=%22AIS%22%20%22fishing%20vessel%22&mode=artlist&maxrecords=250&format=csv&sort=datedesc
```

**Query 4 — "vessel seized" + fishing:**
```
https://api.gdeltproject.org/api/v2/doc/doc?query=%22vessel%20seized%22%20fishing&mode=artlist&maxrecords=250&format=csv&sort=datedesc
```

**Query 5 — "forced labor" + fishing:**
```
https://api.gdeltproject.org/api/v2/doc/doc?query=%22forced%20labor%22%20fishing&mode=artlist&maxrecords=250&format=csv&sort=datedesc
```

**Step 4:** Each returns a CSV. Save each one into `Project/text/gdelt/` as:
- `gdelt_illegal_fishing.csv`
- `gdelt_iuu_fishing.csv`
- `gdelt_ais_fishing_vessel.csv`
- `gdelt_vessel_seized.csv`
- `gdelt_forced_labor_fishing.csv`

**Step 5:** The CSV columns are:
```
url, url_mobile, title, seendate, socialimage, domain, language, sourcecountry
```

**Limitation:** The API returns max 250 records per query. To get more coverage, use time-windowed queries (see Method B) or the Python client.

### Method A+ : Tone Chart (Sentiment Data)

Change `mode=artlist` to `mode=tonechart` to get sentiment scores over time:

```
https://api.gdeltproject.org/api/v2/doc/doc?query=%22illegal%20fishing%22&mode=tonechart&format=csv
```

This returns date-bucketed tone averages — perfect for a Tableau line chart of media sentiment.

### Method B: Python Client (More records, scripted)

**Step 1:** Install the GDELT Python client:
```bash
pip install gdelt-doc-api
```

**Step 2:** Create a script `Project/text/fetch_gdelt.py`:

```python
from gdeltdoc import GdeltDoc, Filters
import pandas as pd

gd = GdeltDoc()

# Define search queries
queries = {
    "illegal_fishing": '"illegal fishing"',
    "iuu_fishing": '"IUU fishing"',
    "vessel_seized": '"vessel seized" fishing',
    "ais_disabled": '"AIS" disabled fishing',
    "forced_labor_fishing": '"forced labor" fishing',
    "dark_vessel": '"dark vessel" OR "dark fleet" fishing',
}

all_results = []

for name, query in queries.items():
    print(f"Fetching: {name}...")
    f = Filters(
        keyword=query,
        start_date="2020-01-01",
        end_date="2024-12-31",
        num_records=250,
    )
    articles = gd.article_search(f)
    if not articles.empty:
        articles["query_name"] = name
        all_results.append(articles)
        print(f"  Got {len(articles)} articles")

# Combine all results
df = pd.concat(all_results, ignore_index=True)

# Drop duplicates (same article matching multiple queries)
df = df.drop_duplicates(subset="url")

# Parse date
df["date"] = pd.to_datetime(df["seendate"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

# Save
df.to_csv("gdelt/gdelt_iuu_news_combined.csv", index=False)
print(f"\nSaved {len(df)} unique articles to gdelt/gdelt_iuu_news_combined.csv")
```

**Step 3:** Run it:
```bash
cd Project/text
mkdir gdelt
python fetch_gdelt.py
```

### Method C: GDELT Analysis Service (Visual + Export)

**Step 1:** Go to https://analysis.gdeltproject.org/

**Step 2:** This is a point-and-click interface. Select:
- **Tool:** "TimelineVol" for volume over time, or "WordCloud" for term frequency
- **Dataset:** "Global Knowledge Graph"
- **Query:** `"illegal fishing" OR "IUU fishing"`
- **Time range:** 2020-01-01 to 2024-12-31

**Step 3:** Click submit — results are emailed to you with CSV download links.

This is useful for getting pre-computed word clouds and timeline data without coding.

### Cleaning the GDELT Data for Tableau

Once you have the CSV(s), create a cleaning script `Project/text/clean_gdelt.py`:

```python
import pandas as pd

df = pd.read_csv("gdelt/gdelt_iuu_news_combined.csv")

# Parse date properly
df["date"] = pd.to_datetime(df["seendate"], errors="coerce")
df = df.dropna(subset=["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["year_month"] = df["date"].dt.to_period("M").astype(str)

# Clean source country (GDELT uses FIPS codes, not ISO3)
# Common mappings:
fips_to_name = {
    "US": "United States", "UK": "United Kingdom", "CH": "China",
    "AS": "Australia", "CA": "Canada", "SP": "Spain",
    "NZ": "New Zealand", "NO": "Norway", "JA": "Japan",
    "KS": "South Korea", "ID": "Indonesia", "TW": "Taiwan",
    "RS": "Russia", "FR": "France", "GM": "Germany",
}
df["source_country_name"] = df["sourcecountry"].map(fips_to_name).fillna(df["sourcecountry"])

# Extract key terms from titles for word cloud
# Tokenize titles
df["title_clean"] = df["title"].str.lower().str.replace(r"[^a-z\s]", "", regex=True)

# Flag articles by topic based on title keywords
df["topic_iuu"] = df["title"].str.contains("IUU|illegal.*fish", case=False, na=False).astype(int)
df["topic_seized"] = df["title"].str.contains("seize|apprehend|intercept|arrest", case=False, na=False).astype(int)
df["topic_labor"] = df["title"].str.contains("forced labor|slave|trafficking|abuse", case=False, na=False).astype(int)
df["topic_china"] = df["title"].str.contains("China|Chinese", case=False, na=False).astype(int)
df["topic_ais"] = df["title"].str.contains("AIS|tracking|dark.*vessel|dark.*fleet", case=False, na=False).astype(int)
df["topic_subsidy"] = df["title"].str.contains("subsid|WTO", case=False, na=False).astype(int)

# Save clean version for Tableau
keep_cols = [
    "title", "url", "date", "year", "month", "year_month",
    "domain", "language", "sourcecountry", "source_country_name",
    "query_name",
    "topic_iuu", "topic_seized", "topic_labor",
    "topic_china", "topic_ais", "topic_subsidy",
    "title_clean",
]
df[keep_cols].to_csv("gdelt/gdelt_clean_for_tableau.csv", index=False)
print(f"Saved {len(df)} records to gdelt/gdelt_clean_for_tableau.csv")
```

### What You Can Build in Tableau

| Visualization | Fields |
|---------------|--------|
| **Word Cloud** (via Tableau extension or export to external tool) | `title_clean` — tokenize and count words |
| **Article Volume Over Time** (line chart) | `year_month` on Columns, CNTD(url) on Rows |
| **Source Country Bar Chart** | `source_country_name` on Rows, CNTD(url) on Columns |
| **Topic Distribution** (stacked bar) | `year` on Columns, SUM of topic flags on Rows, stacked |
| **Domain Treemap** | `domain` on Color+Label, CNTD(url) on Size |

---

## Source 2: EJF Fisher Testimonies

### What you get
- Direct quotes from 430+ Indonesian and Filipino fishers
- Descriptions of conditions aboard Chinese, Taiwanese, and Korean squid vessels
- Rich qualitative text for word clouds, sentiment coding, theme extraction

### Step 1: Download the Full Report

**PDF link (direct download):**
```
https://ejfoundation.org/resources/downloads/Global-squid-report-2026_ENG.pdf
```

Also grab the two regional sub-reports:
```
https://ejfoundation.org/resources/downloads/Unseen-and-unaccountable-squid-report.pdf
https://ejfoundation.org/resources/downloads/Unseen-and-unregulated.pdf
```

Save all three into `Project/text/ejf/`:
- `Global-squid-report-2026_ENG.pdf`
- `Unseen-and-unaccountable-squid-report.pdf` (Southeast Pacific)
- `Unseen-and-unregulated.pdf` (Southwest Atlantic)

### Step 2: Extract Text from PDF

Use Python to extract the raw text:

```python
# pip install pymupdf
import fitz  # PyMuPDF
import os

pdf_files = [
    "ejf/Global-squid-report-2026_ENG.pdf",
    "ejf/Unseen-and-unaccountable-squid-report.pdf",
    "ejf/Unseen-and-unregulated.pdf",
]

for pdf_path in pdf_files:
    if not os.path.exists(pdf_path):
        print(f"  Skipping {pdf_path} (not found)")
        continue
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    txt_path = pdf_path.replace(".pdf", ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted {len(text):,} chars from {pdf_path} -> {txt_path}")
```

### Step 3: Extract Quotes Into a Structured CSV

The reports contain interview quotes in a recognizable format. Extract them:

```python
import re
import pandas as pd

quotes = []

for txt_file in [
    "ejf/Global-squid-report-2026_ENG.txt",
    "ejf/Unseen-and-unaccountable-squid-report.txt",
    "ejf/Unseen-and-unregulated.pdf.txt",
]:
    if not os.path.exists(txt_file):
        continue
    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Pattern: quoted text followed by attribution
    # EJF quotes typically in italics or quotation marks with "Interview with..." attribution
    pattern = r'"([^"]{30,})"[^"]*?(?:Interview with|Testimony from)[^"]*?(\w+)\s+fisher[^"]*?(\w+-flagged)[^"]*?(\d{4})'
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

    for quote, nationality, flag, year in matches:
        quotes.append({
            "quote": quote.strip(),
            "nationality": nationality.strip(),
            "vessel_flag": flag.strip(),
            "year": int(year),
            "source_file": txt_file,
        })

# If regex doesn't catch enough, manually extract from the summaries we already have
# Add the quotes from our 02_ejf file as fallback
manual_quotes = [
    {"quote": "When we refused to fish, we got scolded and physically abused. We were kicked and hit.",
     "nationality": "Indonesian", "vessel_flag": "Chinese-flagged", "year": 2022,
     "source_file": "manual", "region": "NWIO", "topic": "physical_abuse"},
    {"quote": "A turtle was used as bait. It was only used once. The turtle was accidentally caught in the net, we wanted to help release it but the captain directed us to use it as bait.",
     "nationality": "Filipino", "vessel_flag": "Chinese-flagged", "year": 2023,
     "source_file": "manual", "region": "NWIO", "topic": "wildlife"},
    {"quote": "Without any warning, he was immediately beaten, choked, and kicked. He was beaten up from the work area all the way down to the hold.",
     "nationality": "Indonesian", "vessel_flag": "Chinese-flagged", "year": 2025,
     "source_file": "manual", "region": "NWIO", "topic": "physical_abuse"},
    {"quote": "Speaking of physical abuse, it was frequent. I almost saw it every day. A crew member who was still young, below 20 years old. He was frequently hit. Even his pants were once pulled until they ripped.",
     "nationality": "Indonesian", "vessel_flag": "Korean-flagged", "year": 2024,
     "source_file": "manual", "region": "SWA", "topic": "physical_abuse"},
    {"quote": "The bodies were sometimes thrown away, only the fins were taken. If they were all gathered, there would be a lot, probably around a ton.",
     "nationality": "Indonesian", "vessel_flag": "Taiwanese-flagged", "year": 2023,
     "source_file": "manual", "region": "SWA", "topic": "shark_finning"},
]

df = pd.DataFrame(quotes + manual_quotes)

# Add text analysis columns
df["word_count"] = df["quote"].str.split().str.len()
df["mentions_violence"] = df["quote"].str.contains("beat|kick|hit|punch|choke|abuse|assault", case=False, na=False).astype(int)
df["mentions_wildlife"] = df["quote"].str.contains("shark|turtle|dolphin|whale|seal|fin", case=False, na=False).astype(int)
df["mentions_death"] = df["quote"].str.contains("die|death|dead|kill|drown", case=False, na=False).astype(int)
df["mentions_wages"] = df["quote"].str.contains("wage|pay|money|salary|deduct", case=False, na=False).astype(int)

df.to_csv("ejf/ejf_testimonies.csv", index=False)
print(f"Saved {len(df)} testimonies to ejf/ejf_testimonies.csv")
```

### What You Can Build in Tableau

| Visualization | Fields |
|---------------|--------|
| **Word Cloud** | Tokenize `quote` text, count term frequency |
| **Testimony Count by Flag State** (bar) | `vessel_flag` on Rows, CNTD on Columns, Color by `mentions_violence` |
| **Theme Distribution** (stacked bar) | `vessel_flag` on Columns, SUM of `mentions_violence/wildlife/death/wages` stacked |
| **Timeline of Testimonies** | `year` on Columns, CNTD on Rows — shows when abuse was documented |
| **Quote Length vs. Violence** (scatter) | `word_count` vs. count of violence keywords per quote |

---

## Folder Structure After Completion

```
Project/text/
├── TEXT_SOURCES.md
├── TEXT_VIZ_SOURCES_GUIDE.md      ← this file
├── examples/                       ← annotated summaries (already done)
│   ├── INDEX.md
│   └── 01-08 .md files
├── gdelt/                          ← GDELT news articles
│   ├── gdelt_illegal_fishing.csv   (raw from API)
│   ├── gdelt_iuu_fishing.csv
│   ├── gdelt_vessel_seized.csv
│   ├── gdelt_forced_labor_fishing.csv
│   └── gdelt_clean_for_tableau.csv (cleaned + topic-flagged)
├── ejf/                            ← EJF fisher testimonies
│   ├── Global-squid-report-2026_ENG.pdf
│   ├── Global-squid-report-2026_ENG.txt  (extracted)
│   ├── Unseen-and-unaccountable-squid-report.pdf
│   ├── Unseen-and-unregulated.pdf
│   └── ejf_testimonies.csv         (structured quotes)
├── fetch_gdelt.py                  ← download script
└── clean_gdelt.py                  ← cleaning script
```

## Priority Order

1. **GDELT** — do this first. Open the 5 browser links under Method A, save the CSVs, run the cleaning script. Gives you the most Tableau-ready text data with minimal effort.
2. **EJF** — download the 3 PDFs, run the extraction. The manual quotes from our existing notes are already a good start even before PDF extraction.
