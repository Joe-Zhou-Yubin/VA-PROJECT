"""Plot Google Ngram data — improved version with better segregation and labelling."""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os, shutil

base = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base, "google_ngram_iuu.csv"))
IMG = os.path.join(base, "..", "tableau", "final", "attachments")
OUT = os.path.join(base, "..", "tableau", "final", "data")
os.makedirs(IMG, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

BG = '#0d1b2a'
GRID = '#1b2838'
TEXT = '#e0e0e0'
MUTED = '#607080'

plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': BG,
    'axes.edgecolor': '#2a3a4a', 'text.color': TEXT,
    'axes.labelcolor': TEXT, 'xtick.color': '#8899aa',
    'ytick.color': '#8899aa', 'font.size': 10, 'figure.dpi': 180,
    'axes.grid': True, 'grid.color': GRID, 'grid.alpha': 0.5,
    'grid.linewidth': 0.5,
})

focus = df[df['year'] >= 1970].copy()

# ─── Chart 1: Three-panel faceted view ───────────────────────────────
# Split terms into 3 groups so lines don't overlap
fig, axes = plt.subplots(3, 1, figsize=(13, 10), sharex=True)
fig.suptitle('IUU Fishing Concepts in Published Literature (Google Books, 1970–2019)',
             fontsize=14, fontweight='bold', y=0.98)

# Panel A: The big picture (aquaculture dominates — give it its own panel)
ax = axes[0]
for term, color, ls in [
    ('aquaculture', '#4fc3f7', '-'),
    ('fisheries management', '#66bb6a', '--'),
    ('marine conservation', '#90caf9', ':'),
]:
    grp = focus[focus['term'] == term]
    ax.plot(grp['year'], grp['frequency_ppm'], label=term, color=color,
            linewidth=2.2, linestyle=ls)
    # End-of-line label
    last = grp.iloc[-1]
    ax.text(last['year'] + 0.8, last['frequency_ppm'], term,
            fontsize=8, color=color, va='center')
ax.set_ylabel('ppm')
ax.set_title('Industry & Policy Terms', fontsize=11, loc='left', color=MUTED)
ax.legend().set_visible(False)  # using end-of-line labels instead

# Panel B: The problem terms
ax = axes[1]
for term, color, ls in [
    ('overfishing', '#ff4444', '-'),
    ('bycatch', '#ffb74d', '-'),
    ('fish stocks', '#ce93d8', '--'),
]:
    grp = focus[focus['term'] == term]
    ax.plot(grp['year'], grp['frequency_ppm'], label=term, color=color,
            linewidth=2.2, linestyle=ls)
    last = grp.iloc[-1]
    ax.text(last['year'] + 0.8, last['frequency_ppm'], term,
            fontsize=8, color=color, va='center')
ax.set_ylabel('ppm')
ax.set_title('Problem Recognition', fontsize=11, loc='left', color=MUTED)
# Annotate key moment
peak_yr = 1996
ax.axvline(peak_yr, color='#ffffff', alpha=0.15, linewidth=0.8)
ax.annotate('Peak concern\n~1996', xy=(peak_yr, 0.5), xytext=(1983, 0.55),
            fontsize=8, color='#8899aa',
            arrowprops=dict(arrowstyle='->', color='#8899aa', lw=0.7))

# Panel C: IUU-specific terms (the ones that matter most to our project)
ax = axes[2]
for term, color, ls, lw in [
    ('IUU fishing', '#ff6b6b', '-', 2.8),
    ('illegal fishing', '#ffaa00', '-', 2.8),
    ('forced labour fishing', '#ef5350', '--', 1.8),
]:
    grp = focus[focus['term'] == term]
    ax.plot(grp['year'], grp['frequency_ppm'], label=term, color=color,
            linewidth=lw, linestyle=ls)
    last = grp.iloc[-1]
    ax.text(last['year'] + 0.8, last['frequency_ppm'], term,
            fontsize=8, color=color, va='center')
ax.set_ylabel('ppm')
ax.set_xlabel('Year')
ax.set_title('IUU & Enforcement Terms', fontsize=11, loc='left', color=MUTED)

# Annotate milestones
annotations = [
    (1995, 'UN Fish Stocks\nAgreement'),
    (2001, 'FAO IPOA-IUU\nAction Plan'),
    (2009, 'EU IUU\nRegulation'),
    (2016, 'Port State\nMeasures Agreement'),
]
for yr, label in annotations:
    val = focus[(focus['term'] == 'IUU fishing') & (focus['year'] == yr)]['frequency_ppm']
    if len(val) > 0:
        ax.axvline(yr, color='#ffffff', alpha=0.12, linewidth=0.8)
        ax.annotate(label, xy=(yr, val.values[0]),
                   xytext=(yr, ax.get_ylim()[1] * 0.85),
                   fontsize=7, color='#8899aa', ha='center',
                   arrowprops=dict(arrowstyle='->', color='#8899aa', lw=0.6))

for a in axes:
    a.set_xlim(1970, 2022)  # extra space for end-of-line labels
    a.tick_params(axis='both', labelsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(IMG, 'google_ngram_all_terms.png'), bbox_inches='tight')
plt.close()
print("Saved: google_ngram_all_terms.png")

# ─── Chart 2: The IUU story (single focused panel) ───────────────────
fig, ax = plt.subplots(figsize=(13, 5))

# Shade eras
ax.axvspan(1970, 1992, alpha=0.04, color='#4fc3f7', label='_')
ax.axvspan(1992, 2005, alpha=0.04, color='#ffaa00', label='_')
ax.axvspan(2005, 2019, alpha=0.04, color='#ff6b6b', label='_')
ax.text(1981, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 0.15,
        'Era of Discovery', fontsize=9, color='#4a6a8a', ha='center', style='italic')
ax.text(1998.5, 0.15, 'Era of Alarm', fontsize=9, color='#8a6a3a', ha='center', style='italic')
ax.text(2012, 0.15, 'Era of Action', fontsize=9, color='#8a4a4a', ha='center', style='italic')

terms_focus = [
    ('overfishing', '#ff4444', '-', 2.5, True),
    ('IUU fishing', '#ff6b6b', '-', 2.5, True),
    ('illegal fishing', '#ffaa00', '-', 2.5, True),
    ('bycatch', '#ffb74d', '--', 1.5, False),
    ('fish stocks', '#ce93d8', ':', 1.5, False),
]

for term, color, ls, lw, bold in terms_focus:
    grp = focus[focus['term'] == term]
    alpha = 1.0 if bold else 0.5
    ax.plot(grp['year'], grp['frequency_ppm'], label=term, color=color,
            linewidth=lw, linestyle=ls, alpha=alpha)
    # End-of-line label
    last = grp.iloc[-1]
    ax.annotate(term, xy=(last['year'], last['frequency_ppm']),
               xytext=(last['year'] + 1, last['frequency_ppm']),
               fontsize=9 if bold else 7.5, color=color,
               fontweight='bold' if bold else 'normal', va='center')

# Milestone markers
milestones = [
    (1995, 'UN Fish Stocks Agreement', '△'),
    (2001, 'FAO IPOA-IUU', '◇'),
    (2009, 'EU IUU Regulation', '□'),
    (2016, 'PSMA enters force', '○'),
]
for yr, label, marker in milestones:
    ax.axvline(yr, color='#ffffff', alpha=0.1, linewidth=0.7)
    ax.text(yr, -0.018, f'{yr}', fontsize=7, color='#6a7a8a',
            ha='center', transform=ax.get_xaxis_transform())

ax.set_xlabel('Year')
ax.set_ylabel('Frequency in Books (parts per million)')
ax.set_title('The Rise of IUU Fishing as a Global Concern (Google Books Ngram)',
             fontsize=13, fontweight='bold')
ax.set_xlim(1970, 2023)
ax.set_ylim(bottom=0)

# Custom legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='#ff4444', lw=2.5, label='overfishing'),
    Line2D([0], [0], color='#ff6b6b', lw=2.5, label='IUU fishing'),
    Line2D([0], [0], color='#ffaa00', lw=2.5, label='illegal fishing'),
    Line2D([0], [0], color='#ffb74d', lw=1.5, ls='--', alpha=0.5, label='bycatch'),
    Line2D([0], [0], color='#ce93d8', lw=1.5, ls=':', alpha=0.5, label='fish stocks'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=8,
          framealpha=0.3, edgecolor='#2a3a4a')

plt.tight_layout()
fig.savefig(os.path.join(IMG, 'google_ngram_iuu_focus.png'), bbox_inches='tight')
plt.close()
print("Saved: google_ngram_iuu_focus.png")

# ─── Copy CSV ─────────────────────────────────────────────────────────
shutil.copy2(os.path.join(base, "google_ngram_iuu.csv"),
             os.path.join(OUT, "google_ngram_iuu.csv"))
print("Copied: google_ngram_iuu.csv")
print("Done!")
