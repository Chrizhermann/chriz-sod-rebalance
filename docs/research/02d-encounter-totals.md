# 02d — All-Areas Encounter Totals & Trash Ranking (SoD)

Status: **complete**. Date: 2026-06-21.
Master dataset: **`docs/research/sod_encounters_full.csv`** (one row per `override\BD*.are`, 76 areas,
sorted by `placed_enemy_count` desc). Builder: `C:\tmp\sod_research\prologue\build_full.py` (read-only
on the game dir). Supersedes the scripted-only `sod_areas_dataset.csv` for the trash picture.

## Method (and why it differs from the old CSV)

- **placed_enemy_count** — actors in the ARE actor table (ptr @`0x54`, CRE resref @actor+`0x80`)
  whose referenced CRE has allegiance **EA ≥ EVILCUTOFF (200)** (EA @ CRE `0x270`). This is the
  real combat population and is what the old scripted-only CSV missed entirely.
- **placed_enemy_top** — top ~6 hostile CRE resrefs with counts.
- **scripted_oneoff_enemies** — one-time scripted `CreateCreature*` enemies (EA ≥ 200) from the
  area's own `.baf`, **excluding any resref already placed** (so we don't double-count), and with
  **difficulty-branch dedup**: `Difficulty()`-gated variants of the same spawn block are collapsed
  to their largest variant instead of summed (the player only experiences one difficulty). Companions
  (`*7`/`*7_`), cutscene/quest NPCs, and commoners are excluded automatically — they aren't EA ≥ 200.
- **rest_active / rest_felt_day / rest_felt_night / rest_max** — from the rest struct @`0xC0`;
  felt% = `1−(1−c/100)^8` (the verified per-hour roll, see `01-rest-ambush-mechanic.md`).
- **spawnpoint_enabled_count** — spawn points (ptr @`0x60`) with `enabled=1` (@sp+`0x86`) **and** a
  non-empty creature table. Day/night probabilities intentionally ignored.

### Caveats (read before using the totals)
- **Conservative on reinforcement waves.** Scripted waves that re-summon an already-placed resref
  (e.g. BD0130's ~28 `BDSKGR*`/`BDBONBAT`/`BDSHSOUL` skeleton-wave spawns, all of which are also
  pre-placed) are counted as **0** here to avoid double-counting. So a few set-piece sieges play
  **larger** than their `total_enemy` (BD0130 is ~109 live in practice vs. 81 in this table; the
  per-encounter detail is in `02a-encounters-prologue-coastway.md`).
- **Neutral→hostile actors not counted.** CREs placed as EA=NEUTRAL/ALLY that turn hostile by script
  (doppelgangers, the BD0064 giants, Coldhearth before activation) are not in `placed_enemy_count`
  (correct per the EA≥200 definition, but they are real fights).
- **Dormant/cutscene actors not filtered.** Hostile-EA actors flagged inactive are still counted.
- Spawn-point and rest spawns are **dynamic** and excluded from `total_enemy`.

## Grand total

**~1,329 one-time enemy mobs across all of SoD** = **1,141 pre-placed** + **188 scripted one-off**
(conservative; true live count is somewhat higher once same-resref reinforcement waves are added).
Enabled wandering spawn points are nearly nonexistent (only BD7400 has one) — SoD's dynamic threat
is almost entirely the **rest-header** system, not spawn points.

## Region totals (one-time enemy mobs)

| Region | Placed | Scripted | **Total** |
|---|---:|---:|---:|
| **Wilderness (BD7x)** — Coast Way Forest, Troll Claw, Forest of Wyrms, Dead Man's Pass, Bloodbark | 443 | 33 | **476** |
| **Coast Way + Coldhearth crypt** (BD10/11/12) | 237 | 6 | **243** |
| **Prologue** (Palace + Korlasz, BD00/01) | 140 | 15 | **155** |
| **Underground River** (BD50/51/53) | 111 | 22 | **133** |
| **Travel-ambush arena pool** (BD006x) | 78 | 8 | **86** |
| **Dragonspear / Avernus** (BD4x) | 49 | 37 | **86** |
| **Boareskyr Bridge** (BD20) | 70 | 0 | **70** |
| **Coalition Camp** (BD3000, scripted siege waves) | 0 | 67 | **67** |
| **Sewers / Endgame** (BD6x) | 12 | 0 | **12** |
| Other | 1 | 0 | 1 |

**Takeaway:** the **wilderness chapters (BD7x) carry ~36% of all SoD trash** and are the highest-value
target after the prologue/coastway tier this project started with. Dead Man's Pass and Troll Claw Woods
alone (243 mobs) rival the entire prologue+coastway placed population.

## All-areas trash ranking — top 15 by total enemy count

| # | Area | Name / role | Region | Placed | Script | **Total** | Rest felt@max |
|---|---|---|---|---:|---:|---:|---|
| 1 | BD7300 | Dead Man's Pass | Wilderness | 139 | 0 | **139** | 39/44 @3 |
| 2 | BD1200 | Coldhearth crypt (lower, boss) | Coast Way | 118 | 0 | **118** | 49/49 @3 |
| 3 | BD7100 | Troll Claw Woods | Wilderness | 104 | 0 | **104** | 49/57 @3 |
| 4 | BD1100 | Coldhearth crypt (upper) | Coast Way | 85 | 0 | **85** | 49/49 @3 |
| 5 | BD0130 | Korlasz catacomb L2 (boss) | Prologue | 81 | 0 | **81** (~109 live) | 39/39 @6 |
| 6 | BD3000 | Coalition Camp (siege) | Coalition | 0 | 67 | **67** | — |
| 7 | BD5000 | Underground River | Underground | 39 | 21 | **60** | 39/44 @3 |
| 8 | BD7200 | Forest of Wyrms | Wilderness | 47 | 0 | **47** | 39/44 @3 |
| 9 | BD7400 | Bloodbark Grove | Wilderness | 37 | 8 | **45** | 39/49 @3 (SP=1) |
| 10 | BD0114 | Korlasz spider nest | Prologue | 40 | 0 | **40** | 49/57 @3 |
| 11 | BD0066 | Goblin travel-ambush | Ambush pool | 38 | 0 | **38** | 28/39 @6 |
| 12 | BD7000 | Coast Way Forest | Wilderness | 22 | 16 | **38** | 34/34 @3 |
| 13 | BD2010 | Boareskyr (approach) | Boareskyr | 36 | 0 | **36** | 22/44 @3 |
| 14 | BD7220 | Forest of Wyrms (sub) | Wilderness | 36 | 0 | **36** | 39/49 @3 |
| 15 | BD5100 | Underground River (sub) | Underground | 35 | 0 | **35** | 39/53 @6 |

(Full sorted list of all 76 areas is in `sod_encounters_full.csv`.)

## Implications for the ~70% trash-cut

- A region-balanced cut needs the **wilderness (BD7x)** in scope, not just prologue/coastway — it is
  the single largest reservoir (476 mobs). Dead Man's Pass (139) is the biggest single area in SoD.
- The two **Coldhearth crypt** levels (203) and the **Korlasz catacomb** (81/~109) remain the marquee
  "set-piece buried in trash" cases flagged in `02a`.
- **Coalition Camp (BD3000)** is 100% scripted siege waves (67) — narrative set-piece; treat
  separately from wandering-trash cuts.
- Cutting placed actors is a clean `COPY_EXISTING`-on-`.are` operation (remove/!spawn actor table
  entries); it does **not** touch the rest-header lever (Design 01) or scripted story beats.
