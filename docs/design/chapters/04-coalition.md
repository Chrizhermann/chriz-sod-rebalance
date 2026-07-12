# Chapter pass — the coalition camp (Ch. 10–12: Dead Man's Pass → Bloodbark Grove → Underground River → Kanaglym → camp/castle)

**Status: QUICK-WIN PASS EXECUTED (2026-07-12, components 260/270/280 + 255, v0.6.0,
installed on dev).** The user approved the proposed cuts wholesale to get "a more
smooth game now and available for playtesters" — with everything below the quick-win
line recorded for a later flesh-out round: "we go with your suggestions and we
brainstorm on them later."

## Scope decisions (user, 2026-07-12)

- **Coalition camp (BD4000), Dragonspear Castle assault, Avernus: KEEP mostly vanilla.**
  "Most people think those fights are fun."
- **Boareskyr Bridge scripted battle: KEEP.** "The expansion is called SIEGE of
  Dragonspear, so battles like that actually make some sense." Same reasoning shields
  the camp/castle set-pieces.
- **Hell/Avernus "seems fun for most people"** — no cuts there this pass.
- **MUST-DO 1 — the party dispel at the castle-basement reveal is gone** (comp280).
  "Why does your party get dispelled? It's 1000% anti fun. We have to remove it."
- **MUST-DO 2 — the Boareskyr explosive barrels are durable now** (comp255, fast fix).
  The full elemental/portal sequence rework stays open (below).

## Quick-win pass (EXECUTED 2026-07-12 — components 255/260/270/280, v0.6.0)

All on-disk verification green (cut counts exact per area, chunk rides compiled,
barrel stats verified, zero player-targeted dispels remain in 45A/45B/CUTSKIP).
Numbers from the generator (`research/scripts/gen_ch10.py` →
`comp260_lists.tpa`/`comp270_lists.tpa`); **all cut/keep picks and the barrel
numbers below await user veto** (approved in direction, not yet in detail):

- **comp260 (scouting maps + shadow vault): 183 cuts / 129,495 field XP**
  - BD7300 Dead Man's Pass, 119 of 139 hostiles: all beetles (23), boars (7), both
    displacer packs (19), the hobgoblin camp (10), both orog warbands (21 + 4 worgs),
    dire wolves (11), the NW **ogre camp (12) — cut here even though BD7100's ogre
    camp was kept**: this map keeps the hill-giant camp as its big-camp fight and two
    giant-humanoid camps on one map is exactly the zoo problem. Giant spiders (2),
    phase spiders 7→4, hill giants 10→3+leader (the SE camp of 5 is gone entirely).
    KEPT: the nymph pocket (nymph + hamadryad + 2 dark treants + 2 shamblers — with
    the 15-corpse dead-orog field it explains), both ettins, the gargantuan/sword
    spider elites of both pockets, the hostile cave bear, and every neutral (Raeanne +
    her earth elemental, Gnaler/Kambaldur, Horst/Stalia/Nuber, all fauna).
  - BD7400 Bloodbark Grove, 21 of ~30: beetles (13), bone bats (2) + shadowed soul
    (1) — both on the wave-1 banned list — burning skeletons 9→4. KEPT: the greater
    basilisk, dark treants + shambler, the wight/ghast night pocket, skeletal mage.
  - BD7310 shadow vault, 1: the Unsleeping Guardian (banned list). The 9-body
    shadow/wraith vault fight stays.
  - BD5000 Underground River, 32: the displacer pack (6), huge spiders (3), greater
    wyverns 4→1, the orc camp (20). KEPT: wyvern mama + baby, gargantuan + sword
    spiders, cave bear, and all ~55 neutrals by construction (the crusader river
    camp, **Murs' ogre family — the 12k dialogue quest lives here**, Rigah/Julann,
    the chunks-and-bones displacer kill site set dressing).
  - BD5100 river caves, 10: the three identical corrupted-grove pockets reduced to
    one — pocket A stays intact (3 treants + shambler + gargantuan spider + corrupted
    hamadryad + nymph), pockets B/C lose their treants (4), shamblers (2) and
    gargantuan spiders (3, one kept in C), umber hulks 3→2 (one per myconid pocket).
    Corrupted nymphs/hamadryads all stay (they ARE the druid story). KEPT: the whole
    myconid colony + shriekers, the ettin ghost, the ankheg, and every neutral (the
    drow war party, crusader patrols, Strunk/water spirits, the poisoned crusaders).
  - **XP chunk: +17,300/char** riding the guaranteed 20,000 chapter-11 transition
    award in BD4000.bcs (fires once, after all five maps were available). Note: a
    player who skips the optional maps still gets the chunk — same stance as the
    ledger's completionist calibration; flagged, not fixed.
- **comp270 (Kanaglym): 11 cuts / 6,550** — shadowed souls (3, banned), skeleton
  archers 9→3, armored 3→2, bladed 2→1. The 4,000-XP skeleton-warrior mini-boss
  anchors the remaining 8-skeleton graveyard fight. The south quest cluster (dark
  magicians + Kherriun + sacrifices + Zhadro + the Endless cast) is neutral-until-
  quest and untouched by construction; C0MNEV01 is another mod's creature (never
  touched). **XP chunk: +900/char** riding the Kherriun/Dark-Magicians 12,000 award
  (both RESPONSE branches patched; exactly one fires).
- **comp280 (no party dispel at the basement reveal):** BOTH cutscene variants strip
  the party — BDCUT45A and BDCUT45B each cast bddispel on Player1–6, and CUTSKIP.bcs
  mirrors both (12 more). All 24 player-targeted casts removed; the ward flare
  (bdwardgr + EFF_M08), the bdglowgr holy-glow beat and every enemy-side parley
  dispel (Caelar, lieutenants, the bridge-parley crusader set) stay. Corrects an
  earlier research note that claimed 45B only dispels enemies — it dispels both sides.
- **comp255 (durable barrels):** BDKEGX 25 hp / 0% fire → **120 hp / 75% fire**
  (cold stays 50). Rationale: the battle's loss condition rides barrels that random
  mephit fire splash pops "with no counter" on higher difficulties. Covers all four
  placed barrels + any scripted spawns (CRE-level patch); nothing scripts BDKEGX by
  name; story detonations use Kill() and still work.

Implementation findings (ground truth, 2026-07-12):
- **CUTSKIP mirrors are structurally different from their cutscenes** — the BDCUT14
  mirror has NO bdwforce cast and NO SPFLESHS VFX (ambient + door toggle only), and
  the count-guards caught both mismatches on the first install attempt (fail-loud
  worked as designed; nothing half-patched). Patterns must be verified against the
  compiled CUTSKIP per mirror, not assumed from the cutscene source.
- comp245 (Coast Way group) fixes the CUTSKIP wall mirror + bumps its parley timer to
  FIVE_ROUNDS — the skip rig set the vanilla THREE_ROUNDS even with comp200 installed
  (playtest issue #5, root cause confirmed).
- `ApplySpellRES("bdremove",Player1)` in the same BD4000 transition block was checked
  as a possible second anti-fun dispel: it is opcode 177 (EFF by IDS target) + 168
  (remove portrait icon) — status-icon cleanup, NOT a dispel. Left alone.
- BD5100's script-spawned treant/shambler waves (`CreateCreatureEffect` SPWOOD at the
  SE corner) are a separate scripted encounter — placed-actor cuts don't touch it.

## Later flesh-out round (recorded 2026-07-12, user's own wording)

- **"Do we even need the Bloodbark grove? Why is it there? Just to have something
  more?"** — existence question, not a trim question.
- **"Why are the drow in the underground river? There is just more to have more...
  it's just SO LOADED on such a small space."** Doesn't mean remove everything —
  but the density itself is the problem.
- **"Then the whole druid situation"** — the corrupted-grove/druid content needs a
  real look (this pass only thinned the duplicate pockets).
- **Albino wyverns are "WAY WAY WAY too strong (because of their abilities, not
  because of their stats)"** — ability-level nerf wanted, separate from today's
  count-thinning (4→1 placed).
- **Kanaglym quest-enemy volume:** "ALso the quest enemies - again, are so many" —
  the south-quest cluster sizes themselves are bloated; untouched today because
  they're quest-staged.
- **The Boareskyr elemental/portal sequence needs a big rework:** "They want to blow
  up the bridge with ready-made barrels and they for some reason need a portal to
  the fire plane...? What? Why not just throw a fireball or something like that?"
  The fight until then is fine. comp255 is the stopgap.

## OPEN for the flesh-out round

1. Bloodbark Grove: keep-and-justify vs remove (worldmap unreachability like BD7000?).
2. Underground River composition: what earns its place on the small map (drow war
   party? sahuagin? the crusader camp?).
3. The druid/corrupted-grove storyline treatment across BD5100/BD7300.
4. Albino wyvern ability nerf (design the ability changes, difficulty-gate?).
5. Kanaglym south-quest cluster sizes (quest-staged spawns, needs script surgery).
6. The bridge elemental/portal sequence rework (writing + encounter design).
7. XP ledger checkpoint: chunk-on-transition pays even for map-skippers — revisit
   with playtest curve data.
