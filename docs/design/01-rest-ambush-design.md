# Design 01 — Rest-Ambush Rebalance (SUPERSEDED HISTORICAL PROPOSAL)

> **Current status:** component 100 shipped the signed-off, chance-only 5× frequency
> reduction. It remaps day/night percentages and does **not** change maximum creatures,
> difficulty values, or spawn-table contents. The pack-size, difficulty-sanitizing, and
> table-curation ideas below were never built; they remain historical design material,
> not current component behavior or operational instructions.

Depends on verified mechanic `docs/research/01`. Goal: make resting **reliable** (user: even
50%/rest is "0% fun"), especially in the first dungeon, while keeping rare ambushes as flavor.
Because the engine rolls **per in-game hour**, we set the listed field to hit a target *felt*
rate per 8h rest: `c = 100·(1−(1−F)^(1/8))`.

## Historical proposal: three independent levers
1. **Chance** (`day%`/`night%`) → controls *how often* a rest is interrupted.
2. **Max creatures** (`+0xA4`) → the hard cap on *how many* spawn. This is the reliable count
   control; `difficulty` (`+0x9A`) feeds `partyLevel×difficulty` but is then capped by max, so
   we cap **max** and also sanitize the absurd `difficulty 80/200` down to a normal value.
3. **Spawn-table contents** (`+0x48`) → *what* spawns. From the creature-danger audit
   (`docs/research/06`), several rest tables are rigged with toolkit-nullifying creatures:
   - **Catacomb skeletons `BDSKGR*`** (BD0120/0130): **missile 90% / slash 50% / pierce 50% /
     crush 0%** + CC-immune (RING95 + undead) → archery and crowd-control do nothing, 6 at a
     time, every failed rest. The single worst offender in the project.
   - **Trolls** (`TROLL01` in BD7100's table): full-heal-on-down unless finished with fire/acid
     (+ SCS regen) → an un-killable rest ambush.
   "Safe fodder" suitable for rest tables (per audit): wolves, bandits, hobgoblins, orcs, huge
   spiders, boars. Fix options: (a) swap the rigged creatures out of the *rest tables* (cheapest,
   leaves the placed-encounter versions alone), and/or (b) soften the `BDSKGR*` CREs themselves
   (missile 90→0, slash/pierce 50→0) — this overlaps the Part-1c creature remix and also helps
   the placed catacomb fights. Recommend (a) for the rest mod + (b) tracked under creature remix.

## Historical difficulty context — Difficulty Level 5 (Insane)

Verified from `baldur.lua`: `Difficulty Level = 5` (top tier), `Suppress Extra Difficulty
Damage = 0` (enemies also deal bonus damage). On the top difficulties the **Beamdog engine
inflates spawn counts (~2× observed)** — this is hardcoded, NOT in the `.are` data (GemRB
confirms game-difficulty doesn't scale spawns, so it's a Beamdog addition), so we cannot edit
the multiplier. **Consequence:** the `max` field is a Core-Rules baseline; on Insane the player
sees roughly double. We therefore set baseline `max` LOW so the doubled result is still a
skirmish, and lean harder on table curation + resistance softening (the doubled count ALSO hits
harder via the difficulty damage bonus). Final counts should be eyeballed in-game on Insane.

## Historical proposed policy by area class

| Class | Areas | felt/rest | set `c` (day,night) | baseline `max` | ≈Insane (×2) | set `difficulty` |
|---|---|---|---|---|---|---|
| **Prologue / Korlasz catacombs** | BD00xx, BD01xx active (BD0060-0067, BD0113-0115, BD0120, BD0130) | ~8% | 1, 1 | 1 | ~2 | 2 |
| **Standard wilderness** | BD1000/1010/1100/1200, BD2000/2010, BD7000/7100/7110/7200/7220/7230/7300/7400 | ~15% | 2, 2 | 1 | ~2 | 2 |
| **Dangerous dungeon** | BD5000/5100/5110 (Underground River) | ~22% | 3, 3 | 2 | ~4 | 2 |
| **Avernus** | BD4400/4500 | ~15% | 2, 2 | 1 | ~2 | 2 |

Projected result versus the then-current baseline (felt per 8h rest; counts shown at
the player's Insane setting):

| Area | now (felt, Insane count) | proposed (felt, Insane count) |
|---|---|---|
| BD0120/0130 catacombs (skeletons) | 39% / 39%, **~12** | **8% / 8%, ~2** |
| BD1000 Coast Way | 49% / 57%, ~6 | **15% / 15%, ~2** |
| BD7100 Troll Claw | 49% / 57%, ~6 | **15% / 15%, ~2** |
| BD5110 (worst) | 64% / **80%**, ~6 | **22% / 22%, ~4** |

Projected result: resting becomes reliable; an ambush that *does* fire is ~2 creatures even on Insane,
not ~12 — and the rigged resistant skeletons/trolls are curated out of the rest tables.

## Historical open questions (not current component-100 scope)
- **Prologue leniency:** `c=1/max=1` (≈8%/rest, occasional single straggler) **or fully disable**
  rest-spawns in the catacombs (`max=0`)? You said the first dungeon especially should let you
  rest — I lean to the rare-straggler version for flavor, but 0 is one tweak away.
- **Global vs per-class:** the table above, or a single flat policy everywhere?
- These numbers assume per-hour (verified). If Beamdog were per-rest, they'd be *even more*
  lenient — which still matches your "reliable resting" goal, so this errs safe either way.

## Historical implementation sketch (not shipped)
The unbuilt broader proposal would have patched each affected `BD*.are` as follows:
```
COPY_EXISTING ~BD1000.are~ ~override~
  READ_LONG 0xC0 rest
  WRITE_SHORT (rest + 0xA4) 2     // max creatures
  WRITE_SHORT (rest + 0x9A) 3     // difficulty
  WRITE_SHORT (rest + 0xA8) 2     // day %
  WRITE_SHORT (rest + 0xAA) 2     // night %
  BUT_ONLY
```
Driven by a small table of (area → class). Leave the `BDNOREST` day=100 town areas and the
empty-table areas untouched (they never random-spawn). WeiDU backups preserve the original
bytes, but `--uninstall` is not an operational recovery path for this append-only stack:
any correction ships as a new tail component without uninstalling or reinstalling old entries.
Such an ARE patch would apply to an unvisited area on the next load; component 100 itself
ships only the chance remap described in the banner.
