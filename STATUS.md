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
  - `20260521_fy27-bib-papers` — paper-ingestion line for the FY27 BiB corpus. Three docs ingested + T1/T2/T3 + README built; pending: SWPA dup fix, CMEI delta investigation, NREL→NLR README callout, facility_type column.
  - `20260521_fy26-mapping-scope` — scope and schema for the FY26 DOE budget map. v1 deliverable = T1+T2+T3+classification. Science Volume Drill plan drafted at `plans/science-volume-drill.md` for follow-on line.
  - `20260521_science-cut-drill` — drill into where the FY27 −13.9% Office of Science cut lands at sub-program × lab level. Phase 1 (T5a from existing Lab Tables) in progress. Phase 2 (Science Volume CBJ ingestion for intramural/extramural split) committed as part of deliverable. Originating plan: `docs/active/20260521_fy26-mapping-scope/plans/science-volume-drill.md`.

## Recent sessions

- **2026-05-21** — `20260521_fy27-bib-papers`: setup + naming agreement + Lab Tables URL discovery (plural form). Blocked on energy.gov sandbox allow-list propagation. Fresh chat required to ingest the three FY27 BiB starter docs. See `docs/active/20260521_fy27-bib-papers/RESEARCH_LOG.md`.
- **2026-05-21** — `20260521_fy26-mapping-scope`: scoped FY26 budget map (post-reorg, DOE-only, office→program→lab, $49.1B net / $53.8B gross); reviewed landed T1/T2/T3 from parallel paper-add session; surfaced three data quality issues (SWPA source-duplication +$200M/yr at Undesignated LPI; CMEI $1.15B FY26 unreconciled delta — likely IIJA supplementals; NREL→NLR rename not yet in README); confirmed `facility_type` (8-9 categories); drafted Science Volume Drill plan (3 phases) at `docs/active/20260521_fy26-mapping-scope/plans/science-volume-drill.md` for follow-on line `2026MMDD_science-cut-drill`. Initial workflow error: opened a branch before noticing `main_only` mode — deleted and moved to main.

## Archived research lines

(Research lines that have been completed and merged to main. Empty for now.)
