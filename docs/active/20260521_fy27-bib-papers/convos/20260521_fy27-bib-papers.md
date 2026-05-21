# FY27 BiB papers — session 1 (discovery, blocked on connectivity)

**Date:** 2026-05-21
**Branch:** main (`workflow_mode: main_only`)
**Surface:** claude.ai
**Convo name:** `20260521_fy27-bib-papers`

## Summary

Session was scoped to bulk-ingest three FY2027 DOE Budget-in-Brief volumes via the
`paper-processing-institutional` skill. Most of the time went into legitimate
session-start work — confirming the fresh repo's configuration, agreeing on the
institutional naming convention, locating the Lab Tables URL (which DOE's landing
page mislabels as singular), and probing sandbox network constraints.

No papers were actually ingested. Session hit a hard blocker when `curl` to
`energy.gov` returned HTTP 403 with proxy header `x-deny-reason: host_not_allowed`
— meaning the bash-tool egress proxy didn't permit the domain. Dan changed
claude.ai Settings → Domain Allow List → "all domains", but a re-probe in the
same chat still returned the same `host_not_allowed`. This confirms the upstream
Appendix's empirical note: in-chat allow-list changes do not propagate. A fresh
chat is required to pick up the new setting.

## Topics Explored

- Fresh repo state: no research lines, no `workflow_mode` field (default = `branches`)
- Agreed to switch to `workflow_mode: main_only` (committed; see STATUS.md commit `87ae27f`)
- Triaged FY27 BiB documents as Protocol B (institutional): no abstract, no hypothesis, synthesis docs from a government agency — no need for per-document triage
- Naming convention: `{Institution}_{ShortTitle}_{Year}.pdf` (skill default since `paper_naming.institutional_format` is unset in `personal_info.md`); using pub year 2026 with FY in the ShortTitle
- Located the landing page: <https://www.energy.gov/cfo/articles/fy-2027-budget-justification> — hub for the full FY27 BiB corpus (~25 documents)
- Discovered Lab Tables URL: <https://www.energy.gov/documents/doe-fy-2027-laboratory-tables> — the landing page labels it singular ("Laboratory Table") but the actual document URL is plural
- Bonus URLs from the same pattern: <https://www.energy.gov/documents/doe-fy-2027-state-tables>; likely (unverified) `doe-fy-2027-summary-table-appropriation` and `doe-fy-2027-statistical-tables`
- Confirmed `web_fetch` to BiB returns the PDF content directly (mime: `application/pdf`); useful as a fallback if bash `curl` to energy.gov ever fails again

## Provisional Findings

- DOE's CMS appears to auto-pluralize document slugs from titles ("Laboratory Tables" body text → `-tables` URL), so the landing page's singular labels are misleading. Always test plural first when guessing a DOE document URL.
- The `paper-processing-institutional` skill's Step 1 (`curl -L -o papers/file.pdf URL`) assumes the target domain is in the sandbox allow-list. For non-allow-listed domains in claude.ai, the skill silently fails or returns a proxy 403 with `x-deny-reason: host_not_allowed`. Worth a §7 upstream issue suggesting the skill banner mention this. Mitigation: `web_fetch` works regardless of bash allow-list (and even returns extracted text by default for PDFs).

## Decisions Made

- `workflow_mode: main_only` — locked in STATUS.md (commit `87ae27f`)
- Filenames: `doe_fy27BudgetInBrief_2026`, `doe_fy27SummaryByOrg_2026`, `doe_fy27LaboratoryTables_2026` (note plural on the third — matches the doc's own title)
- Convo name: `20260521_fy27-bib-papers`
- Binary-vs-text-only PDF storage — **deferred** to the fresh session. With `curl` now expected to work, recommend the standard binary-download flow per the skill.

## Open Questions

- Will the "all domains" setting propagate in the next chat? High confidence yes (we got `host_not_allowed` from the proxy rather than a connection error, indicating the proxy is the gate and a fresh session should respect the new settings). Verify before assuming.
- Scope: only the three starter docs Dan listed, or also pull adjacent volumes? The landing page lists ~25 entries. Ask before scope creep.

## Results

None.
