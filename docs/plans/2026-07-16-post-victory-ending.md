# Post-Victory Ending Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:executing-plans to execute this plan task-by-task.

**Goal:** Replace SoD's post-victory murder/arrest/epilogue with a short playable BD4300
celebration and a Dazzo-triggered ending that enters SoA directly on EET or ends at credits on
standalone BG:EE+SoD, with no party visit to the BD6100 ambush and no gear loss.

**Architecture:** Add tail component 290 in a new Ending group, requiring the already shipped
Hooded-Man/dream/Entar removals (120, 130, 185). Patch only the live celebration and retired-band
entry points. On EET, add a local import container to BD4300, clone the currently installed
`K#TELBGT.BCS/.CRE`, guard the clone, and move its local bank to the existing area-qualified
BD6100 bank before the clone's normal campaign transition. On standalone, terminate natively
from Dazzo. Preserve BDCUT59/59A/59B, CUTSKIP response 59, all original K#/AR0602/BD6100
resources, and unrelated BD0104 content.

**Tech Stack:** WeiDU v24600 (`.tp2`, `.tpa`, `.baf`, `.d`, `.tra`), Infinity Engine
ARE/BCS/CRE/DLG formats, Python 3 standard library, PowerShell, Git, EET/EEex runtime console.

---

### Task 1: Add the failing installed-state verifier

**Files:**

- Create: `research/scripts/verify_ending.py`

**Step 1: Implement the verifier before component code**

Model it on `research/scripts/verify_scrying_pool.py`. Accept:

```text
--game-dir PATH
--platform auto|eet|standalone
--baseline-manifest optional.json
```

Use only the standard library. Parse ARE container records directly; invoke the target game's
`weidu.exe` in a temporary directory to decompile scripts/dialogs. Print one PASS/FAIL line per
assertion and exit nonzero on any failure.

Before freezing assertions, exhaustively scan the repo corpus and installed BCS/DLG resources
for `bd_plot=590`, `BDCUT60*`, `BDCUT61*`, `bd_debug_move_to_dream/cell`, the Romance6 globals,
and every inbound reference to the identified coda states. Record a preserved/retired
classification in the verifier so an unaccounted live root is a failure, not an assumption.

The verifier must assert:

- platform detection: all of `K#TELBGT.BCS`, `K#TELBGT.CRE`, and `AR0602.BCS` means EET;
  none means standalone; a partial signature is an error;
- BDCUT59/59A/59B and CUTSKIP are unchanged from the optional pre-install SHA-256 manifest;
- all 18 BD4300 victory-bark timers use `2`, while the final 586→587 convergence survives;
- both Corwin and both Neera finale blocks are false-gated, with neither Romance6 global faked;
- BDDELANC 77–83 retain the public chain and journal 266908, while 95/104 are false-gated;
- BDBENCE 64–65 survive, 65 exits without state 66, and all murder/arrest launch states are
  unreachable;
- BDDAZZO state 0 requires plot 590 and the once flag; states 2/3 have no `bdcut60`, share the
  correct platform endpoint, and erase journal 266908;
- BDRUMOR3 7/20/37, both BDDEBUG dream/cell launchers, and the final BDPALACE Entar block are
  false-gated; unrelated rumor/debug/palace content remains;
- no reachable production path launches BDCUT60/60B/61 or the private Waterdeep coda;
- EET only: BD4300 contains exactly one empty `K#ImportContainer`; the cloned BCS preserves the
  installed K# blocks and six Player-slot `TakeCreatureItems` actions, has a fail-closed local-
  container guard, and adds exactly one BD4300→BD6100 `MoveContainerContents` before the normal
  movie/campaign move; the cloned CRE points to it;
- EET only: original K#TELBGT BCS/CRE, AR0602, BD6100 BCS/ARE, and early BD0104 match the
  manifest; AR0602 still contains exactly the BD6100→AR0602 import move;
- standalone only: no K# dependency exists in the endpoint; the action order is
  `EndCutSceneMode()`, `ContinueGame(FALSE)`, `EndCredits()`; native BD6100 remains unchanged.

When comparing clone/original CREs, whitelist only the chosen script-resref field and, if used,
the death-variable field. When comparing clone/original BCSs, normalize only the prepended guard
and the one intentional cross-area move; every installed third-party block/action must remain.

**Step 2: Run against the current unpatched EET dev install**

```powershell
$repo = 'C:\src\private\chriz-sod-rebalance'
$eet = 'C:\Games\Baldur''s Gate II Enhanced Edition modded - dev eet install'
python "$repo\research\scripts\verify_ending.py" --game-dir $eet --platform eet
```

Expected: FAIL for the missing BD4300 import container/clone, live romance finales, Dazzo's
BDCUT60 actions, live coda/murder roots, old timers, rumors, debug launchers, and Entar residue.

**Step 3: Commit the red verifier**

```powershell
git add research/scripts/verify_ending.py
git commit -m "Test the direct post-victory ending contract"
```

### Task 2: Implement component 290 for both platforms

**Files:**

- Create: `chriz-sod-remix/lib/comp290.tpa`
- Create: `chriz-sod-remix/dlg/csr290common.d`
- Create: `chriz-sod-remix/dlg/csr290eet.d`
- Create: `chriz-sod-remix/dlg/csr290sod.d`
- Create: `chriz-sod-remix/baf/csr290guard.baf`
- Create: `chriz-sod-remix/languages/english/csr290guard.tra`
- Modify: `chriz-sod-remix/setup-chriz-sod-remix.tp2`
- Modify: `chriz-sod-remix/languages/english/setup.tra`

**Step 1: Wire a separately grouped tail component**

- Bump the package from v0.6.3 to v0.6.4.
- Change the TP2 range comment to `260–289` coalition and `290–299` ending.
- Add `@290` and new group `@1005` (Ending and campaign handoff).
- Declare component 290 with predicates for BD4300, BDPALACE, BDDEBUG, BDDAZZO, BDBENCE,
  BDDELANC, and BDRUMOR3.
- Require components 120, 130, and 185. Do not require 160/197: Imoen/Skie party presence is
  supported but the ending cleanup remains independently useful.
- Include `lib/comp290.tpa`.

**Step 2: Preflight platform and patch anchors before loading new text**

In `comp290.tpa`, classify by the three EET-only anchors (`K#TELBGT.BCS`, `K#TELBGT.CRE`,
`AR0602.BCS`): exactly 0 = standalone, exactly 3 = EET, 1–2 = `PATCH_FAIL`. On EET also require
BD6100.ARE with exactly one empty `K#ImportContainer`; on standalone require native BD6100.BCS
with its verified two terminal action triples. Reject drift before compiling the guard TRA.

Count-guard every subsequent anchor. Never choose standalone merely because one EET file is
missing.

**Step 3: Compress and clean the live BD4300 celebration**

Patch the installed BD4300.BCS in place:

- require exactly 18 `bd_mdd1341a_ot_timer` actions in the plot-586 victory-bark chain and
  normalize their values to numeric `2`;
- false-gate the Romance6=0 setter and Romance6=1 forced-dialog block for both Corwin and Neera;
- do not write `bd_CorwinRomance6`, `bd_NeeraRomance6`, or either romance-active global;
- preserve the convergence that advances plot 586→587 and all unrelated BD4300 blocks.

**Step 4: Compile the common dialogue cleanup**

In `csr290common.d`:

- preserve BDDELANC 77–83; false-gate roots 95 and 104;
- preserve BDBENCE 64–65; replace transition 65.0 with soldier-ambience restoration,
  `EscapeArea()`, and `EXIT`;
- false-gate BDBENCE states 6, 9, 10, 67, 68, 70, 71, and 73 so murder/arrest cutscenes cannot
  be resurrected through a direct entry;
- add `Global("bd_plot","GLOBAL",590)` and a zero-valued component once flag to BDDAZZO state 0;
- false-gate BDRUMOR3 states 7, 20, and 37.

Patch BDDEBUG's `bd_debug_move_to_dream` and `bd_debug_move_to_cell` blocks plus their dialogue
setters so no debug route launches BDCUT60/61. False-gate the exact BDPALACE Range/FaceObject
block for BDENTAR. Do not modify BD0104 or delete BDENTAR resources.

**Step 5: Build the EET branch from installed resources**

Only in the complete EET branch:

1. Preflight BD4300 for zero containers named `K#ImportContainer`.
2. Add exactly one invisible, empty type-8 container with the verified EET geometry: location
   `(88,76)`, bounding box `(72,26)-(120,58)`, trap location `(80,70)`, four vertices, script
   name `K#ImportContainer`. Use WeiDU's ARE-structure helper or an equivalently guarded local
   implementation; do not depend on another mod's source file at install time.
3. `COPY_EXISTING` installed `K#TELBGT.BCS` to unused eight-character `CSRETBGT.BCS`.
4. Prepend `csr290guard.baf`. If the local container is absent, it must display `@29000`, fade
   back in, end cutscene mode, mark the attempt failed, destroy the carrier, and stop before any
   named-item sweep or `TakeCreatureItems` action.
5. Count exactly one `StartMovie("INTRO15F")` and one `MoveToCampaign("SoA")`; insert exactly
   `MoveContainerContents("BD4300*K#ImportContainer","BD6100*K#ImportContainer")` immediately
   before the movie in the clone only.
6. Clone installed `K#TELBGT.CRE` to `CSRETBGT.CRE`; change only its override script (CRE 0x248)
   and, if needed for unique object identity, death variable (0x280) to `CSRETBGT`.
7. In `csr290eet.d`, replace both BDDAZZO state-2/3 transitions with the same once-first action:
   set the once flag, erase journal 266908, enter cutscene mode, fade black, and
   `CreateCreatureObject("CSRETBGT",Player1,0,0,0)`.

Never modify original K#TELBGT, AR0602, BD6100, campaign tables, or `ENDOFBG1`.

**Step 6: Build the standalone branch**

Only when all three EET-only anchors are absent, compile `csr290sod.d`. Replace both Dazzo
terminals with the same once-first action: set the flag, erase journal 266908, enter cutscene
mode, fade black, then run `EndCutSceneMode()`, `ContinueGame(FALSE)`, `EndCredits()` in that
order. Do not create, copy, or refer to K# resources.

**Step 7: Run source checks and commit**

```powershell
git diff --check
rg -n 'BDCUT60|BDCUT61|K#TELBGT|CSRETBGT|K#ImportContainer|NeeraRomance6|CorwinRomance6' chriz-sod-remix
git add chriz-sod-remix
git commit -m "End SoD at the Dragonspear victory celebration"
```

### Task 3: Prove the EET install on a disposable full copy

**Files:** component files and verifier as fixes require; no live/dev mutation yet

**Step 1: Create a fresh scratch clone**

Clone the dev EET game to a clearly named disposable path, preserving the source untouched. Use
one PowerShell process end-to-end; verify the resolved source/destination paths before any later
recursive cleanup. Copy with `robocopy /E`, never `/MIR`.

```powershell
$repo = 'C:\src\private\chriz-sod-rebalance'
$eetSource = 'C:\Games\Baldur''s Gate II Enhanced Edition modded - dev eet install'
$eetScratch = 'C:\Games\Baldur''s Gate II Enhanced Edition modded - ending scratch'
robocopy $eetSource $eetScratch /E /R:1 /W:1
robocopy "$repo\chriz-sod-remix" "$eetScratch\chriz-sod-remix" /E /R:1 /W:1
```

Do not reuse a scratch copy after an installation failure or component-code change; restore a
fresh clone so append-only WeiDU state is representative.

**Step 2: Capture immutable-resource and WeiDU baselines**

Write a JSON SHA-256 manifest for original K#TELBGT.BCS/CRE, AR0602.BCS, BD6100.BCS/ARE,
BDCUT59/59A/59B, CUTSKIP, and BD0104. Copy WeiDU.log separately.

**Step 3: Tail-install component 290 and run the verifier**

```powershell
Push-Location $eetScratch
& .\weidu.exe chriz-sod-remix/setup-chriz-sod-remix.tp2 `
  --force-install-list 290 --language 0 --use-lang en_US --no-exit-pause
if ($LASTEXITCODE) { throw "scratch ending install failed: $LASTEXITCODE" }
Pop-Location
python "$repo\research\scripts\verify_ending.py" `
  --game-dir $eetScratch --platform eet --baseline-manifest "$env:TEMP\csr-ending-eet.json"
```

Expected: every semantic/hash check PASS; the old WeiDU.log is an exact prefix and component 290
is the single new final row.

**Step 4: Exercise loud-failure cases on separate fresh scratch copies**

- remove exactly one EET signature resource: install fails as partial EET, with no component-290
  log row;
- mutate one Dazzo/Bence/de Lancie/BD4300 anchor: count guard fails without a partial install;
- remove or duplicate the BD6100 destination container: preflight fails;
- pre-add a conflicting BD4300 import container: preflight fails;
- verify DEBUG contains the intended `PATCH_FAIL`, not an unrelated compile error.

**Step 5: Fix until a fresh positive copy and every negative copy behave correctly**

Every correction is repository code followed by a new scratch clone. Do not install component
290 on the real dev EET target yet.

**Step 6: Commit hardening fixes**

```powershell
git add research/scripts/verify_ending.py chriz-sod-remix
git commit -m "Harden the direct ending handoff against resource drift"
```

### Task 4: Prove the standalone install on a disposable merged-SoD copy

**Files:** component/verifier fixes only

**Step 1: Clone the real merged standalone install**

Use `C:\Games\Baldur's Gate Enhanced Edition modded` as a read-only source and create a new
disposable ending-smoke copy. Do not install into the source or the clean unmerged BG1 dev copy.

Deploy the mod tree, then install component 290's declared prerequisite chain first on this fresh
copy: 120, 130, 140, 150, and 185 (140/150 are required by 185). Confirm those installs before
capturing the component-290 baseline. Do not weaken `REQUIRE_COMPONENT` merely to make a
standalone test copy easier to prepare.

**Step 2: Capture the standalone baseline**

Hash native BD6100.BCS/ARE, BDCUT59/59A/59B, CUTSKIP, and BD0104. Confirm native BD6100 has two
`EndCutSceneMode`→`ContinueGame(FALSE)`→`EndCredits()` terminal paths and zero K#/MoveToCampaign.
Copy WeiDU.log **after** the prerequisite chain; that copy must be an exact prefix after 290.

**Step 3: Tail-install 290 and run static verification**

```powershell
Push-Location $standScratch
& .\weidu.exe chriz-sod-remix/setup-chriz-sod-remix.tp2 `
  --force-install-list 120 130 140 150 185 `
  --language 0 --use-lang en_US --no-exit-pause
if ($LASTEXITCODE) { throw "standalone prerequisite install failed: $LASTEXITCODE" }
# Capture the component-290 resource/hash and WeiDU baselines here.
& .\weidu.exe chriz-sod-remix/setup-chriz-sod-remix.tp2 `
  --force-install-list 290 --language 0 --use-lang en_US --no-exit-pause
if ($LASTEXITCODE) { throw "standalone ending install failed: $LASTEXITCODE" }
Pop-Location
python "$repo\research\scripts\verify_ending.py" `
  --game-dir $standScratch --platform standalone `
  --baseline-manifest "$env:TEMP\csr-ending-standalone.json"
```

Expected: PASS; no CSRETBGT/K# dependency, native BD6100 unchanged, common celebration cleanup
present, and both Dazzo routes carry the native terminal order.

**Step 4: Test partial-signature rejection separately**

On a different fresh standalone scratch copy, introduce only one EET-only signature file. The
install must fail loudly as partial EET rather than choosing standalone.

**Step 5: Commit any platform fixes**

```powershell
git add research/scripts/verify_ending.py chriz-sod-remix
git commit -m "Verify the native standalone ending branch"
```

### Task 5: Review, then install exactly once on the real dev EET target

**Files:** all implementation/test files

**Step 1: Request an independent code review**

Review WeiDU count guards, DLG state/transition indices, ARE structure safety, clone fidelity,
runtime guard ordering, platform classification, romance continuity, and original-resource hash
coverage. Resolve every substantiated blocker on new scratch copies first.

**Step 2: Confirm the real dev target is idle**

Inspect `Baldur`, `InfinityLoader`, EEex, and WeiDU process executable paths. Stop only a process
whose executable lives inside the dev EET target; do not touch another game copy.

**Step 3: Capture final pre-install evidence**

- SHA-256 JSON manifest of immutable resources;
- full WeiDU.log copy;
- dialog.tlk UTC mtime;
- repository/game-copy TP2 hashes.

**Step 4: Deploy conservatively and tail-install only 290**

```powershell
$eet = 'C:\Games\Baldur''s Gate II Enhanced Edition modded - dev eet install'
robocopy "$repo\chriz-sod-remix" "$eet\chriz-sod-remix" /E /R:1 /W:1
Push-Location $eet
& .\weidu.exe chriz-sod-remix/setup-chriz-sod-remix.tp2 `
  --force-install-list 290 --language 0 --use-lang en_US --no-exit-pause
if ($LASTEXITCODE) { throw "dev ending install failed: $LASTEXITCODE" }
Pop-Location
```

This command is run once after scratch approval. Never uninstall/reinstall 290; a later defect is
a new tail component.

**Step 5: Verify the installed state**

- run `verify_ending.py` with the real pre-install manifest;
- prove all old WeiDU.log lines are unchanged and 290 is the sole new last row;
- scan DEBUG for `FATAL|ERROR|NOT INSTALLED|Permission denied|Invalid`;
- prove every immutable-resource hash is unchanged;
- independently decompile the clone, original K# script, AR0602, and endpoint dialogs.

Expected: all PASS before runtime testing.

### Task 6: Run the EET runtime matrix

**Files:**

- Create: `docs/playtest/2026-07-16-post-victory-ending.md`

**Step 1: Verify the missing-container guard first**

Copy save `000000435-safety safe` (BD4300 already baked). Give Player1 a unique marker item and
use Dazzo. Expected: visible diagnostic before any item sweep, fade returns, cutscene mode ends,
all gear remains, the campaign does not move, and the save remains usable after reload.

**Step 2: Stage the primary happy path from an unvisited-area save**

Prefer a genuine save from immediately before BDCUT59 and run BDCUT59→59A→59B normally. If none
exists, create one through the game's debug/console flow from a copy of
`000000018-Kool Koveras-Chapter 10 Start`; its BALDUR.SAV has no BD4300. A first-load shortcut
may move to BD4300 at plot 586 and invoke BDCUT59B to stage that area, but it does **not** count
as the full-spine smoke: BDCUT59/59A must still receive either an in-engine run from their real
source area or explicit separate coverage. Never set plot 590 directly for the primary case.

After BDCUT59B, let the preserved 586→587 timer chain finish, click de Lancie, and follow her
public dialogue into Bence so the game reaches plot 590 through the real conversation.

Confirm:

- all party barks play in roughly two-second cadence;
- public de Lancie and Bence 64–65 play, Bence exits, free control returns;
- the player can talk, loot, save, and reload before Dazzo;
- no private Waterdeep pitch, Corwin/Neera forced finale, Skie check, or other coda fires.

**Step 3: Run party/inventory cases from fresh copies of the unvisited-area seed**

1. full six-person party with ordinary marker items in every Player slot, equipped/quick-slot
   items, bags, and near-full inventories;
2. solo protagonist with empty and full inventory variants;
3. Imoen + Skie together (verify no Imoen displacement, Skie death, or romance finale);
4. one mod NPC plus one dead/unconscious in-party companion;
5. save/reload during celebration, then Dazzo;
6. multiplayer host/client smoke;
7. once/re-entry protection (no duplicate clone or duplicate import).

For each successful case: Dazzo → black → SoA/AR0602; BD6100 never becomes or appears as the
party/current area and no ambush/movie plays. Save serialization of the BD6100 destination
container is allowed. Compare the eligible ordinary-item marker multiset before Dazzo and after
AR0602; require zero unexplained loss/duplication. Check named-import items against the original
K# store semantics and verify gold/containers behave exactly like the unmodified handoff.

**Step 4: Record evidence**

In the playtest document, record save seed/case, party, marker manifest, pre/post area, result,
screenshots or save-parser evidence, and every observed limitation. Do not mark runtime complete
if any matrix row is missing.

**Step 5: Commit the EET runtime record**

```powershell
git add docs/playtest/2026-07-16-post-victory-ending.md
git commit -m "Record EET runtime verification of the direct ending"
```

### Task 7: Run the first-party standalone runtime smoke

**Files:**

- Modify: `docs/playtest/2026-07-16-post-victory-ending.md`

**Step 1: Use only the disposable merged-SoD copy**

Create or stage a save that has not visited BD4300, reach the preserved return/celebration, and
save once free control returns.

**Step 2: Finish through Dazzo**

Expected sequence: Dazzo → fade black → cutscene mode cleared → credits → main menu. There must
be no BD6100 party visit, ambush, `sodcin05`, K# lookup, inventory mutation before termination,
or softlock.

**Step 3: Repeat from the saved celebration once**

Confirm deterministic termination after reload and that Dazzo is unavailable before plot 590.

**Step 4: Record and commit the smoke result**

```powershell
git add docs/playtest/2026-07-16-post-victory-ending.md
git commit -m "Record standalone runtime verification of the direct ending"
```

Community/Discord/stream tests may be appended later, but do not substitute for this smoke.

### Task 8: Update shipped status and documentation

**Files:**

- Modify: `chriz-sod-remix/README.md`
- Modify: `docs/00-feature-inventory.md`
- Modify: `docs/01-remix-wishlist.md`
- Modify: `docs/plans/2026-07-16-post-victory-ending-design.md`
- Modify: `docs/research/14-ending-epilogue-map.md` only if implementation evidence corrects data
- Modify: `docs/plans/2026-07-16-post-victory-ending.md.tasks.json`

**Step 1: Update only verified claims**

- mark component 290 implemented at v0.6.4;
- update declaration/selected counts from 31/30 to 32/31 and install groups from 5 to 6 only
  after the dev install succeeds;
- distinguish static, EET runtime, and standalone runtime status accurately;
- record the actual clone resref, guard behavior, component dependencies, and installed result;
- leave the live non-dev install unchanged;
- leave user-owned untracked `AGENTS.md` unstaged. Its stale local BD6100 wording requires an
  explicit user decision before tracking/editing; tracked CLAUDE.md already points to the
  approved invariant.

**Step 2: Mark task JSON statuses from real evidence**

Do not mark runtime tasks complete from static decompilation alone.

**Step 3: Commit documentation separately**

```powershell
git add chriz-sod-remix/README.md docs
git commit -m "Document the shipped post-victory ending"
```

### Task 9: Final verification and handoff

**Files:** all changed files

**Step 1: Run final verification from a clean shell**

```powershell
git diff --check
python research/scripts/verify_ending.py `
  --game-dir 'C:\Games\Baldur''s Gate II Enhanced Edition modded - dev eet install' `
  --platform eet --baseline-manifest "$env:TEMP\csr-ending-dev.json"
git status --short
```

Rerun the standalone verifier against the disposable smoke copy. Confirm only `AGENTS.md` remains
untracked and no game artifacts, saves, DEBUG files, manifests, credentials, or transcripts are
in Git.

**Step 2: Request a fresh final review**

Review behavior, compatibility, original-resource preservation, test evidence, documentation,
and append-only WeiDU safety. Fix substantiated findings through a new tail component if 290 is
already installed; never rewrite dev WeiDU history.

**Step 3: Commit any final repository-only corrections**

Use narrow commits. Do not stage `AGENTS.md`.

**Step 4: Leave publication explicit**

Report commit hashes, dev/standalone evidence, known limitations, and the unchanged live install.
Do not push, merge, or publish unless the user asks.
