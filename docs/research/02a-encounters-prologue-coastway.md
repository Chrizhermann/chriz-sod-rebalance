# 02a — Combat Encounter Inventory: SoD Prologue + Coast Way

Status: **complete** (objective inventory). Date: 2026-06-21.
Scope: every loose `BD00xx`, `BD01xx`, `BD10xx`, `BD11xx`, `BD12xx` `.are` in the game `override\`.
Read-only on the game dir. Tooling: `C:\tmp\sod_research\prologue\{parse_enc.py,are_parse.py}`
(IF-block CreateCreature parser + ARE actor/spawn-point parser, both EA-classified).

## Method & a critical correction to the dataset

`sod_areas_dataset.csv` counts only **scripted** `CreateCreature` from each area's *own* `.baf`,
and its regex misses the `CreateCreatureEffect`/`CreateCreatureDoor`/etc. variants. **The bulk of
SoD combat in this region is PRE-PLACED actors in the `.are` actor table, not scripted.** Example:
BD0130 lists 32 scripted spawns in the CSV but actually carries **81 pre-placed enemy CREs** plus
~28 scripted reinforcements. So this inventory is built primarily from the `.are` actor lists,
classified by each CRE's allegiance byte (EA @ `0x270`): `EA>=200` = enemy, `4` = ally,
`128` = neutral. Scripted spawns are added on top (one-time), and rest/spawn-point spawns are
tracked separately as *dynamic* sources.

Excluded from enemy counts (per brief): companions/recruits (`*7`/`*7_` import CREs — safana7,
dynahe7, MINSC7_, viconi7, EDWIN7_, JAHEIR7_, dorn7, baelot7, neera7, khalid7, CORWIN7, GLINT7,
rasaad7, bdmkhi7), nobles/commoners/servants/refugees (`BDNOB*`,`BDCOM*`,`BDSERV*`,`BDREF*`,
`BDFATMAN/WOM`,`BDGIRL/BOY`,`BDSIT*`,`BDSLEEP*`), cutscene/quest NPCs (Korlasz dialogue clones
`BDKORDE*`/`BDKORME*`, Imoen, Ophyllis, etc.), Flaming-Fist **allies** (EA=ALLY/GOODBLUE), and
corpse/ambience decoration CREs (the `*D`/`DEAD*`/`SKELDED`/`CORPSE*` props, EA=127).

## Region map (roles)

- **Ducal Palace + Baldur's Gate city (BD0010–BD0050, BD0100–BD0121)** — the prologue's social hub:
  victory return, war council, taverns/inns, refugee crisis, shops. Almost entirely non-combat
  (hundreds of neutral ambience actors). Two scripted story fights only.
- **Korlasz prologue dungeon (BD0113–BD0114, BD0120, BD0130, +empty BD0115/0118/0122)** — the
  actual prologue combat: spider nest, two catacomb levels, the Korlasz boss confrontation.
- **World-map travel-ambush arenas (BD0060–BD0067, +empty BD0065/0070/0072)** — the "You have been
  waylaid by enemies and must defend yourself!" (strref 216493) battle-maps the engine loads on
  **overland travel** ambush (orc/troll/giant/goblin/myconid themes). Region-agnostic pool that
  first becomes reachable once overland travel opens (Coast Way onward), not the linear prologue.
- **Coast Way Crossing (BD1000 "Flaming Fist Encampment", BD1010 spider/mimic cave)** — the
  post-prologue hub camp on a large outdoor map with a wilderness fringe.
- **Coldhearth Lich crypt (BD1100 upper / BD1200 lower)** — an optional undead dungeon in the
  Coast Way tier; boss `BDCOLDH` "Coldhearth Lich" with the `BDMISC60` phylactery puzzle.

## Per-area table

`En.enc` = # of distinct enemy IF-blocks (scripted) | `Placed` = pre-placed enemy actors |
`Total` = placed + one-time scripted enemies | `Rest` = felt% day/ngt @ max | `SP` = spawn points.

### Ducal Palace + City (BD0010–BD0050, BD0100–BD0121)

| Area | Name / role | En.enc | Placed | Total | Rest (felt@max) | SP | Class | Notable |
|---|---|---|---|---|---|---|---|---|
| BD0010 | Ducal Palace exterior | 0 | 0 | 0 | none (BDNOREST town) | 0 | — | 106 neutral ambience |
| BD0020 | City street | 0 | 0 | 0 | none | 0 | — | +1 pickpocket `bdthug06` (neutral) |
| BD0030/0040/0050 | City streets | 0 | 0 | 0 | none | 0 | — | ambience only |
| BD0021/0035 | (interiors) | 0 | 0 | 0 | none | 0 | — | empty/non-combat |
| BD0100 | Palace throne room | 1 | 3 | **6** | none | 0 | **set-piece** | assassins `BDGASS5`×3 (placed) + `bdgass1/2/3` (scripted) — the assassination |
| BD0101 | Palace (celebration) | 0 | 0 | 0 | none | 0 | — | 412 neutral crowd |
| BD0102 | War council | 0 | 0 | 0 | none | 0 | — | council NPCs (scripted, neutral) |
| BD0103 | Imoen's room | 1 | 0 | **~2** | none | 0 | set-piece | `bdgass1`/`bdgass4` assassins (Imoen attacked) |
| BD0104 | Flaming Fist HQ | 0 | 0 | 0 | none | 0 | — | refugees, Tiax |
| BD0105–0112 | Taverns/inns/shelters | 0 | 0 | 0 | none | 0 | — | patrons/sleepers (incl. neutral `BDTHUG*`) |
| BD0116 | Korlasz dungeon entry | 0 | 0 | 0 | none | 0 | story | `BDKORLAS` (neutral, surrender scene) + 3 Fist **allies** |
| BD0117 | (entry hall) | 1 | 0 | ~1 | none | 0 | story | `bdffdopp` doppelganger (neutral→hostile reveal) |
| BD0118 / BD0122 | (empty sub) | 0 | 0 | 0 | none | 0 | — | empty |
| BD0121 | Magic shop / crowd | 0 | 0 | 0 | none | 0 | — | `BDHALBAZ`,`BDKAZZRE`, shop golems (neutral) |

### Korlasz Prologue Dungeon (BD0113–BD0130)

| Area | Name / role | En.enc | Placed | Total | Rest (felt@max) | SP | Class | Notable |
|---|---|---|---|---|---|---|---|---|
| BD0113 | Wyrmling chamber | 0 | 4 | **4** | 57/57 @3 (BDWYRML1) | 0 | set-piece(min) | `BDWYRML1`×3 + `BDWYRMLI` |
| BD0114 | **Spider nest** | 1 | 40 | **~42** | 49/57 @3 (SPIDGI/HU/SW) | 0 | **TRASH** | `SPIDSM0_`×11,`SPIDSW`×8,`SPIDGI`×8,`SPIDPH`×6,`SPIDWR`×2,`BDSPIDGA`×2,`BDSPID7L`; +`SPIDPHAS`×2 on hard. Sub-script BD011406 adds neutral beetles |
| BD0115 | Wolf cave (sub) | 0 | 0 | 0 | 49/57 @3 **diff200** (BDWOLF) | 0 | trash(rest) | empty; rest-only wolf spawns |
| BD0120 | **Korlasz catacomb L1** | 0 | 12 | **12** | **39/39 @6 diff80** (BDSKGR) | 0 | trash+ | `BDSHIS01-07` shades×~9, `BDOGRE01`, `BDSHME01`; 13 neutral Korlasz/Fist NPCs |
| BD0130 | **Korlasz catacomb L2 (boss)** | ~4 | 81 | **~109** | **39/39 @6 diff80** (BDSKGR) | 0 | **set-piece buried in trash** | undead horde: `BDSHAD04`×8,`BDSHZOM1`×6,`BDSKGR0x`×~30,`GHAST`×4,`BDBONBAT`×4,`BDWIGHT1-3`×7,`BDWRAI02`×3,`BDMUMM01`, `BDOGRE02`; +~28 scripted skeleton/bonebat **waves**; boss **`bdkorlas`** (surrender branch) |

### World-map Travel-Ambush Arenas (BD0060–BD0067)

These load on overland-travel ambush (not the linear prologue). Each also has its own rest table.

| Area | Theme | En.enc | Placed | Total | Rest (felt@max) | Class | Notable |
|---|---|---|---|---|---|---|---|
| BD0060 | Orc/troll ambush | 0 | 8 | 8 | 28/39 @3 (ORC01_) | trash | `BDURE1A`×3,`BDURE1B`×2,`TROLL01`×2,`BDURE1C` (+12 corpse props) |
| BD0061 | Troll ambush | 0 | 9 | 9 | 28/39 @2 (TROLL01) | trash | `TROLL01`×4,`TROLLSM`×3,`TROLFR01` |
| BD0062 | Frost-troll + ooze | 3 | 5 | ~9 | 28/39 @3 (TROLFR01) | trash | `TROLFR01`×4,`TROLLGI`; scripted `JELLOC`/`BDMCARRI`/`BDOTYG0x`/`BDCCRAW1` (difficulty-scaled) |
| BD0063 | "Dead-magic" ambush | 0 | 5 | 5 | none (day10 empty) | trash | `BDURE2A–E`; Aura: "Dead magic zone" |
| BD0064 | Hill-giant ambush | 1 | 3 | ~6 | 57/57 @3 (BDGIANHI) | trash | `BDURE4A–C` (neutral→hostile) + scripted `BDURE4D/E` |
| BD0066 | **Goblin horde ambush** | 0 | 41 | **41** | 28/39 **@6** (BDGOB02) | **TRASH** | `BDGOB01-08`×38 + `ANKHEG`×3 |
| BD0067 | Myconid ambush | 0 | 13 | 13 | 57/57 @3 (BDMYCRD) | trash | `BDMYCRD`×7,`BDMYCBL`×2,`BDSHRIE2`×2,`BDBEETBH`×2 |
| BD0065/0070/0071/0072 | (unpopulated) | 0 | 0 | 0 | none | — | empty arena slots |

### Coast Way Crossing + Coldhearth Crypt (BD1000–BD1200)

| Area | Name / role | En.enc | Placed | Total | Rest (felt@max) | SP | Class | Notable |
|---|---|---|---|---|---|---|---|---|
| BD1000 | **Coast Way Crossing** (Fist camp) | 0 | 24 | 24 | 49/57 @3 (BDWOLF/DI/BEAR/BANDAM) | **7** | trash (fringe) | wilderness fringe: spiders `SPID*`/`BDSPIDGA`×17, `ZOMBIE`×2, `BDWRAI01`, `BDBEARBR`, `BDMENGO`. 136 neutral camp NPCs. **7 spawn pts** (Wolves×2, Worgs, Spiders×2, Bears×2) — **all `enabled=0`** by default, max 6 |
| BD1010 | Spider/mimic cave | 4 | 10 | **~18** | 49/57 @3 (JELLOC) | 0 | set-piece(min)+trash | `SPID*`/`BDSPIDGA`×~9; scripted **`BDMIMIC`** ambush + `JELLOC`×4 + `BDOTYG01` + phase spiders (difficulty-scaled) |
| BD1100 | **Coldhearth crypt (upper)** | 0 | 85 | **85** | 49/49 @3 **diff200** (ZOMBIE/GHOUL) | 0 | **TRASH** | `BDMCARRI`×12,`BDSHZOM1`×10,`ZOMBIE`×9,`GHOUL`×9,`GHAST`×8,`BDWIGHT1-3`×12,`BDCCRAW1`×6,`BDGHASTG`×5,`BDUMBER1`×4 umber hulks,`BDOTYG0x`,`BDMUMM01` |
| BD1200 | **Coldhearth crypt (lower, boss)** | 2 | 118 | **118** | 49/49 @3 **diff200** (GHOUL/ZOMBIE/SKGR) | 0 | **set-piece buried in trash** | `BDBONBAT`×17,`BDDEAD01`×10,`BDSHSOUL`×10,`BDSKGR0x`×~40,`BDSHZOM1`×9,`ZOMBIE`×6,`BDWIGHT*`×16,`GHOUL/GHAST`×9,`BDMUMM01`×3,`BDWRAI02`×3,`BDBRONZE`,`BDUNSLGU`; boss **`BDCOLDH`** + `BDMISC60` phylactery respawn mechanic |

## Region tallies (enemy mobs, placed + one-time scripted; rest/SP excluded)

| Sub-region | One-time enemy mobs |
|---|---|
| Ducal Palace + City | ~9 (only BD0100 ≈6, BD0103 ≈2, BD0117 ≈1) |
| Korlasz prologue dungeon | **~167** (BD0114 42, BD0120 12, BD0130 ~109, BD0113 4) |
| Coast Way Crossing + Coldhearth crypt | **~245** (BD1100 85, BD1200 118, BD1000 24, BD1010 18) |
| **Linear-path subtotal** | **~421** |
| Travel-ambush arena pool (BD006x) | ~92 across 7 arenas |
| **Region grand total** | **~513 enemy mobs** |

On top of this: every rest-active area adds dynamic rest-spawns, and BD1000 has 7 (currently
disabled) wandering spawn points. Two areas exist purely for rest-spawns (BD0115 wolves, and the
empty arenas). Most of the city/palace is pure ambience (1000+ neutral actors, zero combat).

> **All-SoD context:** the authoritative all-areas master dataset is `sod_encounters_full.csv`,
> with cross-region totals + trash ranking in `02d-encounter-totals.md`. SoD grand total ≈ **1,329**
> one-time enemy mobs; the **wilderness (BD7x)** chapters (476) are the largest reservoir, ahead of
> this prologue+coastway tier (~243 placed under the master CSV's conservative no-double-count rule).

## (a) Biggest TRASH-cut candidates

1. **BD1200 Coldhearth crypt lower — 118 undead.** ~40 skeletons + 17 bone bats + 16 wights +
   zombies/ghouls/mummies, around one boss. Single largest mob pile in the region.
2. **BD0130 Korlasz catacomb L2 — ~109 undead** (81 placed + ~28 scripted waves). The prologue
   climax is an attrition slog, not a fight.
3. **BD1100 Coldhearth crypt upper — 85 undead** (carrion crawlers, zombies, ghouls, wights,
   4 umber hulks). Pure filler corridor before the boss level.
4. **BD0114 spider nest — ~42 spiders.** One room, eight spider sub-types, zero stakes.
5. **BD0066 goblin travel-ambush — 41** (38 goblins + 3 ankhegs); plus the BD006x pool overall
   (~92 across orc/troll/giant/myconid arenas) is repeatable overland-travel trash and the prime
   target if the travel-ambush *frequency* is also being reduced.
   (Runners-up: BD1000 fringe ~24, BD1010 ~18, BD0067 myconid 13, BD0120 Korlasz L1 12.)

## (b) SET-PIECES worth preserving / enhancing

- **Korlasz boss (BD0130, `bdkorlas`)** — the prologue's named antagonist, with a real
  surrender/spare branch. The fight should be Korlasz + a curated elite undead guard, not 109 mobs.
- **Coldhearth Lich (BD1200, `BDCOLDH`)** — already has the standout `BDMISC60` phylactery puzzle
  (kill → respawns unless phylactery destroyed). Best boss in the region; preserve the mechanic.
- **Mimic ambush (BD1010, `BDMIMIC`)** — characterful difficulty-scaled trap encounter.
- **Palace assassination (BD0100/BD0103)** — story beat; small, already appropriately sized.
- **Wyrmling chamber (BD0113)** — small, thematic; fine as-is.

## (c) "Make it meaningful" — top 3 candidates

1. **Korlasz catacomb climax (BD0120+BD0130).** Cut the ~120 trash undead across both levels by
   ~70%, drop the scripted skeleton waves, and rebuild Korlasz (`bdkorlas`) into a genuine boss
   fight with a handful of distinct elite guards (e.g. a wight/mummy lieutenant + a few skeleton
   warriors). This is the prologue's signature fight and currently its worst slog.
2. **Coldhearth Lich (BD1100→BD1200).** Thin the 203 combined undead to a curated approach +
   throne guard, and let the lich + phylactery puzzle carry the encounter. Highest payoff: a great
   mechanic is currently drowned by trash.
3. **Spider nest (BD0114)** → consolidate ~42 spiders into one meaningful brood encounter (a phase-
   spider matriarch + a small brood, with terrain/webs), or cut hard. *Alternatively* promote the
   **BD1010 Mimic** trap as the 3rd showcase if a non-undead variety beat is preferred.

## Prologue catacomb rest situation

Both Korlasz catacomb levels (**BD0120, BD0130**) carry the same hostile rest header:
`day=6 / night=6` → **felt 39% per 8h rest**, **max 6**, **difficulty 80**, table
`BDSKGR02|BDSKGR00|BDSKGR04` (skeleton warriors/archers — missile- and fire-resistant per their
CREs). diff80 × party level always exceeds 6, so **every** ambush spawns the full **6 skeletons**.
Combined with the static 12 (L1) + ~109 (L2) undead garrison and ~28 scripted reinforcement waves,
the player must rest to recover spell slots mid-dungeon yet faces a 39%/rest skeleton ambush that
heals nothing and forces a re-rest (compounding per `01-rest-ambush-mechanic.md`). This is the
mechanical core of the "prologue shitshow." Recommendation for the prologue dungeon specifically:
make it near-restful (day/night → 1–2, felt ~10–15%) and cap max to 1–2, since the dungeon is
already dense with set static combat. The city/palace areas use `BDNOREST` (town no-rest) and need
no change. The BD006x travel-ambush arenas are entered via the overland map, not rested in.
