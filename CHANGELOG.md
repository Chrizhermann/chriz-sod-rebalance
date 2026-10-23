# Changelog

## Unreleased

- **265** no longer stops the installation after Dark Tidings. A decompiled
  timer is printed with the name the game's `GTIMES.IDS` gives its value, and
  Dark Tidings appends `60 ONE_TURN`, so Shadow Aspect's 60-second summon timer
  then reads `ONE_TURN` instead of `TEN_ROUNDS` and 265 refused the unchanged
  summon block ("HARDEST summon block differs from the original/corrected
  contract"). 265 now asks WeiDU which name this game prints for 60 seconds;
  the rest of its exact check is unchanged. **135, 140, 200, 245, 256 and 266**
  matched their own timers by vanilla name too, and now read the name the same
  way, so a mod that names 6, 10, 12, 18 or 30 seconds differently no longer
  stops them. 200 and 245 write the new 30-second parley timer as the number 30,
  which compiles to the same script as `FIVE_ROUNDS`.

## v0.6.15 - 2026-10-23

- **256** now installs alongside Tweaks Anthology's "Summoned Creatures Clear Fog
  of War" (`cdtweaks` 3500). That tweak gives every summoned creature a permanent
  self-cast of `CDTFOW`, and 256 stopped on it as an unreviewed donor effect:
  on EET at the summoned fire elemental `BDELFIRM`, on BG:EE+SoD also at the
  `SUMELEAR` fallback. `CDTFOW` clears the fog of war only for allies, so the
  hostile bridge elementals now leave exactly that effect behind. Any other
  shape of it, and every other unknown effect, still stops the installation
  before anything is written
  ([#31](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/31)).

## v0.6.14 - 2026-10-18

- Add EET-only choice **292 / 293 / 294** "Imoen in Shadows of Amn" (one of three,
  installed after 160 and 290). Every choice hands an imported or recruited
  Imoen's SoD gear over like the party's before the campaign switch: items on
  EET's installed import lists are imported (one copy, only when the party has
  none), everything else goes to EET's hidden import bank, and she keeps only
  her BG2 belt, now correctly equipped. This fixes the off-party Imoen who
  reached SoA with all her gear and her own belt pushed into the magic-weapon
  slot (she fought bare-handed). She is brought to the transition from any SoD
  area; a dead or never-recruited Imoen is left to EET. Before she leaves the
  party she gets EET's own SoD-party mark (`K#PartySoD`), which EET normally
  sets in the SoD epilogue that the remix's ending replaces. Without it, EET's
  BG1 Imoen script deleted her, gear included, the moment she left the party.
  Leaving the party also opens her post-party dialog at once, which offers to
  rejoin; that dialog (read from SoD's `BDDIALOG.2DA`, `csrimoen` with 160)
  stays closed while the handover runs, and the handover never removes a party
  member.
  - **292** (CEBG default): she becomes EET's Shadows of Amn Imoen (`IMOEN10`) plus
    her BG1/SoD tome boosts (each score capped at 25). No EEex needed. Removing
    her is not enough, because EET carries even a destroyed Imoen into SoA (she
    stays in its list of global creatures); so after her gear is handed over and
    her boosts are read, a stand-in made from `IMOEN10.CRE` takes her place in
    that list and is removed too, and EET creates its own `IMOEN10`. The boosts
    go only to an Imoen without her SoD mark; should the swap fail, her own
    Imoen continues as she was and the game log says so.
  - **293**: she continues as taken along. After her gear is handed over she
    leaves like any companion, so EET gives her SoA's dialog and scripts; left
    in place, she kept SoD's dialog and her BG1 script, and SoA's XP catch-up
    never ran (lab).
  - **294** (requires EEex): a pure single-class thief dual-classes to mage at her
    end-of-SoD thief level. SoA's catch-up XP then goes into mage, and she learns
    `IMOEN10`'s wizard spellbook. Kit, HP, skills and proficiencies stay.
  - Hosts: component 290's ending carrier and, when installed, 910's bedroom
    skip (either install order). Installation stops without changes when EET's
    import rules or arrival script have an unexpected shape.
  - Known issue (open): if Imoen is dead when SoD ends, SoA's opening scene
    never gives control back, because EET has no case for a dead Imoen who
    has been in the party. This already happens with 160 and 290 alone;
    raise her before the ending.

## v0.6.13 - 2026-10-13

- Add component **198**: Skie can join in the palace hall before the first rest;
  Yeslick, Branwen, Ajantis, Coran, Garrick, Kagain, Alora, Xan, Tiax, Kivan and
  Shar-Teel are simple early recruits. Reuse saved actors and their possessions,
  respect known deaths, and use modest BG1 donors for fresh starts.
- Dismissed, previously recruited companions follow the Coast Way, Troll Claw
  and Coalition camps. Retire duplicate cameos, Skie's obsolete cleanup, and
  the Coran/Safana argument; keep Tiax's jail release and once-only native XP.
  Requires 110 and 197. Captured-resource compilation and focused source review
  passed; in-game recruitment, camp movement and normal bedroom rest remain
  for the user's next install. Faldorn, Quayle, Eldoth, Xzar and Montaron remain
  deferred to the second round.
- Add component **177**: report Korlasz's defeat to Liia during ordinary palace
  conversations after the first night, including departure day. Preserve the
  early reward and council/departure scenes; both report routes share the existing
  once-only guard and pay 22,000 XP per present party member.
- Keep the journal pending until Liia receives the report and restore that reminder
  once for existing unpaid city saves. Already-paid saves receive no extra reward.
  Requires 175 and 180; append after 176 if present. Captured-resource compilation
  passed for old and current reward amounts; native verification is deferred.
- Add component **285**: the lower Avernus tower switch becomes a one-way
  portal into the existing confrontation, skipping the lift ride and its
  battles without replacement XP. Belhifet requires +1 weapons, has 60% magic
  resistance and 25% extra movement, with 350/400/450/475/500 HP on
  Easy/Normal/Core/Hard/Insane. Delayed targeted Breach replaces the opening
  mass dispel; Insane opens with four devils and refills one vacancy at most
  every four rounds. Hephernaan keeps his devil form with a finite 14/14
  cleric/mage spellbook. Install before first entering BD4700.
- Relocated Korlasz jailbreak loot (170) and Coast Way camp-chest treasure
  (900) no longer arrive pre-identified. New grants keep the identification
  state of the original item instance; existing inventory and chest records,
  quantities, charges and other flags are unchanged. Existing saves that already
  contain these creatures or chests are not repaired.

## v0.6.12 - 2026-09-27

- Add the approved Boareskyr collapse timer to fresh 256, plus append-only 258
  for existing elemental battles. Story Mode disables it; Easy through Insane
  allow 10/8/7/6/5 unpaused minutes, with five minutes initially on Legacy of Bhaal.
- Show quarter/half/three-quarter warnings above the protagonist and in the log,
  with native rockfall sounds and short shakes. Stop and confirm demolition when
  both mages and all four elementals are defeated, regardless of living guards.
  Preserve the existing Bence aftermath; last-second completion beats expiry.
- Save countdown/warning state, retain the original budget through ordinary
  difficulty changes and retreat, and disable the encounter's deadline if Story
  Mode is enabled. Failure gives a short collapse warning, fades to black and
  invokes native game over, without explosions or forced party deaths.
- The alternative siege consequences remain deferred. Native presentation and
  combat-duration acceptance are pending; see the
  [timer verification record](docs/playtest/2026-09-27-bridge-timer.md).

## v0.6.11 - 2026-09-16

- Fix component 197 failing after Khalid continuity 115 changes the bridge victory
  routes. Recognize the original two victories, 115's four route branches,
  256's single consolidated victory, or the 115/256 pair. Validate their structure
  and remove only the obsolete Skie spawns, preserving route guards, Khalid's
  carried-party protection and all other victory actions. Reject incomplete,
  conflicting or unrecognized layouts before patching.
- Keep component 256 in charge of its pending Bence wrap when 197 is appended
  later. The older 197 starter now defers during that stage, preserving 256's
  combat/dialogue checks and retries.
- Verify public 197 without 115, public 115 followed by 197, and appending 197 after
  later writers in a disposable copy of the affected 369-row collection state.
  These are installer/script checks; no new native playtest is claimed. The
  original installation and collection stream remain untouched. See the
  [collection recovery handoff](docs/recovery/2026-09-16-cebg-alpha16-skie.md).

## v0.6.10 - 2026-09-14

- Add component 115 for Khalid's Bridgefort quest when carried from BG1. The existing
  defender Adirran supplies the briefing and command choices; Khalid remains a companion.
  Adapt conflicting separation dialogue and protect against NPC staging/scene copies,
  preserving the original commander route for non-carried Khalid. Requires 110.
  Guard Voghiln's Jaheira-rescue introduction for carried Jaheira while preserving his
  independent recruitment.
- Protect both native Khalid recruiter blocks directly and check all party slots,
  preventing arriving companions from being moved, neutralized or reassigned NPC AI.
  Wait for occupied party slots before selecting the ordinary first-entry route.
- Support both installation orders with component 256, preserving the carried-Khalid
  aftermath, bridge victory checks and prompt Bence arrival.
- Native playtest passed BD2000 entry, wardstone transport and Adirran's briefing
  with Khalid still controllable. The subsequent save preserves his party allegiance
  and dialogue. Append 115 after 110 before the first BD2000 visit; use an earlier
  save if the original NPC reset has already happened.

## v0.6.9 - 2026-09-13

- Add component 256: replace both Boareskyr finale entry routes with two
  wizards, two veteran guards and four difficulty-scaled fire/earth elementals.
  Use finite prebuffs and defensive recasts, ordinary interruptible combat spells,
  one group Haste on enemy sighting, targeting an elemental, and conservative
  area-spell placement. Credit
  Sword Coast Stratagems for the adapted defensive priorities.
- Remove the bridge's explosive actors, portal controller, obsolete warning and
  map note, animated effects and painted barrel piles in both day/night art.
  Preserve army retreat, Bence's aftermath and onward-passage controls. Reword
  the later Bwoosh provenance without changing that quest. Keep the old fixed
  roster's 4,520 kill XP across difficulties. No collapse timer in version 1.
  Append after existing 255 if present; use a pre-first-BD2000 save. The user
  accepted the stronger bridge fight, prompt Bence arrival, save/reload and
  onward crossing during the combined playtest.
- Strengthen the bridge opening after playtest: move the mages back, share actual
  enemy sightings, and use level-14 Insane variants. Optional component **257**
  adds one finite full sequencer to each Insane mage. Earth uses Greater Malison
  then Slow; fire uses Spell Revisions Dispel Magic
  (Remove Magic otherwise) then Flame Arrow, replacing the Fireball payload that
  never released in the stronger replay. Other tiers retain level-13 mages.
  After victory and combat clearance, Bence appears beside the party to initiate
  his existing wrap and open the passage, replacing the slow walk from his old
  spawn. Eight enemies, total XP and defensive reserves remain unchanged.
  Regular component **256** keeps Haste and all other improvements, without
  sequencer preparation or release. The optional component switches only the
  two Insane mages' AI; no additional enemies, statistics or XP changes.
  Haste now waits for the fire mage's own enemy sighting and targets an elemental,
  while nearby guards can benefit. The final optional split is verified through
  compiled-script and installer tests; individual native spell delivery was not
  independently recorded during the accepted fight.
- Fix component 256 rejecting Artisan's Mystic Monk equipment-policy effects
  on its mage donor. Preserve the reviewed helper effects, validate their
  class filter and dependencies, and continue rejecting unknown donor effects.
  Rehearse against copied resources from the combined Kitpack/SR/SCS stack;
  no upstream Kitpack change or native combat acceptance is implied.
- Add component 135, selected by default: retain the scripted assassin ambush
  while removing its recurring dead-magic spell and misleading area/companion
  remarks. Preserve the assassins, warnings, travel hooks and shared spell.
- Put Mizhena's amulet on the approved existing BD5000 corpse and remove the
  obsolete grants to suppressed displacers. Component 265 preserves existing
  container contents, removes the missed BD5110 Guardian and Shadow Aspect's
  Shadowed Soul summons. Apply the Guardian's 3,200 party-XP
  allowance at the existing chapter reward (106,800 total).
- Preserve Ymori's original dormant quest actor in fresh 230 and append repair
  235 for older cuts. Correct the future road-north reward to 23,100 party XP.
  No saved areas or previously paid awards are modified.
- Record the campaign filler audit, approved triage, and prologue XP recount.
  Set Liia's reward to the approved flat 22,000 XP per character on every
  difficulty. Fresh 175 uses this amount; append 176 to update an older award
  without reinstalling 175 or deducting previously received XP.
- Add default component **266**: limit Shadow Aspect's Insane Mislead to one
  use per actor. Preserve its first cast, ordinary invisibility, other AI and
  remaining summons. The repeated chain is removed; broader encounter
  trivialization and the unfinished native summon check are deferred.
- Fix restored Skie's recruitment XP to follow the native SoD companion tiers
  based on protagonist XP, without lowering higher XP or changing her class/kit.
  Give the condolence reply an appropriate response, retain her rejoin dialogue,
  and convert matching locked SCS potions to their ordinary movable versions
  after recruitment. Preserve installed potion mechanics.
- Preserve the verified Xan/Yeslick companion aliases through the palace strip
  and keep Shar-Teel's field rejoin route usable. These changes do not resolve
  the reported equipment-appearance issue after resting; that remains open.
- Next version: design the Ashatiel Chosen-of-Cyric-style fight with the user,
  including a preparation window and enemy prebuffs. No new encounter design is
  silently selected as part of this release.

## v0.6.8 - 2026-09-06

- Fix component 900 failing on a camp chest containing additional or replaced
  items. Preserve its existing raw item records and append only the eight
  approved rewards, without recreating a sword or changing original item metadata.
- Validate area/table bounds, every container's item run, unique target identity,
  and 16-bit item-count capacity before writing. Other containers and unrelated
  area bytes remain unchanged. Component 901 remains a no-op preference marker.
- Reproduce the reported three-item chest failure and 900-fails/910-succeeds
  partial-install shape on v0.6.7 using real WeiDU in disposable fixtures. Add
  regressions for the fixed 900/910 suffix, empty and modified chests, metadata,
  prerequisites, and malformed structures. No game install or gameplay test is
  claimed; component 910, install order, and collection recipes are unchanged.

## v0.6.7 - 2026-09-06

- Add experimental EET component 910: a two-confirmation bedroom choice,
  normal EET BG2 handoff, and a once-only additive 250,000 protagonist XP award.
- Keep party equipment carried for EET's normal import handling by delaying the
  palace backpack impound until a confirmed No. Include existing imported Imoen
  belongings without collecting fresh Imoen or palace equipment.
- Remove the rejected ground-loot collector, pickup scan, and private staging
  area. Loose-loot recovery and the proposed acquisition-history registry are
  deferred (issue #18).
- Add real WeiDU integration and compiled-script regression coverage. The native
  six-person Yes route reached BG2, with the saved protagonist XP confirming the
  exact award and sampled carried/bag import handling. Visual polish and broader
  native coverage are follow-ups; no collection recipe is changed.

## v0.6.6 - 2026-09-06

- Add component `290`: end SoD after the short playable victory celebration,
  with Dazzo's rest conversation as the deliberate endpoint. Remove the
  post-victory murder, arrest, trial, escape, and ambush sequence.
- Preserve EET's installed import rules and BG2 item placement. The new route
  carries internal import data forward without sending the party through the
  removed ambush; it does not award the party a bag of equipment.
- Fix full-cutscene suspension of the EET carrier. Fresh `290` includes the
  correction; tail component `291` repairs existing `290` installations without
  uninstalling or reinstalling earlier components. Missing saved-area containers
  abort visibly before inventory is touched.
- Add native SoD ending support and platform-aware prerequisite resources.
  Standalone installation/static checks pass; native credits testing is pending.
- Verify the EET guard, actual victory sequence, celebration save/reload, and one
  six-marker inventory handoff with exact potion-bag contents. Expanded party
  variants and multiplayer remain untested.
- Retain v0.6.4 installer ordering and v0.6.5 scrying-pool fixes. Record the bridge,
  Ashatiel, and campaign-filler roadmap tasks without implementing those designs.

## v0.6.5 - 2026-09-05

- Fix component `120` on the current no-Aura four-state `BDSCRY.DLG` by
  targeting the Hooded Man picker route through its semantic local flag instead
  of assuming an optional state `4` exists.
- Apply the same guarded native-layout patch to component `225`'s Imoen and
  Caelar picker routes, while preserving the existing text-only omen and
  component `220` Essence rehome.
- Add WeiDU integration coverage for the native dialog, fail-closed changed
  layouts, and the installed scrying-pool verifier; use the CI-provided WeiDU
  executable when available on `PATH`.

## v0.6.4 - 2026-09-04

- Declare component `210` before component `197`, satisfying the latter's real
  WeiDU dependency when installing the complete 30-component selection.
- Add a regression that preserves all 31 declarations (including the mutually
  exclusive `900`/`901` pair) and locks the dependency-safe order.
