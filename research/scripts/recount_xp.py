"""Recount the SoD XP economy under CORRECTED engine units (2026-07-13).

Engine rules (user-verified in-game 2026-07-12):
  - Kill XP (CRE 0x14): divided among living party members  -> /6 per char
  - AddexperienceParty(X): divided among living party members -> X/6 per char
    (research/03 originally counted these as X per char - 6x overstated)
  - AddXPObject(PlayerN,X): full X to that one character; SoD loops Player1-6
    with the same X -> X per char (count the Player1 line only)

Layers swept:
  1. Script layer: research/data/sod_baf/*.baf (1232 decompiled SoD scripts)
  2. Dialog layer: override BD*.dlg compiled files (action text is stored
     verbatim in DLG). Reply-branch duplication is collapsed with the same
     heuristic research/03 used: identical award value inside one dlg = ONE
     award per run (verified pattern: BDISABEL.dlg carries 12 copies of the
     same AddexperienceParty(9000)).
  3. Placed-kill layer: every BD####.are in override - our components only
     zero appearance schedules, so the vanilla actor tables are intact and
     the sweep reads vanilla placement even on the modded install. EA==255
     hostiles only; scripted spawns are NOT counted (flagged as underestimate).

Output: whole-game per-character completionist totals + the remix delta.
Chapter attribution is future work (this answers the endpoint question).
"""
import struct, glob, os, re, collections

GAME = r"C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install"
OVR = os.path.join(GAME, "override")
BAF = r"C:\src\private\chriz-sod-rebalance\research\data\sod_baf"

files = {os.path.basename(p).lower(): p for p in glob.glob(os.path.join(OVR, '*'))}

# ---- 1. script layer ----
scr_aep = 0      # AddexperienceParty raw sum (party currency), branch-collapsed per script
scr_obj = 0      # AddXPObject per-char sum (Player1 lines only)
scr_detail = []
for p in glob.glob(os.path.join(BAF, '*.baf')):
    name = os.path.basename(p)
    if name.upper() == 'CUTSKIP.BAF':
        continue  # the skip rig mirrors awards that the mirrored scenes also grant
    t = open(p, encoding='latin1').read()
    aep = [int(x) for x in re.findall(r'AddexperienceParty\((\d+)\)', t)]
    obj = [int(x) for x in re.findall(r'AddXPObject\(Player1,(\d+)\)', t)]
    if aep:
        vals = collections.Counter(aep)
        s = sum(v for v in vals)          # one per distinct value per script
        scr_aep += s
        scr_detail.append((name, 'AEP', dict(vals), s))
    if obj:
        vals = collections.Counter(obj)
        s = sum(v for v in vals)
        scr_obj += s
        scr_detail.append((name, 'OBJ', dict(vals), s))

# ---- 2. dialog layer ----
dlg_aep = 0
dlg_obj = 0
dlg_detail = []
for fn, p in sorted(files.items()):
    if not (fn.startswith('bd') and fn.endswith('.dlg')):
        continue
    t = open(p, 'rb').read().decode('latin1', 'replace')
    aep = [int(x) for x in re.findall(r'AddexperienceParty\((\d+)\)', t)]
    obj = [int(x) for x in re.findall(r'AddXPObject\(Player1,(\d+)\)', t)]
    if aep:
        vals = collections.Counter(aep)
        s = sum(v for v in vals)
        dlg_aep += s
        dlg_detail.append((fn, 'AEP', dict(vals), s))
    if obj:
        vals = collections.Counter(obj)
        s = sum(v for v in vals)
        dlg_obj += s
        dlg_detail.append((fn, 'OBJ', dict(vals), s))

# ---- 3. placed-kill layer ----
xpcache = {}
def killxp(cre):
    if cre not in xpcache:
        p = files.get(cre.lower() + '.cre')
        if not p:
            xpcache[cre] = (0, 0)
        else:
            d = open(p, 'rb').read()
            xpcache[cre] = (struct.unpack_from('<I', d, 0x14)[0], d[0x270])
    return xpcache[cre]

kill_total = 0
area_rows = []
for fn, p in sorted(files.items()):
    if not re.fullmatch(r'bd\d{4}[a-z]?\.are', fn):
        continue
    b = open(p, 'rb').read()
    off = struct.unpack_from('<I', b, 0x54)[0]
    cnt = struct.unpack_from('<H', b, 0x58)[0]
    tot = 0
    for i in range(cnt):
        base = off + i * 0x110
        cre = b[base+0x80:base+0x88].split(b'\x00')[0].decode('latin1').strip()
        if not cre:
            continue
        xp, ea = killxp(cre)
        if ea == 255:
            tot += xp
    if tot:
        kill_total += tot
        area_rows.append((fn, tot))

# ---- report ----
per_char = scr_obj + dlg_obj + (scr_aep + dlg_aep + kill_total) / 6.0
print("=== SoD XP economy, corrected units (completionist ceiling) ===")
print(f"script AddXPObject (per char):        {scr_obj:>10,}")
print(f"dialog AddXPObject (per char):        {dlg_obj:>10,}")
print(f"script AddexperienceParty (party):    {scr_aep:>10,}  -> /6 = {scr_aep/6:>9,.0f}")
print(f"dialog AddexperienceParty (party):    {dlg_aep:>10,}  -> /6 = {dlg_aep/6:>9,.0f}")
print(f"placed hostile kill XP (party):       {kill_total:>10,}  -> /6 = {kill_total/6:>9,.0f}")
print(f"TOTAL per character (party of 6):     {per_char:>10,.0f}")
print()
print("top dialog awards (party currency):")
for fn, kind, vals, s in sorted(dlg_detail, key=lambda r: -r[3])[:12]:
    print(f"  {fn:14s} {kind} {vals}")
print()
print("top script awards:")
for fn, kind, vals, s in sorted(scr_detail, key=lambda r: -r[3])[:12]:
    print(f"  {fn:14s} {kind} {vals}")
print()
print("top placed-kill areas (party):")
for fn, tot in sorted(area_rows, key=lambda r: -r[1])[:15]:
    print(f"  {fn:12s} {tot:>8,}")
