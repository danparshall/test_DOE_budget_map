# Research Log — Science Cut Drill

This line drills into where the FY27 −13.9% Office of Science cut request lands at sub-program × lab level. Produces structured data (T5a from existing Lab Tables; T5b from FY27 Science Volume CBJ) and a focused analytical artifact (deltas + viz + ~500-word narrative). Originating plan is in the parent `20260521_fy26-mapping-scope` line.

---

## Line-level: scope, sources, framing

### Originating plan
`docs/active/20260521_fy26-mapping-scope/plans/science-volume-drill.md`

### Originating conversation
`docs/active/20260521_fy26-mapping-scope/convos/20260521_fy26-mapping-scope.md`

### Plan question resolutions (session 1, 2026-05-21)

- **Q1 — Audience:** General policy literacy + focused analytical artifact. **Not** testimony prep, **not** coalition deliverable.
- **Q2 — New line vs. extend parent:** New line, this one. Deliverables (sub-program × lab CSVs, cut analysis, viz) are distinct from the parent budget-map scope.
- **Q3 — Extramural depth:** **Must-have.** Drives commitment to Phase 2 (Science Volume CBJ ingestion). Phase 1 still ships standalone with extramural noted as known gap; Phase 2 follows. Plan's "Phase 1 ships alone if Phase 2 hits extraction trouble" graceful-degradation is honored — but the deliverable is not complete without the extramural picture.
- **Q4 — Framing (cut-centric vs. composition-centric):** **Deferred.** The composition framing ("ASCR grows while basic research shrinks") presupposes a pattern that the plan flags as "worth confirming, not assuming." Decide after Phase 1 numbers land. Cut-centric is the safe default if the data turns out to be more uniform than expected.

### Sources

| File | Role |
|---|---|
| `papers/text/doe_fy27LaboratoryTables_2026.txt` | Primary source for Phase 1 (T5a). Per-lab Science sub-program rollups. |
| `data/fy27_lab_by_office.csv` (T3) | Reconciliation target — per-lab Science office totals must match. |
| `data/fy27_summary_by_org.csv` (T1) | Reconciliation target for Phase 2 — Science leaf totals. |
| `papers/text/doe_fy27ScienceVolume_2026.txt` | (Pending Phase 2 paper-add) Canonical Science org tree + intramural/extramural split. |

### Calibration: the gross-vs-net Science baseline

The plan headlines a "−13.9% / −$1.15B cut" — this uses the **net discretionary** base from T1 ($8.25B FY26 → $7.10B FY27). T3 (the Phase 1 source) is **gross BA** and shows Science at $8.40B FY26 → $7.14B FY27, a delta of −$1.26B / −15.0%. The $150M gap is IIJA supplemental funding visible in Lab Tables but not in the discretionary org-axis (parent line's RESEARCH_LOG documents this for Science along with similar deltas at CMEI/NE/HGEO). Phase 1's reconciliation tests target the gross ($8.40B) view; the analytical artifact will report both the net and gross views and explain the bridge.

### Schema (T5a — Phase 1 output)

| Column | Type | Description |
|---|---|---|
| `lab_name` | str | Matches T3's `lab_name`. |
| `science_subprogram` | str | ASCR / BES / BER / FES / HEP / NP / ARD&P / SLI / S&S (canonical short forms TBD). |
| `fy25_enacted_k`, `fy26_enacted_k`, `fy27_request_k` | int | $K. |

Note: plan listed 8 sub-programs; source structure also includes **Accelerator R&D and Production** (a 9th sub-program — confirmed at Argonne's Science section).

---

## Session history

### Session 1 — 2026-05-21 — `20260521_science-cut-drill`

(Session in progress. Summary will be added at session end.)
