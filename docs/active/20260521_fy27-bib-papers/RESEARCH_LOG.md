# Research Log — FY27 BiB papers ingestion

This line collects sessions for ingesting the DOE FY2027 Budget-in-Brief corpus
into the repo's `papers/` library. It's a paper-ingestion task, not a research
inquiry per se; each session adds documents until the corpus is sufficient.

---

## Session: 2026-05-21 — `20260521_fy27-bib-papers`

### Topics Explored

- Repo configuration (set `workflow_mode: main_only`)
- Naming convention agreement (Protocol B, FY in ShortTitle, pub year)
- Landing-page hunt for Lab Tables URL (corrected singular → plural)
- Sandbox network constraints — confirmed empirically that in-chat allow-list
  changes do NOT propagate

### Provisional Findings

- DOE landing page: <https://www.energy.gov/cfo/articles/fy-2027-budget-justification>
- DOE document URLs use plural nouns even when the landing page labels singular ("Laboratory Tables", "State Tables")
- `paper-processing-institutional` Step 1 assumes its target domain is in the sandbox allow-list — worth a §7 issue upstream

### Results

None this session.

### Next Steps (for the fresh chat)

After §2 session-start (which will refetch STATUS.md and see `workflow_mode: main_only`),
read this section and pick up here:

**1. Verify connectivity to energy.gov.**

```bash
curl -sI -L -A "Mozilla/5.0" --max-time 15 \
  "https://www.energy.gov/cfo/articles/fy-2027-budget-justification" \
  | head -5
```

Expect `HTTP/2 200`. If you still get `403` with `x-deny-reason: host_not_allowed`,
the allow-list change still hasn't propagated — surface to Dan and don't proceed.

**2. Run `paper-processing-institutional` for each document below.** All three are
already triaged as Protocol B (no need to re-run `add-paper` Step 0):

| Filename (base — no `.pdf`)        | Source URL                                                              |
|------------------------------------|-------------------------------------------------------------------------|
| `doe_fy27BudgetInBrief_2026`       | <https://www.energy.gov/documents/doe-fy-2027-budget-brief>             |
| `doe_fy27SummaryByOrg_2026`        | <https://www.energy.gov/documents/doe-fy-2027-summary-table-organization> |
| `doe_fy27LaboratoryTables_2026`    | <https://www.energy.gov/documents/doe-fy-2027-laboratory-tables>        |

Skill Step 5 (BibTeX) is skipped — `BIB_FILE` is unset in STATUS.md.

**3. Confirm scope before pulling more.** The landing page lists ~25 documents
(Summary by Appropriation, State Tables, NNSA volumes, CMEI, HGEO, Science volumes,
EM, ARPA-E, etc.). Ask Dan before expanding beyond the initial three.

**4. Pre-discovered URLs ready for scope expansion** (don't fetch unless asked):

- <https://www.energy.gov/documents/doe-fy-2027-state-tables> (confirmed via search)
- `doe-fy-2027-summary-table-appropriation` (linked on landing page; pattern verified for siblings)
- `doe-fy-2027-statistical-tables` (likely — pattern is plural; not yet verified)

**5. Optional cleanup — draft a §7 upstream issue** about the
`paper-processing-institutional` Step 1 `curl` assumption. Dan declined to draft
it this session but it's a real skill gap. Body should describe the
`host_not_allowed` failure mode and suggest either (a) a `web_fetch` fallback in
the skill, or (b) a sandbox-aware banner.

### Skill state

- `add-paper` (triage) → routes to `paper-processing-institutional` (Protocol B)
- No need to re-triage in the fresh session; doc class is unambiguous for the entire BiB corpus.

---

## Session: 2026-05-21 — `20260521_fy27-bib-ingest`

Fresh chat opened after sandbox allow-list propagation. Connectivity verified
(`HTTP/2 200` from `energy.gov`). Picked up Next Steps from the
`20260521_fy27-bib-papers` setup session and executed the full ingest plus a
structured-data follow-on that wasn't in the original plan.

### Topics Explored

- Three-doc ingestion via `paper-processing-institutional` (Protocol B)
- OCR fallback for custom-encoded font PDFs (doc #2)
- Structured-table extraction (T1 + T2) with reconciliation against printed totals
- Office-rename cascade (EERE → CMEI, Fossil Energy → HGEO) traced at sub-program level
- Defense / Non-Defense rebalance ($41.38B / $12.53B FY27 vs $34.11B / $15.00B FY26)
- Science-vs-NNSA story visible at every level (office, lab)
- IIJA cancellation mechanics ($15.2B nominal; $4.7B reappears in FY27 offsets → AIQ + Baseload)

### Provisional Findings

- **BiB systematically obscures cuts.** Office of Science cut −13% framed as "investments in scientific discovery." CESER −16% framed as "$160 million to enhance security." Nuclear Energy −9% framed as "supporting the safe expansion." Indian Energy −33%, ARPA-E −43%, OE −22%, OCED eliminated. Budget map cannot trust the BiB narrative — only the line items.
- **CMEI is the deepest cut hiding behind a rename.** $3.10B FY25 → $1.88B FY26 → $1.12B FY27 = **−64% over two years**, the largest percentage cut among major offices, with sub-program reorganization documented in the Lab Tables' `(formerly X)` annotations.
- **Science-vs-NNSA story at lab level** is the cleanest visualization of the policy choice. ANL/LBNL/ORNL/BNL/SLAC/PNNL all cut 13–22%. LANL +32%, SNL +24%, LLNL +21%, Y-12 +5%, Pantex +15%, KCNSC +37%, NNSS +63%, NRF +41%, Savannah River +38%.
- **IIJA cancellation flow visible:** $15.2B nominal cancellation in BiB → $4.7B reappears in FY27 Receipts and Offsets as "Repurposed IIJA Funding" → reallocated to Baseload Power ($3.5B new) + AIQ ($1.2B new). Remaining ~$10.5B is pure rescission, not visible in this corpus.
- **AIQ money not where BiB implies.** BiB: "$1.2B AI supercomputers at Argonne and Oak Ridge." Lab Tables show ANL and ORNL *cut* (−17% and −16%); the $1.2B sits in Washington Headquarters (+37% to $8.03B) or Undesignated LPI (+125% to $6.04B). Has not yet been allocated to those labs in this document set.
- **Gross-vs-net reconciliation:** Lab Tables (gross BA) total $61.90B FY27; BiB / SummaryByOrg (net discretionary) total $53.91B FY27. ~$8B gap is supplements − offsets. Documented in `data/README.md`.

### Skill-gap findings (queued for upstream issue)

- **`paper-processing-institutional` Step 2 needs an OCR fallback.** Doc #2 (`SummaryByOrg`) used a custom subset font with no `/ToUnicode` CMap. `pdftotext` and `pymupdf` both returned glyph indices. Worked: `pdftoppm -r 300 -png` → `tesseract`. Symptom is identifiable (control chars U+0010–U+001F mixed with printable bytes in the first ~20 lines), so the skill's existing "verify the extraction is reasonable" caught it — but no documented fallback path.
- **`paper-processing-institutional` Step 1 sandbox allow-list assumption** — carried over from setup session. Two real gaps in the institutional skill; one upstream issue covers both plus the OCR-vs-printed-percentage data-quality finding below.
- **OCR-vs-printed-percentage data quality:** Tribal Energy Loan Guarantee Program FY26→FY27 was OCR'd as `-65%`; PNG verification shows printed value is `-68%`. Build script computes pct from dollar values, so the CSV is right by construction — but if a future analyst takes printed percentages at face value, that's a class of error to watch for.

### Results

**Papers ingested (3 docs, 12 commits):**

| Filename                            | Pages | Extraction         | Commits |
|-------------------------------------|-------|--------------------|---------|
| `doe_fy27BudgetInBrief_2026.pdf`    | ~80   | pdftotext (clean)  | 4 (57800b0 / aa11e7d / 9bcba75 / 82dff9f) |
| `doe_fy27SummaryByOrg_2026.pdf`     | 3     | tesseract OCR @ 300 DPI (custom font defeated pdftotext) | 4 (292feeb / db00918 / 434fe73 / 8caed90) |
| `doe_fy27LaboratoryTables_2026.pdf` | 124   | pdftotext (clean)  | 4 (954d931 / d03f708 / dc1445a / b653bee) |

**Structured tables built (T1 + T2, 5 commits):**

- `data/fy27_summary_by_org.csv` — **76 rows** × 11 cols (line, FY25/26/27 $k, delta, pct, group, subgroup, level, footnote, notes). All 30 reconciliation checks pass against printed subtotals + grand total.
- `data/fy27_lab_summary.csv` — **94 rows** × 4 cols (lpi_name, FY25/26/27 $k). Reconciles to printed lab-table total ($61,901,062k FY27).
- `scripts/build_fy27_summary_by_org.py` — manual-transcription parser with full reconciliation tree (Petroleum / EDF / PMA / EM nested subtotals + 5 section totals + grand total).
- `scripts/build_fy27_lab_summary.py` — regex parser over `pdftotext -layout` output.
- `data/README.md` — schema, provenance, hierarchy diagram, **gross-vs-net caveat** between T1 ($53.91B net) and T2 ($61.90B gross).

**Structured tables T3 + first budget-map artifact:** see commits below this session entry's date.

### Next Steps (for the next session)

The three-doc starter ingest is complete and structured. The corpus supports a first-pass budget map. Probable next directions:

1. **Decide on scope expansion.** Pre-discovered URLs still queued: `doe-fy-2027-state-tables` (geographic cut), `doe-fy-2027-summary-table-appropriation` (appropriation-axis), `doe-fy-2027-statistical-tables`. Don't pull without specific use case.
2. **Per-volume JEDIs.** The Science volume (separate document not yet ingested) is where the −13% Science cut breaks down by sub-program. Would resolve the question of which sub-programs absorb the cut and where the AIQ $1.2B actually ends up.
3. **Track remaining ~$10.5B IIJA rescission** outside this document set. Likely in a separate cancellation schedule (look for "rescission" or "cancellation" docs on the FY27 landing page).
4. **Resolve "Undesignated LPI" growth.** +$3.36B / +125% in Lab Tables, likely contains some of AIQ and Baseload Power before lab allocation. Worth tracing once the Science / NE volumes are in the library.
5. **Build T3 (per-lab × per-program detail) for specific drill-downs** once a question motivates it.

### Skill state

- `add-paper` triage → `paper-processing-institutional` Protocol B, doc class unambiguous for entire BiB corpus.
- §7 upstream issue drafted this session (combines all three skill-gap findings).
