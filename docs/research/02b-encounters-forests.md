# 02b — SoD Encounter Inventory: Wilderness / Forest Region

Status: **verified** against the live install's loose `override\BD7*.are` / `.cre` files and the
decompiled area scripts in `research/data/sod_baf/`. Date: 2026-06-21.

Scope: every `BD7xxx` area present as a loose file in `override\` (11 areas). Method per the
standard: (1) area role, (2) scripted enemy spawns from the `.baf` (`CreateCreature*`), (3) rest
table from the ARE rest struct, (4) spawn-point presence, (5) TRASH vs SET-PIECE, (6) totals.

## Data provenance / method notes
- **Placed actors + spawn points + rest tables** parsed directly from each `.are` with a Python
  reader (`C:\tmp\sod_research\forests\are_parse.py`, `rest.py`, `coords.py`). For every actor the
  referenced CRE was opened and its **allegiance byte (0x270)**, **max HP (0x26)**, **kill-XP
  (0x14)** and **class levels (0x234)** read — so "enemy" here is **objective EA=ENEMY (255)**, not
  a guess. Quest creatures that ship `EA=NEUTRAL` but turn hostile in-quest are called out per area.
- **Scripted spawns** taken from the existing decompiled `.baf` (not re-decompiled).
- **Difficulty scaling caveat:** SoD places per-difficulty creature variants (name suffixes
  `_NORMAL/_CORE/_HARD/_INSANE`). Coordinate dump confirms these sit at *distinct* positions, i.e.
  higher difficulty adds *more* mobs at *more* points. So **placed count = the Insane/LoB upper
  bound; live count on Core/Normal is lower.** This is material only in **BD7220** (and the
  `_AMBUSH` variants in BD7230). BD7100/BD7200/BD7300 packs are *not* difficulty-suffixed → placed ≈ live.
- **Spawn-point day/night %**: the appearance-schedule dword at struct+0x88 shifts those fields, so
  I report only the reliable `enabled`/`max`/`table` for spawn points. Rest-struct day/night are the
  authoritative verified offsets (matches `sod_areas_dataset.csv`).
- **Rest ambushes** all spawn at `max=3`. `difficulty` is either 200 or 2 — but at a 6-character SoD
  party (total party level ~40-60) even `diff=2` yields `partyLevel×2 ≥ 3`, so **every forest rest
  ambush spawns the full 3** regardless. Felt %/8h rest from `research/01`.

---

## Per-area inventory

### BD7000 — Coast Way Forest  (role: first overland wilderness after the prologue; Rasaad re-meet)
Quest/neutral NPCs present: Isabella + Ikros (undead-hunter quest givers, SDD123), Koko, Rasaad
(re-join), rats/deer/birds (ambient fauna). Tsolak the vampire (`bdtsolak`) is the SDD123 boss
(spawned/sub-area, not a BD7000 placed actor).

| Group | resref | EA | each HP / kill-XP | count | class |
|---|---|---|---|---|---|
| Orc warriors | `ORC01_` | ENEMY | 30 / 120 | 5 | trash |
| Orc archers | `ORC02_` | ENEMY | 30 / 120 | 8 | trash |
| Orc priest | `ORC03_` | ENEMY | 24 / 175 | 1 | trash |
| Orc leader | `ORC04_` | ENEMY | 60 / 150 | 1 | trash |
| Orc shaman | `ORC05_` | ENEMY | 48 / 420 | 1 | trash |
| Orc raiders | `ORC06_` | ENEMY | 35 / 135 | 2 | trash |
| Orc bowmasters | `ORC07` | ENEMY | 40 / 175 | 2 | trash |
| Wargs | `BDWORG` | ENEMY | 27 / 120 | 2 | trash |

- **Placed enemies: 22** (one orc raiding party).
- **Scripted (SET-PIECE):** SDD123 vampire fight — `bd_123_summon_wolves` summons **`wolfdi` dire
  wolves** scaled by difficulty: **6** (below-Normal) / **11** (Normal) / **15** (Hard+). Tsolak boss.
- **Spawn point:** `Orcs` (`ORC01_/ORC02_`, max 6) — script-managed: `SpawnPtDeactivate` on load,
  `SpawnPtActivate` 1 day after the area is cleared (a respawn loop).
- **Rest:** en=1, **day 5 / night 5 → felt 34%**, max 3, table `BDWOLF, BDWOLFDI, ANKHEG,
  BDBOAR02, BDSPIDGI`.
- **Classification:** orc party = borderline (the area's signature fight); dire wolves = quest
  set-piece. Modest area.

### BD7100 — Troll Claw Woods  (role: becomes the **Coalition / Flaming Fist army camp** hub in Ch.9)
This is the major hub: entering forces `IncrementChapter("SODTXT9")`, an autosave, and moves **every
joinable NPC** (Baeloth, Corwin, Dynaheir, Edwin, Glint, Minsc, M'Khiin, Rasaad, Safana, Viconia)
plus Jaheira/Voghiln + the FF camp (Bence Duncan, Otilda, Belegarm, Mizhena, Thaird…) into the camp
corner. ~24 NEUTRAL camp/quest NPCs — **not combat**. The monster population fills the wilderness
parts of this large map.

| Group | resref(s) | each HP / kill-XP | count |
|---|---|---|---|
| Trolls (regular) | `TROLL01` | 54 / 1400 | 16 |
| Spectral trolls | `TROLSP01` | 64 / 1500 | 8 |
| Small / giant trolls | `TROLLSM` / `TROLLGI` | 32 / 750 · 64 / 1600 | 5 / 3 |
| Hobgoblins (cap/vet/scout/archer/priest) | `BDHOBG01-05` | 16-40 / 35-65 | 16 |
| Spiders (giant/huge/sword/gargantuan) | `SPIDGI/SPIDHU/SPIDSW/BDSPIDGA` | 18-72 / 270-3000 | 15 |
| Orcs (warrior/archer/raider/bowmaster/shaman/priest/leader) | `ORC0*` | 24-60 / 120-420 | 13 |
| Ogres (ogre/berserker/mage/half-ogre/shaman/chieftain) | `BDOGRE01-06` | 33-84 / 270-975 | 10 |
| Beetles (bombardier/boring) | `BDBEETMH/BDBEETBH` | 18-40 / 120-175 | 8 |
| Displacer beasts (+pack lord) | `BDDISPBE/BDDISPBP` | 48-72 / 975-1200 | 6 |
| Wild boars | `BDBOAR02` | 27 / 175 | 2 |
| Brown bears | `BEARBR` | 41 / 420 | 2 |

- **Placed enemies: ~105** — the second-densest forest map.
- **Scripted (SET-PIECE):** "The Irregulars" SDD225 trio **Kava / Farrl / Rend** (`BDKAVA/BDFARRL/
  BDREND`); Soralis + Lesser Stone Golem (golem-buy quest). Skie scene = cutscene, no combat.
- **Spawn points (9):** Spiders01/02, Wolves01, Hobgoblins01/02, Trolls01/02, Boars01/02 — **all
  `SpawnPtDeactivate`d on load**, reactivate 1 day after the area is cleared (respawn loop).
- **Rest (the heavy one):** en=1, **day 8 / night 10 → felt 49% / 57%**, max 3, table `BDBANDIT,
  BDWOLFDI, BDBOAR02, BDSPIDGI, BDBEARBL, **TROLL01**` — a 1400-XP troll can drop on a rest.
- **Classification:** overwhelmingly TRASH (troll/spider/ogre/hobgoblin sprawl) wrapped around a
  non-combat camp. Top-tier cut candidate.

### BD7110 — Troll lair (sub-area of BD7100)  (role: troll-cave set-piece)
Empty area script. Placed: `TROLL01`×5, `TROLLSM`×2, `TROLLGI`×3, `TROLSP01`×5, **`BDTROLSH` Troll
Shamaness** (56 HP / 2000 XP) boss.
- **Placed enemies: 16 trolls + shamaness.** Rest: day 8 / night 8 → felt 49%, table `TROLL01,
  TROLLSM`.
- **Classification:** SET-PIECE (troll lair w/ named boss), though oversized at 16.

### BD7200 — Forest of Wyrms (overland)  (role: wyvern/bugbear wilderness; gateway to the cult dungeon)
Neutral: Coogan (NPC), mountain lion, fauna.

| Group | resref(s) | each HP / kill-XP | count |
|---|---|---|---|
| Wyverns (baby/wyvern/greater) | `BDWYVR02/01/03` | 40-88 / 450-2000 | 13 |
| Bugbears (+vet/shaman/warleader/stalker) | `BDBUGB01/02/04/10/12/20` | 35-60 / 175-650 | 11 |
| Displacer beasts (+pack lord) | `BDDISPBE/BDDISPBP` | 48-72 / 975-1200 | 7 |
| Phase spiders (+astral) | `SPIDPH/SPIDPHAS` | 44-84 / 1400-4000 | 5 |
| Dire wolves | `WOLFDI` | 33 / 125 | 5 |
| Small spiders | `BDSPIDER` | 8 / 65 | 5 |
| Hill giant | `BDGIANHI` | 98 / 3000 | 1 |

- **Placed enemies: ~47.**
- **Spawn points:** Wolves/Boars/Wyverns/Spiders — script-deactivated/reactivated (respawn loop).
- **Rest:** day 6 / night 7 → felt 39% / 44%, max 3, table `BDWOLFDI, BDBOAR02, BDSPIDGI, BDBEARBR`.
- **Classification:** TRASH (wyvern + bugbear + displacer packs).

### BD7210 — Morentherene's cavern (sub of BD7200)  (role: **green-dragon set-piece**)
Single placed actor: **`BDMORENT` Morentherene** — young green dragon, 112 HP / **13000 XP**,
EA=NEUTRAL, asleep. Script lets you **sneak past** or wake it (casting a spell near it wakes it).
On wake at **Hard/Hardest** it summons reinforcements off-screen: `BDWYVR03` Greater Wyverns ×2/3/5
+ `BDDRGGRY` Young Green Dragons ×0/1/2 (Normal/Hard/Hardest). Area is `NOREST` until the dragon dies.
- **Classification:** marquee SET-PIECE. Preserve (and a prime "make it meaningful" anchor).

### BD7220 — Bugbear cave / Greater Shadow (sub of BD7200)  (role: spectacles-quest + bugbear warren)
- Placed: **36 bugbears** (`BDBUGB01/02/03/04/10/11/12/20/21`) **+ `BDSNORGA` Snorgash** (named
  chief, 70 HP / 975 XP) **+ `BDSHADOW` Greater Shadow** (72 HP / 3000 XP, EA=NEUTRAL, SDD118
  "spectacles" quest — only visible/active while a party member wears `bdmisc01`).
- **Difficulty-scaled:** many bugbears are `_HARD`/`_INSANE`/`_CORE` tagged → **live count on
  Core/Normal ≈ 22-24**, full 36 only on Insane.
- **Scripted:** ambush cultist `bdcultx2` at the BD7230 transition.
- **Rest:** day 6 / night 8 → felt 39% / 49%, max 3, table `BDBUGB01, BDBUGB10, BDBUGB20`.
- **Classification:** TRASH (bugbear warren) + one quest mini-set-piece (Greater Shadow / Snorgash).

### BD7230 — Bhaalist Cult Temple (sub of BD7200)  (role: **Forest-of-Wyrms climax dungeon**)
Mostly EA=NEUTRAL cultists you can parley/side-with or fight (quest-gated). Forced/triggered combat
and bosses:

| Creature | resref | HP / kill-XP | note |
|---|---|---|---|
| **Neothelid** | `BDNEOTHE` | 128 / **20000** | the marquee monster (eats a cultist in a cutscene) |
| **Darskhelin** | `BDDARSKH` | 68 / 9000 | boss |
| **Shadow Aspect** | `BDASHIRU` | 96 / 6000 | boss |
| **Akanna** | `BDAKANNA` | 66 / 4000 | boss; summons `bdservsu` Aerial Servants (1-2 by difficulty) |
| **Ziatar** | `BDZIATAR` | 81 / 3000 | boss |
| Umber Hulks | `UMBHUL01` | 74 / 4000 | ×2 |
| Invisible Stalkers | `STALKE_` | 64 / 3000 | ×3 |
| Mutated Crawlers | `BDMCARRI` | 42 / 650 | ×3 |
| Enthralled Cultists | `BDCULT41-44` | 40-90 / 1400-2000 | ×4 (Neothelid room) |
| Worgs | `WORG` | 26 / 120 | ×3 |
| Cultists (parley-able) | `BDCULT01-30` | 36-74 / 420-2000 | ~20, EA=NEUTRAL |

- **Scripted:** `BD7230AM` — 6 `cultist_ambushN` go invisible (`bdinvis`) and reposition to ambush
  *after* the Neothelid dies. `BD7230IN` = lootable-shelf flavor only.
- **Classification:** pure SET-PIECE quest dungeon. Preserve. (Trash content here is minimal — the
  worgs and maybe the enthralled cultists.)

### BD7300 — Dead Man's Pass  (role: largest overland trash field; Coalition parley cutscene; spectacles quest)
Quest/neutral NPCs: Gnaler, Kambaldur, Madele, Horst/Stalia/Nuber, plus the **spectacles** hidden
enemies — `bdearthe` Earth Elemental (128 HP / **11000 XP**) and `BDRAEANN` tiefling Raeanndra
(59 HP / 2500 XP) are EA=NEUTRAL and only hostile while a PC wears `bdmisc01`. `bdephrik` (Ephrik)
spawns after the Korlasz surrender. The `bd_plot 390` Corwin parley (crusaders bddelanc/bdnederl/
bdstoneh/bdbence/bddagf59/bdwtr61) is a **cutscene that retreats** — not combat. ~14 `BDOROG1D`
dead-orog corpses = battlefield-aftermath props.

| Group | resref(s) | each HP / kill-XP | count |
|---|---|---|---|
| Displacer beasts (+2 pack lords) | `BDDISPBE/BDDISPBP` | 48-72 / 975-1200 | 19 |
| Beetles (bombardier/boring) | `BDBEETMH/BDBEETBH` | 18-40 / 120-175 | 23 |
| Orogs (warrior/elite/scout/priest/shaman/chief) | `BDOROG01-05/SG` | 30-60 / 120-650 | 21 |
| Hill giants (+leader) | `BDGIANHI/BDGIANHL` | 98-130 / 3000-3500 | 11 |
| Dire wolves | `WOLFDI` | 33 / 125 | 11 |
| Ogres (all kinds) | `BDOGRE01-06` | 33-84 / 270-975 | 12 |
| Spiders (phase/sword/giant/gargantuan) | `SPIDPH/SPIDSW01/SPIDGI/BDSPIDGA` | 35-72 / 450-3000 | 12 |
| Hobgoblins | `BDHOBG01-04` | 16-40 / 35-65 | 10 |
| Wild boars | `BDBOAR02` | 27 / 175 | 7 |
| Worgs | `BDWORG` | 27 / 120 | 4 |
| Ettins | `PETTIN` | 80 / 3000 | 2 |
| Shambling mounds | `BDSHAMB` | 64 / 6000 | 2 |
| Dark treants | `BDTREANT` | 72 / 4000 | 2 |
| Cave bear / hamadryad / nymph | `BD328OSO/BDHAMADR/BDNYMP01` | 32-66 / 650-1400 | 1 / 1 / 1 |

- **Placed enemies: ~139** — the densest forest map by a wide margin.
- **Spawn points:** Boars/Wolves/Spiders/Bears — script-managed (Bears left deactivated).
- **Rest:** en=1, **day 6 / night 7 → felt 39% / 44%**, max 3, table `HOBGOB, BDWOLF, BDWOLFDI,
  BDSPIDGI, BDBOAR02, BDOROG01, **BDGIANHI**, BDBEARBR` — a 3000-XP **hill giant** can drop on a rest.
- **Classification:** overwhelmingly TRASH. The single biggest cut target in the region.

### BD7310 — Shadow tomb (sub of BD7300)  (role: undead set-piece room)
Empty area script. Placed: **`BDUNSLGU` Unsleeping Guardian** (58 HP / 4000 XP boss), `BDSHAD04`
Shadows ×5, `BDSHADGR` Greater Shadows ×2, `BDWRAI02` Wraiths ×2. = **10 undead.** No rest spawns
(empty table). SET-PIECE.

### BD7400 — Bloodbark Grove  (role: undead/fey-corruption wilderness; Neera "Uncommon Cold" SDD302; Basilisk quest)
Quest/neutral NPCs: Onoroth, Lord Dushwick, Chalmers, Grizzly Hunter.

| Group | resref(s) | each HP / kill-XP | count |
|---|---|---|---|
| Beetles (bombardier/boring) | `BDBEETMH/BDBEETBH` | 18-40 / 120-175 | 13 |
| Burning skeletons (+skel mage) | `BDSKGR05/06/07` | 20-40 / 300-900 | 9 |
| Cold wights | `BDWIGHT3` | 48 / 1400 | 4 |
| Imbued wights | `BDWIGHT2` | 40 / 1200 | 2 |
| Ghasts | `GHAST` | 32 / 650 | 2 |
| Bonebats | `BDBONBAT` | 40 / 975 | 2 |
| Dark treants | `BDTREANT` | 72 / 4000 | 2 |
| Greater basilisk | `BD302BAS` | 80 / **7000** | 1 (SET-PIECE, "Basilisk Sighting") |
| Shambling mound / shadowed soul | `BDSHAMB/BDSHSOUL` | 64-56 / 6000-1100 | 1 / 1 |

- **Placed enemies: ~37.**
- **Scripted (SET-PIECE):** SDD302 "Uncommon Cold" wolf-pack — `BDWOLFVA` Vampiric Wolf +
  `BDWOLFDR` Dread Wolves ×3 + `BDWOLF` ×4 (= **8**) ambush on the Neera quest.
- **Spawn point:** `Spawn 1` — **the only ACTIVE (en=1) streaming spawn point in the whole forest
  region**, max 6, table `BDSKGR00, GHOUL, GHAST, BDWRAIT1, BDWOLF/DI, BDSPIDGI/HU, BDBOAR02,
  BDBEARBR`. Deactivated while Lord Dushwick is present; reactivates 1 day later.
- **Rest:** day 6 / night 8 → felt 39% / 49%, max 3, undead table `BDSKGR00, GHOUL, GHAST,
  BDSPIDGI, BDWOLF, BDWRAIT1, BDBOAR02, BDBEARBR, BDWOLFDI, BDSPIDHU`.
- **Classification:** mixed — undead/beetle TRASH + good set-pieces (Greater Basilisk, the
  Bloodbark wolf-pack, the vampire den below).

### BD7410 — Vampire den (sub of BD7400)  (role: vampire set-piece)
Empty area script. Placed: **`VAMFLM01` Fledgling Vampire** (67 HP / **8000 XP** boss), `BDWOLFDR`
Dread Wolves ×4, `BDWOLFVA` Vampiric Wolves ×4, `WOLF` ×5 (+ neutral rats/bats). = **14 enemies.**
No rest (disabled). SET-PIECE.

---

## Region summary

**Total hard-placed hostiles (objective EA=ENEMY) across the 11 forest areas: ≈ 445.**
On top of that: per-hour **rest ambushes** in 9 of 11 areas (felt **34-57%/rest**, always max 3),
script-managed **respawning spawn points** (re-arm 1 day after each area is cleared) in BD7000/7100/
7200/7300, and **one always-on** spawn point in BD7400. (Rest design detail lives in `research/01`;
felt rates there confirm BD7100 day8/night10 = 49%/57% is the worst forest rest pressure, with a
1400-XP troll in its table; BD7300's rest table can drop a 3000-XP hill giant.)

Breakdown of placed hostiles by area:
| Area | role | placed enemies | dominant trash |
|---|---|---:|---|
| BD7300 Dead Man's Pass | overland | **~139** | displacers 19, beetles 23, orogs 21, hill giants 11, dire wolves 11, ogres 12 |
| BD7100 Troll Claw Woods | camp hub + wild | **~105** | trolls 32, hobgoblins 16, spiders 15, orcs 13, ogres 10 |
| BD7200 Forest of Wyrms | overland | **~47** | wyverns 13, bugbears 11, displacers 7 |
| BD7400 Bloodbark Grove | overland | **~37** | beetles 13, burning skeletons 9, wights 6 |
| BD7220 Bugbear cave | sub | ~36 (live ~24 Core) | bugbears |
| BD7000 Coast Way Forest | entry | 22 | orc warband |
| BD7230 Cult Temple | dungeon | ~18 forced (+~20 parley cultists) | set-piece |
| BD7110 Troll lair | sub | 16 | trolls (set-piece) |
| BD7410 Vampire den | sub | 14 | set-piece |
| BD7310 Shadow tomb | sub | 10 | undead (set-piece) |
| BD7210 Morentherene | sub | 1 (+ adds) | set-piece dragon |

### Top 5 TRASH-cut candidates (biggest, lowest-value, most repetitive)
1. **BD7300 Dead Man's Pass — cut hardest.** ~139 placed. The **23 beetles** (120-175 XP), **19
   displacer beasts**, **21 orogs**, **11 dire wolves**, **7 boars** are pure filler. A ~70% cut
   here removes ~95 mobs and barely dents the story. Keep the hill-giant-leader band + shambling
   mounds/dark treants/ettins as the area's threats.
2. **BD7100 Troll Claw Woods — cut hard.** ~105 placed. **32 trolls** + **16 hobgoblins** + **15
   spiders** stuffed around the army-camp hub. Thin the troll horde drastically (it's also a
   chapter-9 safe-zone), drop the hobgoblin/spider/beetle filler.
3. **Region-wide bug/beetle/spider/displacer filler.** Beetles ≈ **44** region-wide (8/23/13 in
   7100/7300/7400), displacer beasts ≈ **32** (6/7/19), low-XP spiders in every area. These are the
   clearest "delete on sight" trash — almost no narrative weight.
4. **BD7200 Forest of Wyrms overland — thin the wyvern/bugbear/displacer packs** (~47 → ~15). Leave
   a token wyvern presence as flavor before the dragon.
5. **BD7220 bugbear warren — shrink** (live ~24 → ~8) and lean on Snorgash + the Greater Shadow as
   the reason to enter.

### 2-3 fights to make MEANINGFUL (preserve / elevate; don't shrink these)
1. **Morentherene the green dragon (BD7210)** — already the model set-piece: sneak-or-fight, scales
   with difficulty, 13000 XP. Keep; this is the Forest-of-Wyrms payoff. Pair the cleared trash with
   a beefier single dragon fight.
2. **Hill Giant Leader warband (BD7300)** — promote the `BDGIANHL` leader + a tight giant/ogre core
   into *the* Dead Man's Pass set-piece that replaces the 139-mob slog. (Ettins / shambling mounds /
   dark treants are good secondary "elite pockets".)
3. **Troll Shamaness lair (BD7110)** or **Bloodbark Vampire den (BD7410) + Greater Basilisk
   (BD7400)** — a dangerous named troll-cave and a vampire/undead set-piece to anchor those regions
   after the surrounding troll/undead trash is thinned.

Untouchable set-piece dungeons (already quality, mostly non-trash): **BD7230 cult temple**
(Neothelid 20000 XP + Ziatar/Akanna/Darskhelin/Shadow Aspect) and **BD7310 shadow tomb**.
