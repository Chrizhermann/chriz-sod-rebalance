# Optional SoD skip: native acceptance and reproduction

Component 910, `20260906-r3`, was accepted by Christopher on 6 September 2026
for release in v0.6.7. The working direct handoff replaces the rejected private
area and ground-loot pickup scanner. Visual transition polish is deferred.
This feature is separate from v0.6.6's component-290 victory ending.

## Verified native result

The six-person BG1 fixture reached the automatic bedroom question. Confirmed
Yes reached EET's normal BG2 opening; Christopher reported that it worked and
authorized release, with awkward scene changes left for later polish.

The read-only observer recorded:

- Skip phase 1 at epoch 1788635380 in BD0103.
- Original EET handoff, phase 6, at 1788635382 in BD6100: about **2 seconds**.
- AR0602 at 1788635403: about **23 seconds total**, including EET's transition.

These are one observed run's wall-clock timings, not a performance guarantee.
The old several-minute scanner is not present.

The resulting **Beverly Hills Skie-Chapter 13 Dungeon** save confirms:

- AR0602, `CSR_SKIP_CHOICE=1`, `CSR_SKIP_PHASE=6`,
  `CSR_SKIP_ITEMS_READY=1`, and `CSR_SKIP_XP=1`; no recorded failure flag.
- Protagonist XP **412,209**: the earlier native bedroom baseline was 162,209,
  giving the requested **+250,000**. BG1's starting fixture had 161,000; the
  normal BG1-to-SoD bootstrap accounts for the intervening 1,209.
- Normal BG2 party state (protagonist plus BG2 Imoen), not the old six-person
  SoD party transplanted into BG2.
- PlayerChest00 empty, BD6100's import bank empty after forwarding, and the
  remaining carried equipment in AR0602's existing hidden import bank.
- EET's import store records the carried markers, including the marker selected
  from BAG06_. That bag's marker count is now zero, while its EET store entry is
  one. Downstream EET selection has already consumed several other entries.
- The deliberately dropped SW1H15 remains in the bedroom ground pile. This is
  the approved exclusion, not a failed import. Fresh Imoen's storage and both
  bookcases remain untouched.

Save SHA-256:

- GAM: `6c92ad1b261d5ff0f6bae4f7102a4c033d33dd0a285fe1c599a229355363837d`
- SAV: `b6366de9c68f75ef7446067fdff5fbe5277cf8a2fbdc352644248a7e388631f4`

This verifies the saved result, not a separate reload of that BG2 save or every
downstream item location. No such broader runtime pass is claimed.

## Repeat the focused test

1. With other game sessions closed, double-click
   `C:\Users\chris\Games\CEBG-SOD-ground-probe-20260905\Launch CSR910 Test.cmd`.
   It launches only this isolated, copy-local offline game and refuses a second
   game or a stale remote-console request.
2. Choose **Load Game**, not Continue, and load **CSR910 BEFORE SKIP**.
   A fixture-only hook starts the original BG1-to-SoD bootstrap automatically.
   Skip opening movies if desired, then wait for the bedroom question.
3. Choose **Yes**, then confirm **Yes**. Expect the normal BG2 opening. There is
   no ground-item scan to wait through. Report a stuck sequence or error message.
4. Once control returns, check XP, save under a new name, and reload to check
   the once-only guard. Do not overwrite the starting fixture.
5. For No coverage, reload the starting fixture. Both confirmation declines
   should return to the question; confirming play-SoD should leave normal control,
   allow the original backpack impound, and award no skip XP.

Game: `C:\Users\chris\Games\CEBG-SOD-ground-probe-20260905\game`.
Profile: `C:\Users\chris\OneDrive\Documents\CEBG SoD Ground Probe Offline 20260905`.
Starting fixture: `save\000000911-CSR910 BEFORE SKIP`.
Do not use an old already-impounded bedroom save to test this arrival hook.

## Automated and remaining coverage

The pre-integration feature worktree passed **34 tests** on Windows with Python
3.11 and WeiDU 249. Public component compilation/decompilation uses synthetic
EET fixtures and checks prerequisites, rejected effective rules/layouts, the exact
three-new/three-modified resource set, protected-resource identity, confirmation
loops, XP/failure guards, delayed impound, and imported-Imoen receipt ordering.
The release notes record the final integrated suite results.

Earlier candidate native evidence covers both confirmation declines, confirmed
No, helper cleanup, no skip XP, and No save/reload. The current candidate changes
the No impound gate, so that earlier result is not a complete retest of r3.

Follow-up coverage: imported off-party Imoen including bags; final No impound
and servant/rest/council continuation; a protagonist award crossing 500,000 XP;
explicit BG2 reload/re-entry; broader party and multiplayer variants. Synthetic
tests do not prove native scheduling or persistence for those cases. Component
910 is EET-only; standalone is deliberately rejected.

## Evidence and harness boundaries

External evidence: `C:\Users\chris\Games\CEBG-SOD-ground-probe-20260905\evidence`.
The immutable `skip-bg1-fixture`, earlier `skip-no` save/report, and test-only
`skip-trace.tsv` are retained. The trace also contains old rejected runs; use
the timestamps above to identify the accepted r3 run.

Current disposable tail: `game\csr910-direct2\setup-csr910-direct2.tp2`, component
0, version `20260906-r3`; log `skip910-direct2.log`. It restores recorded hook
preimages, removes obsolete candidate-owned resources, and installs the verified
current component. An earlier r2 staging copy mistakenly used old source; it was
superseded before any game launch. No WeiDU entry was uninstalled or hand-edited.

Protected K#TELBGT.BCS, AR0602.BCS, CAMPAIGN.2DA, and STARTARE.2DA hashes remain
unchanged. Production adds no EEex dependency; EEex is only an external observer
in this clone. No live/stream install or save was modified.

The read-only save inspector is
`research/prototypes/optional-sod-skip/inspect_skip_save.py`; pass it the full
result-save directory. It reads the save and prints JSON without changing it.

Remote-console acknowledgements mean queued work, not completed actions. Do not
leave a timed-out request for startup: object lookups on the start menu can crash
the game. The observer avoids requests while the action bar is hidden. The UI
capture failure in this session meant Christopher operated the game; native
evidence comes from his report, the observer, and saved-state inspection.
