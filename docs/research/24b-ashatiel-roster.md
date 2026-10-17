# Ashatiel preparation: the northern named party and reusable resources

> **2026-09-26 decision:** keep the northern party in place and separate. Its
> builds remain useful reference data; merging it into Ashatiel is no longer an
> open option. See [current design](../design/wave1/09-ashatiel-party-brawl.md).

Research only, 2026-09-22. No encounter design is approved by this document and
no game resources were changed. Companion/roster choices, balance, extra enemies,
and the treatment of the existing northern fight remain OPEN.

## Sources and limits

The effective snapshot inspected was
`%USERPROFILE%\CEBG-Tests\Combined-20260908\game` (read only). Creature data,
scripts and strings were copied/read into a separate research fixture at
`%USERPROFILE%\CEBG-Tests\Ashatiel-20260922\roster`. All WeiDU decompilation
targeted that scratch fixture, never the source installation. The scratch files
`roster.json`, `area.json`, and `decompiled/` retain the detailed observations.

The checked-in baseline `research/data/sod_baf/BDCUT41.baf` and `BDCUT42.baf`
agree with the effective snapshot on the named party's creation coordinates
and the two returning enemies' death checks. These are **modded-install build
snapshots**, not universal vanilla statistics or a balance prescription.
Spell names below come from the effective installed SPL/TLK, so Spell Revisions
changes are reflected rather than inferred from familiar resource numbers.

## The group the user remembers

Yes: the upper/northwestern part of the castle's outer grounds contains an
existing named adventuring party. They are **script-created assault actors**,
not the peaceful/infiltration actors in the BD4000 ARE table. Looking only at
placed actors misses them.

`BDCUT41.baf:106–114` creates six named champions, plus two conditional returning
enemies. Screen coordinates below use the area's top-left origin (x right,
y down). `BDCUT42.baf:195–210` subsequently removes the Barghest and Oloneiros
if their earlier incarnations have already died.

| Character | CRE | Assault coordinate | Effective build / HP | Existing equipment and role |
|---|---|---|---|---|
| Axe Poet | `BDCHAL01` | 1795, 940 | Fighter 12; Barbarian rage; 99 HP | Splint, battle axe +2, heroism and extra healing; melee |
| Thasz | `BDCHAL02` | 1525, 830 | Fighter 12; 99 HP | Plate +1, longswords +2/+1 in weapon/offhand slots, invulnerability and healing; melee |
| Alexandria | `BDCHAL03` | 1650, 675 | Cleric 12; 78 HP | Plate, shield +1, morning star +1, sling +1/bullets +2, Wand of the Heavens, healing; divine support |
| Dram | `BDCHAL04` | 1765, 775 | Mage 12; 42 HP | Robe, staff +1, stunning darts, Wand of Frost, healing; arcane support/control |
| Chloe | `BDCHAL05` | 1235, 955 | Fighter 9 / Thief 13; 102 HP | AC 6 bracers, protection amulet +1, dagger +2, stunning darts, invisibility/healing potions; stealth attacker |
| Bluebeard | `BDCHAL06` | 1705, 845 | Fighter 12; 99 HP | Plate, heavy crossbow +2, lightning/+2 bolts, hammer +1, clarity/healing; ranged attacker |
| The Barghest | `BDBARGH2` | 1590, 915 | Fighter 12; Enrage; 99 HP | Full plate, large shield +1, Chill Axe +2, power/healing; returning melee officer |
| Oloneiros | `BDOLONE2` | 1920, 900 | Mage 13; 43 HP | Staff Spear +2, Asp's Nest darts, AC 6 bracers, protection cloak, Wand of Frost, clarity/healing; returning mage |

Chloe receives `ApplySpellRES("bdinvis","bdchal05")` immediately after creation.
All six champions are in the unconditional assault-setup block; the surrounding
ordinary crusader/mage additions have separate difficulty gates.

Their existing kill rewards total **22,000 party XP** (3k/3k/4k/4k/5k/3k).
Ashatiel is another 5,000; the two returning officers add 3,000/5,000 if present.
These are existing rewards to account for if encounters are combined, not a
recommendation to add more compensation or additional copies of the loot.

This is already a useful palette of melee, ranged, thief, mage and cleric roles.
It does **not** establish that all six should join Ashatiel: that would be seven
enemies before counting either returning officer. Keeping, moving, replacing or
folding their existing fight into the new encounter needs an explicit decision.

## Existing AI and spells worth inspecting before replacing anything

All six champions use `BDCHALL` as override, `BDSHOUT` as race script, no class
script, and the following individual general scripts:

| Character | Combat script | Concrete reusable behavior |
|---|---|---|
| Axe Poet | `BDFIGH32` | Existing barbarian/melee package; finite rage/healing/heroism resources |
| Thasz | `BDFIGH33` | Existing melee/potion package |
| Alexandria | `BDCLER38` | Sight-triggered prebuffs, divine control, heals and support |
| Dram | `BDMAGE37` | Sight-triggered prebuffs, defensive recasts, Haste support, antimagic and control |
| Chloe | `BDTHIE10` | Ambush invisibility, invisibility potions, healing and Poison Weapon resources |
| Bluebeard | `BDFIGH34` | Crossbow attacks, switch to melee within range 5, clarity/healing potions |

The Barghest and Oloneiros also use `BDCHALL` / `BDSHOUT`, with `BDFIGH35`
and `BDMAGE38` respectively. They retain their earlier story death variables
(`bdbarghe`, `bdolonei`) and dialogues; they are not independent duplicate NPCs.

### Dram

The installed spellbook includes Shield, Mirror Image, two Stoneskins, Improved
Invisibility, Globe of Invulnerability, Spell Deflection, Vocalize, Haste,
Greater Malison, Slow, Spell Thrust, Flame Arrow, Hold Person/Monster, Confusion,
Power Word Silence and Chain Lightning, among others. The effective SR-named
list also includes Obscuring Mist and Summon Shadow; do not assume the vanilla
spell at an old SPWI number.

`BDMAGE37` has an existing `bd_prebuff` opening sequence: on detecting an enemy
it consumes and applies available defenses, with difficulty-dependent gates.
The consumed copies matter. For example, Dram has two Stoneskins, enabling a
later recast; the logic does not promise unlimited defenses. Defensive recasts
share `bd_defence_timer` and ordinary casting uses `bd_cast`. Haste already has
ally selection and checks for slowed/unhasted allies, with a separate timer.

This provides implementation material, but it is not a promise that the exact
native priorities fit the new fight. Existing combat spells remain ordinary,
interruptible casts where the scripts use `Spell`; the opening prebuffs use
`RemoveSpell` plus `ReallyForceSpell`.

No sequencer/trigger/contingency actions or corresponding symbolic spell names
were found in the effective `BDMAGE37`, `BDMAGE38` or `BDFMCL01` decompiles.
Adding a chosen opening combination would therefore need explicit new logic;
it is not already a hidden feature of these three scripts.

### Alexandria

Her opening code includes Armor of Faith, Defensive Harmony, Draw Upon Divine
Might, resistance and Free Action checks. Prepared spells also include Bless,
Resist Fear, Silence, Hold Person, Miscast Magic, Holy Smite, Invisibility Purge,
Mental Domination, two Mass Cures and two Aerial Servants. Her finite spellbook,
healing potion and Wand of the Heavens can support a coherent enemy party
without inventing a new cleric resource.

## Ashatiel herself

`BDASHATI.CRE` is a Fighter/Mage/Cleric **9/10/9**, **67 HP** in this snapshot.
Scripts: `BDASHATI` override, `BDSHOUT` race, `BDFMCL01` general. Dialogue:
`BDASHATI`. Her resource is used by earlier story scenes as well as this fight.

Current gear includes a throwing dagger, mace +2, small shield +2, AC 5 bracers,
Ring of Free Action, Golden Girdle, protection cloak +1, extra healing, magic
shielding, and a Wand of Frost. She also carries `MINHP1` and a special
`BDERINYE` animation item: blindly cloning the inventory or changing the shared
CRE globally would carry story/cutscene behavior into the new combatant.

Her existing prepared magic includes Mirror Image, Stoneskin, Minor Globe,
Spell Deflection, Breach, Secret Word, Slow, Flame Arrow, Greater Command,
Holy Smite, Silence and healing. Exact loadout, protection timing, removal of
story protection, and her role remain design decisions.

## Ashatiel's own six escorts: a second existing roster

The northern champions are **not** Ashatiel's existing six escorts. Her native
encounter already brings another mixed party, `BDASHA01–06`, created by the two
route-dependent branches in `BDEXDUEL.baf:22–28` and `69–75`. The first branch
places them around x1075–1200/y1930–2035; the second around
x1865–1995/y1580–1665. Neither is the northern champions' location.

The same read-only snapshot supplied these builds. Full item/spell data are in
scratch `roster/escorts.json`, with decompiles in `roster/escorts-decompiled/`;
the earlier roster evidence was retained separately. CRE/ITM/SPL signatures and
KEY-to-BIFF resource types/ordinals were checked during this extraction.

| Escort | CRE | Effective build / HP | Existing combat role and resources | General combat script |
|---|---|---|---|---|
| Wormgums | `BDASHA01` | Gnoll Fighter 10; 93 HP | Halberd +2, three Barbarian Rages, invulnerability and healing; frontline | `BDFIGH01` |
| Small Kimble | `BDASHA02` | Gnome Mage 11; 41 HP | Wand of Paralyzation, stunning darts, two Hastes, Greater Malison, Confusion, Fireball, Hold Monster, Mirror Image/Blur/Shield; arcane control/support | `BDMAGE01` |
| Marius of Tethyr | `BDASHA03` | Human Paladin 10; 93 HP | Plate +1, shield +1, longsword +1, stone giant strength/healing, Armor of Faith/Bless/Lay on Hands; armored melee | `BDPAL01` |
| Zoe Kryn | `BDASHA04` | Halfling Fighter 8 / Thief 10; 70 HP | Studded leather +1, shortsword +1, invisibility/healing potions, two Set Snares; stealth/melee | `BDFTHI01` |
| Sarginson | `BDASHA05` | Human Fighter 7 / Mage 10; 82 HP | Composite longbow +1, fire arrows, longsword +1, Wand of Frost, Haste, Spell Thrust, Mirror Image, Improved Invisibility, control spells; archer/caster | `BDFMAG01` |
| Balvin Steadyhand | `BDASHA06` | Dwarf Fighter 9 / Cleric 9; 81 HP | Plate, shield +1, hammer +1, sling +1/bullets +2, Wand of the Heavens, Defensive Harmony, Free Action, Silence, healing; divine support/melee | `BDFCLE01` |

All six use **`BDDSC` override, `BDCRUSDS` class, `BDSHOUT` race**, their
individual general script above, and the generic `BDCRUS` dialogue. This differs
from the northern group's `BDCHALL` setup. `BDCRUSDS` initializes lane movement,
sets `bd_no_retreat=1`, and makes them hostile while Ashatiel is alive; `BDDSC`
also owns duel and castle-phase behavior. These are not generic AI-only donors.
Their combined native kill reward is **14,000 party XP**, plus Ashatiel's 5,000.

Both existing rosters already have complementary roles. Choosing whether to
improve her own escorts, draw from the northern group, or combine selected
members is therefore the useful next design discussion; there is no technical
need to invent a complete roster first. This inspection does not add either
party to the other or approve a thirteen-character fight.

## Reuse boundaries and implementation traps

- `BDCHALL` immediately sets `HOSTILES3`, calls `Enemy()`, and sets
  `bd_no_search=1`. Reusing the actors unchanged next to the party would not
  provide the requested 30-second safe preparation window. A new preparation
  phase must own their activation; disabling only their general AI is inadequate.
- `BDSHOUT` contains shared assistance, search and retreat behavior. The
  `bd_no_search` setting limits searches; it does not create an isolated arena
  or guarantee the entire group engages together. Ally buffs may affect nearby
  eligible crusaders, not only the intended new encounter roster.
- These champions do **not** use the ordinary army's `BDDSC` script.
  Its duel ceasefire, area-victory retreat and death cleanup therefore do not
  automatically govern them. Each relevant phase must be checked against
  their actual `BDCHALL` / `BDSHOUT` / general-script stack.
- `BDMAGE37`, `BDCLER38` and the other general scripts are reusable resources,
  but changes to a shared script can affect other creatures. New encounter-only
  variants can avoid altering unrelated users; whether to clone or move the
  existing named actors is still OPEN.
- Preserving named identities includes preventing duplicate spawns and duplicate
  loot. Barghest/Oloneiros additionally need their earlier death history honored.
- Area-wide victory currently keys off Ashatiel's death. A surviving enemy party
  must not be left behind when the castle declares victory. The sequence audit
  must determine the new completion contract before implementation.
- Spell Revisions can relocate/redefine spell resources, and SCS adds spell
  markers and item infrastructure to these CREs. Installed spell identities,
  known/memorized spell lists and AI must agree. Existing `DW#HASPT`/`DW#RND*`
  items in the snapshot are mod infrastructure, not proposed encounter loot.
- Group spawn changes belong to assault setup, including the effective
  cutscene-skip behavior, not blanket edits to BD4000's earlier peaceful roster.

An exact-name scan of the effective override BCS/DLG files found `BDCHAL01–06`
only in `BDCUT41.BCS`; the checked-in SoD script corpus likewise references them
only there. This supports a relatively self-contained six-person group, but
does not prove that external mods, string-built references or save data cannot
refer to them. Snapshot fingerprints: `BDCUT41.BCS`
`0c34f610bec2785c3ecd53fe7772b5246863ce223d3e639b5dff0b6c0b1ac2e9`,
`BDCHALL.BCS`
`cb99a31df93b2d28fce98aa23c82b26ff30fb85ecb734c5323b5248da435be36`.

## Other nearby resources, without committing them to the fight

The approach southwest of this party already has Tristian (`BDTRIST2`,
1020,1310; Paladin 10, 93 HP), with `BDCRUW45` (1045,1255; Mage 10) and
`BDCRUC45` (930,1325; Cleric 10), plus melee troops. These are a distinct
approach encounter, not members of the six-person northern group.

Other named assault returns include Commander Dreon, Sallo, Ravoc, Damarr,
Leopas, Valis, Delton, Corinth and Beno Famari around the central army; Gnarg
Big-Bug and his mercenaries/trolls occupy the eastern wall-breach sector.
Delgar Munsch, Kharm and Hormorn have earlier Bridgefort outcome/death gates.
Using them as guaranteed new roster members would require decisions about
their existing quests and prior deaths. They are less self-contained donors
than the six northern champions.

## Chosen of Cyric reference: available locally

The installed Rogue Rebalancing sources are present under
`game/rr/rr_cyric/compile`, with the component's detailed notes in
`game/rr/doc/rr_cyric.html`. Its documented combat baseline is a six-character
party with roughly **2.95–4 million XP per character**; its numbers, high-level
spells and gear must not be treated as a suitable SoD baseline.

Useful patterns to evaluate together are complementary party roles, finite
consumables, situational target selection, allies curing each other, and bounded
sequencers/contingencies. Its published explanation emphasizes normal
interruptible combat casting, class/level-appropriate abilities and limited
sequencer types. The reference prepares its own party during a two-round
sequence while the player is trapped; that is distinct from the user's agreed
brief of roughly 30 seconds of player-controlled preparation with buffs kept.

This research does not adopt its ambush barrier, gear, anti-illusion advantages,
backstab cadence or difficulty scheme. Its documentation licenses code and
documentation under CC BY-NC-SA 3.0; any actual source reuse needs attribution
and a license check rather than silent copying. The fight's patterns can be
discussed without importing its assets or adding a dependency.

The source implementation qualifies the prose promise: `rr#seli.baf` uses
`ReallyForceSpell` to implement its one-use contingency/sequencer payloads,
guarded by `RR#CHCntg`, `RR#Cntg`, `RR#Trig` and `RR#Seq` locals. It uses a
separate global phase gate (`RR#CSAVE`) and ordinary casting cooldown, as well
as silence/immobility/death/charm checks. This is a concrete reference for
bounded scripted combinations; it does not mean all RR casts are ordinary
`Spell` actions or that those exact BG2-level combinations should be copied.

## Discussion-ready choices (not decisions)

1. Use the existing northern location, the current Ashatiel approach, or another
   map position after the map/route inspection.
2. Make the northern champions Ashatiel's allies, use only selected members, or
   preserve their encounter separately and create encounter-specific copies.
3. If incorporating them, establish which party members remain and whether
   Barghest/Oloneiros can participate conditionally without varying the fight
   too much or resurrecting dead NPCs.
4. Decide how the preparation window starts, where actors wait/spawn, and what
   happens if the party retreats or attacks before it ends.
5. Only then select Ashatiel's role, spells, prebuffs, sequencers, consumable
   budgets, difficulty changes, reward treatment and victory condition.
