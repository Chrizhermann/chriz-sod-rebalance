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
12. Skie playable, with her regular BG1 soundpack. Keep some of her flavor beats that make
    sense ("don't tell daddy about this" etc.).

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

## Relationship to existing design docs
- Items 5–8 supersede/absorb the rebalance levers in `design/01` (rest rates), `design/02a–c`
  (trash cut), `design/05` (travel ambushes) — same research base, more aggressive intent.
- Item 17 extends the "make meaningful" lever (`design/00` §candidates).
- Items 1–4, 9–16 are NEW scope beyond the original rebalance design.
