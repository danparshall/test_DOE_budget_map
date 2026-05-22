"""
Parse the FY 2027 Laboratory Tables into a per-lab Science sub-program matrix
(T5a, the lab-axis side of the Science Volume Drill).

Source: papers/text/doe_fy27LaboratoryTables_2026.txt
Output: data/fy27_science_by_lab_subprogram.csv

For each Science-funded lab (as identified by T3 having a row with office='Science'),
emit one output row per (lab_name, science_subprogram) capturing FY25/26/27 dollars.
The 12 canonical Science sub-programs are listed in SCIENCE_SUBPROGRAMS below.

Reconciliation (the embedded behavior test, fail-loud):
  (a) For every Science-funded lab, sum of T5a sub-program rows for that lab
      must equal T3's Science total for that lab, in all three years.
  (b) Global sum of T5a must equal T3's Science grand total ($8.40B FY26, etc).
If either fails, the CSV is NOT written.

Sub-program structure in the source PDF:
  Each lab's per-office section lists leaves (prefixed "Research - <X>" or
  "Construction - <X>") followed by a sub-program rollup row whose label is
  the canonical sub-program name. We capture the rollup rows. A few sub-programs
  appear as single leaves without a separate rollup wrapper:
  - Safeguards and Security - SC
  - Program Direction - SC
  - Workforce Development for Teachers & Scientists  (sometimes wrapped, sometimes leaf-only)
  These match the same regex (canonical name + 3 numbers) so they're captured
  uniformly.

Schema:
  - lab_name (str): matches T3's lab_name
  - science_subprogram (str): one of SCIENCE_SUBPROGRAMS
  - fy25_enacted_k (int): FY 2025 enacted, $ in thousands
  - fy26_enacted_k (int): FY 2026 enacted, $ in thousands
  - fy27_request_k (int): FY 2027 President's Budget request, $ in thousands
"""
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path("/home/claude/repo_local")
SRC = REPO_ROOT / "papers/text/doe_fy27LaboratoryTables_2026.txt"
T3_CSV = REPO_ROOT / "data/fy27_lab_by_office.csv"
T2_CSV = REPO_ROOT / "data/fy27_lab_summary.csv"
OUT = REPO_ROOT / "data/fy27_science_by_lab_subprogram.csv"

# Canonical Science sub-program rollup names. Order matches DOE's typical listing.
# Each appears in the source as a rollup row label followed by 3 dollar values.
# (Some appear as single-leaf rows without a separate rollup; the same regex matches.)
SCIENCE_SUBPROGRAMS = [
    "Advanced Scientific Computing Research",
    "Basic Energy Sciences",
    "Biological and Environmental Research",
    "Fusion Energy Sciences",
    "High Energy Physics",
    "Nuclear Physics",
    "Isotope R&D and Production",
    "Accelerator R&D and Production",
    "Workforce Development for Teachers & Scientists",
    "Science Laboratories Infrastructure",
    "Safeguards and Security - SC",
    "Program Direction - SC",
]

NUM = r"-?\d[\d,]*"
# For each canonical sub-program name, anchored to start-of-line (allowing
# leading whitespace), followed by 2+ spaces, then three numbers.
# Using re.escape because some names contain "&" and "-".
SUBPROGRAM_RES = [
    (name, re.compile(rf"^\s*{re.escape(name)}\s{{2,}}(?P<a>{NUM})\s+(?P<b>{NUM})\s+(?P<c>{NUM})\s*$"))
    for name in SCIENCE_SUBPROGRAMS
]

# Lab-end marker, same pattern as build_fy27_lab_by_office.py
TOTAL_LAB_RE = re.compile(
    rf"^Total\s+(?P<lab>.+?)\s{{2,}}(?P<a>{NUM})\s+(?P<b>{NUM})\s+(?P<c>{NUM})\s*$"
)


def parse_int(s: str) -> int:
    return int(s.replace(",", ""))


def load_t2_lab_names() -> set[str]:
    with T2_CSV.open() as f:
        return {r["lpi_name"] for r in csv.DictReader(f)}


def load_t3_science_totals() -> dict[str, dict[str, int]]:
    """Load T3 Science-only rows: lab_name -> {fy25_enacted_k, fy26_enacted_k, fy27_request_k}."""
    totals = {}
    with T3_CSV.open() as f:
        for r in csv.DictReader(f):
            if r["office"] == "Science":
                totals[r["lab_name"]] = {
                    "fy25_enacted_k": int(r["fy25_enacted_k"]),
                    "fy26_enacted_k": int(r["fy26_enacted_k"]),
                    "fy27_request_k": int(r["fy27_request_k"]),
                }
    return totals


def parse_subprograms(text: str, known_labs: set[str]) -> list[dict]:
    """
    Walk text line by line. Track current lab (via Total <lab> markers).
    Capture every Science sub-program rollup match; attribute to the lab
    in whose section it appears.

    Returns list of dicts: lab_name, science_subprogram, fy25/26/27_enacted_k.
    """
    rows = []
    pending = []  # rows captured but not yet attributed to a lab
    for line in text.splitlines():
        # Try sub-program matches first (more specific than Total <lab>)
        matched = False
        for name, regex in SUBPROGRAM_RES:
            m = regex.match(line)
            if m:
                pending.append({
                    "science_subprogram": name,
                    "fy25_enacted_k": parse_int(m["a"]),
                    "fy26_enacted_k": parse_int(m["b"]),
                    "fy27_request_k": parse_int(m["c"]),
                })
                matched = True
                break
        if matched:
            continue

        # Check lab-end marker
        m = TOTAL_LAB_RE.match(line)
        if m:
            lab = m["lab"].strip()
            if lab not in known_labs:
                # False positives like "Total, Stockpile Modernization" — those
                # have a comma after Total and don't match TOTAL_LAB_RE anyway,
                # but defense in depth.
                continue
            for p in pending:
                rows.append({"lab_name": lab, **p})
            pending = []

    # Any leftover pending rows mean we never hit a matching Total <lab>; report.
    if pending:
        print(f"WARNING: {len(pending)} sub-program rows captured but never attributed "
              f"to a lab (orphan tail).", file=sys.stderr)
        for p in pending[:5]:
            print(f"   {p}", file=sys.stderr)
    return rows


def reconcile(rows: list[dict], t3_science: dict[str, dict[str, int]]) -> bool:
    """Per-lab and global reconciliation vs T3 Science totals."""
    by_lab = {}
    for r in rows:
        by_lab.setdefault(r["lab_name"], []).append(r)

    print(f"Reconciling {len(by_lab)} labs with sub-program rows "
          f"against T3 Science totals ({len(t3_science)} labs)...\n")

    failures = []
    for lab in sorted(t3_science):
        captured = by_lab.get(lab, [])
        t3 = t3_science[lab]
        for yr in ("fy25_enacted_k", "fy26_enacted_k", "fy27_request_k"):
            our_sum = sum(r[yr] for r in captured)
            if our_sum != t3[yr]:
                failures.append((lab, yr, our_sum, t3[yr], our_sum - t3[yr]))

    # Labs we captured rows for that aren't in T3 Science (shouldn't happen)
    extra_labs = set(by_lab) - set(t3_science)
    for lab in sorted(extra_labs):
        for yr in ("fy25_enacted_k", "fy26_enacted_k", "fy27_request_k"):
            our_sum = sum(r[yr] for r in by_lab[lab])
            if our_sum != 0:
                failures.append((lab, yr, our_sum, 0, our_sum))

    if failures:
        print(f"  ✗ {len(failures)} per-lab/year mismatches:", file=sys.stderr)
        for lab, yr, got, expected, delta in failures[:50]:
            print(f"      {lab:<55} {yr:<18} got={got:>13,}  expected={expected:>13,}  Δ={delta:>+13,}",
                  file=sys.stderr)
        if len(failures) > 50:
            print(f"      ... and {len(failures) - 50} more", file=sys.stderr)
        return False
    print(f"  ✓ All {len(t3_science)} labs reconciled against T3 Science totals (all 3 years).")

    # Global recon
    for yr in ("fy25_enacted_k", "fy26_enacted_k", "fy27_request_k"):
        our_global = sum(r[yr] for r in rows)
        t3_global = sum(t3[yr] for t3 in t3_science.values())
        if our_global != t3_global:
            print(f"  ✗ Global mismatch for {yr}: our={our_global:,}  T3={t3_global:,}",
                  file=sys.stderr)
            return False
        print(f"  ✓ Global {yr}: {our_global:,} (matches T3 Science total)")

    return True


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: source file not found: {SRC}", file=sys.stderr)
        return 1

    text = SRC.read_text()
    known_labs = load_t2_lab_names()
    t3_science = load_t3_science_totals()
    print(f"Loaded {len(known_labs)} known lab names from T2.")
    print(f"Loaded {len(t3_science)} Science-funded labs from T3.\n")

    rows = parse_subprograms(text, known_labs)
    print(f"Parsed {len(rows)} (lab, sub-program) rows.\n")

    if not reconcile(rows, t3_science):
        print("\nReconciliation FAILED. CSV NOT written. Investigate mismatches above.",
              file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "lab_name", "science_subprogram",
            "fy25_enacted_k", "fy26_enacted_k", "fy27_request_k",
        ])
        w.writeheader()
        w.writerows(rows)

    print(f"\n✓ Reconciliation PASSED. Wrote {OUT.relative_to(REPO_ROOT)} ({len(rows)} rows).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
