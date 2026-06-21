# 06 — SoD Ambush / Trash Creature Danger Audit

Status: **verified** against the live install's `override\*.CRE` / `*.ITM` / `*.SPL` binaries
(post AK + CDTweaks + SCS — these are the files the player actually fights).
Date: 2026-06-21. Read-only. Scratch: `C:\tmp\sod_research\creatures\` (`parse_cre.py`,
`parse_itm.py`, `cre_dump.txt`).

## Method / offset verification

CRE V1.0 header offsets verified via IESDP. Resistances are **signed bytes** at `0x59`–`0x63`
(fire/cold/elec/acid/magic/magic-fire/magic-cold, then slash/crush/pierce/missile). HP max
`0x26`, natural AC `0x46`, THAC0 `0x52`, APR byte `0x53`, saves `0x54`–`0x58`, class levels
`0x234`–`0x236`, kill-XP `0x14`, General/Race/Class `0x271`/`0x272`/`0x273`.

Embedded CRE effects here are **V2 (264-byte)** blocks (`0x33`=1). The opcode is at block
offset **`0x08`** (NOT 0x00 — verified by hex-dump; the WebFetch/IESDP table was wrong),
param1 `0x14`, param2 `0x18`, timing `0x1c`, duration `0x20`, resource `0x28`. ITM equipped
effects are V1 (48-byte): opcode `0x00`, p1 `0x04`, p2 `0x08`, resource `0x14`; equipped table
via header `0x6a`/`0x6e`/`0x70`.

**Key structural finding:** almost none of the danger lives in the CRE resistance bytes for
most creatures. It lives in three **shared "immunity/regen" items** the CREs carry —
`RING95`, `RING94`, `IMMUNE1`, `TROLLIMM`, `TROLLREG`, `REGHP1` — plus engine UNDEAD/animal
type immunities, plus SCS-added effects. Those are decoded in their own section below.

---

## Master stat / resistance table

Resistances shown only where non-zero. "Phys" = slash/pierce/crush/missile. APR = raw CRE
attack byte (higher = more attacks/round). All listed creatures are `EA=ENEMY` unless noted.

| CRE | Role / lvl | HP | AC | THAC0 | APR | killXP | Elemental resist | Phys resist (S/P/C/M) | Gating item(s) |
|---|---|---|---|---|---|---|---|---|---|
| **BDSKGR00** | skeleton, L1 | 8 | 7 | 19 | 1 | 65 | cold100, elec100, mcold100 | 50/50/**0**/**90** | RING95 |
| **BDSKGR01** | skel warrior F6 | 60 | 3 | 14 | 1 | 750 | cold100, mcold100 | 50/50/0/90 | RING95 |
| **BDSKGR02** | skel warrior F6 | 60 | 6 | 15 | 1 | 400 | cold100, mcold100 | 50/50/0/90 | RING95 |
| **BDSKGR03** | Bane Guard L9 | 90 | 0 | 11 | 3 | 1000 | cold100, mcold100 | 50/50/0/90 | RING95 |
| **BDSKGR04** | skel archer F4 | 40 | 7 | 17 | 1 | 250 | cold100, mcold100 | 50/50/0/90 | RING95 (bow) |
| **BDSKGR05** | **fire** skel F4 | 40 | 5 | 17 | 1 | 300 | **fire100, mfire100** | 50/50/0/90 | RING95 |
| **BDSKGR06** | **fire** archer F4 | 40 | 5 | 17 | 1 | 300 | **fire100, mfire100** | 50/50/0/90 | RING95 (bow) |
| **BDSKGR07** | skeleton **MAGE** L5 | 20 | 7 | 19 | 1 | 900 | cold100, mcold100 | 50/50/0/90 | RING95 + spellbook |
| **BDSKGR08** | boss skel F9 | 90 | 2 | 11 | 1 | 4000 | cold100, mcold100, **magic90** | 50/50/0/90 | RING95 + **IMMUNE1** |
| **BDBONBAT** | bone bat (skel) L5 | 40 | 7 | 15 | 2 | 975 | cold100, mcold100 | 50/50/0/90 | RING95 (flies) |
| BDWOLF | wolf L3 | 24 | 7 | 17 | 1 | 65 | — | — | — |
| BDWOLFDI | dire wolf L5 | 40 | 6 | 15 | 1 | 175 | — | — | — |
| **BDWOLFDR** | dread wolf (undead) L5 | 40 | 6 | 15 | 1 | 420 | cold100, mcold100, elec50 | — | **TROLLIMM** |
| **BDWOLFVA** | vampiric wolf (undead) L6 | 52 | 2 | 13 | 1 | 2000 | — | — | **IMMUNE1** + RING95 |
| **TROLL01** | troll L6 | 54 | 4 | 13 | 3 | 1400 | — | — | **TROLLIMM+TROLLREG** |
| **TROLLSM** | troll (small) L4 | 32 | 6 | 15 | 2 | 750 | — | — | **TROLLIMM+TROLLREG** |
| **TROLFR01** | troll L5 | 45 | 3 | 15 | 3 | 650 | — | — | **TROLLIMM+TROLLREG** |
| **BDTROLL1/2** | troll (scripted, neutral) L8 | 64 | 4 | 12 | 3 | 1400 | — | — | **TROLLIMM+TROLLREG** |
| BDSPIDGI/SPIDGI | giant spider L4-5 | 35-40 | 4 | 13-15 | 1 | 420-450 | — | — | ANTIWEB (poison hit) |
| SPIDHU | huge spider L2 | 18 | 6 | 16 | 1 | 270 | — | — | ANTIWEB |
| **SPIDSW** | sword spider L5 | 45 | 3 | 12 | **4** | 2000 | — | — | ANTIWEB (poison hit) |
| **SPIDPHAS** | phase spider L5 | 84 | 1 | **7** | 2 | 4000 | — | — | teleports; save-spell **2** |
| ZOMBIE / BDSHZOM1 | zombie L2 | 16 | 8 | 18 | 1 | 65 | cold100 | — | RING94 |
| **GHOUL** | ghoul L2 | 16 | 6 | 17 | 3 | 175 | — | — | RING95 (paralyze hit) |
| **GHAST** | ghast L4 | 32 | 4 | 14 | 3 | 650 | — | — | RING95 (paralyze hit) |
| **BDSHSOUL** | shadow (undead) L7 | 56 | 5 | 13 | 1 | 1100 | cold100, mcold100 | — | **IMMUNE1** + RING95 |
| BDBATOUT | bat (neutral) | 8 | 10 | 19 | 1 | 0 | — | — | non-combat |
| **BDIMP** | imp (fiend) L2 | 18 | 2 | 18 | 1 | 1400 | **fire/cold/elec 100, magic25** | — | **IMMUNE1** + ~45 spell-immunities |
| **BDLEMURE** | lemure (fiend) L2 | 16 | 7 | 18 | 1 | 120 | **fire100, cold50** | — | **REGHP1 (+6 HP/round regen)** |
| BDBANDIT / BDBANDAM | human bandit L1 | 10 | 10 | 20 | 1 | 15-65 | — | — | bow+sword |
| BDBUGB01 | bugbear F4 | 40 | 5 | 16 | 1 | 175 | — | — | — |
| BDBUGB10 | bugbear F5 | 50 | 5 | 15 | 1 | 270 | — | — | — |
| BDBUGB20 | bugbear **CLERIC** L6 | 48 | 5 | 16 | 1 | 650 | — | — | casts priest spells |
| BDBOAR02 | boar L3 | 27 | 7 | 17 | 1 | 175 | — | — | — |
| BDBEARBR | brown bear L6 | 48 | 6 | 14 | 3 | 420 | — | — | enrage (SPCL321) |
| BDBEARBL | black bear L3 (neutral) | 27 | 7 | 17 | 3 | 120 | — | — | — |
| **ANKHEG** | ankheg L8 | 64 | 2 | 12 | 2 | 975 | fire25 | — | acid spit (ranged), burrows |
| ORC01_ | orc L3 | 30 | 6 | 18 | 1 | 120 | — | — | halberd |
| HOBGOB | hobgoblin L1 | 8 | 5 | 19 | 1 | 35 | — | — | — |
| **BDMYCRD** | myconid (plant) L5 | 40 | 10 | 15 | 1 | 420 | — | — | confusion spores (BDMYCSP1) |
| **JELLOC** | ochre jelly (slime) L6 | 48 | 4 | 13 | 1 | 270 | cold50, mcold50, magic10 | **/-/-/missile100** | splits (DW#JELOC); acid |
| **JELLYGR** | green slime L2 | 16 | 8 | 17 | 1 | 65 | **elec100** | **/-/-/missile100** | acid/poison |
| **BDGIANHI** | hill giant L12 | 98 | 3 | **8** | 1 | 3000 | — | — | throws rocks (GIANT1/2/3) |
| **BDWYRML1** | wyvern L7 | 56 | **-1** | 13 | 3 | 1400 | cold100, mcold100 | — | poison sting; flies |

(Not present in this install: `BDWOLFWI` winter wolf, `TROLL01.ITM` is a weapon not a CRE,
`SPIDGI` has a 2nd identical-name variant. `BDWOLF02` is a neutral non-combat "hunter" wolf.)

---

## Decoded immunity / regeneration items (the real danger)

### RING95 (76 equip effects) — worn by every catacomb skeleton, ghoul, ghast, shadow, slime, bone bat
A blanket crowd-control immunity package. Confirmed immunities (op101 / op296 / op328):
**charm (5), sleep (39 + 109 unconsciousness), poison (25), confusion (128), berserk/horror
(24 + cdhorror.spl), command/hold-family, feeblemind, plus spell-level protections (spwi604
Power Word: Stun, SpPr704 family).** Net effect: at SoD-prologue level the party's entire
soft-CC kit (Sleep, Command, Horror, Charm, Hold) does **nothing** to these enemies — and
they're already engine-UNDEAD-immune to most of it anyway.

### RING94 (51 equip effects) — zombies
Same idea, zombie flavour: immune to charm/sleep/confusion/horror/poison + SpPr704 (Slay
Living) family. Zombies are pure HP sponges with no answers needed beyond damage.

### IMMUNE1 (3 equip effects) — BDSKGR08, BDWOLFVA, BDSHSOUL, BDIMP
`op120 Immunity-to-Weapons p1=0 p2=2` → **immune to non-magical (enchantment-0) weapons** +
op328 spell-state 178 + op282. This is the classic "needs a +1 weapon to hit." Any party
member still on a mundane weapon **cannot damage** the boss skeleton, vampiric wolf, shadow,
or imp at all.

### TROLLIMM (56 equip effects) — every troll + the dread wolf (BDWOLFDR)
The heaviest disabler-immunity blanket in the set: op101/op296 immunity to **slow (45),
hold/paralyze (109), maze (175?), charm (5), confusion (128), horror (cdhorror), mind-flayer
stun (spflayer), feeblemind (cdfeeble), petrification family (185/210), + spell-turning /
spin853 / spwi413 protections.** Trolls (and dread wolves) shrug off essentially all
control magic.

### TROLLREG + dwtrrg2 (troll regeneration) — THE troll problem
- `TROLLREG.ITM`: `op232 Cast-spell-on-condition → trollreg.spl / #TROLLRE.spl`.
- `trollreg.spl` on trigger: `op39` knock-down (prone) **then `op17 p1=100 p2=2` = set HP to
  100% of max** = **full heal**. This is the "troll falls down and gets back up at FULL HP
  unless you finish it with fire or acid while it's down." Physical/normal damage alone can
  **never** kill a troll.
- `dwtrrg2.SPL` (SCS-added): `op17 p1=2 p2=0` = **+2 HP every round passive regen** layered on
  top of the vanilla downed-heal. SCS makes the chip damage you do between knockdowns regen back.

### REGHP1 (lemure) — `op98 p1=6 p2=3` = **regenerate 6 HP/round**
A 16-HP fiend that heals 6/round. If you can't burst it, it out-heals a low-level party.

---

## Tedium offenders (ranked) + softening direction

### 1. Catacomb skeletons `BDSKGR00-04` (prologue rest table) — worst, highest-frequency
**Why it's a slog:** the rest table that fires at 39% felt / max 6 / diff 80. Every skeleton
is **missile-90% (archery nearly useless), slash-50% & pierce-50% (most martial weapons
half-damage)**, crush-0% — so **only blunt weapons do full damage** — *and* RING95 + engine
UNDEAD immunity means **no CC works** (Sleep/Command/Horror/Charm all blank). A fresh party
with bows/swords and crowd-control spells has been handed a fight where its whole toolkit is
turned off, then handed six of them, repeatedly, every failed rest.
**Softening:** drop **missile 90→0** and **slash/pierce 50→0** on the rest-table skeletons
(keep crush-0 so blunt stays good and the undead "blunt is best" flavour survives; optionally
keep a token cold immunity). Optionally allow Sleep/Command to work by removing RING95 from the
low-tier `BDSKGR00`. This single change makes archers and fighters functional and is the
highest-leverage edit in the whole project.

### 2. Trolls (`TROLL01/SM`, `TROLFR01`, `BDTROLL1/2`) — un-killable without fire/acid
**Why:** downed → **full-heal** (trollreg) + **+2 HP/round** SCS passive + total disabler
immunity. At low level, without a reliable fire/acid source on every troll knockdown, the
fight loops forever; one missed finish resets the troll to full.
**Softening (remix-level):** for trash trolls, either (a) strip `dwtrrg2` so chip damage
sticks, and/or (b) lower the trollreg downed-heal from 100% to a fixed small value so a troll
that's beaten down stays beatable, or (c) simplest for spawn tables — **don't put trolls in
rest/trash tables at all**; reserve them for 1-2 deliberate scripted fights where the party is
expected to have fire/acid. Do NOT touch TROLLIMM lightly (it's load-bearing for the intended
"trolls resist disablers" identity) — the heal is the problem, not the immunity.

### 3. Magic-weapon-gated elites in low-level pools — `IMMUNE1` carriers
`BDWOLFVA` (vampiric wolf), `BDSHSOUL` (shadow), `BDSKGR08`, `BDIMP` are **immune to
non-magical weapons**. If any of these appear in a wilderness rest table during a stretch
where party members still carry mundane weapons, those characters contribute zero.
**Softening:** keep them out of random rest tables (scripted-only), OR for remix trash
versions, remove `IMMUNE1` so they can be hit normally.

### 4. Skeleton mage `BDSKGR07` — surprise spellcasting in a "trash" pack
Knows `SPWI125/112/213/212/305` (L1-L3 arcane — incl. a L3 nuke). A rest ambush that quietly
includes a caster spikes difficulty unpredictably and rewards save-scumming.
**Softening:** exclude casters from rest tables, or down-rank its spellbook to non-damage
utility.

### 5. Resist/regen specialists that punish a single damage type
- **JELLOC / JELLYGR (slimes): missile-100% (fully immune to arrows/bolts/slings/darts)** —
  archery does nothing; JELLOC also splits. JELLYGR elec-100, JELLOC cold/magic-resistant.
- **Fire skeletons BDSKGR05/06:** fire-immune (punishes a fire-mage party that just learned
  fire works on the *other* skeletons).
- **Lemure BDLEMURE:** 6 HP/round regen + fire/cold resistance.
- **BDIMP:** fire/cold/elec-100 + magic-25 + ~45 SCS spell immunities + teleport — effectively
  un-nukeable; only safe as a deliberate scripted nuisance, never trash.
**Softening:** for trash variants, cut the single-type 100% immunities down to ~50% so the
type is "bad against this" rather than "does literally nothing," preventing the
"my whole build is invalid this fight" feel.

### 6. High-APR / strong-save bruisers (lower priority — these are "fair" danger)
`SPIDPHAS` (84 HP, THAC0 7, save-vs-spell 2, teleports), `SPIDSW` (4 APR), `GHOUL`/`GHAST`
(paralysis-on-hit — a real party-wipe vector at low level), `BDWYRML1` (poison sting, AC -1),
`BDGIANHI` (98 HP, THAC0 8, rock throws). These aren't resistance-tedium; they're just
**lethal**, so they belong in the "few meaningful fights" bucket, not rest tables. Ghoul/ghast
paralysis is the one to watch for the rest-table selection — a paralyzing enemy on a failed
rest can chain-lock a sleeping party.

---

## Recommended rest-spawn-table inputs (for the 01-rest-ambush work)

- **Safe-ish rest fodder** (low HP, no resistances, no CC immunity, beatable by any toolkit):
  `BDWOLF`, `BDWOLFDI`, `BDBANDIT`, `HOBGOB`, `ORC01_`, `SPIDHU`, `BDBOAR02`, `BDBEARBL`.
- **Acceptable with the skeleton softening applied** (see offender #1): `BDSKGR00/04`.
- **Keep OUT of random rest tables** (scripted-only / meaningful fights): all **trolls**, all
  **IMMUNE1** carriers (`BDWOLFVA`, `BDSHSOUL`, `BDSKGR08`, `BDIMP`), `BDLEMURE`, `SPIDPHAS`,
  `SPIDSW`, `BDWYRML1`, `BDGIANHI`, `BDMYCRD`, the slimes (missile immunity), and the skeleton
  **mage** `BDSKGR07`.
- **Paralysis caution:** if `GHOUL`/`GHAST` stay in any rest table, pair the felt-rate cut from
  doc 01 with a hard `max` cap of 1-2 so a failed rest can't chain-paralyze the party.
