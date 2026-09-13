# Boareskyr first-version encounter — acceptance record

Component **256** was fought in the isolated Combined test installation on
September 13, 2026, alongside [PR #21](https://github.com/Chrizhermann/chriz-sod-rebalance/pull/21).
The user reported that the encounter worked well, but was too easy and retained
an invisible passage barrier until Bence's conversation. The live install was
not modified. The subsequently approved stronger revision was installed into
Combined on September 13 after the user authorized the replay. Native save 947
(`CSR TEST 17`) records that replay: Bence was late, the fire sequencer never
released, and Haste was not observed. The latest corrections below are now
installed as row 425, superseding the row-424 Fireball/approach/spawn-Haste build;
the user has now won that replay, approved the harder combat and confirmed
prompt Bence arrival. Save/reload persistence and individual spell delivery
remain separate, unverified checks.

## Latest replay result and challenge-pack decision

The user described the row-425 fight as brutal in a positive sense, then
explicitly confirmed: fight won; Bence arrived promptly. Record combat feel and
Bence's arrival as user-observed passes. No new save name or parsed effect
evidence has yet been supplied, so do not infer every spell-delivery assertion
or reload check from that feedback.

The user clarified that regular Insane keeps the current fight, including Haste,
but omits both mage sequencers. A separate optional Extra Challenge component
adds only those sequencers. This split is approved but not implemented. The user
will reference it in another challenge-pack task;
see the [design decision](../design/wave1/08-boareskyr-bridge.md#decided--optional-extra-challenge-split-september-13).
Bence's prompt arrival remains a general fix. Current source/test resources
still represent the challenge version.

Next: save after Bence as **CSR TEST 18 — Extra Challenge bridge won**, reload,
and cross the opened passage once. Check no duplicate encounter, Bence or reward.
Then continue with the retained assassin ambush and removed dead-magic effect.

**Completed:** the user saved/reloaded and crossed the bridge, reporting that
everything seemed fine. Save 949 is `CSR TEST 18 — Extra Challenge bridge won`;
save 948 is `CSR TEST 18 - Bridge hardest won, Bence done`. A read-only remote
check after crossing found the game paused in BD2000 at plot295, all six party
members alive on the far side. Record save/reload and onward passage as native
user-observed passes. The protagonist's unrelated-looking spoken text is
reported but deliberately not investigated: the user suspects an imported
soundset mismatch and explicitly excluded a deep investigation.

## September 13 native feedback

- The user won the staged bridge fight and completed Bence's conversation.
  Named native save 946 is **CSR TEST 16 — Bridge won, Bence done**; save945
  is **CSR TEST 15 — Bridge ready**. Both folders were found in the isolated
  Combined profile. The post-victory save has not yet been parsed or reloaded
  for duplicate-spawn/persistence verification.
- The barrel artwork is gone, but the closed `Bridge_Barrels` door still blocks
  passage until BDBENCE state32. This reproduces the retained progression order,
  but leaves an unexplained invisible wall. The component197 automatic starter
  requires a PC within25 units; Bence spawns well behind the fight at[2425,2660].
  The first source correction made Bence approach the party after victory and initiate
  the existing wrap once combat clears and dialogue is possible. Do not simply
  open the door early: crossing BDBOARB can advance plot295 before his plot293
  dialogue runs. The following BDFFMERC soldier also retains barrel-transport
  dialogue; include that obsolete text in the eventual aftermath correction.
  Its subsequent replay and replacement are recorded below.
- The first tuning discussion considered two mages of each type on
  Insane with deeper placement and coordinated engagement, or reliable opening
  Haste and a stronger sequencer, or an additional cleric providing group buffs.
  The user then selected the stronger two-mage opening described below; the
  additional mages and cleric are deferred.
- This report establishes a completed fight and working manually reached Bence
  wrap. It does not independently prove every mage cast, group Haste delivery,
  defensive recast, alternate entrance, night art or reload regression.

## September 13 first stronger revision — installed and replayed

- Keep the eight-enemy roster and **4,520 total kill XP** on every tier. Move
  the fire mage to [1456,1860] and the earth mage to [1344,1920]. Static footprint,
  path and Haste-radius checks cover this formation; native crowding is untested.
- Give the fire mage one opening group Haste on every difficulty, spending its
  single copy. A real sighting alerts the group to a last-seen location; each
  actor still requires its own sight/range for attacks and spells.
- On Insane only, use level-14 mages with one full sequencer each: earth
  **Greater Malison then Slow**; fire **Dispel Magic with Spell Revisions, or
  Remove Magic without it, then Fireball**. Other tiers remain level 13.
  Preparation reserves and spends the finite payload copies. The fire mage
  waits for a safe target rather than ignoring its allies' positions.
- After victory and combat, Bence approaches and starts his existing wrap when
  dialogue is possible, retrying if needed. That dialogue still opens the door
  before the onward vision. The remaining BDFFMERC barrel-transport text is a
  separate unresolved aftermath cleanup.

This earlier revision's verification passed with Windows WeiDU 249: **252 regression
tests (including 94 bridge tests), 41 research tests, 14 ending-contract self-tests,
and 55 TP2/TPA parse checks**, with no skips. Distinct synthetic Dispel/Remove spell
identities verify both installation branches; additional checks cover friendly
dispel safety, finite sequencer spending, disabled casters, real-sighting awareness,
and Bence retries plus preserved native initialization.

The public installer also passed against disposable copies of the current
Combined Kitpack/SR/SCS inputs, using original component-256 backups for resources
already changed by that component. All four eight-actor rosters and the Insane
books/payloads were checked. Bence's native initialization remains first, and his
entire original script body is preserved as a suffix. Disposable uninstall restored
the original override bytes. All 132 actual input resources and the actual TLK/log
were rechecked unchanged. Local ignored evidence:
`research/data/bridge-tuning-20260913-actual/report.json`.

These historical results are separate from the first-build results below and do
not verify the latest Flame Arrow/Haste/Bence correction. They do not establish native
Haste delivery, sequencer effects, challenge, coordinated movement or Bence's
approach. The actual replay findings follow below.

### Save 947 findings and latest approved correction

- The user reported Bence arriving too late, no fire sequencer release, and no
  observed Haste. Saved fire-mage locals are `CSR256_PREP=1`, `CSR256_HASTE=1`
  and `CSR256_SEQUENCE=1`: preparation and the Haste attempt ran, and the sequence
  remained charged. The earth mage has `CSR256_SEQUENCE=2`, marking its sequence
  spent. These flags do not establish which Haste effects reached the group.
- The user approved replacing Fireball in the fire sequence with **Flame Arrow**.
  Keep **Dispel Magic on Spell Revisions, Remove Magic otherwise**, followed by
  Flame Arrow. On Insane, two Flame Arrows supply one reserved payload and one
  ordinary cast; Fireball falls to one on SR and zero where level-3 Protection
  from Fire needs that slot. Haste/dispel copy counts and defensive reserves are unchanged.
- Bence must wait until combat clears, then **appear beside the party** and start
  his existing wrap. This replaces his long walk from the old spawn; the dialogue
  still opens the passage before the onward vision.
- Haste's cause remains unknown; expiry between initial spawn and the party's
  approach is a hypothesis. The user explicitly directed casting **when the fire
  mage sees an enemy**, targeting an elemental rather than casting at spawn.
  Source now prefers the central fire elemental, with the other elementals as
  fallback targets; guards can benefit but are never targets. The single finite
  Haste copy is unchanged. Native delivery under this timing remains unverified.

The latest correction is **installed, with native replay pending**. Its exact
tail-package rehearsal and disposable restore passed, as did the final **96
bridge tests** (28.563 seconds, no skips). No broader new test result is claimed.
With the game closed, installation appended row 425 and preserved all 424 prior
package/language/component rows. Three output resources and three backups were
verified; the TLK is unchanged. Evidence:
`C:/Users/chris/CEBG-Tests/Combined-20260908/bridge-correction-20260913/installed.json`.
Preserve the row-424 evidence and saves 945–947. Checkpoint 945, **CSR TEST 15 —
Bridge ready**, remains suitable for the next native replay.

### Authorized Combined installation

Installed the frozen local tail package
`bridge-tuning-install-20260913/setup-csr-bridge-tuning-playtest.tp2` with the game
closed. It appends row 424, preserving the original 423 package/language/component
entries in order. Eight output resources and all six original WeiDU backups were
verified against the rehearsed manifest; the TLK is byte-identical. The payload
includes the source-level Skie potion correction. Existing base mages, all other
creatures and the saved games were not rewritten.

The update patches the current BD2000 script's eight mage spawn entries only,
preserving other late-installed behavior. Bence and Skie retain their previous
script bodies beneath the added prefixes. The exact local tail package passed a
disposable installation and byte-exact uninstall before the actual installation.
Evidence: `C:/Users/chris/CEBG-Tests/Combined-20260908/bridge-tuning-install-20260913/installed.json`.

Parsed native save945, **CSR TEST 15 — Bridge ready**, is suitable for this update:
Chapter7/plot279, retreat1, bridgePlot/request/stage/alert0, no owned encounter
actors or death counters, six living rested members and 88 ready memorized spells.
Its cached area retains script BD2000, so new actor creation uses the updated
scripts and CREs. No reset or teleport is required. The profile already has
Insane selected. Preserve completed save946 as the first-build result.

That replay is now recorded in save 947 (`CSR TEST 17`), with the findings above.
Save/reload duplicate checks and normal onward passage remain open. Skie's
movable-potion check can be done on a separate older save with her in the party.

## Installation and checkpoint boundary

Use a save from **before the first entry into BD2000**. The old area's actors,
region script and animation state can be cached in a visited-area save. A save
made just before the battle in an already visited bridge area is insufficient.
The installer deliberately does not rewrite saved areas or mid-finale globals.

Append 256 to the designated dev copy after its existing rows, along with the
applicable filler corrections from PR #21. An installed 255 stays installed;
256 supersedes its encounter. Do not reinstall earlier components. Record the
exact commits and appended WeiDU rows when preparing the combined test copy.
The collection's combined installation reached this component on September 9
and exposed a donor-compatibility guard failure. The source correction and
copied-resource rehearsal are recorded in the
[full-stack compatibility note](../research/2026-09-09-bridge-fullstack-compatibility.md).
Recovery of that retained installation belongs to the collection task; a
successful rehearsal does not clear its failed receipt or establish checkpoints.

## Agent verification — first-build baseline

Final Windows verification: **167 regression tests + 41 research tests + 14 ending
contract self-tests passed**, with no skips. The TP2 and all 48 TPA libraries
parse successfully. The 57 new component tests also passed using Linux WeiDU
249 on a case-sensitive temporary copy; the final optional-Skie change received
its own six-test Linux world rerun.

The public installer succeeds against copies of both current effective EET
resources and the standalone SoD reference. The final EET run uses the filler
PR's already-corrected BD2000 ARE/BCS and preserves Ymori's exact actor record.
All 123 EET and 116 standalone source resources retain their original hashes.
All seven copied component libraries match the final implementation bytes.
Standalone's native Skie aftermath spawn is preserved when another component
has not already removed it; the EET target's already-removed variant also works.

Local ignored evidence: `research/data/issue14-public-combined-final-1788871428820403200/report.json`,
`research/data/issue14-public-standalone-1788871355717481800/report.json`,
`research/data/issue14-public-smoke/tests-final.log`, and
`research/data/issue14-world-review/linux-world-skie-result.json`.
These are resource/installer checks, not a native fight or full standalone campaign.

- Real WeiDU fixtures exercise the public installer, finite creature spellbooks,
  compiled AI decisions, both native finale entry seams, victory predicates,
  resource-local dialogue edits and both PVRZ/palette tile formats.
- Public integration checks installation, an existing 255 followed by 256,
  synthetic uninstall restoration, and failure before any encounter/TLK write
  when a late art resource conflicts. Synthetic uninstall is confined to throwaway
  test games and is not an instruction for real installed WeiDU rows.
- The two old spawn lists and both old success predicates are replaced precisely.
  The wider siege and the original Bence/Khalid/journal/rest aftermath survive.
  `Barrel_spot` retains its retreat destination while its old controller is detached.
  BDFISTM1's obsolete warning actor has no remaining creation route. Bence opens
  the normal passage after plot 293 without reading old portal globals.
- The final formation was checked against the actual search map and closed-door
  cells. Full creature footprints do not overlap and party-sized paths reach
  every actor. This catches static obstruction, not dynamic combat congestion.
- Resulting day/night tile records were decoded and visually compared. All three
  baked barrel clusters and the four closed-door alternatives are cleaned; WED
  data, water-overlay alternatives and the original transparency silhouette remain.
- Preparation uses actual caster-level instant casts plus one-copy removal;
  normal combat casts spend their own memorized copies. Haste's once-attempt guard
  applies to the owned freshly created group, not arbitrary third-party haste.

## Next short manual run — latest correction installed, native replay pending

Use one Insane fight to assess the new sequencers and upper challenge envelope.
There is no need to fight all five tiers: automated checks cover tier selection
and resource counts. Preserve saves 945/946 as the first-build evidence and
record the updated test-copy fingerprint with the next checkpoint.

1. Finish the siege/retreat normally. Confirm one short warning, two mages, two
   veterans, two earth elementals and two fire elementals. No barrels, portal,
   barrel instructions or sudden old failure sequence should appear.
2. Watch the mages' starting protections and opening group Haste. Confirm the
   nearby frontline actually receives Haste, rather than merely seeing a cast
   animation. Check that fighting through protections prompts a limited defensive
   recast and that interruptions/control remain useful. On Insane, check both
   sequencers release Greater Malison/Slow and the selected dispel/Flame Arrow
   once when valid targets are available. Verify Haste waits for the fire mage's
   enemy sighting, targets an elemental and actually reaches nearby allies.
3. Fight normally and watch for blocked actors, endless pursuit, spell spam or
   repeated friendly Fireballs. Grease is deliberately uncommon when melee units
   could enter its persistent area. The finite group receives no reinforcements.
4. After all eight are defeated/removed and combat clears, confirm Bence appears
   beside the party and initiates his aftermath. Confirm dialogue then opens onward
   passage. Save/reload after victory: no duplicate roster, Bence or reward.
5. If convenient, inspect the bridge at night too. Report visible seams, water
   coverage problems or any remaining barrel artwork. The installer/render checks
   already cover both assets; this is a brief native visual check.

There is **no collapse timer** in version 1. Version 2 will need the separate
visible, generous five-turn timing discussion and an observed Insane fight.
Do the assassin, XP and quest-loot samples from the
[combined filler checklist](2026-09-08-filler-fixes.md#next-manual-session--agreed-2026-09-08)
in this same session. Ymori remains a low-priority side-quest check.
