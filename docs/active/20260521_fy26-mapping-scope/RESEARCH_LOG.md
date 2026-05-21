# Research Log — FY26 budget mapping scope

This line covers initial scoping and schema design for the FY26 DOE budget map (by office, program, and lab). Output is a structured table joining DOE offices → programs → labs with FY26 enacted dollars; this line tracks the sessions setting up that work. Once the schema is locked and validated against sample labs, follow-on extraction/validation work may live in separate research lines.

---

## Line-level: scope, sources, schema

### Scope

- **Budget year:** FY2026 enacted (current FY)
- **Budget concept:** budget authority (gross). Per FY27 Lab Tables prefatory note: includes discretionary and supplemental funding; does NOT consider revenues/receipts, use of prior year balances, deferrals, rescissions, or other adjustments appropriated as offsets.
- **Scope of "DOE":** DOE-only. Non-DOE flows (DOD/NIH Work for Others, SPPs) are out of scope.
- **Org chart:** post-Nov-2025 reorganization. New offices: Critical Minerals and Energy Innovation (CMEI, absorbing EERE), Hydrocarbons and Geothermal Energy Office (HGEO, absorbing Fossil Energy), Office of Artificial Intelligence and Quantum (AIQ), Office of Fusion, Office of Strategy and Technology Roadmaps, Office of Technology Commercialization, Office of Energy Dominance Financing, Baseload Power. Stable offices: Science, NNSA (Weapons Activities, DNN, Naval Reactors), Nuclear Energy, Environmental Management, ARPA-E, CESER, Electricity (OE), Indian Energy, EIA, departmental admin. Legacy office/program labels preserved per-line where the FY27 BiB provides the crosswalk (typically as parenthetical `(formerly X - <old office>)` annotations).
- **Use case:** general DOE budget literacy / reference. Not tilted toward AI policy.

### Total to map

DOE FY2026 enacted = **$49,104,527K (~$49.1B)** per FY27 Summary Table by Organization. Reconcilable against per-lab rollup totals in the Lab Table Summary Report.

### Sources (in repo)

| File | Format | Size | Role |
|---|---|---|---|
| `papers/text/doe_fy27SummaryByOrg_2026.txt` | tesseract OCR | 6.5 KB | Org-axis spine: $K by office for FY25/26 enacted + FY27 request. The reconciliation target. |
| `papers/text/doe_fy27LaboratoryTables_2026.txt` | pdftotext | 553 KB | Per-lab detailed tables: office → program → activity → $. Primary extraction source. |
| `papers/text/doe_fy27BudgetInBrief_2026.txt` | pdftotext | 272 KB | Narrative context + summary tables. Cross-check / context. |

Structured CSV extracts pending (Dan running separate session for paper-add work).

Authoritative landing page: <https://www.energy.gov/cfo/articles/fy-2027-budget-justification>

### Schema (v1)

Flat tidy-format, one row per (office, program_path, lab) leaf:

| Field | Description |
|---|---|
| `office` | Top-level DOE office, post-reorg. E.g., `Science`, `Critical Minerals and Energy Innovation`, `NNSA - Weapons Activities`. |
| `program_path` | Hierarchical program location within the office, ` > `-separated. E.g., `Basic Energy Sciences > Research`. |
| `legacy_label` | Parenthetical legacy office/program name where the FY27 BiB provides one. E.g., `Bioenergy Technologies - EERE`. NULL where no crosswalk. |
| `lab` | Lab/site/facility name as in the Lab Table (e.g., `Argonne National Laboratory`, `NNSA Albuquerque Complex`). |
| `facility_type` | Classification (`national_lab`, `site_office`, `field_office`, `production_facility`, `cleanup_site`, `petroleum_reserve`, `university`, `other`). Open — see Open items. |
| `fy25_enacted_kusd` | FY2025 enacted, $ thousands |
| `fy26_enacted_kusd` | FY2026 enacted, $ thousands |
| `fy27_request_kusd` | FY2027 request, $ thousands |
| `source_section` | E.g., `FY27 Lab Tables > Argonne National Laboratory`. |

**Extraction rules:**
- Emit only leaf rows. Subtotal lines (e.g., `Subtotal, Science`) are useful for in-extract validation but not stored as rows — they'd double-count.
- A program funding extramural work that's bundled at office level but doesn't appear at any lab → synthetic `lab = "(extramural / not lab-distributed)"` row so office totals reconcile.

### Open items

- **Facility scope:** the Lab Tables source includes ~90 facilities — true national labs, but also site offices, field offices, SPR caverns, cleanup sites, contractor production facilities (KCNSC, Y-12, Pantex, NNSS), and universities. Keep all with a `facility_type` column, or filter to national labs only? Dan to decide. Default proposal: keep all + classify; filtering is cheaper than reconstructing.
- **Extraction approach:** the Lab Tables pdftotext output uses indent depth to encode program hierarchy, but not perfectly consistently. Needs a parser pass with light heuristics on indent + subtotal-line detection. Next session work.
- **Cross-validation:** sum(extracted leaf rows, by office) and sum(by lab) should equal (a) Lab Table Summary Report per-lab rollups, and (b) FY27 Summary By Org office totals — modulo the mandated-transfer footnotes ($96.7M FY26 transfer to NE for Advanced Test Reactor; $20M FY26 collection to American Energy Independence Fund).
- **Office-specific volumes:** for higher-granularity drill-downs on specific programs, the FY27 office-specific volumes (Science vol 4, CMEI vol 2, HGEO vol 3, etc.) are the next layer. Out of scope unless we hit ambiguity in the Lab Tables.

---

## Session history

### Session: 2026-05-21 — `20260521_fy26-mapping-scope`

#### Topics explored

- Scoped FY26 enacted DOE budget map: granularity, budget year, direction (office→lab), use case (general literacy, not AI-tilted)
- Discovered the DOE Nov-2025 reorganization affects the office axis — settled on post-reorg structure with per-line legacy_label crosswalks
- Corrected source plan: FY26 BiB only contains the FY26 *request*, not enacted; FY26 enacted lives in FY27 BiB (released April 3, 2026)
- Verified schema works against sample lab (Argonne)

#### Findings

1. **Per-line legacy crosswalk is embedded in the source.** FY27 BiB Lab Tables annotate moved activities with `(formerly X - <old office>)` directly in line item names. No separate crosswalk table needed.
2. **Reorg is deeper than office renames.** Activities re-bundled within new offices: former Vehicle Technologies → Transportation Technologies; Bioenergy → Alternative Fuels & Feedstocks; Solar/Wind/Grid Integration → Integrated Energy Systems (all under CMEI). Multiple former-EERE programs collapse into single CMEI line items.
3. **Brand-new FY27 offices have no FY26 enacted activity.** AIQ ($1.2B FY27 request), Office of Fusion ($10M), Strategy & Tech Roadmaps ($3M), Baseload Power ($3.5B) all show $0 for FY25 and FY26. Their FY27 funding repurposes prior-year unobligated IIJA money rather than new appropriations.
4. **Lab Tables cover more than national labs.** ~90 facilities total: national labs + site offices + field offices + SPR caverns + cleanup sites + contractor production facilities + universities. Schema's `lab` field needs `facility_type` classification.
5. **NNSA dominates lab dollar flows.** Top labs by FY26 enacted: Los Alamos $5.13B; Savannah River Site $3.43B; Sandia $3.21B; LLNL $2.65B; ORNL $2.21B; Office of River Protection $2.20B; Idaho National Laboratory $1.69B; NNSA Albuquerque Complex $1.29B; Pantex $1.18B; Hanford Site $1.16B. Of top 10, 6 are NNSA-driven.

#### Results

- Active line established with scope, schema v1, and source manifest (this file).
- STATUS.md project framing updated to reflect post-reorg org chart.
- Initial workflow error: opened a branch `fy26-office-program-lab` before noticing `workflow_mode: main_only` — deleted; work moved to this main-line directory.

#### Next steps

- **Decide:** facility scope (national labs only vs. all-facilities-with-classification).
- **Plan:** write extraction plan via `write-a-plan` skill — covers Lab Tables parser, leaf-row emission rules, validation checks against rollups + org totals. Likely next session.
- **Maybe:** classification list for `facility_type` (~90 facilities). Either ad-hoc during extraction or pre-classified from the Lab Table TOC.
