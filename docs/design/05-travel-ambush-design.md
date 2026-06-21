# Design 05 — Travel-Ambush Reduction (PROPOSAL)

Depends on `docs/research/07-travel-ambush-system.md`. This is the *second* ambush system the
user complained about ("random/annoying ambushes" while traveling) — distinct from rest-ambushes
(`design/01`). Verdict from research: **modest system, small win** — the rest system is the
heavy offender; this is polish.

## Mechanism (verified)
Script-driven, NOT the engine's WMP random-encounter feature. While in a wilderness area, that
area's `.bcs` periodically runs `ForceRandomEncounterEntry("BD00xx","Exit")` to pull the party
onto a battle-map arena. Gating per trigger:
- shared 8h cooldown `GlobalTimer("BD_TIMER_URE","GLOBAL")` = `EIGHT_HOURS`
- one-at-a-time `Global("BD_FRE","GLOBAL",0)`
- per-encounter one-shot `Global("BD_UREn",...,0)` — set to 1 on fire, **never reset**
- plot cutoff (`GlobalLT("bd_plot",...)`)
- weighted die: `RESPONSE #40` fire / `RESPONSE #60` skip+rearm timer → **~40% per 8h travel**

Because the `BD_UREn` globals never reset, the combat-arena pool is **finite: ≤4 per playthrough**
— URE1 orc (BD0060), URE2 dead-magic (BD0063), URE3 goblin horde (BD0066), URE4 giant (BD0064).

## Story vs random (the clean split)
- **REDUCE:** URE1–4 — the random `ForceRandomEncounterEntry` combat arenas (the annoying ones).
- **KEEP:** URE6–10 — scripted roadside vignettes, named NPCs + dialogue, fire once on entry
  (refugees, Myrleena, Ephrik, the "Lebass" chase). Characterful, not arena ambushes.
- **UNTOUCHED:** true crusade set-pieces (Boareskyr, Coalition Camp BD3000, Dragonspear assault)
  — not `BD_URE`/`BD_FRE`-gated at all; separate plot scripts.

## Proposed change (pick a tier)
All script-only, reversible, applied on next area load. Mod patches BD7000/7100/7200/7300/7400/
2000/3000/5000.BCS via `COPY_EXISTING` + `DECOMPILE_BCS_TO_BAF` + `REPLACE_TEXTUALLY` + recompile.

| Tier | Change | Result |
|---|---|---|
| **Light (rec.)** | fire weight `#40 → #15`, cooldown `EIGHT_HOURS → ONE_DAY` | arenas become rare flavor; ~1–2 over a playthrough instead of up to 4 |
| **Medium** | above + NOP the worst arena (URE3 goblin horde / BD0066) | drops the most-complained-about pile-on entirely |
| **Off** | pre-set `BD_URE1–4 = 1` at install (or NOP all four fire blocks) | zero random travel arenas; roadside story vignettes still play |

Pairs with `design/02a` (which shrinks each arena's *roster*): this lever = how *often*, 02a =
how *big*. On the user's Insane setting the arena rosters are ~2× — another reason to thin them.

## Decision for you
- Which tier? (Recommend **Light** — you said keep story ambushes; this keeps the system as rare
  flavor while killing the "yanked onto a battle map again" annoyance.)
- Specifically kill the **goblin horde (URE3)**? It's the biggest pile-on of the four.

## Note
The research caveat is important: most of the "constantly jumped while traveling" feeling is
actually **rest-ambushes during recovery** (`design/01`), not these ≤4 arenas. Ship both together;
don't expect this lever alone to move the needle much.
