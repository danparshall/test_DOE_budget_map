# Data — structured tables derived from `papers/`

This directory contains queryable tables extracted from the DOE FY 2027 Congressional Justification corpus in `../papers/`. The companion `../PAPER_SUMMARIES.md` is the narrative summary of each source document; the tables here are for analysis.

Build scripts live in `../scripts/`. To rebuild a table, run its build script from the repo root:

```bash
python3 scripts/build_fy27_summary_by_org.py
python3 scripts/build_fy27_lab_summary.py
```

Each script runs reconciliation checks against the source document's printed totals before writing the CSV. If reconciliation fails, the script exits with a non-zero status and does **not** write the CSV — so any CSV present is by construction reconciled.

---

## `fy27_summary_by_org.csv`

**Source:** `papers/doe_fy27SummaryByOrg_2026.pdf` (DOE/CF, April 2026) — FY 2027 Summary Table by Organization. The structured form of the source PDF's 3-page office-by-office table. **76 rows** (leaves + nested subtotals + section totals + grand total).

**Build script:** `scripts/build_fy27_summary_by_org.py`

**Extraction provenance:** The source PDF uses a custom-encoded subset font with no `/ToUnicode` CMap, so `pdftotext` and `pymupdf` both return glyph indices rather than Unicode characters. Text was recovered via tesseract OCR at 300 DPI on rasterized pages. Every numeric cell in this CSV was either (a) transcribed verbatim from the OCR output where the OCR was unambiguous, or (b) verified against the rasterized PNG when the OCR contained suspicious characters. The build script encodes the values inline, so the source of truth is the script's `ROWS` list, not a regex over OCR output. One OCR error caught and corrected: Tribal Energy Loan Guarantee Program FY26→FY27 was reported as −65% in the OCR but the printed PDF shows −68% (the parser computes the percentage from the dollar values, so this is fixed by construction).

### Schema

| Column | Type | Description |
|---|---|---|
| `line` | str | Program / office / subtotal label as printed in the source |
| `fy25_enacted_k` | int | FY 2025 enacted, dollars in thousands. Negative for offset lines. |
| `fy26_enacted_k` | int | FY 2026 enacted, dollars in thousands. |
| `fy27_request_k` | int | FY 2027 President's Budget request, dollars in thousands. |
| `delta_k` | int | FY27 − FY26 (computed from columns above; not transcribed). |
| `pct_change` | float \| null | `(FY27 / FY26 − 1) × 100`, computed. Null when FY26 = 0 (the doc prints "N/A"). |
| `group` | str | Top-level grouping (see hierarchy below). |
| `subgroup` | str \| null | Second-level grouping for nested subtotals (Petroleum Reserves, Energy Dominance Financing, Power Marketing Administrations, Environmental Management). Null for rows outside a nested subtotal. |
| `level` | str | `leaf` (individual program), `subtotal` (nested rollup), `section_total` (top-level section rollup), `grand_total` (Total, Funding by Organization). |
| `footnote` | str \| null | Footnote markers from the source document (`4` = WFTC mandatory supplement note; `5` = AIQ repurposes IIJA; `6` = Baseload Power repurposes IIJA). |
| `notes` | str \| null | Analyst observations (cut percentages, office renamings, etc.). |

### Hierarchy

```
Grand Total — Total, Funding by Organization
├── NNSA (section_total)
│   ├── Federal Salaries and Expenses (leaf)
│   ├── Weapons Activities (leaf)
│   ├── Defense Nuclear Nonproliferation (leaf)
│   └── Naval Reactors (leaf)
├── Undersecretary for Science (section_total)
│   ├── Science (leaf)
│   ├── Artificial Intelligence and Quantum (leaf, new FY27)
│   ├── Office of Fusion (leaf, new FY27)
│   ├── Strategy & Technology Roadmaps (leaf, new FY27)
│   └── Office of Technology Commercialization (leaf)
├── Undersecretary for Energy (section_total)
│   ├── CESER, Nuclear Energy, NWDF, HGEO (4 leaves)
│   ├── Petroleum Reserves (subtotal) ← contains 4 leaves
│   ├── Electricity, Baseload Power, Indian Energy, OCED (4 leaves)
│   ├── Energy Dominance Financing (subtotal) ← contains 3 leaves
│   └── Power Marketing Administrations (subtotal) ← contains 5 leaves
├── Direct Reports (section_total)
│   ├── Environmental Management (subtotal) ← contains 4 leaves
│   └── ~25 other direct-report offices (CMEI, EHSS, ARPA-E, EIA, ...)
├── Other (Energy Projects — standalone, not in any subtotal)
└── Receipts and Offsets (section_total)
    ├── Excess Fees and Recovery, FERC
    ├── Title XVII Loan Guar. Prog Section 1703 Negative Credit Subsidy Receipt
    ├── UED&D Fund Offset
    ├── Sale of Northeast Home Heating Oil Reserve
    └── Repurposed IIJA Funding
```

Two structural facts worth noting:

1. **`Environmental Management` is a sub-category WITHIN `Direct Reports`**, not its own top-level section. (Direct Reports total = EM subtotal + ~25 non-EM offices.) This is the DOE org-chart convention — EM reports directly to the Secretary.
2. **`Energy Projects` is standalone** — it appears between Direct Reports and Receipts/Offsets visually in the source PDF but it is not part of either subtotal. The Grand Total formula is `NNSA + UndersecSci + UndersecEnergy + DirectReports + EnergyProjects + Offsets`.

### Common queries

```python
import pandas as pd
df = pd.read_csv("data/fy27_summary_by_org.csv")

# All leaf programs only (no subtotals/totals)
leaves = df[df["level"] == "leaf"]

# Largest cuts (FY27 vs FY26)
leaves.nsmallest(10, "delta_k")[["line", "fy26_enacted_k", "fy27_request_k", "delta_k", "pct_change"]]

# Largest percentage cuts (excluding new programs where FY26 was 0)
leaves[leaves["pct_change"].notna()].nsmallest(10, "pct_change")

# All NNSA programs
df[df["group"] == "NNSA"]

# All Undersecretary for Energy programs INCLUDING nested rollups
df[df["group"] == "Undersecretary for Energy"]

# Reconcile section totals
df[df["level"] == "section_total"]
```

---

## `fy27_lab_summary.csv`

**Source:** `papers/doe_fy27LaboratoryTables_2026.pdf` (DOE/CF-0229, April 2026), pages 1–3 — Laboratory Table Summary Report. The structured form of the lab/plant/installation-level aggregation. **94 rows**, one per LPI.

**Build script:** `scripts/build_fy27_lab_summary.py`

**Extraction provenance:** This PDF uses standard fonts with proper Unicode mapping (unlike the Summary by Organization), so `pdftotext -layout` extracts cleanly. The build script regex-parses the extracted text and validates against the document's printed `Total by Lab, Plant, and Installation` row.

### Schema

| Column | Type | Description |
|---|---|---|
| `lpi_name` | str | Laboratory, Plant, or Installation name as printed |
| `fy25_enacted_k` | int | FY 2025 enacted, dollars in thousands |
| `fy26_enacted_k` | int | FY 2026 enacted, dollars in thousands |
| `fy27_request_k` | int | FY 2027 President's Budget request, dollars in thousands |

### Coverage

The 94 LPIs include national labs (NNSA labs, Office of Science labs, NREL), Site Offices, Operations Offices, EM sites, SPR sites, Power Marketing Administration offices, and a handful of catch-all categories (`Other`, `Undesignated LPI`, `Washington Headquarters`). The full per-lab detail (sub-program breakdowns under each lab) lives in pages 4–124 of the source PDF and is **not** included here — see "Pending tables" below.

---

## `fy27_lab_by_office.csv`

**Source:** `papers/doe_fy27LaboratoryTables_2026.pdf`, all pages — `Subtotal, <office>` rows within each lab's table section. **347 rows** (one per (lab, office) cell where the lab receives money from that office). The lab × office matrix.

**Build script:** `scripts/build_fy27_lab_by_office.py`

**Extraction provenance:** Walks the text extraction line by line; matches `Subtotal, <office>  <fy25>  <fy26>  <fy27>` lines and `Total <lab>  <fy25>  <fy26>  <fy27>` lines (verified against T2's 94 lab names). For each lab, the script reconciles `sum(office subtotals) == T2 lab total` across all three fiscal years. The script writes the CSV only after reconciliation passes.

Two parsing complications, both handled explicitly:

1. **Nested sub-rollups within an office.** The PDF presents some office categories as parent + children — for example, `Subtotal, Petroleum Reserves` is the parent of `Subtotal, Strategic Petroleum Reserve` + `Subtotal, Naval Petroleum & Oil Shale Reserves` + `Subtotal, SPR Petroleum Account` + `Subtotal, Northeast Home Heating Oil Reserves`. Including both parent and children causes double-counting. The script skips the children (the parent IS the office-level rollup the matrix wants). Same for `(Gross)` and `(DA)` modifier variants on Departmental Administration and Office of Technology Commercialization. Skip list is hard-coded in the script and documented inline.

2. **Orphan leaves at Washington Headquarters and Undesignated LPI.** Two labs have rows that contribute to the lab total but are not under any `Subtotal, X` parent — e.g., Washington HQ has a direct `Energy Information Administration` leaf at $135M. Enumerating all such orphans (especially at Undesignated LPI, which has many) is brittle. Instead, the parser adds a synthetic `Other (not under office subtotal)` row per affected lab carrying the exact residual that makes the lab reconcile to T2. Currently 2 such residuals (Washington HQ: $135M/$135M/$138M; Undesignated LPI: $337M/$416M/$324M). The CSV is therefore 100% reconciled to T2 with the limitation visible in the `office` column.

### Schema

| Column | Type | Description |
|---|---|---|
| `lab_name` | str | Lab/plant/installation name (matches T2's `lpi_name`) |
| `office` | str | Office category (e.g., "Weapons Activities", "Science", "Critical Minerals and Energy Innovation"). The synthetic "Other (not under office subtotal)" value flags residual orphan-leaf money at Washington HQ and Undesignated LPI. |
| `fy25_enacted_k` | int | FY 2025 enacted, $ in thousands |
| `fy26_enacted_k` | int | FY 2026 enacted, $ in thousands |
| `fy27_request_k` | int | FY 2027 President's Budget request, $ in thousands |

### Coverage

- 93 labs (94 in T2 minus Battelle Savannah River Alliance which has $0 across all years)
- 37 distinct office categories
- All FY25/FY26/FY27 totals reconcile to T2 globally and per-lab

### Common queries

```python
import pandas as pd
df = pd.read_csv("data/fy27_lab_by_office.csv")

# How much does each office give Sandia in FY27?
df[df["lab_name"] == "Sandia National Laboratories"][["office", "fy27_request_k"]] \
    .sort_values("fy27_request_k", ascending=False)

# Pivot: full lab × office matrix
matrix = df.pivot_table(
    index="lab_name", columns="office", values="fy27_request_k",
    aggfunc="sum", fill_value=0
)

# Office totals across all labs (note: NOT the same as T1's office totals
# because T3 is gross BA, T1 is net discretionary — see gross-vs-net caveat below)
office_totals = df.groupby("office")["fy27_request_k"].sum().sort_values(ascending=False)
```

### Reconciliation to T1 (does NOT match exactly)

Summing T3 office totals does NOT exactly match T1's office-level numbers. T3 is gross budget authority at the lab level (per the source PDF's methodology); T1 is net discretionary from the Summary by Organization PDF. Example: T3 "Weapons Activities" sums to $27,400M FY27 across all labs; T1 "Weapons Activities" = $27,441M. The ~$41M gap likely lives in the gross-vs-net adjustments (supplements, offsets, mandatory transfers excluded from one view but not the other). For accurate office-level totals, use T1. T3 is the cross-section, not a substitute for T1.

---



## `fy27_science_by_lab_subprogram.csv`

**Source:** `papers/doe_fy27LaboratoryTables_2026.pdf`, per-lab sections (pp 4-124) — Office of Science sub-program rollup rows within each Science-funded lab. **139 rows** spanning the 35 Science-funded LPIs and 12 Science sub-programs.

**Build script:** `scripts/build_fy27_science_by_lab_subprogram.py`

**Extraction provenance:** Walks the text extract line-by-line; matches rollup rows whose label exactly matches one of the 12 canonical Science sub-program names (regex anchored to start-of-line, allowing leading whitespace, requiring 3 dollar values). The canonical-name approach exploits the source's consistent use of un-prefixed labels for rollup rows vs. `Research - X` or `Construction - X` prefixes for leaves — so no false matches from sub-leaves. Sub-programs that appear as single leaves without a separate rollup wrapper (Safeguards and Security - SC, Program Direction - SC, Workforce Development for Teachers & Scientists, at some labs) match the same pattern. Lab attribution uses the `Total <lab>` markers from T2's lab list.

**The 12 sub-programs captured:** ASCR, BES, BER, FES, HEP, NP, Isotope R&D and Production, Accelerator R&D and Production, Workforce Development for Teachers & Scientists, Science Laboratories Infrastructure, Safeguards and Security - SC, Program Direction - SC.

### Schema

| Column | Type | Description |
|---|---|---|
| `lab_name` | str | Lab/plant/installation name (matches T2's `lpi_name` and T3's `lab_name`) |
| `science_subprogram` | str | One of the 12 canonical sub-programs listed above |
| `fy25_enacted_k` | int | FY 2025 enacted, $ in thousands |
| `fy26_enacted_k` | int | FY 2026 enacted, $ in thousands |
| `fy27_request_k` | int | FY 2027 President's Budget request, $ in thousands |

### Coverage and reconciliation

- 35 Science-funded labs (= T3's count of rows with `office='Science'`)
- 12 distinct sub-programs, though no single lab carries all 12
- 139 rows: ASCR/BES/BER/FES/HEP/NP/SLI/S&S/PD/ARDAP/WDTS/IRP rollups attributed per lab where present
- All per-lab × per-year sums reconcile EXACTLY to T3's Science totals; global FY25/FY26/FY27 sums match T3's Science grand totals ($8.24B / $8.40B / $7.14B)

### Caveat: lab-axis (gross BA) view only — extramural not captured here

This is the **intramural** (lab-side) picture only — money attributed to the 17 DOE national labs plus catch-alls (`Other`, `Undesignated LPI`) plus co-located site offices. Office of Science also funds **extramural** research at universities, instrumentation grants, EFRCs, and fellowships — none of which appear in the Lab Tables source. The full Science org tree including the intramural/extramural split lives in the FY27 Science Volume CBJ (`papers/doe_fy27ScienceVolume_2026.pdf`, pending ingestion). When that lands, a companion T5b table will cover the extramural side. Until then, **this table understates Science cuts on the university side of the ledger**.

Additionally, the totals here are **gross BA at the lab axis** (matching T3), not the net-discretionary view in T1. T3 FY26 Science = $8.40B; T1 FY26 Science = $8.25B; the $150M delta is IIJA supplemental funding visible in Lab Tables but not in the discretionary org-axis. The FY27 request shows little supplemental delta ($7.14B gross ≈ $7.10B net), so the headline cut is similar in either view (−$1.26B/−15.0% gross, −$1.15B/−13.9% net).

### Common queries

```python
import pandas as pd
df = pd.read_csv("data/fy27_science_by_lab_subprogram.csv")

# Sub-program totals across all labs (FY26→FY27 deltas)
sub = df.groupby("science_subprogram").agg(
    fy26=("fy26_enacted_k","sum"),
    fy27=("fy27_request_k","sum"),
)
sub["delta_k"] = sub["fy27"] - sub["fy26"]
sub["pct_change"] = (sub["fy27"]/sub["fy26"] - 1) * 100
sub.sort_values("pct_change")

# Top labs by absolute Science cut FY26→FY27
lab = df.groupby("lab_name").agg(
    fy26=("fy26_enacted_k","sum"),
    fy27=("fy27_request_k","sum"),
)
lab["delta_k"] = lab["fy27"] - lab["fy26"]
lab.nsmallest(10, "delta_k")

# Where does the BES cut land? (lab-level)
df[df["science_subprogram"] == "Basic Energy Sciences"] \
    .sort_values("fy27_request_k", ascending=False)[
    ["lab_name", "fy26_enacted_k", "fy27_request_k"]
]
```

---

**The two CSVs answer different questions and do NOT sum to the same total.** Mixing them in a single visualization without normalization will mislead:

| | FY27 total | What it measures |
|---|---|---|
| `fy27_summary_by_org.csv` Grand Total | **$53,912,977k = $53.91B** | **Net** discretionary budget authority. Includes the −$5,417,127k Receipts and Offsets row. Matches the BiB topline. |
| `fy27_lab_summary.csv` sum | **$61,901,062k = $61.90B** | **Gross** budget authority at the lab level. Includes discretionary + supplemental funding. **Excludes** offsets, receipts, prior-year balances, deferrals, and rescissions (per the source document's own methodology note). |

The ~$8B gap is the supplements (WFTC mandatory $3.885B FY26 etc.) plus the offsets (Repurposed IIJA $4.7B FY27 etc.) that cancel out of the net but appear separately in the gross. Any budget-map artifact mixing the two axes needs to carry this reconciliation explicitly.

---

## Pending tables (not yet built)

- **Per-lab × per-sub-program detail across ALL offices (T4)** — pages 4–124 of `doe_fy27LaboratoryTables_2026.pdf` contain sub-program detail under each office subtotal (e.g., Argonne CMEI broken down into Vehicle Tech / Hydrogen / Solar / Wind / Hydropower / etc.). T3 captures the office-level rollup. The Science-only slice landed as `fy27_science_by_lab_subprogram.csv` (T5a) for the Science Volume Drill; the full T4 covering all offices (~3–5k rows) remains deferred until a specific use case requires it.
- **Science sub-program detail including extramural split (T5b)** — pending FY27 Science Volume CBJ paper-add. Will cover the intramural/extramural breakdown that T5a (lab-axis only) cannot.
- **BiB headline figures table** — small (~15 rows) Defense / Non-Defense / NNSA / Science / EM / etc. table from the BiB's overview. Mostly redundant with `fy27_summary_by_org.csv` rolled up to section level; build only if convenient framing for a deliverable.

---

## Provenance summary

| CSV | Source PDF | Source pages | Extraction method | Rows | Reconciliation |
|---|---|---|---|---|---|
| `fy27_summary_by_org.csv` | `doe_fy27SummaryByOrg_2026.pdf` | 1–3 | tesseract OCR @ 300 DPI + manual transcription (custom-font PDF defeated pdftotext) | 76 | 30 checks: 4 nested subtotals × 3 yrs + 5 section totals × 3 yrs + grand total × 3 yrs |
| `fy27_lab_summary.csv` | `doe_fy27LaboratoryTables_2026.pdf` | 1–3 | `pdftotext -layout` + regex | 94 | 1 check: sum of rows = printed total, × 3 yrs |
| `fy27_lab_by_office.csv` | `doe_fy27LaboratoryTables_2026.pdf` | 4–124 | `pdftotext -layout` + regex on `Subtotal,` lines, with skip rules for nested rollups and synthetic residual rows for orphan leaves | 347 | per-lab × 3 yrs: 93 labs × 3 yrs = 279 checks (plus global sum = T2 global sum, × 3 yrs) |
| `fy27_science_by_lab_subprogram.csv` | `doe_fy27LaboratoryTables_2026.pdf` | 4–124 | `pdftotext -layout` + regex matching the 12 canonical Science sub-program rollup names (anchored, requires 3 dollar values; leaf rows have `Research -`/`Construction -` prefixes that don't match) | 139 | per-lab × 3 yrs: 35 labs × 3 yrs = 105 checks (plus global sum = T3 Science grand total, × 3 yrs) |
