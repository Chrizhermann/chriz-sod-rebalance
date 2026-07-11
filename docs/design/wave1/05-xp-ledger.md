# Wave 1 — XP Ledger (scaffold)

**Status:** policy decided; baseline recount pending. This is infrastructure, not a game change.

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
| Prologue | 220–250k | 8,000/char (Imoen 5k + Ammon 3k, verified 2026-07-10) | 19,163/char (garrison 18,747 + Korlasz 417; Normal, guaranteed) | jailbreak kills ~1,600/char (shipped, comp170) + **24,000/char SHIPPED (comp175, user option c 2026-07-10)** | Liia's return-beat reward (csrcele state 2, before DestroySelf) | entry + ~25.6k |
| Coast Way: dig site | — | 0 | 21,437/char cut (128,620 party) + drowned 4,800 party (2026-07-10 polish) | **17,800/char SHIPPED** (80%, comp220 regenerated) | Coldhearth clean-kill `AddExperienceParty` (BD1200.baf) | — |
| Coast Way: BD7000 removal | — | **not yet ledgered** (area removed by comp210; its kill/quest XP TBD — flag) | | | | |
| Road north: main line | — | 0 | 29,025 party (BD7100 27,425 + BD2000 1,015 + BD2010 585) ≈ 4,838/char | **3,900/char SHIPPED** (80%, comp230) | own once-block on the Boareskyr resolution (`bd_plot > 292`, both branches) | — |
| Road north: Forest of Wyrms (optional loop) | — | 0 | 28,395 party (BD7200 10,835 + BD7230 ambush 2,750 + unreachable BD7220 14,810 incl. 3,000 quest shadow) ≈ 4,733/char | **3,800/char SHIPPED** (80%, comp240) | own once-block on the Neothelid kill (optional content → optional XP) | — |
| … | | | | | | |

## Known reinjection carriers (from `research/03`, all guaranteed awards)
- Chapter transitions: BD7100 10k · BD3000 15k · BD4000 20k · BD4400 20k (= 65k/char)
- Coldhearth Lich (BD1200 script): 22k
- Kherriun + Dark Magicians (BD5300): 12k
- Free Halatathlaer (BDHALAT/BDCORWIJ dialogue): 32k
- Free Daeros (BDDAEROS dialogue): 18k

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
