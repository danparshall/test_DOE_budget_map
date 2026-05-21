# DOE FY 2027 Budget Map — v0

**Status:** First-cut artifact (v0) built from the three FY27 Congressional Justification documents in `papers/` and the three derived tables in `data/`. The structure here is a synthesis target, not a final design — meant to orient and to expose the choices a finished map will need to make. Iterate.

**Last updated:** 2026-05-21 (session `20260521_fy27-bib-ingest`)

**Source documents:**
- BiB (narrative, $53.91B topline): `papers/doe_fy27BudgetInBrief_2026.pdf`
- Summary by Organization (line items): `papers/doe_fy27SummaryByOrg_2026.pdf`
- Laboratory Tables (lab × program detail): `papers/doe_fy27LaboratoryTables_2026.pdf`

**Derived data (all reconciled to source totals):**
- T1 — `data/fy27_summary_by_org.csv` (76 rows; office-level)
- T2 — `data/fy27_lab_summary.csv` (94 rows; lab-level)
- T3 — `data/fy27_lab_by_office.csv` (347 rows; lab × office matrix)

---

## 1. The headline

DOE FY 2027 discretionary request: **$53.91 B**, up $4.81 B / +10% from FY26 enacted ($49.10 B). Two stories sit on top of that topline; the BiB tells one, the line-item data tells the other.

**Story 1 (BiB narrative):** "Unleashing the Golden Era of American Energy Dominance, Accelerating Scientific Capabilities, and Protecting the Nation." Big investments in nuclear deterrent modernization, baseload power, AI infrastructure, and energy security.

**Story 2 (line items):** A defense/non-defense rebalance. NNSA +29%, science / clean energy / consumer-energy programs cut substantially. The narrative does not characterize the cuts; the data shows them.

```
                              FY25 enacted    FY26 enacted    FY27 request    Δ vs FY26
Defense (050)                  $32.97 B       $34.11 B        $41.38 B         +21%
Non-Defense (non-050)          $16.97 B       $15.00 B        $12.53 B         −16%
─────────────────────────────────────────────────────────────────────────────────────
Total DOE discretionary        $49.94 B       $49.10 B        $53.91 B         +10%
```

The $4.81 B topline increase is the net of Defense going up $7.27 B and Non-Defense going down $2.47 B.

---

## 2. Where the money goes (by section)

Top-level section rollups from T1. Numbers are FY 2027 request, $B.

| Section | FY27 | Δ vs FY26 | Share of total |
|---|---|---|---|
| **National Nuclear Security Administration** | $32.80 B | +29% | 60.8% |
| **Direct Reports** (incl. Environmental Management) | $11.44 B | −8% | 21.2% |
| **Undersecretary for Science** | $8.38 B | +1% | 15.5% |
| **Undersecretary for Energy** | $6.71 B | +115% | 12.4% |
| **Energy Projects** (standalone) | $0 | −100% | 0.0% |
| **Receipts and Offsets** | −$5.42 B | offset | −10.0% |
| **Grand Total** | **$53.91 B** | +10% | 100.0% |

Three things to flag in this view:

- **NNSA is 60.8% of the discretionary topline.** Defense activity dominates the request.
- **Undersecretary for Energy is +115%** ($3.13 B → $6.71 B) — but $3.5 B of that growth is the new Baseload Power initiative funded by repurposed IIJA dollars. Without Baseload Power, the section would be roughly flat.
- **Receipts and Offsets jumps from −$0.17 B to −$5.42 B** — almost all of that is the new −$4.7 B "Repurposed IIJA Funding" offset that cancels out against Baseload Power + AIQ on the spending side.

---

## 3. The cuts the BiB narrative omits

These are leaf-level programs from T1 where the FY27 request is meaningfully below FY26 enacted. The BiB does not characterize any of these as cuts.

| Program | FY26 enacted | FY27 request | Δ |
|---|---|---|---|
| Critical Minerals and Energy Innovation (rebranded EERE) | $1.88 B | $1.12 B | **−40%** |
| Office of Science | $8.25 B | $7.14 B | **−13%** |
| Advanced Research Projects Agency - Energy (ARPA-E) | $350 M | $200 M | **−43%** |
| Office of Electricity | $260 M | $203 M | **−22%** |
| Cybersecurity, Energy Security, and Emergency Response (CESER) | $190 M | $160 M | **−16%** |
| Nuclear Energy | $1.69 B | $1.53 B | **−9%** |
| Indian Energy Policy and Programs | $75 M | $50 M | **−33%** |
| Inspector General | $90 M | $77 M | **−14%** |
| Hydrocarbons and Geothermal Energy Office (rebranded Fossil Energy) | $647 M | $676 M | flat |
| Office of Clean Energy Demonstrations | $0 | $0 | (eliminated in FY26, stays eliminated) |
| Statutorily Required Civil Rights/EEO Functions | $4 M | $0 | (proposed to zero) |
| Northeast Home Heating Oil Reserve | $7.15 M | $3.58 M | −50% |
| Tribal Energy Loan Guarantee Program | $6.3 M | $2 M | −68% |

**Cleanest single finding:** the Office of Science line is cut −13% ($1.11 B), but the BiB's framing — "$7.14 billion to support cutting-edge basic research" — doesn't characterize it as a cut. Downstream Science volume of the JEDIs will need re-anchoring on the delta.

**Sneakiest:** the EERE → CMEI rebrand. The new name reframes the office's scope around critical minerals; the actual budget moves −40% in one year and −64% over two years.

---

## 4. The increases

| Program | FY26 enacted | FY27 request | Δ |
|---|---|---|---|
| **Weapons Activities (NNSA)** | $20.38 B | **$27.44 B** | **+35%** ($+7.06 B) |
| **Baseload Power** (new) | $0 | **$3.50 B** | new |
| **Artificial Intelligence and Quantum** (new office) | $0 | **$1.20 B** | new |
| **Title 17 Innovative Technology Loan Guarantee** | −$57 M | $180 M | +$237 M (+416%) |
| Strategic Petroleum Reserve | $206 M | $295 M | +43% |
| Office of Petroleum Reserves (total) | $227 M | $312 M | +38% |
| Defense Uranium Enrichment D&D | $0 | $253 M | new |
| Naval Reactors (NNSA) | $2.13 B | $2.39 B | +12% |
| Federal Salaries and Expenses (NNSA) | $525 M | $577 M | +10% |
| Office of Management | $57 M | $111 M | +95% |
| Office of Fusion (new standalone office) | $0 | $10 M | new |
| Office of Arctic Energy (new office) | $0 | $2 M | new |

**The 60.8% concentration:** Weapons Activities alone is 50.9% of the topline. Together with Defense Nuclear Nonproliferation, Naval Reactors, and NNSA Federal Salaries, the four NNSA programs sum to $32.80 B of the $53.91 B topline.

---

## 5. The IIJA cancellation mechanics

The BiB references "$15.2 billion of unobligated dollars from the Infrastructure Investment and Jobs Act" being cancelled. T1's Receipts and Offsets section + footnotes 5 and 6 of T1 give the FY27 mechanics:

```
−$4.7 B   "Repurposed IIJA Funding"  (offset line)
+$3.5 B   Baseload Power               (new line, funded by repurposed IIJA)
+$1.2 B   Artificial Intelligence and Quantum  (new office, funded by repurposed IIJA)
─────────────────────────────────────────────────────────────
   $0     net effect on topline (the $4.7B cancels against the $4.7B of new spending)
```

So $4.7 B of the $15.2 B cancellation is **reallocated** within FY27 (defense the reallocation, not the rescission, is what shows in the topline). The other ~$10.5 B is **pure rescission against prior-year obligations** — not visible in this corpus.

---

## 6. The Science-vs-NNSA story at lab level

This is the clearest single visualization the FY27 request offers. Pulled from T3 (lab × office). FY27 vs FY26 enacted, $M.

**NNSA-anchored labs (all up):**

| Lab | FY26 | FY27 | Δ |
|---|---|---|---|
| Los Alamos National Laboratory | $5,125 | **$6,754** | **+32%** |
| Sandia National Laboratories | $3,205 | **$3,976** | +24% |
| Lawrence Livermore National Laboratory | $2,646 | **$3,204** | +21% |
| Y-12 National Security Complex | $2,423 | $2,547 | +5% |
| Kansas City National Security Complex | $1,590 | **$2,176** | +37% |
| Nevada National Security Site | $849 | **$1,384** | **+63%** |
| Pantex Plant | $1,182 | $1,359 | +15% |
| Savannah River Site (NNSA tritium + EM cleanup) | $3,430 | **$4,732** | +38% |
| Naval Reactors Facility | $679 | $959 | +41% |

**Office-of-Science-anchored labs (all down):**

| Lab | FY26 | FY27 | Δ |
|---|---|---|---|
| Argonne National Laboratory | $910 | **$754** | **−17%** |
| Lawrence Berkeley National Laboratory | $1,034 | **$831** | **−20%** |
| Brookhaven National Laboratory | $741 | $644 | −13% |
| Oak Ridge National Laboratory | $2,215 | **$1,860** | **−16%** |
| Pacific Northwest National Laboratory | $776 | **$619** | **−20%** |
| SLAC National Accelerator Laboratory | $621 | **$481** | **−22%** |
| Thomas Jefferson National Accelerator Facility | $230 | $215 | −6% |
| Fermi National Accelerator Laboratory | $725 | $803 | +11% *(only Science-lab exception)* |
| Princeton Plasma Physics Laboratory | $106 | $105 | flat |

**Renewables/EERE-dominated sites (deepest cuts):**

| Lab | FY26 | FY27 | Δ |
|---|---|---|---|
| National Laboratory of the Rockies (NREL) | $510 | **$246** | **−52%** |
| Golden Field Office (EERE/CMEI field office) | $601 | **$192** | **−68%** |

---

## 7. AIQ / Genesis Mission — where is the money actually parked?

BiB framing: *"With $1.2 billion to support multiple AI supercomputers at Argonne and Oak Ridge National Laboratories, the DOE's Genesis Mission will integrate the full power of our 17 National Laboratories..."*

T3 actual placement:

| Lab × Office | FY27 ($M) |
|---|---|
| Undesignated LPI × Baseload Power | $3,500 |
| Washington Headquarters × Artificial Intelligence and Quantum | $1,200 |
| Argonne National Laboratory × Artificial Intelligence and Quantum | $0 |
| Oak Ridge National Laboratory × Artificial Intelligence and Quantum | $0 |

**Both the AIQ $1.2 B and the Baseload Power $3.5 B are currently parked at central accounts (Washington Headquarters, Undesignated LPI), not yet flowing to the ANL/ORNL labs that the BiB names.** Per BiB footnotes 5 and 6, both lines repurpose prior-year unobligated IIJA dollars. The mapping from central pool → specific lab will appear in the Science volume of the per-organization JEDIs (not yet in our corpus). Worth tracing once that volume is in `papers/`.

This is the kind of mismatch between narrative and accounting that this map can surface routinely.

---

## 8. Office-level concentration: how lopsided is FY27?

From T3, top 10 offices by total FY27 across all labs:

| Office | FY27 ($M) | Share of lab-level total |
|---|---|---|
| Weapons Activities | $27,400 | 44.3% |
| Science | $7,139 | 11.5% |
| Defense Environmental Cleanup | $6,983 | 11.3% |
| Baseload Power | $3,500 | 5.7% |
| Defense Nuclear Nonproliferation | $2,430 | 3.9% |
| Naval Reactors | $2,395 | 3.9% |
| Nuclear Energy | $1,524 | 2.5% |
| Artificial Intelligence and Quantum | $1,200 | 1.9% |
| Other Defense Activities | $1,185 | 1.9% |
| Critical Minerals and Energy Innovation | $1,122 | 1.8% |

**Weapons Activities alone is 44.3% of DOE's gross lab-level spending in FY27.** The top 3 offices (Weapons Activities, Science, Defense Environmental Cleanup) together are 67.1% — almost exactly two-thirds of all DOE lab spending.

*(Note: This table's totals do NOT exactly match T1's office-level totals because T3 uses gross BA from the Laboratory Tables PDF while T1 uses net discretionary from the Summary by Organization PDF. The gross-vs-net gap is documented in `data/README.md`.)*

---

## Open questions for v1+

Things this v0 deliberately does not do. Each is a candidate task for follow-up.

1. **No visualizations yet.** This is text + tables. A v1 should include at minimum: a treemap (or sunburst) of office × lab, a bar chart of office-level deltas, and a Defense/Non-Defense sankey. Probably worth a separate `notebooks/` or `analysis/` directory.
2. **No reconciliation to the appropriations (vs. request) numbers.** This map is the *request* only. The final FY27 appropriation will likely differ. A v2 should include a column for "Final FY27 enacted" once available, and a delta from request.
3. **No FY28 outyear forecast.** The BiB doesn't show outyears; finding them requires the per-organization JEDIs (not yet in corpus).
4. **No sub-program drill-down.** T3 stops at the office level per lab. Sub-program detail (per-lab × per-sub-program; ~3-5k rows once flattened) lives in pp. 4–124 of the Laboratory Tables PDF and would be T4. Worth building once a specific question requires it.
5. **No outside reference numbers.** This map is purely internal to the DOE request. Cross-referencing to CBO projections, GAO oversight findings, or appropriations subcommittee markup would be a v2 task.
6. **The American Energy Independence Fund mechanics** are still undocumented in our corpus (only footnote references). Track for next document ingestion.
7. **The ~$10.5 B "pure rescission" portion of the $15.2 B IIJA cancellation** is not traced. Probably lives in a separate cancellation schedule outside the three documents we have. Worth pulling if budget-map work goes deeper into appropriations mechanics.
