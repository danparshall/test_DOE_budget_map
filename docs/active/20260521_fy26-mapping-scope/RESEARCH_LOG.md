# Research Log — FY26 budget mapping scope

This line covers initial scoping and schema design for the FY26 DOE budget map (by office, program, and lab). Output is a structured table joining DOE offices → programs → labs with FY26 enacted dollars; this line tracks the sessions setting up that work. Once the schema is locked and validated against sample labs, follow-on extraction/visualization work may live in separate research lines.

---

## Line-level: scope, sources, schema

### Scope

- **Budget year:** FY2026 enacted (current FY)
- **Budget concept:** budget authority (gross at lab axis, net at org axis — see gross-vs-net section).
- **Scope of "DOE":** DOE-only. Non-DOE flows (DOD/NIH Work for Others, SPPs) are out of scope.
- **Org chart:** post-Nov-2025 reorganization. New offices: CMEI (absorbing EERE), HGEO (absorbing Fossil Energy), Office of Artificial Intelligence and Quantum (AIQ), Office of Fusion, Office of Strategy and Technology Roadmaps, Office of Technology Commercialization, Office of Energy Dominance Financing, Baseload Power. Stable: Science, NNSA (Weapons Activities, DNN, Naval Reactors), Nuclear Energy, Environmental Management, ARPA-E, CESER, Electricity (OE), Indian Energy, EIA, departmental admin. Legacy office/program labels preserved per-line where the FY27 BiB provides the crosswalk (typically parenthetical `(formerly X - <old office>)` annotations).
- **Use case:** general DOE budget literacy / reference. Not tilted toward AI policy.

### Total to map

DOE FY2026 enacted = **$49,104,527K (~$49.1B)** per FY27 Summary Table by Organization (net discretionary). At the lab axis (gross BA), the same year sums to $53.82B in the Lab Tables — a ~$4.7B gap that's partly gross-vs-net (PMA offsetting collections, ~$1.9B) and partly IIJA supplemental funding visible in Lab Tables but not in the discretionary org-axis ($1.15B at CMEI, plus smaller amounts at Science / NE / HGEO).

### Sources (in repo)

| File | Format | Size | Role |
|---|---|---|---|
| `papers/text/doe_fy27SummaryByOrg_2026.txt` | tesseract OCR | 6.5 KB | Org-axis spine. Reconciliation target. |
| `papers/text/doe_fy27LaboratoryTables_2026.txt` | pdftotext | 553 KB | Per-lab detailed tables: office → program → activity → $. Primary extraction source. |
| `papers/text/doe_fy27BudgetInBrief_2026.txt` | pdftotext | 272 KB | Narrative context + summary tables. Cross-check / context. |

Structured tables produced from these:

| CSV | Source pages | Rows | Description |
|---|---|---|---|
| `data/fy27_summary_by_org.csv` | SummaryByOrg pp 1-3 | 76 | T1 — every program from the org table with hierarchy (leaf/subtotal/section_total/grand_total). Net discretionary. |
| `data/fy27_lab_summary.csv` | LabTables pp 1-3 | 94 | T2 — one row per LPI rollup. Gross BA. |
| `data/fy27_lab_by_office.csv` | LabTables pp 4-124 | 347 | T3 — (lab, office) join via `Subtotal,` lines. Includes synthetic residual rows for orphan leaves. |

Authoritative landing page: <https://www.energy.gov/cfo/articles/fy-2027-budget-justification>

### Schema (v1, conceptual)

The (office, program, lab) tidy table that motivated this line maps to two complementary tables in practice:
- **T1** holds the office × program structure at the org-axis (net discretionary).
- **T3** holds the (office, lab) join at the lab-axis (gross BA).

A full join — (office, program, lab) at the line-item level — was originally planned as T3 but the implementation chose to keep T1 and T3 as separate-axis tables, with the cross-product join deferred. v1 of the budget map = T1 + T2 + T3 + facility classification.

**`facility_type` column for T2/T3** (decided this session, pending implementation): 8-9 categories — `national_lab`, `nnsa_production_facility`, `naval_reactors_facility`, `em_cleanup_site`, `spr_facility`, `doe_admin_office`, `pma_office`, `university`, `catchall`. Will be added to T2 (and T3 via join) in next paper-add session.

### Known data quality issues (pending fix)

1. **SWPA source-duplication.** The DOE source PDF prints `Subtotal, SWPA` and `Subtotal, Southwestern Power Administration` as two consecutive identical lines (lines 4590-4591 of the extract). Both got carried into T3 → Undesignated LPI is inflated by ~$200M/yr (FY25 $182,891K, FY26 $201,887K, FY27 $196,158K). T2 inherits the same source bug, so the T2↔T3 reconciliation "passes" while both are off by the same amount vs. the DOE document's underlying truth. Fix: add SWPA to the skip list in `build_fy27_lab_by_office.py` and corresponding fix in T2's build.
2. **CMEI $1.15B unreconciled delta (FY26).** T3 CMEI sum = $3,033,250K; T1 CMEI leaf = $1,883,250K. Likely IIJA supplemental funding included in Lab Tables but not in the discretionary org-axis. Similar (smaller) patterns at Science (+$150M), Nuclear Energy (+$100M), HGEO (+$140M). README's gross-vs-net framing focuses on FY27 and doesn't currently document the FY26 picture. Fix: investigate and document explicitly.
3. **NREL → NLR rename.** NREL was renamed to National Laboratory of the Rockies (NLR) effective Dec 1, 2025 under the new CMEI umbrella. Lab Tables already use the new name. README needs a 2-line callout so analysts encountering the new name can map back. Fix: README addition.

### Open items

- **T4 (per-program offsetting-collections lookup)** — would let analysts compute gross OR net at any granularity. Open whether to build before Phase 3 viz of the science drill.
- **"Other" / "Undesignated LPI" catch-alls** — together $4.94B FY26 (≈9% of T2), unclassified. Worth a pp. 124-125 spot-check to either re-attribute or document what's in them.
- **Office-axis crosswalk T3↔T1.** T3 uses appropriation-account axis (Weapons Activities, Other Defense Activities); T1 uses office-chart axis (Undersecretary for Science, Direct Reports). A small lookup table would let either be pivoted to the other.
- **Office-specific volumes:** for higher-granularity drill-downs, the FY27 office-specific volumes (Science vol 4, CMEI vol 2, HGEO vol 3, etc.) are the next layer. First use case: Science Volume Drill (plan in `plans/science-volume-drill.md`).

### Next direction

**Science Volume Drill** — plan saved at `plans/science-volume-drill.md`. Three phases:
- Phase 1 (T5a): Science sub-program × lab from existing Lab Tables — no new paper.
- Phase 2 (T5b): Science Volume CBJ ingestion → sub-program tree with intramural/extramural split.
- Phase 3: Cut analysis + viz on where the FY27 −13.9% Science cut lands.

Implementation proposed to open a new line `2026MMDD_science-cut-drill` at start of Phase 1, with the data quality fixes above running in parallel via paper-add session beforehand.

---

## Session history

### Session: 2026-05-21 — `20260521_fy26-mapping-scope`

#### Topics explored

- Project scoping: FY26 enacted, DOE-only, office→program→lab axis, post-reorg structure, general literacy use case
- DOE Nov-2025 reorganization and its impact on the office axis
- Source document strategy correction (FY27 BiB rather than FY26 BiB for FY26 enacted figures)
- Schema v1 design, including the legacy_label crosswalk approach
- Review of landed T1/T2/T3 tables (reconciliation, schema, gross-vs-net surface)
- Facility scope decision (keep all 94 LPIs with classification)
- Gross-vs-net reconciliation deeper than the README's initial framing
- NREL → NLR rename and verification via web search
- Three forward directions: viz, Science cut drill, State Tables
- Science Volume Drill plan drafted

#### Findings

1. Per-line legacy crosswalk is embedded in the FY27 BiB Lab Tables as `(formerly X - <old office>)` annotations. No separate crosswalk table needed.
2. NNSA dominates lab dollar flows — 6 of top 10 labs by FY26 enacted are NNSA-driven; Office of Science labs enter at rank 5+. A single budget map structurally compresses two distinct lab ecosystems.
3. T3's office axis is the appropriation-account axis (Weapons Activities, etc.); T1's is the office-chart axis (Undersecretary for Science, etc.). A T3↔T1 join requires a small crosswalk.
4. SWPA source-duplication bug: the DOE source PDF itself prints the SWPA subtotal twice (lines 4590-4591). Carried through T2 and T3, inflating Undesignated LPI ~$200M/yr. Per-lab reconciliation "passes" because T2 inherits the same bug.
5. The $1.15B FY26 CMEI delta between T1 and T3 is most likely IIJA supplemental funding at the labs. Plus similar smaller deltas at Science, NE, HGEO. Total FY26 ex-PMA unexplained delta ~$1.5B, not currently documented.
6. NREL → NLR rename effective Dec 1, 2025 — DOE Lab Tables already use the new name.

#### Results

- T1/T2/T3 + `data/README.md` landed mid-session from the parallel paper-add work.
- Three raw text extracts landed in `papers/text/`.
- This RESEARCH_LOG.md established and updated.
- STATUS.md updated with new active line and project framing for post-reorg org chart.
- `plans/science-volume-drill.md` drafted for follow-on implementation.
- Initial workflow error: opened a branch `fy26-office-program-lab` before noticing `workflow_mode: main_only` in STATUS — deleted; work moved to main directory.

#### Next steps

- **Parallel paper-add session work:** fix SWPA dup in T2/T3 build scripts; investigate and document the FY26 CMEI/Science/NE/HGEO unreconciled deltas; add NREL→NLR README callout; add `facility_type` column to T2/T3.
- **Next chat session:** open new line `2026MMDD_science-cut-drill`; implement Phase 1 (T5a) per `plans/science-volume-drill.md`. Audience/framing questions in the plan to be answered at start of that session.
- **Possible side quest:** T4 (offsetting-collections lookup) — small but high-utility for gross/net normalization. Could go in this line or its own.
