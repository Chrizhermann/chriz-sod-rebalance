# chriz-sod-remix

WeiDU tail-mod for the Siege of Dragonspear remix/overhaul. Research and design live in the
parent repo (`docs/`); every component ships only after explicit sign-off
(`docs/design/wave1/` carries the DECIDED/OPEN state per component).

## Components (Wave 1)

| # | Component | What it does |
|---|---|---|
| 100 | Rest-ambush 5× | Maps every active SoD rest-header day/night % through a felt-rate÷5 table (30 areas, felt 22–80% → 8–15% per rest). Composes with other mods (reads current values). BDNOREST untouched; pack size untouched (per-chapter decision). |
| 110 | Keep all companions | Neutralizes the 28 vanilla LeaveParty/DestroySelf strip blocks in BD0103.bcs; adds in-party skip-guards to 9 recruiter-area scripts so kept companions aren't yanked/converted mid-party. Mod-NPC strips untouched. |
| 120 | No mid-campaign hooded man | Removes all five hooded-man appearances (palace bedside, bdcut11 vision, Boareskyr vision cameo, scrying option, Underground River cameo) + the two dangling dialogue replies. Endgame chain untouched (dies with the ending rework). |
| 130 | Skip chapter dreams | Pre-sets `bd_ddd=4` from BDBALDUR.BCS — the four PLAYER1D rest-dreams never fire. Dream content documented in `docs/research/09-sod-dreams.md`. |

## Install

Copy `chriz-sod-remix/` into the game directory, then:

```
weidu.exe chriz-sod-remix/setup-chriz-sod-remix.tp2 --force-install-list 100 110 120 130 --language 0 --use-lang en_US --no-exit-pause
```

Position: tail-install (after EET_end on EET installs — all patches are in-place edits of
final files). Standalone BG:EE+SoD is supported by the same components. Reversible via the
standard WeiDU backups (`weidu_external/backup/chriz-sod-remix`).

## Live-save behavior

`.are`/`.bcs`/`.dlg` load by resref at runtime: changes apply to areas not yet visited and on
next area (re)load. Scenes whose gate globals are already past simply never re-fire.
