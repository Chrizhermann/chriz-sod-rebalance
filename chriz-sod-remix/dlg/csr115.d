// Component 115: conditional Bridgefort continuity. Native route 2 retains
// its dialogue. Route 1 uses Adirran as the persistent local contact so a
// dead or dismissed Khalid cannot remove the quest's command menu.
// Party-state bindings and key native handoffs are checked by csr115_dialog.tpa.

// Voghiln's scripted introduction assumes an independent Jaheira can
// interject. Without her, its fallback attacks the party. Kept Jaheira
// instead leaves his independent recruitment dialogue available.
ADD_STATE_TRIGGER ~BDVOGHIL~ 9 ~!InPartyAllowDead("jaheira")
!Global("csr_jh_carry","GLOBAL",1)~

ADD_STATE_TRIGGER ~BDBFORT~ 2 ~!Global("csr_kh_fort","GLOBAL",1)~
ADD_STATE_TRIGGER ~BDBFORT~ 3 ~!Global("csr_kh_fort","GLOBAL",1)~
ADD_STATE_TRIGGER ~BDKHALID~ 30 ~!Global("csr_kh_fort","GLOBAL",1)~
ADD_STATE_TRIGGER ~BDKHALID~ 48 ~!Global("csr_kh_fort","GLOBAL",1)~
ADD_STATE_TRIGGER ~BDKHALID~ 49 ~!Global("csr_kh_fort","GLOBAL",1)~
ADD_STATE_TRIGGER ~BDKHALID~ 50 ~!Global("csr_kh_fort","GLOBAL",1)~
ADD_STATE_TRIGGER ~BDKHALID~ 51 ~!Global("csr_kh_fort","GLOBAL",1)~
ADD_STATE_TRIGGER ~BDKHALID~ 70 ~!Global("csr_kh_fort","GLOBAL",1)~
ADD_STATE_TRIGGER ~BDKHALID~ 71 ~!Global("csr_kh_fort","GLOBAL",1)~
ADD_STATE_TRIGGER ~BDKHALID~ 23 ~!Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)~
ADD_STATE_TRIGGER ~%csr115_kh_j%~ %csr115_reunion_state% ~!Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)~

APPEND ~BDBFORT~
IF WEIGHT #-10 ~Global("csr_kh_fort","GLOBAL",1)
GlobalLT("bd_bridgefort_plot","GLOBAL",5)
GlobalLT("bd_plot","GLOBAL",250)~ THEN BEGIN csr115_intro
  SAY @0
  IF ~~ THEN REPLY @1 GOTO csr115_brief
END

IF ~~ THEN BEGIN csr115_brief
  SAY @2
  IF ~!IsValidForPartyDialogue("Khalid")~ THEN REPLY @3 GOTO csr115_depart
  IF ~IsValidForPartyDialogue("Khalid")~ THEN REPLY @3 EXTERN ~%csr115_kh_j%~ csr115_lead
END

IF ~~ THEN BEGIN csr115_depart
  SAY @5
  IF ~~ THEN DO ~SetGlobal("bd_bridgefort_plot","GLOBAL",5)
SetGlobal("csr115_briefed","GLOBAL",1)
MakeGlobalOverride()
SaveLocation("LOCALS","bd_default_loc",[2900.1310])
SetGlobal("bd_retreat","LOCALS",0)
EndCutSceneMode()
EscapeAreaMove("bd2000",2900,1310,E)~ UNSOLVED_JOURNAL @90 EXIT
END

IF WEIGHT #-10 ~Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","GLOBAL",5)
AreaCheck("bd2000")
Global("bd_bf_action_plan","GLOBAL",0)~ THEN BEGIN csr115_report
  SAY @6
  IF ~GlobalGT("bd_jegg_plot","GLOBAL",0)
GlobalGT("bd_wynan_plot","GLOBAL",1)~ THEN REPLY @7 DO ~SetGlobal("bd_bf_action_plan","GLOBAL",1)
EraseJournalEntry(@90)~ UNSOLVED_JOURNAL @91 GOTO csr115_plan
  IF ~GlobalLT("bd_wynan_plot","GLOBAL",2)~ THEN REPLY @8 GOTO csr115_wait
  IF ~Global("bd_jegg_plot","GLOBAL",0)~ THEN REPLY @9 GOTO csr115_wait
  IF ~~ THEN REPLY @10 GOTO csr115_wait
END

IF WEIGHT #-10 ~Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","GLOBAL",5)
AreaCheck("bd2000")
GlobalGT("bd_bf_action_plan","GLOBAL",0)~ THEN BEGIN csr115_plan
  SAY @12
  IF ~~ THEN REPLY @13 GOTO csr115_attack
  IF ~~ THEN REPLY @14 GOTO csr115_surrender
  IF ~Global("BD2100GL","GLOBAL",2)
Global("BD_SDD200","GLOBAL",1)~ THEN REPLY @15 GOTO csr115_stone
  IF ~~ THEN REPLY @10 GOTO csr115_wait
END

IF ~~ THEN BEGIN csr115_attack
  SAY @16
  IF ~Global("bd_fists_attack","GLOBAL",2)
!Global("BD_SDD200","GLOBAL",1)~ THEN REPLY @17 GOTO csr115_charge
  IF ~Global("bd_fists_attack","GLOBAL",2)
Global("BD_SDD200","GLOBAL",1)~ THEN REPLY @17 GOTO csr115_weakened
  IF ~GlobalLT("bd_fists_attack","GLOBAL",2)~ THEN REPLY @18 DO ~SetGlobal("bd_bf_attack","GLOBAL",1)~ GOTO csr115_alone
  IF ~GlobalLT("bd_fists_attack","GLOBAL",2)~ THEN REPLY @19 DO ~SetGlobal("bd_bf_attack","GLOBAL",1)
SetGlobal("bd_bf_action_plan","GLOBAL",2)~ GOTO csr115_ready
  IF ~~ THEN REPLY @20 DO ~SetGlobal("bd_bf_action_plan","GLOBAL",2)~ GOTO csr115_wait
END

IF ~~ THEN BEGIN csr115_alone
  SAY @21
  IF ~!Global("BD_SDD200","GLOBAL",1)~ THEN REPLY @22 GOTO csr115_charge
  IF ~Global("BD_SDD200","GLOBAL",1)~ THEN REPLY @22 GOTO csr115_weakened
  IF ~~ THEN REPLY @23 DO ~SetGlobal("bd_bf_action_plan","GLOBAL",2)~ GOTO csr115_ready
  IF ~~ THEN REPLY @20 DO ~SetGlobal("bd_bf_action_plan","GLOBAL",2)~ GOTO csr115_wait
END

IF ~~ THEN BEGIN csr115_weakened
  SAY @24
  IF ~~ THEN REPLY @25 GOTO csr115_charge
  IF ~~ THEN REPLY @26 GOTO csr115_wait
END

IF ~~ THEN BEGIN csr115_charge
  SAY @27
  IF ~~ THEN DO ~SetGlobal("bd_bridgefort_plot","GLOBAL",30)~ EXIT
END

IF ~~ THEN BEGIN csr115_ready
  SAY @28
  IF ~~ THEN UNSOLVED_JOURNAL @92 EXIT
END

IF ~~ THEN BEGIN csr115_wait
  SAY @11
  IF ~~ THEN EXIT
END

IF ~~ THEN BEGIN csr115_surrender
  SAY @29
  IF ~~ THEN REPLY @30 GOTO csr115_negotiate
  IF ~~ THEN REPLY @31 DO ~SetGlobal("bd_bf_action_plan","GLOBAL",3)~ GOTO csr115_wait
END

IF ~~ THEN BEGIN csr115_negotiate
  SAY @32
  IF ~~ THEN DO ~SetGlobal("bd_bridgefort_plot","GLOBAL",6)~ EXIT
  IF ~!Dead("bdjegg")~ THEN DO ~SetGlobal("bd_bridgefort_plot","GLOBAL",6)
CreateCreature("bdjegg",[3180.1375],SW)~ EXIT
END

IF ~~ THEN BEGIN csr115_stone
  SAY @33
  IF ~PartyHasItem("BDSCRL02")~ THEN REPLY @34 GOTO csr115_scroll
  IF ~~ THEN REPLY @35 GOTO csr115_no_scroll
END
IF ~~ THEN BEGIN csr115_scroll
  SAY @36
  IF ~~ THEN EXIT
END
IF ~~ THEN BEGIN csr115_no_scroll
  SAY @37
  IF ~~ THEN EXIT
END
END

APPEND ~%csr115_kh_j%~
IF ~~ THEN BEGIN csr115_lead
  SAY @4
  IF ~~ THEN EXTERN ~BDBFORT~ csr115_depart
END
IF ~~ THEN BEGIN csr115_gift
  SAY @40
  COPY_TRANS ~%csr115_kh_j%~ %csr115_gift_state%
END
IF ~~ THEN BEGIN csr115_neera
  SAY @46
  COPY_TRANS ~%csr115_kh_j%~ %csr115_neera_state%
END
END

APPEND ~BDKHALID~
IF ~~ THEN BEGIN csr115_gift
  SAY @40
  COPY_TRANS ~BDKHALID~ 79
END
IF ~~ THEN BEGIN csr115_parting
  SAY @41
  COPY_TRANS ~BDKHALID~ 11
END
END

APPEND ~BDJAHEIR~
IF ~~ THEN BEGIN csr115_north
  SAY @42
  COPY_TRANS ~BDJAHEIR~ 27
END
IF ~~ THEN BEGIN csr115_search
  SAY @44
  COPY_TRANS ~BDJAHEIR~ 43
END
IF ~~ THEN BEGIN csr115_parting
  SAY @50
  COPY_TRANS ~BDJAHEIR~ 12
END
END

ALTER_TRANS ~BDJAHEIR~ BEGIN csr115_north csr115_search END BEGIN 0 END BEGIN
  ~REPLY~ ~@43~
END

// The smithy cameo has a private death variable/dialogue. It must never
// select Adirran's quest menu or make the persistent commander disappear.
BEGIN ~CSR115AD~
IF ~~ THEN BEGIN 0
  SAY #%csr115_ad0_say%
  COPY_TRANS ~BDBFORT~ 0
END
IF ~~ THEN BEGIN 1
  SAY #%csr115_ad1_say%
  COPY_TRANS ~BDBFORT~ 1
END
