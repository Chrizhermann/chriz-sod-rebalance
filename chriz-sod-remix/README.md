# chriz-sod-remix

WeiDU tail-mod for the Siege of Dragonspear remix/overhaul. Research and design live in the
parent repo (`docs/`); every component ships only after explicit sign-off
(`docs/design/wave1/` carries the DECIDED/OPEN state per component).

## Components

| # | Component | What it does |
|---|---|---|
| 100 | Rest-ambush 5× | Maps every active SoD rest-header day/night % through a felt-rate÷5 table (30 areas, felt 22–80% → 8–15% per rest). Composes with other mods (reads current values). BDNOREST untouched; pack size untouched (per-chapter decision). |
| 110 | Keep all companions | Neutralizes the 28 vanilla LeaveParty/DestroySelf strip blocks in BD0103.bcs; adds in-party skip-guards to 9 recruiter-area scripts so kept companions aren't yanked/converted mid-party. Mod-NPC strips untouched. |
| 120 | No mid-campaign hooded man | Removes all five hooded-man appearances (palace bedside, bdcut11 vision, Boareskyr vision cameo, scrying option, Underground River cameo) + the two dangling dialogue replies. Component 290 removes the endgame chain. |
| 130 | Skip chapter dreams | Pre-sets `bd_ddd=4` from BDBALDUR.BCS — the four PLAYER1D rest-dreams never fire. Dream content documented in `docs/research/09-sod-dreams.md`. |
| 290 | Victory celebration ending | Keeps the real return and playable celebration; Dazzo ends SoD after the public victory dialogue. Removes the optional codas and murder/arrest/epilogue chain. EET enters normal SoA through its existing import rules; standalone ends at native credits. |
| 291 | Existing EET ending repair | Append-only fix for the original 290 carrier-script softlock. Fresh 290 already includes it; an already-corrected installation is left unchanged. Requires 290 and EET. |

This table highlights the global and ending components; `COMPONENTS.md` in the
release contains the complete inventory.

## Install

Extract the release ZIP into the game directory that contains `chitin.key`,
close the game and any mod manager using that directory, then run:

```
setup-chriz-sod-remix.exe
```

Release v0.6.6 exposes **33 declarations in six install groups**. A normal fresh
selection installs **31 components**: omit repair `291` and select one of the
mutually exclusive `900`/`901` alternatives. The designated dev installation has
**32 installed rows**, including its existing `290` and appended repair `291`.

Position: tail-install (after EET_end on EET installs — all patches are in-place edits of
final files). Standalone BG:EE+SoD is supported by the same components. Reversible via the
standard WeiDU backups (`weidu_external/backup/chriz-sod-remix`).

## Live-save behavior

`.are`/`.bcs`/`.dlg` load by resref at runtime: changes apply to areas not yet visited and on
next area (re)load. Scenes whose gate globals are already past simply never re-fire.

## Victory ending (components 290 and 291)

Component 290 keeps the short victory celebration and uses Dazzo's rest conversation
to end SoD. On EET it preserves the installed equipment-import rules and moves directly
into BG2's normal opening. Imported gear goes through EET's normal hidden import
bank; downstream placement is unchanged, rather than being awarded directly to
the party. Standalone SoD uses its native credits endpoint. Install 290
with its declared prerequisites before first visiting BD4300. An older save without the
local import container receives a diagnostic and keeps its equipment and control.

For an EET installation that already has 290, append **291** to repair the original
carrier-script softlock. Do not reinstall 290 or uninstall earlier components:

```
weidu.exe chriz-sod-remix/setup-chriz-sod-remix.tp2 --force-install-list 291 --language 0 --use-lang en_US --no-exit-pause
```

Fresh 290 installations already include this correction; 291 then leaves game resources
unchanged. The repair refuses unexpected endpoint or guard changes before writing.
The isolated EET guard/save-reload check and one real return/celebration run,
celebration reload, and reduced inventory handoff test passed. Six markers and a
bag reached the hidden AR0602 import bank exactly, with saved bag contents intact.
This verifies retention through the standard import rules, not that all equipment
is immediately lootable. Standalone runtime and the original expanded party and
inventory matrix remain untested. See the [runtime evidence](../docs/playtest/2026-09-06-ending-runtime.md).
