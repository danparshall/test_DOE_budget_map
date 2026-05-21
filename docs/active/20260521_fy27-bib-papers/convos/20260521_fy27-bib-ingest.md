# 20260521_fy27-bib-ingest

**Date:** 2026-05-21
**Branch:** main (workflow_mode `main_only`)
**Surface:** claude.ai
**Research line:** `20260521_fy27-bib-papers`

## Summary

Continued the work from the `20260521_fy27-bib-papers` setup session after the sandbox allow-list propagation cleared. The starter ingest of three FY27 BiB documents had already been completed in the prior chat and checkpointed mid-session; this chat then built three structured tables on top of that corpus, identified two skill gaps and one data-quality finding for an upstream issue, and produced a first-cut budget-map artifact synthesizing the line-item picture across all three tables.

Two scope choices made along the way are worth flagging. First, T1 (Summary by Organization) was extracted via OCR + manual transcription rather than automated parsing, because the source PDF uses a custom-encoded subset font with no `/ToUnicode` CMap and `pdftotext`/`pymupdf` both returned mojibake; OCR + a fully reconciled reconciliation tree (30 checks across nested subtotals, section totals, and grand total) gave a more defensible CSV. Second, T3 was scoped to the lab × *office* matrix (subtotal level) rather than the full lab × *sub-program* detail (~3-5k rows); the office-level rollup is sufficient for a first budget map, and the sub-program flat (T4) defers to a later session when a specific question demands the detail.

## Topics Explored

- BiB starter corpus ingestion via `paper-processing-institutional` (Protocol B): three PDFs, 12 commits
- OCR fallback for `doe_fy27SummaryByOrg_2026.pdf` (custom subset font defeated standard text extraction)
- T1 — `data/fy27_summary_by_org.csv`: 76 rows, hierarchy-tagged, 30 reconciliation checks
- T2 — `data/fy27_lab_summary.csv`: 94 LPI rows, regex-parsed from clean `pdftotext` output
- T3 — `data/fy27_lab_by_office.csv`: 347 lab × office cells, with skip rules for nested rollups and synthetic residual rows for orphan leaves
- `data/README.md` — schema, provenance, hierarchy, gross-vs-net caveat
- `budget_map_v0.md` — first-cut artifact synthesizing the corpus into a usable map
- §7 upstream issue composed (covers Step 1 sandbox precondition + Step 2 OCR fallback + bonus printed-percentage finding)

## Provisional Findings

- **The FY27 request rebalances Defense up (+21%) and Non-Defense down (−16%) for a net +10% topline.** The BiB narrative does not characterize the non-defense cuts.
- **Office of Science is cut −13%** ($8.25B → $7.14B). The BiB calls this "$7.14 billion to support cutting-edge basic research" without naming it as a cut.
- **CMEI (rebranded EERE) is cut −40% FY26→FY27 and −64% over two years** — the largest percentage cut among major offices, hidden behind a rename.
- **Other meaningful cuts:** ARPA-E −43%, OE −22%, CESER −16%, NE −9%, Indian Energy −33%, IG −14%, Tribal Energy Loan Guarantee −68%.
- **Weapons Activities is 50.9% of the FY27 topline** ($27.44B). With the rest of NNSA, the four programs are 60.8% of $53.91B.
- **At lab level, the Science-vs-NNSA story is the cleanest visualization.** Every Office-of-Science-anchored lab is cut 13-22% (ANL −17%, LBNL −20%, ORNL −16%, BNL −13%, PNNL −20%, SLAC −22%; Fermi +11% is the only exception). Every NNSA-anchored lab is up 5-63% (LANL +32%, Sandia +24%, LLNL +21%, KCNSC +37%, NNSS +63%).
- **The AIQ $1.2B and Baseload Power $3.5B currently live at central accounts** (Washington Headquarters and Undesignated LPI) not at the ANL/ORNL labs the BiB names. Both are funded by repurposing prior-year unobligated IIJA dollars.
- **The IIJA cancellation has two visible parts:** $4.7B reappears in FY27 Receipts and Offsets as "Repurposed IIJA Funding" and reallocates to Baseload + AIQ; remaining ~$10.5B is pure rescission not traced in this corpus.
- **Gross-vs-net reconciliation:** Lab Tables aggregate to $61.90B FY27 (gross BA); SummaryByOrg / BiB aggregate to $53.91B FY27 (net discretionary). ~$8B gap is supplements minus offsets. Documented in `data/README.md`.

## Decisions Made

- T3 scoped to lab × office (subtotal level) for v0; T4 (full lab × sub-program detail) deferred until a specific question motivates it.
- T1 extracted via OCR + manual transcription with full reconciliation tree, not regex parsing (custom font defeated `pdftotext`).
- Two synthetic residual rows added to T3 (Washington HQ, Undesignated LPI) labeled `Other (not under office subtotal)` to capture orphan leaves and make T3 reconcile exactly to T2. Documented in README rather than enumerated.
- First budget-map artifact `budget_map_v0.md` is markdown at repo root (not a notebook, not HTML). v0 is text + tables; visualizations deferred to v1.

## Results

Committed to the repo this session:

- [`papers/doe_fy27BudgetInBrief_2026.pdf`](https://github.com/danparshall/test_DOE_budget_map/blob/main/papers/doe_fy27BudgetInBrief_2026.pdf) + extracted text + summary (4 commits)
- [`papers/doe_fy27SummaryByOrg_2026.pdf`](https://github.com/danparshall/test_DOE_budget_map/blob/main/papers/doe_fy27SummaryByOrg_2026.pdf) + OCR text + summary (4 commits)
- [`papers/doe_fy27LaboratoryTables_2026.pdf`](https://github.com/danparshall/test_DOE_budget_map/blob/main/papers/doe_fy27LaboratoryTables_2026.pdf) + extracted text + summary (4 commits)
- [`scripts/build_fy27_summary_by_org.py`](https://github.com/danparshall/test_DOE_budget_map/blob/main/scripts/build_fy27_summary_by_org.py) — T1 build script with 30-check reconciliation tree
- [`data/fy27_summary_by_org.csv`](https://github.com/danparshall/test_DOE_budget_map/blob/main/data/fy27_summary_by_org.csv) — T1, 76 rows
- [`scripts/build_fy27_lab_summary.py`](https://github.com/danparshall/test_DOE_budget_map/blob/main/scripts/build_fy27_lab_summary.py) — T2 build script
- [`data/fy27_lab_summary.csv`](https://github.com/danparshall/test_DOE_budget_map/blob/main/data/fy27_lab_summary.csv) — T2, 94 LPI rows
- [`scripts/build_fy27_lab_by_office.py`](https://github.com/danparshall/test_DOE_budget_map/blob/main/scripts/build_fy27_lab_by_office.py) — T3 build script with skip rules + residual logic
- [`data/fy27_lab_by_office.csv`](https://github.com/danparshall/test_DOE_budget_map/blob/main/data/fy27_lab_by_office.csv) — T3, 347 lab × office cells
- [`data/README.md`](https://github.com/danparshall/test_DOE_budget_map/blob/main/data/README.md) — schema, provenance, reconciliation hierarchy, gross-vs-net caveat
- [`budget_map_v0.md`](https://github.com/danparshall/test_DOE_budget_map/blob/main/budget_map_v0.md) — first-cut budget map synthesizing T1+T2+T3

Total commits this session: ~29 (12 from doc ingest, 5 from T1+T2 + data README, 4 from T3 + budget map + README update, plus this convo's update-docs commits).

## Open Questions

- **What's in the remaining ~$10.5B IIJA rescission?** Likely a separate cancellation schedule outside the three documents we have. Probably worth pulling if budget-map work goes deeper into appropriations mechanics.
- **Where does AIQ $1.2B actually flow at the labs?** Currently parked at Washington HQ. The Science volume of the per-organization JEDIs (not yet ingested) would resolve this.
- **What absorbs the −13% Science cut at the sub-program level?** Same JEDI volume would tell us — is it BES, BER, HEP, NP, ASCR, or FES taking the cut. T4 (sub-program flat) would also answer this from the Lab Tables alone.
- **Should we expand to the State Tables (geographic cut) and Summary by Appropriation?** Pre-discovered URLs queued in the prior session's RESEARCH_LOG. Not pulled this session pending Dan's scope decision.
- **The Office of Science cut framed as "investment":** does this BiB pattern repeat for other agencies' FY27 requests? Worth checking against DOE FY26 for whether this is a one-off or a general pattern.
- **§7 upstream issue is composed but not yet filed.** Dan has the pre-filled URL.
