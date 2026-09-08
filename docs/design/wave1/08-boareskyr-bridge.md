# Boareskyr Bridge — elemental demolition finale

Issue: [#14](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/14).
Status: first-version encounter and combat direction approved by the user on
2026-09-08, including stronger defensive recasting informed by comparable SCS
mages. Remaining implementation details are listed below. No replacement
encounter is installed.

## DECIDED — version 1

- Keep the wider siege battle and the crusaders' retreat.
- Remove all smokepowder barrels, their objectives, text and destruction mechanics.
  Retire the single weak wizard / Plane-of-Fire portal sequence. Component 255 is
  the old stopgap, not a mechanic the replacement must retain.
- Two capable wizards: one focused on fire, one on earth and battlefield control.
  Both have appropriate protections and participate in combat.
- Four elementals already summoned: two earth and two fire.
- Two veteran crusader guards protect the casters.
- Relative formation: earth elementals toward the party's approach; wizards
  farther along the bridge and separated; fire elementals and guards around them.
  Exact coordinates require space/pathing verification for the actual creatures.
- Sequence: siege ends -> crusaders retreat -> short demolition warning -> player
  approaches and fights the prepared group -> defeat leads into Bence's existing
  aftermath and onward passage.
- No bridge-collapse timer in version 1. Start with this finite encounter; no
  scripted reinforcement-wave system is required for the first version.
- Test this together with PR #21's filler fixes during the user's next manual
  session. Prepare checkpoint saves after implementation; see the
  [combined test plan](../../playtest/2026-09-08-filler-fixes.md#next-manual-session--agreed-2026-09-08).

## DECIDED — spells, AI and difficulty (2026-09-08)

The user accepted the following proposal and requested more defensive recasting,
with comparable SCS mage AI checked and adapted where useful. This supersedes the
earlier suggestion of only one spare Mirror Image. Web is deferred for the first
test, following the accepted recommendation to start with Slow and Grease.

- Both wizards are level 13. Reserve their sixth-level summon budget for their
  two initial elementals; no additional combat summoning is selected.
- Fire: Flame Arrow as the main attack in mixed melee, Fireball at separated
  targets where allies are safe, Magic Missile as an alternative, and a finite
  Breach against meaningful defenses.
- **Added by the user:** one prepared regular Haste for the fire mage, with
  explicit combat AI. Use an ordinary interruptible cast after urgent defensive
  renewal and before routine damage when at least two nearby living elemental/
  guard allies can benefit. Choose an ally that places the useful group inside
  the installed spell's area; avoid redundant Haste and exclude unrelated
  retreating crusaders. Haste is not part of instant preparation.
- Control: Slow, Glitterdust, one carefully placed Grease, and a finite Breach;
  Greater Malison is the accepted Hard/Insane tuning option.
- Shared opening defenses: Stoneskin, Mirror Image, Shield. Fire additionally
  uses red Fire Shield and Protection from Fire; control uses Spirit Armor and
  Minor Spell Deflection. Any optional extra ward must fit the reserve budget.
- Ordinary removable protections, once-only opening preparation, and finite
  memorized copies for subsequent recasting. Combat casts are interruptible.
- One healing potion per wizard as the initial allowance. Guards intercept
  attackers reaching the wizards; caster movement stays local to the formation.
- AI respects line of sight, chooses useful targets and avoids wasting spells
  on known protections. Fireball must not rely on free blanket fire immunity
  for the earth elementals and human guards.
- Elementals persist as encounter actors until defeated or otherwise removed;
  the normal summon spell's short expiry is not the encounter's completion clock.
- Keep rewards consistent across difficulties, preserve normal elemental
  weaknesses/control options, and add no second difficulty damage multiplier.

| Difficulty | Initial elemental composition |
| --- | --- |
| Easy / Normal | Two lesser of each element, with their actual damage checked and softened as needed. |
| Core | Two standard earth, two standard fire. |
| Hard | One greater earth, one standard earth, two standard fire. |
| Insane | One greater and one standard of each element. |

Four greater elementals are not the first-test baseline. Preserve the same
eight-enemy roster; difficulty tuning does not authorize additional waves.

### Initial defensive allocation — implementation baseline for playtesting

Use two total Stoneskins and three total Mirror Images per wizard: one of each
for preparation leaves **one Stoneskin and two Mirror Images for combat**.
The control wizard has two Minor Spell Deflections, leaving one after preparation.
Refreshes require actual remaining copies; none of these reserves should be
silently consumed by another preparation block.

This fits the level-13 generalist budget with the selected roles. The fire mage's
four level-4 slots are two Stoneskins, Fire Shield and Protection from Fire. The
control mage uses two Stoneskins and Spirit Armor, with its fourth slot available
for the selected difficulty option, such as Greater Malison on Hard/Insane.
The earlier optional Minor Globe suggestion must not consume a nonexistent fifth
slot or displace the requested Stoneskin reserve. On level 2, three Mirror Images
still leave two slots for the control mage's Glitterdust. On level 3, two Minor
Spell Deflections leave three Slow copies. Exact unused slots and lower-difficulty
allowances can be finalized during implementation without inventing extra slots.

The fire mage's five level-3 slots are now **Haste x1, Flame Arrow x2, Fireball x2**.
This accommodates the requested support spell without using defensive reserves
or adding slots. Apply the same ordinary availability, casting-failure and shared
casting-timer checks as other combat spells. Resolve the installed original Haste,
use normal `Spell()` spending, and do not attach another `RemoveSpell` or use an
SCS instant-preparation helper for this combat cast.

The current SR Haste does not set ordinary `STATE_HASTED`; its spell-state marker
188 is the shared `PRIORITY_DISPEL`, not a Haste identifier. Use the owned fresh
group's preparation contract and single reserved cast to prevent repeats. Do not
infer foreign/equivalent Haste from those flags; any such detection needs a
resource-specific compatible check. Existing `BDMAGE01` already provides normal
ally-targeted Haste casting and cooldown patterns. The source comparison also
found SCS uses a local one-shot guard for its SR Haste path.

The user approved more recasting; these copy counts are the first implementation
allocation, not a permanently locked balance value. Revisit them using the combined
native playtest if the mages collapse immediately or spend too long only defending.

## DECIDED — version 2 direction

Add actual collapse pressure in version 2, after the first fight has been tested.
The timer must be obvious to follow and generous enough to defeat the opponents
even on Insane. The fight is the main attraction; the timer should add only mild
damage-output pressure. Failure should mainly result from running away or taking
an exceptionally long time, not from an ordinary deliberate combat approach.

**User's starting proposal: about five turns.** That is roughly five minutes of
unpaused gameplay, not five rounds. The current dev `GTIMES.IDS` defines
`FIVE_TURNS` as 301 seconds and `ONE_ROUND` as 6 seconds. This is a proposed tuning
baseline, not evidence that the eventual Insane fight fits the budget.

Presentation, exact trigger and duration, pause/save behavior, warning intervals,
victory cancellation, retreat/re-entry behavior and the actual failure outcome
still need a version-2 design pass. A visible remaining-time display and a clock
that starts after the warning returns control are implementation proposals, not
yet chosen UI or timing rules. Do not add any hidden timer to version 1.

## OPEN — details for the first implementation

- Final spell-copy allocation beyond the defensive baseline, source adaptations,
  and wizard display names. Specific new characters or backstories are not
  required; additional combat summon spells are not selected.
- Exact lower-difficulty elemental adjustments; guard equipment/stat packages.
  The elemental tier progression above is approved.
- Exact coordinates and pathing with two earth and two fire elementals present.
- Short warning/dialogue text and cleanup of the old portal/barrel claims.
- Kill XP and loot accounting. The earlier flat quest-XP decision is not approval
  of a new bridge reward or difficulty-dependent quest payouts.
- Component number, old-255 coexistence, and the supported installation paths.

## Existing sequence — implementation seams

The September 7 effective-dev decompiles were checked during the September 8
design pass. Current dev `BD2000.BCS` still matched the recorded hash. These are
code findings, not native encounter acceptance or a fresh audit of every resource.

| Seam | Existing behavior and replacement requirement |
| --- | --- |
| Siege victory | `BD2000.BCS` sets plot 280, orders retreat, opens the gate and spawns the old finale group. Preserve the wider battle and replace this spawn list. |
| Alternate resolution | A separate surrender/sabotage retreat branch spawns the same group. Update both entry paths. |
| Warning | `BDBOARB2` starts `BDCUT26`, which brings in the warning mage. Rework the warning without preserving claims about barrels or the portal. |
| Old mage | `BDCRUBB` suppresses ordinary mage AI, creates the portal and escapes. Copying that behavior would reproduce the unwanted encounter. |
| Demolition controller | `BDBOARB2` owns repeated fire summons and two barrel-related party-kill paths. Replace those paths; simply removing the barrel actors is insufficient. |
| Victory | Two existing area-script predicates accept either portal completion or early mage-and-guard kills. Replace both with completion for the new group, then preserve the plot-293 Bence aftermath. |
| Retreat destination | `Barrel_spot` is also used by the wider army as a retreat anchor. Preserve its destination function while replacing the attached demolition script. Its internal name does not require an on-screen barrel. |
| Onward passage | Bence's dialogue opens `Bridge_Barrels`; crossing then launches the retained Bhaal vision. Preserve this order rather than opening the passage during enemy setup. |

Relevant tracked aftermath source:
`chriz-sod-remix/baf/csr197bnc.baf`. Placed barrels, map notes, portal effects,
ambients, dialogue and journal text all need coverage in the removal audit.
The earlier CUTSKIP audit found no bridge-finale replay; recheck the effective
skip resources when implementing.

The old authored formation has a mage at `(1465,1910)`, four melee at
`(1605,1900)`, `(1540,1935)`, `(1480,1985)`, `(1430,2030)`, and two archers at
`(1530,1865)`, `(1400,1960)`. These are research anchors, not approved or tested
coordinates for the new formation. The extracted current search map confirms
that this section of the approach is on the narrow diagonal bridge.

## Current donor research — options, not selected balance

Read-only inspection of the current dev EET resources on 2026-09-08 found:

| Role | Existing template | Useful contents / caveat |
| --- | --- | --- |
| Fire wizard | `BDCRU58`, level 9 / 36 HP | Fireball, Flame Arrow, Fire Shield, Stoneskin, Mirror Image and Breach; a low-effort fire spellbook, not a locked strength target. |
| Control wizard | `BDCRUW46`, level 10 / 40 HP | Stoneskin, Mirror Image, Glitterdust, Confusion and Breach. Earth-themed control requires deliberate spell/AI selection. |
| Stronger control chassis | `BDOLONEI`, level 13 / 52 HP | Slow, Hold spells and defenses; do not copy the named actor's identity or unique loot. |
| Veteran guard | `BDCRUE45`, level 9 / 108 HP | Plate, two-handed sword +1, two extra-healing charges; remove its Alachi encounter handler. |
| Standard elementals | `BDELFIRM` fire + `ELEAR01` earth | Both 96 HP / 6,000 kill XP. Normal combat donors with no portal sequence. |
| Greater elementals | `BDELFIRG` fire + `ELEARG01` earth | Both 128 HP / 10,000 kill XP. Possible tuning options, not approved additions or difficulty tiers. |

The mage/guard candidates use Beamdog combat scripts on this install, with
native difficulty-gated prebuffs and consumable use. Tail-added clones will not
automatically receive SCS's earlier installation pass. An SCS mage donor would
need its actual assigned script, matching spellbook and helper data preserved;
never graft a hardcoded generated script name onto another creature's spellbook.
The old bridge mage is itself level 10 / 40 HP; its combat-suppressing encounter
controller is a central problem, not simply its level.

Standard/greater earth have animation footprint 5, versus 3 for the fire donors.
Their equipped fists and immunity items also matter: earth fists have 4d8 base
crushing, fire fists 3d8 plus on-hit effects. These are substantial combatants;
do not choose tiers by HP alone or globally change an animation INI to make them
fit the bridge. Four standard elementals yield 24,000 kill XP; four greater yield
40,000 before the humanoids. Any difficulty-tier substitution needs explicit XP
accounting rather than accidentally inheriting different donor rewards.

Use unique clone identities and explicit script slots. Remove inherited siege,
retreat and unrelated death-count handlers; keep only audited combat behavior.
Added spells must be supported by the chosen AI and resolved against installed
spell identities. Fire spell targeting/protection for the earth elementals and
guards is another detail to settle before the first implementation.

Local ignored evidence: `research/data/issue14-mage-audit/README.md`,
`research/data/issue14-elemental-audit/current-dev-20260908/result.json` and
`weapons.json`, plus `research/data/issue14-layout-audit/BD2000SR.BMP`.
These findings do not establish native combat or standalone compatibility.

## Comparable SCS mage research (2026-09-08)

Current installed CRE script slots identified Davaeorn (level 11), Sunin (level
11), and `MAGE12A` (level 12) as suitable comparisons. Their effective generated
scripts were inspected alongside installed SCS 35.21 source. Generated filenames
are installation-specific evidence, not portable dependencies for this component.

Useful source behavior to adapt:

- Initial preparation precedes renewal, which precedes ordinary offense:
  `mage/ssl/main/dw#mage.ssl`, lines 21, 83 and 105.
- `mage/ssl/generalblocks/renew.ssl`, lines 556–580, renews Stoneskin at fewer
  than two skins when a visible enemy is within script range 5 and no stronger
  weapon protection covers the mage. Mirror Image is renewed when absent and
  skins are nearly exhausted. These are reactive defenses, not a fixed rotation.
- `caster_shared/caster_definitions.ssl`, lines 177–188, expands the combat cast
  into availability/spell-failure checks, a shared six-second casting timer and
  ordinary `Spell()`. Renewal additionally uses a seven-second local timer.
- `mage/ssl/combatblocks/renew_antimagic.ssl`, lines 8–40, lets immediate physical
  danger take priority over renewing spell defenses. Renew an approved ward only
  when missing and useful, with a real copy remaining.
- `mage/ssl/combatblocks/attacks_on_PC_defences.ssl`, lines 13–66, checks meaningful
  targets for Breach and spaces antimagic attempts with local timers.

Sunin has three Mirror Images, leaving two after generic preparation. Sunin and
the generic mage use a special already-precast Stoneskin helper that preserves
their one memorized Stoneskin; Davaeorn's ordinary preparation consumes his.
Our chosen baseline explicitly charges the opening copy instead of importing
that special exception. Merely copying a CRE's spell counts is not equivalent.

The generated spell-defense preparation also has overlapping difficulty paths
that can consume multiple copies if the book is enlarged. Adapt the useful
priority/availability logic into one owned preparation-and-combat controller;
do not transplant a whole generated script and assume added reserves survive.
Use installed spell identities, and keep combat renewal separate from instant
opening preparation. Consistent renewal-timer checks should cover both physical
defense branches in our small controller.

Credit David Wallace / Sword Coast Stratagems 35.21 for any literal adaptations,
record source paths and changes, and retain credit with the implementation.
This is code/resource evidence; no new mage has been installed or fought.
Ignored local evidence is under `research/data/issue14-scs-audit/`.

## Validation plan

Before asking the user to play: verify both entry branches, removal of the old
failure/spawn/success paths, once-only victory, Bence/onward progression,
save-boundary requirements, and compatibility with the existing filler fixes.
Use isolated fixtures and copies of effective resources before installing into
the designated dev copy. Never use the live install for these changes.

AI validation must show that preparation spends exactly its allocation and leaves
the documented reserves, intact defenses are not recast, combat renewals use
ordinary casts/cooldowns, and exhausted books do not replenish themselves.
For Haste, cover useful group targeting, an already hasted group, insufficient
eligible allies, the last memorized copy being spent, interruption and higher-
priority self-defense. Native playtesting must verify the frontline receives the
installed Haste effects; merely queuing the cast is not delivery evidence.

Native acceptance should focus on actual casting/protections, challenge, elemental
pathing, formation and progression. Version 1 has no collapse test. Version 2
will need a separately agreed visibility/timing/failure checklist and observed
combat-duration evidence on Insane before the time budget is accepted.
