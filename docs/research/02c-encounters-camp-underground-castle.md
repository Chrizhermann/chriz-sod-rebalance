# 02c — Encounter Inventory: Boareskyr Bridge → Coalition Camp → Underground River → Dragonspear Castle → Avernus → Ambush

Status: **verified** against the live install's decompiled scripts (`research/data/sod_baf/*.baf`),
pristine SoD `.are` actor/spawn-point tables, and per-CRE `EA` allegiance bytes. Date: 2026-06-21.
Region scope: the SoD **mid/late** arc — every loose `BD2###`/`BD3###`/`BD4###`/`BD5###`/`BD6###` area.

## Method & data provenance

- **Scripted spawns** — counted from the live decompiled `.baf` (1232 scripts). Each
  `CreateCreature*` call grouped by enclosing `IF`/`THEN` trigger block (so a "spawn" is tied to its
  story condition). Tooling: `C:\tmp\sod_research\late\analyze.py`, `summarize.py`. Full block dump:
  `C:\tmp\sod_research\late\all_blocks.txt`.
- **Placed actors** — parsed from the area `.are` Actors table (offset `0x54`, 0x110-byte entries;
  CRE resref at `+0x80`, friendly label at `+0x00`). The label field ("Crusader Elite", "GOBLIN_ARCHER",
  "BF SOLDIER") is authoritative for friend/foe. **Sourced from the LIVE install override**
  (`override\BD*.ARE` — note the **uppercase `.ARE`** extension; a lowercase `*.are` glob silently
  misses all 762 area files, which is why an earlier pass wrongly concluded the areas weren't in
  override). **Re-verified 2026-06-21: live-override actor counts are identical to the pristine
  BG1EE+SoD `.are` across all 20 areas** — the only difference is BD5300 carrying one extra actor
  (`c0mnev01` "Black", a mod-added familiar; not an enemy). This confirms SCS/CDTweaks modify CRE
  *stats* in place, not the area actor lists, so the placed-enemy counts here are valid for the live game.
- **Allegiance** — `EA` byte (CRE `0x270`) read for the ambiguous families.
  **Key finding: almost every SoD crusader/monster CRE ships `EA=128 (NEUTRAL)` and is turned hostile
  by script** (`ChangeEnemyAlly`/`Enemy()`) when its battle fires — so `EA` alone under-counts enemies;
  the actor *label* + spawn *trigger* are the real discriminators. Verified hostile-on-spawn (`EA=255`):
  `bdwave*` (siege waves), `bdguar55-60` (river gate attack), `bdmycrd/bdspidgi/bdtreant/bdshad04/bdimp/
  bdlemure/bddevil*` (monsters). Verified **coalition allies** (fight *with* the party): `bdfist*`
  (Flaming Fist), `bdffsol/bdffmag`, `bddagf*` (Daggerford), `bdwtr*`, `bdteam*`, `bdcoa*`, `bdhelp*`,
  `bdbfor*` (Bridgefort). These 344 ally instances are **excluded** from all enemy counts below.
- **Rest spawns** — from `sod_areas_dataset.csv` (felt% per 8h rest already computed; see `01`).
- Caveat: in the big battles many placed crusaders activate in *phases* (battle script gates them), so
  "placed" is the roster, not the simultaneous on-screen count. Counts are enemy *instances*, not
  distinct fights.

## Per-area inventory

Enemy columns = live hostiles (placed actors with hostile labels, minus `DEAD_*` corpses) + scripted
hostile spawns. "Ally" = excluded coalition/garrison combatants.

| Area | Role | Plc Cru | Plc Mon | Scr Cru | Scr Mon | **LIVE enemies** | Ally(excl) | Rest (day/night→felt, max,diff) | Class |
|---|---|--:|--:|--:|--:|--:|--:|---|---|
| **BD2000** | Boareskyr Bridge (hub + bridge battle + goblin raid) | 37 | 33 | 31 | 6 | **107** | 39 | 3/7 → 22%/44%, max3, diff2 | SET-PIECE + TRASH |
| **BD2010** | Bridge approach — goblin warband camp | 0 | 35 | 0 | 0 | **35** | 0 | 3/7 → 22%/44%, max3, diff200 | TRASH |
| **BD2100** | Bridgefort interior (garrison, no combat) | 0 | 1 | 0 | 0 | **1** | 29 | — | NON-COMBAT |
| **BD3000** | Coalition Camp (hub + **climactic siege defense**) | 0 | 5 | 69¹ | 0 | **74** | 214 | — | SET-PIECE (climax) |
| **BD4000** | Dragonspear Castle exterior — **gate assault** | 71 | 3 | 30 | 0 | **104** | 35 | — | SET-PIECE |
| **BD4100** | Castle Keep, 1st floor (Skie/dream, story) | 0 | 2 | 0 | 0 | **2** | 13 | — | NON-COMBAT |
| **BD4300** | Castle Basement — wave dungeon | 20 | 0 | 38 | 4 | **62** | 9 | — | SET-PIECE (mini) |
| **BD4400** | Avernus (hellscape) | 6 | 11 | 0 | 2 | **19** | 0 | 5/5 → 34%/34%, max3, diff200 | TRASH + rest |
| **BD4500** | Avernus Bridge (aftermath) | 0 | 4 | 0 | 0 | **4** | 0 | 5/5 → 34%/34%, max3, diff200 | LIGHT + rest |
| **BD4600/4601** | Avernus sub-areas | 0 | 0 | 0 | 3 | **3** | 0 | — | LIGHT |
| **BD4700** | Caelar Argent confrontation (Avernus portal) | 7 | 6 | 0 | 0 | **13** | 0 | — | SET-PIECE (boss) |
| **BD5000** | Underground River — big wilderness dungeon | 17 | 31 | 14 | 28 | **90** | 3 | 6/7 → 39%/44%, max3, diff200 | TRASH-HEAVY + rest |
| **BD5100** | Underground River warrens (myconid/treant + patrols) | 40 | 29 | 16 | 16 | **101** | 0 | 6/9 → 39%/53%, **max6**, diff2 | TRASH-HEAVY + rest |
| **BD5110** | Underground River — undead pocket | 0 | 16 | 0 | 0 | **16** | 0 | **12/18 → 64%/80%**, max3, diff200 | TRASH + worst rest |
| **BD5200** | The Warrens — crusader muster/barracks (infiltration) | 43 | 3 | 0 | 0 | **46** | 0 | — | ENEMY STRONGHOLD |
| **BD5300** | Crypt (dragon-jar quest) — undead | 0 | 24 | 0 | 0 | **24** | 0 | — | TRASH |
| **BD6000** | Abandoned Sewers (escape route) | 0 | 16 | 0 | 0 | **16** | 2 | — | TRASH (filler) |
| **BD6100** | **The Ambush** — scripted defeat finale | 0 | 0 | 11² | 0 | **11** | 0 | — | SET-PIECE (story) |
| **BD6200** | Sewers Exit | 0 | 0 | 0 | 0 | **0** | 0 | — | EMPTY |

¹ BD3000 scripted-crusade 69 includes ~8 `bdcru01d-08d`/`bdcoa01d-06d` **parley cutscene** actors
(not combat) and the rest are `bdwave*`/`bdcatapu*` siege-assault waves + catapults.
² BD6100: the ambush is a respawning loop — `bdfinal1-5` (Shadow Thieves) `CreateCreatureAtLocation`
up to `bd_spawn_num=6` waves; it is a designed *loss* (party is put to sleep, leads into BG2 opening).

**REGION TOTAL: ~728 enemy instances** (placed + scripted, excl. corpses/allies/ambient/objects/named
NPCs). Plus **344 coalition-ally combatants** and the random rest tables above.

> **Accuracy note on the scripted columns.** Placed-actor counts are **exact and difficulty-independent**
> — the region's placed-enemy baseline is **460** and is the reliable figure for cut planning. The
> **scripted** columns **sum across all difficulty branches and therefore over-count**: SoD battle
> scripts branch on `Difficulty(...)`, and the engine fires only one branch per event. E.g. BD5000's
> `CreateCreatureEffect(…,"SPMONSUM")` wandering-monster wave shows 9 bears + 9 phase-spiders + 6 snakes
> across branches but spawns ~3 + 3 + 2 per trigger (the hardest branch on the user's Difficulty 5).
> Treat scripted totals as an upper bound; the design doc (`docs/design/02c-...`) cuts on the exact
> placed counts and names specific HARD/INSANE scripted branches to NOP.

### Enemy composition of the trash-heavy areas (for curation)

- **BD2000 goblin raid** (separate from the bridge battle): HOBGOBLIN_SCOUT×8, GOBLIN_ARCHER×5,
  GOBLIN_ELITE_ARCHER×3, BROWN_BEAR×3, Troll×2, WARG×2, HOBGOBLIN_VETERAN×2, GOBLIN_WORG_RIDER×2,
  HOBGOBLIN_ELITE_ARCHER×2, + GOBLIN_RAID_LEADER, HOBGOBLIN_CAPTAIN, GOBLIN_SHAMAN, HOBGOBLIN_PRIEST.
- **BD2010** goblin camp: GOBLIN_ELITE_ARCHER×12, GOBLIN_WARRIOR×9, GOBLIN_ARCHER×9,
  GOBLIN_ELITE_WARRIOR×3, GOBLIN_CHIEFTAIN, GOBLIN_SHAMAN.
- **BD5000** river: Ogre×5, GREATER_WYVERN×4, ORC_WARRIOR×4, HUGE_SPIDER×3, Skeleton×3, Rat×3,
  GARGANTUAN_SPIDER×2, Cyclops, BABY/WYVERN, SWORD_SPIDER, BROWN/BLACK/CAVE_BEAR + scripted gate-attack
  crusaders (bdguar55-60, EA255) and gate monsters.
- **BD5100** warrens: DARK_TREANT×7, MYCONID_RED×5, GARGANTUAN_SPIDER×5, MYCONID_BLUE×4,
  SHAMBLING_MOUND×3, Water Elemental×3, Ankheg, Bugbear + Crusader Archer×8 / PATROL×6 /
  PoisonedCrusader×4 / Crusader×4 / Crusader Mage×2.
- **BD5110**: SHADOW×10, WRAITH×4, GREATER_SHADOW×2 (and the game's worst rest rate).
- **BD5300** crypt: SKELETON_ARCHER×9, ZOMBIE×5, ARMORED_SKELETON×3, SHADOWED_SOUL×3,
  BLADED_SKELETON×2, TATTERED/SKELETON_WARRIOR.
- **BD6000** sewers: Rat×11, Green Slime×5 (pure filler).
- **BD4400/4500** Avernus: Lemure×8/×3, Imp×3/×1 (+ rest table BDIMP/BDLEMURE).

### The crusade-army co-op battles (fight alongside the coalition)

These four are the war set-pieces. The party fights *with* a large coalition army (the 344 excluded
allies: `bdfist/bddagf/bdwtr/bdteam/bdcoa`), against crusade forces:

- **BD3000 Coalition Camp siege** — the climax. `bd_battle`/`bd_battle_failed` trigger timed assault
  **waves** (`bdwave21-54`, ~14-16 enemies per wave, escalating with difficulty) + `bdcatapu`×10
  bombardment. Your side: ~214 ally instances (camp garrison + named commanders bdgarrus/bdmordau/
  bdauziel/bdandrus + reinforcement squads).
- **BD4000 Castle gate assault** — `bd_outer_gate_explosion` → crusader waves (`bdcru40-58`,
  `bdwtrx35-37`) vs coalition reinforcements (`bdfist35-38`, `bddagf35-38`); 71 placed crusaders
  (Soldier×17, Recruit×11, Mercenary×9, …) man the walls.
- **BD2000 Boareskyr Bridge battle** — `bd_open_drawbridge`/`bd_fists_attack`: crusaders
  (`bdcrus20-29`, `bdcrubb1/2`) vs Flaming Fist (`bdfist21-27`); plus named bosses The Barghest
  (BDBARGHE) & Oloneiros (BDOLONEI), fire-elemental phase.
- **BD4300 Castle Basement** — `bd_mdd905z_wave` two-wave dungeon: 20 placed + 38 scripted crusaders
  incl. insane cultists (`bdinsa01-07`, EA255) and crusader elites (`bdcrue30-34`).

## Region summary & recommendations

### Top trash-cut candidates (highest filler density, lowest story value)

1. **BD5100 Underground River warrens — 101 enemies, worst-rest dungeon (max6).** ~45 monster filler
   (Dark Treant×7, Myconid Red×5, Gargantuan Spider×5, Myconid Blue×4, Shambling Mound×3) + ~56
   crusader patrols. **Cut ~70% of the wandering monsters and patrols; collapse to a couple of curated
   pockets.** Also the prime rest-rate target.
2. **BD5000 Underground River — 90 enemies, ~60 of them wandering monsters** (ogres/wyverns/orcs/
   spiders/bears/skeletons, a zoo). Pure attrition. **Cut the bulk; keep one signature creature.**
3. **BD2010 + BD2000 goblin/hobgoblin raid — ~68 goblinoids** (35 in the camp + 33 raiding the bridge).
   Two oversized warbands flanking the bridge set-piece. **Cut each warband to a meaningful skirmish.**
4. **BD5200 The Warrens — 43 crusaders** (a barracks/muster you infiltrate). Over-populated; thin to a
   tense, sparser stronghold (most are ambient, combat is partly avoidable by stealth/disguise).
5. **Undead/filler pockets: BD5300 crypt (24), BD5110 shadows (16), BD6000 sewers (16 rats/slimes).**
   Low-stakes filler; halve or better. BD6000's Rat×11 + Slime×5 is the most pointless in the region.

(Region trash subtotal ≈ **300+ enemies** sit in the cut-candidate areas above — comfortably enough to
hit a ~70% region-wide reduction without touching a single set-piece.)

### "Make it meaningful" candidates (2-3)

1. **BD3000 Coalition Camp siege** — the emotional climax of SoD, currently delivered as anonymous
   timed `bdwave` spam (lose-by-attrition framing). Best target: replace endless filler waves with
   **fewer, named crusade champions** leading 2-3 distinct, scripted assaults (a breach, a flanking
   push, a final commander) so the camp's fall/hold *reads* as a battle, not a spawn timer.
2. **BD4000 Dragonspear Castle gate assault** — ~104 crusaders zerging the gate. Tighten into a real
   **breach fight**: a held wall, a battering-ram beat, and a notable gate commander, rather than 71
   identical wall-standers + reinforcement waves.
3. **BD5000/BD5100 Underground River** — after cutting the trash, promote **one** memorable encounter
   (e.g. a Myconid Sovereign with its colony, or the Cyclops/Wyvern pair) into a designed set-piece, so
   the long dungeon has a peak instead of a flat grind. (Alternative third: elevate **BD2000 Boareskyr
   Bridge** — The Barghest/Oloneiros are already named bosses worth leaning into.)

### Preserve (do not cut)

BD3000 siege, BD4000 assault, BD2000 bridge battle, BD4300 basement, BD4700 Caelar Argent (boss),
BD6100 The Ambush (scripted story defeat). These are the region's authored battles; trimming should
target the *trash that surrounds* them, not the set-pieces themselves.
