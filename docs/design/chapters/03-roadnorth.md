# Chapter pass — the road north (Ch. 9: Troll Claw Woods → Forest of Wyrms → Boareskyr Bridge)

**Status: EARLY DIRECTIONS ONLY (user, 2026-07-10).** Census done —
`docs/research/13-roadnorth-census.md` (areas verified: BD7100 Troll Claw Woods →
*optional* BD7200 Forest of Wyrms + BD7210 dragon cave / BD7220 / BD7230 temple →
BD2000 Boareskyr Bridge + BD2010 + BD2100 Bridgefort). Sparring round 1 pending —
the user wants a closer look at the census before big decisions.

## Early directions (user-decided, 2026-07-10)

- **Enemy volume:** the areas are again packed with "way way way too many groups of
  enemies that make no sense." Remove MOST of them — especially the ones that make no
  sense where they stand. Keep their items and XP and re-place those elsewhere (the
  established pattern: re-homed loot + ledger chunks on kept milestones).
- **Bugbear cave: remove the whole area.** Pin RESOLVED against the census
  (2026-07-11): the bugbear cave is **BD7220** (Forest of Wyrms sub-cave, 36 bugbears,
  Snorgash, the Greater Shadow spectacles quest). NOT BD7110 — that is the **troll
  lair** (Shamaness + Wand of Fear), which stays: a troll lair off Troll Claw Woods
  is coherent content.
- **Dragon cave → temple, direct:** the cave connects to the temple and that is its
  only role. Move the fleeing cultist to that exit.
- **The temple should not be here at all (plan):** an actively-used temple whose only
  access is a cave full of wyverns and a dragon makes no in-world sense. Plan to
  relocate the temple somewhere else entirely — structural question for round 1
  (worldmap placement? repurpose another area? what happens to the cave then?).
- **Ziatar (the half-dragon lady) is cool — keep her.** Census note to resolve in
  round 1: vanilla's actual climax in BD7230 is the Neothelid (20k XP); Ziatar is a
  3k parley-adjacent NPC — item 15 ("one big fight vs Ziatar") implies reshaping that.
- Wishlist anchors in this arc — both CONFIRMED into this pass by the Discord post
  (2026-07-10): **item 15** — "one big fight in the temple" (Ziatar; strip the filler)
  and **item 16** — "the dragon fight should be much more scary on high difficulty"
  (Morentherene, BD7210's sleeping dragon, 13k; packaging — in-pass difficulty-gate vs
  separate optional component — still open).

## Quick-win pass (PROPOSED 2026-07-11 — awaiting user confirm)

Context: the user wants a stable, streamable state on his current playthrough soon —
"remove a bunch of things from the next maps and already bump up the main quest
rewards... depending on how much exp is missed (plus a bump for optional
stuff/ambushes, like we did previously)." This pass = trash cut + ledger chunks ONLY.
Explicitly NOT in it (later rounds): temple relocation, Ziatar fight reshape (item
15), Morentherene rework (item 16), bridge-battle rework, recruit simplification.
Rest headers already handled arc-wide by wave-1. Numbers below are census-based
(research/13); final numbers come from the generator against the pristine .are
actor tables (gen220 pattern: schedule-zero cuts, auto-computed chunks, 0.8 factor —
which also absorbs the Insane-vs-Core placed-count overcount, census flag #1).

**BD7100 Troll Claw Woods (104 hostiles / 79,055 field XP):**
- CUT: hobgoblins ×16, orcs ×13, beetles ×8, displacer pack ×6, small spiders ×8
  (SPIDGI/SPIDHU) ≈ 14,425 field. Rationale: chaff + copy-paste spam; trolls are the
  area identity, spiders keep one real nest.
- CUT (default ON, user may veto): troll thin-out by ~⅓ — TROLL01 ×6, TROLSP01 ×3,
  TROLLSM ×2 ≈ 14,400 field. 21 trolls remain.
- KEEP: remaining trolls, the gargantuan+sword spider nest (the census "fun spike"),
  ogres ×10 (the 12k BDMURS ogre-tribe dialogue quest rides on them — verify at
  implementation), boars (fauna), ALL ~24 camp NPCs (chapter-9 camp cast).
- BD7110 troll lair: NO CHANGE (coherent set-piece, Shamaness, Wand of Fear).

**BD7200 Forest of Wyrms overland (47 hostiles / 40,235 field):**
- CUT: bugbears ×11 (their cave is removed — orphaned flavor), displacer pack ×7,
  dire wolves ×5, small spiders ×5 ≈ 11,850 field.
- KEEP: all 13 wyverns (area identity), phase-spider pocket incl. the 4k astral
  (fun spike), hill giant (fun spike; user may veto), Coogan + fauna.

**BD7220 bugbear cave: REMOVE (user-decided 2026-07-10).** Mechanism: deactivate the
entrance transition in BD7200 (region-level, reversible). ≈ 13,760 field removed.
Loot inside is mundane (no re-home needed). Implementation checkpoints: (a) find the
spectacles-quest (bdmisc01/SDD118) giver — if outside BD7220, False()-gate the offer,
zero new text; (b) verify BD7230 temple routing unaffected (main entrance is via
BD7210 dragon cave; the bdcultx2 ambush at BD7220's temple transition dies with the
area — aligns with the cut-scripted-ambushes lean).

**BD7230 temple (quick-win slice only):** CUT the post-Neothelid invisible-cultist
ambush (BD7230AM, 6 invisible JumpToPoint cultists ≈ 10,200 field) — scripted-ambush
lean; False()-gate, no text. Default ON, user may veto. Everything else in the
temple untouched until the item-15 round.

**BD2000/BD2010 Boareskyr (placed layer only):**
- BD2000: CUT beetles ×5, worgs ×2, stray wight ≈ 1,165 field. KEEP the
  hobgoblin/goblin scouts (siege pickets make sense). Scripted battle untouched.
- BD2010 goblin warren: trim ~28 chaff goblins ≈ 700 field; KEEP chieftain + witch
  doctor + ~6 guards + Circlet of Lost Souls loot.

**XP chunks (0.8 convention, rounded to 100s, default config):**
- Main line: BD7100 + BD2000/2010 cuts ≈ 30,690 field → **+4,100/char** additive
  chunk on the Boareskyr resolution beat (bd_plot 293, rides the existing 6k+3k —
  additive block + once-flag, Beamdog numbers untouched).
- Optional loop: BD7200 + BD7220 + temple ambush ≈ 35,810 field → **+4,800/char**
  chunk on the Neothelid kill (Dead("BDNEOTHE") + once-flag).
- Packaging: two components — 230 (main line) + 240 (Forest of Wyrms/optional loop),
  individually selectable, generator-produced cut lists.

## OPEN for sparring round 1

1. Per-area cut/keep lists (census tables: 292 placed hostiles, ~37k/char kill XP —
   concentration: BD7100 104 bodies / BD7200 47 / BD7230 18 forced).
2. The Forest-of-Wyrms loop is OPTIONAL (worldmap: bd7100 → bd2000 direct). Keep it
   optional as-is, or fold the (relocated) temple into the main road?
3. Boareskyr Bridge is a SCRIPTED set-piece (only 34 trivial placed mobs; a ~90-actor
   neutral crusader army flips hostile in the bridge battle, Khalid leads the
   defenders) — treatment? Early user note (2026-07-10 Discord post): rework wanted,
   "at least the explosive barrels part"; user filed it under "later," so it may
   split out of round 1.
4. Temple relocation target + the cave/temple/Ziatar/Neothelid recomposition (item 15
   fight shape).
5. Morentherene treatment (item 16 optional component; she guards the cave→temple
   path — how does that interact with the relocation?).
6. XP ledger row for the arc: what's removed vs which carriers get the re-injection
   (BD7100 10k chapter award; BD2000 6k+3k; dialogue-layer 12k×3: M'Khiin, ogres,
   camp cluster).
7. Voghiln + Neera recruit at Bridgefort — untouched, or simplified like the others?
8. Rest/zero-ambush designations for the arc (wave-1 already dropped felt rates to
   ~8-15%; census: no banned no-save creatures anywhere in this arc).
