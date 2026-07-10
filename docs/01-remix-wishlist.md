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
  "weren't you killed?" resurrection reply gated. **Still deferred (epilogue-coupled):**
  his BD0035 trial placement/guards, BDCUT62 trial/exile, and deletion of
  BDENTAR.CRE/DLG — they die with the post-victory epilogue removal, and the trial
  still references the CRE/DLG, so deleting them now would spam "creature not found."
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
- **Still deferred (flagged, not built):**
  - **Skie as a clean talk-to-join BG1-style companion (item 12 core):** research done
    2026-07-10 (docs/research/15-skie-recruitment.md) — Beamdog left a functional
    JoinParty scaffold in BDSKIE (states 5→6 first-join / 1→2 re-join, camp-gated) and
    her SoD CRE already carries the BG1 SKIEE## soundset, so the pass is re-gating that
    scaffold to a sensible meeting spot + neutralizing her remaining plot surface
    (palace first-meeting 8-15, Bence intro 33-36, bd_skie_plot 37-62, dig 84-90).
  - **Full Corwin dialogue rewrite:** user finds SoD-Corwin's writing poor and wants a
    proper redo later; comp195 only removed her assassination residue, not rewrote her.
  - **Epilogue-coupled Entar removal** (BD0035 trial, BDCUT62, BDENTAR.CRE/DLG).

## Decisions locked (2026-07-10, triage round)
- **Prologue XP:** option (c) **24,000/char**, delivered as **Liia's quest reward** on
  the jailbreak return beat (component 175, installed). Numbers: 01-prologue.md §7.
- **Dig-site polish executed:** the six "Drowned in Blood" are cut; the honor guard
  **literally replaces them** on their vacated coords; no backfill bodies; the XP
  returns via the regenerated lich chunk (17,100 → **17,800/char**).
- **Placement principle (locked):** never place creatures where no enemy was placed
  before — vacated original-actor coordinates (walkable by construction) or
  searchmap-verified tiles only. (Born from the honor-guard void-placement bug.)
- **XP-fill principle (locked):** garrison cuts return as quest rewards/chunks, never
  as replacement bodies.
- **Ending pass scope CONFIRMED = pure removal, no rewrites:** the campaign ends at
  the post-Avernus victory celebration; the whole dream → Skie murder → arrest → trial
  → jail → breakout → endgame-hooded-man band (bd_plot 590–671, research/14) is
  removed; straight to the BG2 handoff (EET: the preserved BD6100 seam; standalone:
  native campaign end). Caelar as final boss reaffirmed — the Avernus/end-fight rework
  itself is item 13, a separate later pass.
- **Skie scope sharpened:** remove EVERYTHING else of her SoD plot involvement; she
  becomes the BG1-style talk-to-join recruit (research/15 has the surface: Beamdog's
  own JoinParty scaffold + her CRE already carries the BG1 soundset).
- **Later component (backlog): BG1 soundsets for returning BG1 companions in SoD**
  (Khalid, Jaheira, Safana, ...) — one component; per-NPC coverage to research.
- **Dig-site tiered encounter (later):** BG2-style XP-gated miniboss ("lich-lite") to
  keep the dungeon from boring high-XP parties — mechanism + candidates research
  running (docs/research/17 + 18). Guiding reminder (user): *shorter AND more fun* —
  fun is a co-equal goal of the remix.
- **Chapter 9 early directions** recorded in docs/design/chapters/03-roadnorth.md
  (round 1 pending the user's closer look).

## Additions (2026-07-10, Discord announcement post — user's own wording)
- **Boareskyr bridge-battle rework** is on the list — "at least the explosive barrels
  part." (Filed by the user under "later"; the battle itself is ch-9 content — see
  03-roadnorth.md OPEN #3.)
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

## Relationship to existing design docs
- Items 5–8 supersede/absorb the rebalance levers in `design/01` (rest rates), `design/02a–c`
  (trash cut), `design/05` (travel ambushes) — same research base, more aggressive intent.
- Item 17 extends the "make meaningful" lever (`design/00` §candidates).
- Items 1–4, 9–16 are NEW scope beyond the original rebalance design.
