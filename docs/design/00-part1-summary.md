# Design 00 — Part 1 (SoD Remix) Sign-Off Package

One-page consolidation of the SoD-remix design. Backed by `docs/research/01–07` (all verified
against the live install) and detailed in `docs/design/01–05`. **Nothing is installed yet** —
this is the plan for your sign-off. You play **Difficulty 5 (Insane)**, which doubles dynamic
spawn counts; all numbers below account for that.

## The problem, verified
1. **Resting is unreliable.** The engine rolls the rest-interrupt **per in-game hour**, so listed
   6–18% becomes **39–80% felt per 8h rest**, and interrupted rests compound. (`research/01`)
2. **Ambushes dump too many enemies.** `Difficulty 80/200` forces every rest-ambush to its max;
   on Insane that's doubled (~12 catacomb skeletons). Rest tables are rigged with
   toolkit-nullifying creatures (skeletons: missile 90% / slash·pierce 50%; trolls self-heal).
   (`research/01`, `research/06`)
3. **~1,300 enemies, mostly pre-placed trash.** Wilderness alone is ~36%. Set-pieces are drowned
   in filler. (`research/02a/b/c/d`)
4. **A second, smaller travel-ambush system** yanks you onto battle maps (~4 one-shots, 40%/8h).
   (`research/07`)
5. XP is fine to rebalance: SoD is already **82–88% quest XP**, no XP cap on this install, so
   cutting trash barely dents progression and is trivially re-injected into quests. (`research/03`)

## The plan — 6 levers (all reversible WeiDU tail-mods)

| # | Lever | What | Design |
|---|---|---|---|
| 1 | **Rest rates** | day/night % → felt ~8% prologue / ~15% wilderness / ~22% dungeon; cap `max` to 1–2 (≈2–4 on Insane); sanitize `difficulty 80/200→2` | `01` |
| 2 | **Trash cut ~70%** | remove pre-placed filler; preserve set-pieces | `02a/b/c` |
| 3 | **Creature softening** | catacomb skeletons missile 90→0, slash/pierce 50→0; keep trolls/slimes out of rest tables | `04` |
| 4 | **Travel ambushes** | lower fire weight + lengthen cooldown (keep story vignettes) | `05` |
| 5 | **XP reweight** | shift removed trash-XP into the big guaranteed quest awards (`.baf` **and** `.dlg`) | `03` |
| 6 | **Meaningful fights** | rebuild a focused few into quality encounters | `02a/b/c` |

## Trash-cut totals (placed enemies; set-pieces preserved)

| Region | Before | After | Cut |
|---|---|---|---|
| Prologue + Coast Way | ~511 | ~140 | −73% |
| Forests (BD7x) | 476 | 189 | −69% |
| Camp / Underground / Castle | 460 | ~247 | −46% region (−69% on trash; ~149 set-piece enemies preserved) |
| **Approx. SoD total** | **~1,300** | **~580** | **trash −~70%, set-pieces intact** |

## "Make meaningful" candidate menu (you wanted 2–3; pick a set)
- **Prologue:** Korlasz climax rebuild · Coldhearth Lich + phylactery (curate guards) · spider matriarch
- **Forests:** Hill-Giant warband · Troll Shamaness · Bloodbark vampire
- **Camp/Castle:** goblin chieftain (BD2010) · Cyclops gate-guardian (BD5000) · Myconid Sovereign (BD5100)
- **Stretch (phase 2, bigger `.bcs` reworks):** Coalition Camp siege (named champions vs wave-spam) · castle gate-breach commander
- *Recommendation:* do **Korlasz climax + Coldhearth Lich + one wilderness boss** now; defer the siege/breach reworks to phase 2.

## Preserved set-pieces (never cut)
Morentherene (BD7210), Neothelid cult temple (BD7230), shadow tomb (BD7310), Coldhearth Lich,
Coalition Camp siege (BD3000), castle assault (BD4000), Boareskyr bridge (BD2000), basement
(BD4300), **Caelar Argent** (BD4700), The Ambush (BD6100), roadside story vignettes (URE6–10).

## Implementation sequence (after sign-off — phase 2)
One mod, component-per-lever, appended after the current last WeiDU.log entry; **never uninstalls
anything**; full WeiDU backups → reversible. Suggested order: 1 (rest) → 3 (creatures) → 2 (trash)
→ 4 (travel) → 5 (XP) → 6 (meaningful fights). Levers 1/3 are the highest value-per-effort and
could ship first as a standalone "resting fix."

**Live-save caveat (important):** once you've *entered* a SoD area in your current save, that
area's actor layout and state are baked into the save — `.are` edits (trash cuts, rest header)
then apply only to areas you **haven't visited yet** / a fresh SoD run. `.cre` stat softening
(lever 3) applies to newly-spawned creatures. Script/`.dlg` edits (levers 4/5) apply on next
load. So on your existing playthrough the benefit lands on the road ahead, not areas behind you —
worth confirming where you are before we pick a rollout. (We can verify the rest-header specifically.)

## Decisions to lock Part 1 (defaults in **bold**)
1. Prologue resting: rare straggler (~8%) **(rec)** vs fully off.
2. Ambush feel: wilderness ~15% / dungeon ~22% **(rec)** vs more lenient.
3. Trash depth: **~70%** vs push 80%.
4. Meaningful fights: **Korlasz + Coldhearth + 1 wilderness boss** now, siege/breach phase 2 — or a different set.
5. Boss rebuilds genuinely harder per-creature **(rec, modest)** vs fewer-bodies-only.
6. Creature softening scope: **game-wide BDSKGR\*** + keep undead CC-immunity (rec) vs prologue-only.
7. Travel ambushes: **Light tier** + kill the goblin-horde arena (rec) vs leave / fully off.
8. XP: **neutral** (trash→quests, same total) vs generous (+10–20%); main-quest-only **(rec)** vs also side-quests.

## Deferred
- **Part 2 (companions)** — held for your weakest-NPC shortlist (Baeloth flagged as the nerf).
- **Part 3 (SCS / base-game tweaks)** — after Part 1 direction is locked.
