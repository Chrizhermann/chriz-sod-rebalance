# 19 — SoD XP recount under corrected engine units

**Status:** research (2026-07-13). Supersedes research/03's absolute totals (its unit
error — `AddexperienceParty` counted per-char instead of party-divided — was
user-verified 2026-07-12 and corrected in 03 §0). Rankings/shape in 03 remain useful;
THIS doc is the number to calibrate against. Tooling:
`research/scripts/recount_xp.py` (sweeps the 1232-script corpus, all override
`BD*.dlg` compiled dialogs, and every `BD####.are` actor table — our components only
zero appearance schedules, so the vanilla placement is still readable on the modded
install).

## Whole-game totals (completionist ceiling, party of 6)

| Layer | Raw | Per character |
|---|---:|---:|
| Script `AddXPObject` (chapter transitions etc.) | — | 88,500 |
| Dialog `AddXPObject` | — | 18,500 |
| Script `AddexperienceParty` (party currency) | 110,700 | 18,450 |
| Dialog `AddexperienceParty` (party currency) | 662,400 | 110,400 |
| Placed hostile kill XP (EA=255 actors) | 1,070,705 | 178,451 |
| **Total swept** | | **≈ 414,300** |

## Reconciliation with the observed anchor

The user's vanilla playthroughs on this install: enter SoD ~220–250k, finish
~700–750k → observed gain **450–530k/char**. The swept ceiling (414k) sits below
that, and the gap is exactly the layers the sweep does NOT count:

- **Scripted/spawned kills** (battle waves, spawn points, rest/travel ambushes,
  bosses spawned by script — e.g. Belhifet's arena, the Boareskyr crusader army).
- **Neutral-flagged creatures that flip hostile** (EA=128 with `Enemy()` — Tsolak,
  Korlasz, quest fights) — excluded by the EA=255 filter.
- **Non-kill mechanical XP**: scroll learning, lock/trap XP (big for mage parties).

Under the OLD per-member model these same sweeps would have projected far above the
observed anchor; under corrected units the model finally sits consistently *below*
it with known-positive missing terms. **The corrected model is the first one
compatible with the observed curve.**

## Known sweep caveats (both directions)

- **Scaled-award overcount:** the reply-branch dedup collapses identical values in
  one dlg but counts *distinct* values separately — dialogs with level-scaled
  variants of one award (e.g. `bdhigg01.dlg`: 6,750/11,500/15,500/15,750 variants)
  are counted at the SUM of variants instead of the one that fires (~38k party
  overcount there alone). Ceiling is therefore slightly generous on the award layer.
- `bdcoun01/02.dlg` carry 19,500–50,000 party grants that look like import/catch-up
  floor adjustments, not earned play — included in the ceiling, flagged.
- CUTSKIP.baf excluded (mirrors duplicate the scenes' own awards).

## The remix delta (the actual question: do we still land at 700–750k?)

All shipped cuts and chunks in party currency (v0.6.2):

| | Party XP |
|---|---:|
| Cut: dig site 133,420 + road north 29,025 + FoW 28,395 + coalition 129,495 + Kanaglym 6,550 + BD7000 20,665 | **347,550** |
| Returned (80% chunks: 106,700 + 23,200 + 22,700 + 103,600 + 5,200 + 16,500) | **277,900** |
| Net vs full-completionist vanilla | **−69,650 party ≈ −11,600/char** |

Plus the prologue: vanilla dungeon ≈24,663/char lost, remix returns ≈25,600/char
(jailbreak kills + the 24,000 AddXPObject reward) → **+~950/char**.

**Verdict: the remix sits ≈ −10,700/char (~2–3% of the observed gain) below a
100%-clearing vanilla run — and closer to neutral against a realistic run, since
the −20% models trash nobody fully cleared. The 700–750k endpoint stands.** The
agreed calibration lever (+10% on main-quest rewards) remains in reserve, to be
pulled only if the stream playthrough's curve comes in low.

## Future work

- Chapter-by-chapter attribution (areas/dialogs → chapter buckets) so each chapter
  pass sees its own budget — needed only if the endpoint drifts.
- Sweep scripted spawns + EA-flip creatures to close the ceiling gap properly.
