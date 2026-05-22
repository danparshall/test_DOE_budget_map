# Convo — 20260521_science-cut-drill (session 1)

**Date:** 2026-05-21 (DC)
**Line:** `20260521_science-cut-drill` (main_only mode)
**Originating plan:** `docs/active/20260521_fy26-mapping-scope/plans/science-volume-drill.md`
**Session goal:** Open the line. Resolve the plan's four open questions. Begin Phase 1 (T5a build).

---

## Plan question resolutions

- **Q1 — Audience.** General policy literacy + focused analytical artifact. Not testimony prep, not coalition deliverable.
- **Q2 — New line vs. extend parent.** New line. Confirmed clean state on `main` before opening (only `main` branch; parent line's work all committed; no orphans).
- **Q3 — Extramural depth.** Must-have. Phase 2 (Science Volume CBJ) committed as part of deliverable. Phase 1 ships standalone with extramural noted as known gap; Phase 2 follows. The plan's graceful-degradation pattern (Phase 1 ships alone if Phase 2 hits extraction trouble) is preserved as a fallback.
- **Q4 — Framing.** Deferred. Composition framing ("ASCR grows while basic research shrinks") presupposes a pattern that's well-established in administration messaging but not yet confirmed in the data. Pick after Phase 1 numbers land. If the data turns out more uniform than expected, default to cut-centric.

## Calibration points found before starting Phase 1

These were surfaced by sampling the source before writing the build, not assumed from the plan.

1. **35 Science-funded labs in T3** — not the plan's estimated ~17. About 17 are major labs; the rest are co-located site offices (Argonne Site Office, Brookhaven Site Office, etc.), catch-alls (`Other`, `Undesignated LPI`), and one-offs (Michigan State, ORISE, OSTI). Most site offices are <$10M/yr. T5a should include all 35 for reconciliation to work; whether to filter for the headline analysis is a Phase 3 question.
2. **FY26 Science in T3 = $8,400,000K, not $8,250,000K.** Plan used the net-discretionary base from T1. Phase 1 reconciles against T3 (gross). The $150M delta is the IIJA supplemental noted in the parent line's known-data-quality section. Phase 1 will report both views.
3. **9 sub-programs, not 8.** Plan listed: ASCR / BES / BER / FES / HEP / NP / SLI / S&S. Argonne's section confirms a 9th: **Accelerator R&D and Production** (small line at Argonne — $371K FY25, $0 FY26-27 — but it exists and probably appears at other labs too).
4. **Source structure is messier than "Subtotal, <subprogram>".** Science sub-programs are NOT formatted as `Subtotal, X` rows like the T3 office aggregates. They appear as un-prefixed rollup rows (e.g., `  Advanced Scientific Computing Research   225,984   248,789   241,880`) with their leaves indented one level deeper above them. T5a parsing strategy: match by exact canonical sub-program name within each lab's section, bounded by the lab header and `Subtotal, Science`.

## Phase 1 plan (TDD per the originating plan)

1. Inventory the 35 Science-funded labs from T3.
2. For each, slice the Lab Tables text section between the lab's start and `Subtotal, Science` (within that lab); extract Science sub-program rollups by canonical-name match.
3. Write reconciliation tests FIRST: (a) per-lab sum of sub-programs == T3 Science total for that lab, all three years; (b) global sum of T5a == T3 Science grand total, all three years.
4. Then write the parser. Run tests; iterate until both reconciliations pass.
5. Write `data/fy27_science_by_lab_subprogram.csv` only on pass; fail loudly otherwise (same pattern as `build_fy27_lab_by_office.py`).
6. Update `data/README.md` with T5a section.

(Session work continues below.)
