# chriz-sod-rebalance

A **remix/overhaul + rebalance mod** for **Siege of Dragonspear** (SoD), targeting a
heavily-modded **BG2:EE + EET** install (standalone BG:EE+SoD also in scope). Two parts:

1. **SoD remix** — slim SoD down hard: remove maps/conversations/plot points (removal over
   rewriting), keep ALL companions at SoD start, remove the hooded-man/Irenicus and the
   entire post-victory epilogue (Skie death, trial, jail), Caelar as main antagonist and
   final boss, Skie playable, far fewer ambushes/trash, XP-neutral via a per-chapter ledger.
   **Scope anchor + locked decisions: `docs/01-remix-wishlist.md`** (living document).
2. **Companion rebalance** — buff the weakest joinables; nerf outliers (e.g. Baeloth).

(Part 3, SCS/base-game tweaks, moved to the sibling repo `chriz-bg-rebalance`.)

**Provenance warning:** `docs/design/00–05` were authored by a prior agent WITHOUT the user —
proposals only, never user decisions. Decisions live in `docs/01-remix-wishlist.md` and
`docs/design/wave1/`. Research docs (`docs/research/`) remain valid as data.

This repo is **research/design/plan first**. Implementation (WeiDU tail-mods) comes after the
user signs off each design. Process: global/system levers first (`docs/design/wave1/`), arc
treatment up front, then chapter-by-chapter passes (map removals, cut lists, zero-ambush
areas, XP ledger updates all decided there). **Implementation/testing happens on a separate
game copy** (user maintains copies; dev-target path TBD) — never on the live install below.
The user works sparring-style: no unsolicited decisions; designs list DECIDED vs OPEN.

## Install matrix
- **Dev/test target (install + test mods HERE):**
  `C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install\` — clone of the live
  install (417 WeiDU entries). Tail-install after the last log entry, same rules as live.
- **Clean installs (later compat/hardening tests only):**
  `C:\Games\Baldur's Gate Enhanced Edition modded - dev clean install\` (BG1:EE) and
  `C:\Games\Baldur's Gate II Enhanced Edition modded - dev clean install\` (BG2:EE).
- **Live install (read-only reference, do NOT modify without explicit sign-off):**

## Target install (read-only reference, do NOT modify without sign-off)
- Game dir: `C:\Games\Baldur's Gate II Enhanced Edition modded\`
- Launched via `InfinityLoader.exe` (EEex). WeiDU: `weidu.exe` (v24600) in game dir.
- SoD content lives as **loose `BD####` files in `override\`** (EET imports it there; it is
  NOT in `chitin.key`/biffs). BG1 areas are `BG####`, BG2 are `AR####`, EE bonus `OH####`.
- This is the same install documented by the user's global memory + the `bg-modding` skill.

## How modding this install works (inherited rules — follow exactly)
- **Never uninstall any WeiDU.log entry.** Fixes = direct `override` edits OR new tail-install
  WeiDU mods appended after the current last log entry. Never the old uninstall/reinstall dance.
- **Never manually edit** `WeiDU.log`, `.dlg`, or `.baf` source. Patch via WeiDU
  (`COPY_EXISTING` + `WRITE_*`/`ALTER_*`), which creates reversible backups.
- Domain knowledge (WeiDU, IE file formats, EEex, gotchas) is in the `bg-modding` skill —
  invoke it when implementing. Verified landmines live in its `gotchas.md`.
- Live saves: area `.are`/`.spl`/`.2da` edits apply on next load/cast; already-active spawns
  and joined-CRE data are baked into the save.

## Verified core finding (the reason SoD ambushes feel broken)
The **Beamdog engine rolls the rest-interrupt check PER IN-GAME HOUR**, not once per rest
(IESDP labels the field "per hour"; GemRB diverges to once-per-rest). So an area's listed
day/night chance `c` yields a *felt* chance per 8h rest of **1 − (1 − c/100)⁸**:
`6%→39%`, `8%→49%`, `10%→57%`, `18%→80%`. Interrupted rests heal nothing → you re-rest →
roll again, compounding to ~75–88% during a recovery. Rest-ambushes are the **random
rest-header system** (`.are` offset `0xC0`), NOT scripted — confirmed: no SoD *area* script
uses `Rested()`. So lowering these numbers touches **zero** story/scripted encounters.
To hit a target felt rate `F`, set the field to `100·(1−(1−F)^(1/8))` (≈ `F=15%→2`, `F=20%→3`).
See `docs/research/01-rest-ambush-mechanic.md`.

## Verified EET-transition hard requirement (for the ending rework)
On EET, SoD→BG2 must end with the party in **BD6100** ("The Ambush"): gear banked into
`K#ImportContainer` there and `CreateCreatureObject("K#TELBGT",Player1,...)` fired —
`ar0602.bcs` hardcodes BD6100 as the gear source. **Never modify** `K#TELBGT.BCS`,
`ar0602.bcs`, `CAMPAIGN.2DA`/`STARTARE.2DA`, or the `ENDOFBG1` global (third-party mods patch
them). Mid-campaign hooded-man scenes set nothing the endgame reads (safe to remove); the
trial/jail sequence is self-contained between clean seams (BDCUT61 entry / BD6200 exit).

## Layout
- `docs/01-remix-wishlist.md` — **scope anchor**: the user's wishlist + locked decisions.
- `docs/research/` — verified findings + data (the audit). Source of truth before design.
- `docs/design/wave1/` — current design docs (user-era, DECIDED vs OPEN per doc).
- `docs/design/` (00–05) — prior-agent proposals; data useful, decisions void.
- `research/data/sod_baf/` — all 1232 decompiled SoD scripts (`.baf`) for analysis.
- `research/scripts/` — Python analysis tooling (ARE rest parser, dataset builder).
- `docs/research/sod_areas_dataset.csv` — master per-area rest + scripted-spawn dataset.

## ARE rest-interruption struct (verified offsets; pointer at area header `0xC0`)
`+0x48` 10×resref creature table · `+0x98` table count · `+0x9A` difficulty ·
`+0xA4` max creatures · `+0xA6` enabled · `+0xA8` day% · `+0xAA` night%.
Engine spawns on rest only if `count>0 && enabled && max>0` (empty table ⇒ never spawns).
`spawnamount = partyLevel × difficulty`, capped at `max` — high difficulty ⇒ always max.
