# Chosen of Cyric: source reference for the Ashatiel discussion

> **2026-09-26 update:** reset the player party before preparation; no literal
> enemy reset is required. Enemies start present, hostile and prepared out of
> sight, attacking on early contact or advancing after the opening few rounds.
> This supersedes both preserving existing player buffs and spawning enemies
> after preparation. RR's opening does not replace the agreed fair start. See
> [current design](../design/wave1/09-ashatiel-party-brawl.md).

Status: read-only research, 2026-09-22. This records encounter techniques from Rogue
Rebalancing; it approves no Ashatiel design, roster, spell list, or implementation.

## Original starting brief (superseded by the update above)

The current [wishlist](../01-remix-wishlist.md#ashatiel-chosen-of-cyric-style-party-fight--15)
already requests a party encounter with **about 30 seconds of player-controlled
buffing before the opposing group spawns**, a warning, preservation of the player's
existing buffs, and enemy prebuffs, sequencers and potions. These are the starting
brief for discussion, not unanswered questions for the RR reference to decide.
The full encounter still requires user/agent design discussion before implementation.
The exact warning, preparation trigger, timing and presentation remain OPEN, as
do the roster, placement, spell/potion packages and difficulty tiers.

## Evidence and limits

The full RR v4.92 source is available under
`%USERPROFILE%\CEBG-Tests\Combined-20260908\game\rr\`.
Paths below are relative to that directory unless stated otherwise. This audit
read distributed source and the current installation log; it did not launch the
game, install anything, or decompile the effective post-modification BCS files.
Source behavior below is therefore an intended-script finding, not live acceptance
of the Combined installation.

The Combined `WeiDU.log` records:

- line 23: RR component 11, Chosen of Cyric, v4.92;
- line 71: Spell Revisions main component, v4.21-chriz.3;
- line 228: `SRCB_RR_COMPAT` component 0, v4.21-chriz.4;
- lines 239–245: SCS 35.21 innate sequencers/contingencies, AI initialization,
  general AI, calls for help, mages, priests, and NPC potions.

RR's own encounter description is `doc/rr_cyric.html`, especially its teamwork,
difficulty, starting-the-battle, and individual-character sections. Where it
describes the enemies as obeying player rules, the actual actions still need
inspection: several displayed sequencers and dispelling-arrow assists use
`ReallyForceSpell`, not ordinary spell/item use.

## Opening and preparation

RR is an ambush with a substantial opening disadvantage for the player. Its
two-round preparation is for the **enemy**, not a player preparation window.

`rr_cyric/compile/rr#camb2.baf` places the six enemies, then uses actual items or
spells in the cutscene:

| Actor | Source opening preparation |
|---|---|
| Venduris | Frost Giant Strength potion variant; Magic Protection potion |
| Grok | Defense and Magic Shielding potions |
| Bodak | Clarity and Invulnerability potions |
| Selina | Freedom potion; Barrier Amulet |
| Zaeron | Power and Frost Giant Strength potions |
| Kerith | Magic Resistance; Holy Power |

`rr#camb3.baf` then applies `TRAP_ARROW_DISPELLING` separately to Player1–Player6,
shows the sealing wards, and begins the leader's dialogue. `rr#vend.d` has combat
exits into `RR#CSAVE`; `rr#csave.baf` sets the six enemies hostile, has Venduris
apply his ring's Mass Invisibility, sets the combat gate `RR#CSAVE=2`, saves,
and ends cutscene mode. No player-controlled preparation interval was found in
this audited opening path. The source also contains dialogue alternatives; this
is not an audit of every noncombat branch.

The reusable structural idea is a distinct staging phase, a leader exchange,
and one explicit release into combat. Ashatiel's established starting brief
changes RR's opening: warn the player, provide about 30 seconds of controllable
buffing before the enemy group spawns, and preserve existing buffs. The source
offers no reason to import RR's party dispel or enemy-only preparation. The exact
warning, trigger, duration, staging and spawn presentation still need discussion.

## Combat roles and coordination

The group is recognizably an adventuring party: an assassin, barbarian, ranged
attacker, arcane caster, hybrid caster/thief, and priest. Its coordination is
concrete and reactive rather than six copies of generic attack AI.

- **Recover disabled allies.** `rr#kert.baf:423–469` checks named living allies
  for stun/held status, available Remove Paralysis, the priest's own casting
  conditions, and cooldowns. It spends an ordinary `Spell` action to help the
  ally. Further blocks cover poison/blindness and other afflictions.
- **Protect the damage dealers.** `rr#seli.baf:1200–1240` includes Improved Haste
  casts on Grok and Bodak, conditioned on their current state and her available
  spell/casting conditions.
- **Ask another role for assistance.** `rr#seli.baf:101–135` lets a caster with
  Insect Plague reveal herself or move toward Bodak. `rr#bodk.baf:189–290` contains
  corresponding dispelling-arrow-style assists, including voiced requests for
  help. These actions force the dispel spell; the first insect/silence blocks do
  not check or consume an arrow. This is a useful teamwork reference, not proof
  of a strictly finite ammunition implementation.
- **Choose targets by vulnerability.** Grok's script checks weapon protections,
  damage resistance, Stoneskin and panic before attack selection; the arcane
  scripts inspect protections and disabling effects before casting. The full
  target logic is extensive and tied to BG2-level spell assumptions.

For Ashatiel the open question is which small number of visible, understandable
relationships would define the group: for example a priest clearing an ally's
disable, a caster supporting a frontliner, or a ranged enemy disrupting party
casters. Choosing such relationships does not require inheriting RR's exact
classes, spell levels, or named enemies.

## Sequencers, contingencies, and finite resources

Selina's `rr#seli.baf:19–99` explicitly scripts one-use opening packages:

- a local `RR#CHCntg` flag gates the displayed Chain Contingency and forced
  Protection from Magical Weapons, Improved Haste and Spell Turning casts;
- `RR#Cntg` gates a below-51%-HP Improved Invisibility contingency;
- `RR#Trig` gates the displayed Spell Trigger: Greater Malison, Slow, then
  Chaos, with short waits between forced casts; Easy substitutes Confusion.

`rr#seli.baf:155–184` has another one-use local flag for a defensive sequence
of Improved Invisibility, Stoneskin and Mirror Image. These are script packages
with labels and guards, not proof that an enemy holds a player-style stored
sequencer payload. Ordinary later casting uses availability and casting-state
checks. A six-second local casting timer appears across ordinary cast and potion
blocks.

The portable design distinction is between an announced opening package,
one-use emergency response, and ordinary subsequent casting. Exact packages,
allowed tiers, and difficulty differences for SoD remain open.

## Healing, withdrawal, and counterplay

`rr#vend.baf:45–98` enters healing mode below 80 HP, tries an Invisibility potion,
then drinks Extra Healing under the same six-second action timer. It exits that
mode above 93 HP or when the healing potion is unavailable. Availability checks
and `UseItem` make those potion actions inventory-dependent.

`rr#kert.baf:200–285` also uses a healing mode and checks potion inventory;
Sanctuary is an ordinary available-spell cast below 50% HP, with silence,
spell-failure, Insect Plague and detection-related conditions. Other members
have their own healing/escape rules. The encounter documentation describes
withdrawal into the northern trapped area, giving movement a tactical purpose.

This supports discussing limited consumables, recoverable emergencies, and
meaningful support-target choices. It does not establish an appropriate potion
budget, invisibility frequency, trap field, healing threshold, or escape route
for Ashatiel. Those depend on the actual SoD roster and arena.

## Completion

`rr#001.baf:1–17` waits for all six named enemies to be dead while the combat
state is 2, then advances it once to 3 and updates the journal. A separate block
requires their deaths plus possession of Venduris' scroll to start the exit
dialogue. `rr#cend1.baf` performs the ward removal and journal/encounter cleanup.

Thus defeating the group and reopening the route are separate, explicit state
changes. Ashatiel needs its own completion condition integrated with existing
SoD siege progression; neither a mandatory six-death condition nor a looted-scroll
exit requirement transfers automatically.

## Compatibility boundaries for this installation

The installed compatibility source at
`game\srcb_rr_compat\setup-srcb_rr_compat.tp2` and
`game\srcb_rr_compat\lib\rr_spell_semantics.tpa` explicitly repairs RR Chaos
spellbooks/scripts and Selina's Spell Deflection guard after RR and SR. Its
library separates spellbook migration, script normalization and the guard fix.
This means unmodified RR source is not the final authority for spell semantics
on Combined.

The BG modding skill's current `rr-sr-compatibility.md` explains why: SR reuses
spell slots; cast identifiers, prepared CRE resources, and active-state guards
can diverge. Its example is RR Chaos migration plus the old Spell Turning cast
becoming SR Greater Spell Deflection. The script and spellbook need to agree,
and a cast symbol must not be confused with an active-state stat. That reference
is supporting guidance; this audit did not independently validate final compiled
IDs, spellbook migration or live recasts.

SCS is present, but its presence alone proves neither that every RR combat block
has been rewritten nor that every custom future SoD actor would acquire the
desired AI automatically. A later implementation would need to inspect the
effective chosen SoD actors, their script slots and the final installed spells.
Ordinary SCS casting, custom staging, custom one-use openings and bespoke ally
assistance have distinct responsibilities that must be decided deliberately.

## Remaining design questions within the starting brief

1. What exact warning and trigger start the requested roughly 30-second
   preparation interval, and how are the countdown and enemy arrival presented?
2. Which existing SoD characters supply distinct roles and two or three clear
   teamwork relationships?
3. Which prebuffs/opening packages fit their level and identity, and which should
   be one-use?
4. What finite healing budget and repositioning behavior makes pressure
   interesting without making the fight chase-heavy?
5. How does defeat release the existing siege progression, including cases where
   a surviving enemy is disabled, charmed, or temporarily absent?

No game resources, save files, installer files or encounter code were changed
during this research.
