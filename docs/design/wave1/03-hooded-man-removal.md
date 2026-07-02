# Wave 1 — Hooded Man (Irenicus) Mid-Campaign Removal

**Status:** awaiting user sign-off. Complete appearance inventory verified against the live
install (no `.are` placements exist — every appearance is script-created; corpus-wide search).

## Decided (user, 2026-07-03)
Remove the hooded man / Irenicus 100% from the plot. This component removes every
**mid-campaign** appearance. The **endgame** appearances (dream/arrest/jail) die with the
ending rework (separate component) — until that ships, the endgame chain stays functional.

Verified safety: none of the five mid-campaign scenes sets any variable the endgame reads.

## The five appearances and their surgery

| # | Scene | Surgery | What survives |
|---|---|---|---|
| 1 | **BD0103** palace night visit (bdireni at Imoen's bedside, `bd_plot 54`) | Remove the single `CreateCreature("bdireni")` action from the block | The scene itself: Imoen's recovery + farewell chain is gated on `!See("bdireni")` → fires normally without him; Skie's morning wake-up unaffected |
| 2 | **BDCUT11** Caelar-interrogation vision (during BG departure) | Skip the whole cutscene: in `BDCUT10.bcs` replace `StartCutSceneEx("bdcut11")` with `FadeFromColor + EndCutSceneMode` | Party placement, +7500 XP award, chapter increment — all happen in BDCUT10 *before* the vision. The scene is structurally an interrogation *by* the hooded man; nothing meaningful remains without him |
| 3 | **BDCUT28** Boareskyr Bhaal-vision (bridge collapse scene) | Keep the scene; remove the `CreateCreature` + his dialog tail; append `EndCutSceneMode` (required — the dialog normally terminates cutscene mode) | The `sodcin02` movie, journals, `bd_plot=295`, Flaming Fist wake-up |
| 4 | **BDSCRY05/06** scrying-pool vision (opt-in) | Delete the player option: False()-gate reply "~The Hooded Man...~" in `BDSCRY.dlg` states 0 and 4 | The Imoen and Caelar visions and the shared continuation cutscene |
| 5 | **BD5100** Underground River silent cameo | Excise both twin blocks wholesale (avoids a stranded `SetCutSceneLite`) | Nothing else lives in those blocks |

Optional string hygiene (recommended): False()-gate the Imoen reply "~What was that man in
the hood doing here?~" (`BDIMOEN.dlg` state 67, transition 1) — states 68/69 become
unreachable automatically. No `dialog.tlk` edits needed anywhere.

## New finding — a SECOND Hooded Man (decision needed)
`BDCCIRE.CRE` (same display name, different creature) appears **and speaks** in all four
chapter rest-dreams (`PLAYER1D.BCS` → BDDDD1–4 chains, staged in bd0072). His dialogue states
are load-bearing — they carry the dream conclusions and launch the exit cutscenes, so this is
dialogue rework, not a `CreateCreature` deletion.

**Open question:** what happens to the dreams? Options: (a) leave the dreams for now (they're
Bhaal-arc content; handle with the ending/arc work), (b) rework his lines/speaker, (c) cut
the dreams entirely. This component ships without touching them unless you decide otherwise.

## Minor open question
Three tavern-rumor lines (`BDRUMOR3`, chapters 8/9/10) mention "a hooded fellow asking about
you." Once the ending rework removes him entirely, they're red herrings. Remove them here, or
with the ending component?

## Implementation sketch (after sign-off)
Tail-mod `COPY_EXISTING` patches: `BD0103.bcs`, `BDCUT10.bcs`, `BDCUT28.bcs`, `BD5100.bcs`
(`DECOMPILE_AND_PATCH` + `REPLACE_TEXTUALLY`), `BDSCRY.dlg` (+ optionally `BDIMOEN.dlg`) via
`ALTER_TRANS`/state-trigger patching. Reversible; applies on next area load. Scenes already
past in a running save simply never re-fire (gate globals already advanced) — desired
behavior. Compat: pattern-matched edits, no whole-file replacement; endgame boundary
(BD4100/BD0104/BDCUT60\*/BDCUT63/`BDIRENI.dlg`) untouched by this component.
