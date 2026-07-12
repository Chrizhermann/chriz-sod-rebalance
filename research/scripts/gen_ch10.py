"""Generate comp260_lists.tpa + comp270_lists.tpa (coalition-camp quick-win pass).

Design: docs/design/chapters/04-coalition.md "Quick-win pass" (user-approved
2026-07-12: "we go with your suggestions and we brainstorm on them later").
Cut selection by verified actor index (scratchpad ch10_dump.txt, 2026-07-11),
emitted as CRE@X@Y keys like gen_ch9.

  comp260 (the scouting maps + the shadow vault):
    BD7300 Dead Man's Pass (119): beetles x23, boars x7, displacers x19,
      hobgoblin camp x10, both orog warbands x21 (+4 worgs), dire wolves x11,
      the NW ogre camp x12, giant spiders x2, phase spiders 7->4, hill
      giants 10->3 (SE camp gone, NW camp keeps leader + 3). KEEPS: the
      nymph pocket (nymph/hamadryad/2 treants/2 shamblers + the dead-orog
      field it explains), both ettins, gargantuan/sword spider elites,
      the hostile cave bears, every neutral (Raeanne/earth elemental,
      Gnaler/Kambaldur, Horst/Stalia/Nuber, fauna).
    BD7400 Bloodbark Grove (21): beetles x13, bone bats x2 (banned),
      shadowed soul x1 (banned), burning skeletons 9->4. KEEPS: the
      greater basilisk, dark treants + shambler, the SE wight/ghast
      night pocket, skeletal mage.
    BD7310 shadow vault (1): the Unsleeping Guardian (banned list);
      shadows/greater shadows/wraiths stay as the vault fight.
    BD5000 Underground River (32): displacer pack x6, huge spiders x3,
      greater wyverns 4->1, the orc camp x20. KEEPS: wyvern mama+baby,
      gargantuan+sword spiders, hostile cave bear, ALL neutrals (the
      crusader camp, Murs' ogre family, Rigah/Julann, fauna).
    BD5100 river caves (10): the B/C corrupted-grove pockets thinned -
      dark treants 7->3, shamblers 3->1, gargantuan spiders 5->2, umber
      hulks 3->2. KEEPS: pocket A intact (the corrupted grove), all
      corrupted nymphs/hamadryads, the whole myconid colony, ettin
      ghost, ankheg, every neutral (drow, crusaders, ghost story cast).
  comp270 (Kanaglym):
    BD5300 (11): shadowed souls x3 (banned), skeleton archers 9->3,
      armored 3->2, bladed 2->1. KEEPS: the skeleton-warrior mini-boss,
      tattered skeleton, the ENTIRE south quest cluster (dark magicians/
      Kherriun are neutral-until-quest = untouched by construction),
      Zhadro/Endless ghosts, C0MNEV01 (mod-added, never touch).

ARE SOURCE: WeiDU backups of the component (pre-patch pristine files) when
present, else override (valid only while 260/270 are NOT installed).
"""
import struct, os, glob

GAME = r"C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install"
OVR = os.path.join(GAME, "override")
BAKROOT = os.path.join(GAME, r"weidu_external\backup\chriz-sod-remix")
OUT260 = r"C:\src\private\chriz-sod-rebalance\chriz-sod-remix\lib\comp260_lists.tpa"
OUT270 = r"C:\src\private\chriz-sod-rebalance\chriz-sod-remix\lib\comp270_lists.tpa"

def cstr(b):
    z = b.find(b'\x00')
    if z >= 0: b = b[:z]
    return b.decode('latin1', 'replace').strip()

def load(area, comp):
    bak = os.path.join(BAKROOT, str(comp), area + '.are')
    if os.path.isfile(bak):
        print(f"  {area}: using pre-{comp} backup ARE")
        return open(bak, 'rb').read()
    for p in glob.glob(os.path.join(OVR, '*')):
        if os.path.basename(p).lower() == (area + '.are').lower():
            print(f"  {area}: WARNING - no {comp} backup found, using override "
                  f"(only valid if {comp} is NOT installed)")
            return open(p, 'rb').read()
    raise SystemExit(f"{area} not found")

def actors(b):
    off = struct.unpack_from('<I', b, 0x54)[0]
    cnt = struct.unpack_from('<H', b, 0x58)[0]
    out = {}
    for i in range(cnt):
        base = off + i * 0x110
        out[i] = dict(name=cstr(b[base:base+32]),
                      x=struct.unpack_from('<h', b, base+0x20)[0],
                      y=struct.unpack_from('<h', b, base+0x22)[0],
                      cre=cstr(b[base+0x80:base+0x88]).upper())
    return out

xpcache = {}
def killxp(cre):
    if cre not in xpcache:
        for p in glob.glob(os.path.join(OVR, '*')):
            if os.path.basename(p).lower() == cre.lower() + '.cre':
                d = open(p, 'rb').read()
                xpcache[cre] = (struct.unpack_from('<I', d, 0x14)[0], d[0x270])
                break
        else:
            raise SystemExit(f"CRE {cre} not in override")
    return xpcache[cre]

# ---- cut selections (verified actor indices, ch10_dump.txt 2026-07-11) ----
CUTS = {
    # comp260
    'bd7300': ({56,138,139,140,141,161,163,182,183,                       # boring beetles
                54,55,135,136,137,142,143,159,160,162,164,179,180,181,    # bombardier beetles
                167,168,169,170,171,172,173,                              # wild boars
                116,117,118,119,121,122,123,124,                          # displacers S pack
                126,127,128,129,130,131,132,133,134,                      # displacers N ridge
                120,125,                                                  # pack lords
                57,58,59,60,61,62,112,113,114,115,                        # hobgoblin camp
                32,33,34,35,38,39,49,108,109,110,111,                     # orog warband NE
                40,41,42,43,48,103,104,105,106,107,                       # orog warband SW
                36,37,44,45,                                              # worgs
                4,5,64,65,150,151,152,153,154,155,156,                    # dire wolves
                87,88,89,90,91,187,188,189,190,191,192,193,               # ogre camp NW
                174,175,                                                  # giant spiders
                66,176,177,                                               # phase spiders 7->4
                147,148,6,7,8,144,145}, 255),                             # hill giants 10->3
    'bd7400': ({14,15,25,45,                                              # boring beetles
                12,13,33,34,35,43,44,53,54,                               # bombardier beetles
                47,48,                                                    # bone bats (banned)
                52,                                                       # shadowed soul (banned)
                7,9,40,41,42}, 255),                                      # burning skeletons 9->4
    'bd7310': ({0}, 255),                                                 # Unsleeping Guardian
    'bd5000': ({66,67,68,69,70,71,                                        # displacer pack
                82,83,86,                                                 # huge spiders
                41,44,45,                                                 # greater wyverns 4->1
                46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65}, 255),  # orc camp
    'bd5100': ({75,76,85,89,                                              # dark treants 7->3
                86,91,                                                    # shamblers 3->1
                88,90,104,                                                # gargantuan spiders 5->2
                94}, 255),                                                # umber hulks 3->2
    # comp270
    'bd5300': ({20,29,30,                                                 # shadowed souls (banned)
                21,22,28,32,33,34,                                        # skeleton archers 9->3
                17,                                                       # armored skeleton 3->2
                27}, 255),                                                # bladed skeleton 2->1
}

def emit(outpath, comp, areas):
    lines = [f"// GENERATED by research/scripts/gen_ch10.py (2026-07-12) from the",
             f"// pre-{comp} pristine AREs. Keys are CRE@X@Y of vanilla placed actors;",
             "// regenerate rather than hand-edit.", ""]
    total_cut = 0
    for area in areas:
        idxs, want_ea = CUTS[area]
        b = load(area, comp)
        acts = actors(b)
        missing = idxs - set(acts)
        if missing:
            raise SystemExit(f"{area}: cut indices not present: {missing}")
        keys = set()
        cutxp = 0
        lines.append(f"// ---- {area}: {len(idxs)} cuts ----")
        for i in sorted(idxs):
            a = acts[i]
            xp, ea = killxp(a['cre'])
            if ea != want_ea:
                raise SystemExit(f"{area} idx{i} {a['cre']}: EA={ea}, expected {want_ea}")
            key = f'{a["cre"]}@{a["x"]}@{a["y"]}'
            if key in keys:
                raise SystemExit(f"{area} idx{i}: duplicate key {key} - "
                                 "coordinate matching would double-count")
            keys.add(key)
            cutxp += xp
            lines.append(f'OUTER_SPRINT $csr_cut_{area}(~{key}~) ~1~'
                         f'   // idx{i} {a["name"]} ({xp} xp)')
        lines.append(f"OUTER_SET csr_cutn_{area} = {len(idxs)}")
        lines.append(f"// {area} cut kill-XP: {cutxp}")
        lines.append("")
        total_cut += cutxp
        print(f"  {area}: {len(idxs)} cuts, {cutxp} xp")
    chunk = int(round(total_cut * 0.8 / 6.0 / 100.0)) * 100
    lines.append(f"// XP ledger: cut kill-XP {total_cut}.")
    lines.append("// Compensation = cut * 0.8 / 6 (party-of-6 ledger baseline,")
    lines.append(f"// AddexperienceParty grants per member) rounded to 100 -> {chunk}/char.")
    lines.append(f"OUTER_SET csr_xp_chunk_{comp} = {chunk}")
    lines.append("")
    open(outpath, 'w', newline='\n').write('\n'.join(lines))
    print(f"  -> chunk_{comp} = {chunk}  ({outpath})")

print("comp260:")
emit(OUT260, 260, ('bd7300', 'bd7400', 'bd7310', 'bd5000', 'bd5100'))

print("comp270:")
emit(OUT270, 270, ('bd5300',))
