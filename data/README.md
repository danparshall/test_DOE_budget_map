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

## Gross-vs-net reconciliation (critical caveat)

**The two CSVs answer different questions and do NOT sum to the same total.** Mixing them in a single visualization without normalization will mislead:

| | FY27 total | What it measures |
|---|---|---|
| `fy27_summary_by_org.csv` Grand Total | **$53,912,977k = $53.91B** | **Net** discretionary budget authority. Includes the −$5,417,127k Receipts and Offsets row. Matches the BiB topline. |
| `fy27_lab_summary.csv` sum | **$61,901,062k = $61.90B** | **Gross** budget authority at the lab level. Includes discretionary + supplemental funding. **Excludes** offsets, receipts, prior-year balances, deferrals, and rescissions (per the source document's own methodology note). |

The ~$8B gap is the supplements (WFTC mandatory $3.885B FY26 etc.) plus the offsets (Repurposed IIJA $4.7B FY27 etc.) that cancel out of the net but appear separately in the gross. Any budget-map artifact mixing the two axes needs to carry this reconciliation explicitly.

---

## Pending tables (not yet built)

- **Per-lab × per-program detail (T3)** — pages 4–124 of `doe_fy27LaboratoryTables_2026.pdf` contain a sub-program breakdown for every LPI (e.g., Argonne broken down into Basic Energy Sciences / High Energy Physics / CMEI subtotal / Subsurface Energy / etc.). This is the "expand the row" detail layer; ~3–5k rows total once flattened. Deferred until a specific use case requires it.
- **BiB headline figures table** — small (~15 rows) Defense / Non-Defense / NNSA / Science / EM / etc. table from the BiB's overview. Mostly redundant with `fy27_summary_by_org.csv` rolled up to section level; build only if convenient framing for a deliverable.

---

## Provenance summary

| CSV | Source PDF | Source pages | Extraction method | Rows | Reconciliation |
|---|---|---|---|---|---|
| `fy27_summary_by_org.csv` | `doe_fy27SummaryByOrg_2026.pdf` | 1–3 | tesseract OCR @ 300 DPI + manual transcription (custom-font PDF defeated pdftotext) | 76 | 30 checks: 4 nested subtotals × 3 yrs + 5 section totals × 3 yrs + grand total × 3 yrs |
| `fy27_lab_summary.csv` | `doe_fy27LaboratoryTables_2026.pdf` | 1–3 | `pdftotext -layout` + regex | 94 | 1 check: sum of rows = printed total, × 3 yrs |
