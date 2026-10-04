from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from urllib.parse import quote
import os

QUERIES = {
    "illegal_fishing": '"illegal fishing" sourcelang:english',
    "iuu_fishing": '"IUU fishing" sourcelang:english',
    "forced_labor_fishing": '("forced labor" OR "forced labour" OR "slave labor") fishing vessel sourcelang:english',
    "vessel_seized": '("vessel seized" OR "vessel apprehended" OR "boat seized") fishing sourcelang:english',
    "dark_fleet": '("dark fleet" OR "dark vessel" OR "AIS disabled" OR "AIS disabling") fishing sourcelang:english',
    "illegal_vessel": '("illegal vessel" OR "illegal trawler" OR "poaching vessel") sourcelang:english',
}

TIME_WINDOWS = []
for year in range(2020, 2025):
    TIME_WINDOWS.append(
        (f"{year}0101000000", f"{year}1231235959", str(year))
    )

API_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"

wb = Workbook()
ws = wb.active
ws.title = "GDELT Queries"

header_font = Font(name="Arial", bold=True, color="FFFFFF", size=11)
header_fill = PatternFill("solid", fgColor="2F5496")
header_align = Alignment(horizontal="center", vertical="center")
link_font = Font(name="Arial", color="0563C1", underline="single", size=10)
done_fill = PatternFill("solid", fgColor="C6EFCE")
normal_font = Font(name="Arial", size=10)
thin_border = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9"),
)

headers = ["#", "Query Group", "Period", "Start Date", "End Date", "API Link (click to open in browser)", "Done?", "Articles Found"]
ws.append(headers)

for col_idx in range(1, len(headers) + 1):
    cell = ws.cell(row=1, column=col_idx)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_align
    cell.border = thin_border

ws.column_dimensions["A"].width = 5
ws.column_dimensions["B"].width = 22
ws.column_dimensions["C"].width = 10
ws.column_dimensions["D"].width = 12
ws.column_dimensions["E"].width = 12
ws.column_dimensions["F"].width = 85
ws.column_dimensions["G"].width = 8
ws.column_dimensions["H"].width = 15

ws.auto_filter.ref = f"A1:H1"
ws.freeze_panes = "A2"

row_num = 1
for query_name, query_str in QUERIES.items():
    for start_dt, end_dt, period_label in TIME_WINDOWS:
        row_num += 1
        url = f"{API_BASE}?query={quote(query_str)}&mode=artlist&maxrecords=250&format=csv&sort=datedesc&startdatetime={start_dt}&enddatetime={end_dt}"
        display_start = f"{start_dt[:4]}-{start_dt[4:6]}-{start_dt[6:8]}"
        display_end = f"{end_dt[:4]}-{end_dt[4:6]}-{end_dt[6:8]}"

        ws.cell(row=row_num, column=1, value=row_num - 1).font = normal_font
        ws.cell(row=row_num, column=2, value=query_name).font = normal_font
        ws.cell(row=row_num, column=3, value=period_label).font = normal_font
        ws.cell(row=row_num, column=4, value=display_start).font = normal_font
        ws.cell(row=row_num, column=5, value=display_end).font = normal_font

        link_cell = ws.cell(row=row_num, column=6)
        link_cell.value = url
        link_cell.hyperlink = url
        link_cell.font = link_font

        ws.cell(row=row_num, column=7, value="").font = normal_font
        ws.cell(row=row_num, column=8, value="").font = normal_font

        for col_idx in range(1, len(headers) + 1):
            ws.cell(row=row_num, column=col_idx).border = thin_border
            ws.cell(row=row_num, column=col_idx).alignment = Alignment(vertical="center")

# Summary sheet
ws2 = wb.create_sheet("Summary")
ws2.append(["Query Group", "Description", "Total Links", "Example Search Terms"])
for col_idx in range(1, 5):
    cell = ws2.cell(row=1, column=col_idx)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_align

descriptions = {
    "illegal_fishing": ("Articles mentioning illegal fishing broadly", '"illegal fishing"'),
    "iuu_fishing": ("Articles specifically about IUU fishing", '"IUU fishing"'),
    "forced_labor_fishing": ("Forced/slave labour on fishing vessels", '"forced labor" OR "forced labour" + fishing vessel'),
    "vessel_seized": ("Enforcement actions, vessel seizures", '"vessel seized" OR "vessel apprehended" + fishing'),
    "dark_fleet": ("AIS disabling, dark vessels/fleets", '"dark fleet" OR "AIS disabled" + fishing'),
    "illegal_vessel": ("Illegal trawlers, poaching vessels", '"illegal vessel" OR "illegal trawler" OR "poaching vessel"'),
}

for i, (qname, (desc, terms)) in enumerate(descriptions.items(), start=2):
    ws2.cell(row=i, column=1, value=qname).font = normal_font
    ws2.cell(row=i, column=2, value=desc).font = normal_font
    ws2.cell(row=i, column=3, value=20).font = normal_font
    ws2.cell(row=i, column=4, value=terms).font = normal_font

ws2.column_dimensions["A"].width = 22
ws2.column_dimensions["B"].width = 45
ws2.column_dimensions["C"].width = 12
ws2.column_dimensions["D"].width = 55

# Instructions sheet
ws3 = wb.create_sheet("Instructions")
ws3.column_dimensions["A"].width = 100
instructions = [
    "GDELT Query Links — How to Use",
    "",
    "1. Go to the 'GDELT Queries' tab. There are 120 links (6 query groups x 20 quarters).",
    "2. Click a link in column F — it opens in your browser and downloads a CSV.",
    "3. Save the CSV into: Project/text/GDELT/raw/",
    "4. Suggested naming: {query_group}_{period}.csv  (e.g. illegal_fishing_2020-Q1.csv)",
    "5. Mark column G as done and note the article count in column H.",
    "6. Each link returns max 250 articles. If a query returns exactly 250, it may be truncated.",
    "",
    "Tips:",
    "- Work through one query group at a time (filter column B).",
    "- If a link returns a blank page or error, wait 60 seconds and retry (rate limit).",
    "- The two most important groups are: illegal_fishing and iuu_fishing.",
    "- forced_labor_fishing and vessel_seized are the next priority.",
    "",
    "After downloading all CSVs, run the merge script to combine them into one clean file.",
]
for i, line in enumerate(instructions, start=1):
    cell = ws3.cell(row=i, column=1, value=line)
    cell.font = Font(name="Arial", bold=(i == 1), size=12 if i == 1 else 10)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GDELT_Query_Links_v2.xlsx")
wb.save(out_path)
print(f"Saved: {out_path}")
print(f"Total links: {row_num - 1}")
