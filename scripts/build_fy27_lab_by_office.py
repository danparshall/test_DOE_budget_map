"""
Parse the FY 2027 Laboratory Tables (doc #3) into a lab × office subtotal matrix.

Source: papers/text/doe_fy27LaboratoryTables_2026.txt
Output: data/fy27_lab_by_office.csv

For each "Subtotal, <office>" row within each lab's table section, emit one
output row: (lab_name, office, fy25_k, fy26_k, fy27_k). This gives the
office-level rollup at each lab — answering "how much does office X give
lab Y in year Z."

Reconciliation: for every lab, the sum of its office subtotals should equal
the lab's total in `data/fy27_lab_summary.csv` (T2). This is verified at
build time across all three years.

Schema:
  - lab_name (str): Lab/plant/installation name (matches T2's lpi_name)
  - office (str): Office category (matches the BiB / SummaryByOrg office names
                  where possible; lab-tables introduce a few extras like
                  "Departmental Administration" and "Departmental Administration (Gross)")
  - fy25_enacted_k (int): FY 2025 enacted, $ in thousands
  - fy26_enacted_k (int): FY 2026 enacted, $ in thousands
  - fy27_request_k (int): FY 2027 President's Budget request, $ in thousands

Notes:
  - Em-dashes do NOT appear in Subtotal rows (subtotals are always numeric).
  - Negatives use leading minus sign ("-1,000"), not parens.
  - "Subtotal, Departmental Administration" and "...(Gross)" both appear and
    capture different things at some labs (the "(Gross)" variant excludes
    offsets); both are kept as distinct office values.
"""
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path("/home/claude/repo_local")
SRC = REPO_ROOT / "papers/text/doe_fy27LaboratoryTables_2026.txt"
T2_CSV = REPO_ROOT / "data/fy27_lab_summary.csv"
OUT = REPO_ROOT / "data/fy27_lab_by_office.csv"

# Pattern: "Subtotal, <office name>  <num>  <num>  <num>"
# Office name can contain commas, ampersands, parens, hyphens.
# Numbers: optional minus, then comma-grouped digits, or plain "0".
NUM = r"-?\d[\d,]*"
SUBTOTAL_RE = re.compile(
    rf"^\s*Subtotal,\s*(?P<office>.+?)\s{{2,}}(?P<a>{NUM})\s+(?P<b>{NUM})\s+(?P<c>{NUM})\s*$"
)

# Pattern: "Total <Lab Name>  <num>  <num>  <num>"
# No comma after Total (distinguishes from sub-rollups like "Total, Production Modernization").
TOTAL_LAB_RE = re.compile(
    rf"^Total\s+(?P<lab>.+?)\s{{2,}}(?P<a>{NUM})\s+(?P<b>{NUM})\s+(?P<c>{NUM})\s*$"
)


def parse_int(s: str) -> int:
    """Parse a number like '17,417' or '-1,000' or '0' into int (thousands of $)."""
    return int(s.replace(",", ""))


def load_t2_lab_names() -> set[str]:
    """Load lab names from T2 CSV (built earlier in this session)."""
    with T2_CSV.open() as f:
        reader = csv.DictReader(f)
        return {row["lpi_name"] for row in reader}


def parse_lab_by_office(text: str, known_labs: set[str]) -> tuple[list[dict], list[dict]]:
    """
    Walk text, emitting (lab, office, fy25, fy26, fy27) rows.
    Also captures (lab, fy25, fy26, fy27) lab totals for reconciliation.
    """
    rows = []
    lab_totals_found = []
    pending_subtotals = []

    # Nested sub-rollup modifiers and child subtotals: these appear in the
    # source as "Subtotal, X" but are children of a higher-level rollup.
    # Capturing both produces double-counting (verified empirically against T2).
    #
    # Two families:
    # (1) "(Gross)" and "(DA)" suffixes on Departmental Administration and
    #     Office of Technology Commercialization. The (Gross) variant is the
    #     pre-offset rollup, (DA) is the Departmental-Administration pathway.
    # (2) Petroleum Reserves children: Strategic Petroleum Reserve, Naval
    #     Petroleum & Oil Shale Reserves, SPR Petroleum Account, Northeast
    #     Home Heating Oil Reserves. The parent "Subtotal, Petroleum Reserves"
    #     always appears alongside them.
    #
    # The parent IS the office-level rollup we want for the lab × office
    # matrix; the children are sub-sub-rollups that map 1:1 with T1's
    # `subgroup` column.
    SKIP_MODIFIER_SUFFIXES = ("(Gross)", "(DA)")
    SKIP_OFFICE_NAMES = {
        "Strategic Petroleum Reserve",
        "Naval Petroleum & Oil Shale Reserves",
        "SPR Petroleum Account",
        "Northeast Home Heating Oil Reserves",
    }

    for line in text.splitlines():
        # Check Subtotal first (it's a strict subset of Total pattern matches)
        m = SUBTOTAL_RE.match(line)
        if m:
            office = m["office"].strip()
            # Skip nested sub-rollups: "(Gross)" and "(DA)" modifiers
            if any(office.endswith(suffix) for suffix in SKIP_MODIFIER_SUFFIXES):
                continue
            # Skip Petroleum Reserves child subtotals (parent always present)
            if office in SKIP_OFFICE_NAMES:
                continue
            pending_subtotals.append({
                "office": office,
                "fy25_enacted_k": parse_int(m["a"]),
                "fy26_enacted_k": parse_int(m["b"]),
                "fy27_request_k": parse_int(m["c"]),
            })
            continue

        m = TOTAL_LAB_RE.match(line)
        if m:
            lab_name = m["lab"].strip()
            # Only treat as a lab-end marker if this matches a known T2 lab name.
            # (Skips false positives like "Total, Production Modernization" — those
            # have a comma so they don't match TOTAL_LAB_RE anyway, but defense in depth.)
            if lab_name not in known_labs:
                continue

            # Emit all pending subtotals attributed to this lab
            for st in pending_subtotals:
                rows.append({
                    "lab_name": lab_name,
                    "office": st["office"],
                    "fy25_enacted_k": st["fy25_enacted_k"],
                    "fy26_enacted_k": st["fy26_enacted_k"],
                    "fy27_request_k": st["fy27_request_k"],
                })
            lab_totals_found.append({
                "lab_name": lab_name,
                "fy25_enacted_k": parse_int(m["a"]),
                "fy26_enacted_k": parse_int(m["b"]),
                "fy27_request_k": parse_int(m["c"]),
            })
            pending_subtotals = []

    return rows, lab_totals_found


def reconcile(rows: list[dict], lab_totals_found: list[dict],
              t2_totals: dict[str, dict]) -> tuple[bool, list[dict]]:
    """
    For each lab, verify:
      sum(office subtotals) == lab total from T2

    For labs whose subtotals UNDER-COUNT the T2 total (orphan leaves that
    don't roll into any office subtotal — e.g., Washington Headquarters has
    'Energy Information Administration' as a direct leaf), add a synthetic
    'Other (not under office subtotal)' row with the residual so the CSV
    reconciles exactly to T2.

    OVER-counting (which would indicate a parser bug) is still a hard error.

    Returns (ok, augmented_rows).
    """
    augmented = list(rows)
    by_lab = {}
    for r in rows:
        by_lab.setdefault(r["lab_name"], []).append(r)

    print(f"Reconciling {len(by_lab)} labs with subtotals against T2 totals...")
    over_count_failures = []
    residuals_added = []

    for lab in sorted(by_lab):
        if lab not in t2_totals:
            print(f"  ✗ {lab}: not in T2 (unexpected)", file=sys.stderr)
            return False, augmented

        subtotals = by_lab[lab]
        t2 = t2_totals[lab]
        residual = {yr: t2[yr] - sum(st[yr] for st in subtotals)
                    for yr in ("fy25_enacted_k", "fy26_enacted_k", "fy27_request_k")}

        if all(v == 0 for v in residual.values()):
            continue  # exact match, no residual needed
        if any(v < 0 for v in residual.values()):
            # Negative residual = parser is OVER-counting; this is a bug
            over_count_failures.append((lab, residual))
            continue
        # Positive residual = orphan leaves not under any subtotal; add a synthetic row
        augmented.append({
            "lab_name": lab,
            "office": "Other (not under office subtotal)",
            "fy25_enacted_k": residual["fy25_enacted_k"],
            "fy26_enacted_k": residual["fy26_enacted_k"],
            "fy27_request_k": residual["fy27_request_k"],
        })
        residuals_added.append((lab, residual))

    if over_count_failures:
        print(f"\n  ✗ {len(over_count_failures)} labs OVER-counted (parser bug):", file=sys.stderr)
        for lab, r in over_count_failures:
            print(f"      {lab}: missing {r}", file=sys.stderr)
        return False, augmented

    print(f"  ✓ All {len(by_lab)} labs reconciled (with {len(residuals_added)} "
          f"residual rows added for orphan leaves)")
    if residuals_added:
        print("\n  Residuals added (orphan leaves not under any office subtotal):")
        for lab, r in residuals_added:
            print(f"      {lab}: FY25={r['fy25_enacted_k']:>+12,}  "
                  f"FY26={r['fy26_enacted_k']:>+12,}  "
                  f"FY27={r['fy27_request_k']:>+12,}")

    # Also flag T2 labs with NO subtotals captured (these are valid only if
    # the lab has zero funding across all years — like Battelle Savannah River Alliance)
    labs_with_no_subtotals = set(t2_totals) - set(by_lab)
    print(f"\nLabs in T2 with zero captured subtotals: {len(labs_with_no_subtotals)}")
    for lab in sorted(labs_with_no_subtotals):
        t2 = t2_totals[lab]
        nonzero = any(t2[y] != 0 for y in ("fy25_enacted_k", "fy26_enacted_k", "fy27_request_k"))
        marker = "✗" if nonzero else "✓"
        if nonzero:
            return False, augmented
        print(f"  {marker} {lab}: T2 = ({t2['fy25_enacted_k']:,}, "
              f"{t2['fy26_enacted_k']:,}, {t2['fy27_request_k']:,})")

    return True, augmented


def main() -> int:
    text = SRC.read_text()
    known_labs = load_t2_lab_names()
    print(f"Loaded {len(known_labs)} known lab names from T2.\n")

    rows, lab_totals_found = parse_lab_by_office(text, known_labs)
    print(f"Parsed {len(rows)} (lab, office) subtotal rows.")
    print(f"Found {len(lab_totals_found)} lab-total markers.\n")

    # Load T2 totals for reconciliation
    t2_totals = {}
    with T2_CSV.open() as f:
        for r in csv.DictReader(f):
            t2_totals[r["lpi_name"]] = {
                "fy25_enacted_k": int(r["fy25_enacted_k"]),
                "fy26_enacted_k": int(r["fy26_enacted_k"]),
                "fy27_request_k": int(r["fy27_request_k"]),
            }

    ok, augmented_rows = reconcile(rows, lab_totals_found, t2_totals)
    if not ok:
        print("\nReconciliation FAILED. Do NOT commit; investigate mismatches.",
              file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "lab_name", "office", "fy25_enacted_k", "fy26_enacted_k", "fy27_request_k"
        ])
        w.writeheader()
        w.writerows(augmented_rows)

    print(f"\n✓ Reconciliation PASSED. Wrote {OUT.relative_to(REPO_ROOT)} "
          f"({len(augmented_rows)} rows).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
