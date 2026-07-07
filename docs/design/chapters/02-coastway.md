# Chapter Pass — Coast Way tier (BD1000 / BD1100 / BD1200 / BD7000)

**Status: DESIGN OPEN — sparring round 1 pending.** Inputs: the user's parked notes
(`02-coastway-notes.md`, 2026-07-06) mapped onto the verified census
(`docs/research/12-coastway-census.md`, 2026-07-07). Nothing below is implemented.
Per-item state is marked **[USER NOTE]** (his parked direction, not yet sparred in
detail) or **[OPEN]** (needs a round-1 decision).

## 0. What the census corrects

- **There is no separate "first camp" area.** The Flaming Fist Encampment IS
  BD1000 (Coast Way Crossing) — companions are relocated into it at
  `BD1000.baf:149-283`. "Put Rasaad in the camp" therefore means: move his spawn
  block to BD1000.
- The "vampire hunters area" = **BD7000 Coast Way Forest** (worldmap node), also
  hosting the 22-orc warband, a random-encounter hook — and **a Skie sub-quest**
  (regions `Sddskie1`/`Skie_escape`).
- The dwarf dungeon's undead are **100% pre-placed actors, zero scripted spawns**
  — a cut is pure ARE surgery, no script seams to respect (boss/quest scripts are
  separate and untouched).

## 1. Coast Way Crossing (BD1000) — [USER NOTE, mechanics verified]

- **West spider group removed**: the 8 placed NW spiders (SPIDPH ×3, BDSPIDGA ×2,
  SPIDGI ×2, SPIDHU ×1 at X≈467-644/Y≈1459-1594). Sub-question [OPEN]: also remove
  the two web traps + the disabled `Spiders02` re-arm point there, or leave the
  point (respawns a wandering pack 1 day after clear)?
- **Magic wall removed** from the bridge fight: drop `BDCUT14.baf:397-403`
  (bdwforce cast + SPFLESHS VFX + `AmbientActivate("force_wall")` +
  `CloseDoor("force_wall_door")`).
- **Fight-interrupt timer ~150%**: vanilla `THREE_ROUNDS`
  (`SetGlobalTimer("bd_caelar_timer","bd1000",...)`, `BDCUT14.baf:417`). 150% of 3
  = 4.5 — [OPEN] pick FOUR_ROUNDS (~133%) or FIVE_ROUNDS (~167%).

## 2. BD7000 removal + Rasaad to camp — [USER NOTE, surface verified]

- **Rasaad**: his spawn block (`BD7000.baf:20-78`) is self-contained (Chapter==8
  gate, MoveGlobal-or-Create, dialog bdrasaad) — relocate to BD1000. [OPEN] his camp
  spot (the companion camp rows sit at `BD1000.baf:149-283`; give him one of the
  camp positions).
- **Area removal shape** [OPEN]: BD7000 is a worldmap node — "removal" = never
  reveal/strip the worldmap entry vs. leave it reachable but gutted. Needs the
  standalone-vs-EET reveal mechanics checked at implementation.
- **Item re-homing** (cookbook #12): the one true unique is **BDDAGG03 "Gemblade"**;
  Tsolak's conditional `ring09` (Ring of Free Action) only drops on a clean kill;
  plus minor treasures (SODTRE08/09, BDMISC63 — name unresolved). [OPEN] where they
  land (a BD1000 container? a crew/NPC?). Carried gear of Tsolak/Isabella/Ikros
  still unverified.
- **Skie sub-quest lives here** (`Sddskie1`/`Skie_escape` regions) — [OPEN, gates
  the removal]: check what it is and whether it moves or dies, coordinated with the
  Skie-playable plan.

## 3. Dwarven dig site (BD1100/BD1200) — [USER NOTE: "way too many"; density OPEN]

Census: **85 hostiles upper** (59 undead + 26 dig-monsters), **~118 lower** (nearly
all undead; headline stacks BDBONBAT ×17, BDDEAD01 ×10, BDSHSOUL ×10, skeleton-guard
families ×~30). All placed; quest content (Deepvein, Semahl, the clerics, Coldhearth
+ phylactery + arena wall, 22,000 XP clean-kill award) is script-side and untouched
by an actor cut.

[OPEN] round-1 decisions:
1. Target density per level (e.g. "cut to roughly a third", or per-group curation).
2. Composition: keep the flavor stacks (bone bats? shadowed souls?) or thin
   uniformly; the Unsleeping Guardian miniboss stays?
3. The dig-monsters on L1 (carrion crawlers/umber hulks/otyughs) — same cut or
   different treatment?
4. XP ledger consequence: the garrison is a big chunk of tier XP — ledger row after
   the cut is sized (delivery per the §7 prologue rule if compensation is wanted).

## 4. Backtracking without EET — [USER NOTE, global lever]

Parity with EET's backtracking on standalone. Global design (not this tier alone);
parked here until its own pass.

## OPEN — sparring round 1 (the ball is with the user)

1. §1 spider sub-question (traps + re-arm point) + timer 4 vs 5 rounds.
2. §2 removal shape, Rasaad's camp spot, loot landing spot, and the Skie sub-quest
   disposition.
3. §3 the four dungeon-density decisions.
4. Confirm §0's "camp = BD1000" reading matches what you meant by "the camp".
