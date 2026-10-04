"""
Extract text from EJF PDFs, then parse into structured CSVs for Tableau text visualization.

Outputs in Project/text/EJF/:
  1. ejf_full_text.csv         — one row per page per PDF (for word clouds, topic modeling)
  2. ejf_testimonies.csv       — extracted fisher quotes with metadata (for sentiment, theme analysis)
  3. ejf_statistics.csv        — extracted numeric claims/stats (for annotation overlays)
"""

import os
import re
import fitz  # PyMuPDF
import pandas as pd
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EJF_DIR = os.path.join(SCRIPT_DIR, "EJF")

PDF_FILES = [
    ("Global-squid-report-2026_ENG.pdf", "Global Report 2026"),
    ("Unseen-and-unaccountable-squid-report.pdf", "Southeast Pacific 2025"),
    ("Unseen-and-unregulated.pdf", "Southwest Atlantic 2025"),
]

# ============================================================
# 1. Extract full text — one row per page
# ============================================================
def extract_full_text():
    print("=== 1/3  Extracting full text ===")
    rows = []
    for filename, report_name in PDF_FILES:
        path = os.path.join(EJF_DIR, filename)
        if not os.path.exists(path):
            print(f"  Skipping {filename} (not found)")
            continue
        doc = fitz.open(path)
        print(f"  {filename}: {len(doc)} pages")
        for i, page in enumerate(doc):
            text = page.get_text()
            if len(text.strip()) < 20:
                continue
            rows.append({
                "report": report_name,
                "filename": filename,
                "page": i + 1,
                "text": text.strip(),
                "char_count": len(text),
                "word_count": len(text.split()),
            })
        doc.close()

    df = pd.DataFrame(rows)
    out = os.path.join(EJF_DIR, "ejf_full_text.csv")
    df.to_csv(out, index=False)
    print(f"  Saved {out} ({len(df)} pages)\n")
    return df


# ============================================================
# 2. Extract testimonies / quotes
# ============================================================
def extract_testimonies(full_text_df):
    print("=== 2/3  Extracting testimonies ===")
    quotes = []

    all_text = "\n\n".join(full_text_df["text"].tolist())

    # Pattern 1: Text in quotes followed by attribution with nationality, flag, region, date
    # EJF format: "quote text" — Interview with [nationality] fisher... [flag]-flagged... [year]
    patterns = [
        # "quote" ... Interview with ... fisher ... flagged ... year
        r'["\u201c]([^"\u201d]{40,})["\u201d][^"]*?(?:Interview with|Testimony from)\s+(?:an?\s+)?(\w+)\s+fisher[^"]*?(\w+)[\s-]*flagged[^"]*?(\b20\d{2}\b)',
        # "quote" ... Indonesian/Filipino ... Chinese/Korean/Taiwanese ... 2022/2023/etc
        r'["\u201c]([^"\u201d]{40,})["\u201d][^"]*?(Indonesian|Filipino)\s+(?:fisher|crew)[^"]*?(Chinese|Korean|Taiwanese|Japanese)[^"]*?(\b20\d{2}\b)',
        # Simpler: long quoted text near a year
        r'["\u201c]([^"\u201d]{50,})["\u201d]',
    ]

    seen_quotes = set()

    for pattern in patterns[:2]:  # Use the specific patterns first
        for match in re.finditer(pattern, all_text, re.DOTALL | re.IGNORECASE):
            quote = match.group(1).strip()
            quote = re.sub(r'\s+', ' ', quote)  # normalize whitespace

            if quote in seen_quotes or len(quote) < 40:
                continue
            seen_quotes.add(quote)

            nationality = match.group(2).strip() if match.lastindex >= 2 else ""
            vessel_flag = match.group(3).strip() if match.lastindex >= 3 else ""
            year = match.group(4).strip() if match.lastindex >= 4 else ""

            quotes.append({
                "quote": quote,
                "nationality": nationality,
                "vessel_flag": vessel_flag,
                "year": year,
                "source": "pdf_extraction",
            })

    # Also grab longer quoted passages even without clear attribution
    for match in re.finditer(r'["\u201c]([^"\u201d]{60,300})["\u201d]', all_text):
        quote = re.sub(r'\s+', ' ', match.group(1).strip())
        if quote not in seen_quotes:
            seen_quotes.add(quote)
            quotes.append({
                "quote": quote,
                "nationality": "",
                "vessel_flag": "",
                "year": "",
                "source": "pdf_broad_extraction",
            })

    # Add the manual quotes we already have (known good ones from our earlier research)
    manual = [
        {"quote": "When we refused to fish, we got scolded and physically abused. We were kicked and hit. I experienced it often.",
         "nationality": "Indonesian", "vessel_flag": "Chinese", "year": "2022", "source": "manual",
         "region": "NWIO", "vessel_type": "light seiner"},
        {"quote": "A turtle was used as bait. It was only used once. The turtle was accidentally caught in the net, we wanted to help release it but the captain directed us to use it as bait. It was there for almost three months, the turtle was severely wounded.",
         "nationality": "Filipino", "vessel_flag": "Chinese", "year": "2023", "source": "manual",
         "region": "NWIO", "vessel_type": "light seiner"},
        {"quote": "Without any warning, he was immediately beaten, choked, and kicked. He was beaten up from the work area all the way down to the hold. The captain and the bosun acted like it was normal. One of them even laughed.",
         "nationality": "Indonesian", "vessel_flag": "Chinese", "year": "2025", "source": "manual",
         "region": "NWIO", "vessel_type": "light seiner"},
        {"quote": "Speaking of physical abuse, it was frequent. I almost saw it every day. A crew member who was still young, below 20 years old. He was frequently hit. Even his pants were once pulled until they ripped.",
         "nationality": "Indonesian", "vessel_flag": "Korean", "year": "2024", "source": "manual",
         "region": "SWA", "vessel_type": "squid vessel"},
        {"quote": "The bodies were sometimes thrown away, only the fins were taken. If they were all gathered, there would be a lot, probably around a ton. There really were quite a lot of them. They were put into sacks first before being stored in the freezer.",
         "nationality": "Indonesian", "vessel_flag": "Taiwanese", "year": "2023", "source": "manual",
         "region": "SWA", "vessel_type": "squid/saury vessel"},
    ]
    for m in manual:
        if m["quote"] not in seen_quotes:
            quotes.append(m)

    df = pd.DataFrame(quotes)

    # Add text analysis columns
    df["word_count"] = df["quote"].str.split().str.len()
    df["char_count"] = df["quote"].str.len()

    # Theme flags
    df["theme_violence"] = df["quote"].str.contains(
        r"beat|kick|hit|punch|choke|slap|abuse|assault|attack|threat", case=False, na=False
    ).astype(int)
    df["theme_wildlife"] = df["quote"].str.contains(
        r"shark|turtle|dolphin|whale|seal|fin|bycatch|endanger", case=False, na=False
    ).astype(int)
    df["theme_death"] = df["quote"].str.contains(
        r"\bdie\b|death|dead|kill|drown|body|bodies|burial", case=False, na=False
    ).astype(int)
    df["theme_wages"] = df["quote"].str.contains(
        r"wage|pay|money|salary|deduct|debt|unpaid|owe", case=False, na=False
    ).astype(int)
    df["theme_conditions"] = df["quote"].str.contains(
        r"hours|sleep|rest|food|water|sick|medicine|exhaust|overwork", case=False, na=False
    ).astype(int)
    df["theme_transshipment"] = df["quote"].str.contains(
        r"transship|transfer|reefer|carrier|supply vessel|at.sea", case=False, na=False
    ).astype(int)

    # Sentiment proxy: count negative vs positive words
    neg_words = r"abuse|violent|beat|kick|pain|suffer|fear|threat|force|cruel|die|death|illegal|exploit|trap"
    pos_words = r"help|safe|protect|rescue|good|friend|hope|improve|free"
    df["neg_word_count"] = df["quote"].str.lower().str.findall(neg_words).str.len()
    df["pos_word_count"] = df["quote"].str.lower().str.findall(pos_words).str.len()
    df["sentiment_score"] = df["pos_word_count"] - df["neg_word_count"]

    out = os.path.join(EJF_DIR, "ejf_testimonies.csv")
    df.to_csv(out, index=False)
    print(f"  Saved {out} ({len(df)} testimonies)\n")
    return df


# ============================================================
# 3. Extract statistics / numeric claims
# ============================================================
def extract_statistics(full_text_df):
    print("=== 3/3  Extracting statistics ===")
    stats = []
    all_text = "\n".join(full_text_df["text"].tolist())

    # Look for sentences containing percentages or large numbers near fishing keywords
    sentences = re.split(r'[.!?\n]', all_text)
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 20 or len(sent) > 500:
            continue

        has_number = bool(re.search(r'\d+[%,.]?\d*', sent))
        has_keyword = bool(re.search(
            r'fish|vessel|fleet|crew|worker|catch|labour|labor|abuse|shark|squid|IUU|mortality|death|interview',
            sent, re.IGNORECASE
        ))

        if has_number and has_keyword:
            # Extract the numeric values
            numbers = re.findall(r'(\d[\d,.]*\d|\d+)(?:\s*%)?', sent)
            stats.append({
                "statement": re.sub(r'\s+', ' ', sent),
                "numbers_found": "; ".join(numbers[:5]),
                "has_percentage": "%" in sent,
                "category": categorize_stat(sent),
            })

    df = pd.DataFrame(stats)
    df = df.drop_duplicates(subset="statement")

    out = os.path.join(EJF_DIR, "ejf_statistics.csv")
    df.to_csv(out, index=False)
    print(f"  Saved {out} ({len(df)} statistics)\n")
    return df


def categorize_stat(text):
    t = text.lower()
    if any(w in t for w in ["interview", "fisher", "crew", "worker"]):
        return "methodology"
    if any(w in t for w in ["abuse", "violen", "beat", "force", "labour", "labor"]):
        return "human_rights"
    if any(w in t for w in ["shark", "turtle", "bycatch", "species", "dolphin"]):
        return "environment"
    if any(w in t for w in ["vessel", "fleet", "flag", "registered"]):
        return "fleet_operations"
    if any(w in t for w in ["catch", "ton", "squid", "fish", "landing"]):
        return "fisheries"
    if any(w in t for w in ["transship", "port", "supply"]):
        return "supply_chain"
    return "other"


# ============================================================
# 4. Build word frequency table for word cloud
# ============================================================
def build_word_freq(full_text_df):
    print("=== Bonus: Building word frequency table ===")

    # Stopwords to exclude
    stopwords = set("""
        the a an and or but in on at to for of is it its was were be been being
        has have had do does did will would shall should may might can could
        this that these those with from by as are not no nor so if then than
        more most very also about up out into over after before between through
        during each all both other some such only own same which what when where
        who how their there here just even still already too much many any
        figure table page report section chapter see note above below source
        et al pp vol ed eds doi http https www com org pdf
        one two three four five six seven eight nine ten per cent
    """.split())

    all_text = " ".join(full_text_df["text"].tolist()).lower()
    # Remove non-alpha
    all_text = re.sub(r'[^a-z\s]', ' ', all_text)
    words = [w for w in all_text.split() if len(w) > 2 and w not in stopwords]

    freq = Counter(words)

    # Build bigrams
    bigrams = []
    word_list = all_text.split()
    filtered = [w for w in word_list if len(w) > 2 and w not in stopwords]
    for i in range(len(filtered) - 1):
        bigrams.append(f"{filtered[i]} {filtered[i+1]}")
    bigram_freq = Counter(bigrams)

    # Save unigrams
    uni_df = pd.DataFrame(freq.most_common(500), columns=["word", "count"])
    uni_path = os.path.join(EJF_DIR, "ejf_word_freq.csv")
    uni_df.to_csv(uni_path, index=False)
    print(f"  Saved {uni_path} ({len(uni_df)} words)")

    # Save bigrams
    bi_df = pd.DataFrame(bigram_freq.most_common(300), columns=["bigram", "count"])
    bi_path = os.path.join(EJF_DIR, "ejf_bigram_freq.csv")
    bi_df.to_csv(bi_path, index=False)
    print(f"  Saved {bi_path} ({len(bi_df)} bigrams)\n")


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("Extracting EJF report data for text visualization...\n")

    full_text = extract_full_text()
    testimonies = extract_testimonies(full_text)
    statistics = extract_statistics(full_text)
    build_word_freq(full_text)

    print("=" * 50)
    print("Done! Files in Project/text/EJF/:")
    print("  ejf_full_text.csv       — page-level text for topic analysis")
    print("  ejf_testimonies.csv     — structured quotes with theme flags")
    print("  ejf_statistics.csv      — numeric claims for annotations")
    print("  ejf_word_freq.csv       — top 500 words for word cloud")
    print("  ejf_bigram_freq.csv     — top 300 bigrams for word cloud")
