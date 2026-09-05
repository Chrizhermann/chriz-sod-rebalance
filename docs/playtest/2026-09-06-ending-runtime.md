# Component 290 runtime verification — 2026-09-06

Status: **the corrected EET guard, real victory/celebration sequence, celebration
reload, and user-approved reduced inventory handoff test pass. Standalone remains
pending; the original expanded runtime matrix was not completed.** No new creative
directive was needed. After the isolated runtime pass, the actual dev EET
installation received tail component 291 and passed its installed-state verifier.
The live installation remains untouched.

The user accepted release of this tested scope on 2026-09-06. Remaining standalone,
party-variant, multiplayer, and re-entry coverage is tracked in
[#17](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/17); unrun rows below
remain unrun. Release v0.6.6 integrates the existing v0.6.4 installer ordering and
v0.6.5 scrying-pool fix. All 59 integrated tests and the TP2/35-library WeiDU 249
parse check pass. The ending runtime test used the pre-merge ending resources;
the integrated release was not separately played through end to end.

## Isolated test environment

- Task root: `C:\Games\csr290-test-20260905`.
- EET game: `C:\Games\csr290-test-20260905\eet`.
- Standalone game: `C:\Games\csr290-test-20260905\sod`.
- EET profile: `C:\Users\chris\OneDrive\Documents\Baldur's Gate - Enhanced Edition Trilogy - CSR290 20260905`.
- Standalone profile: `C:\Users\chris\OneDrive\Documents\Baldur's Gate - Enhanced Edition - CSR290 20260905`.

Each clone's `engine.lua` selects its separate profile. Original saves remain in
the user's ordinary EET profile, under `save backups`; test copies and evidence
remain outside Git. Computer input is shared with other agents and must be
coordinated before native testing.
The EET process was closed after the successful run and computer input handed back
to the other agent.

## Reproduced failure and correction

The R0 seed was a copy of `000000435-safety safe`, whose saved BD4300 predates the
new import container. The staged pre-run save is in BD4300 at plot 590 with six
party members, after the actual de Lancie/Bence dialogue chain advanced the plot.
Dazzo's state-3 endpoint hid the UI and left the game in full
cutscene mode; remote-console processing also ceased. The process was subsequently
closed. This is a **FAIL of the original guard acceptance case**, not evidence that
inventory was retained: no completed post-run inventory comparison exists.

The old endpoint called `StartCutSceneMode()` and then created the carrier without
releasing full mode. Full cutscene mode stops ordinary scripts, preventing both
the carrier's guard and its normal import logic from executing. Native EET's
BD6100 caller instead uses `EndCutSceneMode()`, `SetCutSceneLite(TRUE)`, then
`CreateCreatureObject("K#TELBGT",Player1,0,0,0)`. Lite mode withholds input while
allowing scripts to run. See IESDP's [StartCutSceneMode](https://gibberlings3.github.io/iesdp/scripting/actions/bgeeactions.htm#121)
and [SetCutSceneLite](https://gibberlings3.github.io/iesdp/scripting/actions/bgeeactions.htm#338)
and the [installed native caller](C:/Games/csr290-test-20260905/evidence/native-bd6100-caller.baf).

Fresh component 290 now inserts that native full-mode/lite-mode boundary before
creating `CSRETBGT`. Its failure guard explicitly clears lite mode. Tail component
291 repairs an existing 290 installation, validates both legacy/current endpoints
and the complete first guard before writing, and leaves an already-corrected
installation unchanged. Standalone 290 retains its native credits endpoint.

The repaired R0 native retest displayed the `@29000` diagnostic and restored the
full UI. A live query confirmed `CSR_ENDING_USED=1`, `CSR_ENDING_FAILED=1`, and
cutscene mode false. The before/after save comparison passed **13/13 checks**:
all six party members retained their gear and slots, including marker `M290G001`
with two charges in Player1's `backpack13`.

The native menu then loaded the actual post-guard `Quick-Save-4` normally, restoring
all six portraits and the toolbar. A live query after reload confirmed BD4300,
plot 590, `CSR_ENDING_USED=1`, `CSR_ENDING_FAILED=1`, and cutscene mode false.
Clicking the gear button opened the Options menu, proving interaction after
reload. **R0 corrected guard acceptance passes.**

An initial marker discrepancy came from parsing a stale unsuffixed quicksave
folder. Native quicksaves rotate through suffixes such as `-2`, `-3`, and `-4`;
selecting the newest `BALDUR.GAM` timestamp resolved it. Both actual comparison
saves contain the marker with two charges.

A subsequent harness call to `optionsScreen:LoadGame()` through the remote console
while the world screen was active crashed the process. An uninitialized options
engine is the working inference, not a demonstrated cause; this occurred after
the repaired guard had completed. Restarting and using the native UI produced
the successful reload described above. This harness incident does not establish
a component 290 endpoint failure.

## Successful EET return, reload, and reduced inventory test

The user reduced inventory testing to one handoff run. This run covers the real
return sequence and celebration reload as well; it does not complete the original
expanded inventory, party-variant, multiplayer, or re-entry matrix.

Starting from native BDCUT58 staging, the run followed Caelar state 84 and Aun
states 47–48 into BDCUT59 → 59A → 59B. All six party members moved from BD4400 to
BD4300 at **2026-09-05 16:08:33–34 UTC**. Plot 581 advanced naturally to 586, the
victory barks ran, and plot reached 587. The actual public de Lancie states 77–83
and Bence states 64–65 advanced it to 590. The playable celebration was saved as
`904VictoryBase`, then reloaded through the native UI before talking to Dazzo.
This completes **R1 and R6**.

The recorded carrier actions at **16:15:58 UTC** moved the bank, played `INTRO15F`,
and requested the normal SoA campaign transition. AR0602 appeared at **16:18:50**;
the native Imoen opening finished with control restored at **16:39:26**. The live
query then confirmed plot 700, `CSR_ENDING_USED=1`, `CSR_ENDING_FAILED=0`, cutscene
mode false, and AR0602. A post-run save was captured. The recorded party route
contains no BD6100 visit.

The [before/after comparison](C:/Games/csr290-test-20260905/evidence/R1-comparison.json)
passed **13/13 checks**. Markers `M290P001` through `M290P006` and `BAG06_` each
reached AR0602 exactly once through its normal hidden EET import container, with
no marker remaining in the serialized BD4300 source or BD6100 intermediate bank.
The saved finite `BAG06_` store retained all **45 rows and stock total 528** exactly.
This proves the tested items' bank retention under standard EET import behavior;
it does not prove that all gear is freely lootable. The saved bag-store comparison
also does not independently establish the carried item's store association.

## Completed source and installed-state evidence

All **33 repository tests actually passed across two runs**: discovery ran 27
successfully and skipped six without `WEIDU_EXE`; those six container fixtures were
then rerun with the executable configured and all passed. The verifier's 14
contract fixtures are a separate suite.

| Check | Result |
|---|---|
| Component 291 actual WeiDU fixtures | **11/11 PASS**: legacy repair, corrected byte-exact no-op, drift rejection, misplaced guard rejection, protected resources |
| Container-name collision fixtures using actual WeiDU | **6/6 PASS**: case/space aliases cannot evade conflict or duplicate checks |
| Verifier contract fixtures | **14/14 PASS** |
| Repaired isolated EET installed-state verifier | **43 PASS, 0 FAIL** |
| Repaired designated dev EET installed-state verifier | **43 PASS, 0 FAIL** |
| Independent preservation audit | **13/13 PASS**: only the intended endpoint/guard changes; all 74 carrier-tail blocks and 601 unrelated dialogue states preserved |
| Isolated EET WeiDU history | Prior log is an exact text prefix; component 291 is the sole appended row |

The isolated repair installed successfully under the existing `v0.6.4` package
marker; no package-version decision is implied. Its WeiDU mappings contain only
`BDDAZZO.DLG` and private `CSRETBGT.BCS`.

The same repair was then tail-installed on the designated dev EET copy. Its old
WeiDU log remains an exact prefix, with only component 291 appended. Both changed
resources are byte-identical to the isolated runtime-tested versions. No earlier
component was uninstalled or reinstalled. See the [dev install log](C:/Games/csr290-test-20260905/evidence/dev-install-291.log),
[43-check verifier result](C:/Games/csr290-test-20260905/evidence/dev-verifier-after-291.txt),
and [history/resource comparison](C:/Games/csr290-test-20260905/evidence/dev-291-preservation.json).

Local evidence:

- [Install log](C:/Games/csr290-test-20260905/evidence/install-291.log) and [pre-repair WeiDU log](C:/Games/csr290-test-20260905/evidence/eet-before-291.log).
- [Archived isolated WeiDU log](C:/Games/csr290-test-20260905/evidence/isolated-eet-after-291.log).
- [Installed-state verifier output](C:/Games/csr290-test-20260905/evidence/csr291-verifier-scratch-20260906.txt).
- [Repository test discovery](C:/Games/csr290-test-20260905/evidence/source-suite.log) and [explicit six-test WeiDU rerun](C:/Games/csr290-test-20260905/evidence/container-suite.log).
- [Preservation audit manifest](C:/Games/csr290-test-20260905/evidence/291-preservation.json).
- [R0 pre-run save manifest](C:/Games/csr290-test-20260905/evidence/R0-before.json); its raw save copy remains beside it in `evidence/R0-before`.
- [Repaired R0 comparison](C:/Games/csr290-test-20260905/evidence/R0-retest-comparison.json), with raw [before](C:/Games/csr290-test-20260905/evidence/R0-retest-before) and [after](C:/Games/csr290-test-20260905/evidence/R0-retest-after) save copies.
- [Successful EET before-save manifest](C:/Games/csr290-test-20260905/evidence/R1-before.json) and [after-save manifest](C:/Games/csr290-test-20260905/evidence/R1-after.json), with raw [before](C:/Games/csr290-test-20260905/evidence/R1-before) and [after](C:/Games/csr290-test-20260905/evidence/R1-after) save copies.
- [Recorded runtime trace](C:/Games/csr290-test-20260905/evidence/runtime-trace.tsv) and [read-only instrumentation](C:/Games/csr290-test-20260905/evidence/runtime-trace.lua). Save snapshots alone cannot prove transient areas, movie playback, or control recovery; those findings also use the native observations and trace.

## Native acceptance status

| Case | Status | Required evidence |
|---|---|---|
| R0 corrected guard retest | **PASS** | Diagnostic and control recovery observed; 13/13 inventory/party/flag checks passed; native post-guard save reloaded with correct flags and usable Options menu |
| R1 real return/celebration spine | **PASS** | Native 59 → 59A → 59B, victory barks and 586 → 587, actual public de Lancie/Bence conversation, playable celebration |
| Reduced single inventory handoff | **PASS — agreed reduced scope** | Six distinct markers and bag retained exactly in AR0602; 13/13 saved-state checks; native opening completed and control restored |
| R2 original loaded-inventory matrix | **NOT RUN in full** | Equipped, quick-slot, bagged, and near-full variants were not all exercised; the reduced test above does not close this original row |
| R3 solo, empty/full inventory | **NOT RUN** | Both original inventory variants remain untested |
| R4 Imoen and Skie together | **NOT RUN** | Original party variant remains untested |
| R5 mod NPC and dead/unconscious companion | **NOT RUN** | Original party variant remains untested |
| R6 celebration save/reload | **PASS** | Native UI reloaded `904VictoryBase`; Dazzo then completed the SoA handoff |
| R7 multiplayer host/client | **NOT RUN** | Multiplayer synchronization remains untested |
| R8 once/re-entry protection | **NOT RUN** | Once flag verified during one handoff; a second trigger/re-entry was not exercised |
| Standalone native smoke | **PENDING** | Dazzo → credits → menu, repeated after reload |

Successful EET cases must reach AR0602 without a party/current-area visit to
BD6100 and without unexplained item loss or duplication. Storage serialization of
BD6100's destination container is allowed. Static checks do not complete any row
in this runtime table.
