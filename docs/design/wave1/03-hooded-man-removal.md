# Wave 1 — Hooded Man (Irenicus) Mid-Campaign Removal

**Status: SIGNED OFF (user, 2026-07-03)**, including the dream decision below. Complete
appearance inventory verified against the live install (no `.are` placements exist — every
appearance is script-created; corpus-wide search).

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
| 4 | **BDSCRY05/06** scrying-pool vision (opt-in) | Delete the player option: False()-gate reply "~The Hooded Man...~" in `BDSCRY.dlg` states 0 and 4 | At component 120's release, the Imoen/Caelar choices and shared continuation survived; component 225 now supersedes that preservation and retires every old vision route |
| 5 | **BD5100** Underground River silent cameo | Excise both twin blocks wholesale (avoids a stranded `SetCutSceneLite`) | Nothing else lives in those blocks |

Optional string hygiene (recommended): False()-gate the Imoen reply "~What was that man in
the hood doing here?~" (`BDIMOEN.dlg` state 67, transition 1) — states 68/69 become
unreachable automatically. No `dialog.tlk` edits needed anywhere.

**Current follow-on (v0.6.3):** component 225 keeps the dialog resource and Aura's
state-0 interjection structure, but False-gates the Imoen and Caelar replies and removes
the pool object's dialog launcher. `BDSCRY01`–`BDSCRY07` remain on disk only as
unreachable historical resources; the sole live payoff is the text-only Caelar omen.

## The chapter dreams — DECIDED (user, 2026-07-03): document, then SKIP
`BDCCIRE.CRE` (same display name, different creature) appears **and speaks** in all four
chapter rest-dreams (`PLAYER1D.BCS` → BDDDD1–4 chains, staged in bd0072). User verdict: the
dreams are very low quality — **skip them entirely**. Content is preserved in
`docs/research/09-sod-dreams.md` for a maybe-someday rewrite.

**Skip mechanism (verified, ready to implement):** pre-set the sequence global past its
terminal value. `bd_ddd` and `bd_dream_timer` have **zero consumers outside `PLAYER1D.BCS`**
(exhaustive grep: all 1232 SoD scripts, all override `.bcs`/`.dlg`), and every launcher block
requires `bd_ddd` exactly 0–3, so `bd_ddd=4` equals the natural post-all-dreams state.
Implementation: `EXTEND_TOP` the master script (`BALDUR.BCS` on EET, `BDBALDUR.BCS` on
standalone SoD) with:
`IF GlobalLT("bd_ddd","global",4) GlobalGT("chapter","global",7) GlobalLT("chapter","global",13)
THEN SetGlobal("bd_ddd","global",4) Continue()`
Save-agnostic (catches mid-chain saves at bd_ddd 1–3), works on new playthroughs, never
touches Beamdog/EET block text (`PLAYER1D.BCS` is EET-generated and extended by Xan/Sirene
mods on this install — block surgery there would be compat-hostile), and automatically covers
the orphaned alternate dream chain (BDDDD1AA) on any install variant.
Mechanical cost of skipping: four guaranteed ambush-proof full-heal rests become normal
rests — negligible under the 5× ambush reduction. The endgame celebration dream (`BDCUT60`,
BD4100) runs on its own dialog-launched locals and is unaffected.

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
