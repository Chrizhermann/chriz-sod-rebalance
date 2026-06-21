# 01 — Rest-Ambush Mechanic (VERIFIED)

Status: **verified** against engine source + the live install's `.are`/`.bcs` files.
Date: 2026-06-21.

## How rest-ambushes work

Every area carries a 228-byte **Rest Interruptions** struct, pointed to from the `.are`
header at offset `0xC0`. Relevant fields (offsets within the struct):

| Off | Field | Notes |
|---|---|---|
| `+0x48` | 10 × CRE resref | the spawn table the ambush draws from |
| `+0x98` | table count | # valid entries |
| `+0x9A` | **difficulty** | `spawnamount = totalPartyLevel × difficulty` |
| `+0xA4` | **max creatures** | hard cap on spawn count |
| `+0xA6` | enabled (0/1) | |
| `+0xA8` | **day %** | |
| `+0xAA` | **night %** | |

**Engine logic** (GemRB `Map::CheckRestInterruptsAndPassTime`, verbatim-checked): spawns on
rest only if `count>0 && enabled && max>0`. So every `day=10 / empty-table` SoD area
(BD0100, BD0102, …) **never** random-spawns — its table is empty.

When it does fire: `spawnamount = partyLevel × difficulty`, spawned up to `max`. SoD sets
**difficulty = 80 or 200** on most ambush areas → `partyLevel × 80` is always ≥ `max`, so
**every ambush spawns the full max** (3–6), never a token one or two. This is the
"more enemies = more fun" signature.

## The per-hour roll — the actual culprit

The listed `day%`/`night%` is rolled **per in-game hour** by the Beamdog engine, not once per
rest. Evidence:
- IESDP labels the field literally "probability **per hour**".
- GemRB implements once-per-rest and its own source comments the loop is "a bit odd … the
  only way this not to return immediately is from a data error" — i.e. GemRB knowingly
  diverged from the original.
- Community-reported and player-confirmed: "it rolls every hour."
- The math then matches lived experience exactly.

Felt chance of ≥1 ambush in an 8-hour rest = **1 − (1 − c/100)⁸**:

| listed `c` | felt per rest |
|---|---|
| 3 | 22% |
| 5 | 34% |
| 6 | 39% |
| 8 | 49% |
| 10 | 57% |
| 12 | 64% |
| 18 | 80% |

**Compounding:** an interrupted rest restores nothing → you rest again → roll again. Needing
2–3 rests to recover at ~50% each ⇒ ~75–88% chance of getting jumped during a single recovery.
That is the felt "you can't reliably rest" of the SoD prologue.

## Not scripted — confirmed

No SoD **area** script (`BD0###`/`BD1###`/`BD2###`/`BD4###`/`BD5###`/`BD7###`) uses the
`Rested()`/`PartyRested()` trigger. Only **companion** scripts do (post-rest banter:
Baeloth, Edwin, Minsc, …). Therefore the rest-ambushes are purely the random rest-header
system. **Lowering these values cannot affect any story/scripted encounter.** (`BDNOREST`
is the town/no-rest creature spawned at `day=100` to cancel resting — separate concern.)

## The data (this install — vanilla SoD values, untouched by SCS/CDTweaks)

Full table: `docs/research/sod_areas_dataset.csv`. 76 BD areas; **35** have an active random
rest-ambush. Highlights (felt% per 8h rest):

- **BD5110** day 12→64% / **night 18→80%**, max 3, diff 200 — worst in the game.
- **First-dungeon catacombs BD0120/BD0130**: day/night 6→**39%**, **max 6**, diff 80,
  table = `BDSKGR*` skeletons (missile + fire resistant per CRE) → the prologue "shitshow".
- **Wilderness** (BD1000 Coast Way, BD7100 Troll Claw, BD7200 Forest of Wyrms, BD7300 Dead
  Man's Pass, BD5000 Underground River, BD7400 Bloodbark…): day 6–8 / night 7–10 →
  **39–57%**, max 3, diff 200 (always max).

For scale: SoD's *listed* numbers aren't higher than BG1/BG2 — BG1 has day=30 city areas.
The difference is (a) the per-hour roll applied to **every** SoD wilderness/dungeon area,
(b) `max 3–6 @ difficulty 80–200` so each ambush is a full pitched fight, (c) SoD's attrition
design forcing frequent rests, (d) SCS toughening the spawned creatures.

## Fix levers (design seed — see docs/design/)

1. **Lower day/night %** to target felt rates. Invert per-hour: `c = 100·(1−(1−F)^(1/8))`.
   - F=15%/rest → `c=2`; F=20% → `c=3`; F=10% → `c=1`; F=25% → `c=3–4`.
2. **Cap `max`** (e.g. 3–6 → 1–2) so an ambush is a skirmish.
3. **Cap `difficulty`** (200/80 → small) so it isn't auto-max.
4. **Per-area policy**, not one global number — safe-ish wilderness vs genuinely dangerous
   dungeons can differ. The first dungeon especially should be near-restful.
5. Optional: curate/soften the worst spawn tables (resistant skeletons) — overlaps with the
   "remix" creature work.

Implementation = one WeiDU tail-mod, `COPY_EXISTING` each `BD*.are` + `WRITE_SHORT` the rest
fields, fully reversible. Open question for design: exact target felt-rate per area class
(user wants resting *reliable*; even 50% is "0% fun").
