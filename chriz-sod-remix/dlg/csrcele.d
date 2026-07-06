// chriz-sod-remix component 180 -- celebration dialog + Korlasz return beat +
// council proclamation line. Design: docs/design/chapters/01-prologue.md sec. 6 +
// sec. 9 + sec. 10; mechanics: docs/research/11a-council-seam.md.
//
// REWRITTEN 2026-07-07 (user, playtest 3): the beat no longer reuses vanilla SoD
// praise strrefs (the old opener borrowed BDLIIA state 11's council pitch, which
// made no sense cold - "We would have you join them" with no antecedent; that
// line now plays only where it belongs, at the next morning's war council). All
// celebration text is ours, written to the BG1 duchess register (user style rule:
// BG1/BG2 voice over SoD; dropping VO is fine). Belt keeps ONE custom line in an
// APPENDed BDBELT state so his name shows as speaker.
//
// State order matters: `praise` and `korlret` carry real triggers; `closing` and
// `korlret2` are transition-only. csrcele is only ever attached via SetDialogue
// on throwaway BDLIIA instances spawned by baf/csrceleb.baf.

BEGIN ~csrcele~

// The celebration beat (first hall entry, plot-50 evening).
IF ~Global("CSR_CELEB_QUEST","GLOBAL",0)~ THEN BEGIN praise
  SAY @18005
  IF ~~ THEN REPLY @18002 EXTERN ~BDBELT~ csr180_praise1
  IF ~~ THEN REPLY @18003 EXTERN ~BDBELT~ csr180_praise1
END

// The Korlasz return beat (spawner block 4 in csrceleb.baf sets CSR_KORL_RET=1).
IF ~Global("CSR_KORL_RET","GLOBAL",1)~ THEN BEGIN korlret
  SAY @18012
  IF ~~ THEN REPLY @18013 GOTO korlret2
  IF ~~ THEN REPLY @18014 GOTO korlret2
END

IF ~~ THEN BEGIN korlret2
  SAY @18015
  IF ~~ THEN DO ~SetGlobal("CSR_KORL_RET","GLOBAL",2)
DestroySelf()~ EXIT
END

// Quest hook + proclamation hand-over (design sec. 6 mini-quest hook, sec. 9
// delivery 1). CSR_CELEB_QUEST=1 is the cross-component signal. Journal @18001
// reuses the vanilla quest title "Sarevok's Servant" so component 170's vanilla
// entries (261626 hint / 261627 kill QUEST_DONE) open and close the SAME journal
// group. EndCutSceneMode is load-bearing: the forced dialog is what ends the
// cutscene (cookbook #6) and every celebration path funnels into this exit.
// DestroySelf despawns the dukes so the plot-51 council variants' own
// CreateCreature calls stay canonical (research 11a sec. 1).
IF ~~ THEN BEGIN closing
  SAY @18000
  IF ~~ THEN REPLY @18004 DO ~SetGlobal("CSR_CELEB_QUEST","GLOBAL",1)
AddJournalEntry(@18001,QUEST)
GiveItemCreate("csrpam",Player1,0,0,0)
EndCutSceneMode()
ActionOverride("BDBELT",DestroySelf())
DestroySelf()~ EXIT
END

// Belt's toast, custom text (no VO), reachable only from csrcele.praise.
APPEND ~BDBELT~

IF ~~ THEN BEGIN csr180_praise1
  SAY @18007
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
INTERJECT_COPY_TRANS ~BDBELT~ 36 CSR_CELEB_BELT_LINE
  == ~BDBELT~ IF ~Global("CSR_CELEB_QUEST","GLOBAL",1)~ THEN @18020
END
