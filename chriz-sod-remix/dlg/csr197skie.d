// csr197skie.d — component 197: Skie becomes a plain talk-to-join recruit at
// the Ducal Palace; her whole SoD plot surface is retired (issue #2 / PT-4).
//
// Design (user, playtest 2026-07-11): "skip all that and just have her there
// joinable? Maybe talk about her father's dead for a moment and keep it short."
// All @-strings are NEW dialogue and remain PENDING word-level sign-off
// (BG1/BG2 register). Everything else reuses vanilla strrefs.
//
// Surface map: docs/research/15-skie-recruitment.md + issue #2. Key facts the
// edits below rely on (all verified against the dev decompile 2026-07-12):
//  - BDSKIE 8-15 is the vanilla palace meeting ("talking to Daddy" — the PT-4
//    lore contradiction, Entar is dead via comp185). Entered by dialog-start
//    scan when the player clicks her after the council (bd_plot_003=2);
//    BDCUT04A (the alternative StartDialogNoSet entry) is an ORPHANED cutscene
//    (research 11a: no launcher anywhere).
//  - States 5-7 / 1-4 are Beamdog CUT CONTENT: the only JoinParty() calls in
//    the file, gated to BD0120/BD0130 which Skie never reaches in vanilla.
//    Vanilla SoD Skie is not recruitable at all. We resurrect that machinery.
//  - State 34 (+BDBENCE 25) advances bd_plot 293->294. 294 has ZERO readers
//    anywhere (.baf corpus grep + binary DLG grep); the bridge trigger BDBOARB
//    only needs bd_plot<295. The advance is kept on BDBENCE 25 for
//    bookkeeping/compat anyway.
//  - The Boareskyr bridge door (Bridge_Barrels) opens ONLY in BDBENCE 32,
//    which vanilla reaches through the auto-fired Skie banter — the re-routes
//    below keep that reachable Skie-free (Bence auto-starter: csr197bnc.baf).

// ============================================================
// A. BDSKIE — retire the vanilla palace meeting + plot states
// ============================================================

// 8  = palace first meeting root -> replaced by csr197_meet below.
// 34 = BD2000 Boareskyr "things at camp were dull" banter (in-party Skie would
//      still select it on a click at bd_plot=293).
// 37/39 = BD4000 subquest roots, gated bd_skie_plot<5/<10 — with the plot
//      never started both PASS at 0, so a click on in-party Skie in BD4000
//      would start the subquest on a party member.
// 53 = BD4100 "captured Skie" root (bd_skie_plot=10 never happens; gated for
//      the same in-party-click reason).
ADD_STATE_TRIGGER ~BDSKIE~ 8  ~False()~
ADD_STATE_TRIGGER ~BDSKIE~ 34 ~False()~
ADD_STATE_TRIGGER ~BDSKIE~ 37 ~False()~
ADD_STATE_TRIGGER ~BDSKIE~ 39 ~False()~
ADD_STATE_TRIGGER ~BDSKIE~ 53 ~False()~

// ------------------------------------------------------------
// The new palace meeting: short Entar beat -> talk-to-join.
// ------------------------------------------------------------
// CSR_SKIE_PALACE: 0 = not met, 1 = met (offer open), 2 = joined.
// AreaCheck("BD0102") matters: bd_plot_003("bd0102")=2 stays true forever and
// BDDIALOG.2DA's SKIE row flips a dismissed BG1-import Skie onto BDSKIE.dlg —
// without the area gate she could replay the palace meeting anywhere.
// The join replies are hidden while a BG1-carried Skie (DV "SKIE", kept by
// comp110) is in the party — no second Skie (the council-spawn cameo itself
// is PT-3b audit territory, not touched here).
// Join action: bd_joined=1 is the camp-cluster handshake LOCAL states 1-4
// read; ChangeAIScript mirrors BDPARTY's ChangeAIScript(...,CLASS) idiom —
// her CLASS slot ships empty and BDSKIEC is the standard BD party combat AI.

APPEND ~BDSKIE~

IF ~  Global("bd_plot_003","bd0102",2)
Global("EscapeBD0102","BD0102",0)
Global("CSR_SKIE_PALACE","GLOBAL",0)
AreaCheck("BD0102")
~ THEN BEGIN csr197_meet
  SAY @0
  IF ~~ THEN REPLY @1 DO ~SetGlobal("CSR_SKIE_PALACE","GLOBAL",1)~ GOTO csr197_ask
  IF ~~ THEN REPLY @2 DO ~SetGlobal("CSR_SKIE_PALACE","GLOBAL",1)~ GOTO csr197_ask
END

IF ~~ THEN BEGIN csr197_ask
  SAY @3
  IF ~  !InParty("SKIE")
~ THEN REPLY @4 GOTO csr197_join
  IF ~~ THEN REPLY @5 GOTO csr197_stay
END

IF ~~ THEN BEGIN csr197_join
  SAY @6
  IF ~~ THEN DO ~SetGlobal("CSR_SKIE_PALACE","GLOBAL",2)
SetGlobal("bd_joined","locals",1)
ChangeAIScript("bdskiec",CLASS)
JoinParty()~ EXIT
END

IF ~~ THEN BEGIN csr197_stay
  SAY @7
  IF ~~ THEN EXIT
END

// Re-offer while she still waits in the hall (she is cleaned up at the
// BD_plot=55 departure by the comp197 BD0102 blocks if never recruited).
IF ~  Global("CSR_SKIE_PALACE","GLOBAL",1)
AreaCheck("BD0102")
~ THEN BEGIN csr197_again
  SAY @8
  IF ~  !InParty("SKIE")
~ THEN REPLY @9 GOTO csr197_join
  IF ~~ THEN REPLY @10 EXIT
END

// Field re-recruit catch-all: dismissed anywhere outside BD0120/BD0130 she
// would otherwise have nothing to say (the camp cluster 1-4 is area-gated and
// BDPARTY has no Skie handling — she's a BG1-style "waits where dropped"
// companion). Reuses the camp-cluster strrefs and JoinParty states verbatim:
// #266436 "What is it? What do you want now?" -> #266437 rejoin (state 6),
// #266438 wait (state 7). Scanned after every vanilla state, so at BD0120/
// BD0130 the vanilla cluster still wins.
IF ~  GlobalGT("bd_joined","locals",0)
!InParty(Myself)
~ THEN BEGIN csr197_field
  SAY #266436
  IF ~~ THEN REPLY #266437 GOTO 6
  IF ~~ THEN REPLY #266438 GOTO 7
END

END

// ============================================================
// B. BDBENCE — Boareskyr wrap-up works without Skie; the
//    BD3000 "Skie's gone missing" quest never starts
// ============================================================

// State 25 ("You did well here today", bd_plot=293) EXTERNed into the cut
// Skie banter (BDSKIE 33). Re-route it straight to the Bence wrap-up, and
// reproduce state 29's saved/lost branch: unconditional -> 30, gated -> 31
// (continuation transitions: LAST valid wins — vanilla precedent). The
// bd_plot 293->294 bookkeeping stays on both paths.
ALTER_TRANS ~BDBENCE~ BEGIN 25 END BEGIN 0 END BEGIN
  EPILOGUE ~GOTO 30~
END

EXTEND_BOTTOM ~BDBENCE~ 25
  IF ~  !Global("bd_bridgefort_saved","GLOBAL",1)
~ THEN DO ~SetGlobal("bd_plot","global",294)~ GOTO 31
END

// State 32 opens the bridge; its action list EscapeAreaObject'd "bdskie" —
// a no-op when she was never spawned, but it would eject an in-party Skie
// from the area. Same action minus the bdskie line.
ALTER_TRANS ~BDBENCE~ BEGIN 32 END BEGIN 0 END BEGIN
  ACTION ~AddJournalEntry(265108,QUEST)
CreateCreature("bdffmerc",[1380.1925],NW)
OpenDoor("Bridge_Barrels")
EscapeAreaObject("Crusade_camp_exit")~
END

// States 33 (Corwin variant) / 39 (solo variant) start the BD3000
// missing-Skie quest (bd_skie_plot 0->1, journal 259783, readers: BDNEDERL/
// BDWILCH/BDCRUM30/BDCORWIJ + the BD4000/BD4100 chain). The script starter
// block in BDBENCE.bcs is False()-gated by comp197.tpa; these gates cover a
// direct player click at bd_plot=310.
ADD_STATE_TRIGGER ~BDBENCE~ 33 ~False()~
ADD_STATE_TRIGGER ~BDBENCE~ 39 ~False()~

// ============================================================
// C. BDNEDERL — the Marshal never asks you to find Skie
// ============================================================
// State 30's greeting replies exist in gated pairs: (bd_nederlok_skie=0 AND
// bd_skie_plot<5) -> state 32 (the "where is Skie" ask, living-Entar line
// included), complement -> state 31 (plain goodbye). With bd_skie_plot parked
// at 0 forever the ask-pair would ALWAYS win — re-point transitions 2/4/6 to
// state 31 instead of False()-gating them (their complements are false at
// (0,<5), which would strand state 30 with no valid reply). Transition 0
// (the bd_skie_plot>9 reward turn-in) dies naturally.
ALTER_TRANS ~BDNEDERL~ BEGIN 30 END BEGIN 2 4 6 END BEGIN
  EPILOGUE ~GOTO 31~
END
