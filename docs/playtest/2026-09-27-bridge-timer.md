# Boareskyr collapse timer — implementation verification

Implemented on `codex/bridge-collapse-timer`, starting from v0.6.11 master.
Fresh component 256 includes the timer; component 258 upgrades an existing 256
without reinstalling any previous row. Optional 257 still changes only the two
Insane mage AI pointers. The user authorized v0.6.12 release after review and
automated checks, deferring native playtesting to the next collection test pass.
No game installation or native acceptance is implied by this record.

## Behavior

- Story Mode: no deadline or timed-collapse warnings. Easy/Normal/Core/Hard/Insane
  use 600/480/420/360/300 game-time seconds. Explicit Legacy of Bhaal detection
  initially selects 300 seconds. A pause freezes simulation time.
- The first update after the existing ready stage displays the opening warning
  and arms all four saved deadlines. Difficulty is sampled once. Story Mode
  enabled later disables the deadline for that encounter permanently, with a
  confirmation message; toggling it off does not silently restart the clock.
- Warnings at 25/50/75 percent appear overhead and once in the log. Native
  AMB_E17A/B rockfall sounds accompany small increasing shakes. Saved warning
  progress prevents repeats; overdue warnings coalesce to the most urgent one.
- Death/petrification/removal of both mages and all four elementals stops the
  countdown before any warning or expiry check, including at the deadline.
  Surviving guards and CombatCounter do not gate this confirmation. The old
  all-eight/combat-clear Bence wrap remains separately guarded by completion.
- Expiry first latches failure and retires the active encounter stage, then
  launches CSR26END once. The short unskippable helper displays the reason,
  plays rocks, waits two seconds, fades for one second, restores cutscene UI
  state and invokes native GameOver with that reason. No damage/kill/explosion
  actions or changes to CUTSKIP are involved.
- Retreat does not restart the saved deadline. The area controller processes
  completion/expiry on returning to BD2000. It does not run a failure scene in
  another area. An old active stage-2 save receives a new full allowance on
  upgrade; a completed stage-3 save is unchanged.

## Compatibility boundary

The removal check intentionally retains existing component256 semantics.
Read-only inspection of current dev SR Banishment found the chain SPWI605 /
SPPR616 → DVBANISH → DESTSELF → opcode168 Remove Creature; requiring ordinary
death would break that counterplay. Native Maze suspension is indistinguishable
from removal to these triggers, so temporarily removing the final remaining
threat can also resolve demolition. This is an inherited encounter limitation,
not a newly verified Maze-safe implementation. Ordinary invisibility does not
make an actor absent from the area.

## Offline verification

- All 25 focused timer tests and 12 public bridge-installer tests passed with
  WeiDU 249. They cover the compiled controller, deadlines/warnings, Story Mode,
  last-second completion, eligible enemies, failure sequencing, companion patch
  order, append-only upgrade, fresh-install no-op and rollback/collision safety.
- The full local regression run passed: 347 main tests, 41 research tests and
  14 ending-contract tests. Three additional effective collection-capture checks
  were skipped because their external fixture was not configured in that run.
  After locating the existing capture, all three passed separately on disposable
  copies: **405 tests passed in total, no checks left unverified by a skip**.
- The public installer and all 62 TPA libraries parsed cleanly with WeiDU 249;
  the source whitespace check passed. Independent source review found no
  actionable defect.

Automated installer checks use disposable synthetic games or isolated copies
of captured resources, never the live installation. Such checks cannot establish
native audiovisual presentation or that an Insane/LoB fight fits the initial budget.

## Remaining native checklist

1. From a pre-fight save in an isolated game copy, check each finale entry route
   reaches the opening warning only after control returns. Check Story Mode has
   the ordinary objective but no timed warnings or collapse.
2. On a timed tier, verify overhead/log readability, rock audibility, shake
   strength and all three warning moments. Pause for a measured interval and
   verify it does not consume the budget; save/reload without resetting it.
3. Kill the two mages/four elementals while a guard survives: immediate safety
   confirmation, no later warning/failure, then normal Bence dialogue after the
   remaining fight. Repeat with a banished eligible elemental and petrification.
4. Let the clock expire: one short collapse sequence, readable custom reason,
   usable normal game-over/reload UI and no original barrel explosion. Reload a
   pre-failure save to confirm ordinary game control and camera/fade restoration.
5. Change ordinary difficulty mid-fight without restarting the budget. Enable
   Story Mode near expiry: deadline disabled, no delayed failure when disabled
   again. Retreat/return without gaining a fresh allowance.
6. Check carried Khalid/Skie configurations, optional257 and onward crossing;
   record actual Insane and LoB combat duration before calling balance accepted.
