"""
Parse the FY 2027 Summary Table by Organization (doc #2) into a CSV.

Source: papers/text/doe_fy27SummaryByOrg_2026.txt (tesseract OCR)
Output: data/fy27_summary_by_org.csv

Because the source is OCR'd text from a PDF with custom-encoded fonts (not
pdftotext-extractable), this parser uses MANUAL TRANSCRIPTION of the table
values, with reconciliation checks against the document's printed subtotals
and grand total. Every cell was verified against either the OCR output or
the rasterized PNG (`pdftoppm -r 300`) of the source PDF.

Schema:
  - line (str): Program / office / subtotal label as printed
  - fy25_enacted_k (int): FY 2025 enacted, $ in thousands
  - fy26_enacted_k (int): FY 2026 enacted, $ in thousands
  - fy27_request_k (int): FY 2027 President's Budget request, $ in thousands
  - delta_k (int): FY27 - FY26 (computed, not transcribed)
  - pct_change (float | None): (FY27 / FY26 - 1) * 100 (computed); None when FY26 == 0
  - group (str): NNSA | Undersecretary for Science | Undersecretary for Energy |
                  Direct Reports | Other | Receipts and Offsets | Grand Total
  - subgroup (str | None): Petroleum Reserves | Energy Dominance Financing |
                           Power Marketing Administrations | Environmental Management
                           (None for rows that don't belong to a nested subtotal)
  - level (str): leaf | subtotal | section_total | grand_total
  - footnote (str | None): "4" for Weapons Activities, "5" for AIQ, "6" for
                           Baseload Power (footnotes from the source document)
  - notes (str | None): Free-text observations

Reconciliation hierarchy (every node verified at run time):
  Grand Total = NNSA + UndersecSci + UndersecEnergy + DirectReports + EnergyProjects + Offsets
  NNSA section_total = sum(NNSA leaves)
  UndersecSci section_total = sum(Sci leaves)
  UndersecEnergy section_total = sum(Energy leaves + nested subtotals)
    where nested subtotals: Petroleum Reserves, Energy Dominance Financing, Power Marketing Admins
  DirectReports section_total = sum(DR leaves + EM subtotal)
    where EM subtotal = sum(EM leaves)
  Receipts and Offsets section_total = sum(offset leaves)
  Energy Projects: standalone leaf (not in any subtotal)

OCR error caught: Tribal Energy Loan Guarantee Program FY26→FY27 was reported as
-65% in OCR but PNG verification shows -68%. Document's printed % uses
integer rounding; the parser computes pct exactly from dollar values.
"""
import csv
import sys
from pathlib import Path

REPO_ROOT = Path("/home/claude/repo_local")
OUT = REPO_ROOT / "data/fy27_summary_by_org.csv"


# Each entry is (line, fy25_k, fy26_k, fy27_k, group, subgroup, level, footnote, notes)
# Values transcribed verbatim from OCR + PNG-verified for ambiguous lines.
# Em-dashes in the source ("—") represent $0 unless otherwise noted.
ROWS = [
    # ==================== NNSA ====================
    ("Federal Salaries and Expenses",
        500_000, 525_000, 577_097, "NNSA", None, "leaf", None, None),
    ("Weapons Activities",
        19_293_000, 20_378_000, 27_441_159, "NNSA", None, "leaf", "4",
        "Footnote 4: P.L. 119-21 (WFTC) provided $3,885,000k mandatory FY26 supplement."),
    ("Defense Nuclear Nonproliferation",
        2_396_000, 2_367_000, 2_389_595, "NNSA", None, "leaf", None, None),
    ("Naval Reactors",
        1_946_000, 2_134_000, 2_393_692, "NNSA", None, "leaf", None, None),
    ("Total, National Nuclear Security Administration",
        24_135_000, 25_404_000, 32_801_543, "NNSA", None, "section_total", None, None),

    # ==================== Undersecretary for Science ====================
    ("Science",
        8_240_000, 8_250_000, 7_138_815, "Undersecretary for Science", None,
        "leaf", None, "Office of Science; -13% from FY26 enacted."),
    ("Artificial Intelligence and Quantum",
        0, 0, 1_200_000, "Undersecretary for Science", None, "leaf", "5",
        "New office FY27. Footnote 5: repurposes prior year unobligated IIJA funding."),
    ("Office of Fusion",
        0, 0, 10_000, "Undersecretary for Science", None, "leaf", None,
        "New standalone office FY27."),
    ("Strategy & Technology Roadmaps",
        0, 0, 3_000, "Undersecretary for Science", None, "leaf", None,
        "New office FY27."),
    ("Office of Technology Commercialization",
        20_000, 13_000, 26_555, "Undersecretary for Science", None, "leaf", None, None),
    ("Total, Undersecretary for Science",
        8_260_000, 8_263_000, 8_378_370, "Undersecretary for Science", None,
        "section_total", None, None),

    # ==================== Undersecretary for Energy ====================
    ("Cybersecurity, Energy Security and Emergency Response",
        200_000, 190_000, 160_173, "Undersecretary for Energy", None, "leaf", None,
        "CESER. -16% from FY26."),
    ("Nuclear Energy",
        1_685_000, 1_685_000, 1_533_735, "Undersecretary for Energy", None, "leaf", None,
        "Office of Nuclear Energy. -9% from FY26."),
    ("Nuclear Waste Disposal Fund",
        12_040, 12_040, 12_040, "Undersecretary for Energy", None, "leaf", None, None),
    ("Hydrocarbons and Geothermal Energy Office",
        1_226_909, 647_000, 676_042, "Undersecretary for Energy", None, "leaf", None,
        "HGEO. Rebranded from Office of Fossil Energy."),
    # Petroleum Reserves nested subtotal
    ("Strategic Petroleum Reserve",
        213_390, 206_325, 295_102, "Undersecretary for Energy", "Petroleum Reserves",
        "leaf", None, None),
    ("Naval Petroleum and Oil Shale Reserves",
        13_010, 13_000, 13_000, "Undersecretary for Energy", "Petroleum Reserves",
        "leaf", None, None),
    ("SPR Petroleum Account",
        100, 100, 100, "Undersecretary for Energy", "Petroleum Reserves",
        "leaf", None, None),
    ("Northeast Home Heating Oil Reserve",
        7_150, 7_150, 3_575, "Undersecretary for Energy", "Petroleum Reserves",
        "leaf", None, None),
    ("Total, Petroleum Reserves",
        233_650, 226_575, 311_777, "Undersecretary for Energy", "Petroleum Reserves",
        "subtotal", None, None),
    # End Petroleum Reserves
    ("Electricity",
        339_750, 259_750, 203_477, "Undersecretary for Energy", None, "leaf", None,
        "Office of Electricity. -22% from FY26."),
    ("Baseload Power",
        0, 0, 3_500_000, "Undersecretary for Energy", None, "leaf", "6",
        "New initiative FY27. Footnote 6: repurposes prior year unobligated IIJA funding."),
    ("Indian Energy Policy and Programs",
        70_000, 75_000, 50_038, "Undersecretary for Energy", None, "leaf", None,
        "-33% from FY26."),
    ("Office of Clean Energy Demonstrations",
        50_000, 0, 0, "Undersecretary for Energy", None, "leaf", None,
        "Eliminated in FY26 enacted; stays eliminated FY27."),
    # Energy Dominance Financing nested subtotal
    ("Title 17 Innovative Technology Loan Guarantee Program",
        -29_140, -56_753, 179_588, "Undersecretary for Energy",
        "Energy Dominance Financing", "leaf", None,
        "Sign change: FY25/FY26 net offset, FY27 positive funding."),
    ("Advanced Technology Vehicles Manufacturing Loan Program",
        13_000, 9_500, 9_500, "Undersecretary for Energy",
        "Energy Dominance Financing", "leaf", None, None),
    ("Tribal Energy Loan Guarantee Program",
        6_300, 6_300, 2_000, "Undersecretary for Energy",
        "Energy Dominance Financing", "leaf", None,
        "OCR reported -65%; PNG verifies -68%."),
    ("Total, Energy Dominance Financing",
        -9_840, -40_953, 191_088, "Undersecretary for Energy",
        "Energy Dominance Financing", "subtotal", None,
        "+567% from FY26 enacted (printed)."),
    # End Energy Dominance Financing
    # Power Marketing Administrations nested subtotal
    ("Southeastern Power Administration",
        0, 0, 0, "Undersecretary for Energy", "Power Marketing Administrations",
        "leaf", None, None),
    ("Southwestern Power Administration",
        11_440, 10_400, 10_400, "Undersecretary for Energy", "Power Marketing Administrations",
        "leaf", None, None),
    ("Western Area Power Administration",
        99_872, 63_372, 63_388, "Undersecretary for Energy", "Power Marketing Administrations",
        "leaf", None, None),
    ("Falcon and Amistad Operating and Maintenance Fund",
        228, 228, 228, "Undersecretary for Energy", "Power Marketing Administrations",
        "leaf", None, None),
    ("Colorado River Basin Marketing Fund",
        0, 0, 0, "Undersecretary for Energy", "Power Marketing Administrations",
        "leaf", None, None),
    ("Total, Power Marketing Administrations",
        111_540, 74_000, 74_016, "Undersecretary for Energy", "Power Marketing Administrations",
        "subtotal", None, None),
    # End Power Marketing Administrations
    ("Total, Undersecretary for Energy",
        3_919_049, 3_128_412, 6_712_386, "Undersecretary for Energy", None,
        "section_total", None, None),

    # ==================== Direct Reports ====================
    # Environmental Management nested subtotal (within Direct Reports)
    ("Non-Defense Environmental Cleanup",
        342_000, 322_371, 338_490, "Direct Reports", "Environmental Management",
        "leaf", None, None),
    ("Uranium Enrichment Decontamination and Decommissioning",
        855_000, 865_000, 854_583, "Direct Reports", "Environmental Management",
        "leaf", None, None),
    ("Defense Environmental Cleanup",
        7_285_000, 7_375_000, 6_983_318, "Direct Reports", "Environmental Management",
        "leaf", None, None),
    ("Defense Uranium Enrichment D&D",
        285_000, 0, 253_000, "Direct Reports", "Environmental Management",
        "leaf", None, "FY26 enacted = $0; FY27 restored."),
    ("Total, Environmental Management",
        8_767_000, 8_562_371, 8_429_391, "Direct Reports", "Environmental Management",
        "subtotal", None, None),
    # End EM
    ("Critical Minerals and Energy Innovation",
        3_098_341, 1_883_250, 1_121_742, "Direct Reports", None, "leaf", None,
        "CMEI. Rebranded from EERE. -40% from FY26; -64% over 2 years."),
    ("Environment, Health, Safety, and Security",
        231_263, 230_463, 231_940, "Direct Reports", None, "leaf", None, None),
    ("Office of Enterprise Assessments",
        94_154, 86_154, 88_815, "Direct Reports", None, "leaf", None, None),
    ("Specialized Security Activities",
        377_000, 441_000, 471_082, "Direct Reports", None, "leaf", None, None),
    ("Legacy Management",
        196_302, 198_208, 200_386, "Direct Reports", None, "leaf", None, None),
    ("Office of Hearings And Appeals",
        5_499, 4_499, 5_023, "Direct Reports", None, "leaf", None, None),
    ("Advanced Research Projects Agency - Energy",
        460_000, 350_000, 200_292, "Direct Reports", None, "leaf", None,
        "ARPA-E. -43% from FY26."),
    ("Energy Information Administration",
        135_000, 135_000, 135_370, "Direct Reports", None, "leaf", None, None),
    ("Office of the Secretary",
        6_642, 6_642, 6_717, "Direct Reports", None, "leaf", None, None),
    ("Congressional & Intergovernmental Affairs",
        5_500, 5_000, 7_032, "Direct Reports", None, "leaf", None, None),
    ("Office of the Chief Financial Officer",
        63_283, 62_500, 64_325, "Direct Reports", None, "leaf", None, None),
    ("Chief Information Officer",
        219_000, 196_862, 205_359, "Direct Reports", None, "leaf", None, None),
    ("Industrial Emission and Technology Coordination",
        1_000, 0, 0, "Direct Reports", None, "leaf", None,
        "FY25 only; eliminated FY26-FY27."),
    ("Office of Management",
        70_000, 56_576, 110_510, "Direct Reports", None, "leaf", None, "+95% from FY26."),
    ("Project Management",
        16_000, 10_890, 11_000, "Direct Reports", None, "leaf", None, None),
    ("Office of Human Capital Management",
        38_500, 30_509, 34_264, "Direct Reports", None, "leaf", None, None),
    ("Office of Small & Disadvantaged Business Utilization",
        4_800, 2_500, 3_000, "Direct Reports", None, "leaf", None, None),
    ("General Counsel",
        37_000, 38_000, 41_176, "Direct Reports", None, "leaf", None, None),
    ("Office of Policy",
        24_950, 15_000, 18_064, "Direct Reports", None, "leaf", None, None),
    ("Office of Arctic Energy",
        0, 0, 2_000, "Direct Reports", None, "leaf", None, "New office FY27."),
    ("Public Affairs",
        4_500, 6_750, 7_032, "Direct Reports", None, "leaf", None, None),
    ("Office of International Affairs",
        31_000, 22_000, 26_463, "Direct Reports", None, "leaf", None, None),
    ("Statutorily Required Civil Rights/EEO Functions",
        0, 4_025, 0, "Direct Reports", None, "leaf", None,
        "Proposed to zero in FY27 after FY26 funding."),
    ("Minority Economic Impact",
        27_685, 0, 0, "Direct Reports", None, "leaf", None,
        "FY25 only; eliminated FY26-FY27."),
    ("Strategic Partnership Projects",
        40_000, 40_000, 40_000, "Direct Reports", None, "leaf", None, None),
    ("Inspector General",
        86_000, 90_000, 77_400, "Direct Reports", None, "leaf", None, "-14% from FY26."),
    ("Miscellaneous Revenues",
        -100_578, -100_578, -100_578, "Direct Reports", None, "leaf", None,
        "Negative line: revenue receipts offsetting BA."),
    ("Total, Direct Reports",
        13_939_841, 12_377_621, 11_437_805, "Direct Reports", None,
        "section_total", None, None),

    # ==================== Other (standalone, outside subtotals) ====================
    ("Energy Projects",
        0, 97_557, 0, "Other", None, "leaf", None,
        "Standalone line — not part of Direct Reports or Receipts/Offsets totals. "
        "FY26 only; goes to zero FY27."),

    # ==================== Receipts and Offsets ====================
    ("Excess Fees and Recovery, FERC",
        -9_000, -9_000, -9_000, "Receipts and Offsets", None, "leaf", None,
        "OCR rendered 'Fees' as 'Fess'."),
    ("Title XVII Loan Guar. Prog Section 1703 Negative Credit Subsidy Receipt",
        -15_739, -157_063, -355_127, "Receipts and Offsets", None, "leaf", None, None),
    ("UED&D Fund Offset",
        -285_000, 0, -253_000, "Receipts and Offsets", None, "leaf", None,
        "FY26 enacted = 0."),
    ("Sale of Northeast Home Heating Oil Reserve",
        0, 0, -100_000, "Receipts and Offsets", None, "leaf", None,
        "New FY27 receipt from asset sale."),
    ("Repurposed IIJA Funding",
        0, 0, -4_700_000, "Receipts and Offsets", None, "leaf", None,
        "New FY27 offset. Reallocates to Baseload Power ($3.5B) + AIQ ($1.2B). "
        "$4.7B of the $15.2B IIJA cancellation visible here; remaining ~$10.5B "
        "is pure rescission not in this table."),
    ("Total, Receipts and Offsets",
        -309_739, -166_063, -5_417_127, "Receipts and Offsets", None,
        "section_total", None, None),

    # ==================== Grand Total ====================
    ("Total, Funding by Organization",
        49_944_151, 49_104_527, 53_912_977, "Grand Total", None,
        "grand_total", None, None),
]


def reconcile(rows: list[dict]) -> bool:
    """Run full reconciliation tree. Return True if all checks pass."""
    by_line = {r["line"]: r for r in rows}
    ok = True

    def check(name: str, expected_line: str, *leaf_filter):
        nonlocal ok
        if expected_line not in by_line:
            print(f"  ✗ {name}: '{expected_line}' not found in rows", file=sys.stderr)
            ok = False
            return
        expected = by_line[expected_line]
        # Find all leaves matching the filter
        matches = [r for r in rows if r["level"] == "leaf" and all(
            r.get(k) == v for k, v in leaf_filter[0].items())]
        for yr in ("fy25_enacted_k", "fy26_enacted_k", "fy27_request_k"):
            s = sum(m[yr] for m in matches)
            if s != expected[yr]:
                print(f"  ✗ {name} {yr}: sum {s:,} != printed {expected[yr]:,} "
                      f"(diff {s - expected[yr]:+,}; n={len(matches)} leaves)",
                      file=sys.stderr)
                ok = False
            else:
                print(f"  ✓ {name} {yr}: {s:,}")

    # Nested subtotals (sum leaves within subgroup)
    check("Petroleum Reserves subtotal", "Total, Petroleum Reserves",
          {"subgroup": "Petroleum Reserves"})
    check("Energy Dominance Financing subtotal", "Total, Energy Dominance Financing",
          {"subgroup": "Energy Dominance Financing"})
    check("Power Marketing Administrations subtotal", "Total, Power Marketing Administrations",
          {"subgroup": "Power Marketing Administrations"})
    check("Environmental Management subtotal", "Total, Environmental Management",
          {"subgroup": "Environmental Management"})

    # Section totals (sum leaves + nested subtotals within group)
    # For section totals, leaves can have subgroup=None OR subgroup=any-of-the-nested
    # but we should treat nested-subtotal-rows as the rollup of their leaves
    # — so the section total = sum(leaves where group==X) (which includes both
    # standalone leaves and the leaves under nested subgroups).
    check("NNSA section total", "Total, National Nuclear Security Administration",
          {"group": "NNSA"})
    check("Undersec Sci section total", "Total, Undersecretary for Science",
          {"group": "Undersecretary for Science"})
    check("Undersec Energy section total", "Total, Undersecretary for Energy",
          {"group": "Undersecretary for Energy"})
    check("Direct Reports section total", "Total, Direct Reports",
          {"group": "Direct Reports"})
    check("Receipts and Offsets section total", "Total, Receipts and Offsets",
          {"group": "Receipts and Offsets"})

    # Grand total = all section_totals + Energy Projects
    print()
    grand = by_line["Total, Funding by Organization"]
    section_total_lines = [r for r in rows if r["level"] == "section_total"]
    energy_projects = by_line["Energy Projects"]
    for yr in ("fy25_enacted_k", "fy26_enacted_k", "fy27_request_k"):
        s = sum(r[yr] for r in section_total_lines) + energy_projects[yr]
        if s != grand[yr]:
            print(f"  ✗ Grand Total {yr}: sum {s:,} != printed {grand[yr]:,} "
                  f"(diff {s - grand[yr]:+,})", file=sys.stderr)
            ok = False
        else:
            print(f"  ✓ Grand Total {yr}: {s:,}")

    return ok


def main() -> int:
    # Build dict rows with computed delta and pct_change
    rows = []
    for tup in ROWS:
        line, fy25, fy26, fy27, group, subgroup, level, footnote, notes = tup
        delta = fy27 - fy26
        if fy26 == 0:
            pct = None
        else:
            pct = round((fy27 - fy26) / fy26 * 100, 2)
        rows.append({
            "line": line,
            "fy25_enacted_k": fy25,
            "fy26_enacted_k": fy26,
            "fy27_request_k": fy27,
            "delta_k": delta,
            "pct_change": pct,
            "group": group,
            "subgroup": subgroup,
            "level": level,
            "footnote": footnote,
            "notes": notes,
        })

    print(f"Parsed {len(rows)} rows. Running reconciliation...\n")
    if not reconcile(rows):
        print("\nReconciliation FAILED. Do NOT commit; fix transcription errors.",
              file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "line", "fy25_enacted_k", "fy26_enacted_k", "fy27_request_k",
            "delta_k", "pct_change", "group", "subgroup", "level",
            "footnote", "notes"
        ])
        w.writeheader()
        w.writerows(rows)

    print(f"\n✓ Reconciliation PASSED. Wrote {OUT.relative_to(REPO_ROOT)} "
          f"({len(rows)} rows).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
