"""Wave-1 rest-ambush 5x reduction table.

Policy (user-decided 2026-07-03): reduce the FELT per-8h-rest interrupt chance ~5x.
felt(c) = 1 - (1 - c/100)^8  (engine rolls per in-game hour; see research/01).
new_c = invert(felt_old / 5), rounded to nearest int, floor 1 (0 stays 0).

Excluded: BDNOREST pseudo-tables (day/night=100 'cannot rest here' cancellers),
inactive headers, empty tables. Zero-ambush area list is decided per-chapter, NOT here.
"""
import csv, math, pathlib

SRC = pathlib.Path(__file__).resolve().parents[2] / "docs" / "research" / "sod_areas_dataset.csv"

def felt(c: float) -> float:
    return (1 - (1 - c / 100) ** 8) * 100

def invert(f: float) -> float:
    return (1 - (1 - f / 100) ** (1 / 8)) * 100

def reduce5(c: int) -> int:
    if c <= 0:
        return 0
    return max(1, round(invert(felt(c) / 5)))

rows = []
with open(SRC, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        if r["rest_active"] != "1" or int(r["table_count"] or 0) == 0:
            continue
        if r["rest_table"].strip() == "BDNOREST":
            continue
        day, night = int(r["day"]), int(r["night"])
        if day == 0 and night == 0:
            continue
        nd, nn = reduce5(day), reduce5(night)
        rows.append((r["area"], r["name"] or "?", day, night, felt(day), felt(night),
                     nd, nn, felt(nd), felt(nn), r["max_spawn"], r["difficulty"],
                     r["rest_table"]))

rows.sort(key=lambda x: -max(x[4], x[5]))
print(f"{len(rows)} areas with an active non-BDNOREST rest table\n")
print("| Area | Name | day/night now | felt now | day/night NEW | felt NEW | max | diff | table |")
print("|---|---|---|---|---|---|---|---|---|")
for a in rows:
    print(f"| {a[0]} | {a[1]} | {a[2]}/{a[3]} | {a[4]:.0f}%/{a[5]:.0f}% | "
          f"**{a[6]}/{a[7]}** | {a[8]:.0f}%/{a[9]:.0f}% | {a[10]} | {a[11]} | {a[12][:44]} |")
