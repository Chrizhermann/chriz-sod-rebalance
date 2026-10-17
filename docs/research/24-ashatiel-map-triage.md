# Ashatiel: map inspection and encounter preparation

> **2026-09-26 update:** this is the September 22 research snapshot. The user
> subsequently chose to keep the northern party separate, preserve duel/refusal
> routes, and add a rested/dispelled group brawl in another bounded arena.
> [Current decisions](../design/wave1/09-ashatiel-party-brawl.md) supersede the
> earlier preserve-buffs brief and roster/route questions below.
> Follow-on research: [alternative arenas](24d-ashatiel-arena-candidates.md) and
> [reset/boundary feasibility](24e-ashatiel-reset-and-boundaries.md).

Research for [issue #15](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/15),
2026-09-22. **Research complete enough for the next design discussion; encounter
design and implementation are not approved.** The user requested inspection of
the map, existing characters and reusable resources, particularly the named
party in the far upper-left part of the castle grounds.

## Established brief

The [wishlist](../01-remix-wishlist.md#ashatiel-chosen-of-cyric-style-party-fight--15)
requests a separate component for a Chosen of Cyric-style Ashatiel party fight,
with roughly 30 seconds of player-controlled buffing before the enemy group
spawns, a warning, preservation of existing buffs, and enemy prebuffs,
sequencers and potions. Exact roster, arena, dialogue, timing details, spell
packages, difficulty scaling, rewards and existing duel routes remain OPEN.

## What is actually on the map

The area is **BD4000, Dragonspear Castle exterior**, during the final assault.
The remembered northern group exists and already resembles an adventuring party:

| Character | Existing role in the inspected installation |
|---|---|
| Axe Poet | Level-12 fighter with Barbarian rage; axe melee |
| Thasz | Level-12 fighter; dual longswords |
| Alexandria | Level-12 cleric; divine support and healing |
| Dram | Level-12 mage; protections, control and Haste |
| Chloe | Fighter 9 / Thief 13; invisible at the start |
| Bluebeard | Level-12 fighter; heavy crossbow |

The Barghest and Oloneiros are also staged there, then removed if their earlier
incarnations have already died. They cannot be assumed available in every run.
This party is created by the assault cutscene, so an ARE-only actor inventory
would miss it. Current builds are modded-snapshot observations, not proposed
statistics for our component.

There is **another, separate named group**: Ashatiel's existing six escorts,
Wormgums, Small Kimble, Marius of Tethyr, Zoe Kryn, Sarginson and Balvin Steadyhand.
Her introduction creates them in one of two formations depending on the approach.
The northern six are not her existing bodyguard formation.

The [roster audit](24b-ashatiel-roster.md) records builds, gear, current spellbooks,
AI and other named assault actors. The [sequence audit](24a-ashatiel-sequence.md)
records both Ashatiel formations, dialogue paths and progression dependencies.

## Spatial findings and prepared maps

Map art was reconstructed directly from the installed WED/TIS/PVRZ resources;
the ground image is **5120 by 3840 game coordinates**. The local figures annotate
verified current positions, not proposed spawn positions:

- [Whole-area encounter locations](%USERPROFILE%/CEBG-Tests/Ashatiel-20260922/map/BD4000-locations.png)
- [Northern camp and named actors](%USERPROFILE%/CEBG-Tests/Ashatiel-20260922/map/BD4000-northern-party.png)

| Existing landmark | Coordinates | Relevance |
|---|---|---|
| Northern party | x1235–1795, y675–955 | Already has melee, ranged, arcane, divine and stealth roles |
| Ashatiel after duel refusal/cheating | 825,1280 | Existing Crusader Commander location, southwest of that party |
| Ashatiel approach A | 1140,1985 | Existing scripted introduction, with six escorts |
| Ashatiel approach B | 1920,1675 | Alternative introduction, not a second encounter |
| Solo duel | Player1 1400,1805; Ashatiel 1485,1880 | Existing one-on-one staging |
| Inner-gate map marker | 2793,1775 | Later Caelar progression |
| Wall-breach map marker | 3143,3367 | Southeastern assault route |

**Visual assessment:** the northern party occupies a camp enclosure with a
central lane between tents and ruined walls, behind a palisade opening. It
offers an identifiable location and existing ranged/rear positions, but it is
not an empty arena. Tent footprints, wall edges, approaches and the narrow
entrance could matter for line of sight, area spells and bringing the whole
party into combat. The current Ashatiel positions are farther south among the
other tents. Choosing the northern camp changes where the player is directed
and how the existing approach introduction leads into combat.

These are observations from the ground render and scripts. No live pathfinding,
line-of-sight, available-floor-capacity or safe-spawn test has been performed.
The figures show first-frame daytime ground tiles, not current dynamic door
states, actors, animations or spell effects. The search map was extracted for
later placement verification; attractive-looking ground is not proof of a
valid spawn point.

## Reusable work, and the constraints that matter

1. **A complete existing enemy party.** Dram already has sight-triggered
   prebuffs, defensive recasts, finite memorized spells and ally-targeted Haste.
   Alexandria already has divine prebuffs and healing. Their current scripts
   provide a starting point; the new fight does not require inventing every
   combat role. They do not already contain the requested sequencer packages.
2. **Existing entrances and story assets.** The two approach triggers,
   dimension-door arrival, Ashatiel's dialogue and the later gate/Caelar handoff
   are identifiable reusable pieces. They need not all be retained unchanged.
3. **Preparation needs explicit staging.** The northern party's `BDCHALL`
   initializes hostility immediately. The original duel's army ceasefire does
   not pause these actors. They cannot simply be moved beside a buffing party
   and expected to wait. Creating all six alongside Ashatiel means seven enemies;
   including both returning officers makes nine, before ordinary nearby troops.
4. **Victory currently means Ashatiel dies.** Her death advances the siege,
   opens the gate and makes ordinary crusaders retreat. A separate door safeguard
   also watches her death. A party battle must define its victory condition and
   adapt all relevant consumers together, especially if Ashatiel dies first.
5. **The solo rules cannot govern the new fight.** Companion attacks and loss
   of sight currently trigger duel-cheating behavior. Whether the solo option
   survives is open; the new party route must not inherit those penalties.
6. **Reuse must not duplicate identities or rewards.** The northern six already
   award 22,000 total kill XP and carry equipment. Integrating their existing
   encounter must account for its old spawns and loot. Returning named officers
   have earlier death history. Ashatiel's shared CRE has earlier story uses and
   protection/animation items that cannot blindly become new combat defaults.

The [Chosen of Cyric source audit](24c-chosen-of-cyric-reference.md) also prepares
specific patterns worth discussing: a priest clearing allied disables, a mage
supporting damage dealers, finite healing potions, and one-use opening/emergency
packages. Its original ambush removes player buffs and prepares the enemies
while the player is trapped. Those behaviors conflict with our established
starting brief and are not carried forward by this research. Its BG2-level
statistics and spell packages are not a SoD balance baseline.

## Preparation completed before any encounter decisions

- Decoded the effective area and reconstructed its ground map; plotted known
  formations and landmarks.
- Inventoried named actors, current resources, equipment, spellbooks and AI.
- Traced both introductions, dialogue branches, solo/party behavior, army
  ceasefire, duplicate-spawn exclusion, victory and the Caelar handoff.
- Located the actual Rogue Rebalancing reference source and separated useful
  cooperation patterns from unwanted opening behavior and BG2 power levels.
- Identified future focused checks: both approaches create exactly one encounter;
  preparation keeps player control and buffs; its stage/timer survives reload;
  an in-progress player cast is not accidentally cleared; old duel penalties do
  not fire; selected actors engage together; killing Ashatiel first/last produces
  the approved victory result; gate, retreat and Caelar continue once; earlier
  parley, named deaths, loot and unrelated component edits survive.

No installer, creature, AI, dialogue or save was changed. No game was launched.
There is no claim of a balance or compatibility playtest. SCS/SR-modified
resources are useful evidence, but SCS presence does not automatically grant
new encounter actors the desired behavior. Spell identities, memorized spells
and AI guards need to be checked against the install during implementation;
kit/build choices remain undecided.

## Smallest useful next discussion

First choose **whose party this is and where it fights**:

- Incorporate the northern champions into Ashatiel's encounter, keeping their
  distinct roles and deciding how many actually participate.
- Keep the northern fight separate and build around Ashatiel's current escorts.
- Select a smaller group from the existing characters, deciding what happens
  to the unused actors and their original encounters.

The northern party is a promising reuse candidate because it already supplies
the requested adventuring-party structure. That is an assessment, not a roster
decision. Once roster/location are agreed, the warning/preparation sequence,
duel treatment and individual spell/consumable choices can be discussed in turn.

## Reproducibility

Inspected source: `%USERPROFILE%\CEBG-Tests\Combined-20260908\game`, read only.
Scratch evidence: `%USERPROFILE%\CEBG-Tests\Ashatiel-20260922\`, with `map`,
`sequence` and `roster` subdirectories. Map extraction and coordinate-plot scripts,
resource origins/hashes and decoded metadata remain there. The sequence and
roster notes retain selected fingerprints and decompilation boundaries. Original
game art and copied game resources were not added to the repository.

Map format interpretation follows the IESDP references for
[WED](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/wed_v1.3.htm),
[TIS](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/tis_v1.htm), and
[PVRZ](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/pvrz.htm).
