# 20 — Dig-site scrying pool: mechanics, locked replacement, and component 225

**Status:** research complete; user decision locked 2026-07-15; implemented in
`chriz-sod-remix` v0.6.3 as component 225. The component is tail-installed on the dev EET
copy and the semantic verifier reports `SUMMARY: 0 failure(s)`. Runtime checks remain for
the next SoD playthrough. The live install remains on v0.5.0 and was not changed.

Issue: GitHub #6 (PT-6). Playtest source:
`docs/playtest/2026-07-11-stream-playtest.md`. Design record:
`docs/plans/2026-07-15-scrying-pool-caelar-omen-design.md`.

Verified against the decompiled SoD corpus (`research/data/sod_baf/`), installed dev
resources (`BDODSCRY.BCS`, `BDSCRY.DLG`, `BD1200.ARE`), component 225's WeiDU source, and
`research/scripts/verify_scrying_pool.py`.

## 1. Vanilla machine, end to end

The pool object uses `BDODSCRY.BCS` in BD1200 at approximately `(1325,2095)`.

1. Three Silver Scepters (`BDMISC55`) are inserted into the pedestal, advancing
   `BD_SDDD12_COUNTER` from 0 to 3. The third insertion grants **3,000 party-total XP** via
   `AddexperienceParty(3000)`.
2. **`BD_SDDD12_CLOUDY` defaults to 0.** Once the third scepter is inserted, the first old
   vision is therefore available without an Essence. This corrects the earlier reading that
   the completed pedestal began cloudy.
3. Choosing a vision in `BDSCRY.DLG` sets `BD_SDDD12_CLOUDY` to 1 before launching its
   cutscene. The next vision then requires one Essence of Clarity (`BDMISC59`), which the
   object script consumes while changing the global back to 0.
4. Vanilla supplies two Essences, so they pay for old visions two and three. The actual
   vanilla economy was **first vision free, then one Essence for each remaining vision**.

The old picker used states 0 and 4 of `BDSCRY.DLG`:

| Choice | Local once-flag | Old route | Staging |
|---|---|---|---|
| Imoen | `bd_sddd12_imoen` | `BDSCRY01` → dialog → `BDSCRY02` | Party moved to BD0118; Imoen trains with Liia Jannath |
| Caelar Argent | `bd_sddd12_caelar` | `BDSCRY03`/`BDSCRY3A` → dialog → `BDSCRY04`/`BDSCRY4A` | Party moved to BD0071; Caelar, Oloneiros, spies, and a large staged crusader army |
| Hooded Man | `bd_sddd12_hood` | `BDSCRY05` → dialog → `BDSCRY06` | Party moved to BD0070; Hephernaan and Irenicus |

All three routes ended through `BDSCRY07`, which restored the murky pool ambients, granted
500 XP to each of Player1–6, and ended cutscene mode. None of the `BDSCRY*` scripts registers
with SoD's CUTSKIP rig, so there was no separate skip-state mirror to patch.

## 2. Item sources and the component-220 interaction

The three scepters are container-held in `Table01` `(1859,2408)`, `Sarcophagus01`
`(2414,1736)`, and `Table02` `(2350,805)`. The two vanilla Essences came from:

- the `Shelf` container at `(1146,1230)`; and
- the droppable inventory of `BDWIGHDD` at `(2474,1951)`.

Component 220 schedule-zeroed that plot-inert wight, reducing reachable Essence sources from
two to one. That was a genuine missing-item regression, but the corrected cloudy-state trace
changes its gameplay consequence: after component 120 removed the Hooded-Man option, the
first surviving vision was free and the second required only one Essence. Component 220 did
**not** prevent either surviving old vision from being watched. The second Essence becomes
required again only because the locked replacement deliberately requires every quest item.

`BDWIGHDD` is not Brother Deepvein's quest wight (`BD_DOD_WIGHT1`). It has no plot consumers,
so restoring it would only reintroduce a cut trash encounter.

## 3. Locked replacement (user, 2026-07-15)

- Remove the Imoen vision completely. Component 160 can make Imoen an active party member,
  so showing her remotely training in Baldur's Gate is incoherent.
- Keep the Hooded-Man vision removed and remove the original Caelar cinematic too.
- Remove the picker, teleports, staged actors and army, forced dialogs, shared teardown, and
  every reachable route through `BDSCRY01`–`BDSCRY07`.
- Keep the item hunt, but require and expend **all three `BDMISC55` scepters and both
  `BDMISC59` Essences** for one payoff.
- Keep `BDWIGHDD` cut. Rehome its Essence into the existing, unlocked, untrapped,
  unscripted `Sarcophagus01` at `(2414,1736)`, alongside that container's original scepter.
- Show exactly one abstract, text-only Caelar omen, with no dialog picker or cutscene:

  > The water clears. A woman in argent armor stands before a door beneath the world.
  > Something waits beyond it—something she knows, or believes she knows. She reaches out.
  > For an instant, you cannot tell whether she is opening the way or being drawn through.
  > Then the water clouds.

- Preserve the 3,000 party-total scepter-completion award. Replace the two surviving
  post-component-120 vision rewards with one **1,000-XP award to each of Player1–6**.
- Make the pool permanently dormant after the omen.

## 4. Component 225 implementation

Component 225 requires components 120 and 220 and is installed after both in the Coast Way
group.

- A count-guarded `BDODSCRY.BCS` patch disables the old one-Essence branches and its sole
  `StartDialogNoSet` launcher. Three `EXTEND_TOP` blocks then own every in-range click after
  `BD_SDDD12_COUNTER=3`: an insufficient-items message, the one-time success transaction,
  and a permanent dormant message.
- The success block requires at least two Essences, sets `CSR_SCRY_DONE=1` before any payment,
  sets `BD_SDDD12_CLOUDY=2` as a terminal value, consumes exactly two Essences, awards
  Player1–6 1,000 XP each, displays the approved text, and restores the murky ambient state.
- The existing 3,000 party-total reward on the third scepter remains untouched.
- `BD1200.ARE` retains the original Shelf Essence and all three scepters. The missing Essence
  is appended to `Sarcophagus01` without restoring `BDWIGHDD` or overwriting its scepter.
- Component 120 already False-gates the Hooded-Man transitions in `BDSCRY` states 0 and 4;
  component 225 False-gates the Imoen and Caelar transitions there as well. The dialog file
  and its state structure remain installed, preserving Aura's state-0 interjection target,
  but the pool object no longer launches the dialog at all.
- The old `BDSCRY01`–`BDSCRY07` resources remain on disk as unreachable dead code. There is
  no live area travel, cutscene-mode entry, creature creation, dialog continuation, retry
  loop, or CUTSKIP path from the pool.

## 5. Verification state

Completed on the v0.6.3 dev EET install:

- sandbox verification is green;
- component 225 tail-install completed;
- the semantic verifier found exactly three reachable container-held scepters and two
  reachable container-held Essences, with the new Essence in `Sarcophagus01`;
- `BDWIGHDD` remains schedule-zero;
- the installed pool has one two-Essence transaction, one once-first completion flag, six
  1,000-XP slot awards, one preserved 3,000 party-total award, no old dialog launcher, and
  all six vanilla picker routes False-gated; and
- verifier result: `SUMMARY: 0 failure(s)`.

Still pending for the next SoD playthrough: acquire all five items naturally, confirm that
one Essence is rejected without consumption or XP, activate the exact omen with both, save
and reload, re-click the dormant pool, and confirm visually that no dialog, cutscene, travel,
or staged actor appears.
