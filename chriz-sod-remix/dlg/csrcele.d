// chriz-sod-remix component 180 -- celebration dialog + council proclamation line.
// Design: docs/design/chapters/01-prologue.md sec. 6 + sec. 9; mechanics ground
// truth: docs/research/11a-council-seam.md. Compiled with EVALUATE_BUFFER; the
// praise lines are EXISTING SoD strrefs resolved at install time from the dialog
// state tables (see lib/comp180.tpa) because EET remaps SoD strrefs (this install:
// 234300 / 264733 / 264741) while standalone BG:EE+SoD numbers differ:
//   %csr_praise_liia%  = BDLIIA state 11 SAY ("We would have you join them...", no VO)
//   %csr_praise_belt1% = BDBELT state 38 SAY ("Excellent. I knew our faith...", VO BD64733)
//   %csr_praise_belt2% = BDBELT state 41 SAY ("You're doing Baldur's Gate a great
//                        service...", VO BD64741)
// Belt's two lines live in APPENDed BDBELT states rather than csrcele so his
// voice-over plays under the correct speaker name. The appended states have no
// state trigger and no inbound vanilla transition -- unreachable outside this scene.

BEGIN ~csrcele~

// Spoken by the throwaway bdliia instance spawned in baf/csrceleb.baf (attached
// via SetDialogue, so the canonical BDLIIA.dlg small-talk states can never
// hijack the beat). The trigger is a belt-and-braces idempotence guard: the
// quest flag is only ever set by this dialog's own exit.
IF ~Global("CSR_CELEB_QUEST","GLOBAL",0)~ THEN BEGIN praise
  SAY #%csr_praise_liia%
  IF ~~ THEN REPLY @18002 EXTERN ~BDBELT~ csr180_praise1
  IF ~~ THEN REPLY @18003 EXTERN ~BDBELT~ csr180_praise1
END

// Quest hook + proclamation hand-over (design sec. 6 mini-quest hook, sec. 9
// delivery 1). CSR_CELEB_QUEST=1 is the cross-component signal (component 170's
// jailbreak hint may key on it). Journal @18001 reuses the vanilla quest title
// "Sarevok's Servant" so component 170's vanilla entries (261626 hint / 261627
// kill QUEST_DONE) open and close the SAME journal group. EndCutSceneMode is
// load-bearing: the forced dialog is what ends the cutscene (cookbook #6) and
// every dialog path funnels into this single exit. DestroySelf despawns the
// celebration spawns so the plot-51 council variants' own CreateCreature calls
// stay canonical (research 11a sec. 1); safe because neither duke sets any
// global on spawn (BDLIIA.bcs only acts in bd0103 at bd_001_plot=8; the BDBELT
// script resource does not exist -- verified against the dev install).
IF ~~ THEN BEGIN closing
  SAY @18000
  IF ~~ THEN REPLY @18004 DO ~SetGlobal("CSR_CELEB_QUEST","GLOBAL",1)
AddJournalEntry(@18001,QUEST)
GiveItemCreate("csrpam",Player1,0,0,0)
EndCutSceneMode()
ActionOverride("BDBELT",DestroySelf())
DestroySelf()~ EXIT
END

// Belt's praise beat, correct VO, reachable only from csrcele above.
APPEND ~BDBELT~

IF ~~ THEN BEGIN csr180_praise1
  SAY #%csr_praise_belt1%
  IF ~~ THEN GOTO csr180_praise2
END

IF ~~ THEN BEGIN csr180_praise2
  SAY #%csr_praise_belt2%
  IF ~~ THEN EXTERN ~csrcele~ closing
END

END

// Council reference (design sec. 9 delivery 2): one Belt line inserted after his
// last crusade-report state 36 ("...dispatched a hundred Flaming Fists...march on
// Caelar's stronghold", text-anchored at install time in comp180.tpa), falling
// through to BDELTAN 2 ("every sword north") via the copied transition -- so the
// proclamation mention lands directly before Eltan's pitch. This survives
// component 150's council re-points, which touch BDELTAN 4 -> BDBELT 35,
// BDBELT 38 -> 39 and BDLIIA 11 replies only (research 11a sec. 2/3); state 36's
// outgoing transition is not among them. Gated on CSR_CELEB_QUEST so the line
// only plays when the player actually holds the proclamation.
// Verified codegen (dry-run compiled + dumped 2026-07-06): I_C_T APPENDS a
// guarded transition after the original unconditional one; that is correct
// because the engine takes the LAST valid continuation transition (vanilla
// precedent: BDLIIA state 3 lists an unconditional GOTO before a Gender-gated
// one). When the trigger fails, the original transition to BDELTAN 2 plays
// unchanged. The label doubles as a once-flag GLOBAL (WeiDU sets it =1 on
// play), hence it must sit in this component's CSR_CELEB* variable namespace.
INTERJECT_COPY_TRANS ~BDBELT~ 36 CSR_CELEB_BELT_LINE
  == ~BDBELT~ IF ~Global("CSR_CELEB_QUEST","GLOBAL",1)~ THEN @18020
END
