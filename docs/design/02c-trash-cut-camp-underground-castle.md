# Design 02c — Trash-Cut Proposal: Boareskyr Bridge → Coalition Camp → Underground River → Dragonspear Castle → Avernus

Status: **proposal / not implemented** (markdown only; WeiDU tail-mod comes after sign-off).
Date: 2026-06-21. Scope: BD2xxx (bridge), BD3xxx (camp), BD4xxx (castle/Avernus), BD5xxx (underground
river/warrens), BD6xxx (sewers/ambush).
Sources: inventory `docs/research/02c-encounters-camp-underground-castle.md` (re-verified against the
**live override** `BD*.ARE`, 2026-06-21 — placed-actor counts identical to pristine), rest dataset
`docs/research/sod_areas_dataset.csv`. Related design: rest-ambush `01-rest-ambush-design.md`,
XP `03-xp-reweight.md`, creature-softening `04-creature-softening.md`.

## Framing & conventions

- **Counts are placed-actor baselines = the fixed pre-placed enemy population in each `.are`.** These
  are **exact and difficulty-independent** — identical on Story…Insane — so a placed-actor cut is a
  clean reduction that applies as-is on the user's **Difficulty 5 (Legacy of Bhaal / "Insane")** game.
  This region's placed-enemy baseline is **460** (excl. corpses, the 344 coalition allies, ambient
  animals, objects, named NPCs). This is the reliable backbone of the proposal.
- **Scripted waves are a separate, difficulty-gated lever.** SoD's battle scripts branch on difficulty
  (`Difficulty(HARDEST)`, `DifficultyGT(NORMAL)` …); the inventory's scripted totals **sum across all
  branches and therefore over-count** — the engine fires only one branch per event (e.g. BD5000's
  `CreateCreatureEffect(…,"SPMONSUM")` monster wave is ~3 bears+3 phase-spiders+2 snakes per trigger,
  not the 9+9+6 the all-branch sum shows). On Insane the *hardest* branch fires, so **NOP-ing the
  HARD/INSANE reinforcement branches is doubly effective for this user.** Scripted cuts below name the
  specific response blocks.
- **The rest tables** for BD5000/BD5100/BD5110 (the random rest-ambush spawns) are handled by the
  day/night-% and `max`/`difficulty` levers in **Design 01**, not here.
- **Implementation** = `COPY_EXISTING` each `BD*.ARE`, remove targeted actor-table entries (or flag
  never-spawn), reversible backup. Scripted-wave removal = `EXTEND_TOP`/`COMPILE` to NOP the relevant
  `CreateCreature*` response blocks, reversible. No `.dlg` edits. "Make-meaningful" upgrades that buff a
  CRE into a boss are a CRE/`.bcs` touch, flagged per case.
- **XP caveat:** cutting ~215 trash mobs removes encounter XP. Compensate via the big-quest reweight in
  `03-xp-reweight.md` (Coalition-Camp defense, castle assault, river-traversal quest completions).
- **"Keep" picks are category-level**; exact elite-variant CRE selection to be confirmed against stats
  at implementation (overlaps with `04-creature-softening.md`).

## Preserve — set-pieces, do NOT cut (per directive)

These are the region's authored battles. Trimming targets the trash *around* them, never the battles:

- **BD3000 Coalition Camp siege** — the climax (scripted `bdwave*` assault waves + your ~214-strong
  coalition army). See "Make-meaningful #1" for a *quality* redesign that is **not** a cut.
- **BD4000 Dragonspear Castle gate assault** — 71 placed crusaders + reinforcement waves. See
  "Make-meaningful #2".
- **BD2000 Boareskyr Bridge battle** — the crusader half (37 placed + ~37 scripted: `bdcrus*`,
  `bdcrubb*`, `bdguar2x`, Front_Attackers) + named bosses The Barghest (BDBARGHE) & Oloneiros
  (BDOLONEI) + fire-elemental phase. **Only the goblin/hobgoblin raid sharing the map is cut** (below).
- **BD4300 Castle Basement** — `bd_mdd905z` two-wave dungeon (crusader elites + insane cultists).
- **BD4700 Caelar Argent** — boss confrontation (Caelar `bdcaela3` + her devils `bdcut57*` + crusaders).
- **BD6100 The Ambush** — the scripted *defeat* finale (`bdfinal1-5` Shadow Thieves, designed to be
  lost; leads into BG2's opening). Never touch.

---

## Part 1 — Boareskyr Bridge region (BD2xxx)

### BD2000 — Boareskyr Bridge: goblin/hobgoblin raid — **33 → 10 (−70%)**
The bridge **battle** (crusaders + bosses) is preserved. A separate **goblinoid warband** is placed on
the map as a skirmish. Current monster placed: `bdhobg02`×8 (scout), `bdgob01`×5 (archer), `bearbr`×3,
`bdgob07`×3 (elite archer), `bdgob05`×2 (worg rider), `bdhobg05`×2 (veteran), `bdworg`×2,
`bdhobg03`×2 (elite archer), `bdtroll1/2`×2, + leaders `bdgob06` (raid leader), `bdhobg01` (captain),
`bdgob04` (shaman), `bdhobg04` (priest).
- **KEEP (10):** `bdgob06`×1 (raid leader), `bdhobg01`×1 (captain), `bdgob04`×1 (shaman),
  `bdhobg02`×3 (scouts), `bdgob01`×1, `bdgob07`×1, `bdworg`×1, `bdtroll1`×1.
- **REMOVE (23):** `bdhobg02`×5, `bdgob01`×4, `bearbr`×3, `bdgob07`×2, `bdgob05`×2, `bdhobg05`×2,
  `bdworg`×1, `bdhobg03`×2, `bdtroll2`×1, `bdhobg04`×1 (priest).
- **Judgment call:** confirm the goblin raid is a free-cut skirmish and not narratively load-bearing
  for the bridge approach. If it is tied to a "help repel the raid" beat, keep the leaders + a token
  squad (the KEEP set already does this).

### BD2010 — Bridge approach goblin camp — **35 → 10 (−71%)**  ★ make-meaningful (chieftain warband)
Pure goblin field, no story. Current: `bdgob07`×12 (elite archer), `bdgob02`×9 (warrior),
`bdgob01`×9 (archer), `bdgob08`×3 (elite warrior), `bdgob03`×1 (chieftain), `bdgob04`×1 (shaman).
- **Upgrade, don't just delete:** make it the **chieftain's last stand** — a tight, real warband
  around `bdgob03` (buff to a named chieftain) + `bdgob04` shaman support.
- **KEEP (10):** `bdgob03`×1 (chieftain, buff), `bdgob04`×1 (shaman), `bdgob08`×2 (elite warriors,
  bodyguard), `bdgob07`×3 (elite archers), `bdgob02`×2, `bdgob01`×1.
- **REMOVE (25):** `bdgob07`×9, `bdgob02`×7, `bdgob01`×8, `bdgob08`×1.
- Rest header: 22/44% felt @max3 diff200 — soften per Design 01.

*(BD2100 Bridgefort interior = garrison/non-combat, 1 wraith — leave. BD2000 bridge battle preserved.)*

---

## Part 2 — Coalition Camp (BD3000)  — PRESERVE + make-meaningful #1

**No trash cut** (placed enemies = 5 rats only; the rest is your 214-strong coalition army + the siege
waves). The siege is the emotional climax of SoD.

### ★ Make-meaningful #1 — BD3000 Coalition Camp siege (quality redesign, not a cut)
**Problem:** the climax is currently delivered as **anonymous timed spam** — `bd_battle_failed` /
`GlobalTimerExpired` fire generic `bdwave21-54` waves (~14-16 identical crusaders per wave, escalating
with `DifficultyGT`/`Difficulty(HARDEST)`), plus `bdcatapu`×10 bombardment. It reads as a spawn timer,
not a battle.
**Upgrade:**
- Replace the anonymous wave loop with **2-3 distinct, named crusade assaults** — e.g. a vanguard
  champion leading a focused breach, a flanking cavalry push, then a final commander — each a
  hand-placed pack with a leader CRE, instead of `bdwave` filler tiers.
- Keep the catapult bombardment beat (it's good tension), but tie its end to killing a **siege-master**
  rather than a timer.
- Net on-screen crusaders can *drop* (fewer, tougher, named) while the battle reads bigger.
- Implementation: `.bcs` rework of the `bd_battle*` blocks + a few new/buffed leader CREs. Larger
  effort than a cut — flag as a stretch goal separate from the trash pass.

---

## Part 3 — Dragonspear Castle & Avernus (BD4xxx)

### BD4000 / BD4300 / BD4700 — PRESERVE (set-pieces). See make-meaningful #2 for BD4000.

### ★ Make-meaningful #2 — BD4000 castle gate assault (quality redesign, light trim)
**Problem:** ~71 placed crusaders man the walls + `bd_outer_gate_explosion` reinforcement waves —
a 100-body zerg on a single gate. **Upgrade into a breach fight:** a defended wall section, a
battering-ram beat, and a named **gate commander** as the kill-target, with the wall-standers thinned
to a credible garrison (a *light* ~30-40% trim of the identical `bdcru*`/`bdcruml` milling minions is
acceptable here since they're filler around the set-piece, but the assault itself stays). Flag: this is
a design upgrade, not part of the core ~70% trash number.

### BD4400 — Avernus (hellscape) — **17 → 6 (−65%)**
Current placed: `bdlemure`×5, `bdimp`×3, `bdlemurd`×3, `bdcrus50`×1 (elite), `bdcrval`×1 (sergeant),
`bdcrus5d/6d/7d/8d`×1 each (crusader elites). Plus scripted `bddevil1/2`×1 (keep — they're the
characterful greater devils).
- **KEEP (6):** `bdcrval`×1 (sergeant, leader), `bdcrus50`×1 (elite), `bdlemure`×2, `bdimp`×1,
  `bdlemurd`×1. + scripted `bddevil1/2` (unchanged).
- **REMOVE (11):** `bdlemure`×3, `bdimp`×2, `bdlemurd`×2, `bdcrus5d/6d/7d/8d`×1 each.
- Rest header: 34/34% felt @max3 diff200 — soften per Design 01.

### BD4500 — Avernus Bridge (aftermath) — **4 → 4 (leave)**
Only `bdlemure`×3 + `bdimp`×1; already light, an aftermath corridor. No cut (or trivial −2 if strict).
*(BD4601 = `bdlemure`×2/`bdimp`×1 scripted — leave. BD4600/BD4700 see preserve.)*

---

## Part 4 — Underground River (BD5xxx) — the biggest trash field

### BD5000 — Underground River — **48 placed → 15 (−69%)** + thin scripted waves  ★ make-meaningful #3a
Crusade-occupied river with a monster zoo. Current placed: `bdwyvr03`×4 (greater wyvern), `orc01_`×4,
`bdogref`×3 + `bdogrem`×2 (ogres), `bdcrsit1`×3 (sitting crusaders), `spidhu`×3, `skelded`×3, `bdrat`×3,
`bdspidga`×2, `bdcrus97/94`×2 each, `bdguar50-54`×1 (gate crusaders), `bdcrus86/99/93/98/96`×1,
`bdentran`×1 (**Cyclops**), `bdwyvr02`×1 (baby), `bdwyvr01`×1 (wyvern), `spidsw`×1, `bearbr/bearbl/bearca`×1.
- **★ Signature peak:** anchor the area on **`bdentran` the Cyclops** (buff to a real gate-guardian
  mini-boss) flanked by a wyvern pair — so the long river has a memorable beat.
- **KEEP (15):** `bdentran`×1 (Cyclops mini-boss), `bdwyvr03`×2 (greater wyverns), `bdwyvr01`×1,
  `bdogref`×2 (ogres), `orc01_`×2, `bdspidga`×1, `spidhu`×1, `bearca`×1 (cave bear), + crusade gate
  pocket `bdguar50`×1 + `bdguar53`×1 (archer) + `bdcrus97`×1.
- **REMOVE (33):** `orc01_`×2, `bdogref`×1, `bdogrem`×2, `bdcrsit1`×3, `spidhu`×2, `skelded`×3,
  `bdrat`×3, `bdspidga`×1, `bdcrus97`×1, `bdcrus94`×2, `bdguar51/52/54`×1, `bdcrus86/99/93/98/96`×1,
  `bdwyvr02`×1 (baby), `spidsw`×1, `bearbr`×1, `bearbl`×1.
- **Scripted:** thin the `CreateCreatureEffect(…,"SPMONSUM")` wandering-monster waves (lines ~96-157 of
  `BD5000.baf`) to a single small branch; drop the `Difficulty(HARDEST)` crusader gate-attack branch
  (`bdguar55-60` + `bdcru103/104`). On Insane this is the doubly-effective lever.

### BD5100 — Underground River warrens — **69 placed → 20 (−71%)** + thin scripted  ★ make-meaningful #3b
Myconid/treant infestation + crusader occupation; the region's worst rest area (max6). Current placed:
`bdtreant`×7 (dark treant), `bdmycrd`×5 (myconid red), `bdspidga`×5 (gargantuan spider), `bdmycbl`×4
(myconid blue), `bdwe1str`×3 (water elemental), `bdshamb`×3 (shambling mound), crusaders
(`bdrcrus`×3, `bdcrusm5`×3, `bdcrus93`×3, `bdcruaf5`×2, `bdcrus91/97/89`×2, patrols `bdcrus80-85`×1
each, workers, casters `bdcrucm7`/`bdcrumf7`/`bdcrus92`, door guards `bdguar5a/5b`), `bdankh01`×1.
- **★ Signature peak:** promote one **`bdmycrd` → Myconid Sovereign** and build a real colony fight
  around it (red+blue myconid circle + spore tactics) — the thematic heart of the warrens.
- **KEEP (20):** `bdmycrd`×1 (Sovereign, buff) + `bdmycrd`×2 + `bdmycbl`×2 (colony), `bdtreant`×2
  (dark treants), `bdspidga`×2, `bdshamb`×1, `bdwe1str`×1, `bdankh01`×1, + one crusader patrol pocket:
  `bdcrus80`×1 + `bdcrus83`×1 (patrol), `bdguar5a/5b`×2 (door guards), `bdcrucm7`×1 (cleric) +
  `bdcrumf7`×1 (mage — the real threat).
- **REMOVE (49):** `bdtreant`×5, `bdmycrd`×2, `bdspidga`×3, `bdmycbl`×2, `bdwe1str`×2, `bdshamb`×2,
  all the redundant crusader rank-and-file (`bdrcrus`×3, `bdcrusm5`×3, `bdcrus93`×3, `bdcruaf5`×2,
  `bdcrus91/97/89/87/88`, `bdcrus81/82/84/85`, `bdcrus90/92/94/95/96/98/99`, `bdcru100/101`, recruits).
- **Scripted:** drop the `bd_warrens_escape_hard` / `bd_sdd705_turin_hard` `Difficulty(HARDEST)`
  crusader reinforcement branches (`bdcru104-123`); keep one small escape pack.

### BD5110 — Underground River, undead pocket — **16 → 5 (−69%)**
Current: `bdshad04`×10 (shadow), `bdwrai02`×4 (wraith), `bdshadgr`×2 (greater shadow). Also the game's
**worst rest area** (64/80% felt) — primary Design 01 target.
- **KEEP (5):** `bdshadgr`×2 (greater shadows, the threat), `bdwrai02`×1, `bdshad04`×2.
- **REMOVE (11):** `bdshad04`×8, `bdwrai02`×3.

### BD5200 — The Warrens (crusader muster/barracks) — **46 → 14 (−70%)**
A crusade staging hall the player infiltrates: ~43 `bdcru*`/`bdcrus*` (labelled generic "Actor NN")
+ training archers (`bdcrus93`/`bdcrus97`/`bdcru117`/`bdcrur31` + `bdtarget` dummies) + `bdpolvi`
(Crusader Priest Polvi, named) + `bdslug`.
- **KEEP (14):** `bdpolvi`×1 (named priest, the encounter's face), a tight guard contingent —
  `bdcru103`×2, `bdcrus99`×2, `bdcrus98`×2, `bdcrus91`×2, `bdcru102`×1, `bdcru104`×1, `bdcru105`×1,
  `bdcrus97`×1 (training archer) + `bdslug`×1.
- **REMOVE (32):** the bulk of the duplicated "Actor NN" crowd (`bdcrus93`×5, `bdcrus95/96`×2 each,
  `bdcru106`×2, `bdcru100`×2, `bdcru103`×3 [keep 2 → drop 1+the monster-tagged dup], `bdcru109/107/108/101`,
  `bdcrus92/94`, `bdcru117`, `bdcrur31`, training-archer dups…).
- **Judgment call:** much of this crowd is **ambient muster / partly avoidable by stealth or disguise**;
  confirm whether you want a leaner *combat* barracks (this proposal) or to keep it as a populated
  backdrop and only thin the actively-hostile guards.

### BD5300 — Crypt (`BD_SDD350_JAR` quest) — **24 → 7 (−71%)**
Undead crypt. Current: `bdskgr04`×9 (skeleton archer), `bdunsen`×3 + `bdzombie`×2 (zombies),
`bdskgr01`×3 (armored skeleton), `bdshsoul`×3 (shadowed soul), `bdskgr03`×2 (bladed skeleton),
`bdskgr02`×1, `bdskgr08`×1 (skeleton warrior).
- **KEEP (7):** `bdskgr08`×1 (warrior), `bdskgr01`×2 (armored), `bdshsoul`×2 (shadowed souls, the
  threat), `bdskgr04`×2 (archers).
- **REMOVE (17):** `bdskgr04`×7, `bdunsen`×3, `bdzombie`×2, `bdskgr01`×1, `bdshsoul`×1, `bdskgr03`×2,
  `bdskgr02`×1.

---

## Part 5 — Sewers / escape (BD6xxx)

### BD6000 — Abandoned Sewers — **16 → 4 (−75%)**
Pure filler on the escape route: `bdrat`×11, `jellygr`×5 (green slime). (Plus the L#2 Bristlelick mod
NPC event — untouched.)
- **KEEP (4):** `bdrat`×3, `jellygr`×1.
- **REMOVE (12):** `bdrat`×8, `jellygr`×4.

*(BD6100 The Ambush = preserve. BD6200 Sewers Exit = empty.)*

---

## Region summary

| Sub-region | Trash before | After | Removed | % cut |
|---|---:|---:|---:|---:|
| BD2000 goblin raid (bridge battle preserved) | 33 | 10 | 23 | −70% |
| BD2010 goblin camp ★ | 35 | 10 | 25 | −71% |
| BD4400/4500 Avernus | 21 | 10 | 11 | −52% |
| BD5000 Underground River ★ | 48 | 15 | 33 | −69% |
| BD5100 warrens ★ | 69 | 20 | 49 | −71% |
| BD5110 undead pocket | 16 | 5 | 11 | −69% |
| BD5200 The Warrens muster | 46 | 14 | 32 | −70% |
| BD5300 crypt | 24 | 7 | 17 | −71% |
| BD6000 sewers | 16 | 4 | 12 | −75% |
| **Trash total (placed)** | **308** | **95** | **213** | **−69%** |

Plus scripted-wave thinning on BD5000/BD5100 (drop the HARD/INSANE reinforcement branches — doubly
effective on the user's Difficulty 5). **Set-pieces preserved:** BD3000 siege, BD4000 assault (light
filler trim only), BD2000 bridge battle, BD4300 basement, BD4700 Caelar, BD6100 ambush
(~149 placed enemies, untouched).

Region placed-enemy baseline **460 → ~247** (−46% region-wide; **−69% on the trash**, set-pieces by
design preserved). Three encounters are *upgraded* not just shrunk: BD2010 goblin chieftain, BD5000
Cyclops gate-guardian, BD5100 Myconid Sovereign — plus the two big quality redesigns (BD3000 siege,
BD4000 breach) flagged as stretch goals.

## Judgment calls for the user

1. **BD2000 goblin raid** — free-cut skirmish, or is it a scripted "repel the raid" beat? (KEEP set
   preserves the leaders + a token squad either way.)
2. **BD5200 The Warrens** — lean *combat* barracks (this proposal) vs. keep the muster as a populated
   backdrop and thin only actively-hostile guards? Depends how the infiltration plays for you.
3. **Underground River signature peaks** — Cyclops gate-guardian (BD5000) + Myconid Sovereign (BD5100):
   buff these into real mini-bosses (CRE/`.bcs` work), or just leave them as the largest survivors?
4. **Make-meaningful stretch goals** (BD3000 siege named-champion redesign, BD4000 gate-breach
   commander) are larger `.bcs` reworks separate from the trash pass — do them now, or ship the trash
   cut first and design the set-piece upgrades as a phase 2?
5. **BD4000 light filler trim** — OK to thin the identical `bdcruml` milling minions ~30-40% around the
   preserved assault, or leave the castle assault 100% intact?
6. **Aggressiveness** — these land ~70% on trash. Push deeper (toward 80%, à la BD0066/BD0130 in 02a),
   or is ~70% the ceiling so the dungeons still feel inhabited?
7. **XP** — ~213 removed mobs need the Design 03 quest-reward reweight (river traversal, camp defense)
   so progression isn't gutted.
