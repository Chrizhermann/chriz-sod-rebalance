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

## Quick-win pass (EXECUTED 2026-07-11 — components 230/240/250, v0.5.0, installed on dev)

**Shipped.** All on-disk verification green (cut counts exact per area, both region
retargets in place, zero remaining travel regions target BD7220, chunk blocks
compiled, both SPLs byte-verified). Final numbers from the generator
(`research/scripts/gen_ch9.py` → `comp230_lists.tpa`/`comp240_lists.tpa`):

- **comp230 (main line):** BD7100 63 cuts / 27,425 field XP (hobgoblins 16, orcs 14,
  beetles 8, displacers 6, small spiders 8, troll thin-out 11 → 21 trolls stay in
  four real clusters) · BD2000 8 cuts / 1,015 (beetles, worgs, stray wight — siege
  pickets + scripted battle untouched) · BD2010 27 cuts / 585 (warren core of 8
  stays). Total 29,025 → **+3,900/char** once-block on `bd_plot > 292` (both battle
  branches set 293; the existing 6000/3000 in BD2000.baf turned out to be the
  Dorn-release / missing-patrol SIDE quests — census correction — so the chunk
  rides its own block).
- **comp240 (optional loop):** BD7200 28 cuts / 10,835 (bugbear door-guards 11,
  displacers 7, dire wolves 5, small spiders 5 — wyverns/phase-spiders/hill giant
  stay) · BD7230 6 ambusher cuts / 2,750 · BD7220 removed by unreachability,
  ledgered 14,810 (11,810 hostiles + 3,000 quest shadow). Total 28,395 →
  **+3,800/char** once-block on the Neothelid kill.
- **comp250 (Morentherene tiers):** Hard+ = +56 HP (168) / AC −5 (−6) / THAC0 +4
  (−2) / saves +3 / MR +20 (35); Insane stacks +62 HP (230) / AC −3 (−9) / THAC0
  +2 (−4) / saves +2 / MR +15 (50) / +1 APR (4). Applied asleep via the vanilla
  ApplySpellRES delivery; breath/buffet/AI untouched; Core plays vanilla.
  **Numbers awaiting user veto.**

Implementation findings (ground truth, 2026-07-11):
- **Vanilla chain confirmed:** overland → dragon cave → bugbear cave → temple; the
  only two travel regions in the game pointing at BD7220 were BD7210's and
  BD7230's `TranBD7220`. Retargeted at each other's vanilla `ExitBD7220`
  entrances; region NAMES kept, so `EscapeAreaObject("TranBD7220")` still works —
  **the temple's fleeing cultist (CULTIST_NEO_ESCAPE, BD7230.baf:128) now flees
  into the dragon cave**, fulfilling the user's "move the fleeing cultist to that
  exit" by construction. The bugbear cave's own alarm-runner beat (bdcultx2,
  BD7220.baf) dies with the area.
- **Spectacles gimmick survives:** bdmisc01 is carried by BDZAVIAK in BD0109 (city);
  8 other areas run the same equip-check shadow mechanic. Only BD7220's Greater
  Shadow instance is lost (ledgered).
- **Ambusher loot: mundane** (leather, short swords, daggers, minor potions + SCS
  random-treasure tokens) — user asked; nothing worth re-homing. The ambush region
  script (BD7230AM) keys every block on the named actors being alive-and-neutral,
  so with the actors never spawning it is permanently inert — zero script edits.
- **Ogre-camp correction:** the BD7100 ogres are NOT the 12k BDMURS dialogue quest
  (BDMURS lives in BDCUT42) — kept anyway as a real coherent fight, one word flips
  it (regenerate + reinstall).
- Spawn points in BD7100/7200 (deactivate-on-load, re-arm post-clear) left as-is —
  ambient respawn is not part of this pass.

User decisions on the proposal (2026-07-11):
- **Troll thin-out: ON** ("It's way too much"). Later idea logged: add something MORE
  dangerous to Troll Claw for higher difficulties (wishlist-adjacent, not this pass).
- **Hill giant: KEEP.**
- **Invisible cultist ambush (BD7230AM): CUT now.** It is "an impossible to beat
  encounter on higher difficulties currently"; whether a rebalanced version returns
  is DEFERRED to the item-15 round. Check + report whether the six ambushers carry
  any important items.
- **Routing requirement (user):** with BD7220 removed, the cult temple must be
  reachable from the wyrm cave DIRECTLY and back — the vanilla chain routes through
  the bugbear cave; rewire so BD7210 ↔ BD7230 works both directions with no
  BD7220 leg. Verify the vanilla transition graph from the .are files first.
- **NEW in-pass item — Morentherene difficulty scaling (component of its own):**
  "make the dragon scale harder and more fun on higher difficulties. It's really
  weak and easy to kill currently, its only dangerous two abilities being the wing
  buffet and its breath. Otherwise it has laughable HP and laughable attacks and
  defenses." → difficulty-gated stat/defense buffs (comp170 ApplySpellRES pattern),
  numbers presented for veto with the install report. Core and below untouched.

Scope guard (unchanged): this pass = trash cut + ledger chunks + the dragon tiers
ONLY. Explicitly NOT in it (later rounds): temple relocation, Ziatar fight reshape
(item 15), bridge-battle rework, recruit simplification. Rest headers already
handled arc-wide by wave-1. (The original census-estimate proposal tables were
superseded by the EXECUTED block above — ground-truth dumps corrected the ambusher
XP, the BD2000 award attribution, the ogre-quest claim and the BD7220 entrance
mechanism; the confirmed cut/keep intent carried over 1:1.)

## OPEN for sparring round 1

1. Per-area cut/keep lists (census tables: 292 placed hostiles, ~37k/char kill XP —
   concentration: BD7100 104 bodies / BD7200 47 / BD7230 18 forced).
2. The Forest-of-Wyrms loop is OPTIONAL (worldmap: bd7100 → bd2000 direct). Keep it
   optional as-is, or fold the (relocated) temple into the main road?
3. Boareskyr Bridge is a SCRIPTED set-piece (only 34 trivial placed mobs; a ~90-actor
   neutral crusader army flips hostile in the bridge battle, Khalid leads the
   defenders) — treatment? Early user note (2026-07-10 Discord post): rework wanted,
   "at least the explosive barrels part"; user filed it under "later," so it may
   split out of round 1. **PARTIALLY EXECUTED 2026-07-12: the battle itself is
   KEPT ("the expansion is called SIEGE of Dragonspear"), and comp255 shipped the
   barrel fast-fix (BDKEGX 25 hp/0% fire → 120 hp/75% fire — random mephit splash
   no longer a no-counter loss).** The elemental/portal sequence rework ("why not
   just throw a fireball?") stays open — see 04-coalition.md later-flesh list.
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
