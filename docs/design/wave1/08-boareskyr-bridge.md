# Boareskyr Bridge — elemental demolition finale

Issue: [#14](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/14).
Status: first-version encounter and combat direction approved by the user on
2026-09-08, including stronger defensive recasting informed by comparable SCS
mages. The user then authorized implementation. Component 256 is implemented
on its separate branch. The user completed the first native fight and Bence's
wrap in the isolated Combined test copy on September 13. The stronger version-1
revision was replayed in Combined and saved as native save 947 (`CSR TEST 17`).
Bence arrived late, the fire sequencer did not release, and Haste was not observed.
The latest Flame Arrow, Haste and nearby-Bence corrections below are installed
in Combined as row 425, superseding the earlier row-424 build. The user won its
replay, liked the much harder fight and confirmed Bence arrived promptly after
combat. The subsequent save/reload and onward crossing passed by user report;
a remote check confirmed plot295 and the living party beyond the bridge.
Individual spell delivery has not been independently verified. The live install
was not modified.

## DECIDED — optional Extra Challenge split, September 13

After playing row 425, the user requested a separate optional Extra Challenge
component for their planned challenge pack, then specified the exact split:
**regular Insane keeps the current encounter but omits both mage sequencers;
Extra Challenge adds only those sequencers**. Haste on enemy sight, elemental
targeting, formation, shared engagement, current stats, ordinary spellcasting,
defensive reserves and prompt Bence arrival all remain in the regular version.
The user will reference this decision in another task handling that pack.

The source extraction into optional **component257** is **implemented and
offline-verified** for the current release. Component256 keeps the current regular
encounter and cannot prepare or release either sequencer; 257 adds only the
Insane sequencers by selecting their challenge AI. Both modes preserve the same
level-14 Insane mages, spellbooks, stats and world setup. Regular AI may use the
payload spells as ordinary casts. No installation of this split in the test game
is claimed.
All 101 bridge tests passed, including compiled common-AI equivalence and the
two-pointer-only install/disposable restore contract; see the
[release report](../../releases/v0.6.9.md). This adds no new native acceptance.
Preserve both local manifests:
`bridge-tuning-install-20260913/installed.json` (row 424, preceding balance) and
`bridge-correction-20260913/installed.json` (row 425, newly accepted challenge),
under `C:/Users/chris/CEBG-Tests/Combined-20260908/`. These are historical evidence,
not instructions to revert row 425. The installed test copy still contains
row 425's combat behavior. The optional Insane-only payloads are fire:
Dispel Magic with SR / Remove Magic without SR + Flame Arrow; earth: Greater
Malison + Slow. Regular mode must not prepare or release either sequencer.
External pack integration remains for the challenge-pack task; the component
numbering and gameplay boundary are decided. Release preparation is the current
priority; no additional native fight is requested by this record.

## DECIDED — stronger version 1 after the first native fight, September 13

The user liked the encounter's functioning but found it too easy. They observed
the invisible `Bridge_Barrels` barrier until speaking to Bence and suggested
automatic dialogue on victory. Bence already has a proximity-gated automatic
starter, but spawns behind the fight. The first correction's long approach was
still too slow in the replay. The latest approved correction waits for combat to
clear, then creates Bence beside the party to initiate his existing wrap. Preserve
dialogue before the door opens and the onward vision starts. The user confirmed
prompt arrival after winning the row-425 replay, then passed save/reload and
onward crossing.

The user approved keeping the same eight enemies and strengthening their opening:

- One group Haste on every difficulty **when the fire mage sees an enemy**, not
  at spawn, spending his single prepared copy. Target an owned elemental, with
  the central fire elemental preferred; guards may benefit but are never the
  Haste target. Move both mages slightly farther back and let a real sighting
  alert the whole group; each actor still needs its own sight/range to attack.
- Insane-only full sequencers: earth releases **Greater Malison then Slow**;
  fire releases **Dispel Magic with Spell Revisions, or Remove Magic without it,
  then Flame Arrow**. Flame Arrow replaces Fireball following the replay, where
  the fire sequence remained charged without releasing. Each wizard gets one
  preparation slot and spends the payload copies once.
- Insane mages are level 14 to support that seventh-level preparation slot;
  other tiers remain level 13. HP, defensive reserves, roster and total kill XP
  remain unchanged.

Haste remains under investigation. Save 947 has fire-mage locals `PREP=1`,
`HASTE=1`, `SEQUENCE=1`; these establish a preparation/Haste attempt and a reserved,
unreleased sequence, not delivery of Haste. The earth mage has `SEQUENCE=2`.
Haste expiring between spawn and the party's approach is an unconfirmed hypothesis.
The user has now explicitly directed the enemy-sighting timing above; that source
change is installed in Combined row 425; native effect delivery remains unverified.

Additional mages and a cleric with area buffs are **deferred**. The retired
`8e68/chriz-bg-script-engine` worktree is gone, but its surviving
`codex/aoe-prebuff-design` branch contains a callable helper that was tested
applying Haste to its caster and an ally while spending a copy. This is real
prior work; it is not evidence of completed automatic hostile-AI integration or
an installed component that supplies these bridge actors with group buffs.
Cleric integration can build on that work in a later design pass.

The completed first encounter is recorded in the
[native acceptance notes](../../playtest/2026-09-08-bridge-finale.md#september-13-native-feedback).

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
  Current coordinates pass static footprint/path checks; native movement in the
  revised formation still needs verification.
- Sequence: siege ends -> crusaders retreat -> short demolition warning -> player
  approaches and fights the prepared group -> defeat leads into Bence's existing
  aftermath and onward passage.
- No bridge-collapse timer in version 1. Start with this finite encounter; no
  scripted reinforcement-wave system is required for the first version.
- Test this together with PR #21's filler fixes during the user's next manual
  session. Prepare checkpoint saves after implementation; see the
  [combined test plan](../../playtest/2026-09-08-filler-fixes.md#next-manual-session--agreed-2026-09-08).

## DECIDED — spells, AI and difficulty (September 8, revised September 13)

The user accepted the following proposal and requested more defensive recasting,
with comparable SCS mage AI checked and adapted where useful. This supersedes the
earlier suggestion of only one spare Mirror Image. Web is deferred for the first
test, following the accepted recommendation to start with Slow and Grease.

- Both wizards are level 13 below Insane and level 14 on Insane. Reserve their
  sixth-level summon budget for their two initial elementals; no additional
  combat summoning is selected.
- Fire: Flame Arrow as the main attack in mixed melee, Fireball at separated
  targets where allies are safe, Magic Missile as an alternative, and a finite
  Breach against meaningful defenses.
- **Revised after the second playtest:** one prepared regular Haste for the fire
  mage on every difficulty, triggered only when he sees an enemy. Target a living
  owned elemental, preferring the central fire elemental so the installed spell's
  area covers the group. Guards can benefit but are never its target. Require at least
  two nearby living owned allies and exclude unrelated retreating crusaders.
  This supersedes the prior spawn-time Haste preparation.
- Control: Slow, Glitterdust, one carefully placed Grease, and a finite Breach;
  Greater Malison is the accepted Hard/Insane tuning option.
- Shared opening defenses: Stoneskin, Mirror Image, Shield. Fire additionally
  uses red Fire Shield and Protection from Fire; control uses Spirit Armor and
  Minor Spell Deflection. Any optional extra ward must fit the reserve budget.
- Ordinary removable protections, once-only opening preparation, and finite
  memorized copies for subsequent recasting. Ordinary combat casts are
  interruptible; the Insane sequencers release their reserved payloads together.
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

Below Insane, the SR fire mage's five level-3 slots are **Haste x1, Flame Arrow
x2, Fireball x2**. Where Protection from Fire is level 3, it replaces one
Fireball. On Insane, use Haste x1, Flame Arrow x2, the selected dispel x1 and
Fireball x1 on SR; where Protection from Fire is level 3 it replaces that last
Fireball. The sequencer reserves the dispel and one Flame Arrow, leaving one
Flame Arrow for ordinary offense.
The earth sequencer similarly reserves its one Greater Malison and one of its
three Slow copies. Each Insane mage has one full Spell Sequencer preparation
slot; neither the payloads nor the stored sequence replenish after use or reload.

Haste uses the installed original spell at the caster's actual level and
explicitly spends one copy, matching the preparation spending contract. It now
requires the fire mage's own enemy sighting and an eligible elemental target;
the remaining defensive preparation still runs at spawn.

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

### DECIDED — warnings, cancellation and failure (September 27)

- Give clear warnings at **25%, 50% and 75% of the chosen time budget elapsed**,
  showing the bridge deteriorating under elemental power. Show a clear
  confirmation when demolition stops.
- The demolition enemies are **the two mages and four elementals only**. The
  veteran guards and other sword/bow crusaders do not keep demolition going.
  Stop the timer as soon as those six threats are defeated, even if other
  enemies remain in combat. Keep this separate from Bence's existing
  combat-clear aftermath and onward progression.
- For this version, expiry causes a **simple game over**: a heavy stone crack
  and short rumble, a brief collapse message, fade to black, then the normal
  game-over flow. The user disliked the original explosion; do not reuse its
  fireball/explosion spectacle or build an elaborate collapse animation.
- Check demolition completion before expiry so a last-second victory counts.
- **Scale the timer by difficulty and omit it in Story Mode.** The user said
  "story mode or whatever the easiest is"; Story Mode has its own native
  `StoryModeOn()` trigger. The user then authorized implementation of the
  proposed allowances below.

The user authorized implementation and release after review and automated checks
on September 27. Version 0.6.12 includes the countdown for fresh component 256
and append-only update 258. Native timer/game-over acceptance remains pending
for the user's next collection test pass. Version 0.6.11 had no clock.

### IMPLEMENTED — difficulty allowances and presentation

Keep the original roughly five-minute budget for Insane and increase the
allowance below it. These are the accepted initial implementation values;
combat-duration tuning still needs native playtesting.

| Difficulty | Unpaused time budget |
| --- | --- |
| Story Mode | No timer or timed-collapse failure |
| Easy | 10 minutes |
| Normal | 8 minutes |
| Core Rules | 7 minutes |
| Hard | 6 minutes |
| Insane | 5 minutes |
| Legacy of Bhaal | 5 minutes (explicitly detected; same initial budget as Insane) |

The warnings use percentages of the selected budget, not fixed timestamps.
Story Mode should not receive escalating timed-collapse warnings for a deadline
that does not exist. The six-enemy objective and completion confirmation remain.
The time budget is sampled once when the ready encounter hands control back.
Ordinary difficulty changes do not reset or resize it. Enabling Story Mode while
the encounter controller runs permanently disables that encounter's deadline;
switching it off does not restart a hidden clock. Save/reload preserves the
deadlines and emitted-warning state. Pausing freezes the game-time clock.
Leaving the area does not reset the deadline; on return, the controller checks
completion first, then expiry. If several warning milestones are overdue, only
the most urgent is shown. No warning is replayed after completion.

Implemented text (the source uses an ASCII dash in the urgent warning):

| Point | Message |
| --- | --- |
| Start | The mages and their elementals are tearing the bridge apart. Stop them before it collapses! |
| 25% elapsed | The bridge shudders. Elemental power cracks the stonework. |
| 50% elapsed | Fragments of stone plunge into the river. The bridge is weakening! |
| 75% elapsed | The bridge is giving way! The demolition must be stopped—now! |
| Demolition stopped | The destructive magic fades. The tremors subside. The bridge will hold. |
| Failure | The bridge gives way. The road to Dragonspear is lost. |

Display the short warnings above the protagonist and copy them to the message
log as narration. Native `DisplayStringHeadNoLog(Player1,...)` plus
`DisplayStringNoName(Player1,...)` supports this without dialogue or issuing
orders to the protagonist. Warnings play the native rockfall sounds AMB_E17A/B
with brief, increasing screen shakes. These sounds exist in both clean BG:EE
and EET and are used by native rockfall ambients. There are no dust effects or
explosion spells. Failure uses the same rocks, a two-second warning, a one-second
black fade and native GameOver with the collapse message. The initial warning
and deadline are armed together after the encounter-ready stage. No continuously
visible numerical countdown is added. Audibility, text dwell time, shake strength
and the game-over UI require native verification.

Technical references: [StoryModeOn](https://gibberlings3.github.io/iesdp/scripting/triggers/bgeetriggers.htm#0x40FA),
[overhead text](https://gibberlings3.github.io/iesdp/scripting/actions/bgeeactions.htm#388),
[unattributed log text](https://gibberlings3.github.io/iesdp/scripting/actions/bgeeactions.htm#262),
and [custom GameOver](https://gibberlings3.github.io/iesdp/scripting/actions/bgeeactions.htm#366).
These establish available native actions, not acceptance of the new sequence.

Difficulty implementation note: native `EASIEST/EASY/NORMAL/HARD/HARDEST`
values 1–5 correspond to the player-facing Easy/Normal/Core Rules/Hard/Insane
labels. Story Mode is separate. Legacy of Bhaal has its own `NightmareModeOn()`
trigger; do not assume that `Difficulty(HARDEST)` alone identifies it. This
mapping was checked against the dev EET `trigger.ids` and `UI.menu` plus
[IESDP difficulty identifiers](https://gibberlings3.github.io/iesdp/files/ids/bgee/difflev.htm).

### DEFERRED — continuing after the bridge is lost

The user liked an alternative to game over but explicitly saved it for later.
The leading idea is **delayed reinforcements**: the party can reach the far side
by another route, while an identifiable allied contingent cannot arrive for the
Dragonspear siege. The later battle consequently has fewer allied troops.

Other brainstormed possibilities are lost supply wagons/reduced camp supplies,
a costly alternative crossing, or rescuing stranded soldiers after demolition
becomes unstoppable, with survivors affecting later reinforcements. None of
these is an approved implementation or a reason to add routes, rescue mechanics,
troop losses or siege edits to this timer version. The alternative route,
affected contingent, consequences and campaign integration require later design.

### Implementation boundaries and remaining native acceptance

- Fresh 256 includes the shared timer; existing installations append 258 without
  uninstalling 256/257 or any other row. On an already updated 256, 258 performs
  no resource changes. It preserves both entry routes, optional sequencers,
  Khalid/Skie continuity and the existing combat-clear Bence wrap.
- Prefer a pre-fight save. An upgraded active stage-2 encounter receives a fresh
  allowance and opening warning on its first eligible update; already-completed
  encounters never arm a timer. No save is edited by the installer.
- The six-threat check preserves the existing encounter's death, petrification
  and removal semantics. This is necessary for installed SR Banishment, which
  uses opcode 168 removal rather than ordinary death. **Known inherited limit:**
  native scripts cannot distinguish a removed actor from one temporarily
  suspended by Maze; temporarily removing the final threat can count as success.
  Invisibility/offscreen position alone do not satisfy the removal check.
- Legacy of Bhaal reuses the five-minute Insane budget as an implementation
  fallback; this is not a claim that LoB combat duration has been playtested.
- See the [timer verification record](../../playtest/2026-09-27-bridge-timer.md)
  for offline evidence and the outstanding native checklist.

## Accepted row-425 challenge-build details

These details describe the accepted challenge build. The component257 extraction
above moves only sequencer preparation/release out of regular component256.

The latest Flame Arrow/Haste/Bence build below passed the user's Combined fight
and progression test. Individual spell delivery was not independently recorded.
The first native playtest used the earlier formation, level-13 mages,
mid-combat Haste and no sequencers; the second used Fireball in the sequencer and
Bence's long approach.

- Component **256**, independently selectable or appended after installed 255.
  Both use the existing mod's tail-install process; no old row is uninstalled.
- **Crusader Fire Mage** and **Crusader Earth Mage**, level 13 (14 on Insane) with 52 HP. Opening
  preparation casts the original spells at actual caster level and spends one
  memorized copy each. The planned Stoneskin/Mirror Image/Deflection reserves
  remain for ordinary interruptible casts. Each has three Magic Missiles as a
  finite fallback and one Potion of Superior Healing.
- Vanilla Protection from Fire is level 3, unlike SR's level 4. On that spell
  layout the fire mage trades one Fireball copy for Protection from Fire, keeping
  Haste and every defensive reserve within the same slot caps. Insane keeps two
  Flame Arrows and replaces one Fireball with the selected dispel as above.
- Two level-9 veterans with plate and +1 two-handed swords, retaining the installed
  donor's HP (108 on the target EET copy; 80 on the standalone reference). Their armor
  and swords remain undroppable; duplicate named/random loot helpers are removed.
- Lesser earth attacks use a private +2, 2d6 fist; lesser fire attacks use a
  private +2, 1d6 physical fist retaining its installed fire/on-hit effects.
  Shared creature resources, weapons and animation definitions are unchanged.
- Standalone SoD lacks the preferred BG2 lesser/standard earth templates. Its
  replacement clones use the native summoned lesser and greater earth resources,
  normalized to the approved lesser/standard earth HP, THAC0 and saves. Their
  small/large footprints and elemental weaknesses remain. The EET templates
  remain preferred wherever present; lesser fire keeps its installed donor HP.
- Fixed group kill XP remains **4,520**: 1,000 per mage and 420 per guard/elemental,
  on every tier. This preserves the old fixed mage-and-six-guard budget; old
  variable portal reinforcements did not have one reproducible total.
- Haste fires once on enemy sighting, targeting an owned elemental. Static
  geometry places all eight actors inside its current installed radius when
  centered on the preferred fire elemental. Its local guard prevents repetition;
  it does not infer arbitrary foreign Haste from SR's shared spell-state marker.
- A real enemy sighting within the encounter boundary records a last-seen
  location and alerts the group. Allies without sight can move there; attacks
  and spells still require their own valid visible target. Existing local
  pursuit limits remain.
- Insane sequencers are finite and once-only. Disabled/silenced casters retain
  their charge until they can release it. Ordinary Fireball checks ally distance;
  the fire sequencer now uses targeted Flame Arrow. A dispel variant that can
  affect allies receives its own
  distance check. Persistent Grease must lie beyond the melee pursuit boundary
  and may therefore be rare.
- Two native finale spawn lists request the owned group at retreat completion.
  A short warning replaces the old cutscene. Victory requires all eight actors
  dead, absent or petrified, then retains Bence, Khalid, journal and rest actions.
  After combat clears, Bence appears beside the party and retries his existing
  wrap when dialogue is possible. His dialogue still opens the passage; victory
  does not open it early.
  The old portal region keeps its army escape destination but loses its script.
- The four barrel actors are suppressed before rendering. Eight old animations,
  the portal ambient and obsolete map-note addition are disabled. A small art
  patch cleans both day/night TIS resources while retaining WED/door geometry.
  Phossey's later explanation and the Bwoosh description refer to captured
  crusader supplies; the Bwoosh quest and mod-added interjections remain intact.

| Actor | Position |
| --- | --- |
| Fire mage | 1456,1860 |
| Earth/control mage | 1344,1920 |
| Veterans | 1560,1990 and 1608,1920 |
| Earth elementals | 1615,2035 and 1680,1965 |
| Fire elementals | 1544,1944 and 1440,1990 |

The formation passes static search-map checks with the native passage still
closed: 3x3 humanoid/fire and 5x5 earth footprints are walkable, nonoverlapping
and reachable from the party approach. This does not establish native crowding
or combat pathing. Combat uses a common center at 1500,1950 and a local pursuit
radius of 18 script units. Native challenge, visuals and movement are the next
acceptance questions for this revision; the collapse design remains version-2 work.

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
| Greater elementals | `BDELFIRG` fire + `ELEARG01` earth | Both 128 HP / 10,000 original kill XP. Later selected for the approved Hard/Insane tiers, with owned XP overrides. |

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
spell identities. The implementation above resolves fire targeting through
conservative ally-distance checks, without granting blanket fire immunity.

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
This September 8 comparison is code/resource evidence, not native verification
of the later tuning.
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
For Haste, cover waiting without enemy sight, elemental-only targeting, insufficient
eligible allies, the last memorized copy being spent and the once-only guard.
For sequencers, cover Insane gating, complete finite payload reservation, disabled
casters, safe target selection, release order and persistence after spending.
Check shared awareness preserves sight requirements for actual attacks and
Bence retries without skipping the retained dialogue. Native playtesting must
verify the frontline receives the
installed Haste effects; merely queuing the cast is not delivery evidence.

Native acceptance should focus on actual casting/protections, challenge, elemental
pathing, formation and progression. Version 1 had no collapse test. The implemented
version-2 timer has a separate visibility/timing/failure checklist and still needs
observed combat-duration evidence on Insane before its balance is accepted.
