"""
Parse the Laboratory Table Summary Report (pp. 1-3 of doc #3) into a CSV.

Source: papers/text/doe_fy27LaboratoryTables_2026.txt
Output: data/fy27_lab_summary.csv

Schema:
  - lpi_name (str): Laboratory, Plant, or Installation name as printed
  - fy25_enacted_k (int): FY 2025 enacted, $ in thousands
  - fy26_enacted_k (int): FY 2026 enacted, $ in thousands
  - fy27_request_k (int): FY 2027 President's Budget request, $ in thousands

Reconciliation: sum of all LPI rows must equal the document's printed total
  ($53,019,764 / $53,821,313 / $61,901,062 in $k for FY25 / FY26 / FY27).

Caveats documented:
  - Numbers are GROSS budget authority (include discretionary + supplemental,
    exclude offsets / receipts / rescissions). Per the document's own note.
  - Lab totals do NOT reconcile to the BiB topline ($53.91B FY27 net
    discretionary) — there's a ~$8B gap which is the supplements + offsets
    + rescissions delta. See data/README.md.
"""
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path("/home/claude/repo_local")
SRC = REPO_ROOT / "papers/text/doe_fy27LaboratoryTables_2026.txt"
OUT = REPO_ROOT / "data/fy27_lab_summary.csv"

# Expected reconciliation targets (read off the printed "Total by Lab..." line)
EXPECTED_TOTALS = {
    "fy25": 53_019_764,
    "fy26": 53_821_313,
    "fy27": 61_901_062,
}

# Pattern: <name (anything non-numeric at end)> <num> <num> <num>
# Numbers are comma-grouped thousands, possibly with leading spaces.
NUM = r"[\d,]+"
ROW_RE = re.compile(rf"^\s*(?P<name>.+?)\s{{2,}}(?P<a>{NUM})\s{{2,}}(?P<b>{NUM})\s{{2,}}(?P<c>{NUM})\s*$")

# Sentinels to ignore (page headers, the document header, etc.)
SKIP_PHRASES = {
    "DEPARTMENT OF ENERGY",
    "Laboratory Table Summary Report",
    "FY 2027",
    "(Dollars in Thousands)",
    "DOE Laboratory Tables",
    "FY 2027 Congressional Justification",
}
TOTAL_LINE_PREFIX = "Total by Lab, Plant, and Installation"


def parse_lab_summary(text: str) -> tuple[list[dict], dict]:
    """Return (rows, totals) where totals is a dict of the printed Total row."""
    rows = []
    totals = None
    in_summary = False

    for line in text.splitlines():
        line_stripped = line.strip()

        # Bounds of the summary section
        if "Laboratory Table Summary Report" in line:
            in_summary = True
            continue
        if line_stripped.startswith(TOTAL_LINE_PREFIX):
            m = ROW_RE.match(line)
            if m:
                totals = {
                    "fy25": int(m["a"].replace(",", "")),
                    "fy26": int(m["b"].replace(",", "")),
                    "fy27": int(m["c"].replace(",", "")),
                }
            in_summary = False
            continue

        if not in_summary:
            continue

        # Skip page-furniture lines and blanks
        if not line_stripped:
            continue
        if any(phrase in line_stripped for phrase in SKIP_PHRASES):
            continue
        if line_stripped in {"FY 2025", "FY 2026", "FY 2027",
                              "Enacted", "President's Budget"}:
            continue

        m = ROW_RE.match(line)
        if not m:
            # Helpful for debugging: print non-matching lines we DIDN'T skip
            # (commented out unless needed)
            # print(f"  non-matching: {line!r}", file=sys.stderr)
            continue

        name = m["name"].strip()
        # Header rows like "FY 2025 / FY 2026 / FY 2027" sometimes survive
        # with leftover words. Filter by checking the name isn't a pure
        # year label or the page footer.
        if name in SKIP_PHRASES or name.startswith("DOE Laboratory Tables"):
            continue

        rows.append({
            "lpi_name": name,
            "fy25_enacted_k": int(m["a"].replace(",", "")),
            "fy26_enacted_k": int(m["b"].replace(",", "")),
            "fy27_request_k": int(m["c"].replace(",", "")),
        })

    return rows, totals


def main() -> int:
    text = SRC.read_text()
    rows, totals = parse_lab_summary(text)

    if totals is None:
        print("ERROR: did not find 'Total by Lab, Plant, and Installation' row",
              file=sys.stderr)
        return 1

    # Reconcile sums against printed total
    sums = {
        "fy25": sum(r["fy25_enacted_k"] for r in rows),
        "fy26": sum(r["fy26_enacted_k"] for r in rows),
        "fy27": sum(r["fy27_request_k"] for r in rows),
    }

    print(f"Parsed {len(rows)} LPI rows.")
    print(f"  Sum FY25 {sums['fy25']:>12,} vs printed total {totals['fy25']:>12,} "
          f"(expected {EXPECTED_TOTALS['fy25']:>12,})")
    print(f"  Sum FY26 {sums['fy26']:>12,} vs printed total {totals['fy26']:>12,} "
          f"(expected {EXPECTED_TOTALS['fy26']:>12,})")
    print(f"  Sum FY27 {sums['fy27']:>12,} vs printed total {totals['fy27']:>12,} "
          f"(expected {EXPECTED_TOTALS['fy27']:>12,})")

    ok = True
    for yr in ("fy25", "fy26", "fy27"):
        if sums[yr] != totals[yr]:
            print(f"  ✗ {yr}: sum of rows != printed total "
                  f"(diff {sums[yr] - totals[yr]:+,})", file=sys.stderr)
            ok = False
        if totals[yr] != EXPECTED_TOTALS[yr]:
            print(f"  ✗ {yr}: printed total != expected total "
                  f"(diff {totals[yr] - EXPECTED_TOTALS[yr]:+,})", file=sys.stderr)
            ok = False

    if not ok:
        print("Reconciliation failed. Inspect rows above; do NOT commit.",
              file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "lpi_name", "fy25_enacted_k", "fy26_enacted_k", "fy27_request_k"
        ])
        w.writeheader()
        w.writerows(rows)

    print(f"\n✓ Reconciliation passed. Wrote {OUT.relative_to(REPO_ROOT)} "
          f"({len(rows)} rows).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
