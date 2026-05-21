# Paper Summaries

Protocol B (institutional) and Protocol A (academic) summaries for documents in the `papers/` collection. Entries are added by `paper-processing-institutional` and `paper-processing-academic` skills. See `PAPER_INDEX.md` for the short-form listing.

---

### DOE FY 2027 Congressional Justification — Budget in Brief

- Institution: U.S. Department of Energy, Office of the Chief Financial Officer (OCFO)
- Date: April 2026
- File: `doe_fy27BudgetInBrief_2026.pdf`
- Source: <https://www.energy.gov/documents/doe-fy-2027-budget-brief>
- DOE document ID: DOE/CF-0222

**(a) What the report argues** — The Budget in Brief (BiB) is the OCFO's executive-level companion to the multi-volume FY 2027 Congressional Justification. It frames the FY27 request as a three-pronged story: *"Unleashing the Golden Era of American Energy Dominance, Accelerating Scientific Capabilities, and Protecting the Nation."* The argued position: rebalance toward defense and traditional energy resources; ramp NNSA modernization; cancel unobligated Infrastructure Investment and Jobs Act (IIJA) funds; and walk Congress through the President's request office by office. As the BiB, it is intentionally concise (≈80 pp) — it presents the rationale and top-line numbers but defers detailed program tables to the per-organization volumes (NNSA, Science, EM, etc.). It is the political narrative of the request, paired with two reference documents in the same release set (Laboratory Tables, Summary by Organization).

**(b) Document type, methods, and findings** —

- **Document provenance:** Annual budget request narrative published by DOE OCFO; DOE/CF-0222; companion to the line-item FY27 Congressional Justification volumes (NNSA, Science/CMEI/HGEO, EM/NE/CESER, etc.), the Summary by Organization, and the Laboratory Tables.
- **Frameworks and databases drawn on:** The BiB is a request document, not a research synthesis — no external frameworks. It does reference the July 2025 DOE *Report on Evaluating U.S. Grid Reliability and Security* as justification for grid/baseload investment, and P.L. 119-21 (the Working Families and Tax Cut Act, "WFTC") which provides mandatory resources to NNSA, the Strategic Petroleum Reserve (SPR), Energy Dominance Financing (EDF), and Science outside the discretionary topline.
- **Headline numerical claims:**
  - **Total discretionary:** $53.91B FY27 request — **+$4.81B / +10%** over FY26 enacted ($49.10B); +$3.97B over FY25 enacted ($49.94B).
  - **Defense (050):** $41.38B FY27 (**+21%** vs FY26 enacted $34.11B). **Non-Defense:** $12.53B FY27 (**−16%** vs FY26 enacted $15.00B). The Defense/Non-Defense rebalance is the clearest structural shift in this request.
  - **NNSA: $32.80B** (**+29%** discretionary; +12% when WFTC mandatory resources are included). Within NNSA: Weapons Activities $27.44B (+35%); Defense Nuclear Nonproliferation $2.39B (+1%); Naval Reactors $2.39B (+12%); Federal Salaries & Expenses $577M (+10%).
  - **Office of Science: $7.14B** — note this is a **−$1.11B / −13% cut** from FY26 enacted $8.25B, despite the BiB narrative framing it as "investments in scientific discovery." The cut is material and the narrative does not flag it explicitly. Watch for full treatment in the Science volume of the per-organization JEDIs.
  - **Environmental Management: $8.18B** discretionary (with $2.95B for Hanford cleanup specifically); EM appropriation total $8.43B is −2% vs FY26.
  - **Critical Minerals and Energy Innovation (CMEI): $1.12B** — this is the **rebranded** Office of Energy Efficiency and Renewable Energy (EERE), with refocused mission on critical mineral supply chains and energy affordability.
  - **Hydrocarbons and Geothermal Energy Office (HGEO): $676M** — **rebranded** Office of Fossil Energy, broadened to include geothermal.
  - **Office of Nuclear Energy (NE): $1.53B**, including $226M for the Advanced Reactors Demonstration Program.
  - **Office of Petroleum Reserves (OPR): $312M** (+38%); plus $5.42B in WFTC reconciliation resources for SPR not counted in the discretionary total.
  - **Energy Dominance Financing (EDF): $191M** (+567% — moved from a small negative net offset to a substantial positive line; functions as a new financing program for baseload projects).
  - **Genesis Mission / AI supercomputers:** $1.2B for AI supercomputers at Argonne and Oak Ridge National Laboratories.
  - **Office of Artificial Intelligence and Quantum (AIQ):** new centralized coordinator for AI, quantum, and Genesis Mission activities Department-wide. Dollar figure folded into Genesis / cross-office allocations.
  - **Office of Fusion (OF): $10M** (new standalone fusion coordination office).
  - **Baseload Power initiative: $3.5B** (new) for upgrades to coal, natural gas plants, nuclear equipment; reconductoring transmission lines; hydropower uprate; new geothermal capacity.
  - **CESER (Cybersecurity, Energy Security, and Emergency Response): $160M.**
  - **Office of Electricity (OE): $203M.**
  - **Office of Legacy Management (LM): $200M** for long-term management of >100 WW2/Cold War era sites.
  - **IIJA cancellation:** **$15.2B of unobligated IIJA dollars proposed for rescission** — a structural counterweight to the discretionary increase that should be tracked separately from the topline.
- **Policy framework or recommendations:** The BiB is a request, not a policy framework, but it embeds several structural choices worth noting: (i) **office rebranding** (EERE→CMEI, Fossil Energy→HGEO) which reframes program scope through renaming; (ii) **creation of two new centralized offices** (AIQ, OF) signaling cross-cutting coordination strategy for AI/quantum and fusion; (iii) **proposed IIJA cancellation paired with new initiatives**, repurposing resources from the prior administration's priorities; (iv) **introduction of the "American Energy Independence Fund"** mentioned only in footnote 1 — collects ~$20M in FY26 collections; the BiB does not yet explain the fund's mechanics or eventual scale.
- **Country case studies:** N/A — domestic budget document.

**(c)** — `CONDITIONAL_SECTION` is unset in `STATUS.md`; section omitted.

**(d) Relevance to the project** —

- **Why this matters for `PROJECT_QUESTION`** ("Mapping the U.S. Department of Energy budget by program and mission area"): This is the canonical top-level entry point for the budget map. The BiB's office-by-office structure (TOC pp. 1–80) is essentially the map's outline. The total ($53.91B), the Defense/Non-Defense split ($41.38B / $12.53B), and the per-office numbers are the anchors against which every more-detailed volume must reconcile. Without this document, the program-level detail in the Summary by Organization and Laboratory Tables has no narrative scaffolding.
- **What position does this report represent:** This is DOE's authoritative public statement of the FY27 *funding request* as transmitted to Congress in April 2026 by the Office of the Chief Financial Officer. It is the **executive branch position** — what Congress ultimately appropriates may differ substantially. Citing the BiB cites the request, not the law.
- **Cross-references in the existing library:** None yet — this is the first paper in the corpus. The companion documents in the same release set (`doe_fy27SummaryByOrg_2026.pdf` for line-item appropriations, `doe_fy27LaboratoryTables_2026.pdf` for lab-level allocations) are queued for ingestion in this session and should cross-reference back to this document for narrative framing.

**Structural caveats and watch items:**

- The narrative's framing of Office of Science as "$7.14B to support cutting-edge basic research" is a **13% cut** compared to FY26 enacted. The BiB does not characterize the change. Downstream summaries of the per-office Science volume should re-anchor on the −13% delta and document where the cut falls (sub-program detail not in BiB).
- Several offices were **renamed** (EERE→CMEI, Fossil Energy→HGEO). Year-over-year program-level comparisons need to be done at sub-program granularity to avoid conflating renaming with substantive change (or vice versa).
- The **American Energy Independence Fund** appears only in a footnote in the BiB — watch for fuller treatment in the Summary by Organization or per-volume justifications. Mechanics, scale, and statutory basis are not yet documented in our corpus.
- **WFTC mandatory resources** (P.L. 119-21) supplement the discretionary topline for NNSA, SPR, EDF, and Science but are not added to the headline $53.91B. Total DOE FY27 outlays including WFTC will be higher; track separately.
- The **$15.2B IIJA rescission** is a budget-mapping consideration in its own right — it's not a program cut visible in the per-office line items but a separate cancellation against prior-year obligations. Map separately from FY27 request flow.

---

### DOE FY 2027 Congressional Justification — Summary Table by Organization

- Institution: U.S. Department of Energy, Office of the Chief Financial Officer (OCFO)
- Date: April 2026
- File: `doe_fy27SummaryByOrg_2026.pdf`
- Source: <https://www.energy.gov/documents/doe-fy-2027-summary-table-organization>
- Pages: 3
- Extraction note: pdftotext failed (the PDF uses a custom-encoded subset font with no `/ToUnicode` CMap, so the byte stream is glyph indices rather than ASCII). Text was recovered via tesseract OCR at 300 DPI on rasterized pages. The OCR output is in `papers/text/doe_fy27SummaryByOrg_2026.txt` with a provenance note prepended. Numbers cited below were spot-checked against the rasterized PDF.

**(a) What the report argues** — This is the reference table accompanying the BiB and the per-volume justifications. It is not a narrative document; it makes no argument as such. Its function is to give Congress (and the public) the complete office-by-office FY25 enacted / FY26 enacted / FY27 request comparison in a single 3-page table, with $ change and % change columns. As a budget map source, this is **the most structurally important document in the FY27 release set**: every other DOE FY27 document is reconciliation against (or detail beneath) the totals here.

**(b) Document type, methods, and findings** —

- **Document provenance:** Annual companion table to the FY27 Congressional Justification; format identical year-over-year. Two columns of historical comparison (FY25 enacted, FY26 enacted) plus the FY27 request, plus computed $ and % deltas.

- **Headline numerical claims (reconciled against the BiB):**
  - **Total Funding by Organization:** $49,944,151k FY25 → $49,104,527k FY26 → **$53,912,977k FY27**; +$4,808,450k / +10% ✓ matches BiB topline.
  - **Total NNSA:** $24,135,000k FY25 → $25,404,000k FY26 → **$32,801,543k FY27**; +$7,397,543k / +29% ✓ matches BiB.
  - **Total Direct Reports:** $13,939,841k FY25 → $12,377,621k FY26 → $11,437,805k FY27; −$939,816k / **−8%** (Direct Reports is the catch-all category for all the small offices outside NNSA/Science/EM/CMEI/etc.).
  - **Total Receipts and Offsets:** −$309,739k FY25 → −$166,063k FY26 → **−$5,417,127k FY27**; −$5,348,621k change (the offset line absorbs most of the structural rebalance).

- **Findings the BiB obscures or omits** — these are the entries where the line-item table reveals something the narrative doesn't say:

  - **Critical Minerals and Energy Innovation (CMEI, formerly EERE): $3,098,341k FY25 → $1,883,250k FY26 → $1,121,742k FY27.** This is **−40% from FY26 enacted** and **−64% from FY25 enacted**. The BiB describes the $1.12B figure but does not characterize the cut. This is the **largest percentage cut among major offices in the FY27 request**.
  - **Office of Science: $8,240,000k FY25 → $8,250,000k FY26 → $7,138,815k FY27 (−13%).** The "Total, Undersecretary for Science" line of $8,378,370k is **+1% over FY26** — but only because the +$1.2B Artificial Intelligence and Quantum (AIQ) line is added underneath the Undersecretary. AIQ funding "repurposes prior year unobligated IIJA funding" per footnote 5 — so the Undersecretary-level "growth" is structurally a reallocation, not new appropriation. The Office of Science line itself is cut 13%.
  - **ARPA-E:** $460M FY25 → $350M FY26 → **$200M FY27 (−43% from FY26)**.
  - **Office of Electricity:** $340M FY25 → $260M FY26 → **$203M FY27 (−22% from FY26)**.
  - **Indian Energy Policy and Programs:** $70M → $75M → **$50M (−33% from FY26)**.
  - **CESER (cybersecurity):** $200M → $190M → **$160M (−16% from FY26)** — the BiB says "$160 million to enhance the security of energy infrastructure" without noting the cut.
  - **Nuclear Energy:** $1,685M → $1,685M → **$1,534M (−9% from FY26)** — despite BiB framing of "supporting the safe expansion of nuclear energy programs."
  - **Office of Clean Energy Demonstrations:** $50M FY25 → $0 FY26 → $0 FY27 (eliminated in FY26 enacted, stays eliminated).
  - **Statutorily Required Civil Rights/EEO Functions:** $0 → $4,025k → $0 (the line was funded in FY26 enacted but proposed to zero in FY27).
  - **Tribal Energy Loan Guarantee Program:** $6.3M → $6.3M → $2M (−65%).
  - **Northeast Home Heating Oil Reserve:** $7.15M → $7.15M → $3.6M (−50%); plus the BiB's footnote about sale of the reserve shows up here as a separate −$100M receipt line.
  - **Inspector General:** $86M → $90M → **$77M (−14%)**.

- **Large increases not in the BiB narrative:**

  - **Title 17 Innovative Technology Loan Guarantee Program:** −$29M FY25 (negative because of net offset accounting) → −$57M FY26 → **+$180M FY27** (a $237M swing, +416%). This is the program through which non-nuclear baseload financing flows.
  - **Office of Management:** $70M → $57M → $111M (+95%).
  - **Specialized Security Activities:** $377M → $441M → $471M (+7%).
  - **Office of Arctic Energy:** new line at **$2M** (did not exist in FY25 or FY26).
  - **Office of International Affairs:** $31M → $22M → $26M (+20% vs FY26 but still below FY25).

- **The IIJA cancellation mechanics (NEW information not in BiB):** The BiB references "$15.2 billion of unobligated dollars from the Infrastructure Investment and Jobs Act" being cancelled. This document shows the FY27 mechanics:

  - **−$4,700,000k "Repurposed IIJA Funding"** appears as an offset in Total Receipts and Offsets (the largest single line in the offsets total).
  - **+$3,500,000k Baseload Power** (new line) "repurposes prior year unobligated IIJA funding" per footnote 6.
  - **+$1,200,000k Artificial Intelligence and Quantum** "repurposes prior year unobligated IIJA funding" per footnote 5.
  - $3.5B + $1.2B = $4.7B reallocation; matches the offset. The other ~$10.5B of the $15.2B IIJA cancellation must appear elsewhere (likely a separate rescission schedule outside this organizational table).

- **WFTC supplement (footnote 4):** Public Law 119-21 (Working Families and Tax Cut Act) provided **$3,885,000k in FY26 funding to DOE/NNSA** that is shown in a separate column on this table and excluded from the "FY 2026 Enacted" discretionary figure. The BiB references this in its "+12% when accounting for mandatory WFTC Act resources" framing.

- **Mandated ATR transfers (footnotes 1–2):** The Advanced Test Reactor at INL receives mandated transfers ($92.8M FY25, $96.7M FY26) from Weapons Activities to the Office of Nuclear Energy; the comparison columns exclude these transfers, so any reader using this table for true year-over-year comparison should add the transfers back into Nuclear Energy's effective funding.

- **American Energy Independence Fund (footnote 3):** $20M in FY26 collections; the BiB also references this in a footnote. No FY27 number disclosed. Mechanics still undocumented in our corpus.

**(c)** — `CONDITIONAL_SECTION` is unset in `STATUS.md`; section omitted.

**(d) Relevance to the project** —

- **Why this matters for `PROJECT_QUESTION`:** This is the **most directly useful single document in the FY27 release set** for the budget-mapping question. It gives every DOE office's three-year trajectory in one place, at sub-program granularity. The BiB provides narrative framing; this document provides the actual numbers. For any budget-map artifact (visualizations, comparisons, deltas), this is the source-of-truth table.
- **What position does this report represent:** This is the OCFO's authoritative line-item summary of the FY27 request. It is reference material rather than political document — the framing is more neutral here than in the BiB. The numbers are the executive branch's request; what Congress appropriates may differ.
- **Cross-references in the existing library:**
  - `doe_fy27BudgetInBrief_2026.pdf` (companion narrative; this table's numbers should match the BiB at the office level).
  - `doe_fy27LaboratoryTables_2026.pdf` (companion; lab-level cross-section of the same dollars).

**Skill-gap findings worth flagging (for §7 upstream issue):**

- `paper-processing-institutional` Step 2 assumes pdftotext or pymupdf will extract clean text. Government PDFs that use custom subset fonts (no `/ToUnicode` CMap) defeat both tools — the byte stream is glyph indices, not Unicode. The fallback that worked here: `pdftoppm -r 300 -png` → `tesseract` on each page. Skill should mention OCR as a sanctioned fallback when the first extraction looks garbled (the symptom is identifiable: control characters in U+0010–U+001F range mixed with printable bytes).
- The Step 2 "Verify the extraction is reasonable: check the first ~20 lines" rule worked correctly here — the garbled extraction was visible in the first chunk and we caught it before writing the summary. The rule is doing its job; what's missing is the next step's documented fallback path.

---
