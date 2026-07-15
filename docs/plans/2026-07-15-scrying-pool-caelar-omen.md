# Single Caelar Omen Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:executing-plans to execute this plan task-by-task.

**Goal:** Replace the dig-site scrying pool's Imoen/Caelar/Hooded-Man picker and all vision
cutscenes with one non-modal, abstract Caelar omen that requires and consumes all three Silver
Scepters and both Essences of Clarity, pays the combined XP of the two visions that formerly
survived after component 120 and before component 225, and then
leaves the pool permanently dormant.

**Architecture:** Add tail component 225 in the Coast Way group, requiring components 120 and
220. Preserve the existing three-scepter insertion and 3,000 party-total completion award.
Extend the real pool object script at top priority with an exhaustive two-Essence/done state
machine, neutralize its vanilla dialog launcher, and False-gate every vanilla picker reply in
`BDSCRY.DLG` without replacing the dialog. Rehome the Essence carried by comp220's removed
`BDWIGHDD` into the closest safe existing container. Retired cutscene resources remain on disk
as harmless dead code for compatibility.

**Tech Stack:** WeiDU v24600 (`.tp2`, `.tpa`, `.baf`, `.d`, `.tra`), Infinity Engine ARE/BCS/
DLG formats, Python 3 standard-library verification, PowerShell, Git.

---

### Task 1: Add a failing semantic verifier

**Files:**

- Create: `research/scripts/verify_scrying_pool.py`

**Step 1: Write the verifier before component code**

Implement a standard-library script accepting `--game-dir`. It must:

- parse `override/BD1200.ARE` container and actor records;
- invoke that install's `weidu.exe` in a temporary directory to decompile `BDODSCRY.BCS`
  and `BDSCRY.DLG`;
- verify three reachable container-held `BDMISC55` items;
- verify exactly two reachable container-held `BDMISC59` items;
- verify `Sarcophagus01` at `(2414,1736)` contains its original `BDMISC55` plus one
  `BDMISC59`;
- verify `BDWIGHDD` at `(2474,1951)` remains schedule-zero;
- verify the active pool script has one two-Essence trigger/consumption path, a once-flag set
  before consumption and XP, six 1,000-XP slot awards, and no active BDSCRY/cutscene/travel/
  creature-spawn/CUTSKIP path;
- verify BDSCRY states 0 and 4 have their Imoen, Caelar, and Hooded-Man replies False-gated;
- verify `BDSCEPT1/2/3` are absent from BD1200's live resource references.

The script should print individual PASS/FAIL lines and exit nonzero if any assertion fails.

**Step 2: Run against the current v0.6.2 dev install and observe the intended failure**

Run:

```powershell
python research/scripts/verify_scrying_pool.py --game-dir "C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install"
```

Expected: FAIL because only one reachable Essence exists, the active pool still launches
`BDSCRY`, there is no two-vial once-path, and Imoen/Caelar replies remain reachable.

**Step 3: Commit the red test**

```powershell
git add research/scripts/verify_scrying_pool.py
git commit -m "Test the single-omen scrying-pool contract"
```

### Task 2: Implement component 225 test-first

**Files:**

- Create: `chriz-sod-remix/lib/comp225.tpa`
- Create: `chriz-sod-remix/baf/csr225om.baf`
- Create: `chriz-sod-remix/languages/english/csr225om.tra`
- Create: `chriz-sod-remix/dlg/csr225scry.d`
- Modify: `chriz-sod-remix/setup-chriz-sod-remix.tp2`
- Modify: `chriz-sod-remix/languages/english/setup.tra`

**Step 1: Wire the new component**

- Bump the package version from `v0.6.2` to `v0.6.3`.
- Add component 225 after component 220 in source order, in group `@1002`, label
  `csr_scrying_pool_omen`.
- Require components 120 and 220 and predicate-check `bd1200.are`, `bdodscry.bcs`, and
  `bdscry.dlg`.
- Include `lib/comp225.tpa` and add setup translation `@225`.

**Step 2: Add the non-modal object-script state machine**

In `csr225om.baf`, add mutually exclusive `EXTEND_TOP` blocks for clicks after
`BD_SDDD12_COUNTER=3`:

1. `CSR_SCRY_DONE=1`: show only a short dormant-pool description.
2. `CSR_SCRY_DONE=0` and fewer than two `BDMISC59`: explain that two Essences are required;
   consume nothing.
3. `CSR_SCRY_DONE=0` and at least two `BDMISC59`: set the done flag first, set
   `BD_SDDD12_CLOUDY` to terminal value 2, consume exactly two with
   `TakePartyItemNum("BDMISC59",2)`, play only the existing pool splash/ambient changes,
   display the approved omen with `DisplayStringNoNameHead`, return the pool to its murky
   ambient state, and grant `AddXPObject(Player1..6,1000)` exactly once.

The response must contain no dialog launch, cutscene mode, area travel, creature creation,
party relocation, or CUTSKIP action. The matching `csr225om.tra` must contain the approved
omen text and the two concise interaction descriptions because BAF AUTO_TRA lookup is by
matching basename.

**Step 3: Neutralize every old live route without replacing third-party surfaces**

In `comp225.tpa`:

- count-guard the single vanilla
  `ActionOverride("BDSCRY",StartDialogNoSet(LastTrigger))` in `BDODSCRY.BCS`, then replace it
  with `NoAction()`;
- `EXTEND_TOP` the patched script with `csr225om.baf`;
- compile `csr225scry.d`, which adds `False()` to transitions 0 and 1 in BDSCRY states 0 and
  4. Component 120 already False-gates transition 2; do not delete or wholesale-replace
  `BDSCRY.DLG`, so Aura's state-0 interjection remains structurally valid but dormant.

**Step 4: Rehome the missing Essence without reviving the removed wight**

Patch `BD1200.ARE` with loud guards:

- find exactly one `Sarcophagus01` at `(2414,1736)`;
- require the current area to contain exactly three `BDMISC55`, exactly one container-held
  `BDMISC59`, and no Essence in the target;
- require `BDWIGHDD` at `(2474,1951)` to remain schedule-zero;
- relocate the full shared item array to EOF, copy the target's existing 20-byte scepter
  record unchanged, append one zero-charge/zero-flag `BDMISC59` record, and repoint only the
  target container's item run plus the ARE item header.

Do not edit `comp220_lists.tpa` and do not restore `BDWIGHDD`.

**Step 5: Compile-check component 225 in an isolated disposable game copy if needed**

Use WeiDU's normal install path for definitive compilation; do not touch the live or clean
installs.

**Step 6: Commit the implementation**

```powershell
git add chriz-sod-remix
git commit -m "Replace the scrying visions with one Caelar omen"
```

### Task 3: Integrate research and decision documentation

**Files:**

- Create: `docs/research/20-scrying-pool.md`
- Modify: `docs/01-remix-wishlist.md`
- Modify: `docs/design/chapters/02-coastway.md`
- Modify: `docs/00-feature-inventory.md`
- Modify: `docs/playtest/2026-07-11-stream-playtest.md`
- Modify: `docs/plans/2026-07-15-scrying-pool-caelar-omen-design.md`

**Step 1: Integrate, do not merge, PR #9's research**

Port the factual research from commit `7e7d214` to `docs/research/20-scrying-pool.md` because
master already owns `19-xp-recount.md`. Correct the flow detail: the initial
`BD_SDDD12_CLOUDY=0` makes the first old vision free; the two Essences gate visions two and
three. Mark the decision as locked and point to the approved design and component 225.

**Step 2: Update all living design/status surfaces**

- Add the user's locked one-omen/all-items/no-cutscene decision to the wishlist.
- Add component 225 to the Coast Way chapter design and feature inventory.
- Update inventory metadata to v0.6.3, 31 declarations, and 30 selected components on dev
  only after installation succeeds.
- Mark PT-6 built/install-verified while keeping runtime playthrough checks explicitly pending.
- Change the approved design status only after all automated/dev-install checks pass.

**Step 3: Commit documentation separately**

```powershell
git add docs
git commit -m "Record the single-omen scrying-pool decision"
```

### Task 4: Install and verify on the dev EET target only

**Files:**

- Read: `C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install\WeiDU.log`
- Modify via installer: dev EET install only

**Step 1: Verify no process is using the dev target**

Inspect executable paths for `Baldur`, `InfinityLoader`, `EEex`, and WeiDU-related processes.
Do not terminate the unrelated running game-copy process. Stop only a process whose executable
path is inside the dev EET target, if one exists.

**Step 2: Copy the mod tree conservatively**

From the repository root, copy `chriz-sod-remix` into the dev game with `robocopy /E` and no
`/MIR` or destructive deletion option. Verify the TP2 hash after copying.

**Step 3: Tail-install only component 225**

From the dev game directory:

```powershell
& .\weidu.exe chriz-sod-remix/setup-chriz-sod-remix.tp2 `
  --force-install-list 225 `
  --language 0 --use-lang en_US --no-exit-pause
```

**Execution record:** the command above was used once to append component 225 at the tail.
Do not uninstall or reinstall components 120, 220, 225, or any other existing WeiDU.log
entry. Any future correction to this feature must ship as a new tail component and verify
against the current installed state.

**Step 4: Run semantic verification**

```powershell
python research/scripts/verify_scrying_pool.py --game-dir "C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install"
```

Expected: all checks PASS, including two reachable Essences, schedule-zero wight, two-vial
one-shot path, six 1,000-XP awards, sealed picker replies, and zero active cinematic route.

**Step 5: Inspect installer evidence**

- Confirm WeiDU.log ends with component 225 at v0.6.3.
- Confirm no earlier log entry moved.
- Decompile installed resources independently and inspect the omen action ordering.
- Confirm repository and copied mod TP2 hashes match.

Runtime verification is intentionally deferred until the next SoD playthrough (using a save
from before first entering BD1200): 0/1/2 Essence feedback, exact inventory and XP deltas,
repeat-click safety, save/reload persistence, Imoen present in party, responsive controls, and
no cinematic transition.

### Task 5: Review and hand off

**Files:** all changed files

**Step 1: Run source and install verification again from a clean shell**

Review `git diff`, run the semantic verifier, and ensure `AGENTS.md` remains untracked and
unstaged.

**Step 2: Request independent code review**

Have a fresh reviewer inspect behavior, WeiDU/ARE safety, compatibility, XP/item economy, and
documentation consistency. Fix any substantiated findings and rerun verification.

**Step 3: Commit final verification/doc corrections if needed**

Use narrow commits and never stage `AGENTS.md`.

**Step 4: Leave external publication explicit**

Report that PR #9 should be closed as incorporated and issue #6 should be closed by the future
publication PR. Do not merge/close/push external state unless the user asks for publication.
