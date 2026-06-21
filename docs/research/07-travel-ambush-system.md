# 07 — SoD Worldmap Travel-Ambush System (VERIFIED)

Status: **verified** against the live install's decompiled scripts + `worldmap.wmp`. Date: 2026-06-21.
This is the **second** ambush system, distinct from the rest-header system in `01-rest-ambush-mechanic.md`
/ `design/01`. Read-only on the game dir; scratch in `C:\tmp\sod_research\travel\`.

## TL;DR

SoD's travel ambushes are **100% script-driven**, not engine-automatic. While the party is walking in
a wilderness area, that area's `.bcs` periodically rolls a **`ForceRandomEncounterEntry("BDxxxx",
"Exit")`** action that yanks the party into a dedicated battle-map arena. The roll is gated by a
**shared 8-hour cooldown** (`BD_TIMER_URE`), a **`RESPONSE #40 / #60` weighted die (40% fire / 60%
skip+reset)**, a **one-at-a-time flag** (`BD_FRE`), and a **per-encounter one-shot global**
(`BD_UREn`). Because no `BD_UREn` is ever reset, the whole thing is a **finite, curated pool of
one-time encounters** — at most **4 combat-arena ambushes per playthrough** (orc, "dead-magic",
goblin, giant), each ~8h apart at 40% each. **`worldmap.wmp` contains none of the arena resrefs and
no 2DA is involved** — the engine's built-in WMP random-encounter feature is NOT used here.

## 1. The trigger mechanism

Example block (BD7300 Dead Man's Pass; identical pattern in all 8 travel areas):

```
IF
  GlobalLT("bd_plot","global",390)              // only active before this plot stage
  Global("BD_FRE","GLOBAL",0)                   // no encounter currently active
  !GlobalTimerNotExpired("BD_TIMER_URE","GLOBAL") // the 8h cooldown has expired
  Global("BD_URE3","GLOBAL",0)                   // this specific encounter not yet used
THEN
  RESPONSE #40                                   // 40% : FIRE the ambush
    SetGlobal("BD_FRE","GLOBAL",1)
    SetGlobalTimer("BD_TIMER_URE","GLOBAL",EIGHT_HOURS)
    SetGlobal("BD_URE3","GLOBAL",1)              // consume this encounter (one-shot)
    ForceRandomEncounterEntry("BD0066","ExitSE") // -> load the goblin arena
  RESPONSE #60                                   // 60% : do nothing, just reset the 8h timer
    SetGlobalTimer("BD_TIMER_URE","GLOBAL",EIGHT_HOURS)
END
```

- `ForceRandomEncounterEntry(area, entrance)` is the EE-engine action that loads the battle map and
  drops the party at the named entrance. **This is the travel-ambush trigger.** (Grep: 18 calls total
  across 8 area scripts, hitting just 4 arenas.)
- The area script runs every AI tick while you're in the wilderness area, so the block becomes
  eligible the first tick after the 8h cooldown clears, fires its single 40/60 roll, then re-arms the
  cooldown either way. Net cadence: **~40% chance of one ambush per 8 in-game hours of wilderness
  travel**, drawing the next un-used encounter.
- `BD_FRE` (Force-Random-Encounter "busy" flag) is set to 1 on fire and **reset to 0 inside each
  arena's own script** (`BD0060/BD0063/BD0064/BD0066.baf`, on arena init) so the next URE can arm
  after you leave.
- `GlobalLT("bd_plot",...)` (390 in the BD7x woods, 295 at Boareskyr) **switches the random ambushes
  off once the main plot advances** — they're a mid-game travel-phase feature.

## 2. The frequency variables (exactly where they live)

All in the **wilderness area `.bcs` scripts**, nowhere else:

| Lever | Token | Effect | Where |
|---|---|---|---|
| **Per-roll fire chance** | `RESPONSE #40` vs `#60` | 40% fire / 60% skip | every FREE block (×18) |
| **Cooldown / spacing** | `SetGlobalTimer("BD_TIMER_URE","GLOBAL",EIGHT_HOURS)` | min 8h between ambushes (shared) | 36 occurrences across all travel scripts |
| **One-at-a-time gate** | `Global("BD_FRE","GLOBAL",0)` | blocks overlap | every FREE block |
| **One-shot consume** | `Global("BD_UREn","GLOBAL",0)` → set 1 | each encounter fires once, ever | per encounter |
| **Plot cutoff** | `GlobalLT("bd_plot","global",390/295)` | disables after plot stage | per area |

There is **no master 2DA, no `.ini`, no WMP probability** governing this. It is purely these script
globals/weights.

## 3. The arenas — enumeration, selection, contents

**Selection:** not a random table — the *current area's script* offers a fixed list of `BD_UREn`
blocks in order; the first un-used one whose gate passes is the candidate, and the 40/60 die decides.
So which arena you get depends on **which wilderness area you're in and which URE you haven't used
yet**. The same encounter (e.g. URE3 goblins) is offered from many areas but, being one-shot, fires
only once total.

| URE | Arena | Entrance | Theme (intro line) | Offered from |
|---|---|---|---|---|
| **URE1** | **BD0060** | ExitSW | Orc/troll waylay | BD7000, BD7100, BD7200, BD2000 |
| **URE2** | **BD0063** | ExitW | "Dead-magic" zone; mercenaries — *"Proceed as instructed."* (`BDURE2A`) | BD7300, BD7400, BD2000 |
| **URE3** | **BD0066** | ExitSE | Goblin horde — *"This our place! We take treasure! You go!"* (`BDURE3B`); explosion opens a cavern → chains to **BD0067** (myconids) via `BDURE3A` | BD7100, BD7200, BD7300, BD7400, BD2000, BD3000 |
| **URE4** | **BD0064** | ExitE | Hill giants — *"You spoil our dinner... Smash and cook you!"* (`BDURE4B`) | BD7100, BD7200 |

Connected sub-arenas (not direct FREE targets): **BD0061** (troll) / **BD0062** (frost-troll+ooze,
reached via the `Tranbd0062` region trigger in `BDPOOL`) / **BD0067** (myconid, reached from the BD0066
goblin chain). Per-arena enemy rosters and counts are in `02a-encounters-prologue-coastway.md` and
`sod_encounters_full.csv` (BD0066 = 41 mobs is the worst; BD0060 ≈8, BD0063 ≈5, BD0064 ≈6, BD0067 ≈13).

## 4. Story vs random — the split the user cares about

The `BD_UREn` pool actually contains **two kinds** of encounter:

**A. RANDOM combat-arena ambushes (the annoying ones → REDUCE):** **URE1, URE2, URE3, URE4** — the
four `ForceRandomEncounterEntry` arena loads above. Pure combat trash maps. URE2 has a thin "someone
sent us" flavor but is mechanically in the random pool.

**B. Scripted roadside vignettes (flavor/story → KEEP):** **URE6–URE10** are NOT arena ambushes —
they spawn creatures/NPCs *in place* on `Entered([PC])` with `RESPONSE #100` (guaranteed once, no
40/60 die, not on the 8h timer). They are characterful, often with named NPCs and dialogue:
- **URE6** (BD7300): a refugee group (`BDURE6A/B/C` "Refugee" + `BDURE6D`).
- **URE7**: Myrleena dialogue scene — *"See, Myrleena? I told ye he wasn't gonna help us."* (`BDURE7A/B`).
- **URE8** (BD7300): named NPC `bdephrik` ("Ephrik").
- **URE10**: a chase vignette — *"Lebass! Get back here, ye wingein' faintheart!"* (`BDURE10A/B`).
- (URE5, URE9 not located in the 8 travel scripts — likely other chapters or unused; verify before touching.)

**C. TRUE story set-pieces (→ KEEP, untouched):** the crusade attacks, Boareskyr Bridge battle,
Coalition Camp siege (BD3000, 67 scripted), Dragonspear assault, etc. are **not** `BD_URE`/`BD_FRE`
gated at all — they're dedicated plot scripts/cutscenes. The travel-ambush levers below don't touch them.

## 5. Reduction recommendation (reversible tail-mod, script-only)

The arena ambushes are already finite (≤4) and cooldown-gated, so the realistic goal is "make the few
that fire rarer and optionally drop the worst one." Levers, in order of bang-for-buck:

1. **Lengthen the cooldown** — global replace `"BD_TIMER_URE","GLOBAL",EIGHT_HOURS` →
   a larger value (e.g. `ONE_DAY`/`THREE_DAYS`, or a raw seconds count) across the 8 travel scripts.
   Single-token, widens spacing so you rarely meet the 40% window during a chapter.
2. **Lower the fire weight** — `RESPONSE #40` → `RESPONSE #10` (or `#5`) in the FREE blocks. Cuts the
   per-window chance from 40% to 10%/5%. (Leave the paired `#60` skip branch; its relative weight rises.)
3. **Drop the worst arena entirely** — delete/NOP the `BD_URE3`/`BD0066` blocks (the 41-mob goblin
   horde) so that encounter never fires. Optionally pre-set `BD_URE3`=1 at install so it's "already used."
4. Pairs with `design/02a` (which *shrinks* each arena's roster): levers here reduce **how often**,
   02a reduces **how big**.

**Implementation (no WMP, no 2DA):** one WeiDU tail-mod that, for each of `BD7000/BD7100/BD7200/
BD7300/BD7400/BD2000/BD3000/BD5000.BCS`, does `COPY_EXISTING … DECOMPILE_BCS_TO_BAF` →
`REPLACE_TEXTUALLY` the timer constant and/or `RESPONSE #40`→`#10` (scoped to lines near
`ForceRandomEncounterEntry` to avoid touching unrelated weighted blocks) → `COMPILE_BAF_TO_BCS`.
Fully reversible (WeiDU backup). Alternatively, a `RANDOM_ENCOUNTER`-style approach isn't available
since the engine WMP path is unused. Applies on next area load for a live save (no new game needed).

## 6. Important caveat — which ambush system actually dominates the "constant ambush" feel

This travel-arena system is **modest**: ≤4 one-shot combat ambushes per playthrough, 40% per 8h. The
**rest-header system (`01`/`design/01`) is the heavier offender** — it's per-area, per-rest,
**repeatable**, and rolls per in-game hour (39–80% felt per 8h rest, max 3–6 each). If the user feels
"I get jumped constantly while traveling," most of that is the **rest** ambushes fired during
recovery, plus the in-area rest/spawn systems — not these 4 arenas. Recommend shipping the travel-
ambush cooldown/weight nerf **together with** the Design 01 rest nerf; on its own, the travel lever is
a small (but genuine — being yanked onto a battle map mid-travel is jarring) quality win.
