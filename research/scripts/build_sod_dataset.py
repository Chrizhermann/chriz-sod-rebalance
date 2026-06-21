"""
Build the master SoD encounter dataset.
For every SoD (BD####) area:
  - rest-header fields (enabled, day%, night%, max creatures, difficulty, table)
  - scripted CreateCreature spawns from the decompiled area script
Outputs CSV + a markdown table to docs/research/.

Run from anywhere; paths are absolute.
NOTE: rest day/night % is rolled PER IN-GAME HOUR by the Beamdog engine,
so felt chance per 8h rest = 1-(1-c/100)**8. See docs/research/01-*.
"""
import struct, os, re, glob, csv, math
from collections import Counter

GAME = r"C:\Games\Baldur's Gate II Enhanced Edition modded"
OVR  = os.path.join(GAME, "override")
BAF  = r"C:\src\private\chriz-sod-rebalance\research\data\sod_baf"
OUT  = r"C:\src\private\chriz-sod-rebalance\docs\research"

# friendly names from EET table
names = {}
tbl = os.path.join(GAME, "EET", "tbl", "map_eet_areas.tbl")
for line in open(tbl, encoding="ascii", errors="replace"):
    m = re.match(r"\s*(BD\w+)\b.*?//\s*\[?([^\]]*?)\]?\s*$", line)
    if m:
        names[m.group(1).upper()] = m.group(2).strip()

def rest(path):
    d = open(path, "rb").read()
    if d[0:4] != b"AREA" or len(d) < 0xC4:
        return None
    ro, = struct.unpack_from("<I", d, 0xC0)
    if ro == 0 or ro + 0xAC > len(d):
        return dict(en=0, day=0, ngt=0, mx=0, diff=0, cnt=0, cr=[])
    cr = [d[ro+0x48+k*8:ro+0x48+(k+1)*8].split(b"\x00")[0].decode("ascii","replace") for k in range(10)]
    cr = [c for c in cr if c]
    cnt, = struct.unpack_from("<H", d, ro+0x98)
    diff,= struct.unpack_from("<H", d, ro+0x9a)
    mx,  = struct.unpack_from("<H", d, ro+0xa4)
    en,  = struct.unpack_from("<H", d, ro+0xa6)
    day, = struct.unpack_from("<H", d, ro+0xa8)
    ngt, = struct.unpack_from("<H", d, ro+0xaa)
    return dict(en=en, day=day, ngt=ngt, mx=mx, diff=diff, cnt=cnt, cr=cr)

def scripted_spawns(area):
    p = os.path.join(BAF, area + ".baf")
    if not os.path.exists(p):
        return []
    return re.findall(r'CreateCreature(?:Object[A-Za-z]*)?\("([^"]+)"', open(p, encoding="ascii", errors="replace").read())

def felt(c, hours=8):
    return round((1 - (1 - c/100.0)**hours) * 100)

files = sorted({*glob.glob(os.path.join(OVR,"BD*.are")), *glob.glob(os.path.join(OVR,"BD*.ARE"))},
               key=lambda x: os.path.basename(x).upper())
rows = []
for f in files:
    a = os.path.basename(f).upper().replace(".ARE","")
    r = rest(f)
    if not r:
        continue
    sp = scripted_spawns(a)
    spc = Counter(sp)
    # "active rest ambush" = enabled AND has a creature table (engine skips empty tables)
    active = 1 if (r["en"] and r["cnt"] > 0 and r["mx"] > 0) else 0
    rows.append(dict(
        area=a, name=names.get(a, ""),
        rest_active=active, day=r["day"], night=r["ngt"],
        felt_day=felt(r["day"]) if active else 0,
        felt_night=felt(r["ngt"]) if active else 0,
        max_spawn=r["mx"], difficulty=r["diff"], table_count=r["cnt"],
        rest_table="|".join(r["cr"]),
        scripted_spawn_calls=len(sp),
        scripted_creatures="|".join(f"{k}x{v}" for k,v in spc.most_common(8)),
    ))

os.makedirs(OUT, exist_ok=True)
cols = ["area","name","rest_active","day","night","felt_day","felt_night",
        "max_spawn","difficulty","table_count","rest_table",
        "scripted_spawn_calls","scripted_creatures"]
with open(os.path.join(OUT, "sod_areas_dataset.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow(r)

# summary
active = [r for r in rows if r["rest_active"]]
print(f"areas: {len(rows)}  rest-active(real ambush): {len(active)}")
print(f"CSV -> {os.path.join(OUT,'sod_areas_dataset.csv')}")
print("\nReal rest-ambush areas (felt% per 8h rest), worst first:")
for r in sorted(active, key=lambda x:-x["felt_night"]):
    print(f"  {r['area']:7} {r['name'][:26]:26} day={r['day']:>2}->{r['felt_day']:>2}% night={r['night']:>2}->{r['felt_night']:>2}% max={r['max_spawn']} diff={r['difficulty']:>3} [{r['rest_table'][:34]}]")
