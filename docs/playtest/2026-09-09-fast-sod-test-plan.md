# Fast SoD test session

Plan prepared September 9, 2026; native testing started September 12. The
combined installation contains all 35 selected SoD components, including
corrected 256. The September 12 AFK audit counted 419 actual WeiDU entries
before its four test tails and 423 afterward. The collection task's earlier
446/446 report is a separate build count. The first bridge fight and manually
reached Bence wrap passed on September 13. The row-425 correction subsequently
passed the user's harder bridge replay, prompt Bence arrival, save/reload and
onward crossing; individual spell effects were not independently verified.

**Current priority: release preparation, with no further live QA now.** The
optional component257 sequencer split and default-selected component266 one-use
Insane Mislead correction are implemented and offline-verified. Neither is claimed
installed in the test game. Shadow Aspect native testing is deprioritized and
does not block release; the user wants that encounter made trivial eventually,
as deferred work. Ashatiel's Chosen of Cyric-style encounter is next-version
work and still requires the full back-and-forth design discussion. The test
history and coverage notes below are evidence and future reference, not a new
instruction to resume testing.

Current candidate checks passed: **273 main tests** (including 101 bridge and
13 Mislead tests), **41 research tests**, **14 ending self-tests**, and the TP2
plus all **56 TPA libraries** parsed with WeiDU249. The bridge split preserves
compiled common AI and changes only two CRE AI pointers; public install/disposable
restore checks passed. See the [candidate report](../releases/v0.6.9.md). Historical
build totals below remain separate; these checks add no native acceptance.

## Native results — September 12

- The selected `jajaja i am lord` party completed the native BG1-to-SoD
  transition and selected **No** at the skip offer. Palace save 921 retains
  all six original party members. The user then set everyone to 400,000 XP for
  testing; this save cannot establish the exact transition XP delta.
- Palace celebration/jailbreak and Imoen recruitment ran successfully.
  Imoen replaced Xan. Save 922 records Korlasz dead and Liia's reward pending.
  The user described the **Korlasz** fight as difficult on Insane and liked it.
  This is not bridge-fight acceptance.
- Liia's actual dialogue awarded **exactly 22,000 XP to each of the six
  characters**, verified by comparing save 922 with save 923. Save 924, made
  after reloading and waiting, preserves all six XP values with no second
  award. `CSR_KORL_RET` advances from 1 to 2 and remains 2. Derived local
  evidence: `research/data/fast-playtest-20260912/liia-reward-reload.json`.
- Appearance issue remains under investigation: Khalid, Viconia and Edwin
  looked unequipped on both their map avatars and inventory paper dolls.
  Their saved animation IDs, colors and equipped loadouts match the source
  save; equipped item appearance fields are valid. Source inspection found
  no armor mutation. Re-equipping restored both appearances temporarily,
  but the first palace night made them look unequipped again. That night
  sends all six actors into `SEQ_SLEEP`, then explicitly sends only Player1
  through `SEQ_AWAKE` / `SEQ_READY`. Whether this omission causes the
  appearance defect remains unproven. The later one-character wake diagnostic
  was inconclusive. No permanent appearance patch has been made.
- Bedtime and the council completed natively. Save 925 records the six
  living party members in BD0102, `CSR_BEDTIME=1`, `BD_PLOT=52` and the
  area's `BD_PLOT_003=2`. The reward remains paid and all six XP values are
  unchanged. Derived local evidence:
  `research/data/fast-playtest-20260912/council-finished.json`.
- Skie's decline/re-offer/recruit sequence completed. The user confirmed
  movement/inventory looked fine and saved 926 with BDSKIE in Imoen's former
  slot; `CSR_SKIE_PALACE=2`. Two defects were reported: the condolence reply
  led to "Because you're here," and Skie remained at 64,000 XP despite
  Player1 having 422,163 XP. Derived local evidence:
  `research/data/fast-playtest-20260912/skie-joined.json`.
- Source fixes prepared: a separate condolence acknowledgement and the
  native SoD join-XP ladder in BDSKIE's existing script. The latter raises
  this saved recruit to 250,000 total XP without reducing higher XP or
  replacing her class, kit, equipment or actor. The initial tests passed;
  the final expanded validation totals are recorded below. Real WeiDU
  compilation verified both dialogue branches, and an isolated repair dry run
  preserved all existing dialogue
  states except the condolence transition's destination. The test-game
  repair is prepared outside the game at
  `C:\Users\chris\CEBG-Tests\Combined-20260908\skie-playtest-fix-20260912`;
  it was installed with the game closed during the authorized AFK test run.
  Native XP correction and the condolence branch passed as described below.
- Still pending: palace departure and the remaining
  checkpoint groups below, including the bridge and assassin encounter.

### Authorized AFK mechanical checks

The user authorized autonomous console/UI checks, excluding real fights,
balance/feel judgements and creative decisions. The original named checkpoints
remain intact. New checkpoints are separate copies of native saves; no GAM or
SAV bytes were manually edited.

- **Installation integrity:** Remote Console v0.2.0, the Skie XP/condolence
  repair, the renamed-Xan/Yeslick retention repair and the Skie/Shar-Teel
  dialogue repair were appended with the game closed. All original 419
  component identities/order remain; there are now 423. The final independent
  comparison of 40,708 watched original files found exactly seven expected
  changes, two console resources added, none removed and no read errors.
  The remaining 40,701 originals are byte-identical. BDDIALOG.2DA and
  BDSHARTE.DLG are the only additional original changes since the first three
  tails; both installed hashes match their actual-resource rehearsals.
  Final record: `final-after-dialogue-verification.json` in the evidence folder.
  WeiDU rewrote log description comments, so this is not a byte-identical
  log-prefix claim. Evidence lives outside the repo in
  `C:\Users\chris\CEBG-Tests\Combined-20260908\afk-evidence-20260912`.
- **Skie XP, native pass:** save 930 (`CSR AFK 00 - User handoff`) retains the
  user's 64,000-XP Skie. Loading it on the repaired script raised Skie to
  250,000 without manually awarding XP. Native save 931 (`CSR AFK 01 - Skie XP
  fixed`) persisted the correction. Normal UI reload and dismissal/rejoin
  both kept 250,000; the other five XP values stayed unchanged.
- **Condolence, native pass:** loading user save 925 and choosing the condolence
  reply displayed the new "Thank you" acknowledgement and the existing
  recruitment choices. Save 933 (`CSR AFK 03 - Condolence verified`) records
  that branch followed by declining; the user's joined-Skie save is intact.
- **Palace Skie dismissal/rejoin, repaired native pass:** the missing BDSKIE
  row in BDDIALOG previously selected MULTIG's generic fallback. The repair
  appends only that actor's row. Reform Party now opens her existing Skie
  dialogue. Selecting the wait-here reply, ending, saving, and talking again
  presents her proper recruitment choices; inviting her restores six members.
  Saves 941/942 record waiting/rejoined, with Skie still at 250,000 XP. Independent
  saved-data comparison confirms the same unique actor, all nine item records,
  equipment slots and known spells are preserved; other party XP is unchanged.
- **Shar-Teel dismissal/rejoin, repaired native pass:** native removal in
  BD0102 originally left her unable to talk outside the crypt (save 932).
  The narrow repair reuses her existing neutral question and join/wait replies,
  preserving every original crypt state. Loading that stuck save and talking
  normally now allows her to rejoin. Save 940 (`CSR AFK 10 - SharTeel rejoin
  verified`) retains the original Shar-Teel at 422,163 XP. Independent comparison
  with save 932 preserves all 13 item records, equipment slots, known spells
  and other party XP. Evidence: `native-rejoin-evidence.json` in the companion
  audit directory.
- **Other changed companions, source audit:** all 17 retained BG1-only actors
  were inspected. Xan/Yeslick's normalized names still had palace removal
  actions; the installed retention repair removes only those actions. Real
  WeiDU tests and an actual-resource rehearsal passed, but the user's legacy
  Xan actor does not exercise the normalized identity. Several other retained
  companions share crypt-only rejoin gates, and Yeslick's configured SoD
  dismissal dialogue is missing in this stack. Existing-text repair candidates
  are recorded in `research/data/issue197-companion-audit/AUDIT.md`; these
  broader routes remain audit findings, not installed or individually tested
  fixes. The old imported-Imoen path also remains a separate untested case;
  the palace tests used the newly created CSRIMO actor.
- **Amulet, native pass:** saves 934/935 show BDMISC68 moving from BD5000's
  existing dead fighter to the protagonist through normal quickloot. The
  complete item record is unchanged; the corpse's other three records and all
  party XP remain unchanged. The helper positioned the party west of the
  nearby trap and did not create or grant the item.
- **Camp chest, native pass:** normal lockpicking opened BD1000 Container009.
  Save 936 contains all five fixed added records, three valid random-table
  results and its original sword. Normal UI pickup of the Gemblade produces
  save 937: only that item moves to the protagonist, with its record unchanged.
  The other eight chest records, other carried items, XP and gold are unchanged
  across that pickup. The earlier arrival/lockpicking interval is excluded from
  the reward baseline because it added 920 total party XP.
- **Mizhena, native pass:** her actual BD1000 dialogue consumes the looted
  amulet, completes the quest and awards 500 gold plus 1,000 raw saved XP to
  each of six members (937 to 938). A normal reload and repeat conversation
  produce save 939 with no repeated item transfer, XP or gold. Imoen's effective
  XP gain is 900 because the installed Trickster kit applies 90% XP; her raw
  saved award is the full 1,000. No kit correction was made.
- **Final source validation:** 209 main tests, 41 research tests, 14 ending
  self-tests and 53 WeiDU parse checks passed. Actual-resource rehearsals also
  verified the two dialogue repairs preserve unrelated states/table rows and
  are idempotent. These checks do not establish fight balance or native
  acceptance of the remaining companion candidates.
- **Appearance, unresolved:** the reported bad appearance was not clearly
  present after restarting. Khalid's wake/ready diagnostic showed no discernible
  change; removing/re-equipping armor visibly changed/restored his armored
  paper doll. This neither establishes a fix nor disproves the reported rest
  issue. No permanent appearance patch was applied.
- **Tooling limitation:** 22 Remote Console smoke checks passed, but invoking
  the native load-menu sequence directly from its render callback crashed in
  Infinity_PopMenu. Subsequent normal UI loads worked. Keep this tooling crash
  separate from mod acceptance; never repeat that remote load shortcut.

**AFK handoff:** the game is paused in BD0102 with all six party members.
Load `CSR AFK 12 - Party ready` (save 942) to resume this palace branch. Skie
has 250,000 XP; the other five retain their pre-test XP. The amulet/chest tests
are separate disposable branches and have not advanced this palace save.
The original named user checkpoints remain available. No merge, push or
release was performed during this AFK test batch.

### September 13: bridge preparation and potion report

The user returned to checkpoint 942, replaced Skie with Imoen, and reported that
Skie's two invisibility potions could not be moved. The saved stack is
`DW#PTN10`, an SCS NPC-only clone; its instance flags are zero, while the ITM
resource lacks the droppable flag. The current `POTN10` differs only by that
flag. The other stock SCS token on BDSKIE can similarly produce `DW#PTN45`
(Freedom), also equal to `POTN45` apart from that flag. The requested outcome is
a permanent component-197 compatibility fix, rather than acceptance of a
one-off test-actor repair. `comp197_potions.tpa` now converts these two stock
clones only on recruited palace BDSKIE, after checking each installed pair is
identical except for the droppable flag. This runs in her existing script and
therefore covers both fresh token rolls and saved recruits. No-SCS and
single-pair installations are supported. Twelve focused tests, all 221 main
tests, 54 installer parse checks, and an actual-resource copied rehearsal pass.
The rehearsal changed only BDSKIE.BCS, preserved its original script suffix,
was idempotent and restored exactly on synthetic uninstall. The source game
was not changed by that rehearsal. The permanent fix has not been installed
into the open test game; native potion movement is still unverified.

The current party was preserved in save 943 (`CSR TEST 13 - Before bridge
staging`). Native rest/healing produced save 944 (`CSR TEST 14 - Fully rested`):
all six are at full effective HP, and every saved memorized spell is ready.
XP and gold are unchanged. The current party contains Imoen, not Skie.
Derived evidence: `bridge-evidence-20260913/rest-943-944.json` under the isolated
Combined test directory.

**Control preference:** use the remote console for game actions. The user is
busy on the computer; ask them to perform any required UI action or provide a
screenshot. Do not use Computer Use without a new explicit request.

The reviewed bridge staging uses Chapter7/plot279 and the southeast approach
near [1872,2480]. Leave the retreat and owned encounter flags zero while arrival
settles; pause before setting only `bd_crusaders_retreat=1`. Unpausing should
then execute the installed native fallback and initialize the fight. Opening
mage buffs have no distance gate, so do not initialize the roster while waiting.
The user finished Edwin's arrival dialogue, restoring remote-console polling.
All six reached BD2000 at full effective HP, plot279, with all owned encounter
flags zero and no owned fight actors. However, native area setup moved Khalid
to [2900,1310] and reset his NPC behavior. The mod already has an
InPartyAllowDead guard in skip2000; the staggered test transfer may temporarily
have made that actor unavailable to area-script lookup. The exact cause is
unproven, so no speculative production guard was added. Reloading rested
checkpoint 944 and sending Khalid first reproduced the reset. Setting an area
variable before BD2000 was loaded did not persist; do not reuse that approach.

**Bridge staging, live ready; native save pending:** with BD2000 loaded and
`BD_KHAL_SPAWN=1`, native actions restored Khalid's known checkpoint-944
settings: EA2, specifics1, scripts BDKHALID/AGEN/empty/empty/DPLAYER2, dialogue
KHALIJ, and zero-valued joined/retreat/default-location locals. His baseline
42 permanent effects have no identified match for the native rejuvenation
spell's removal effects; no effects were recreated. Exact post-transfer saved
effect equivalence remains unverified. Edwin's local `BD_EDWIN_WAIT=1` avoids
repeating the arrival conversation already completed by the user. These are
test-fixture adjustments, not production changes or a native group-travel test.

All six party members now resolve in BD2000 at the six southeast staging
points, each with PC allegiance, full effective HP and fatigue0. Khalid's five
script slots and specifics were verified after queued actions executed. The
game remains paused at Chapter7/plot279. Only the loaded area's
`BD_CRUSADERS_RETREAT` was then set to1; `BD_BRIDGE_PLOT`, `CSR256_REQUEST` and
`CSR256_STAGE` remain0, and all eight owned encounter actors are absent.
Evidence and the guarded staging scripts are outside the repo in
`bridge-evidence-20260913`, including `bridge-ready-live.json`.

The user made native save945, **CSR TEST 15 — Bridge ready**, won the fight,
and completed Bence's dialogue. They reported that the encounter worked well
but was too easy. The invisible barrier where the removed barrels stood stayed
closed until that conversation. They then made save946, **CSR TEST 16 — Bridge
won, Bence done**. Both folders were verified to exist. A pre-Bence replay is
not required now; the user is willing to replay from945 if later needed.
See the [bridge acceptance record](2026-09-08-bridge-finale.md#september-13-native-feedback)
for the diagnosed barrier cause and the subsequently approved tuning.
Native saved-state parsing/reload and individual cast verification remain open.

### September 13: first stronger bridge revision, installed and replayed

The user approved opening group Haste, slightly deeper mage positions and group
engagement from a real sighting. The fire mage now starts at [1456,1860] and the
earth mage at [1344,1920]. Their opening Haste spends one copy on every tier.
The eight actors and **4,520 total kill XP** are unchanged. Static geometry
covers walkable footprints and the installed Haste radius; native movement and
actual group buff delivery still need checking.

Insane now has level-14 mages and one full sequencer each: earth **Greater
Malison then Slow**; fire **Dispel Magic with Spell Revisions, or Remove Magic
without it, then Fireball**. Other difficulties retain level-13 mages. The
payloads are reserved from finite spellbooks and release once; the fire sequence
can wait for a target clear of allies. Disabled/silenced casters cannot release
their stored charge. Bence's source revision makes him approach after victory
and start his existing wrap once combat clears and dialogue is possible. The
wrap still opens the passage before the onward vision.

Additional mages and a cleric remain deferred. The retired script-engine worktree
did contain real AoE ally-buff work: the surviving branch has a callable helper
tested Hasting its caster and an ally. Automatic hostile-AI integration and an
installed encounter-wide buff system were not established by that evidence.

That revision's checks passed: 252 regression tests (94 bridge), 41 research tests,
14 ending self-tests, and 55 installer/library parse checks. A public-install
rehearsal against copied Combined resources also passed, preserved Bence's native
initialization and original script body, and restored the disposable override
byte-exactly on uninstall. All 132 actual resource inputs and TLK/log were unchanged.
See `research/data/bridge-tuning-20260913-actual/report.json` for local evidence.

The user subsequently authorized installation: the stronger bridge revision and
Skie potion correction are now tail-installed in Combined (row424), with all eight
outputs/six backups verified and unchanged TLK. The replay used
**CSR TEST 15 — Bridge ready** on Insane: parsed save945 contains no spawned
encounter actors and has all six members rested, so no staging helper was needed.
Its result is native save 947 (`CSR TEST 17`), described below. Full installation evidence is in
`C:/Users/chris/CEBG-Tests/Combined-20260908/bridge-tuning-install-20260913/installed.json`.

### Save 947 feedback and latest correction — installed, native replay pending

The user reported Bence arriving late, the fire sequencer never releasing, and
Haste not being observed. Fire-mage saved locals `CSR256_PREP=1`, `CSR256_HASTE=1`
and `CSR256_SEQUENCE=1` establish the preparation/Haste attempt and an unreleased
stored sequence. Earth has `CSR256_SEQUENCE=2`. The Haste flag does not prove
delivery; expiry before the party approaches is only a hypothesis. The user then
explicitly directed Haste to wait until the fire mage sees an enemy and target
an elemental. Source now prefers the central fire elemental, with other owned
elementals as fallbacks; guards can benefit but cannot be the target. The one-copy
budget is unchanged. This timing change still needs native delivery verification.

The approved fire sequence is now **Dispel Magic with Spell Revisions, or Remove
Magic without it, then Flame Arrow**, replacing Fireball. Insane keeps two Flame
Arrows, one for the sequence and one ordinary reserve; it has one ordinary
Fireball on SR and none where level-3 Protection from Fire occupies that slot.
Haste/dispel copy counts and defensive reserves are unchanged. Bence must wait until combat
clears, then **appear beside the party** to initiate his existing wrap; no long
walk from his old spawn. The wrap still opens the passage.

These latest corrections are installed in Combined as row 425, superseding the
row-424 Fireball/approach/spawn-Haste build. The 252-test and other totals above
apply to that earlier build. The latest exact tail rehearsal and disposable
restore passed, together with **96 bridge tests** (28.563 seconds, no skips);
no broader new test result is claimed. Installation ran with the game closed,
preserved all 424 previous package/language/component rows, verified three outputs
and three backups, and left the TLK unchanged. Evidence:
`C:/Users/chris/CEBG-Tests/Combined-20260908/bridge-correction-20260913/installed.json`.
Preserve saves 945–947. Checkpoint 945, **CSR TEST 15 — Bridge ready**, is suitable
for the next Insane replay. Native Haste delivery and replay remain pending; the
soldier's remaining barrel-transport text and save/reload checks remain open.

### Latest row-425 user replay

The user won, approved the much harder fight, and explicitly confirmed Bence
arrived promptly after combat. Combat feel and prompt arrival pass by user
observation; individual spell effects and save/reload have not been independently
verified. Save after Bence as **CSR TEST 18 — Extra Challenge bridge won**, reload,
then cross the opened passage and check for no duplicate encounter/reward.

The user clarified the exact split: regular Insane keeps the current fight,
including Haste and all other changes, but omits both mage sequencers. The
optional Extra Challenge component257 adds only those sequencers. Its source
extraction is implemented and offline-verified; the installed row-425 test resources still contain
the accepted challenge version. The bridge design records the two preserved
build manifests and open pack integration details for the other task; the
gameplay boundary is decided. Both source modes preserve the same level-14
Insane mages, spellbooks and world setup; regular AI can use the payload spells
as ordinary casts, but does not prepare or release a sequencer.

The subsequent test order was bridge persistence, the assassin ambush, then
Guardian/Shadow Aspect. This historical order is superseded by release preparation;
do not repeat already accepted palace/Liia or native amulet/Mizhena checks.

**Bridge persistence/onward check completed:** the user saved/reloaded, crossed
and reported no problem. Save949 (`CSR TEST 18 — Extra Challenge bridge won`)
exists; the subsequent read-only remote snapshot showed paused BD2000, plot295,
and all six living party members beyond the bridge. Native user-observed pass.
Random protagonist speech is left outside this investigation at the user's
request; their suspected soundset mismatch is not a confirmed diagnosis.

**Assassin staging queued:** read-only parsing of save949 confirmed no cached
BD0063.ARE. From paused post-crossing BD2000/plot295, the remote console executed
the native BD5000 successful queue branch once: BD_FRE=1, eight-hour URE timer,
BD_URE2=1, ForceRandomEncounterEntry("BD0063","ExitW"). The game remains paused
in BD2000; the user must take normal world-map travel to consume the queue.
No BD0063 initialization, enemies, completion or rest flags were set. The
test-only queue intentionally replaces an earlier pending encounter (URE4=1);
preserve save949 as the unmodified parent. Native arrival remains unverified.
Helper/result: `C:/Users/chris/CEBG-Tests/Combined-20260908/assassin-evidence-20260913/`.

**Travel staging blocked:** the user reports that the world map still treats
this shortcut save as being in the city, preventing the intended journey.
The remote snapshot before opening the map was BD2000/plot295/Chapter7. Do not
claim the queued travel launcher passed or infer a production component135 bug.
Use direct placement at BD0063's native ExitW to test area initialization,
retained assassins, magic and rest unlock separately. This fallback has not yet
run: read-only console probes time out while the user is on the world map;
return to the paused world screen before staging. Do not rerun the existing
one-shot encounter queue; its flags were already set successfully.

**User stopped the assassin test after a magic pass:** direct placement reached
BD0063 with Viconia, Edwin and Shar-Teel. Native initialization advanced URE2 to2
and FRE to0; the earlier forced-travel queue was cleared with the documented
`ForceRandomEncounter("")`, and `IsForcedRandomEncounterActive("BD0063")` returned
false. The protagonist, Khalid and Imoen still remained in BD2000 at the last
read-only snapshot. Thus this was a partial-party area test, not a completed
checkpoint or travel-launcher acceptance.

The user reported casting a spell and observing it continue to last, then
explicitly ended testing. Record native spellcasting and persistent magic as
user-observed passes; do not assert an independently measured duration, full
combat, rest unlock or complete dialogue-text coverage. No further game actions
were taken after that instruction. Resume from intact save949 / CSR TEST18 for
future staging, not from the temporary split-party runtime state.

Staging diagnosis: the response parser compiled only the first action when
several BCS actions were put on one line. A read-only comparison produced `[86]`
for the one-line recovery and `[86,110,86,472]` with newlines. The first recovery
therefore only changed interruption state; it did not transfer the missing PCs.
The corrected newline recovery validated all four actions but aborted at its
paused-state assertion before any mutation because the user had resumed play.
Do not rerun any guarded staging helper blindly. The original map-edge partial
transfer's exact cause was not separately established. Logs/scripts remain in
the isolated `assassin-evidence-20260913` folder; no production component changed.

### Guardian pass and Shadow Aspect staging

**Latest status: user stopped and quit the game; native follow-up is deprioritized.**
The summon check is unfinished and not a release blocker; there is no saved
Shadow Aspect checkpoint. Mislead's unlimited two-round retry remains in the
inspected installed script; the one-use component266 correction is implemented
and offline-verified, without a new native pass.
The user wants the whole encounter made trivial eventually, as deferred work.
See [the September 13 evidence and optional resume record](2026-09-13-shadow-aspect-resume.md).

After the user accepted Edwin's spellcasting/persistence sample and requested
the next test, they reloaded save949 and paused. Its party coordinates matched
the live group (portrait and join order differ); neither BD5110 nor BD7230 was
cached in the save. Newline-separated, compiled-action-validated transfers
moved all six members and paused after all six arrival callbacks. No quest or
enemy-state flags were set. Native `Rest()` was applied for spell availability;
it did not heal Khalid's42HP, so this is not a full-heal claim.

**Guardian, native active-state pass:** in freshly loaded BD5110, the
UNSLEEPING_GUARDIAN/BDUNSLGU placed record retains schedule0. The live area object
list still contains its sprite at[681,924], but `IsActive(Myself)` on that sprite
returns false while ordinary nearby BDSHAD04 shadows return true. Enumerating a
sprite is therefore not evidence that the removed encounter is active. No user
fight in this area was needed.

**Historical ready snapshot, summon test still pending:** the party was paused together in
BD7230 at[2216,2082], [2264,2082], [2312,2082], [2248,2118], [2296,2118],
[2344,2118], inside the chamber and outside trap/door footprints. Insane was
verified with Difficulty(HARDEST). BDASHIRU is alive at[2393,2005], hp81,
bd_summons=0; no BDSHAD04 or BDSHSOUL summons had appeared in the ready snapshot.
The original intended sample was one native summon cycle: two ordinary Shadows
and no Shadowed Souls, without finishing the fight. It did not run to acceptance
and is now deferred. If revisited, avoid the confusion trap south of the chamber.

Evidence/helpers: `C:/Users/chris/CEBG-Tests/Combined-20260908/filler-evidence-20260913/`
(`guardian-active-state.json`, `aspect-ready-state.json`). These are live staging
snapshots, not native saved checkpoints. The user then ended testing and closed
the game; summon acceptance remains unfinished.

The user wants the easiest setup and is happy with an existing party of any
reasonable strength. Do not spend preparation time rebuilding or balancing a
new party. This session checks mechanics and sequence behavior; tuning can use
the user's observations of an overpowered or underpowered group.

## Starting point

Use the finished game at
`C:\Users\chris\CEBG-Tests\Combined-20260908\game\InfinityLoader.exe`, with
that game directory as the working directory. Its isolated profile is
`C:\Users\chris\OneDrive\Documents\CEBG Combined Playtest 2026-09-08 - c2a832a75741`.
September 12 update: the game has been launched, saves are present, and Debug
Mode was enabled in this isolated profile while the game was closed. Restart
through InfinityLoader before using Ctrl+Space.

The user explicitly selected **jajaja i am lord** on September 12, replacing
the older proposed test seed. Source:
`C:\Users\chris\OneDrive\Documents\Baldur's Gate - Enhanced Edition Trilogy - Chriz RC 20260903\save\000000055-jajaja i am lord`.
An identical GAM/SAV copy already exists under the Combined profile's `save`
directory; its party and story data have not been edited by this preparation.

Inspection found six living party members in BG0800, Chapter 5, **no saved SoD areas**,
and no missing resources among the 289 distinct party item/spell/script/dialogue
references checked against the finished install. Begin with a brief native load,
party/spellbook inspection, save and reload. Cross-stack character effects and
string references are not thereby proven identical. This is a practical scene
test party, not acceptance of current Kitpack grants or companion rebalance.

Do not return to the superseded CSR910 baseline without a reason. The separately
named `CSR910 BEFORE SKIP` also contains extra fixture flags. Do not use the
late CSR290 ending seed for fresh-area tests: BD2000 and
several filler maps are already cached there. If the preferred baseline fails
the load smoke, use a fresh party on the final stack instead of repairing the
old save indiscriminately.

From the copied baseline, reuse the previously verified native `BDSODTRN`
transition recipe. Allow BD0120 and the original SoD initialization to run.
Make an untouched arrival baseline before branching the tests. A direct jump
into the palace would bypass the very import/startup behavior we want to check.

## How the shortcuts work

Prepare named native saves, each just before the real interaction under test.
Test-only Lua/console staging can position the party and establish the upstream
chapter/quest conditions, then stop. Production scripts must perform the fight
spawn, reward payment, item pickup, quest completion and campaign handoff.

Keep an unvisited-area parent save for every affected map. Once a checkpoint is
created on this final stack, it may contain that correctly initialized map and
be reloaded normally. The restriction is against importing an old map snapshot,
not against saving immediately before a freshly prepared fight.

The user loads a save, follows a short instruction, and reports the result.
The agent handles staging, numeric XP comparisons, actor/effect checks and
before/after evidence. No campaign traversal between unrelated tests is needed.
For a doorway/travel test, however, walk through the actual doorway: teleporting
to its destination would bypass the changed link.

EEex and LuaJIT are installed. The simplest proposed controller is a test-only
Lua file outside the game, loaded through the normal Lua console after checking
that `dofile` is available. It can expose one short command per checkpoint;
the user ultimately needs only the resulting named saves. No additional WeiDU
component is required for this method. Remote Console v0.2.0 was tail-installed
during the authorized AFK session. It supplies serialized world-state reads and
queued BCS actions. Use normal UI for checkpoint loads. Quicksaves can be copied
in full to new descriptive save-directory names when native text entry is unavailable.
Keep helpers and evidence separate from production mod sources. If desktop
control is occupied by another agent, defer input and continue read-only work;
use one owner and one serialized console client during staging.

## Original first-session checklist — retained for coverage reference

This checklist does not establish a mandatory next session. Current release
preparation takes priority; preserve the accepted results above without replaying
them, and leave the unfinished Shadow Aspect sample deferred.

Budget roughly **35–55 minutes of user interaction**, excluding checkpoint
preparation and bug investigation. These are estimates, not timers.

| Named checkpoint/group | User action | What it establishes |
| --- | --- | --- |
| **Bridge — before retreat encounter, updated copy** | Fight once on Insane; confirm Bence appears nearby after combat; save/reload and walk onward. Allow the opening casts time to happen before killing the mages. | Haste diagnosis, dispel/Flame Arrow and Malison/Slow once-only sequencers, coordinated engagement, defensive recasts and automatic Bence wrap. Same two mages/two guards/four elementals, with no barrels/portal. About 10–15 minutes. |
| **Assassins — before road ambush** | Enter with a long-duration buff, cast a spell, fight, then try resting. | Assassins retained, buffs/casting survive at least two rounds, no dead-magic text, normal rest unlock. About 3–5 minutes. |
| **Palace — arrival and jailbreak** | Choose No at the skip offer, recruit Imoen, follow celebration/jailbreak, return for Liia's reward, sleep/council and recruit Skie. | Normal startup and impound, no unwanted assassination/Entar/Skie-night scene, 22,000 XP per character once, playable companions and departure. About 15–20 minutes. |
| **Quest loot — corpse and Mizhena** | Already completed autonomously; no user repeat needed. | Native pickup, turn-in, exact reward and no duplicate on reload passed in saves 934–939. |
| **Guardian / Shadow Aspect** | Guardian check passed. Shadow Aspect's summon sample is deferred at the user's request. | No additional native check is required for this release; the unfinished sample is not a pass. |

The bridge's alternate siege/cinematic entry can be checked by the agent from a
separate branch. The user need not fight every difficulty or both entry routes.
The agent should check actual ally Haste effects rather than treating the
vanilla haste-state bit as authoritative on Spell Revisions.

Liia's before/after XP snapshot starts **after Korlasz's fight**, immediately
before the upstairs payment. That excludes kill XP. A reload after payment
must not grant another award. Other chapter awards are party XP and retain
their own ledger values; the flat 22,000 decision applies to Liia's award.

## Original second-pass checklist — retained for coverage reference

Allow roughly **20–35 more minutes**, or split this into a later session.
Previously accepted pool and ending cases get brief regressions; the user does
not need to repeat the old exhaustive inventory matrix.

| Checkpoint/group | Fast native check | Agent work and limits |
| --- | --- | --- |
| **Coast Way camp / crossing** | Chest pickup already passed. Remaining: check Rasaad and the removed forest destination; walk the crossing scene, including a short skipped-cutscene branch. | All eight added chest records and preservation of old contents verified. Still check no force wall and the retained five-round crossing sequence. This is the earlier crossing, separate from Boareskyr. |
| **Dig site / pool** | Briefly inspect the changed rooms; take the rehomed Essence from its sarcophagus and use the pool normally. | Prepare near the relevant objects, skipping travel. Preserve actual ingredient pickup/insertion/payment. Confirm one omen and no repeat payment after reload. Existing pool acceptance supplies prior evidence. |
| **Forest of Wyrms / temple** | Walk the dragon-cave/temple link both ways and inspect the reduced ambush area. Optionally wake Morentherene on Hard/Insane. | Agent checks difficulty stat application and one-time behavior. A full dragon fight is optional tuning feedback, not required merely to prove the route. |
| **Scouting areas / Kanaglym** | Short scene samples if desired; use checkpoints near retained quest actors. | Agent checks the complete cut lists, remaining actors, banned creatures and compensated awards. A user need not hunt every removed creature or replay all scouting quests. Label these as resource coverage unless the relevant native closure is actually run. |
| **Basement reveal** | Enter with a buff, watch the reveal; repeat once using scene skip if practical. | Stage before the original launcher, not after the reveal. Confirm buffs survive both paths and control returns. Full prerequisites still need a preparation dry run. |
| **Victory → BG2** | Start just before the native return from Avernus, follow the celebration/Dazzo choice, save/reload and reach the BG2 opening. | Reuse the verified ending staging recipe. No unchanged Avernus boss replay, no direct plot590 shortcut, no item-by-item delivery checklist. Sample normal equipment import using the accepted reduced approach. |
| **Skip SoD — Yes branch** | Reload palace arrival and accept the two-confirmation skip. | Check normal BG2 opening and one protagonist +250,000 award. The **No** branch is already covered by the palace route. Prior Yes acceptance avoids rebuilding its complete inventory matrix. |

One ordinary rest during the palace/camp checks gives a smoke check for rest
and dream behavior. The reduced random-ambush probabilities are checked from
installed area data; a handful of rests cannot measure their statistical rate.

Optional Ymori: use the fresh bridge branch for a two-minute body/activation
check. Keep it bounded, as agreed; it is not a release-blocking demand for a
complete side-quest playthrough.

## Verified preparation seams

These are implementation notes for checkpoint preparation, **not a bulk console
script to run on a campaign save**. Each recipe needs a native dry run before
handing its save to the user.

- **Bridge, BD2000:** native fallback checks `bd_bridge_plot<2` and
  `bd_crusaders_retreat=1`. It opens the gate, disables the blockade and queues
  the owned encounter. Leave `CSR256_REQUEST` and `CSR256_STAGE` zero before
  that seam; never manually create the roster or mark it victorious. After the
  eight actors resolve, native progression reaches plot293; Bence near
  [2425,2660] provides the onward step in the original build. The earlier row 424
  made him approach after combat. Installed row 425 now waits for combat
  clearance and creates him beside the party for that dialogue instead.
  Source: [comp256_world.tpa](../../chriz-sod-remix/lib/comp256_world.tpa).
- **Ambush, BD0063:** prefer the native queued random-encounter entry at ExitW
  followed by normal travel. Leave `BD_Init=0`; do not preset rest-unlock or
  encounter-completion flags. A direct teleport would prove area behavior only,
  not the travel launcher. Source: installed BD0063.BCS and
  [comp135.tpa](../../chriz-sod-remix/lib/comp135.tpa).
- **Amulet:** BD5000 `Dead_fighter` [4295,1098], item BDMISC68. Stage west of
  the corpse: the trap immediately east spans approximately x4320–4441,
  y1022–1418. The verified turn-in uses existing Mizhena in **BD1000** near
  [85,3740] on the Chapter7 branch. Higher-chapter cleanup can remove this
  actor; do not force quest/completion flags. Let her real dialogue consume
  the looted item. Do not grant the amulet in the helper.
  Source: [comp265.tpa](../../chriz-sod-remix/lib/comp265.tpa).
- **Banned creatures:** BD5110 Guardian location [681,924]; Shadow Aspect is
  in **BD7230** near [2393,2005]. Select Insane before engagement and verify an
  actual summon cycle occurred; killing it early does not test the correction.
- **Jailbreak:** approach the BD0102 basement stairs near [591,198] with the
  hint unfired. Let the cell interaction and subsequent combat advance the
  native state. Liia's return/payment requires the completed celebration,
  Korlasz dead, plot50 and no combat. Sources:
  [jbhint.baf](../../chriz-sod-remix/baf/jbhint.baf),
  [csrceleb.baf](../../chriz-sod-remix/baf/csrceleb.baf),
  [csr175.d](../../chriz-sod-remix/dlg/csr175.d).
- **Camp chest:** BD1000 Container009 [509,3220], fresh area.
  **Pool:** BD1200; Sarcophagus01 [2414,1736] holds the rehomed Essence.
  Sources: [comp900.tpa](../../chriz-sod-remix/lib/comp900.tpa),
  [comp225.tpa](../../chriz-sod-remix/lib/comp225.tpa).
- **Ending:** native BDCUT58 → Caelar/Aun dialogue → BDCUT59/59A/59B.
  Adapt `C:\Games\csr290-test-20260905\evidence\stage-r1.lua` as a recipe;
  do not run its old assumptions blindly. The final-fight redesign is still
  future work; component290 changes the return/ending spine.

## Coverage and result recording

| Installed components | Coverage group |
| --- | --- |
| 110, 120, 140, 145, 150, 160, 170, 175, 180, 185, 187, 190, 195, 197 | Native arrival, palace mini-route; a brief fresh-SoD branch separately checks no default party. |
| 100, 130 | Installed-data audit plus normal rest/dream smoke; not a statistical trial. |
| 135 | Assassin ambush. |
| 200, 210, 215, 245, 900 | Coast Way camp, crossing, removed map/loot and reward checks. |
| 220, 225 | Dig-site roster/reward audit and pool regression. |
| 230, 255, 256 | Road-north audit, optional Ymori, native bridge/aftermath. 256 supersedes 255; do not test obsolete barrels. |
| 240, 250 | Forest/temple route, retained quest/reward and dragon difficulty checks. |
| 260, 265, 270 | Scouting/quest/XP audit, native amulet and Guardian/Shadow Aspect checks. |
| 280 | Basement reveal and skip branch. |
| 290, 910 | Ending and optional full-skip branches. |

Tail repairs 176/235/291 and alternative treasure selection901 are not selected
in this fresh combined installation; their automated tests are not native
acceptance of that alternative configuration. The future Ashatiel redesign and
bridge collapse timer are not implemented and are outside this session.

For each prepared checkpoint record the game/source fingerprint, parent save,
staging actions, before/after native save, observations and status. Distinguish
**native pass**, **resource/automated pass**, **not run**, and **blocked**.
Remote acknowledgement, if used, only means queued work: confirm resulting
world state and native save persistence. Use native UI for save/load and keep
the original saves intact. No release or merge follows automatically from
preparing the checkpoints.

Related acceptance records:
[filler fixes](2026-09-08-filler-fixes.md),
[bridge](2026-09-08-bridge-finale.md),
[ending](2026-09-06-ending-runtime.md),
[pool](2026-09-05-scrying-pool-v065.md).
