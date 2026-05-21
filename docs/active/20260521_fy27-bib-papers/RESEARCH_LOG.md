# Research Log — FY27 BiB papers ingestion

This line collects sessions for ingesting the DOE FY2027 Budget-in-Brief corpus
into the repo's `papers/` library. It's a paper-ingestion task, not a research
inquiry per se; each session adds documents until the corpus is sufficient.

---

## Session: 2026-05-21 — `20260521_fy27-bib-papers`

### Topics Explored

- Repo configuration (set `workflow_mode: main_only`)
- Naming convention agreement (Protocol B, FY in ShortTitle, pub year)
- Landing-page hunt for Lab Tables URL (corrected singular → plural)
- Sandbox network constraints — confirmed empirically that in-chat allow-list
  changes do NOT propagate

### Provisional Findings

- DOE landing page: <https://www.energy.gov/cfo/articles/fy-2027-budget-justification>
- DOE document URLs use plural nouns even when the landing page labels singular ("Laboratory Tables", "State Tables")
- `paper-processing-institutional` Step 1 assumes its target domain is in the sandbox allow-list — worth a §7 issue upstream

### Results

None this session.

### Next Steps (for the fresh chat)

After §2 session-start (which will refetch STATUS.md and see `workflow_mode: main_only`),
read this section and pick up here:

**1. Verify connectivity to energy.gov.**

```bash
curl -sI -L -A "Mozilla/5.0" --max-time 15 \
  "https://www.energy.gov/cfo/articles/fy-2027-budget-justification" \
  | head -5
```

Expect `HTTP/2 200`. If you still get `403` with `x-deny-reason: host_not_allowed`,
the allow-list change still hasn't propagated — surface to Dan and don't proceed.

**2. Run `paper-processing-institutional` for each document below.** All three are
already triaged as Protocol B (no need to re-run `add-paper` Step 0):

| Filename (base — no `.pdf`)        | Source URL                                                              |
|------------------------------------|-------------------------------------------------------------------------|
| `doe_fy27BudgetInBrief_2026`       | <https://www.energy.gov/documents/doe-fy-2027-budget-brief>             |
| `doe_fy27SummaryByOrg_2026`        | <https://www.energy.gov/documents/doe-fy-2027-summary-table-organization> |
| `doe_fy27LaboratoryTables_2026`    | <https://www.energy.gov/documents/doe-fy-2027-laboratory-tables>        |

Skill Step 5 (BibTeX) is skipped — `BIB_FILE` is unset in STATUS.md.

**3. Confirm scope before pulling more.** The landing page lists ~25 documents
(Summary by Appropriation, State Tables, NNSA volumes, CMEI, HGEO, Science volumes,
EM, ARPA-E, etc.). Ask Dan before expanding beyond the initial three.

**4. Pre-discovered URLs ready for scope expansion** (don't fetch unless asked):

- <https://www.energy.gov/documents/doe-fy-2027-state-tables> (confirmed via search)
- `doe-fy-2027-summary-table-appropriation` (linked on landing page; pattern verified for siblings)
- `doe-fy-2027-statistical-tables` (likely — pattern is plural; not yet verified)

**5. Optional cleanup — draft a §7 upstream issue** about the
`paper-processing-institutional` Step 1 `curl` assumption. Dan declined to draft
it this session but it's a real skill gap. Body should describe the
`host_not_allowed` failure mode and suggest either (a) a `web_fetch` fallback in
the skill, or (b) a sandbox-aware banner.

### Skill state

- `add-paper` (triage) → routes to `paper-processing-institutional` (Protocol B)
- No need to re-triage in the fresh session; doc class is unambiguous for the entire BiB corpus.
