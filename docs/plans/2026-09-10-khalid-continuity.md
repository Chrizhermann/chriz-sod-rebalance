# Khalid carryover and Bridgefort continuity

Status: direction approved on 2026-09-10; unreleased component 115 is being integrated
onto v0.6.9. The earlier designated-dev installation is historical evidence.
Native normal fort-entry and quest-route acceptance remain pending. The revised
arrival protection and Combined tail installer have passed offline verification.
The user accepted a modest conditional rewrite, prioritizing clean implementation and
consistency over a story overhaul. This addresses the Khalid/Jaheira consequences of
component 110 without redesigning the siege or its barrel finale; completeness is
not established by the previous installer checks.

## September 14 integration and reproduced entry failure

The Combined playtest copy lacked component 115. Entering BD2000 reproduced an
immediate Khalid reset, so normal fort continuity is not accepted. The earlier
bridge-finale test used staged progression that bypassed this route and cannot
serve as its acceptance evidence. The existing 115 has not yet been demonstrated
to solve this reproduction. The current work corrects its arrival protection
before another user test; do not repeat the failed baseline merely to reconfirm it.

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
- Read-only remote inspection confirms the failed session remains paused, with
  Khalid at `[2900,1310]` and route/carry markers unset. Direct party-slot identity
  works in that session. This does not prove fresh-entry timing or acceptance.
- The real Combined game has not yet received the patch. Close it before the
  prepared installation; reload a clean pre-entry checkpoint afterward. Do not
  repair the current neutralized Khalid by hand and count that as a product pass.

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

Required evidence: real WeiDU compilation against effective-resource fixtures; preserved
ordinary dialogue/progression branches and gift rewards; clean failure on missing or
changed resources; carried entry/menus; scene actors and party safety; attack, waiting for
the Fist, surrender and betrayal flags. Dev installation is separate from native playtest
acceptance. Runtime cases include Khalid alive/dead/dismissed, Jaheira present/absent,
save/reload, and completion through the bridge and onward campaign progression.

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
