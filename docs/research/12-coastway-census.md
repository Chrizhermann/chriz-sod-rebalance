# 12 — Coast Way tier census (chapter-2 pass research)

Verified 2026-07-07 (research agent, read-only). Placed-actor counts parsed live from
the dev install's `override/*.are`; script citations are `research/data/sod_baf/*.baf`.
Cross-checks against `02a`/`02b` research (BD1100=85, BD1200=118 hostiles) pass.

## Area map & travel

| Resref | In-game name | Role | Reached from |
|---|---|---|---|
| **BD1000** | Coast Way Crossing | First overland area; **IS the Flaming Fist camp** (no separate camp area) + the bridge/Caelar fight | City, forced via `BDCUT10.baf:16-22` |
| BD1010 | spider/mimic cave | Sub-cave | Door on BD1000 (door id unverified) |
| **BD1100** | Dwarven dig site, upper (Coldhearth crypt) | Dig level 1 | BD1000 region `Tranbd1100` |
| **BD1200** | Dwarven dig site, lower | Level 2 + Coldhearth Lich | BD1100 `TranBD1200` ↔ `TranBD1100` |
| **BD7000** | Coast Way Forest | Vampire hunters + Tsolak + orc warband + **Rasaad** | Worldmap (`Tradeway_exit`) |
| BD2000 | Boareskyr Bridge | Next tier | Revealed post-bridge-fight (`BD1000.baf:488`) |
| BD3000 | Coalition Camp | Chapter 9 — NOT this tier | — |

Worldmap nodes this tier: BD1000/BD7000/BD2000 only (BD1010/1100/1200 are local
transitions — `worldmap.wmp` parse). **Companion relocation into BD1000 camp:
`BD1000.baf:149-283`** (every kept companion gets a camp spot).

## The bridge fight (magic wall + timer)

Trigger: region `Bd_bridge` → `bd_plot=144` → `BD1000.baf:303-315` → `BDCUT14.baf`.

- Wall: `bdcrus13` casts `bdwforce` at `[3780.1110]` (`BDCUT14.baf:397`), plus
  `CreateVisualEffect("SPFLESHS",…)` (`:398-400`), `AmbientActivate("force_wall",TRUE)`
  (`:402`), `CloseDoor("force_wall_door")` (`:403`). Wall = door + ambient VVC + VFX,
  all in BD1000.are. Removal surface = those lines.
- Timer: `SetGlobalTimer("bd_caelar_timer","bd1000",THREE_ROUNDS)` (`BDCUT14.baf:417`);
  expiry check `BD1000.baf:326-336` → `bd_plot=160` → `BDCUT15` (Caelar arrives,
  parley: spawn `:10`, `StartDialogNoSet` `:131`). Vanilla ≈ 18 s; +50% ≈ 4-5 rounds.

## Spiders (BD1000)

- **WEST group (the cut target): 8 placed spiders** at X≈467-644, Y≈1459-1594 (NW, at
  spawn-point `Spiders02` (550,1474), near `Trap_web01/02`): SPIDPH ×3, BDSPIDGA ×2,
  SPIDGI ×2, SPIDHU ×1.
- East group (kept for contrast): 9 spiders at X≈4573-4812 (`Spiders01`).
- Both wandering spawn points ship **disabled**, re-arm 1 day after clear
  (`BD1000.baf:794-805`).

## BD7000 (Coast Way Forest)

- **Rasaad**: `BD7000.baf:20-78`, Chapter==8 gate; previously-in-party →
  `MoveGlobal(...RASAAD,[2050.1500])` (`:40`), else `CreateCreature("rasaad7",…)`
  (`:69`); dialog `bdrasaad`; map note add `:15` / remove `:289`. Block is
  self-contained — independent of the vampire quest; clean to relocate.
- Vampire quest SDD123: Tsolak (`bdtsolak`) + hunters Isabella/Ikros + Koko;
  night-gated (`:141-152`); dire-wolf summons 6/11/15 by difficulty (`:165-239`).
- Skie content: regions `Sddskie1`/`Skie_escape` host a Skie sub-quest — REMOVAL
  TOUCHES SKIE (relevant to the Skie-playable plan).
- Unique loot (the victim-pile containers ~ (1200,1600)): **BDDAGG03 "Gemblade"**
  (the real re-home target); `SHLD01A` plain Small Shield (not unique);
  `SODTRE08 ×2`/`SODTRE09` treasures + `BDMISC63` (name unresolved). Tsolak drops
  `ring09` (Ring of Free Action) via `vampreg` ONLY if killed outright
  (`:100/116/132/147`) — conditional.
- Filler: 22-orc placed warband + disabled `Orcs` spawn point (`:255-279`);
  overland random-encounter hook to BD0060 (`:241-253`).
- UNVERIFIED: carried gear of Tsolak/Isabella/Ikros (CRE parse failed) — check in
  NI/WeiDU before any full re-home.

## Dwarven dig site — undead census

**All hostiles are PRE-PLACED, active on load, zero scripted spawns** (area scripts
are quest/boss logic only). Cutting = ARE placed-actor removal.

- **BD1100 (upper): 85 hostiles** = 59 undead (BDSHZOM1 ×10, GHOUL ×9, ZOMBIE ×9,
  GHAST ×8, BDWIGHT3 ×6, BDGHASTG ×5, BDWIGHT1 ×4, BDGHAST ×3, BDWIGHT2 ×2,
  BDMUMM01/BDWIGHT/BDWRAI02 ×1) + 26 dig-monsters (BDMCARRI ×12, BDCCRAW1 ×6,
  CARRIO ×2, BDUMBER1 ×4, BDOTYG01/02) . Quest NPCs to keep: BDDCLER1-3, BDDEEP
  (Brother Deepvein), BDDODWD, BDSEMAHL.
- **BD1200 (lower): ~118 hostiles**, headline stacks: BDBONBAT ×17, BDDEAD01 ×10,
  BDSHSOUL ×10, BDSHZOM1 ×9, BDSKGR04 ×9, ZOMBIE ×6, BDSKGR05 ×5, BDWIGHT1 ×5,
  skeleton-guard families ×~20 more, BDSHADGR ×2, BDUNSLGU ×1 miniboss.
- Boss: Coldhearth Lich (`BDCOLDH`) — respawns after TEN_ROUNDS unless phylactery
  `BDMISC60` destroyed (`BD1200.baf:100-146`); arena force-wall via
  `BD_DOD_NO_ESCAPE` (`:178-200`, regions `Forcewall`/`Lichtran`); clean kill →
  `AddExperienceParty(22000)` (`:10-18`).
- Rest tables both levels: felt 49%/49%, difficulty 200 (always max 3) — wave-1
  component 100 already rescales these on install.

## Flagged uncertain
1. BD1010 entry door id.
2. Tsolak/hunter carried gear.
3. `BDMISC63` in-game name.
4. `THREE_ROUNDS` exact seconds (≈18 s assumed).
