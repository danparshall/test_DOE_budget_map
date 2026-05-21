# Status — test_DOE_budget_map

workflow_mode: main_only

## What this repo is

Mapping the U.S. Department of Energy budget by office, program, and national lab — tracing how appropriations flow across DOE offices and what work each line item funds at the labs. Uses the post-Nov-2025 DOE reorganization structure as the primary org axis (Science, NNSA, CMEI [absorbing EERE], HGEO [absorbing Fossil Energy], Nuclear Energy, Environmental Management, ARPA-E, and others), with legacy office/program labels preserved per-line where the source documents provide a crosswalk.

## Project parameters

Per-project configuration the skills read at runtime. Update only when the project's scope or conventions change.

- `PROJECT_QUESTION`: Mapping the U.S. Department of Energy budget by office, program, and national lab — tracing how appropriations flow across DOE offices and what work each line item funds at the labs. Uses the post-Nov-2025 DOE reorganization structure as the primary org axis, with legacy office/program labels preserved per-line where the source documents provide a crosswalk.
- `CONDITIONAL_SECTION`: unset
- `BIB_FILE`: unset
- `PAPERS_INDEX`: PAPER_INDEX.md
- `paper_summaries.structure`: single-file

## Current state

- **Workflow:** main_only.
- **Active research lines:**
  - `20260521_fy27-bib-papers` — FY27 BiB corpus line. Three docs ingested + 3 reconciled structured tables (T1 `data/fy27_summary_by_org.csv`, T2 `data/fy27_lab_summary.csv`, T3 `data/fy27_lab_by_office.csv`) + first-cut `budget_map_v0.md`. **Default pickup:** file composed §7 issue (URL in `docs/active/20260521_fy27-bib-papers/convos/20260521_fy27-bib-ingest.md`) → start v1 budget-map visualizations. Alternatives if question requires: Science JEDI (sub-program detail) or State Tables (geographic cut). See research-line RESEARCH_LOG for full options.
  - `20260521_fy26-mapping-scope` — scope and schema for the FY26 DOE budget map. v1 schema drafted; awaiting facility-scope decision before extraction.

## Recent sessions

- **2026-05-21** — `20260521_fy27-bib-ingest`: ingested 3 FY27 BiB docs (incl. OCR fallback for custom-font PDF), built T1 (`data/fy27_summary_by_org.csv`, 76 rows) + T2 (`data/fy27_lab_summary.csv`, 94 rows) + T3 (`data/fy27_lab_by_office.csv`, 347 rows) all reconciled to source totals, produced first-cut `budget_map_v0.md`. ~29 commits. §7 issue composed but not filed. See `docs/active/20260521_fy27-bib-papers/convos/20260521_fy27-bib-ingest.md`.
- **2026-05-21** — `20260521_fy27-bib-papers`: setup + naming agreement + Lab Tables URL discovery (plural form). Blocked on energy.gov sandbox allow-list propagation. Fresh chat required to ingest the three FY27 BiB starter docs. See `docs/active/20260521_fy27-bib-papers/RESEARCH_LOG.md`.
- **2026-05-21** — `20260521_fy26-mapping-scope`: scoped FY26 budget map (post-reorg, DOE-only, office→program→lab, $49.1B total); discovered DOE Nov-2025 reorganization affects office axis; corrected source plan (FY27 BiB, not FY26 BiB); verified v1 schema against Argonne sample. Initial workflow error: opened a branch before noticing `main_only` mode — deleted and moved to main. See `docs/active/20260521_fy26-mapping-scope/RESEARCH_LOG.md`.

## Archived research lines

(Research lines that have been completed and merged to main. Empty for now.)
