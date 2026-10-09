"""Run the text viz notebook cells as a plain script (no Jupyter needed)."""
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os, re, shutil
from collections import Counter
from urllib.parse import urlparse

# Paths
PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TEXT = os.path.join(PROJECT, 'text')
DATASETS = os.path.join(PROJECT, 'datasets')
OUT = os.path.join(PROJECT, 'tableau', 'final', 'data')
IMG = os.path.join(PROJECT, 'tableau', 'final', 'attachments')
os.makedirs(OUT, exist_ok=True)
os.makedirs(IMG, exist_ok=True)

plt.rcParams.update({
    'figure.facecolor': '#0d1b2a', 'axes.facecolor': '#0d1b2a',
    'axes.edgecolor': '#4a5568', 'text.color': '#e0e0e0',
    'axes.labelcolor': '#e0e0e0', 'xtick.color': '#a0aec0',
    'ytick.color': '#a0aec0', 'font.size': 11, 'figure.dpi': 150,
})

print("Loading data...")
gdelt = pd.read_csv(os.path.join(TEXT, 'GDELT', 'gdelt_iuu_news_clean.csv'))
gdelt['date'] = pd.to_datetime(gdelt['date'], errors='coerce')
gdelt = gdelt.dropna(subset=['date'])
gdelt['quarter'] = gdelt['date'].dt.to_period('Q').astype(str)

testimonies = pd.read_csv(os.path.join(TEXT, 'EJF', 'ejf_testimonies.csv'))
word_freq = pd.read_csv(os.path.join(TEXT, 'EJF', 'ejf_word_freq.csv'))
bigram_freq = pd.read_csv(os.path.join(TEXT, 'EJF', 'ejf_bigram_freq.csv'))
iuu_idx = pd.read_csv(os.path.join(DATASETS, 'iuu_fishing_index.csv'))
print(f"  GDELT: {len(gdelt)}, EJF: {len(testimonies)}, Words: {len(word_freq)}, Bigrams: {len(bigram_freq)}, IUU Index: {len(iuu_idx)}")

# --- 2a. News volume ---
print("\n[2a] News volume over time...")
monthly = gdelt.groupby(['year_month', 'query_name']).size().reset_index(name='article_count')
fig, ax = plt.subplots(figsize=(14, 5))
for qname, grp in monthly.groupby('query_name'):
    ax.plot(grp['year_month'], grp['article_count'], marker='.', label=qname, alpha=0.8)
ax.set_xlabel('Month'); ax.set_ylabel('Articles')
ax.set_title('IUU Fishing News Volume by Query Group (GDELT)', fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=8)
ticks = sorted(monthly['year_month'].unique())
ax.set_xticks(ticks[::3]); ax.tick_params(axis='x', rotation=45)
plt.tight_layout(); fig.savefig(os.path.join(IMG, 'gdelt_news_volume.png'), bbox_inches='tight'); plt.close()
monthly.to_csv(os.path.join(OUT, 'gdelt_monthly_by_query.csv'), index=False)
print(f"  Saved gdelt_monthly_by_query.csv + gdelt_news_volume.png")

# --- 2b. Topics by year ---
print("[2b] Topics by year...")
topic_cols = [c for c in gdelt.columns if c.startswith('topic_')]
yearly_topics = gdelt.groupby('year')[topic_cols].sum().reset_index()
yearly_topics = yearly_topics[yearly_topics['year'] <= 2024]
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(yearly_topics)); width = 0.11
colors = ['#ff4444', '#ffaa00', '#ff6b9d', '#4fc3f7', '#66bb6a', '#ce93d8', '#ffb74d']
labels = [c.replace('topic_', '').title() for c in topic_cols]
for i, (col, label) in enumerate(zip(topic_cols, labels)):
    ax.bar(x + i * width, yearly_topics[col], width, label=label, color=colors[i], alpha=0.85)
ax.set_xlabel('Year'); ax.set_ylabel('Articles')
ax.set_title('Topic Prevalence in IUU News Coverage by Year', fontsize=14, fontweight='bold')
ax.set_xticks(x + width * 3); ax.set_xticklabels(yearly_topics['year'].astype(int))
ax.legend(fontsize=9, ncol=4); plt.tight_layout()
fig.savefig(os.path.join(IMG, 'gdelt_topics_by_year.png'), bbox_inches='tight'); plt.close()
yearly_topics.to_csv(os.path.join(OUT, 'gdelt_yearly_topics.csv'), index=False)
print(f"  Saved gdelt_yearly_topics.csv + gdelt_topics_by_year.png")

# --- 2c. Title word freq ---
print("[2c] Title word frequencies...")
stopwords = set('the a an and or but in on of to for is it that this was with as at by from are be has have had been its not will can do did may would should could about all also more than over into their they them some other which what when where who how new s t us said says after between most no so up out just these those he she we his her our if your my am were being each few many much two first one any'.split())
all_words = []
for title in gdelt['title'].dropna():
    words = re.findall(r'[a-z]+', title.lower())
    all_words.extend([w for w in words if w not in stopwords and len(w) > 2])
gdelt_words = pd.DataFrame(Counter(all_words).most_common(200), columns=['word', 'count'])
gdelt_words.to_csv(os.path.join(OUT, 'gdelt_title_word_freq.csv'), index=False)
print(f"  Saved gdelt_title_word_freq.csv (200 words)")

# --- 2d. Domain enrichment ---
print("[2d] Domain enrichment...")
def extract_domain(url):
    try: return urlparse(str(url)).netloc.replace('www.', '')
    except: return ''
tld_country = {'.uk':'UK','.au':'Australia','.ca':'Canada','.nz':'New Zealand','.in':'India',
    '.sg':'Singapore','.ph':'Philippines','.ng':'Nigeria','.za':'South Africa','.id':'Indonesia',
    '.jp':'Japan','.kr':'South Korea','.cn':'China','.tw':'Taiwan','.fr':'France','.de':'Germany',
    '.es':'Spain','.no':'Norway','.br':'Brazil','.ar':'Argentina','.mx':'Mexico'}
def guess_country(d):
    for tld, c in tld_country.items():
        if d.endswith(tld): return c
    return 'US/International' if d.endswith(('.com','.org','.net')) else 'Other'
gdelt['domain'] = gdelt['url'].apply(extract_domain)
gdelt['source_country'] = gdelt['domain'].apply(guess_country)
gdelt.to_csv(os.path.join(OUT, 'gdelt_enriched.csv'), index=False)
print(f"  Saved gdelt_enriched.csv ({len(gdelt)} rows)")

# --- 3a. EJF themes by flag ---
print("\n[3a] EJF themes by flag...")
t_flagged = testimonies.dropna(subset=['vessel_flag']).copy()
theme_cols = [c for c in t_flagged.columns if c.startswith('theme_')]
theme_by_flag = t_flagged.groupby('vessel_flag')[theme_cols].sum().T
theme_labels = [c.replace('theme_', '').replace('_', ' ').title() for c in theme_cols]
fig, ax = plt.subplots(figsize=(10, 6))
theme_by_flag.index = theme_labels
theme_by_flag.plot(kind='barh', ax=ax, color=['#ff4444', '#ffaa00', '#4fc3f7'], width=0.7)
ax.set_xlabel('Testimonies'); ax.set_title('Testimony Themes by Vessel Flag State', fontsize=14, fontweight='bold')
ax.legend(title='Vessel Flag'); plt.tight_layout()
fig.savefig(os.path.join(IMG, 'ejf_themes_by_flag.png'), bbox_inches='tight'); plt.close()
print(f"  Saved ejf_themes_by_flag.png")

# --- 3b. Bigrams ---
print("[3b] Top bigrams...")
top_bg = bigram_freq.head(25).copy()
fig, ax = plt.subplots(figsize=(10, 8))
clrs = ['#ff6b6b' if any(w in bg for w in ['forced','abuse','labour','slave','violence'])
        else '#ffaa00' if any(w in bg for w in ['iuu','illegal','poach','dark'])
        else '#4fc3f7' for bg in top_bg['bigram']]
ax.barh(top_bg['bigram'][::-1], top_bg['count'][::-1], color=clrs[::-1])
ax.set_xlabel('Frequency'); ax.set_title('Top 25 Bigrams in EJF Fisher Reports', fontsize=14, fontweight='bold')
plt.tight_layout(); fig.savefig(os.path.join(IMG, 'ejf_top_bigrams.png'), bbox_inches='tight'); plt.close()
print(f"  Saved ejf_top_bigrams.png")

# --- 3c. Sentiment ---
print("[3c] Sentiment scatter...")
flag_colors = {'Chinese': '#ff4444', 'Taiwanese': '#ffaa00', 'Korean': '#4fc3f7'}
fig, ax = plt.subplots(figsize=(8, 5))
t_sent = t_flagged[t_flagged['word_count'] < 500].copy()  # filter outliers
for flag, grp in t_sent.groupby('vessel_flag'):
    ax.scatter(grp['word_count'], grp['sentiment_score'], s=grp['neg_word_count']*20+30,
              c=flag_colors.get(flag,'#78909c'), alpha=0.6, label=flag, edgecolors='white', linewidth=0.5)
ax.axhline(y=0, color='#4a5568', linestyle='--', alpha=0.5)
ax.set_xlabel('Quote Length (words)'); ax.set_ylabel('Sentiment Score')
ax.set_title('Testimony Sentiment vs Length', fontsize=13, fontweight='bold')
ax.legend(); plt.tight_layout()
fig.savefig(os.path.join(IMG, 'ejf_sentiment_scatter.png'), bbox_inches='tight'); plt.close()
print(f"  Saved ejf_sentiment_scatter.png ({len(t_sent)} of {len(t_flagged)} testimonies, filtered word_count < 500)")

# --- 3d. Testimonies by year ---
print("[3d] Testimonies over time...")
yearly_test = t_flagged.groupby(['year', 'vessel_flag']).size().reset_index(name='count')
yearly_test = yearly_test[yearly_test['year'] <= 2025]
fig, ax = plt.subplots(figsize=(10, 5))
for flag, grp in yearly_test.groupby('vessel_flag'):
    offset = {'Chinese': -0.25, 'Taiwanese': 0, 'Korean': 0.25}.get(flag, 0)
    ax.bar(grp['year'] + offset, grp['count'], width=0.25, label=flag,
           color=flag_colors.get(flag, '#78909c'), alpha=0.85)
ax.set_xlabel('Year'); ax.set_ylabel('Testimonies')
ax.set_title('Fisher Testimonies by Year and Vessel Flag', fontsize=14, fontweight='bold')
ax.legend(); ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
plt.tight_layout(); fig.savefig(os.path.join(IMG, 'ejf_testimonies_by_year.png'), bbox_inches='tight'); plt.close()
print(f"  Saved ejf_testimonies_by_year.png")

# --- 4a. China trend + co-occurrence ---
print("\n[4a] China mentions + topic co-occurrence...")
yearly_china = gdelt[gdelt['year']<=2024].groupby('year').agg(total=('title','size'),china_mentions=('topic_china','sum')).reset_index()
yearly_china['china_pct'] = (yearly_china['china_mentions']/yearly_china['total']*100).round(1)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.bar(yearly_china['year'], yearly_china['china_pct'], color='#ff6b6b', alpha=0.8)
ax1.set_xlabel('Year'); ax1.set_ylabel('% Articles Mentioning China')
ax1.set_title('China in IUU News', fontsize=13, fontweight='bold')
ax1.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
for _, r in yearly_china.iterrows():
    ax1.text(r['year'], r['china_pct']+0.5, f"{r['china_pct']}%", ha='center', fontsize=9, color='#e0e0e0')
cooc = gdelt[topic_cols].corr()
im = ax2.imshow(cooc.values, cmap='RdYlBu_r', vmin=-0.2, vmax=0.5)
labs = [c.replace('topic_','') for c in topic_cols]
ax2.set_xticks(range(len(labs))); ax2.set_yticks(range(len(labs)))
ax2.set_xticklabels(labs, rotation=45, ha='right', fontsize=9); ax2.set_yticklabels(labs, fontsize=9)
ax2.set_title('Topic Co-occurrence', fontsize=13, fontweight='bold')
plt.colorbar(im, ax=ax2, shrink=0.8); plt.tight_layout()
fig.savefig(os.path.join(IMG, 'gdelt_china_and_cooccurrence.png'), bbox_inches='tight'); plt.close()
print(f"  Saved gdelt_china_and_cooccurrence.png")

# --- 4b. Precision check sample ---
print("[4b] Precision check sample...")
precision_samples = []
for topic in topic_cols:
    flagged = gdelt[gdelt[topic]==1]
    n = min(20, len(flagged))
    if n > 0:
        s = flagged.sample(n, random_state=42)[['title','url','query_name']].copy()
        s['topic_flag'] = topic.replace('topic_',''); s['correct'] = ''
        precision_samples.append(s)
precision_df = pd.concat(precision_samples, ignore_index=True)
precision_df.to_csv(os.path.join(OUT, 'gdelt_precision_check.csv'), index=False)
print(f"  Saved gdelt_precision_check.csv ({len(precision_df)} articles to review)")

# --- 5. Copy EJF + IUU Index ---
print("\n[5] Copying reference files...")
for f in ['ejf_testimonies.csv', 'ejf_word_freq.csv', 'ejf_bigram_freq.csv']:
    shutil.copy2(os.path.join(TEXT, 'EJF', f), os.path.join(OUT, f))
shutil.copy2(os.path.join(DATASETS, 'iuu_fishing_index.csv'), os.path.join(OUT, 'iuu_fishing_index.csv'))

print("\n=== OUTPUT FILES ===")
for f in sorted(os.listdir(OUT)):
    sz = os.path.getsize(os.path.join(OUT, f))
    print(f"  {f:45s} {sz:>10,} bytes")

print("\n=== IMAGE FILES ===")
for f in sorted(os.listdir(IMG)):
    if f.endswith('.png'):
        sz = os.path.getsize(os.path.join(IMG, f))
        print(f"  {f:45s} {sz:>10,} bytes")

print("\nDone!")
