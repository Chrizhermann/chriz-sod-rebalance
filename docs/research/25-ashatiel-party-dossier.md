# Ashatiel brawl: current opponents and the decisions to make

Read-only audit, 2026-09-26. This is a factual starting point for discussion,
not a chosen new loadout. Ashatiel's six original escorts are examined as
available candidates; retaining all six has not been decided. The separate
northern party remains untouched. The [current design](../design/wave1/09-ashatiel-party-brawl.md)
governs the arena, player reset, early contact, timed advance and victory.

## Main finding

They already have substantial native SoD combat AI: conditional preparation,
defensive reactions, target checks, potions, support magic and weapon fallback.
They do **not** currently form a deliberately coordinated SCS-style party, and
their long generic scripts contain many branches their actual spellbooks cannot
use. None of these seven has a sequencer/contingency package in its current
assigned general script.

The most useful work is to make each role coherent and give it a deliberate
opening and finite reserves. Adding every protection from a reference fight
would miss that point. SCS Drasus and Chosen of Cyric are references for the
questions we should ask, not approved spell/equipment shopping lists.

## What was inspected

Effective creatures, their complete prepared spellbooks, equipped items and
consumables, assigned combat and encounter scripts, current spell/item contents,
and difficulty/time identifiers from the read-only Combined test installation:
`%USERPROFILE%/CEBG-Tests/Combined-20260908/game`.

This includes Spell Revisions, SCS, Artisan's Kitpack and other installed changes.
It is not a claim that unmodified SoD or every mod combination has these exact
spell effects. SCS is installed, but these seven still use native `BD*` combat
scripts. Current CRE/combat-script bytes match the previous September 22 capture.
No game was launched or modified; effective combat stats, ally buff coverage,
timing and balance still require later engine checks.

Detailed evidence:

- [Arcane AI, full spellbooks, actual opening guards and recasts](25a-ashatiel-arcane-ai.md)
- [Martial/divine AI, support, consumables and kit interactions](25b-ashatiel-martial-divine-ai.md)
- [SCS Drasus and Chosen of Cyric reference checklist](25c-scs-drasus-design-checklist.md)
- [All seven builds, complete inventories, prepared spell counts and stored effects](25d-ashatiel-party-resource-ledger.md)

## Existing builds and resources

HP here is stored CRE HP, before runtime buffs/difficulty. Gear listed is what
they carry, not a promise that every item becomes loot. The full ledger separates
inventory flags, quantities, hidden story items and mod initialization markers.

| Character | Existing build | HP | Principal equipment | Finite consumables |
|---|---|---:|---|---|
| Ashatiel | Elf Fighter 9 / Mage 10 / Cleric 9 | 67 | Mace +2, throwing daggers, small shield +2, AC 5 bracers, Free Action ring, Golden Girdle, protection cloak +1, robe | 2 Extra Healing; 1 Magic Shielding; 5 Frost wand charges |
| Wormgums | Gnoll Fighter 10, Barbarian kit | 93 | Halberd +2, hidden helmet | 2 Extra Healing; 1 Invulnerability; 3 prepared Rages |
| Small Kimble | Gnome Illusionist 11 | 41 | Dagger and 20 stunning darts; no armor-defense robe in this inventory | 1 Extra Healing; 4 Paralyzation wand charges |
| Marius of Tethyr | Human Cavalier 10 | 93 | Plate +1, large shield +1, longsword +1 | 2 Extra Healing; 1 Stone Giant Strength; 1 Lay on Hands |
| Zoe Kryn | Halfling Fighter 8 / Thief 10 | 70 | Studded leather +1, shortsword +1 | 1 Extra Healing; 4 Invisibility |
| Sarginson | Human Fighter 7 / Mage 10 | 82 | Composite longbow +1, 40 fire arrows +2, longsword +1 | 1 Extra Healing; 4 Frost wand charges |
| Balvin Steadyhand | Dwarf Fighter 9 / Cleric 9 | 81 | Plate, medium shield +1, war hammer +1, sling +1, 40 bullets +2 | 1 Extra Healing; 1 Clarity; 2 Heavens wand charges |

The current seven total 527 stored HP and 19,000 kill XP. That is a reference
total, not a proposed reward or difficulty target. Sarginson has four longbow
proficiency points but two **shortsword** points while carrying a **longsword**;
that mismatch is worth resolving if his melee fallback is meant to matter.

## What they currently prebuff with

The table gives the fullest normal hostile opening supported by their current
books, corresponding to script difficulties 3/4/5 (Core/Hard/Insane on the
ordinary slider). It is a static initial-book analysis, not a capture of active
effects. Exact availability guards and lower-difficulty differences are in the
AI reports.

| Character | Existing initial spell preparation | Later/conditional personal preparation |
|---|---|---|
| Ashatiel | Armor of Faith, Aid, Draw upon Divine Might, Stoneskin, Minor Globe | Magic Shielding potion; Mirror Image and Spell Deflection are conditional reserve defenses |
| Small Kimble | Blur, Shield, Protection from Missiles, Mirror Image, Improved Invisibility, Minor Globe | Shadow Door and Spell Deflection can provide later replacement defenses; Haste is an ordinary ally-support cast |
| Sarginson | Shield, Protection from Normal Weapons, Mirror Image, Improved Invisibility, Minor Spell Deflection | One remaining Mirror Image; Haste is an ordinary ally-support cast |
| Balvin | Armor of Faith, Defensive Harmony, Draw upon Divine Might, Free Action | Clarity potion; Chant as ordinary group support |
| Wormgums | No instant multi-spell opening chain | Rage on enemy sight; Invulnerability potion through normal combat actions |
| Marius | No instant multi-spell opening chain | Protection from Evil when enemy alignment/proximity warrants it; Stone Giant Strength potion |
| Zoe | No spell-based preparation | Invisibility potion, which can be used before sight once she is hostile |

The native caster opening requires enemy detection and spends prepared copies.
Merely spawning them hostile and out of sight does not guarantee our agreed
already-prepared start. Staging needs to establish selected starting buffs and
prevent duplicate preparation, while preserving immediate reactions to early
player contact. No staging implementation was selected in this audit.

A 30-second preparation window also ages their buffs. Balvin's current SR
Defensive Harmony and Draw upon Divine Might last one turn; Wormgums's effective
Artisan's Rage lasts only five rounds (30 seconds). Short combat abilities need
deliberate activation timing rather than being spent at the start of the wait.

There is also a concrete compatibility concern for Haste: the effective SR
spell uses different effect/state markers from those checked by this native
AI. That can let a caster waste a later Haste on an already-buffed ally.
Ashatiel's Free Action ring does not block the movement/APR benefits of this
particular installed spell, although it can hide the icon. These are static
resource findings; the new AI needs a focused SR/non-SR delivery and recast check.

## Each person's actual combat job and limitations

### Ashatiel: hybrid leader, anti-magic and divine pressure

- Her significant offensive/support book includes Breach, Secret Word, Slow,
  Greater Command, Silence twice, Holy Smite twice, Flame Arrow twice, Chant,
  Resist Fear, Detect Invisibility and Invisibility Purge. She has no Haste.
- Healing/defense can take priority over attacking: Sanctuary below 65% HP,
  protected self-healing, potions, Vocalize against silence, and defensive
  spell recasts. Her two Cure Critical Wounds are the current SR spells,
  despite an older symbolic name in the script.
- She has **one Stoneskin total**. If it is spent opening, the script cannot
  invent another. Two Mirror Images and one Spell Deflection are useful reserves,
  subject to their state/target/cooldown checks. Recasts share a 15-second
  defensive timer; normal casting also costs her action time.
- Weapon fallback is mace in close combat and throwing daggers at range.
  Several major roles compete for one actor's actions; not everything happens
  simultaneously or in a fixed sequence.
- Her story `MINHP1` item is removed by the existing introductory dialogue.
  A new combat actor must respect that removal; story protection is not a
  fair combat buff. Her permanent Free Action ring is a separate gear choice.

**Discussion focus:** how much of her identity is frontline leader versus
spellcaster, which existing anti-magic/control tools define her, and how many
defensive recoveries she should have. A full wizard, full cleric and full fighter
opening on one actor is not automatically necessary.

### Small Kimble: fragile control/support caster

- Existing pressure: Greater Malison, Confusion, Hold Monster, Waves of Fatigue,
  Fireball, Flame Arrow, four Magic Missiles, stunning darts and Paralyzation wand.
  Two Hastes provide potential martial support.
- She has only 41 HP and **no Stoneskin**, despite generic script branches for
  it. One Mirror Image remains after normal preparation; Shadow Door and Spell
  Deflection offer conditional replacements. Vocalize is available.
- Her AI does not guarantee Malison before the disabling spells. Fireball
  requires a safe enemy cluster with no nearby ally; the tight arena can make
  that cast unavailable. She switches to a dagger in melee rather than using
  an elaborate retreat routine.
- She has no prepared Breach, Secret Word, Spell Thrust or dispel. Do not count
  generic anti-mage branches as tools she actually possesses.

**Discussion focus:** a clear control/support identity, enough defense to
participate, a deliberate opening priority, and a remaining vulnerability.
Whether to add Stoneskin or change her defenses remains open.

### Sarginson: ranged pressure with arcane support

- His bow and fire arrows can provide pressure between spells. Existing spells
  include one Haste, Spell Thrust, Emotion: Hopelessness, Horror, Feeblemind,
  Melf's Acid Arrow, Obscuring Mist and two Magic Missiles.
- He has **no Stoneskin and no Vocalize**. Protection from Normal Weapons does
  not protect against the player's magical weapons. One Mirror Image remains
  after full preparation; most other defenses have only one prepared copy.
- There is no automatic sequencer and no special kiting controller. He switches
  to melee within range 5. His sword/proficiency mismatch is noted above.
- No Breach, Secret Word, Greater Malison, Fireball or summon is prepared.

**Discussion focus:** make ranged disruption and limited support meaningful
without turning him into a second copy of Kimble or another complete mage.

### Balvin: durable support and recovery

- His opening includes actual self-defense and Defensive Harmony. Whether the
  latter covers teammates depends on the effective spell's delivery and their
  positions; it is not proof of whole-group coverage.
- Existing support includes Chant, Remove Paralysis, Invisibility Purge, Slow
  Poison, Sanctuary/self-healing, one Mass Cure and a Clarity potion. He also has
  Command twice, Hold Person twice, Silence, Miscast Magic and Doom.
- One copy of each starting protection means **no repeated full prebuff cycle**.
  The later Defensive Harmony branch normally has no copy left after opening.
  Gust of Wind is prepared but has no matching cast branch.
- Hammer/sling fallback and the Heavens wand make him useful when not casting.
  Sanctuary/healing or control can postpone other support; the AI does not
  execute every helpful response at once.

**Discussion focus:** which allies he prioritizes, one or two meaningful rescue
tools, and finite group healing. Decide which buffs he supplies for the group
instead of giving everyone duplicate protections.

### Wormgums: direct melee threat

- Halberd, high physical attributes, three Rages, one Invulnerability potion
  and two heals already provide a straightforward role. No ranged weapon is
  carried and his AI primarily attacks the nearest visible enemy.
- His effective Artisan's Rage is not the vanilla ability: at level 10 it gives
  +6 STR/CON for 30 seconds, followed by a fatigue/reuse lock. The existing AI
  checks a marker that expires before that lock ends, so it may spend a later
  Rage while the lock blocks it. This is a static compatibility concern, not
  a live-observed failure.
- His Barbarian kit marker and Rage book do not by themselves prove every kit
  passive is installed on this NPC. The full resource ledger avoids inventing
  final physical resistance, movement or APR numbers.

**Discussion focus:** opening-contact Rage, reliable finite use, and whether
support such as Haste makes his existing weapon pressure sufficient.

### Marius: armored paladin and limited ally support

- Cavalier 10, plate/shield, strength potion, two heals and Lay on Hands. He can
  react to an evil enemy with Protection from Evil and use Remove Fear on a
  panicking ally. Both latter abilities have six prepared uses.
- **Bless and Armor of Faith are prepared but never cast by his current AI.**
  Detect Evil is also unused. He has no prepared Inquisitor dispel/True Sight;
  generic paladin script branches do not grant those abilities.
- No ranged weapon is carried. The present attack loop is simple nearest-enemy
  melee, not a designated bodyguard behavior.

**Discussion focus:** an anchor/protector identity distinct from Wormgums, whether
to use his existing neglected spells, and which modest support action matters.

### Zoe: finite invisibility and melee opportunities

- Four Invisibility potions can conceal her before contact and let her attempt
  further attacks after revealing herself. Her one healing potion competes with
  the higher-priority invisibility behavior for action time.
- The script has no trap placement, poison use, actual Hide action, flanking
  routine or deliberate vulnerable-caster selection. Two prepared Set Snares
  are unused. A separate direct-invisibility ambush branch requires Hide 150;
  her base skill is zero and direct equipment/CRE effects do not supply it.
- She attacks the nearest visible enemy with her shortsword. Invisibility can
  allow a backstab, but positioning, facing and target susceptibility still
  matter; the existing AI does not guarantee one.

**Discussion focus:** meaningful target choice and a limited number of recovery
opportunities, without reproducing CoC's repeated ambush/trap pressure by default.

## What the reference encounters contribute

### SCS Drasus

The installed encounter-specific component adds two levels to the four enemies
and two potions to Drasus. Much of the fight's competence comes from generic
SCS AI, differentiated caster roles, usable equipment and a shared alert.

At maximum supported preparation, effective Kysus can have Shield, Protection
from Missiles, Stoneskin, Mirror Image, Shadow Door, Minor Globe and Spell
Deflection; Rezdan's package is Mage Armor, Stoneskin, Mirror Image and Minor
Globe. These remain configurable/difficulty-dependent, not universal stacks.

Kysus has spare Images and an offensive two-Color-Spray Minor Sequencer;
Rezdan has a defensive Mirror Image + Blur sequence. Recasts cost available
spells and casting time. The interesting principle is **different jobs and
finite recovery**, not copying those exact packages to all Ashatiel casters.

### Chosen of Cyric

Useful patterns: distinct roles, selective ally rescue, finite consumable
recovery, separate opening/emergency sequences, and encounter-wide completion
before removing barriers. Its BG2 spell level, forced-effect tricks and unfair
opening are not an assumed SoD baseline. The agreed player rest/preparation
and current arena rules remain authoritative.

## How to approach scaling together

These are suggested discussion axes, not selected difficulty packages:

1. **Role and roster first:** choose who participates and the one principal job
   of each member. Seven independently strong actors already create substantial
   action pressure before any level/HP increase.
2. **A defined baseline opening:** select defenses and ally buffs that let the
   party function; decide the starting buff cost and remaining spellbook.
3. **Finite recovery:** count spare Images/skins, heals, potions and rescue casts.
   Preserve ways to interrupt, remove, resist or outlast them.
4. **Higher-difficulty coordination:** choose useful target priority, dependable
   support and perhaps selected once-only packages. No blanket sequencers,
   perfect immunities or extra bodies are implied.
5. **Opening pressure:** consider simultaneous control, dispels and weapon damage
   together. An individually reasonable caster can become oppressive when
   multiplied across this group.
6. **Resource compatibility:** resolve actual SR spells and kit powers, check
   permanent item interactions and buff delivery, and retain the non-SR route.
7. **Reward budget:** decide combat gear separately from post-fight loot; account
   for consumed items rather than granting every carried resource afterward.

The native scripts chiefly distinguish Normal versus Core+; these caster
prebuff sets are the same at Core, Hard and Insane, with only limited action
priority differences such as Haste's weighted fall-through. Engine damage and
other installed difficulty systems are separate and were not measured here.
There is no existing carefully differentiated Insane brawl package to inherit.

Start the design conversation with Ashatiel's role and defenses, then the
other participating members individually. No loadout changes, difficulty tiers,
new sequencing or equipment additions have been implemented by this audit.
