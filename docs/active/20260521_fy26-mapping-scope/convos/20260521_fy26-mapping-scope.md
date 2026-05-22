# 20260521_fy26-mapping-scope

**Date:** 2026-05-21
**Branch:** main (line: 20260521_fy26-mapping-scope)
**Surface:** claude.ai

## Summary

Initial scoping session for the FY26 DOE budget mapping project. Worked through scope decisions (FY26 enacted, DOE-only, office→program→lab, post-reorg structure, general policy literacy not AI-tilted), corrected a source-document plan (FY27 BiB rather than FY26 BiB, since FY26 enacted figures live in the FY27 release), and settled on a v1 schema with a `facility_type` classification column. Hit a workflow error early — opened a branch before noticing `workflow_mode: main_only` in STATUS — caught and cleaned up before any other work landed.

Mid-session, three structured tables landed from the parallel paper-add session: T1 (`fy27_summary_by_org.csv`, 76 rows, office-axis), T2 (`fy27_lab_summary.csv`, 94 rows, lab-axis rollups), and T3 (`fy27_lab_by_office.csv`, 347 rows, lab × office join). Reviewed all three: T3 is structurally clean with per-lab reconciliation passing, but the review surfaced three data quality issues — a duplicate `Subtotal, SWPA` / `Subtotal, Southwestern Power Administration` pair in the DOE source PDF (lines 4590-4591) inflating Undesignated LPI by ~$200M/yr (a source-document bug, not a parser bug); a $1.15B unreconciled CMEI delta between T1 and T3 in FY26 that the README's gross-vs-net framing doesn't cover (likely IIJA supplementals); and the NREL → National Laboratory of the Rockies rename (Dec 1, 2025) not yet documented.

Session ended with a drafted Science Volume Drill plan (three phases: T5a from existing Lab Tables, T5b from new Science Volume CBJ ingestion, Phase 3 cut analysis + viz). Plan saved to `plans/science-volume-drill.md`. Implementation proposed to live in a new research line `2026MMDD_science-cut-drill` opened at start of Phase 1.

## Topics Explored

- Scope of FY26 DOE budget map — granularity, year, direction, use case
- DOE Nov-2025 reorganization impact on office axis (CMEI absorbs EERE, HGEO absorbs FE, new AIQ/Fusion/Strategy/TechCom/EDF/Baseload offices)
- Source document strategy (FY27 BiB vs FY26 BiB for FY26-enacted figures)
- v1 schema for office × program × lab with legacy_label crosswalks embedded per-line
- Facility scope decision (keep all 94 LPIs with `facility_type` column, not just true national labs)
- Review of landed T1/T2/T3 tables — structure, reconciliation, schema
- Gross-vs-net reconciliation (PMA offsetting collections, IIJA supplementals at CMEI/Science/NE/HGEO)
- NREL → NLR rename and its policy subtext
- Three forward directions from extraction-agent's note: v1 viz, Science cut drill, State Tables
- Science Volume Drill plan scope, phasing, and dependencies

## Provisional Findings

- Post-reorg crosswalk is embedded per-line in the FY27 BiB source as parenthetical "(formerly X - <old office>)" annotations — no separate crosswalk table needed.
- NNSA dominates lab dollar flows: 6 of top 10 labs by FY26 enacted are NNSA-driven; Office of Science labs only enter at rank 5+. A single "DOE budget map" structurally compresses two pretty different lab ecosystems (NNSA weapons/security vs. open science) into the same axis.
- T3's office axis is the appropriation-account axis (Weapons Activities, Other Defense Activities, etc.) — distinct from T1's office-chart axis (Undersecretary for Science, Direct Reports). A join between T1 and T3 requires a crosswalk lookup.
- $200M FY26 SWPA double-counting bug originates in the DOE source PDF and propagated through T2 and T3. Small relative to $54B but should be fixed in the parsers' skip lists.
- The unreconciled $1.15B FY26 CMEI delta is plausibly IIJA supplemental funding at the labs (CMEI absorbed EERE, which had significant IIJA money). Similar patterns at Science (+$150M), Nuclear Energy (+$100M), HGEO (+$140M) — total FY26 ex-PMA unexplained delta ~$1.5B. The README's gross-vs-net framing focuses on FY27 and undersells the FY26 picture.
- The brand-new FY27 offices (AIQ $1.2B, Baseload Power $3.5B) repurpose prior-year unobligated IIJA money rather than new appropriations — politically loaded but out of scope for FY26 mapping.

## Decisions Made

- v1 schema includes a `facility_type` column with 8-9 categories (national_lab, nnsa_production_facility, naval_reactors_facility, em_cleanup_site, spr_facility, doe_admin_office, pma_office, university, catchall).
- Post-reorg as primary org chart, with legacy office/program labels preserved per-line where the FY27 BiB provides them.
- Data quality fixes (SWPA dup, CMEI delta investigation, NREL rename in README, facility_type addition) will be handled via parallel paper-add session before any viz work.
- Next direction: Science Volume Drill (option B of three; chosen for substantive policy insight per session).
- Science Volume Drill gets its own research line at implementation time rather than extending this one.
- Plan saved to `docs/active/20260521_fy26-mapping-scope/plans/science-volume-drill.md`.

## Results

Files that landed mid-session from the parallel paper-add work:
- `papers/text/doe_fy27SummaryByOrg_2026.txt`, `papers/text/doe_fy27BudgetInBrief_2026.txt`, `papers/text/doe_fy27LaboratoryTables_2026.txt` (extracted text from FY27 BiB volumes)
- `data/fy27_summary_by_org.csv` (T1, 76 rows, office axis)
- `data/fy27_lab_summary.csv` (T2, 94 rows, lab rollups)
- `data/fy27_lab_by_office.csv` (T3, 347 rows, lab × office join)
- `data/README.md` (provenance + gross-vs-net caveat)
- `scripts/build_fy27_*.py` (build scripts with reconciliation)

Drafted this session:
- `docs/active/20260521_fy26-mapping-scope/plans/science-volume-drill.md` (this session's plan output)

## Open Questions

- Audience for the Science cut drill — general policy literacy vs. specific testimony/coalition deliverable. Affects framing and depth.
- Whether to include intramural/extramural split in the science drill (drives whether Phase 2 of the plan is required).
- Framing of the science cut artifact — cut-centric ("-13.9%") vs composition-centric ("ASCR grows while rest shrinks"). Different audiences want different framings.
- What's in T3's "Other (not under office subtotal)" rows ($550M FY26) — synthetic residuals per README, but the underlying line items in pp. 124-125 of source haven't been inspected.
- What's actually in T2/T3's "Other" ($2.26B FY26) and "Undesignated LPI" ($2.68B FY26) catch-all rows — nearly 10% of T2 sits unclassified.
- T4 (per-program offsetting-collections lookup) — would let analysts compute gross OR net at any granularity. Open whether to build this before or after Phase 3 viz.
