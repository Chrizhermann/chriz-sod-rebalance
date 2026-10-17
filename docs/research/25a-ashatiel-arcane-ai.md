# Ashatiel and her arcane escorts: current spellbooks and AI

Research snapshot: 2026-09-26. This records existing behavior, not an approved
new loadout. The northern champions remain separate. The new brawl's reset,
already-hostile staging and preparation period are governed by the
[current design](../design/wave1/09-ashatiel-party-brawl.md).

## Evidence and scope

Source installation, read only:
`%USERPROFILE%\CEBG-Tests\Combined-20260908\game`.
The September 22 decompiles and creature inventories in
`%USERPROFILE%\CEBG-Tests\Ashatiel-20260922\roster` were checked against the
current source bytes. All three CREs and all three general combat BCS files are
unchanged. Current `SPELL.IDS`, `DIFFLEV.IDS`, and `GTIMES.IDS` were read directly.
The current effective SPL/ITM names and higher-priority BCS/DLG resources were
also rechecked: 95 actor-resource/name/stack observations passed, with no drift
from the captured inventories/decompiles. Both inspected wand ability headers
use depletion mode 1, consistent with their finite CRE instance charges.
No game, save, installation or recovery ledger was modified; no live encounter
was run.

Detailed extraction, available-memorization flags, selected script blocks and
hashes are in the separate scratch directory
`%USERPROFILE%\CEBG-Tests\Ashatiel-20260926\caster-audit` (`audit.json`,
`ids.json`, `resources.json`, and `*-held-blocks.txt`). References such as
`BDMAGE01:89-101` below refer to the effective decompiled BAF, not an upstream
template. `BDFMCL01` and `BDASHATI` are in `roster/decompiled`; `BDMAGE01`,
`BDFMAG01`, `BDDSC`, and `BDCRUSDS` are in `roster/escorts-decompiled`.

These actors retain **native SoD general combat scripts**, not a generated SCS
mage script. SCS-related inventory markers do not change that observation.
Their empty Known Spells tables do not mean they cannot cast: Ashatiel has 34,
Kimble 23, and Sarginson 15 memorized records, all with availability flag 1.
Counts below are initial prepared copies, before prebuff consumption.

## What the existing opening actually does

All three scripts start with two combat-suppression checks. A
`bd_no_combat=2` actor is stopped; the retreat/no-combat combination can also
stop the general script. Eligible prebuffs then require:

- local `bd_prebuff=0`;
- `Detect(NearestEnemyOf(Myself))`, not an unconditional OnCreation cast;
- the difficulty gate and a matching available `HaveSpell`;
- any additional negative spell-availability guards described below.

Each selected opening block explicitly removes one prepared copy, uses
`ReallyForceSpell(Myself,spell)`, and continues scanning. The final opening block
sets `bd_prebuff=1` and a four-second defense delay. The forced prebuff action
has zero casting time and does not itself require a memorized copy; the
preceding availability check and removal provide the accounting. `Continue`
can defer execution of collected actions until the scan completes, so the
negative availability checks must not be read as a promise to cast every
listed alternative in succession. [IESDP action reference](https://gibberlings3.github.io/iesdp/scripting/actions/bgeeactions.htm#36)

`Detect` can detect through hearing as well as sight and is not defeated by
Hide in Shadows. Consequently this is not the same trigger as direct visual
contact, nor does merely spawning enemies out of player view establish our
new preparation contract. [IESDP Detect reference](https://gibberlings3.github.io/iesdp/scripting/triggers/bgeetriggers.htm#0x4074)

### Difficulty, using the installed identifiers

The authoritative installed file is **DIFFLEV**, not DIFFMODE:
`1 EASIEST`, `2 EASY`, `3 NORMAL`, `4 HARD`, `5 HARDEST`.
These are script symbols; `NORMAL` here must not be casually substituted for a
similarly named UI setting. The tables use the numeric values to avoid that
ambiguity. An `Allegiance(Myself,GOODCUTOFF)` alternative bypasses many enemy
difficulty restrictions if an actor becomes allied/charmed; the table assumes
the intended hostile encounter.

| Actor | Difficulty 1 | Difficulty 2 | Difficulty 3, 4 or 5 |
|---|---|---|---|
| Ashatiel | No native opening prebuff | Stoneskin and Minor Globe each have a half-range random gate | Armor of Faith, Aid, Draw upon Divine Might, Stoneskin, Minor Globe |
| Small Kimble | No native opening prebuff | Protection from Missiles, Mirror Image, Improved Invisibility and Minor Globe each have a half-range random gate | Blur, Shield, Protection from Missiles, Mirror Image, Improved Invisibility, Minor Globe |
| Sarginson | No native opening prebuff | Protection from Normal Weapons, Mirror Image, Improved Invisibility and Minor Spell Deflection each have a half-range random gate | Shield, Protection from Normal Weapons, Mirror Image, Improved Invisibility, Minor Spell Deflection |

This is the **fresh-book selection** supported by the script, not a live capture
of active effects. Random gates share script-tick random state; they are not
independent coin flips. The exact tests are `RandomNum(2,1)` for weapon/missile
protection, `RandomNum(2,2)` for skin/images, `RandomNumLT(4,3)` for invisibility,
and `RandomNumGT(4,2)` for globe/deflection. No stronger prebuff tier appears
between difficulties 3, 4 and 5 in these three scripts. Ordinary recasting still
exists on difficulty 1; “no prebuff” does not mean “no defenses ever.”
[IESDP random-trigger reference](https://gibberlings3.github.io/iesdp/scripting/triggers/bgeetriggers.htm#0x4047)

### Available alternatives and the guards that exclude them initially

| Actor / alternative | Exact additional guard | Initial implication |
|---|---|---|
| Ashatiel: Mirror Image | `!HaveSpell(WIZARD_STONE_SKIN)` | She initially holds one Stoneskin; do not count two opening Images as extra layers |
| Ashatiel: Spell Deflection | No Shield of the Archons, Minor Globe or Globe available | Her Minor Globe is held initially; Deflection is a reserve candidate |
| Kimble: Shadow Door | `!HaveSpell(WIZARD_IMPROVED_INVISIBILITY)` | Improved Invisibility is held; Shadow Door is a later replacement candidate |
| Kimble: Spell Deflection | No Shield of the Archons, Minor Globe or Globe available | Minor Globe is held; Deflection is a reserve candidate |
| Sarginson: Minor Spell Deflection | No Spell Deflection, Shield of the Archons, Minor Globe or Globe available | All those stronger alternatives are absent, so this opening branch is eligible |

Ashatiel prebuff sources: `BDFMCL01:19-31,47-59,89-101,286-321,378-397,417-437`.
Kimble/Sarginson opening sources: their respective scripts `:19-303` (the arcane
opening layout is shared). A later altered spellbook can change these choices;
the exact amount of stacking should be sampled in the first isolated AI test.

## Ashatiel — Fighter 9 / Mage 10 / Cleric 9

Her role already mixes frontline attacks, anti-magic, divine control and
self-preservation. There is no sequencer/trigger/contingency package in
`BDFMCL01`, and none of those spells is prepared.

### Complete prepared book

These are effective installed spell names, including Spell Revisions changes.

| Prepared magic | Copies |
|---|---:|
| Resist Fear (`SPPR108`) | 2 |
| Sanctuary (`SPPR109`) | 2 |
| Armor of Faith (`SPPR111`) | 1 |
| Command (`SPPR102`) | 1 |
| Silence (`SPPR211`) | 2 |
| Draw upon Divine Might (`SPPR214`) | 1 |
| Aid (`SPPR201`) | 1 |
| Chant (`SPPR203`) | 1 |
| Slow Poison (`SPPR212`) | 1 |
| Invisibility Purge (`SPPR309`) | 1 |
| Holy Smite (`SPPR313`) | 2 |
| Cure Critical Wounds (`SPPR401`) | 2 |
| Greater Command (`SPPR512`) | 1 |
| Obscuring Mist (`SPWI106`) | 2 |
| Magic Missile (`SPWI112`) | 2 |
| Detect Invisibility (`SPWI203`) | 1 |
| Mirror Image (`SPWI212`) | 2 |
| Vocalize (`SPWI219`) | 1 |
| Flame Arrow (`SPWI303`) | 2 |
| Slow (`SPWI312`) | 1 |
| Minor Globe of Invulnerability (`SPWI406`) | 1 |
| Stoneskin (`SPWI408`) | 1 |
| Secret Word (`SPWI419`) | 1 |
| Breach (`SPWI513`) | 1 |
| Spell Deflection (`SPWI522`) | 1 |

The effective Cure Critical spell occupies `SPPR401`; the decompiler labels its
cast `CLERIC_CURE_SERIOUS_WOUNDS`. Resource contents and prepared/cast identity,
not the old symbolic English name alone, establish the actual spell here.

### Opening, emergency response and priorities

- **Opening protection:** the table above. She has no Shield, Blur, fire shield,
  Spirit Armor, Improved Invisibility, Free Action spell, or Magic Resistance
  spell prepared, despite generic branches for those options.
- **Sanctuary/heal:** below 65% HP, seeing an enemy, not already sanctuaried or
  silenced, and with a healing spell/potion available, she can spend a Sanctuary
  at difficulty 3+. The action removes the copy then uses `ForceSpell`, not
  `ReallyForceSpell`. Cure Critical Wounds is then available below 80% HP while
  sanctuaried, untargetable, or not seeing an enemy (`:505-527,614-626`).
- **Poison and silence:** Slow Poison reacts to her being poisoned (`:540-548`);
  Vocalize reacts to silence (`:690-698`). Both spend her one copy. The general
  script can pause with `NoAction` while Sanctuary remains active, HP is below
  80%, an enemy is visible and a healing resource remains (difficulty 2+),
  after its higher-priority healing opportunities (`:700-715`).
- **Items:** two Extra Healing potions, one Magic Shielding potion, Wand of
  Frost with five initial charges. Extra Healing is considered below 75% HP at
  difficulty 2+, weighted 100 use / 50 fall-through. Magic Shielding also needs
  a visible enemy, the defense timer expired, `bd_no_innates=0`, and spell save
  worse than -5 (`:656-671,717-735`). It is a combat potion, not an unconditional
  initial prebuff. The wand is a later damage option (`:3845-3859`).
- **Defensive recasts:** Mirror Image only when neither Images nor Stoneskins
  remain; Spell Deflection and Minor Globe only without `BUFF_PRO_SPELLS` and
  with a visible enemy caster. The script also knows how to recast Stoneskin,
  but her only prepared copy normally went into opening protection. She does
  not have repeated Stoneskins hidden in the AI (`:1071-1250`).
- **Offense/support order among actually held spells:** conditional Holy Smite
  (`:1381`), invisibility removal (`:1673-1776`), Breach against combat protections
  (`:1869,1926`), Secret Word against spell protection (`:1986`), Slow against
  hasted/grouped opponents (`:2056,2121`), Chant with four allies nearby
  (`:2406`), Resist Fear for a panicked ally (`:2575`), Greater Command
  (`:2927`), Silence against isolated enemy spellcasters (`:3098`), Command
  (`:3652`), Obscuring Mist (`:3745`), Flame Arrow (`:3803`), Frost wand, then
  Magic Missile (`:3891`). This is conditional priority, not a fixed rotation.
- **Haste:** there are generic Haste branches, but she has no Haste prepared.
  Resist Fear and Chant are ordinary combat support, not currently part of her
  forced prebuff stack. Her initial Armor of Faith/Aid/Draw upon Divine Might
  have no corresponding ordinary recast branches in this script.
- **Weapon fallback:** equip the most damaging melee weapon if an enemy is
  within range 5; otherwise equip ranged and attack. Her available weapon
  choices are the Mace +2 and 20 throwing daggers (`:3936-3951`).

Her static equipped defenses include AC-5 bracers, Small Shield +2, protection
cloak, Golden Girdle and a Ring of Free Action. The ring supplies particular
movement/disable immunities; it is not general magic immunity. `BDERINYE` adds
no equip-effect combat protection. Exact installed item effects and slots are
in the companion equipment appendix; they must not be inferred from the
creature header's unequipped AC value alone.

### Ashatiel's higher-priority story script

`BDASHATI` override precedes `BDSHOUT` race and `BDFMCL01` general. It owns
introductory dialogue, refusal relocation, duel barks and cheating checks.
During the solo duel at difficulty 1, a block destroys her Frost wand and
removes both Mirror Images plus Spell Deflection (`BDASHATI:31-42`). That is
**duel-specific**, not a generic difficulty-1 group-fight loadout.

Non-protagonist attacks in the duel set the cheating flag; sustained invisibility
can also do so (`BDASHATI:149-202`). The timer symbol `FOUR_MINUTES` resolves to
20 seconds in this installation. These duel rules cannot simply govern the new
agreed group brawl, which explicitly permits all party members and hiding.
Her `MINHP1` item supplies minimum-HP and other story protections. The normal
introductory dialogue's state 1 transition destroys it **before** proceeding
to the duel/refusal choices (`BDASHATI.d:15-21`). Carrying `MINHP1` unchanged
into a new combat actor or bypassing that transition would not make a normal
killable opponent.

## Small Kimble — Mage 11

Kimble already has a broad opening stack and a control/support script, but her
41 HP, **absence of Stoneskin**, and limited memorization remain important.
She has no sequencer, Spell Trigger or contingency in this book/script.

### Complete prepared book

| Prepared magic | Copies |
|---|---:|
| Magic Missile (`SPWI112`) | 4 |
| Shield (`SPWI114`) | 1 |
| Blur (`SPWI201`) | 1 |
| Detect Invisibility (`SPWI203`) | 1 |
| Mirror Image (`SPWI212`) | 2 |
| Vocalize (`SPWI219`) | 1 |
| Flame Arrow (`SPWI303`) | 1 |
| Haste (`SPWI305`) | 2 |
| Protection from Missiles (`SPWI311`) | 1 |
| Fireball (`SPWI304`) | 1 |
| Confusion (`SPWI401`) | 1 |
| Greater Malison (`SPWI412`) | 1 |
| Improved Invisibility (`SPWI405`) | 1 |
| Minor Globe of Invulnerability (`SPWI406`) | 1 |
| Shadow Door (`SPWI505`) | 1 |
| Waves of Fatigue (`SPWI508`) | 1 |
| Spell Deflection (`SPWI522`) | 1 |
| Hold Monster (`SPWI507`) | 1 |

`SPWI508` is Waves of Fatigue in this installation, not a source of level-seven
Chaos. The effective script agrees with that prepared identity.

### What she does with it

- Starts with the eligible stack above; has one Mirror Image copy left if the
  opening spends one. Shadow Door and Spell Deflection are conditional reserve
  layers. No ordinary Blur/Shield recast exists here; the single prepared copy
  of Protection from Missiles is spent if its opening branch fires.
- One Extra Healing potion at <75% HP, difficulty 2+, with 100/50 weighted
  use/fall-through; Vocalize if silenced (`BDMAGE01:335-377`).
- Defense recasts use available Images, missile protection, Deflection/Globe,
  Shadow Door or Improved Invisibility, checking the relevant current
  protection and shared defense cooldown (`:575-753`). Generic Mislead and
  Stoneskin branches exist but cannot fire from this book.
- Fireball is relatively high priority, but only difficulty 3+, and only at a
  visible enemy with another enemy near it and **no member of the caster's
  side within the safety distance**. Its selector starts with farthest enemies.
  This can suppress Fireball in a tight melee brawl (`:808-878`).
- Detect Invisibility reacts to a detectable but unseen opponent (`:1010-1068`).
- Haste has ordinary ally-targeted casts and a 24-second support timer; it is
  **not** in the initial forced stack (`:1414-1561`, shared details below).
- Waves of Fatigue precedes Confusion, both at difficulty 3+; then Greater
  Malison, Hold Monster / Paralyzation wand, Flame Arrow, and Magic Missile
  occur later (`:1920,1938,2262,2402,2417,2599,2657`). In particular **Malison is
  not a guaranteed opening setup before her control spells**.
- The Paralyzation wand has four initial charges and the branch avoids an
  already-disabled target. She has 20 stunning darts and a plain dagger. At
  range 5 she switches to melee; otherwise she uses ranged attacks between
  spells (`:2700-2728`). There is no scripted tactical retreat from melee here.
- She has **no prepared Breach, Secret Word, Spell Thrust or dispel**. Generic
  anti-magic code in the script does not supply those spells.
- The shared equipped `UNICAEL2` cloak is cosmetic: its 19 color effects supply
  no hidden defense or spell preparation. Neither it nor the backpack SCS
  marker item compensates for the missing Stoneskin.

## Sarginson — Fighter 7 / Mage 10

Sarginson's base role is an archer/caster with 82 HP. He too has **no Stoneskin**,
no sequencer/trigger/contingency, and no Vocalize prepared.

### Complete prepared book

| Prepared magic | Copies |
|---|---:|
| Shield (`SPWI114`) | 1 |
| Magic Missile (`SPWI112`) | 2 |
| Obscuring Mist (`SPWI106`) | 1 |
| Horror (`SPWI205`) | 1 |
| Mirror Image (`SPWI212`) | 2 |
| Melf's Acid Arrow (`SPWI211`) | 1 |
| Haste (`SPWI305`) | 1 |
| Minor Spell Deflection (`SPWI318`) | 1 |
| Spell Thrust (`SPWI321`) | 1 |
| Improved Invisibility (`SPWI405`) | 1 |
| Emotion, Hopelessness (`SPWI411`) | 1 |
| Protection from Normal Weapons (`SPWI511`) | 1 |
| Feeblemind (`SPWI509`) | 1 |

### What he does with it

- The opening table gives his initial defenses. Protection from **Normal**
  Weapons should not be mistaken for Protection from Magical Weapons when
  considering how a well-equipped player party will fight him.
- One Extra Healing potion at <75% HP, difficulty 2+, with 100/50 weighted
  use/fall-through (`BDFMAG01:335-350`). No personal potion buff is in his
  captured inventory. Generic potion branches are not extra supplies.
- Mirror Image recast checks both no remaining Images and zero Stoneskins.
  Other recasts cover normal-weapon protection, Minor Spell Deflection and
  Improved Invisibility if copies remain (`:749-927`). At difficulty 3+ most
  of those sole copies were already spent opening; the second Image is the
  clear remaining defensive recast.
- Spell Thrust against detected spell protection precedes Haste, Emotion,
  Horror, Feeblemind, Obscuring Mist, Wand of Frost, Acid Arrow and Magic
  Missile (`:1452,1618-1735,2130,2383,2624,2732,2801,2817,2831`). Emotion is
  difficulty 3+; Horror skips fear-protected/disabled targets. Control spells
  skip already-disabled or appropriately debuffed targets.
- Wand of Frost has four initial charges. Bow is Composite Longbow +1 with
  40 Arrows of Fire +2; melee fallback is Long Sword +1. He equips melee within
  range 5 and ranged otherwise (`:2876-2891`), rather than actively kiting.
- No prepared Breach/Secret Word/dispel, healing spell, summons, Fireball,
  Greater Malison or high-level defensive spell is provided by this script.
- His equipped `UNICAEL2` likewise supplies only cosmetic color effects, not
  armor or magical defenses. The complete equipment appendix distinguishes
  backpack infrastructure from combat items.

## Shared combat mechanics that matter for a fair party fight

### Finite resources and priorities

The long script is a generic menu. `HaveSpell` and `HasItem` make most of it
unavailable to a particular actor. Standard `Spell` casts consume their
prepared spells and can be interrupted; casting generally sets `bd_cast` for
one round (6 seconds). Item branches use `SetInterrupt(FALSE)` around their
action and share that cast timer. Initial item quantities are recorded above;
no item-creation/replenishment branch appears in these three general scripts.

Defensive recasts share a **15-second** `bd_defence_timer`: `GTIMES.IDS` calls
that numeric value `THREE_MINUTES`, meaning in-game minutes, not three minutes
of real combat. This limits defensive frequency but does not manufacture new
prepared copies. The first delay after prebuff setup is 4 seconds.

Most control/defense branches use response weights 100 cast / 50 continue;
damage often uses 100 / 25, anti-magic 100 / 100, and Stoneskin 100 / 35.
They are relative selection weights, not separate percentage chances or a
guaranteed spell schedule. Higher-priority healing/defense can delay offense.
The scripts select candidates with `See(...)`, deliberately false targeting
blocks, and `LastSeenBy`; those `False()` blocks are target acquisition, not
dead code to remove.

`BDSHOUT:481-494` does contain a later out-of-combat heal/rest routine, gated
by a previously set retreat/rest timer, no detected enemy, no combat, and no
retreat in progress. It can reset `bd_prebuff`. That is not unlimited combat
regeneration and is not our proposed opening reset.

### Haste support: Kimble and Sarginson

Their Haste sections are identical apart from line offsets. They scan the
nearest five allies, not named members of an encounter roster. First they can
counter a slowed ally. Otherwise a visible, living, unhasted ally must have
another ally within range 15, an enemy must be within range 30 of the caster,
and the Haste timer must be clear. Both paths spend a prepared Haste and set
`bd_cast=6`, `bd_haste_timer=24`.

Hostile difficulty 1/2 actors fail the `DifficultyGT(EASY)` gate. At difficulty
3, casts have a 100/35 cast/fall-through weighting. At difficulty 4/5 the valid
cast branch has no weighted fall-through. Kimble can supply at most two and
Sarginson one from the current books. This is a useful existing support
behavior, but **does not guarantee a Haste opener or whole-group coverage**;
positions, the effective installed spell and target selection still matter.

These scripts use normal `SPWI305`, not SCS's install-generated prebuff clone.
However, the **effective SR-shaped SPWI305 already diverges from the native
Haste state check**. Inspection of every ability found no opcode 16 and no
casting effects. It instead delivers opcode 176 movement +6, opcode 1 with
parameter 1=6/parameter 2=0 (half an attack per round), spell-state 184, icon 38,
and timed protection from another `SPWI305`. At caster level 10 the main
effects last 84 seconds; at 11, 90 seconds. Its delayed `SPWI305D` child is the
post-Haste fatigue package, not an opcode-16 Haste application.

The native scripts test `STATE_HASTED`, not spell-state 184. Therefore they have
a concrete risk of selecting an already-Hasted ally again after their 24-second
timer, wasting a finite copy against the spell's own stacking protection. This
is a static compatibility finding, not a live reproduction. Any new brawl AI
needs to recognize the installed Haste semantics even if it never uses an SCS
prebuff helper. Delivery radius, eligible allies and marker checks need a
focused runtime sample.

Ashatiel's Ring of Free Action does block opcode 16 and 126, but neither 176 nor
the APR opcode 1. Its opcode 163 Free Action also leaves opcode 176 unaffected.
Thus the ring alone does **not** block these installed Haste movement/APR
effects if they reach her. The ring suppresses icon 38, so a missing Haste icon
would not establish absence of its actual benefits. This conclusion is for
the inspected SR-shaped spell, not universal vanilla/SCS loadouts. Full effect
records and resource hashes are in scratch `haste.json`.
[IESDP movement opcode 176](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm#op176)

### Higher-priority scripts and the old duel

The escorts' stack is `BDDSC` override → `BDCRUSDS` class → `BDSHOUT` race →
their own general combat script. `BDDSC:107-135` makes them neutral and blocks
ordinary actions while `bd_asha_duel>1`; attacks during the solo duel can mark
cheating. `BDCRUSDS` initializes lane movement and hostility. `BDDSC` also owns
retreat after plot 439 and the existing poisoned-supplies consequence.

Therefore their general scripts alone are not a working brawl. Their original
duel spectatorship, assault movement, death cleanup and retreat must be scoped
away from the new fight while preserving the genuine solo duel/refusal paths.
The player's desire to permit hiding also means preserving meaningful finite
invisibility-counter resources rather than giving every enemy permanent
omniscience. No such new ability has been chosen here.

## Focused implications for the next design discussion

There is already usable prebuffing, conditional target choice, consumable use,
anti-magic, invisibility detection, support and limited defensive recasting.
The largest factual gaps are not “these people have no AI”; they are that
generic branches exceed actual spellbooks, two arcane escorts lack Stoneskin,
and several useful team buffs are optional ordinary casts rather than a
coordinated opening. Spellbook copies, prebuff expenditure, defensive reserves,
interruptibility, target protection checks, friendly-fire space, and consumable
budgets are the useful questions to take from SCS/Chosen of Cyric references.
This document selects no new spells, equipment, level increases or difficulty
bonuses.

## Current resource fingerprints

| Resource | SHA-256 |
|---|---|
| `BDASHATI.CRE` | `3d001aeb9de507b4dca55b6e7c072aa0397a6048e9975c1a2551b767e2848ec8` |
| `BDFMCL01.BCS` | `7d082f9cd2e724af1502a7cb372db554525f028a4c083b9a65a49e9f00c8b7a2` |
| `BDASHA02.CRE` | `c86c920f594321d80dde4ec3dbcd4b3fc4202f19f624641e9fe7a34a49b4b4a9` |
| `BDMAGE01.BCS` | `9f888a03c5cb5b3e0ae57e226ef7087de679f164c99c64df3c3f71c047a0c7c8` |
| `BDASHA05.CRE` | `50e0f389a9819bba118fdeae2988cef04226935dd86035bafbcb281927cd776e` |
| `BDFMAG01.BCS` | `27992100b54116798e480299391d2f27b135cdb7c50d2ad41baf5302699f0e7d` |
