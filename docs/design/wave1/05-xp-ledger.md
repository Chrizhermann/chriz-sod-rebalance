# Wave 1 — XP Ledger (scaffold)

**Status:** policy decided; baseline recount pending. This is infrastructure, not a game change.

## ⚠ Engine-unit correction (2026-07-12, user-verified in-game)

`AddexperienceParty(X)` **DIVIDES X among living party members** — console test
`AddexperienceParty(1000)` added 1,000 to the whole party, not per character. The
project had assumed per-member (research/03 §0, now corrected). Consequences:

- **Every shipped chunk was paying 1/6 of intent.** Re-encoded same day (v0.6.1):
  kill-XP chunks are now the **party-total** `cut × 0.8` in one AddexperienceParty —
  the engine divides it exactly like the kill XP it replaces, which also makes them
  party-size-faithful (solo gets the full amount, like vanilla kills). comp175's
  quest reward is now `AddXPObject(Player1..6, 24000)` (Beamdog's own chapter-award
  pattern, truly per character).
- **Vanilla AddexperienceParty awards are party totals too** (Kherriun 12,000 ≈
  2,000/char; Korlasz surrender 1,000 ≈ 167/char; Ammon moss 3,000 ≈ 500/char).
  `AddXPObject(Player1..6,X)` awards (all chapter transitions) are truly X/char.
  The baseline recount (prep task below) must attribute each award by action type.
- The user's observed calibration anchor (enter ~220–250k, finish ~700–750k) is a
  character-sheet observation and is unit-independent — it stands.

## Decided policy (user, 2026-07-03)
- **XP-neutral remix.** Calibration is the user's *actual playthroughs on this install*:
  MC enters SoD at ~220–250k and finishes at **~700–750k (800k max)**. That endpoint is the
  target — whatever content the remix removes, the ledger re-injects into kept milestones so
  the curve still lands there.
- Tracked as a **running per-chapter ledger**, updated during every chapter pass; final
  calibration pass at the end. No one-shot global reweight.
- `research/03`'s totals (~665–715k gain) are an unverified upper bound — useful for the
  *shape* of the economy (quest-XP-dominated, ~82–88%; kill XP ~12–18%), not for budgeting.

## Ledger structure (one row per chapter pass)

| Chapter | Entry XP (proj.) | Quest XP removed | Kill XP removed | Reinjected | Into which carriers | Exit XP (proj.) |
|---|---|---|---|---|---|---|
| Prologue | 220–250k | ~5,500/char (Imoen 5k AddXPObject×6 + Ammon ~500 — unit-corrected) | 19,163/char (garrison 18,747 + Korlasz 417; Normal, guaranteed) | jailbreak kills ~1,600/char (shipped, comp170) + **24,000/char SHIPPED (comp175, user option c 2026-07-10; re-encoded AddXPObject×6 2026-07-12)** | Liia's return-beat reward (csrcele state 2, before DestroySelf) | entry + ~25.6k |
| Coast Way: dig site | — | 0 | 21,437/char cut (128,620 party) + drowned 4,800 party (2026-07-10 polish) | **SHIPPED: 106,700 party-total** (80%; ≈17,800/char at 6; re-encoded 2026-07-12) | Coldhearth clean-kill `AddExperienceParty` (BD1200.baf) | — |
| Coast Way: BD7000 removal | — | Tsolak stake quest 9,000 party ≈ 1,500/char (unit-corrected) | placed 3,165 + Tsolak kill 8,500 ≈ 1,944/char | **SHIPPED: 16,500 party-total** (80% of 20,665; ≈2,750/char at 6; comp215, 2026-07-13) | rides the guaranteed chapter-9 transition award in BD7100.bcs (SODTXT9 block) | — |
| Road north: main line | — | 0 | 29,025 party (BD7100 27,425 + BD2000 1,015 + BD2010 585) ≈ 4,838/char | **SHIPPED: 23,200 party-total** (80%; ≈3,870/char at 6; re-encoded 2026-07-12) | own once-block on the Boareskyr resolution (`bd_plot > 292`, both branches) | — |
| Road north: Forest of Wyrms (optional loop) | — | 0 | 28,395 party (BD7200 10,835 + BD7230 ambush 2,750 + unreachable BD7220 14,810 incl. 3,000 quest shadow) ≈ 4,733/char | **SHIPPED: 22,700 party-total** (80%; ≈3,780/char at 6; re-encoded 2026-07-12) | own once-block on the Neothelid kill (optional content → optional XP) | — |
| Coalition camp: scouting maps | — | 0 | 129,495 party (BD7300 62,270 + BD7400 6,330 + BD7310 4,000 + BD5000 15,895 + BD5100 41,000) ≈ 21,583/char | **SHIPPED: 103,600 party-total** (80%; ≈17,270/char at 6; re-encoded 2026-07-12) | rides the guaranteed ch-11 transition 20k in BD4000.bcs (fires once; pays even if the optional maps were skipped — flagged, calibration is completionist-based) | — |
| Coalition camp: Kanaglym | — | 0 | 6,550 party ≈ 1,092/char | **SHIPPED: 5,200 party-total** (80%; ≈870/char at 6; re-encoded 2026-07-12) | rides the Kherriun/Dark-Magicians 12,000 award (both RESPONSE branches, one fires; the 12,000 itself is a party total ≈2,000/char) | — |
| … | | | | | | |

## Known reinjection carriers (from `research/03`, all guaranteed awards)
**Unit warning (2026-07-12):** chapter transitions are `AddXPObject×6` = truly per
char; the rest are AddexperienceParty-class = **party totals** (÷6 for per-char).
- Chapter transitions: BD7100 10k · BD3000 15k · BD4000 20k · BD4400 20k (= 65k/char ✓)
- Coldhearth Lich (BD1200 script): 22k party ≈ 3,667/char
- Kherriun + Dark Magicians (BD5300): 12k party ≈ 2,000/char
- Free Halatathlaer (BDHALAT/BDCORWIJ dialogue): 32k — **action type to re-verify in the recount**
- Free Daeros (BDDAEROS dialogue): 18k — **action type to re-verify in the recount**

Awards live in **both** `.baf` and `.dlg` (dialogue is the bigger layer) — reweights must
patch both; scale the award constant, not per-occurrence (reply-branch duplication).

## Calibration stance (user, 2026-07-03)
Numbers only matter once we test and see results. **First calibration lever if the curve
comes in low: increase main-quest rewards by a small margin (~10%).** No reweight ships
before playtesting shows the need.

## Prep task (before/during the first chapter pass)
Recount the baseline **per chapter** (attribute every quest award and kill to its chapter)
so each chapter pass sees its own budget. Tooling goes in `research/scripts/`; the prior
whole-game totals get re-derived and cross-checked against the user's observed endpoint.
