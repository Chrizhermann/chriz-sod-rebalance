# 00 — Project Scope & Plan

## Goal
An SCS-style, principled rebalance that makes a heavily-modded SoD (and broader BG) playthrough
**more enjoyable**: less tedium, fewer trash mobs, fairer resting, meaningful fights, viable
companions. Quality bar: every change justified by data + design rationale, fully reversible,
testable without wrecking a live save.

## Part 1 — SoD Remix / Rebalance  (START HERE)
**Problems (user-stated + verified):** too many random rest-ambushes (per-hour roll →
39–80% felt/rest, see `research/01`), too many trash mobs per encounter (`max 3–6 @ diff
80–200` = always max), thin reward for the slog, some pointless filler.

- **1a. Rest-ambushes** — lower day/night % to target felt rates; cap `max`/`difficulty`;
  per-area policy (prologue ≈ restful). Data: `sod_areas_dataset.csv`. Mechanic: `research/01`.
- **1b. Trash-mob reduction (~70%)** — inventory every SoD combat encounter (scripted +
  spawn-point + rest), classify trash vs set-piece, cut/merge trash. Research → `research/02`.
- **1c. Make 2–3 fights *meaningful*** — pick key battles, redesign for quality over quantity.
- **1d. XP reweight** — move XP from deleted trash into big main-quest rewards so total
  progression is preserved. Research SoD XP economy → `research/03`.
- **1e. (low priority) trim useless filler** — needs user calls; defer.

## Part 2 — Companion Rebalance
Buff the weakest joinable NPCs to viability; nerf clear outliers (Baeloth). Research: power
audit of every joinable NPC (class/kit/stats/spells/items) across BG1+SoD+BG2 on THIS install
(kits are heavily modded — see install memory). User has strong opinions → design is
collaborative. → `research/04`.

## Part 3 — Minor SCS + Base-Game Rebalances
Catalog SCS components active in this install + their SoD/balance touchpoints; identify small
high-value tweaks. → `research/05`.

## Method
- Research → design (numbers + rationale) → user sign-off → WeiDU tail-mod(s) → cautious test.
- One mod or a small component set, appended after the current last WeiDU.log entry. Never
  uninstall. `override` edits via `COPY_EXISTING`, reversible backups. Follow CLAUDE.md rules.
- Live playthrough exists: prefer changes that apply cleanly to a loaded save; flag any that
  need new-area/new-save to take effect.

## Open questions for the user
1. **Target felt rest-ambush rate** per area class (prologue / wilderness / dangerous dungeon).
   User signalled even 50% is "0% fun" → leaning low (e.g. 10–20%/rest, prologue near 0).
2. **Trash-cut aggressiveness** — confirm ~70% and whether to also shrink set-piece battles.
3. **Companion priorities** — which NPCs feel weakest to you; confirm Baeloth as the main nerf.
4. Repo/mod naming, and whether Parts 2–3 ship as separate components.

## Status
- [x] Rest-ambush mechanic verified + dataset (`research/01`, `sod_areas_dataset.csv`)
- [x] SoD encounter inventory — all regions (`research/02a/b/c/d`, `sod_encounters_full.csv`, ~1,300 mobs)
- [x] SoD XP economy incl. dialogue (`research/03`, ~585k quest XP/char, no cap)
- [x] SoD creature-danger audit (`research/06`)
- [x] Travel-ambush system (`research/07`)
- [x] **Part 1 design complete** — `design/00-part1-summary` (capstone) + `design/01–05`
- [ ] **Awaiting user sign-off** on the 8 Part-1 decisions (`design/00` §Decisions)
- [ ] Part 1 implementation (WeiDU tail-mod) — after sign-off
- [ ] Part 2 (companions) — held for user's weakest-NPC shortlist
- [ ] Part 3 (SCS / base-game tweaks) — after Part 1 locked
