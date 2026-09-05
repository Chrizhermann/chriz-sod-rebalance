# 01 — SoD Remix Wishlist (living document)

**Status:** draft / living — captured from planning session 2026-07-03. This EXTENDS the
original Part-1 rebalance scope (`00-project-scope.md`, `design/00-part1-summary.md`) into a
full **remix/overhaul**: map removal, plot surgery, flow restructuring — not just rebalancing.
Items are the user's asks, verbatim in intent; numbering preserved from the session. Nothing
here is designed or signed off yet. The list is explicitly incomplete and grows as we plan.

## Guiding principles (user-stated)
- **Compatibility first.** Must play well with, at minimum: vanilla, SCS, Spell Revisions,
  Artisan's Kitpack, CDTweaks, EET. Explicit anti-goal: Artisan's-mods-style fragility with
  other mods. *This is very important.*
- **Slim SoD down hard.** Remove some maps entirely from the campaign flow; when a map goes,
  track what was load-bearing on it (progression triggers, important items, quest givers,
  NPCs) and relocate those elsewhere.
- Remove a lot of conversations; remove some plot points completely.
- **Process:** global/system-wide changes first (e.g. ambush rates); overall arc planning
  (Caelar) up front; then chapter-by-chapter passes for details.

## The list

### Campaign flow & structure
3. Don't start in SoD's worst dungeon. Open chill instead — people celebrating the heroes —
   and kick off the crusade plot at the point where it currently starts (after the
   Imoen-poisoning beat).
4. Korlasz dungeon: drop it entirely, or make it skippable/optional. Its important items get
   re-sourced — probably via a Korlasz fight plus a fun group of enemies.

### Companions
1. Keep your party after defeating Sarevok — companions should not force-leave at SoD start.
2. Keep Imoen; drop the Duke-Jannath/mage-training + poisoning plot completely. Imoen is
   re-recruitable normally, like every other SoD companion. (Trainer verified: Grand Duke
   Liia Jannath, `bdliia` — not "Janneth".)
12. Skie playable, with her regular BG1 soundpack. (Second half superseded 2026-07-09 —
    "keep some flavor beats" is dropped: she becomes a simple BG1-style talk-to-join
    recruit with no SoD plot beats; the "don't tell daddy" night scene is removed
    (component 190). See "Decisions locked 2026-07-09" below.)

### Narrative arc
9. Caelar is the main antagonist.
10. Hooded man / Irenicus: removed 100% from the plot.
11. Skie's death: removed from the plot.
13. Rework Hell (Avernus) and the end fight; rework some of Caelar's dialogue (overall);
    give Caelar a different portrait.
14. Haephernan: not Wormtongue 2.0 — make it less obvious he's the villain.

### Encounters & systems (global)
5. Reduce overall ambush chance ~5× ; remove ambushes entirely in some areas.
6. Remove a lot of enemy groups completely.
7. Replace some enemy masses with a few fun enemies.
8. Rework the scripted ambushes (the ones that sometimes carry special items): kill the huge
   groups; fill with nothing or with something more interesting/fun.
17. Important fights get SCS-style scripting, prebuffs, maybe stat/level adjustments — all
    scaling with difficulty.

### Specific set-pieces
15. Cyric temple: strip a lot of the fights and filler; make it one big fight vs. the
    half-dragon lady (Ziatar) and some strong companions of hers.
16. The green dragon (Morentherene) much scarier and stronger — optional component, and
    difficulty-scaling.

## Provenance warning on the existing design docs
`design/00–05` (trash-cut percentages, per-area rest targets, creature-softening scope,
"8 decisions with defaults") were authored by a **prior agent without the user's input** —
they are research-backed *proposals*, not user decisions. Nothing in them is locked. The
research docs (`research/01–08`) remain valid as data. Decisions live HERE and in the
chapter-pass docs only.

## Decisions locked (2026-07-03, session 2)
- **Removal over rewriting.** Default instinct for unwanted content is REMOVE, not re-author.
  Per-chapter/per-map strip lists decided during the chapter passes.
- **Item 1 (keep party):** keep **everyone**, including the 17 companions with zero SoD
  content (silent passengers are fine — flexibility wins). That's *step 1*. *Step 2* (later):
  optionally place non-party companions somewhere in SoD as pickups, maybe with a little
  dialogue.
- **Items 10/11 (ending):** remove the **entire post-victory epilogue** — dream, Skie murder,
  arrest, trial, jail, breakout, hooded man. No replacement narrative: defeat the final boss,
  victory, fade out, BG2 begins unexplained (the original BG1→BG2 feel). Rationale: the
  scripted transition makes no sense per-character (e.g. a paladin framed for murder keeping
  his powers).
- **Ending shape (open, two candidate shapes):** Caelar is the final boss. Belhifet either
  (a) becomes the fight *before* Caelar, or (b) is defeated *by Caelar* (scene, not player
  fight). To be settled in the arc treatment.
- **Item 12 (Skie):** confirmed — playable, BG1 soundset, death dropped entirely.
- **Test environment:** implementation/testing happens against a separate copy of the game
  (user maintains copies), not the live playthrough install.
- **Compat (Q4):** standalone BG:EE+SoD is in scope alongside EET; the ending replacement
  branches per platform (EET handoff vs. native campaign end).
- **No global locks** for zero-ambush areas or creature softening — both decided
  per-chapter/per-map during the chapter passes.
- **XP anchor (the one global number):** MC enters SoD at ~220–250k XP and should finish at
  ~700–750k — i.e. target gain ≈ **450–530k per character**. XP is tracked as a running
  per-chapter ledger, not one global reweight.
- **XP baseline is NOT trusted yet:** `research/03`'s "~665–715k vanilla gain" is an
  upper-bound estimate (thorough-run assumption, heuristic dedup, kill XP estimated, measured
  on the modded install). Realistic-run reading of the same data ≈ 555–630k, with wide error
  bars. Calibrate against the user's actual playthrough (he completed SoD on this install —
  a save near the BG2 transition is ground truth) and recount per-chapter when the ledger is
  built.
- **Ending shape parked:** Caelar = main antagonist is set; how Belhifet fits (pre-Caelar
  fight vs. defeated by Caelar) is decided later, when the user is creatively ready — nothing
  blocks on it. (Lore verified: Caelar's crusade frees her **uncle**, Aun Argent, Order of
  the Aster, who sacrificed himself into Avernus for her.)

## Wave-1 sign-off state (2026-07-03, session 3)
- `design/wave1/01` rest-ambush 5× sweep: **SIGNED OFF** (as computed; pack size per-chapter).
- `design/wave1/02` keep-all-companions: **SIGNED OFF**.
- `design/wave1/03` hooded-man removal: **SIGNED OFF**; the 4 chapter rest-dreams ("very very
  bad quality") are **skipped** — content documented first for a maybe-someday rewrite.
- `design/wave1/04` travel ambushes: **deferred** to the per-area chapter passes.
- `design/wave1/05` XP: calibrate only after testing; first lever = **+~10% main-quest
  rewards** if the curve comes in low.

## Decisions locked (2026-07-06/07, prologue playtests)
- **Entar Silvershield stays DEAD.** SoD shows him alive (Skie's father — palace/city
  content, the epilogue trial) despite his BG1 Ch.7 assassination; "him being alive
  again is just cringe." Locked direction: **remove him entirely and rewrite whatever
  references him so he remains dead** — the epilogue removal already deletes his trial
  role, and we may add our own content in his place in phase 2/3. **City chapter DONE
  (component 185, 2026-07-09):** unspawned from the plot-51 war council, the plot-56
  departure send-off rebuilt around Belt, Liia's roll-call drops his name, the
  "weren't you killed?" resurrection reply gated. **Superseded/resolved 2026-07-16:**
  the approved ending makes BD0035/BDCUT62 unreachable, gates the last BDPALACE reference,
  and leaves BDENTAR.CRE/DLG inert rather than deleting files that other mods may expect.
- **Fresh-start/import party grant cut** (prologue §10, component 145): the vanilla
  default-party grant on fresh SoD starts is removed — you wake alone and gather your
  party in the city. Item 1's "keep everyone" applies to the *continuous* BG1→SoD
  path, which is untouched.

## Decisions locked (2026-07-08, Coast Way round 1)
- **No no-save/no-roll cheese, anywhere:** shadowed souls (BDSHSOUL — touch with no
  save and no attack roll) are removed from EVERY SoD area they appear in, not just
  the dig site ("those creatures should not exist anywhere"). Apply the same
  judgment forward: bone bats and the Unsleeping Guardian are on the not-fun list.
- **Removed-content treasure = one mod-wide choice component:** every chapter pass
  that deletes content routes its loot through a single component with two flavors —
  "collected conveniently in a container" or "removed with the content." First
  payload: the BD7000 items (Gemblade etc.).
- **SoD's Skie plot: removed/heavily rewritten** (companion piece to Entar-stays-dead
  above; her BD7000 sub-quest dies with that area). Skie PLAYABLE (item 12) stands.
- Coast Way tier decisions (rounds 1+2, design LOCKED) live in
  `docs/design/chapters/02-coastway.md`: BD7000 removed (Rasaad to the BD1000
  camp), west spider installation cut, bridge magic wall cut, interrupt timer
  FIVE_ROUNDS, dig-site garrison replaced by 1 horde room + a couple scary-few
  encounters + ~3 pushover groups + 1 hard group (2 mummies + 2 elite skeleton
  guards at the sealed door); of the dig-monsters only umber hulks survive;
  Semahl's fight beat preserved (small); cut XP returns as ONE chunk on the lich
  clean-kill award; lich-fight rework deferred.

## Decisions locked (2026-07-09, city-chapter Entar/Skie/assassination surgery)
Implemented + installed + verified on the dev install (components 185/190/195):
- **Entar removed (185):** see the 2026-07-06/07 block above — city chapter DONE.
- **Skie's second-night bedroom visit removed (190):** the 3 a.m. "don't tell Daddy"
  cutscene is gone. A Skie-free wake pre-empts both bd0103 night blocks (party sleeps
  through to dawn, `bd_plot` 54→55 as before); the night dialogue tree (BDSKIE 16-32)
  is sealed. Part of dropping Skie's SoD plot (item 12).
- **Assassination/poison residue scrubbed (195):** comp150 removed the first-night
  palace assassination; NPCs still referenced it. All residue removed with **zero new
  dialogue** — reply/state `False()` gates plus two re-routes: BDSCHAEL 227 moves the
  `bd_plot=54` retire-commit onto the "ready to march" reply and EXITs (skipping
  Corwin's "crusader poison" goodnight), and BDLIIA 13 re-routes "how fares Imoen?" to
  Liia's existing training-advice line. Covers BDCORWIN/BDELTAN/BDEDWIN/BDLIIA/BDSCHAEL/
  BDDEBUG/BDFIST05. The de Lancie supply-poison quest is explicitly OUT of scope.
- **Follow-up status:**
  - **Skie talk-to-join core SHIPPED (component 197):** the signed-off short palace
    exchange restores Beamdog's `JoinParty()` scaffold, retires her remaining SoD plot
    surface, and uses the BG1 soundset already on her CRE. It is installed on dev;
    runtime verification remains pending. Only the optional estate/gear inheritance is
    deferred.
  - **Full Corwin dialogue rewrite:** user finds SoD-Corwin's writing poor and wants a
    proper redo later; comp195 only removed her assassination residue, not rewrote her.
  - **Entar's final inert reference:** assigned to the approved 2026-07-16 ending cleanup;
    BD0035/BDCUT62 become unreachable and BDENTAR.CRE/DLG remain harmless files.

## Decisions locked (2026-07-10, triage round)
- **Prologue XP:** option (c) **24,000/char**, delivered as **Liia's quest reward** on
  the jailbreak return beat (component 175, installed). Numbers: 01-prologue.md §7.
- **Dig-site polish executed:** the six "Drowned in Blood" are cut; the honor guard
  **literally replaces them** on their vacated coords; no backfill bodies; the XP
  returns via the **106,700 party-total** lich chunk (≈17,783/char at six).
- **Placement principle (locked):** never place creatures where no enemy was placed
  before — vacated original-actor coordinates (walkable by construction) or
  searchmap-verified tiles only. (Born from the honor-guard void-placement bug.)
- **XP-fill principle (locked):** garrison cuts return as quest rewards/chunks, never
  as replacement bodies.
- **Ending pass scope CONFIRMED = pure removal, no rewrites:** the campaign ends at
  the post-Avernus victory celebration; the whole dream → Skie murder → arrest → trial
  → jail → breakout → endgame-hooded-man band is removed. EET banks the party from
  BD4300 into `BD6100*K#ImportContainer` and enters BG2 without the party entering BD6100;
  standalone ends natively from BD4300. Caelar as final boss reaffirmed — the
  Avernus/end-fight rework itself is item 13, a separate later pass. The precise
  celebration and handoff were approved on 2026-07-16 below.
- **Skie scope sharpened:** remove EVERYTHING else of her SoD plot involvement; she
  becomes the BG1-style talk-to-join recruit (research/15 has the surface: Beamdog's
  own JoinParty scaffold + her CRE already carries the BG1 soundset). **Fulfilled by
  component 197;** only estate/gear remains a possible follow-up.
- **Later component (backlog): BG1 soundsets for returning BG1 companions in SoD**
  (Khalid, Jaheira, Safana, ...) — one component; per-NPC coverage to research.
- **Dig-site tiered encounter (later):** BG2-style XP-gated miniboss ("lich-lite") to
  keep the dungeon from boring high-XP parties — mechanism + candidates research
  running (docs/research/17 + 18). Guiding reminder (user): *shorter AND more fun* —
  fun is a co-equal goal of the remix.
- **Historical Chapter-9 note:** early directions were recorded here before the later
  quick-win pass shipped as components 230/240/250/255. Broader reworks remain separate.

## Additions (2026-07-10, Discord announcement post — user's own wording)
- **Boareskyr bridge-battle rework** is on the list — "at least the explosive barrels
  part." (Filed by the user under "later"; the battle itself is ch-9 content — see
  03-roadnorth.md OPEN #3.) Expanded by the 2026-09-05 roadmap direction below.
- **Scaling encounters generalized:** BG2-style scaling encounters **with better
  pre-buffs, for higher difficulties only** — broadens the dig-site tiered-miniboss
  idea (research 17/18) toward item 17's SCS-style-fights lever.
- **Dialogue-rewrite program:** rewrites for multiple quests/NPCs/companions (Corwin
  absorbed into this), shipped as **optional component(s)**; community ideas welcome
  (not full writing help — ideas/plots).
- **Travel ambushes — user lean:** possibly "just cut ALL scripted ambushes"
  ("are 100 one-hit goblins fun? honestly not sure") — strengthens the full-cut
  option in wave1-04's parked design.
- **Caelar/Belhifet motivation = open writing question (community input invited):**
  why did Caelar go to the Hells, and what did Belhifet actually want? His involvement
  "made no sense before and it's hard to justify him now." Feeds item 13 / the arc
  treatment; collect Discord ideas before that pass.
- Korlasz fight tone restated: SCS-style but **not too hard** — "we don't need another
  Sarevok fight right after Sarevok" (matches the shipped Semaj-parity design).

## Additions (2026-07-11, Discord thread round 2)
Community thread digested; obvious jokes filtered out (recorded here only if the
USER took a position). Statuses explicit — none of these are locked decisions yet.
- **Ashatiel duel → party-vs-party fight (CONSIDERING):** community idea (Archibald),
  user endorsed the direction — "heckin' W. Or we make it optional." User's sketch:
  on insane difficulty a genuinely hard set-piece — you are NOT stripped of buffs,
  you're warned the fight is coming, the enemy side gets real prebuffs + scripted
  sequencers. "I will think about this." (Ashatiel = Caelar's champion; the single
  combat offered during the final assault on Dragonspear Castle.)
  **Update 2026-09-05:** now requested as a separate component for design triage;
  the full encounter still needs a back-and-forth design discussion. See below.
- **Caelar arc — first workshop seeds (feeds the item-13 open writing question):**
  Jester's frame: keep her motive (rescue her uncle from the Hells), but the uncle
  comes back *wrong* — soul-tortured, turned evil — and the final fight is Caelar +
  uncle + Hephernaan. User's response ("maybe we can workshop this, I kind of like
  it") + user's own direction: Caelar as LG shining-paladin-with-good-intentions is
  the cool part and stays; the current plot is indefensible (sacrificing thousands,
  the "army" absurdity); what works: her initial goal is genuinely saving her uncle
  (maybe more souls), and her goals **get twisted as the Crusade goes on**;
  Hephernaan **plays both sides**; the uncle being broken after Hell is "totally
  understandable."
- **Dig-site full-skip component (FLOATED, no decision):** user floated an optional
  component to skip the dig site entirely (Sauler: "maybe yes"); counterpoint in the
  same thread (GachiBalor): as a side adventure it's fine once de-trashed — "that
  state is already done" (user).
- **Frame-the-hero plot (PARKED, far future):** Sauler — post-BG1 Baldur's Gate is
  full of Sarevok loyalists / Iron Throne remnants / corrupt Fist officers with
  motive to frame the hero. User: "I will consider this for the future... this would
  be a lot more work as well."
- **Imoen recruitable later in SoD (community ask, NO user position yet):** Sauler
  wants her back in the party before the end ("after a recovery"). Touches the
  comp160 design (Imoen stays in BG studying); log only, decide later.

## Additions (2026-07-12, coalition-camp quick-win approval — user's own wording)
- **Basement-reveal party dispel: REMOVED (decided + shipped, comp280).** "Why does
  your party get dispelled? It's 1000% anti fun. We have to remove it."
- **Boareskyr barrels: durable now (decided + shipped, comp255)** as the fast fix;
  the **elemental/portal sequence still needs its big rework**: "They want to blow up
  the bridge with ready-made barrels and they for some reason need a portal to the
  fire plane...? Why not just throw a fireball?" The fight until then is fine.
  **Update 2026-09-05:** remove the barrels and their mechanics entirely; the new
  elemental-demolition proposal below supersedes the durable-barrel endpoint.
- **Set-piece battles are KEEPS:** coalition camp, castle assault, Avernus, and the
  Boareskyr scripted battle stay mostly vanilla — "The expansion is called SIEGE of
  dragonspear, so battles like that actually make some sense"; "hell seems fun for
  most people."
- **Later flesh-out list opened** (details in design/chapters/04-coalition.md):
  does Bloodbark Grove need to exist at all; the Underground River is "SO LOADED on
  such a small space" (why drow?); "the whole druid situation"; albino wyverns "WAY
  WAY WAY too strong" via ABILITIES not stats; Kanaglym quest-enemy counts also
  bloated (quest-staged, needs script surgery).

## Decisions locked (2026-07-15, dig-site scrying pool)
- **One abstract Caelar omen; every old vision removed.** No Imoen vision (she can
  literally be in the party under component 160), no Hooded-Man vision, no original
  Caelar cinematic, no picker, teleports, staged army, forced dialogue, or shared
  cutscene teardown. The sole payoff is this exact non-modal text:

  > The water clears. A woman in argent armor stands before a door beneath the world.
  > Something waits beyond it—something she knows, or believes she knows. She reaches out.
  > For an instant, you cannot tell whether she is opening the way or being drawn through.
  > Then the water clouds.

- **Every quest item is required:** all three Silver Scepters (`BDMISC55`) and both
  Essences of Clarity (`BDMISC59`). The cut `BDWIGHDD` stays cut; its Essence is
  re-homed into the existing BD1200 `Sarcophagus01` beside that container's scepter.
- **The pool is one-use and then permanently dormant.** Its third-scepter reward stays
  3,000 party-total XP; the removed Imoen and Caelar vision rewards are consolidated
  into one 1,000-XP award to each of Player1–6.
- **Implemented as component 225 in v0.6.3** and tail-installed plus semantically
  verified on the dev EET copy. Runtime verification waits for the next SoD playthrough;
  the live v0.5.0 install remains unchanged. Full trace: `docs/research/20-scrying-pool.md`.

## Decisions locked (2026-09-06, optional full SoD skip)

- An optional palace-bedroom choice can skip the full expansion using EET's
  normal BG2 opening, with an additive, once-only **250,000 protagonist XP**.
  Both Yes and No have a confirmation; declining confirmation returns to the
  question. Confirmed No continues SoD without an XP award.
- **Use normal carried inventory; defer loose-loot recovery.** The long-running
  pickup scan and private staging area are rejected. Keep backpacks carried on
  Yes; preserve the native palace impound on No. Imported Imoen's existing
  belongings remain in scope, not fresh Imoen or arbitrary palace loot.
- A future save-persistent record of acquired import items is deferred in
  [issue #18](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/18), not
  added to the immediate skip.
- Component 910 is separate from the shortened post-victory ending. The direct
  Yes route was accepted in-game and authorized for v0.6.7; visual transition
  polish and broader runtime coverage are deferred. No collection pin changes.
  Details: [current design](design/wave1/06-optional-sod-skip.md).

## Decisions locked (2026-07-16, post-victory ending)
- **Short playable celebration in BD4300:** preserve BDCUT59/59A/59B, compress the
  party's one-line victory-bark delays to about two seconds, keep de Lancie's public
  acknowledgment and Bence's cheer/acknowledgment, then restore free control. Dazzo's
  existing rest conversation is gated to `bd_plot=590` and is the deliberate endpoint.
- **Everything after the celebration is removed:** no Bence "check on Skie," private
  Waterdeep pitch, Corwin/Neera forced romance finales, other optional plot-590 coda,
  sleep/dream, Skie corpse, Irenicus, arrest, trial, jail, escape, sewers, reunion,
  Shadow-Thief ambush, or ambush movie. Skie and Imoen may both be in the party.
- **Entar remains fully scrapped:** remove his final live SoD reference with the ending
  cleanup while preserving unrelated chapter-7/8 BD0104 Coalition/refugee/Tiax content.
  Retired resource files may remain inert for compatibility and reversibility.
- **Neera's BG2 romance is unaffected:** SoD's `bd_neera_romanceactive` and
  `bd_NeeraRomance6` are separate from BG2's `NeeraRomanceActive`, `NeeraLovetalks`,
  and `NEERA_ROMANCE`. Do not fake SoD-finale completion or synthesize a bridge.
- **Direct platform endings:** on EET, clone the installed K# handoff, bank locally in
  BD4300, move the bank to `BD6100*K#ImportContainer`, and enter SoA without the party visiting
  BD6100; originals stay untouched. Standalone runs `EndCutSceneMode()`,
  `ContinueGame(FALSE)`, and `EndCredits()` directly from Dazzo.
- **First-party tests on both platforms:** thorough EET static/runtime coverage plus
  one staged standalone Dazzo-to-credits smoke. Stream/Discord testing supplements,
  but does not replace, those checks. Full design:
  `docs/plans/2026-07-16-post-victory-ending-design.md`.

## Roadmap additions (2026-09-05, user direction)

These are queued design/audit tasks. Requested directions and open design choices
are separated below; the encounters have not been implemented.

### Boareskyr Bridge: replace the barrel finale — [#14](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/14)

- **DECIDED direction:** overhaul the bridge-destruction sequence and remove all
  smokepowder barrels and associated objectives, staging, dialogue, and destruction
  gimmicks. Retire the single weak unnamed wizard / Plane-of-Fire portal premise.
  Component 255's durable barrels remain the installed stopgap until this ships.
- **PROPOSED replacement:** as the crusaders lose the battle, multiple wizards try
  to destroy the bridge with **fire and earth elementals**, already summoned and/or
  being summoned during the encounter. A difficult battle scaling with difficulty.
- **OPEN for triage/design:** wizard roster and roles, elemental mix/counts, summoning
  presentation and timing, placement, player counterplay, bridge failure conditions,
  difficulty tiers, dialogue, and XP/loot accounting. Preserve the wider siege battle
  direction while designing this replacement finale.
- **Research before implementation:** trace barrel/portal scripts, dialogue, placed
  and spawned objects, bridge-opening/progression dependencies, and CUTSKIP mirrors;
  determine how the replacement supersedes component 255 on both supported platforms.

### Ashatiel: Chosen of Cyric-style party fight — [#15](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/15)

- **DECIDED scope/process:** queue a separate component for the default Ashatiel
  encounter during the final castle assault. Triage first, then a **full back-and-forth
  design discussion with substantial input from both the user and the agent**, before
  implementation. This is separate from the Caelar/Avernus and post-victory passes.
- **Requested starting brief:** a Chosen of Cyric-style party encounter, with about
  **30 seconds for the player to buff before the opposing group spawns**. Enemies get
  prebuffs, sequencers, and potions too. Carry forward the earlier preference to warn
  the player and preserve their existing buffs.
- **OPEN:** reference-fight mechanics to adopt, enemy roster/roles, Ashatiel's role,
  dialogue and existing duel/alternate routes, preparation-window trigger and warning,
  exact timing/spawn positions, spell/potion loadouts, difficulty tiers, and rewards.
  Research the current encounter and reference fight, then bring alternatives to the
  discussion; this sketch is not a signed-off encounter design.

### Campaign filler and trash coverage audit — [#16](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/16)

- **DECIDED task:** double-check whether unnecessary map filler and trash mobs were
  removed across SoD. Reconcile shipped cut lists, chapter decisions, research datasets,
  and effective dev-copy resources, including **scripted spawns, respawns/re-arm loops,
  travel ambushes, and quest-staged groups**, as well as placed actors.
- **Deliverable:** a map-by-map gap list distinguishing missed approved removals,
  intentionally retained encounters, redundant filler, and unreviewed content. Record
  resource/spawn evidence, quest/progression hooks, unique loot/recruit dependencies,
  and XP-ledger impact; distinguish static findings from remaining playtest work.
- **Starting candidates:** road-north ambient respawns; temple/Ziatar filler;
  Bloodbark Grove's purpose; Underground River density/drow; druid/corrupted-grove
  content and scripted treant/shambler waves; Kanaglym south quest clusters; deferred
  travel-ambush arenas. Earlier placed-actor cuts did not cover all these systems.
- **OPEN:** further keep/cut/consolidate decisions and replacement encounters. Present
  findings for triage, retaining the reasons for keeping story/siege set-pieces.
  The audit is queued; its results and additional removals are not yet decided.

## Relationship to existing design docs
- Items 5–8 supersede/absorb the rebalance levers in `design/01` (rest rates), `design/02a–c`
  (trash cut), `design/05` (travel ambushes) — same research base, more aggressive intent.
- Item 17 extends the "make meaningful" lever (`design/00` §candidates).
- Items 1–4, 9–16 are NEW scope beyond the original rebalance design.
