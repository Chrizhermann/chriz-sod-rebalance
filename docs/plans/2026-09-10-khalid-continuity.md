# Khalid carryover and Bridgefort continuity

Status: component 115 is ready for the **v0.6.10 release**, authorized by the user
on 2026-09-14. The earlier designated-dev installation is historical evidence.
Native BD2000 entry, normal wardstone transport and Adirran's briefing passed on
2026-09-14 with Khalid remaining controllable. Saved control state is also verified;
reloaded behavior and later quest branches remain unverified in the native game.
The revised arrival protection and Combined tail installer have also passed
offline verification. Wynan's separate observation below does not block shipment.
The user accepted a modest conditional rewrite, prioritizing clean implementation and
consistency over a story overhaul. This addresses the Khalid/Jaheira consequences of
component 110 without redesigning the siege or its barrel finale; completeness is
not established by the previous installer checks.

## September 14 integration and reproduced entry failure

The Combined playtest copy initially lacked component 115. Entering BD2000 reproduced
an immediate Khalid reset. The earlier
bridge-finale test used staged progression that bypassed this route and cannot
serve as its acceptance evidence. The original unfinished 115 also had an entry
protection gap and an installer conflict with 256. Both were corrected before the
successful fresh-entry test described below.

Preserve the September 10 source/fixture/dev-install evidence below as historical.
It does not describe the Combined copy or establish the current correction's
success. The v0.6.9 release and its accepted finale remain unchanged by this record.

The revised installer protects both native recruiter blocks directly, checks
Khalid's identity in all six party slots as well as the named actor lookup, and
waits for occupied slots to arrive before selecting the ordinary fresh route.
It uses party count rather than a temporarily unresolved actor to identify an
empty slot. Already-started quests retain their separate fallback.

Component 115 and the bridge replacement now compose in both install orders.
The carried aftermath omits Khalid's NPC retreat orders while retaining the
combat-clear gate, enemy checks and prompt Bence arrival.

September 14 verification:

- All 300 tests in `tests/` passed with WeiDU 249 and the copied pre-115 EET
  fixture, including the two component install orders.
- All 18 continuity checks also passed with current Combined resources. A test
  previously hardcoded Jaheira's EET reward state 1162; Combined uses 1151. The
  test now binds by native speech and proves her entire party dialogue unchanged.
- Rehearsing public 115 against the actual Combined log preserves its 425 prior
  entries, emits 37 resources, preserves 330,069 existing strings and adds 55.
- Read-only remote inspection of the failed session showed it paused, with
  Khalid at `[2900,1310]` and route/carry markers unset. Direct party-slot identity
  worked in that session. That snapshot alone did not prove fresh-entry timing or acceptance.
- After the user closed the game and authorized installation, public 115 was
  appended to the real Combined copy as entry 426. All 425 previous entries remain
  in order; all 37 outputs and the resulting TLK match the rehearsal byte for byte.
  Input resources outside the change set remain unchanged. Backups and the
  installation receipt are under the test copy's `khalid-continuity-20260914/`.
- **CSR TEST 14 - Fully rested** provided the clean checkpoint. Direct save parsing
  confirms no cached BD2000/BD2100, a living party-controlled Khalid, and unset fort
  progression/continuity markers. GAM/SAV hashes remain unchanged after installation.
- After the fresh retest the user confirmed that BD2000 arrival, the normal wardstone
  circle and Adirran's completed briefing all worked with Khalid still controllable.
  A read-only remote snapshot independently records all six companions in BD2100,
  `csr_kh_fort=1`, `csr_kh_carry=1`, `csr115_briefed=1` and
  `bd_bridgefort_plot=5`. Khalid is with the party at `[2016,892]`; his retreat flag
  remains 0. No manual allegiance/script repair was performed in this retest.
  This accepts the reproduced entry/control bug and initial briefing; it does not
  claim save/reload, later command branches or the whole fort quest were played.
- Read-only parsing of **000000954-CSR TEST — Khalid fort fixed** confirms Khalid
  is saved with party allegiance **2** and `KHALIJ` dialogue, with all six companions
  in BD2100 and the carried route/briefing recorded. This proves the control state
  was saved; it is not an observed native reload.

## Non-blocking sidenote: Wynan

The user reported that Wynan Hess did not initiate the post-impact conversation
after some Ctrl-J/sequence skipping. The cause is unconfirmed; the user explicitly
keeps this as a sidenote, with no new feature work or release block. No quest
flags or NPC actions were repaired, and the spellstone quest is not a native pass.

Save 954 has `BD2100GL=2`, `bd_wynan_plot=2`, `bd_jegg_plot=1`,
`bd_bridgefort_plot=5` and unset `BD_SDD200`: impact recorded, introduction not
recorded. The automatic starter is `BDBF1.BCS`, gated by no prior defender talk,
impact stage 2, sight of a party member, and Wynan dead or within range 15.

Component 115 changes neither `BDBF1.BCS` nor `BDWYNAN.BCS`; all 32 `BDWYNAN.DLG`
state-entry triggers and speeches match the backup. Only the route-dependent
referral/journal differ; impact and quest actions are preserved. The audit found
no regression attributable to 115.

## Decided

- Keep carried Khalid in the party. No forced departure to manufacture the original plot.
- When he arrives with the player, an existing defender supplies the fort's background
  and quest briefing. Khalid can contribute as an arriving ally and help lead the defence.
- When he was not carried to the fort, preserve the installed original commander route.
- Keep the existing attack, Flaming Fist coordination, preparation, surrender, betrayal,
  and spellstone mechanics. No new quest rewards or combat rebalance.
- Preserve his anniversary gift quest, with only conflicting background wording adapted.
- Remove false Khalid/Jaheira separation references and companion scene collisions.
- Implement as new component **115**, requiring **110**, so existing installations can
  append it without uninstalling or reinstalling any earlier component.

## Concrete implementation

Adirran (`BDBFORT`), the soldier who already greets the party at the wardstone entrance,
gives the local briefing. For the carried route he moves to the existing exterior
commander position after the briefing and offers the fort's command choices. This keeps
the quest accessible if Khalid dies, is dismissed, or is elsewhere. His existing defender
script continues to control the garrison's battle and surrender lifecycle.

The first pre-briefing fort visit records one persistent route:

| Global | Value | Meaning |
|---|---|---|
| `csr_kh_fort` | 0 | Route not selected yet |
| `csr_kh_fort` | 1 | Khalid arrived in the party, including dead-in-party |
| `csr_kh_fort` | 2 | Existing fort story; also the fallback for already-started quests |
| `csr_kh_carry` | 1 | Khalid was carried before his ordinary recruiter placement |
| `csr_jh_carry` | 1 | Jaheira was carried before her ordinary recruiter placement |

History markers support dialogue before the fort. They do not change an already selected
fort route. Dismissal, resurrection, and rejoining do not reset that route.

The first wardstone arrival retains all party transport, XP and quest bookkeeping, but
does not separately move the player's Khalid. His smithy stakeout cameo is skipped while
the remaining investigation continues. The stakeout's separate Adirran cameo uses a
private generic soldier identity so it cannot duplicate or dismiss the quest spokesman.
Post-battle NPC retreat assignments do not target carried Khalid.

The eight stakeout entry scripts dispatch to private copies with trigger evaluation
enabled. This matters because installed callers use `StartCutSceneEx(...,FALSE)`, which
would otherwise run both conditional versions. The private copies retain the original
route and select the carried version only for route 1.

Khalid's conflicting banter openings, biography, reunion and gift introduction are
adapted conditionally. Jaheira's recruitment/parting wording and the relevant defender
journals follow the same history. Voghiln's Jaheira-rescue introduction is suppressed
for a carried Jaheira: its original peaceful branch excludes an in-party Jaheira and
would otherwise fall through to hostility. His independent recruitment remains available.

## Compatibility and acceptance

Read the effective installed resources and validate the audited script/dialogue shapes
before publication. Append conditional states and
guarded script branches; preserve existing states, actions, quest flags and unrelated
mod additions. Party dialogue names must be resolved from the installed game rather than
assuming EET and standalone SoD share names or state numbering.

Install before first entering BD2000, ideally before SoD starts so history markers
also cover the road north. This is not a migration for a quest whose earlier contradictory
scenes have already played.

Verification covers real WeiDU compilation against effective-resource fixtures; preserved
ordinary dialogue/progression branches and gift rewards; clean failure on missing or
changed resources; carried entry/menus; scene actors and party safety; attack, waiting for
the Fist, surrender and betrayal flags. Dev installation is separate from native playtest
acceptance. The entry/control and briefing case is accepted; native reload,
alive/dead/dismissed and Jaheira-present/absent variants, later command branches
and full quest completion remain unverified. They are not new prerequisites for
the shipment the user authorized on September 14.

Automated evidence on 2026-09-10:

- 17 component-115 installer/compiled-resource tests pass against copied effective EET
  inputs with WeiDU 249. The positive install changes exactly 37 audited resources,
  preserves original quest/gift transitions and Voghiln's other 106 states, and leaves
  protected EET resources, areas and party tables unchanged. Negative fixtures cover
  missing prerequisites/resources, changed native handoffs and private-resource collisions.
- The other 45 repository regression tests, 33 research tests and 14 ending verifier
  self-tests pass. WeiDU parse checks pass for all 40 installer/library files.
- An ignored pre-115 resource baseline is retained under `.worktrees/csr115-fixture/`
  for repeatable local checks after dev installation. No game-owned data is committed.
- A disposable fixture built from effective standalone SoD resources also installs
  cleanly with WeiDU 249. `BDDIALOG.2DA` correctly binds `BDKHALIJ`/`BDJAHEIJ`, including
  the different gift/reunion/Neera state numbers. The standalone source remains unchanged.

Dev installation on 2026-09-10:

- Updated installer sources and appended **only 115** on the designated dev EET copy.
  Its prior 446 install records and their order are unchanged; the mod now has 33
  installed components there. Nothing was uninstalled or reinstalled.
- All 37 emitted resources match the tested fixture byte for byte. Hash comparison
  across 46,896 original override files confirms exactly 27 originals changed, 10 private
  resources added, no files removed, and 46,869 original resources unchanged.
- The 354,856 existing TLK entries are preserved; 55 entries were added. `chitin.key`
  and `engine.lua` are unchanged. Local source/log/TLK backups, transcripts and the
  verification report are in `.worktrees/csr115-dev-install/`. WeiDU reprinted the log's
  descriptive comments with `--save-components-name` after its initial `--quick-log` write;
  the original descriptive log is retained in the backup.
- The live install was not modified. No native game session was run for this component.

## Remaining scope

Dorn's captivity and Neera's introduction/personal-quest entry still need their own
continuity audit. Their spawn guards alone do not establish narrative compatibility.
The broader optional placement of BG1-only companions remains a separate feature.
