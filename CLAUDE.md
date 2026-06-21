# chriz-sod-rebalance

An SCS-style rebalance/remix mod project for **Siege of Dragonspear** (SoD) and broader
BG balance, targeting a heavily-modded **BG2:EE + EET** install. Three parts:

1. **SoD remix/rebalance** — far fewer trash mobs (~70%+ cut), a handful of fights made
   *meaningful* instead of numerous, drastically lower rest-ambush rate, big-quest XP
   re-weighting to compensate for removed trash, and (low priority) trimming useless filler.
2. **Companion rebalance** — mostly buff the weakest joinable NPCs up to viability; nerf the
   clear outliers (e.g. Baeloth).
3. **Minor SCS + base-game rebalances.**

This repo is **research/design/plan first**. Implementation (WeiDU tail-mods) comes after the
design is approved. Nothing here is installed into the live game without explicit sign-off —
the user has an **active playthrough** on the target install.

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

## Layout
- `docs/research/` — verified findings + data (the audit). Source of truth before design.
- `docs/design/` — proposed changes + numbers, per part. Written after research, before code.
- `research/data/sod_baf/` — all 1232 decompiled SoD scripts (`.baf`) for analysis.
- `research/scripts/` — Python analysis tooling (ARE rest parser, dataset builder).
- `docs/research/sod_areas_dataset.csv` — master per-area rest + scripted-spawn dataset.

## ARE rest-interruption struct (verified offsets; pointer at area header `0xC0`)
`+0x48` 10×resref creature table · `+0x98` table count · `+0x9A` difficulty ·
`+0xA4` max creatures · `+0xA6` enabled · `+0xA8` day% · `+0xAA` night%.
Engine spawns on rest only if `count>0 && enabled && max>0` (empty table ⇒ never spawns).
`spawnamount = partyLevel × difficulty`, capped at `max` — high difficulty ⇒ always max.
