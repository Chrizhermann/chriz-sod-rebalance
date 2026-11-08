// Complete #115 dialogue states and transitions; unrelated states are retained.

REPLACE ~bdbarghe~
IF %csr115_weight_csr115_0% ~~ THEN BEGIN 31
  SAY #%csr115_s36868%
  IF ~  Global("bd_charname_revealed","global",0)
NumInPartyGT(1)
~ THEN REPLY #%csr115_s36869%  GOTO 37
  IF ~  Global("bd_charname_revealed","global",1)
NumInPartyGT(1)
~ THEN REPLY #%csr115_s36869%  GOTO 32
  IF ~  Global("bd_charname_revealed","global",0)
NumInParty(1)
~ THEN REPLY #%csr115_s65944%  GOTO 37
  IF ~  Global("bd_charname_revealed","global",1)
NumInParty(1)
~ THEN REPLY #%csr115_s65944%  GOTO 32
  IF ~  IsValidForPartyDialogue("khalid")
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY @45  EXTERN ~%csr115_kh_j%~ %csr115_kh_201%
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
IsValidForPartyDialogue("khalid")
~ THEN REPLY #%csr115_s36870%  EXTERN ~%csr115_kh_j%~ %csr115_kh_201%
  IF ~~ THEN REPLY #%csr115_s36871%  GOTO 30
END

END

REPLACE ~bdbfort~
IF %csr115_weight_csr115_1% ~  !Global("csr_kh_fort","GLOBAL",1)
GlobalLT("bd_bridgefort_plot","global",5)
Detect("KHALID")
!IsValidForPartyDialogue("JAHEIRA")
~ THEN BEGIN 2
  SAY #%csr115_s36837%
  IF ~~ THEN DO ~SetGlobal("bd_bridgefort_plot","global",5)
~ EXTERN ~bdkhalid~ 27
END

IF %csr115_weight_csr115_2% ~  !Global("csr_kh_fort","GLOBAL",1)
GlobalLT("bd_bridgefort_plot","global",5)
Detect("KHALID")
IsValidForPartyDialogue("JAHEIRA")
~ THEN BEGIN 3
  SAY #%csr115_s36847%
  IF ~~ THEN DO ~SetGlobal("bd_bridgefort_plot","global",5)
SetGlobal("bd_mdd206","global",2)
~ EXTERN ~bdkhalid~ 28
END

IF %csr115_weight_csr115_3% ~  Global("csr_kh_fort","GLOBAL",1)
GlobalLT("bd_bridgefort_plot","GLOBAL",5)
GlobalLT("bd_plot","GLOBAL",250)
~ THEN BEGIN %csr115_bdbfort_13%
  SAY @0
  IF ~~ THEN REPLY @1  GOTO %csr115_bdbfort_14%
END

IF %csr115_weight_csr115_4% ~~ THEN BEGIN %csr115_bdbfort_14%
  SAY @2
  IF ~  !IsValidForPartyDialogue("Khalid")
~ THEN REPLY @3  GOTO %csr115_bdbfort_15%
  IF ~  IsValidForPartyDialogue("Khalid")
~ THEN REPLY @3  EXTERN ~%csr115_kh_j%~ %csr115_khalij_272%
END

IF %csr115_weight_csr115_5% ~~ THEN BEGIN %csr115_bdbfort_15%
  SAY @5
  IF ~~ THEN DO ~SetGlobal("bd_bridgefort_plot","GLOBAL",5)
SetGlobal("csr115_briefed","GLOBAL",1)
MakeGlobalOverride()
SaveLocation("LOCALS","bd_default_loc",[2900.1310])
SetGlobal("bd_retreat","LOCALS",0)
EndCutSceneMode()
EscapeAreaMove("bd2000",2900,1310,E)
~ UNSOLVED_JOURNAL @90  EXIT
END

IF %csr115_weight_csr115_6% ~  Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","GLOBAL",5)
AreaCheck("bd2000")
Global("bd_bf_action_plan","GLOBAL",0)
~ THEN BEGIN %csr115_bdbfort_16%
  SAY @6
  IF ~  GlobalGT("bd_jegg_plot","GLOBAL",0)
GlobalGT("bd_wynan_plot","GLOBAL",1)
~ THEN REPLY @7  DO ~SetGlobal("bd_bf_action_plan","GLOBAL",1)
EraseJournalEntry(@90)
~ UNSOLVED_JOURNAL @91  GOTO %csr115_bdbfort_17%
  IF ~  GlobalLT("bd_wynan_plot","GLOBAL",2)
~ THEN REPLY @8  GOTO %csr115_bdbfort_23%
  IF ~  Global("bd_jegg_plot","GLOBAL",0)
~ THEN REPLY @9  GOTO %csr115_bdbfort_23%
  IF ~~ THEN REPLY @10  GOTO %csr115_bdbfort_23%
END

IF %csr115_weight_csr115_7% ~  Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","GLOBAL",5)
AreaCheck("bd2000")
GlobalGT("bd_bf_action_plan","GLOBAL",0)
~ THEN BEGIN %csr115_bdbfort_17%
  SAY @12
  IF ~~ THEN REPLY @13  GOTO %csr115_bdbfort_18%
  IF ~~ THEN REPLY @14  GOTO %csr115_bdbfort_24%
  IF ~  Global("BD2100GL","GLOBAL",2)
Global("BD_SDD200","GLOBAL",1)
~ THEN REPLY @15  GOTO %csr115_bdbfort_26%
  IF ~~ THEN REPLY @10  GOTO %csr115_bdbfort_23%
END

IF %csr115_weight_csr115_8% ~~ THEN BEGIN %csr115_bdbfort_18%
  SAY @16
  IF ~  Global("bd_fists_attack","GLOBAL",2)
!Global("BD_SDD200","GLOBAL",1)
~ THEN REPLY @17  GOTO %csr115_bdbfort_21%
  IF ~  Global("bd_fists_attack","GLOBAL",2)
Global("BD_SDD200","GLOBAL",1)
~ THEN REPLY @17  GOTO %csr115_bdbfort_20%
  IF ~  GlobalLT("bd_fists_attack","GLOBAL",2)
~ THEN REPLY @18  DO ~SetGlobal("bd_bf_attack","GLOBAL",1)
~ GOTO %csr115_bdbfort_19%
  IF ~  GlobalLT("bd_fists_attack","GLOBAL",2)
~ THEN REPLY @19  DO ~SetGlobal("bd_bf_attack","GLOBAL",1)
SetGlobal("bd_bf_action_plan","GLOBAL",2)
~ GOTO %csr115_bdbfort_22%
  IF ~~ THEN REPLY @20  DO ~SetGlobal("bd_bf_action_plan","GLOBAL",2)
~ GOTO %csr115_bdbfort_23%
END

IF %csr115_weight_csr115_9% ~~ THEN BEGIN %csr115_bdbfort_19%
  SAY @21
  IF ~  !Global("BD_SDD200","GLOBAL",1)
~ THEN REPLY @22  GOTO %csr115_bdbfort_21%
  IF ~  Global("BD_SDD200","GLOBAL",1)
~ THEN REPLY @22  GOTO %csr115_bdbfort_20%
  IF ~~ THEN REPLY @23  DO ~SetGlobal("bd_bf_action_plan","GLOBAL",2)
~ GOTO %csr115_bdbfort_22%
  IF ~~ THEN REPLY @20  DO ~SetGlobal("bd_bf_action_plan","GLOBAL",2)
~ GOTO %csr115_bdbfort_23%
END

IF %csr115_weight_csr115_10% ~~ THEN BEGIN %csr115_bdbfort_20%
  SAY @24
  IF ~~ THEN REPLY @25  GOTO %csr115_bdbfort_21%
  IF ~~ THEN REPLY @26  GOTO %csr115_bdbfort_23%
END

IF %csr115_weight_csr115_11% ~~ THEN BEGIN %csr115_bdbfort_21%
  SAY @27
  IF ~~ THEN DO ~SetGlobal("bd_bridgefort_plot","GLOBAL",30)
~ EXIT
END

IF %csr115_weight_csr115_12% ~~ THEN BEGIN %csr115_bdbfort_22%
  SAY @28
  IF ~~ THEN UNSOLVED_JOURNAL @92  EXIT
END

IF %csr115_weight_csr115_13% ~~ THEN BEGIN %csr115_bdbfort_23%
  SAY @11
  IF ~~ THEN EXIT
END

IF %csr115_weight_csr115_14% ~~ THEN BEGIN %csr115_bdbfort_24%
  SAY @29
  IF ~~ THEN REPLY @30  GOTO %csr115_bdbfort_25%
  IF ~~ THEN REPLY @31  DO ~SetGlobal("bd_bf_action_plan","GLOBAL",3)
~ GOTO %csr115_bdbfort_23%
END

IF %csr115_weight_csr115_15% ~~ THEN BEGIN %csr115_bdbfort_25%
  SAY @32
  IF ~~ THEN DO ~SetGlobal("bd_bridgefort_plot","GLOBAL",6)
~ EXIT
  IF ~  !Dead("bdjegg")
~ THEN DO ~SetGlobal("bd_bridgefort_plot","GLOBAL",6)
CreateCreature("bdjegg",[3180.1375],SW)
~ EXIT
END

IF %csr115_weight_csr115_16% ~~ THEN BEGIN %csr115_bdbfort_26%
  SAY @33
  IF ~  PartyHasItem("BDSCRL02")
~ THEN REPLY @34  GOTO %csr115_bdbfort_27%
  IF ~~ THEN REPLY #%csr115_s69851%  GOTO %csr115_bdbfort_28%
END

IF %csr115_weight_csr115_17% ~~ THEN BEGIN %csr115_bdbfort_27%
  SAY @36
  IF ~~ THEN EXIT
END

IF %csr115_weight_csr115_18% ~~ THEN BEGIN %csr115_bdbfort_28%
  SAY @37
  IF ~~ THEN EXIT
END

END

REPLACE ~bdjaheir~
IF %csr115_weight_csr115_19% ~~ THEN BEGIN 11
  SAY #%csr115_s57092%
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN GOTO %csr115_bdjaheir_106%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN GOTO 12
END

IF %csr115_weight_csr115_20% ~~ THEN BEGIN 14
  SAY #%csr115_s57098%
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN GOTO %csr115_bdjaheir_106%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN GOTO 12
END

IF %csr115_weight_csr115_21% ~  Global("bd_jaheira_join","global",0)
GlobalLT("bd_plot","global",240)
AreaCheck("bd7100")
~ THEN BEGIN 25
  SAY #%csr115_s42319%
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s42320%  DO ~SetGlobal("bd_jaheira_join","global",1)
SetGlobal("bd_pc_remembers_jaheira","global",1)
~ GOTO %csr115_bdjaheir_104%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s42320%  DO ~SetGlobal("bd_jaheira_join","global",1)
SetGlobal("bd_pc_remembers_jaheira","global",1)
~ GOTO 27
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY @51  DO ~SetGlobal("bd_jaheira_join","global",1)
SetGlobal("bd_pc_remembers_jaheira","global",1)
~ GOTO %csr115_bdjaheir_104%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s42321%  DO ~SetGlobal("bd_jaheira_join","global",1)
SetGlobal("bd_pc_remembers_jaheira","global",1)
~ GOTO 27
END

IF %csr115_weight_csr115_22% ~~ THEN BEGIN 26
  SAY #%csr115_s65486%
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN GOTO %csr115_bdjaheir_104%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN GOTO 27
END

IF %csr115_weight_csr115_23% ~~ THEN BEGIN 42
  SAY #%csr115_s58706%
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s58707%  GOTO %csr115_bdjaheir_104%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s58707%  GOTO 27
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s58708%  GOTO %csr115_bdjaheir_105%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s58708%  GOTO 43
END

IF %csr115_weight_csr115_24% ~~ THEN BEGIN %csr115_bdjaheir_104%
  SAY @42
  IF ~~ THEN REPLY @43  GOTO 29
  IF ~~ THEN REPLY #%csr115_s42325%  GOTO 28
  IF ~~ THEN REPLY #%csr115_s42326%  GOTO 28
END

IF %csr115_weight_csr115_25% ~~ THEN BEGIN %csr115_bdjaheir_105%
  SAY @44
  IF ~~ THEN REPLY @43  GOTO 29
  IF ~~ THEN REPLY #%csr115_s42349%  EXTERN ~bdvoghil~ 14
  IF ~~ THEN REPLY #%csr115_s42350%  GOTO 28
END

IF %csr115_weight_csr115_26% ~~ THEN BEGIN %csr115_bdjaheir_106%
  SAY @50
  IF ~~ THEN REPLY #%csr115_s57094%  GOTO 19
  IF ~~ THEN REPLY #%csr115_s57095%  DO ~ActionOverride("khalid",SetGlobal("bd_npc_camp","locals",1))
SetGlobal("bd_npc_camp","locals",1)
~ GOTO 20
  IF ~~ THEN REPLY #%csr115_s57096%  GOTO 20
END

END

REPLACE ~bdjegg~
IF %csr115_weight_csr115_27% ~~ THEN BEGIN 3
  SAY #%csr115_s43699%
  IF ~  Global("bd_bridgefort_plot","global",5)
Global("bd_jegg_plot","global",0)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY @48  DO ~SetGlobal("bd_jegg_plot","global",1)
~ GOTO 16
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","global",5)
Global("bd_jegg_plot","global",0)
~ THEN REPLY #%csr115_s65992%  DO ~SetGlobal("bd_jegg_plot","global",1)
~ GOTO 16
  IF ~~ THEN REPLY #%csr115_s43700%  EXTERN ~bdmkhiij~ 6
  IF ~  !Race(Player1,DWARF)
Global("bd_205_know_jegg","locals",0)
~ THEN REPLY #%csr115_s43701%  DO ~SetGlobal("bd_205_know_jegg","locals",1)
~ GOTO 11
  IF ~  Race(Player1,DWARF)
Global("bd_205_know_jegg","locals",0)
~ THEN REPLY #%csr115_s43701%  DO ~SetGlobal("bd_205_know_jegg","locals",1)
~ GOTO 12
  IF ~~ THEN REPLY #%csr115_s43702%  GOTO 4
END

IF %csr115_weight_csr115_28% ~~ THEN BEGIN 4
  SAY #%csr115_s43704%
  IF ~  Global("bd_bridgefort_plot","global",5)
Global("bd_jegg_plot","global",0)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY @48  DO ~SetGlobal("bd_jegg_plot","global",1)
~ GOTO 16
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","global",5)
Global("bd_jegg_plot","global",0)
~ THEN REPLY #%csr115_s65993%  DO ~SetGlobal("bd_jegg_plot","global",1)
~ GOTO 16
  IF ~~ THEN REPLY #%csr115_s43706%  GOTO 13
  IF ~  PartyHasItem("bdmisc16")
~ THEN REPLY #%csr115_s65994%  GOTO 43
  IF ~  PartyHasItem("BDSCALEG")
~ THEN REPLY #%csr115_s65995%  GOTO 58
  IF ~  PartyHasItem("bdmisc66")
~ THEN REPLY #%csr115_s70006%  GOTO 61
  IF ~~ THEN REPLY #%csr115_s43707%  GOTO 10
END

IF %csr115_weight_csr115_29% ~  Global("bd_jegg_forge","bd2100",0)
GlobalLT("BD_SDD200","GLOBAL",4)
OR(2)
!IsValidForPartyDialogue("mkhiin")
Global("bd_jegg_reacts_to_mkhiin","global",1)
OR(2)
Global("bd_205_stakeout","global",0)
Global("bd_205_forge_destroyed","global",1)
~ THEN BEGIN 5
  SAY #%csr115_s43709%
  IF ~  Global("bd_bridgefort_plot","global",5)
Global("bd_jegg_plot","global",0)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY @48  DO ~SetGlobal("bd_jegg_plot","global",1)
SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 16
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","global",5)
Global("bd_jegg_plot","global",0)
~ THEN REPLY #%csr115_s65996%  DO ~SetGlobal("bd_jegg_plot","global",1)
SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 16
  IF ~  !Race(Player1,DWARF)
Global("bd_205_know_jegg","locals",0)
~ THEN REPLY #%csr115_s43711%  DO ~SetGlobal("bd_205_know_jegg","locals",1)
SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 11
  IF ~  Race(Player1,DWARF)
Global("bd_205_know_jegg","locals",0)
~ THEN REPLY #%csr115_s43711%  DO ~SetGlobal("bd_205_know_jegg","locals",1)
SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 12
  IF ~  False()
GlobalTimerExpired("bd_205_forge_dragonscale_timer","global")
Global("bd_205_forge_dragonscale","global",1)
~ THEN REPLY #%csr115_s65997%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 60
  IF ~  False()
!GlobalTimerExpired("bd_205_forge_dragonscale_timer","global")
Global("bd_205_forge_dragonscale","global",1)
~ THEN REPLY #%csr115_s65997%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 54
  IF ~  False()
GlobalTimerExpired("bd_205_forge_voidstones_timer","global")
Global("bd_205_forge_voidstones","global",1)
~ THEN REPLY #%csr115_s67123%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 53
  IF ~  False()
!GlobalTimerExpired("bd_205_forge_voidstones_timer","global")
Global("bd_205_forge_voidstones","global",1)
~ THEN REPLY #%csr115_s67123%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 54
  IF ~  PartyHasItem("bdmisc16")
~ THEN REPLY #%csr115_s65994%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 43
  IF ~  PartyHasItem("BDSCALEG")
~ THEN REPLY #%csr115_s65995%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 58
  IF ~  PartyHasItem("bdmisc66")
~ THEN REPLY #%csr115_s70439%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 61
  IF ~~ THEN REPLY #%csr115_s43712%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 13
  IF ~~ THEN REPLY #%csr115_s43713%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 10
END

IF %csr115_weight_csr115_30% ~~ THEN BEGIN 20
  SAY #%csr115_s66014%
  IF ~  Global("csr_kh_fort","GLOBAL",1)
~ THEN DO ~AddJournalEntry(@91,QUEST)
Face(NE)
~ EXIT
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
~ THEN DO ~AddJournalEntry(%csr115_s66016%,QUEST)
Face(NE)
~ EXIT
  IF ~  GlobalLT("bd_wynan_plot","global",2)
Global("csr_kh_fort","GLOBAL",1)
~ THEN DO ~AddJournalEntry(@90,QUEST)
Face(NE)
~ EXIT
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
GlobalLT("bd_wynan_plot","global",2)
~ THEN DO ~AddJournalEntry(%csr115_s66015%,QUEST)
Face(NE)
~ EXIT
END

IF %csr115_weight_csr115_31% ~~ THEN BEGIN 22
  SAY #%csr115_s46541%
  IF ~  Global("csr_kh_fort","GLOBAL",1)
~ THEN EXTERN ~csr115ad~ 0
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
~ THEN EXTERN ~bdbfort~ 0
END

IF %csr115_weight_csr115_32% ~~ THEN BEGIN 23
  SAY #%csr115_s46546%
  IF ~  Global("csr_kh_fort","GLOBAL",1)
~ THEN EXTERN ~csr115ad~ 1
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
~ THEN EXTERN ~bdbfort~ 1
END

IF %csr115_weight_csr115_33% ~~ THEN BEGIN 25
  SAY #%csr115_s46554%
  IF ~  Global("csr_kh_fort","GLOBAL",1)
~ THEN DO ~ActionOverride("bdroark",EscapeArea())
ActionOverride("csr115ad",EscapeArea())
ActionOverride("bdbfort3",EscapeArea())
MoveToPoint([1533.625])
Face(NE)
~ EXIT
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
~ THEN DO ~ActionOverride("bdroark",EscapeArea())
ActionOverride("bdbfort",EscapeArea())
ActionOverride("bdbfort3",EscapeArea())
ActionOverride("khalid",EscapeArea())
MoveToPoint([1533.625])
Face(NE)
~ EXIT
END

IF %csr115_weight_csr115_34% ~  Global("bd_jegg_forge","bd2100",0)
!GlobalLT("BD_SDD200","GLOBAL",4)
OR(2)
!IsValidForPartyDialogue("mkhiin")
Global("bd_jegg_reacts_to_mkhiin","global",1)
~ THEN BEGIN 49
  SAY #%csr115_s43825%
  IF ~  Global("bd_bridgefort_plot","global",5)
Global("bd_jegg_plot","global",0)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY @48  DO ~SetGlobal("bd_jegg_plot","global",1)
SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 16
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","global",5)
Global("bd_jegg_plot","global",0)
~ THEN REPLY #%csr115_s65996%  DO ~SetGlobal("bd_jegg_plot","global",1)
SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 16
  IF ~  False()
GlobalTimerExpired("bd_205_forge_voidstones_timer","global")
Global("bd_205_forge_voidstones","global",1)
~ THEN REPLY #%csr115_s67123%  GOTO 53
  IF ~  False()
!GlobalTimerExpired("bd_205_forge_voidstones_timer","global")
Global("bd_205_forge_voidstones","global",1)
~ THEN REPLY #%csr115_s67123%  GOTO 54
  IF ~  False()
GlobalTimerExpired("bd_205_mhkiin_armor_timer","global")
Global("bd_205_mkhiin_armor","global",1)
~ THEN REPLY #%csr115_s67124%  GOTO 54
  IF ~  False()
!GlobalTimerExpired("bd_205_mhkiin_armor_timer","global")
Global("bd_205_mkhiin_armor","global",1)
~ THEN REPLY #%csr115_s67124%  GOTO 53
  IF ~  BeenInParty("mkhiin")
!IsValidForPartyDialogue("mkhiin")
Global("bd_205_mkhiin_armor","global",0)
~ THEN REPLY #%csr115_s43827%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 50
  IF ~  IsValidForPartyDialogue("mkhiin")
Global("bd_205_mkhiin_armor","global",0)
~ THEN REPLY #%csr115_s43827%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ EXTERN ~bdmkhiij~ 7
  IF ~  PartyHasItem("bdmisc16")
~ THEN REPLY #%csr115_s43828%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 43
  IF ~  False()
GlobalTimerExpired("bd_205_forge_dragonscale_timer","global")
Global("bd_205_forge_dragonscale","global",1)
~ THEN REPLY #%csr115_s65997%  GOTO 60
  IF ~  False()
!GlobalTimerExpired("bd_205_forge_dragonscale_timer","global")
Global("bd_205_forge_dragonscale","global",1)
~ THEN REPLY #%csr115_s65997%  GOTO 54
  IF ~  PartyHasItem("bdmisc66")
~ THEN REPLY #%csr115_s70441%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 61
  IF ~  PartyHasItem("BDSCALEG")
~ THEN REPLY #%csr115_s70442%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 58
  IF ~~ THEN REPLY #%csr115_s43829%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 51
  IF ~~ THEN REPLY #%csr115_s43826%  DO ~SetGlobal("bd_pc_met_jegg","global",1)
~ GOTO 42
END

END

REPLACE ~bdkhalid~
IF %csr115_weight_csr115_35% ~  GlobalGT("bd_joined","locals",0)
~ THEN BEGIN 10
  SAY #%csr115_s57122%
  IF ~  !IsValidForPartyDialogue("jaheira")
GlobalGT("bd_npc_camp_chapter","global",1)
GlobalLT("bd_npc_camp_chapter","global",5)
OR(2)
!Range("ff_camp",999)
NextTriggerObject("ff_camp")
!IsOverMe("khalid")
~ THEN REPLY #%csr115_s57123%  DO ~SetGlobal("bd_npc_camp","locals",1)
~ GOTO 12
  IF ~  IsValidForPartyDialogue("jaheira")
GlobalGT("bd_npc_camp_chapter","global",1)
GlobalLT("bd_npc_camp_chapter","global",5)
OR(2)
!Range("ff_camp",999)
NextTriggerObject("ff_camp")
!IsOverMe("khalid")
OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s57123%  GOTO %csr115_bdkhalid_127%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
IsValidForPartyDialogue("jaheira")
GlobalGT("bd_npc_camp_chapter","global",1)
GlobalLT("bd_npc_camp_chapter","global",5)
OR(2)
!Range("ff_camp",999)
NextTriggerObject("ff_camp")
!IsOverMe("khalid")
~ THEN REPLY #%csr115_s57123%  GOTO 11
  IF ~  !IsValidForPartyDialogue("jaheira")
~ THEN REPLY #%csr115_s57124%  GOTO 14
  IF ~  IsValidForPartyDialogue("jaheira")
OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s57124%  GOTO %csr115_bdkhalid_127%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
IsValidForPartyDialogue("jaheira")
~ THEN REPLY #%csr115_s57124%  GOTO 11
  IF ~~ THEN REPLY #%csr115_s57125%  GOTO 17
  IF ~~ THEN REPLY #%csr115_s57126%  GOTO 16
END

IF %csr115_weight_csr115_36% ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
Global("bd_mdd206","global",1)
~ THEN BEGIN 23
  SAY #%csr115_s42374%
  IF ~~ THEN DO ~SetGlobal("bd_mdd206","global",2)
~ EXTERN ~%csr115_jhd1176%~ %csr115_jhs1176%
END

IF %csr115_weight_csr115_37% ~  !Global("csr_kh_fort","GLOBAL",1)
GlobalLT("bd_bridgefort_plot","global",5)
AreaCheck("bd2000")
~ THEN BEGIN 30
  SAY #%csr115_s57924%
  IF ~~ THEN REPLY #%csr115_s57925%  DO ~SetGlobal("bd_bridgefort_plot","global",5)
~ GOTO 35
  IF ~  !IsValidForPartyDialogue("jaheira")
GlobalGT("bd_jaheira_join","global",0)
~ THEN REPLY #%csr115_s57926%  DO ~SetGlobal("bd_bridgefort_plot","global",5)
~ GOTO 34
  IF ~  Dead("jaheira")
GlobalGT("bd_jaheira_join","global",0)
~ THEN REPLY #%csr115_s57927%  DO ~SetGlobal("bd_bridgefort_plot","global",5)
~ GOTO 31
  IF ~~ THEN REPLY #%csr115_s57928%  DO ~SetGlobal("bd_bridgefort_plot","global",5)
~ GOTO 35
  IF ~~ THEN REPLY #%csr115_s57929%  DO ~SetGlobal("bd_bridgefort_plot","global",5)
~ GOTO 36
END

IF %csr115_weight_csr115_38% ~  !Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","global",5)
AreaCheck("bd2000")
GlobalGT("bd_jegg_plot","global",0)
GlobalLT("bd_wynan_plot","global",2)
~ THEN BEGIN 48
  SAY #%csr115_s65915%
  IF ~~ THEN EXIT
  IF ~  !Global("bd_mdd206","global",2)
See("Jaheira")
IsValidForPartyDialogue("Jaheira")
~ THEN DO ~SetGlobal("bd_mdd206","global",2)
~ EXIT
END

IF %csr115_weight_csr115_39% ~  !Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","global",5)
AreaCheck("bd2000")
Global("bd_jegg_plot","global",0)
!GlobalLT("bd_wynan_plot","global",2)
~ THEN BEGIN 49
  SAY #%csr115_s65916%
  IF ~~ THEN EXIT
  IF ~  !Global("bd_mdd206","global",2)
See("Jaheira")
IsValidForPartyDialogue("Jaheira")
~ THEN DO ~SetGlobal("bd_mdd206","global",2)
~ EXIT
END

IF %csr115_weight_csr115_40% ~  !Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","global",5)
AreaCheck("bd2000")
Global("bd_jegg_plot","global",0)
GlobalLT("bd_wynan_plot","global",2)
~ THEN BEGIN 50
  SAY #%csr115_s57970%
  IF ~~ THEN EXIT
  IF ~  !Global("bd_mdd206","global",2)
See("Jaheira")
IsValidForPartyDialogue("Jaheira")
~ THEN DO ~SetGlobal("bd_mdd206","global",2)
~ EXIT
END

IF %csr115_weight_csr115_41% ~  !Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","global",5)
AreaCheck("bd2000")
GlobalGT("bd_jegg_plot","global",0)
!GlobalLT("bd_wynan_plot","global",2)
GlobalLT("bd_bf_action_plan","global",2)
~ THEN BEGIN 51
  SAY #%csr115_s57971%
  IF ~  Global("bd_bf_action_plan","global",0)
~ THEN REPLY #%csr115_s65917%  DO ~SetGlobal("bd_bf_action_plan","global",1)
AddJournalEntry(%csr115_s65934%,QUEST)
~ GOTO 52
  IF ~  !Global("bd_bf_action_plan","global",0)
Global("bd_fists_attack","global",2)
~ THEN REPLY #%csr115_s59763%  GOTO 56
  IF ~  !Global("bd_bf_action_plan","global",0)
~ THEN REPLY #%csr115_s57972%  GOTO 55
  IF ~  !Global("bd_bf_action_plan","global",0)
Global("BD2100GL","GLOBAL",2)
Global("BD_SDD200","GLOBAL",1)
~ THEN REPLY #%csr115_s57973%  GOTO 75
  IF ~  False()
!Global("bd_bf_action_plan","global",0)
Global("BD_SDD223","GLOBAL",0)
!Dead("JAHEIRA")
OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s57974%  GOTO %csr115_bdkhalid_126%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
False()
!Global("bd_bf_action_plan","global",0)
Global("BD_SDD223","GLOBAL",0)
!Dead("JAHEIRA")
~ THEN REPLY #%csr115_s57974%  GOTO 79
  IF ~  False()
!Global("bd_bf_action_plan","global",0)
Global("BD_SDD223","GLOBAL",1)
PartyHasItem("BDSILK01")
~ THEN REPLY #%csr115_s57975%  GOTO 85
  IF ~~ THEN REPLY #%csr115_s65918%  GOTO 54
END

IF %csr115_weight_csr115_42% ~~ THEN BEGIN 52
  SAY #%csr115_s65919%
  IF ~  Global("bd_fists_attack","global",2)
~ THEN REPLY #%csr115_s59763%  GOTO 56
  IF ~~ THEN REPLY #%csr115_s57972%  GOTO 55
  IF ~  Global("BD2100GL","GLOBAL",2)
Global("BD_SDD200","GLOBAL",1)
~ THEN REPLY #%csr115_s57973%  GOTO 75
  IF ~  False()
Global("BD_SDD223","GLOBAL",0)
!Dead("JAHEIRA")
OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s57974%  GOTO %csr115_bdkhalid_126%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
False()
Global("BD_SDD223","GLOBAL",0)
!Dead("JAHEIRA")
~ THEN REPLY #%csr115_s57974%  GOTO 79
  IF ~  False()
Global("BD_SDD223","GLOBAL",1)
PartyHasItem("BDSILK01")
~ THEN REPLY #%csr115_s57975%  GOTO 85
  IF ~~ THEN REPLY #%csr115_s57976%  GOTO 53
  IF ~~ THEN REPLY #%csr115_s57977%  GOTO 54
END

IF %csr115_weight_csr115_43% ~  !Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","global",5)
AreaCheck("bd2000")
~ THEN BEGIN 70
  SAY #%csr115_s65935%
  IF ~  Global("bd_bf_action_plan","global",2)
Global("bd_fists_attack","global",2)
!Global("BD_SDD200","GLOBAL",1)
~ THEN REPLY #%csr115_s65936%  DO ~SetGlobal("bd_bf_action_plan","global",3)
~ GOTO 57
  IF ~  Global("bd_bf_action_plan","global",2)
Global("bd_fists_attack","global",2)
Global("BD_SDD200","GLOBAL",1)
~ THEN REPLY #%csr115_s65936%  DO ~SetGlobal("bd_bf_action_plan","global",3)
~ GOTO 60
  IF ~  Global("bd_bf_action_plan","global",2)
GlobalLT("bd_fists_attack","global",2)
~ THEN REPLY #%csr115_s65937%  DO ~SetGlobal("bd_bf_attack","GLOBAL",1)
SetGlobal("bd_bf_action_plan","global",3)
~ GOTO 59
  IF ~  Global("bd_bf_action_plan","global",3)
~ THEN REPLY #%csr115_s65938%  DO ~SetGlobal("bd_bf_action_plan","global",2)
~ GOTO 65
  IF ~  Global("bd_bf_action_plan","global",3)
~ THEN REPLY #%csr115_s65939%  DO ~SetGlobal("bd_bf_action_plan","global",2)
~ GOTO 64
  IF ~  Global("BD2100GL","GLOBAL",2)
Global("BD_SDD200","GLOBAL",1)
~ THEN REPLY #%csr115_s57973%  GOTO 75
  IF ~  Global("bd_bf_action_plan","global",2)
~ THEN REPLY #%csr115_s65940%  DO ~SetGlobal("bd_bf_action_plan","global",3)
~ GOTO 62
  IF ~  Global("bd_bf_action_plan","global",3)
~ THEN REPLY #%csr115_s65941%  DO ~SetGlobal("bd_bf_action_plan","global",2)
~ GOTO 56
  IF ~~ THEN REPLY #%csr115_s65942%  GOTO 68
END

IF %csr115_weight_csr115_44% ~  !Global("csr_kh_fort","GLOBAL",1)
Global("bd_bridgefort_plot","global",30)
AreaCheck("bd2000")
~ THEN BEGIN 71
  SAY #%csr115_s38222%
  IF ~~ THEN DO ~SetGlobal("bd_bridgefort_plot","global",31)
~ EXIT
END

IF %csr115_weight_csr115_45% ~  !HappinessLT(Myself,-290)
Global("bd_joined","locals",0)
~ THEN BEGIN 119
  SAY #%csr115_s57104%
  IF ~  OR(3)
!See("jaheira")
IsValidForPartyDialogue("jaheira")
Dead("jaheira")
~ THEN REPLY #%csr115_s57105%  GOTO 120
  IF ~  See("jaheira")
!IsValidForPartyDialogue("jaheira")
!Dead("jaheira")
~ THEN REPLY #%csr115_s57105%  GOTO 121
  IF ~  OR(3)
!See("jaheira")
IsValidForPartyDialogue("jaheira")
Dead("jaheira")
~ THEN REPLY #%csr115_s57106%  GOTO 120
  IF ~  See("jaheira")
!IsValidForPartyDialogue("jaheira")
!Dead("jaheira")
~ THEN REPLY #%csr115_s57106%  GOTO 121
  IF ~  Global("BD_SDD223","GLOBAL",0)
GlobalLT("chapter","global",%csr115_ch11%)
!Dead("JAHEIRA")
OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s57974%  GOTO %csr115_bdkhalid_126%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
Global("BD_SDD223","GLOBAL",0)
GlobalLT("chapter","global",%csr115_ch11%)
!Dead("JAHEIRA")
~ THEN REPLY #%csr115_s57974%  GOTO 79
  IF ~  Global("BD_SDD223","GLOBAL",1)
GlobalLT("chapter","global",%csr115_ch11%)
PartyHasItem("BDSILK01")
!Dead("JAHEIRA")
~ THEN REPLY #%csr115_s57975%  GOTO 85
  IF ~  OR(2)
Global("BD_SDD223","GLOBAL",3)
Global("BD_SDD223","GLOBAL",4)
GlobalLT("chapter","global",%csr115_ch13%)
PartyHasItem("MISC33")
!Dead("JAHEIRA")
~ THEN REPLY #%csr115_s58651%  GOTO 95
  IF ~  OR(3)
!See("jaheira")
IsValidForPartyDialogue("jaheira")
Dead("jaheira")
~ THEN REPLY #%csr115_s57107%  GOTO 124
  IF ~  See("jaheira")
!IsValidForPartyDialogue("jaheira")
!Dead("jaheira")
~ THEN REPLY #%csr115_s57107%  EXTERN ~bdjaheir~ 99
  IF ~~ THEN REPLY #%csr115_s57108%  GOTO 124
END

IF %csr115_weight_csr115_46% ~~ THEN BEGIN %csr115_bdkhalid_126%
  SAY @40
  IF ~~ THEN REPLY #%csr115_s50715%  GOTO 80
  IF ~~ THEN REPLY #%csr115_s50716%  GOTO 80
  IF ~~ THEN REPLY #%csr115_s50717%  GOTO 80
END

IF %csr115_weight_csr115_47% ~~ THEN BEGIN %csr115_bdkhalid_127%
  SAY @41
  IF ~  GlobalGT("bd_npc_camp_chapter","global",1)
GlobalLT("bd_npc_camp_chapter","global",5)
OR(2)
!Range("ff_camp",999)
NextTriggerObject("ff_camp")
!IsOverMe("khalid")
~ THEN REPLY #%csr115_s57128%  DO ~ActionOverride("jaheira",SetGlobal("bd_npc_camp","locals",1))
SetGlobal("bd_npc_camp","locals",1)
~ EXTERN ~%csr115_jhd1166%~ %csr115_jhs1166%
  IF ~~ THEN REPLY #%csr115_s57129%  EXTERN ~%csr115_jhd1167%~ %csr115_jhs1167%
  IF ~~ THEN REPLY #%csr115_s57130%  GOTO 18
END

END

REPLACE ~bdneera~
IF %csr115_weight_csr115_48% ~~ THEN BEGIN 57
  SAY #%csr115_s36444%
  IF ~  !IsValidForPartyDialogue("KHALID")
~ THEN GOTO 64
  IF ~  IsValidForPartyDialogue("KHALID")
OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN EXTERN ~%csr115_kh_j%~ %csr115_khalij_274%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
IsValidForPartyDialogue("KHALID")
~ THEN EXTERN ~%csr115_kh_j%~ %csr115_kh_199%
END

END

REPLACE ~bdvoghil~
IF %csr115_weight_csr115_49% ~  !InPartyAllowDead("jaheira")
!Global("csr_jh_carry","GLOBAL",1)
Global("bd_jaheira_join","global",0)
GlobalLT("bd_plot","global",240)
AreaCheck("bd7100")
~ THEN BEGIN 9
  SAY #%csr115_s42313%
  IF ~~ THEN DO ~SetGlobal("bd_jaheira_join","global",-1)
Enemy()
Shout(ASSIST)
~ EXIT
  IF ~  Detect("jaheira")
!Dead("jaheira")
!IsValidForPartyDialogue("jaheira")
~ THEN DO ~SetGlobal("bd_jaheira_join","global",1)
SetGlobal("bd_voghiln_join","global",1)
~ EXTERN ~bdjaheir~ 24
END

END

REPLACE ~bdwynan~
IF %csr115_weight_csr115_50% ~  GlobalLT("bd_wynan_plot","global",2)
AreaCheck("bd2100")
GlobalLT("bd_bridgefort_plot","global",9)
~ THEN BEGIN 0
  SAY #%csr115_s43408%
  IF ~  Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY @47  DO ~SetGlobal("bd_wynan_plot","global",2)
~ GOTO 1
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s43409%  DO ~SetGlobal("bd_wynan_plot","global",2)
~ GOTO 1
  IF ~~ THEN REPLY #%csr115_s43407%  DO ~SetGlobal("bd_wynan_plot","global",1)
~ GOTO 3
  IF ~~ THEN REPLY #%csr115_s43411%  DO ~SetGlobal("bd_wynan_plot","global",1)
~ GOTO 3
  IF ~~ THEN REPLY #%csr115_s43412%  DO ~SetGlobal("bd_wynan_plot","global",1)
~ GOTO 3
END

IF %csr115_weight_csr115_51% ~~ THEN BEGIN 2
  SAY #%csr115_s43413%
  IF ~  Global("csr_kh_fort","GLOBAL",1)
~ THEN DO ~SetCutSceneLite(TRUE)
AddJournalEntry(@90,QUEST)
AddJournalEntry(%csr115_s43431%,QUEST)
ReallyForceSpellPointRES("SPBD001",[1003.941])
SetGlobal("BD_HARLEM_SHAKE","BD2100",1)
DisplayString(Myself,%csr115_s43415%)
~ EXIT
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
~ THEN DO ~SetCutSceneLite(TRUE)
AddJournalEntry(%csr115_s61738%,QUEST)
AddJournalEntry(%csr115_s43431%,QUEST)
ReallyForceSpellPointRES("SPBD001",[1003.941])
SetGlobal("BD_HARLEM_SHAKE","BD2100",1)
DisplayString(Myself,%csr115_s43415%)
~ EXIT
  IF ~  GlobalGT("bd_jegg_plot","global",0)
Global("csr_kh_fort","GLOBAL",1)
~ THEN DO ~SetCutSceneLite(TRUE)
AddJournalEntry(@91,QUEST)
AddJournalEntry(%csr115_s43431%,QUEST)
ReallyForceSpellPointRES("SPBD001",[1003.941])
SetGlobal("BD_HARLEM_SHAKE","BD2100",1)
DisplayString(Myself,%csr115_s43415%)
~ EXIT
  IF ~  !Global("csr_kh_fort","GLOBAL",1)
GlobalGT("bd_jegg_plot","global",0)
~ THEN DO ~SetCutSceneLite(TRUE)
AddJournalEntry(%csr115_s67430%,QUEST)
AddJournalEntry(%csr115_s43431%,QUEST)
ReallyForceSpellPointRES("SPBD001",[1003.941])
SetGlobal("BD_HARLEM_SHAKE","BD2100",1)
DisplayString(Myself,%csr115_s43415%)
~ EXIT
END

END

REPLACE ~%csr115_kh_j%~
IF %csr115_weight_csr115_52% ~~ THEN BEGIN %csr115_kh_177%
  SAY #%csr115_s57092%
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN EXTERN ~bdjaheir~ %csr115_bdjaheir_106%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN EXTERN ~bdjaheir~ 12
END

IF %csr115_weight_csr115_53% ~~ THEN BEGIN %csr115_kh_178%
  SAY #%csr115_s57098%
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN EXTERN ~bdjaheir~ %csr115_bdjaheir_106%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN EXTERN ~bdjaheir~ 12
END

IF %csr115_weight_csr115_54% ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
Global("bd_mdd206","global",1)
~ THEN BEGIN %csr115_kh_190%
  SAY #%csr115_s42374%
  IF ~~ THEN DO ~SetGlobal("bd_mdd206","global",2)
~ EXTERN ~bdjaheir~ 45
END

IF %csr115_weight_csr115_55% ~~ THEN BEGIN %csr115_kh_234%
  SAY #%csr115_s50709%
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s50710%  GOTO %csr115_khalij_273%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s50710%  GOTO %csr115_kh_235%
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s50711%  GOTO %csr115_khalij_273%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s50711%  GOTO %csr115_kh_235%
  IF ~  OR(2)
Global("csr_kh_carry","GLOBAL",1)
Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s50712%  GOTO %csr115_khalij_273%
  IF ~  !Global("csr_kh_carry","GLOBAL",1)
!Global("csr_kh_fort","GLOBAL",1)
~ THEN REPLY #%csr115_s50712%  GOTO %csr115_kh_235%
END

IF %csr115_weight_csr115_56% ~~ THEN BEGIN %csr115_khalij_272%
  SAY @4
  IF ~~ THEN EXTERN ~bdbfort~ %csr115_bdbfort_15%
END

IF %csr115_weight_csr115_57% ~~ THEN BEGIN %csr115_khalij_273%
  SAY @40
  IF ~~ THEN REPLY #%csr115_s50715%  GOTO %csr115_kh_236%
  IF ~~ THEN REPLY #%csr115_s50716%  GOTO %csr115_kh_236%
  IF ~~ THEN REPLY #%csr115_s50717%  GOTO %csr115_kh_236%
END

IF %csr115_weight_csr115_58% ~~ THEN BEGIN %csr115_khalij_274%
  SAY @46
  IF ~~ THEN EXTERN ~bdneera~ 64
END

END

REPLACE ~csr115ad~
IF %csr115_weight_csr115_59% ~~ THEN BEGIN 0
  SAY #%csr115_s46545%
  IF ~~ THEN EXTERN ~bdjegg~ 23
END

IF %csr115_weight_csr115_60% ~~ THEN BEGIN 1
  SAY #%csr115_s46547%
  IF ~~ THEN REPLY #%csr115_s46548%  DO ~StartCutSceneMode()
ClearAllActions()
StartCutSceneEx("bdc205r",FALSE)
~ EXIT
  IF ~~ THEN REPLY #%csr115_s46549%  DO ~StartCutSceneMode()
ClearAllActions()
StartCutSceneEx("bdc205r",FALSE)
~ EXIT
  IF ~~ THEN REPLY #%csr115_s46550%  DO ~StartCutSceneMode()
ClearAllActions()
StartCutSceneEx("bdc205r",FALSE)
~ EXIT
END

END

SET_WEIGHT ~BDBFORT~ %csr115_bdbfort_13% #-10
SET_WEIGHT ~BDBFORT~ %csr115_bdbfort_16% #-9
SET_WEIGHT ~BDBFORT~ %csr115_bdbfort_17% #-8
