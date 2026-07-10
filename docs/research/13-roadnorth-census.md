# 13 — Road-north / Boareskyr Bridge tier census (chapter-9 pass research)

Research data gathered by subagent 2026-07-10 from the dev install + repo decompiles.
DATA ONLY — decisions live in `docs/design/` and `docs/01-remix-wishlist.md`.

Placed-actor counts parsed live from the DEV install's `override/*.are` (actor list
`@0x54`, CRE resref `@actor+0x80`, allegiance `CRE@0x270`, kill-XP `CRE@0x14`, HP
`@0x26`; names via `lang/en_US/dialog.tlk`). Rest struct `@0xC0`. Worldmap adjacency
from `worldmap.wmp` area-link parse. Script cites are `research/data/sod_baf/*.baf`.
Enemy counts cross-check against `docs/research/02b-encounters-forests.md`
(BD7100≈105, BD7110=16+boss, BD7200≈47, BD7220=36, Morentherene 13k, Neothelid 20k)
— **all reconcile.**

## 0. What this arc is, and two corrections to the brief

This is **Chapter 9**: the march after the Coast Way pass. Entering **Troll Claw Woods
(BD7100)** fires `IncrementChapter("SODTXT9")` + `AddXPObject(Player1..6,10000)` and
sets `bd_plot=200` (`BD7100.baf:369-394`). The arc runs `bd_plot 200 → 293-295`
(Boareskyr resolution); the next area, **Coalition Camp (BD3000)**, fires `SODTXT10`
+15k and reveals the Underground River (`BD3000.baf:475,554`). So the boundaries are
**BD7100 (in) … BD2000 Boareskyr (out)**.

- **Correction 1 — "Forest of Wyrms" is BD7200, not BD5000.** The brief's `BD5000 /
  BD51xx / BD52xx` are a different, LATER cluster: `BD5000`/`BD5100` = **Underground
  River**, `BD5200` = **The Warrens**, `BD5300` carries the `bdhalat` dragon-spirit
  (dataset `name` column; `worldmap.wmp`). All of them hang off **BD3000's** west link
  and are gated `bd_plot 384+` (`BD7300.baf:9`) — i.e. **Chapter 10, the next arc.** The
  Forest of Wyrms this arc means is **BD7200** (+ interiors BD7210/7220/7230).
- **Correction 2 — the 32k dragon-spirit is NOT in this arc.** `BDHALAT`/`BDCORWIJ`
  (Halatathlaer, 32k, `docs/research/03`) is placed in **BD5100/BD5300** (grep:
  `bdhalat` → `BD5100.baf`,`BD5300.baf`,`BDDRAGSP.baf`), the Underground River/Warrens.
  Doc 03's "(Forest of Wyrms)" label is the same BD5000↔BD7200 mixup. This arc's dragon
  is the **living green dragon Morentherene** (BD7210), a different creature.

## Area map & travel

| Resref | In-game name | Role | Reached from (`worldmap.wmp`) |
|---|---|---|---|
| **BD7100** | Troll Claw Woods | **Ch-9 start (+10k)**; becomes the **army-camp hub** in Ch.9 | bd1000/bd7000 (Coast Way) |
| BD7110 | Troll lair (Shamaness) | Set-piece sub-cave | Local transition from BD7100 |
| **BD7200** | Forest of Wyrms | **OPTIONAL** overland detour (bd7100→bd2000 links direct) | bd7100 |
| BD7210 | Morentherene's cavern | Green-dragon set-piece (sub of BD7200) | Local from BD7200 |
| BD7220 | Bugbear cave / Greater Shadow | Bugbear warren + spectacles quest (sub of BD7200) | Local from BD7200 |
| **BD7230** | Bhaalist cult temple | Forest-of-Wyrms climax dungeon (Neothelid, Ziatar) | Local from BD7200 |
| **BD2000** | Boareskyr Bridge | **Arc climax** — Bridgefort siege + bridge battle | bd7100/bd7200; revealed `BD1000.baf:488` |
| BD2010 | (Boareskyr goblin warren) | Goblin-warband sub-area | Local from BD2000 |
| **BD2100** | Bridgefort (interior) | Besieged-fort quest/NPC hub; **Voghiln + Neera recruit** | Local from BD2000 |
| BD3000 | Coalition Camp | **Ch-10 (+15k) — NEXT arc, not censused** | bd2000 |

**Optionality (verified `worldmap.wmp`):** `bd7100` links N→ **bd2000, bd7200**, bd1000,
bd7000. So the main march is **Troll Claw Woods → Boareskyr**; the whole **Forest of
Wyrms + cult temple + Morentherene is a side-loop** you can skip. Matches wishlist item
16 ("Morentherene … optional").

---

## TIER 1 — Troll Claw Woods (BD7100 + BD7110)

### BD7100 — the trash-densest area in the arc, wrapped around the Ch-9 camp
- **104 placed hostiles, 79,055 kill-XP (field/party-total; ÷6 ≈ 13,176/char).** All
  pre-placed & active on load (area script is camp/quest logic). Composition:
  - **Trolls ×32:** TROLL01 ×16 (1400), TROLSP01 spectral ×8 (1500), TROLLGI ×3 (1600),
    TROLLSM ×5 (750) — the signature threat and ~57k of the 79k.
  - **Spiders ×15:** BDSPIDGA gargantuan ×4 (**3000 ea**), SPIDSW sword ×3 (2000),
    SPIDGI ×4 (450), SPIDHU ×4 (270) — the 4 gargantuans alone are 12k.
  - **Hobgoblins ×16** (BDHOBG01-05, 35-65 ea — chaff), **Orcs ×13** (ORC01-07,
    120-420), **Ogres ×10** (BDOGRE01-06, 270-975), **Beetles ×8** (BDBEETMH/BH,
    120-175), **Displacers ×6** (BDDISPBE ×5 975 + BDDISPBP pack lord 1200), Boars ×2.
- **Camp hub (Ch.9):** ~24 NEUTRAL camp/quest NPCs relocate here — Bence Duncan,
  Belegarm, Mizhena, Thaird, Otilda, Voghiln (VOGHIL7 ×2 placed), the Irregulars
  Kava/Farrl/Rend, Soralis, plus Flaming-Fist ranks (BDFIST21-26). All self-destroy at
  `Chapter>9` (`BD7100.baf:64-80`). **A cut here must preserve the camp cast.**
- **Scripted set-pieces:** "The Irregulars" (BDKAVA/BDFARRL/BDREND) + Soralis's stone-
  golem-buy quest (both quest/dialogue, non-hostile placement).
- **Rest (current dev, post-wave-1):** en=1, **day 1 / night 2 → felt 8% / 15%**, max 3,
  diff 2, table `BDBANDIT|BDWOLFDI|BDBOAR02|BDSPIDGI|BDBEARBL|TROLL01` (a 1400-XP troll
  can still drop). **Vanilla was day 8 / night 10 → felt 49% / 57%** (dataset CSV / doc
  02b) — the worst forest rest pressure; wave-1 comp-100 already knocked it down.
- **Spawn points ×9** (Spiders01/02, Wolves01, Hobgoblins01/02, Trolls01/02, Boars01/02)
  — all ship `SpawnPtDeactivate`d, re-arm 1 day after the area clears (doc 02b; respawn
  loop). Tables: spiders BDSPIDGI/HU, wolves, hobgoblins, trolls, boars.
- **Loot:** Glimmer of Hope +2 (BDBLUN08).

### BD7110 — Troll Shamaness lair (sub of BD7100)
- **16 trolls + boss.** TROLL01 ×5, TROLSP01 ×5, TROLLGI ×3, TROLLSM ×2, **BDTROLSH
  Troll Shamaness** (56 HP / **2000**). 22,800 total. Empty area script → pure set-piece.
- **Rest:** day 1 / night 1 → felt 8% (vanilla day8/night8 = 49%), table `TROLL01|TROLLSM`.
- **Loot:** Locket of Embracing (BDAMUL07), Wand of Fear (WAND02), Medium Shield +1
  (SHLD04), Bloodstone Ring.

---

## TIER 2 — Forest of Wyrms (BD7200 + BD7210 + BD7220 + BD7230) — OPTIONAL loop

### BD7200 — overland (wyvern / bugbear / displacer field)
- **47 placed hostiles, 40,235 kill-XP (÷6 ≈ 6,706/char).**
  - **Wyverns ×13:** BDWYVR01 ×5 (1400), BDWYVR02 baby ×4 (450), BDWYVR03 greater ×4
    (2000).
  - **Bugbears ×11** (BDBUGB01-20, 175-650), **Displacers ×7** (BDDISPBE ×6 + pack lord),
    **Phase spiders ×5** (SPIDPH ×4 1400 + SPIDPHAS astral ×1 **4000**), **Dire wolves
    ×5** (125), **Small spiders ×5** (65), **Hill giant ×1** (BDGIANHI, **3000**).
- **Rest:** day 1 / night 1 → felt 8% (vanilla day6/night7 = 39%/44%), table
  `BDWOLFDI|BDBOAR02|BDSPIDGI|BDBEARBR`. **Spawn points ×4** (Wolves/Boars/Wyverns/
  Spiders), respawn loop. Neutral: Coogan (NPC), mountain lion, fauna.

### BD7210 — Morentherene's cavern **[WISHLIST ITEM 16]**
- **1 actor: `BDMORENT` Morentherene**, young green dragon — 112 HP / **13,000**,
  **EA=NEUTRAL, asleep.** Script (doc 02b) lets you **sneak past or wake it**; area is
  **NOREST** until it dies. On wake at Hard/Hardest it summons off-screen reinforcements
  (Greater Wyverns ×2/3/5, Young Green Dragons ×0/1/2). Already the model optional,
  difficulty-scaling set-piece.
- **Loot (hoard):** Sable Cloak (BDCLCK02) + gems (Star Sapphire, Diamond, Emerald,
  King's Tears).

### BD7220 — Bugbear cave / Greater Shadow (sub of BD7200)
- **36 placed bugbears, 11,810 kill-XP** (BDBUGB01-21) + **`BDSNORGA` Snorgash** (chief,
  975) + BDBUGB21 elder (975). **Difficulty-scaled: 36 = Insane upper bound; live ≈ 24 on
  Core** (doc 02b). Neutral: **`BDSHADOW` Greater Shadow** (72 HP / 3000, EA=NEUTRAL —
  only active during the `bdmisc01` "spectacles" quest SDD118).
- **Rest:** day 1 / night 1 → felt 8% (vanilla day6/night8 = 39%/49%), table
  `BDBUGB01|BDBUGB10|BDBUGB20`. **Scripted:** cultist ambush `bdcultx2` at the BD7230
  transition (`BD7220.baf`).
- **Loot:** mostly mundane (Halberd, Bastard Sword, healing/absorption/clarity potions).

### BD7230 — Bhaalist cult temple **[WISHLIST ITEM 15 — the "Cyric/half-dragon" temple]**
Pure set-piece dungeon (58 actors). Wishlist item 15 ("strip filler → one big fight vs.
Ziatar + strong companions of hers") targets THIS area. Note the data shape: **Ziatar is
currently a minor parley NPC, and the marquee fight is the Neothelid, not her.**

**Forced / triggered HOSTILES (18, 60,510 kill-XP; ÷6 ≈ 10,085/char):**
| Creature | resref | HP / kill-XP | note |
|---|---|---|---|
| **Neothelid** | `BDNEOTHE` | 128 / **20,000** | marquee monster; eats a cultist in a cutscene |
| **Darskhelin** | `BDDARSKH` | 68 / 9,000 | boss |
| **Shadow Aspect** | `BDASHIRU` | 96 / 6,000 | boss |
| Umber Hulks | `UMBHUL01` | 74 / 4,000 | ×2 |
| Invisible Stalkers | `STALKE_` | 64 / 3,000 | ×3 |
| Enthralled Cultists | `BDCULT41-44` | 40-90 / 1,400-2,000 | ×4 (Neothelid room) |
| Mutated Crawlers | `BDMCARRI` | 42 / 650 | ×3 |
| Worgs | `WORG` | 26 / 120 | ×3 |

**PARLEY-able NEUTRAL cast (~40, the "filler" item 15 flags):** **`BDZIATAR` Ziatar**
(half-dragon, 81 HP / **3,000**, EA=NEUTRAL), **`BDAKANNA` Akanna** (66 / 4,000, summons
1-2 Aerial Servants `bdservsu`), Madele, Keherrem, and ~24 rank cultists (BDCULT01-30,
BDCULTD1-4, 420-2,000) + Cultist Mages (BDCULT27/28, 2,000) + Enforcers (BDCULT25/26,
1,400). Quest item **Ziatar's Journal `BDMISC48`** gates a peaceful route (`BD7230.baf:48`).
- **Scripted:** `BD7230AM` — after the Neothelid dies, **6 `cultist_ambushN` go invisible
  (`bdinvis`) and JumpToPoint to ambush** the party (verified `BD7230AM.baf:1-60`).
- **Rest:** day 1 / night 1 → felt 8% (vanilla day6/night7 = 39%/44%), table
  `BDSPIDGI|BDCRAWMU`.
- **Loot:** **Fractal Blade +3 (BDSW1H14)** — the signature reward; Dagger +1, Onyx Ring,
  Fire-Giant-Strength/Freedom potions, Mage Armor / Obscuring Mist scrolls.

---

## TIER 3 — Boareskyr Bridge (BD2000 + BD2010 + BD2100) — the arc climax

### BD2000 — the bridge: trivial placed trash, big SCRIPTED battle
- **Placed hostiles: only 34, 2,810 kill-XP** — all chaff: Hobgoblin Scouts ×8 (35),
  Goblins ×14 (BDGOB01/05/06/07, 15-200), Beetles ×5 (120), Worgs ×2, 1 Wight (BDYMORI,
  175), 1 Goblin Witch Doctor (BDGOB04, 500). **The placed layer is a rounding error.**
- **The real combat is the SCRIPTED crusader battle** — a large **EA=NEUTRAL** cast that
  turns hostile at the bridge resolution (`bd_plot 293`, `BD2000.baf:890+`;
  `"…time for Bridgefort to strike back!"` `:577`). Named neutrals-turned-boss:

  | Named | resref | HP / XP | | Named | resref | HP / XP |
  |---|---|---|---|---|---|---|
  | **Oloneiros** | `BDOLONEI` | 52 / **5,000** | | Vichand | `BDVICHAN` | 36 / 1,400 |
  | The Barghest | `BDBARGHE` | 120 / 3,000 | | Kharm | `BDKHARM` | 90 / 1,400 |
  | Hormorn | `BDHORMOR` | 84 / 3,000 | | Delgar Munsch | `BDMUNSCH` | 96 / 975 |
  | 2× chained Troll | `BDTROLL1/2` | 64 / 1,400 ea | | Tharantis | `BDTHARAN` | 80 / 650 |

  …plus **ranks:** ~40 crusaders/guards/mercenaries (BDCRUS22-98, BDCRUR26-29, BDCRUE31/34,
  BDGUAR20-24, BDCRU100-116, 275-650 ea) and Bridgefort defenders (BDBFOR10-16, 275-975).
  **Khalid** (yes, THE Khalid) leads the Bridgefort side (`BD2000.baf:577`). 15× BDTARGET
  = script dummies (ignore).
- **Quest structure (journal strings, `BD2000.baf`):** infiltrate → either **lower the
  drawbridge for the crusade** ("Down With the Drawbridge", Kharm's offer) OR **negotiate
  Bridgefort's surrender / defense** ("The Desperate Defenders": Wynan Hess, smith Jegg
  Hillcarver destroys the supplies). Scripted XP: `AddexperienceParty(6000)` +
  `AddXPObject(Player1..6,3000)` (`BD2000.baf`).
- **Rest:** day 1 / night 1 → felt 8% (vanilla day3/night7 = 22%/44%), table
  `BDWOLF|BDWOLFDI|BDBEARBL|BEARBR|BDBANDIT`. **Spawn points ×4** all `en=0` (Wolves/
  Beetles/Spiders/Bears, max 6).
- **Loot:** The Troll-Tender's Journal (BDMISC64), Arcane Scroll of Impactful Doom
  (BDSCRL02), Short Sword +1.

### BD2010 — goblin warren (sub of BD2000)
- **36 goblins, 1,505 kill-XP** — BDGOB07 sharpshooter ×12 (30), BDGOB02 warrior ×9 (15),
  BDGOB01 archer ×9 (15), BDGOB08 ×3 (30), **Chieftain BDGOB03** (250), **Witch Doctor
  BDGOB04** (500), 1 wild dog. Pure low-tier warband; diff 200 rest table `BDBOAR02|
  BDWOLFDI|JELLYGR|BDBEARBR`.
- **Loot:** **Circlet of Lost Souls (BDHELM16)**, Potion of Clarity.

### BD2100 — Bridgefort interior (quest / NPC hub)
- **1 hostile:** `BDWRAI01` Wraith (48 HP / 2,000). Otherwise a **dialogue hub** of ~35
  NEUTRAL NPCs: **Frair Tajik** (BDFRAIR, 3,000), Wynan Hess (2,000), smith Jegg
  Hillcarver, Junia, Zari/Rayler/Lexa/Herdrin/Kendra (BDBF1-5), Roark, Adirran, + refugees
  (BDREFG*). **No rest** (disabled).
- **Companion recruits (this arc):** **Neera** (`neera7`, scripted spawn — dataset;
  `BD2100.baf`) and **Voghiln** (referenced `BD2000.baf`; camp clone in BD7100). M'Khiin &
  Glint are NOT new here — their camp clones (`BDMKHI7`, `GLINT7`) sit in **BD1000**
  (prior Coast Way arc; placement scan). Rasaad is at the BD1000 camp per comp210.

---

## Rest / spawn summary (current dev = post-wave-1; vanilla in parens)

| Area | felt day/night now | vanilla | max | diff | notable rest drop |
|---|---|---|---:|---:|---|
| BD7100 | 8% / 15% | 49% / 57% | 3 | 2 | TROLL01 (1400) |
| BD7110 | 8% / 8% | 49% / 49% | 3 | 200 | trolls |
| BD7200 | 8% / 8% | 39% / 44% | 3 | 200 | — |
| BD7220 | 8% / 8% | 39% / 49% | 3 | 2 | bugbears |
| BD7230 | 8% / 8% | 39% / 44% | 3 | 200 | — |
| BD2000 | 8% / 8% | 22% / 44% | 3 | 2 | — |
| BD2010 | 8% / 8% | 22% / 44% | 3 | 200 | — |
| BD7210 / BD2100 | NOREST / none | — | — | — | — |

Wave-1 comp-100 has already swept every rest header in this arc. Spawn points across
BD7100/7200 are all deactivate-on-load + re-arm-1-day-after-clear (doc 02b); none stream.

## Quest XP & the banned-creature check

- **Scripted awards (per char):** BD7100 **+10,000** (Ch-9 transition), BD2000 **+6,000 +
  3,000** (bridge). Big kill: **Neothelid 20,000** (kill-XP, party-divided). Everything
  else quest-side is **dialogue-layer** (`docs/research/03`): the M'Khiin line `BDMKHIIJ`
  12k, ogre-tribe `BDMURS` 12k, Boareskyr turn-ins ~6k. **The 32k dragon-spirit is next
  arc** (see Correction 2).
- **Banned no-save/no-roll creatures (wishlist 2026-07-08): this arc is CLEAN.** No
  `BDSHSOUL` (shadowed soul), `BDBONBAT` (bone bat), or `BDUNSLGU` (Unsleeping Guardian)
  in any placed-actor list OR rest/spawn table across BD7100-7230 / BD2000-2100. They
  first appear in the **next** arc (BDUNSLGU in BD7310 shadow tomb; BDSHSOUL/BDBONBAT in
  BD7400 Bloodbark Grove).

## Wishlist content already on the map

- **Item 15 (Cyric/Bhaal temple → one Ziatar fight, strip filler):** = **BD7230**. Data
  reality: 18 forced hostiles (Neothelid-led, 60.5k) + **~40 parley-able cultists** (the
  filler) around **Ziatar** — who is presently a 3,000-XP EA=NEUTRAL parley NPC, *not* the
  climax (the Neothelid is). Elevating Ziatar + cutting the cultist mass is the shape.
- **Item 16 (Morentherene scarier / optional / difficulty-scaling):** = **BD7210**,
  already optional (WMP side-loop), NOREST-locked, difficulty-summons, 13,000. The elevate
  target.
- **Cross-chapter treasure-choice component:** cut content here would route Fractal Blade
  +3 (BD7230), Circlet of Lost Souls (BD2010), Wand of Fear / Locket of Embracing (BD7110),
  Sable Cloak (BD7210), Troll-Tender's Journal / Impactful-Doom scroll (BD2000).

## Flagged uncertain
1. BD7100/7200/7220 difficulty-suffix scaling — placed counts are the **Insane upper
   bound**; live Core counts are lower (quantified only for BD7220 ≈24 in doc 02b).
2. Boareskyr crusader battle — the neutral→hostile roster (~90 actors) turns via plot;
   exact fight size depends on the drawbridge/surrender branch chosen (not summed here).
3. Voghiln's exact recruit trigger — referenced in BD2000, camp clone in BD7100; his
   first-recruit dialog/area not pinned to a line (recruits during the Boareskyr beat).
4. M'Khiin dialogue at Boareskyr (`BD221LT`) is banter, not recruitment (she joins in the
   prior Coast Way arc, BDMKHI7 in BD1000) — confirm no downstream reads if that camp is reworked.
5. `bd_plot` values 200-239 (Troll Claw Woods → Forest of Wyrms) set few flags — the
   Forest-of-Wyrms detour is largely plot-optional; only Boareskyr (240-293) is on-rail.

## Candidate questions for the design round (data-framed, no decisions)

1. **BD7100 is the arc's trash sink AND the Ch-9 camp.** 104 placed hostiles (32 trolls,
   16 hobgoblins, 15 spiders, 13 orcs, 10 ogres, 8 beetles) = 79k, the densest area — but
   any cut has to leave ~24 neutral camp NPCs standing. Same "trash wrapped around a
   safe-zone" problem as the coastway dig site.
2. **The whole Forest of Wyrms (BD7200+7210+7220+7230) is skippable** (WMP: bd7100→bd2000
   direct). ~101 placed hostiles + Morentherene + the cult temple sit on an *optional*
   loop — worth noting before deciding how hard to invest in it.
3. **Item 15's target (BD7230) has an inverted climax:** the "big fight" is the Neothelid
   (20k forced), while Ziatar is a 3k parley NPC buried among ~40 neutral cultists. The
   filler-to-strip is the cultist mass; the "make it Ziatar" ask means promoting her.
4. **Boareskyr's difficulty comes entirely from script, not placed actors** — 34 trivial
   placed mobs (2.8k) vs. a ~90-actor scripted crusader battle with 6+ named bosses (up to
   Oloneiros 5k). It's a set-piece, not a trash field; "cut trash" barely applies.
5. **Two low-tier warbands are pure filler:** BD2010 (36 goblins / 1.5k) and BD7100's
   hobgoblin/orc/beetle tail (~37 mobs / low XP) — the clearest delete-on-sight pockets.
6. **Difficulty spikes to flag:** BD7100 gargantuan spiders ×4 (3k ea) + sword spiders ×3;
   BD7200 astral phase spider (4k) + hill giant (3k); BD7230 umber hulks / stalkers; the
   Boareskyr named-boss stack. These are the "few fun/hard enemies" candidates.
7. **Rest pressure is already handled** — wave-1 dropped every header to felt 8-15%; no
   further rest work needed this arc unless a specific area wants zero.
8. **Arc XP shape (per char, thorough):** ~37k placed kill-XP total (÷6 for party;
   concentrated in BD7100 trolls + BD7230 set-piece) + 10k/6k/3k scripted + dialogue layer
   (M'Khiin 12k, ogres 12k, Boareskyr ~6k). Cutting BD7100/BD7200/BD2010 trash removes
   little per-char; the compensation model from the coastway pass (chunk onto a boss/quest)
   transfers directly — candidate carriers: the Neothelid kill or the Boareskyr resolution.
