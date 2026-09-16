# Changelog

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
