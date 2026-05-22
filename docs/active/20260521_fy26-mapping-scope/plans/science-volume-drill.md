# Science Volume Drill — Implementation Plan

**Goal:** Map where the FY27 −13.9% Office of Science cut request lands at sub-program and lab level, producing structured data plus a focused analytical artifact.

**Originating conversation:** `docs/active/20260521_fy26-mapping-scope/convos/20260521_fy26-mapping-scope.md`

**Context:** The FY27 request proposes cutting Office of Science from $8.25B (FY26 enacted) to ~$7.10B (FY27 request) — a ~$1.15B / −13.9% reduction. The cut is almost certainly non-uniform: ASCR (Advanced Scientific Computing Research) houses the exascale/AI/quantum portfolio prioritized by the administration; the basic research programs (BES, BER, FES, HEP, NP) likely bear the cut. T1/T2/T3 show Science as a single rollup line; this drill adds sub-program granularity and identifies the lab-level concentration of cuts.

**Confidence:** Medium-high on direction (the ASCR-grows-while-rest-shrinks pattern is well-established in administration messaging — but worth confirming, not assuming). Lower confidence on the Phase 2 extraction approach: the Science Volume CBJ PDF font behavior is unknown and may have the same custom-font issue that defeated `pdftotext` on the Summary By Org.

**Architecture:** Three phases.
- **Phase 1 (T5a):** Build `fy27_science_by_lab_subprogram.csv` from the existing Lab Tables source — Science sub-program × lab. No new paper required. Covers the lab portion of the picture but not extramural (university/grants).
- **Phase 2 (T5b):** Ingest FY27 Science Volume CBJ as new paper; build `fy27_science_subprograms.csv` — full Science org tree including intramural/extramural split where the source provides it.
- **Phase 3:** Analysis + viz on the joined data.

**Branch / line:** This work warrants its own line. Proposal: open `2026MMDD_science-cut-drill` at start of Phase 1 implementation session. Until then, plan lives in current line's `plans/` directory.

**Tech Stack:** Python (consistent with existing `scripts/`), `pdftotext -layout` then tesseract OCR fallback (same pattern as Summary By Org), CSV outputs in `data/`, Visualize tool for Phase 3 in-chat artifacts.

---

## Phase 1: T5a — Science sub-program × lab, from existing Lab Tables

The Lab Tables source PDF already contains Science sub-program rows under each Science-funded lab. T3 captures Science only at the office aggregate ($693M FY26 at Argonne); T5a expands this to ASCR / BES / BER / FES / HEP / NP / SLI / Safeguards & Security per lab. ~17 Science-funded labs × ~8 sub-programs ≈ 80-120 rows.

**Steps:**

1. Inventory: list every lab with Science rows in T3 (~17 labs).
2. For each, parse the Science section of its per-lab table from `papers/text/doe_fy27LaboratoryTables_2026.txt` (lines between `Subtotal, Science` and the next office).
3. Emit one row per `(lab, science_subprogram, FY25, FY26, FY27)`.
4. Reconcile: `sum(T5a per lab) == T3 Science total per lab`, all three years.
5. Reconcile: `sum(T5a globally) == T3 Science global total per year` (~$8.4B FY26).
6. Write `data/fy27_science_by_lab_subprogram.csv` only if reconciliations pass.
7. Update `data/README.md` with T5a section.

**Schema:**

| Column | Type | Description |
|---|---|---|
| `lab_name` | str | Matches T2's `lpi_name` and T3's `lab_name` |
| `science_subprogram` | str | ASCR / BES / BER / FES / HEP / NP / SLI / Safeguards & Security |
| `fy25_enacted_k`, `fy26_enacted_k`, `fy27_request_k` | int | $K |

**Testing Plan**

I will add reconciliation functions to the build script:
- For each lab in T5a, `sum(T5a sub-programs)` equals T3 Science total for that lab in all three years.
- Globally, `sum(T5a)` equals T3 Science office grand total in all three years.

Build script writes the CSV only if both reconciliations pass, fail loudly otherwise. Same pattern as `build_fy27_lab_by_office.py`. No parser regex unit tests — the reconciliation against T3 is the test that actually matters for behavior.

NOTE: I will write *all* tests before I add any implementation behavior.

**Cost estimate:** 1 session, no new paper-add needed.

---

## Phase 2: T5b — Sub-program tree from FY27 Science Volume CBJ

The Science Volume CBJ contains the canonical Science org tree including sub-program detail beyond what Lab Tables show (e.g., BES → Materials Sciences and Engineering → individual user facilities) and the intramural/extramural split. Source URL: locate from `https://www.energy.gov/cfo/articles/fy-2027-budget-justification` (Volume 4, Science).

**Paper-add session pre-flight:**

1. Download the Science Volume CBJ PDF.
2. Try `pdftotext -layout` first; if output is garbled or empty (custom font), fall back to tesseract OCR @ 300 DPI on rasterized pages.
3. Report which extraction method worked.
4. Save to `papers/text/doe_fy27ScienceVolume_2026.txt`.

**Steps (after ingestion):**

1. Walk the text extract; identify Science org tree (6 program offices × sub-programs × activities).
2. For each leaf, capture FY25/26/27 dollars and intramural/extramural split where present.
3. Capture narrative excerpts about funding rationale changes in a `notes` field — useful for Phase 3.
4. Emit T5b CSV.
5. Reconcile: `sum(T5b) per year == T1 Science leaf per year` ($8.247B FY25 / $8.250B FY26 / $7.100B FY27, ±$10M for OCR/rounding tolerance).
6. Cross-check vs T5a: `sum(T5b intramural per sub-program) ≈ sum(T5a per sub-program across labs)` modulo IIJA supplementals (Lab Tables include supplementals, Science request doesn't). Document any deltas.
7. Write build script `scripts/build_fy27_science_subprograms.py`.
8. Update README.

**Schema:**

| Column | Type | Description |
|---|---|---|
| `program_office` | str | ASCR / BES / BER / FES / HEP / NP / SLI / S&S |
| `subprogram` | str | E.g., "Materials Sciences and Engineering" |
| `activity` | str \| null | E.g., "Scientific User Facilities Operations". NULL where not detailed. |
| `fy25_enacted_k`, `fy26_enacted_k`, `fy27_request_k` | int | $K |
| `intramural_k` | int \| null | Lab portion in FY27 request, if separated in source |
| `extramural_k` | int \| null | University/grants portion in FY27 request, if separated |
| `notes` | str \| null | Narrative excerpts about funding rationale changes |

**Testing Plan**

Same reconciliation pattern:
- Global sum per year equals T1 Science leaf per year, within $10M tolerance.
- For each program office (ASCR/BES/etc.), sum of sub-programs equals the program-office subtotal printed in the source PDF.

Build script writes CSV only if reconciliations pass.

NOTE: I will write *all* tests before I add any implementation behavior.

**Cost estimate:** 1 paper-add session for ingestion + 2 sessions for the parser. If custom-font issue forces manual transcription, +1-2 sessions.

---

## Phase 3: Cut analysis and viz

With T5a and T5b stable, produce the deliverable.

**Steps:**

1. Compute FY26→FY27 deltas at three levels: program office, sub-program, activity. Identify top 3 growths and top 5 cuts.
2. Quantify ASCR-vs-rest: ASCR FY26→FY27 delta vs aggregate delta for (BES + BER + FES + HEP + NP).
3. Intramural/extramural split of the cut: how much of the −$1.15B falls on labs vs. universities (Phase 2 dependency).
4. Lab-level concentration: from T5a, top 5 labs by absolute and percentage Science FY26→FY27 decline.
5. Viz artifacts in chat via `visualize:show_widget`:
   - Diverging bar chart of FY26→FY27 deltas by sub-program (the key chart)
   - Treemap of Science FY27 request showing relative sub-program sizes with growth/cut color coding
   - Lab × sub-program heatmap of FY27 dollars
6. Brief narrative summary (~500 words) saved as `docs/active/<line>/results/science-cut-analysis.md`.

No code tests for Phase 3 — analysis/visualization, not parser. Spot-check: pick 2 sub-programs and verify viz numbers match the CSVs.

**Cost estimate:** 1-2 chat sessions.

---

**Testing Details**

Both Phase 1 and Phase 2 use reconciliation tests comparing extracted totals against authoritative totals already in the corpus (T1, T3, printed source totals). This tests *behavior* (does extracted data faithfully represent the source) rather than parser internals. Build scripts write CSV only if reconciliations pass — preventing partially-broken data from landing in `data/`. Phase 3 has no code tests; visual spot-check against CSVs.

**Implementation Details**

- Build on the pattern in `scripts/build_fy27_lab_by_office.py` — walk text, match patterns, reconcile, write.
- Phase 1 has no paper-add dependency; Phase 2 does.
- For Phase 2 OCR fallback: same approach as Summary By Org (tesseract @ 300 DPI on rasterized pages).
- Phase 3 viz lives in chat artifacts; narrative as markdown file in `results/`.
- T5a takes precedence for lab-level analysis (more accurate at lab axis). T5b takes precedence for extramural and activity-level detail.
- If Phase 2's intramural/extramural breakdown isn't in the source (sometimes Science only breaks this out at program-office level), estimate extramural ≈ T5b sub-program total − T5a sub-program total summed across labs.
- Phases are loosely coupled: Phase 1 ships alone if Phase 2 hits extraction trouble.

**What could change**

- Custom-font issue on Science Volume CBJ → Phase 2 becomes multi-week manual work. Phase 1 alone ships, extramural treated as known gap in the README.
- If the per-sub-program intramural/extramural breakdown isn't in the source at sub-program level, lose granularity but headline story stays intact.
- The data quality fixes (SWPA dup, CMEI $1.15B delta investigation, NREL rename) running in parallel via paper-add session could change T3 numbers by ~$200M — small relative to Science's $8B but worth re-running Phase 1 reconciliation if T3 is rebuilt.
- If FY27 request gets amended via OMB update mid-cycle (rare but possible), T5b needs re-extraction.

**Questions**

1. **Audience confirmation.** Plan assumes this drill is for general policy literacy + a focused analytical artifact. Not testimony prep, not coalition deliverable. Confirm.
2. **New line vs. extend current?** Proposal: open `2026MMDD_science-cut-drill` for implementation. Alternative: extend `20260521_fy26-mapping-scope` since it's thematically adjacent. I'd vote new line — the deliverables are distinct from "the budget map."
3. **Extramural depth.** Must-have (drives whether Phase 2 is required) or nice-to-have (Phase 1 alone covers the lab story)? Recommend must-have because the cut's political salience is partly about university research, but you might already know whether your audience cares.
4. **Framing.** Lead with "−13.9% cut" (cut-centric framing) or with "ASCR grows while basic research shrinks" (composition-centric framing)? Different framings will read differently to different audiences.
