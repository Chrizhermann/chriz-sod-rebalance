// Missing party-dialogue segment: preserve the native personal quest as well.
REPLACE ~%csr115_kh_j%~
IF %csr115_weight_csr115_party_fallback_0% ~~ THEN BEGIN %csr115_kh_177%
  SAY #%csr115_s57092%
  IF ~~ THEN EXTERN ~bdjaheir~ 12
END

IF %csr115_weight_csr115_party_fallback_1% ~~ THEN BEGIN %csr115_kh_178%
  SAY #%csr115_s57098%
  IF ~~ THEN EXTERN ~bdjaheir~ 12
END

IF %csr115_weight_csr115_party_fallback_2% ~  Global("bd_mdd206","global",1)
~ THEN BEGIN %csr115_kh_190%
  SAY #%csr115_s42374%
  IF ~~ THEN DO ~SetGlobal("bd_mdd206","global",2)
~ EXTERN ~bdjaheir~ 45
END

IF %csr115_weight_csr115_party_fallback_3% ~~ THEN BEGIN %csr115_kh_199%
  SAY #%csr115_s36445%
  IF ~~ THEN EXTERN ~bdneera~ 64
END

IF %csr115_weight_csr115_party_fallback_4% ~~ THEN BEGIN %csr115_kh_201%
  SAY #%csr115_s36878%
  IF ~  Global("bd_charname_revealed","global",0)
NumInPartyGT(2)
~ THEN REPLY #%csr115_s36879%  EXTERN ~bdbarghe~ 37
  IF ~  Global("bd_charname_revealed","global",1)
NumInPartyGT(2)
~ THEN REPLY #%csr115_s36879%  EXTERN ~bdbarghe~ 32
  IF ~  Global("bd_charname_revealed","global",0)
NumInPartyLT(3)
~ THEN REPLY #%csr115_s65945%  EXTERN ~bdbarghe~ 37
  IF ~  Global("bd_charname_revealed","global",1)
NumInPartyLT(3)
~ THEN REPLY #%csr115_s65945%  EXTERN ~bdbarghe~ 32
  IF ~~ THEN REPLY #%csr115_s36880%  EXTERN ~bdbarghe~ 30
END

IF %csr115_weight_csr115_party_fallback_5% ~  !Dead("JAHEIRA")
Global("BD_SDD223","GLOBAL",0)
GlobalLT("chapter","global",%csr115_ch11%)
GlobalGT("bd_plot","global",250)
~ THEN BEGIN %csr115_kh_233%
  SAY #%csr115_s50705%
  IF ~~ THEN REPLY #%csr115_s50706%  GOTO %csr115_kh_234%
  IF ~~ THEN REPLY #%csr115_s50707%  GOTO %csr115_kh_234%
  IF ~~ THEN REPLY #%csr115_s50708%  GOTO %csr115_kh_234%
END

IF %csr115_weight_csr115_party_fallback_6% ~~ THEN BEGIN %csr115_kh_234%
  SAY #%csr115_s50709%
  IF ~~ THEN REPLY #%csr115_s50710%  GOTO %csr115_kh_235%
  IF ~~ THEN REPLY #%csr115_s50711%  GOTO %csr115_kh_235%
  IF ~~ THEN REPLY #%csr115_s50712%  GOTO %csr115_kh_235%
END

IF %csr115_weight_csr115_party_fallback_7% ~~ THEN BEGIN %csr115_kh_235%
  SAY #%csr115_s50714%
  IF ~~ THEN REPLY #%csr115_s50715%  GOTO %csr115_kh_236%
  IF ~~ THEN REPLY #%csr115_s50716%  GOTO %csr115_kh_236%
  IF ~~ THEN REPLY #%csr115_s50717%  GOTO %csr115_kh_236%
END

IF %csr115_weight_csr115_party_fallback_8% ~~ THEN BEGIN %csr115_kh_236%
  SAY #%csr115_s50719%
  IF ~~ THEN REPLY #%csr115_s50720%  GOTO %csr115_kh_237%
  IF ~  !Class(Player1,SHAMAN)
OR(2)
Class(Player1,RANGER_ALL)
Class(Player1,DRUID_ALL)
~ THEN REPLY #%csr115_s50718%  GOTO %csr115_kh_237%
  IF ~~ THEN REPLY #%csr115_s50721%  GOTO %csr115_kh_237%
  IF ~~ THEN REPLY #%csr115_s50722%  GOTO %csr115_kh_237%
END

IF %csr115_weight_csr115_party_fallback_9% ~~ THEN BEGIN %csr115_kh_237%
  SAY #%csr115_s50724%
  IF ~~ THEN GOTO %csr115_kh_238%
END

IF %csr115_weight_csr115_party_fallback_10% ~~ THEN BEGIN %csr115_kh_238%
  SAY #%csr115_s50725%
  IF ~~ THEN REPLY #%csr115_s50726%  GOTO %csr115_kh_239%
  IF ~~ THEN REPLY #%csr115_s50727%  GOTO %csr115_kh_239%
  IF ~~ THEN REPLY #%csr115_s50728%  GOTO %csr115_kh_240%
END

IF %csr115_weight_csr115_party_fallback_11% ~~ THEN BEGIN %csr115_kh_239%
  SAY #%csr115_s50729%
  IF ~~ THEN DO ~SetGlobal("BD_SDD223","GLOBAL",1)
~ UNSOLVED_JOURNAL #%csr115_s56833%  EXIT
END

IF %csr115_weight_csr115_party_fallback_12% ~~ THEN BEGIN %csr115_kh_240%
  SAY #%csr115_s58652%
  IF ~~ THEN DO ~SetGlobal("BD_SDD223","GLOBAL",1)
~ UNSOLVED_JOURNAL #%csr115_s56833%  EXIT
END

IF %csr115_weight_csr115_party_fallback_13% ~  Global("BD_SDD223","GLOBAL",1)
PartyHasItem("BDSILK01")
~ THEN BEGIN %csr115_kh_241%
  SAY #%csr115_s50736%
  IF ~~ THEN REPLY #%csr115_s50737%  GOTO %csr115_kh_242%
  IF ~~ THEN REPLY #%csr115_s50738%  GOTO %csr115_kh_242%
  IF ~~ THEN REPLY #%csr115_s50739%  GOTO %csr115_kh_243%
END

IF %csr115_weight_csr115_party_fallback_14% ~~ THEN BEGIN %csr115_kh_242%
  SAY #%csr115_s50740%
  IF ~~ THEN DO ~SetGlobal("BD_SDD223","GLOBAL",2)
SetGlobalTimer("bd_sdd223_timer","global",ONE_HOUR)
TakePartyItem("BDSILK01")
DestroyItem("BDSILK01")
AddJournalEntry(%csr115_s56838%,QUEST)
~ EXIT
END

IF %csr115_weight_csr115_party_fallback_15% ~~ THEN BEGIN %csr115_kh_243%
  SAY #%csr115_s50741%
  IF ~~ THEN DO ~SetGlobal("BD_SDD223","GLOBAL",2)
SetGlobalTimer("bd_sdd223_timer","global",ONE_HOUR)
TakePartyItem("BDSILK01")
DestroyItem("BDSILK01")
AddJournalEntry(%csr115_s56838%,QUEST)
~ EXIT
END

IF %csr115_weight_csr115_party_fallback_16% ~  !Dead("JAHEIRA")
Global("BD_SDD223","GLOBAL",2)
GlobalLT("chapter","global",%csr115_ch11%)
GlobalGT("bd_plot","global",304)
~ THEN BEGIN %csr115_kh_244%
  SAY #%csr115_s50742%
  IF ~~ THEN REPLY #%csr115_s50743%  DO ~SetGlobal("BD_SDD223","GLOBAL",3)
~ GOTO %csr115_kh_246%
  IF ~~ THEN REPLY #%csr115_s50744%  DO ~SetGlobal("BD_SDD223","GLOBAL",3)
~ GOTO %csr115_kh_245%
  IF ~~ THEN REPLY #%csr115_s50745%  DO ~SetGlobal("BD_SDD223","GLOBAL",3)
~ GOTO %csr115_kh_246%
END

IF %csr115_weight_csr115_party_fallback_17% ~~ THEN BEGIN %csr115_kh_245%
  SAY #%csr115_s50746%
  IF ~~ THEN GOTO %csr115_kh_246%
END

IF %csr115_weight_csr115_party_fallback_18% ~~ THEN BEGIN %csr115_kh_246%
  SAY #%csr115_s50752%
  IF ~~ THEN REPLY #%csr115_s50753%  GOTO %csr115_kh_247%
  IF ~~ THEN REPLY #%csr115_s50754%  GOTO %csr115_kh_247%
  IF ~~ THEN REPLY #%csr115_s50755%  GOTO %csr115_kh_247%
END

IF %csr115_weight_csr115_party_fallback_19% ~~ THEN BEGIN %csr115_kh_247%
  SAY #%csr115_s50756%
  IF ~~ THEN GOTO %csr115_kh_248%
END

IF %csr115_weight_csr115_party_fallback_20% ~~ THEN BEGIN %csr115_kh_248%
  SAY #%csr115_s50758%
  IF ~~ THEN REPLY #%csr115_s50759%  GOTO %csr115_kh_249%
  IF ~~ THEN REPLY #%csr115_s50760%  GOTO %csr115_kh_249%
  IF ~~ THEN REPLY #%csr115_s50761%  GOTO %csr115_kh_249%
END

IF %csr115_weight_csr115_party_fallback_21% ~~ THEN BEGIN %csr115_kh_249%
  SAY #%csr115_s50762%
  IF ~~ THEN REPLY #%csr115_s50763%  GOTO %csr115_kh_256%
  IF ~~ THEN REPLY #%csr115_s50764%  GOTO %csr115_kh_256%
  IF ~  PartyHasItem("misc33")
~ THEN REPLY #%csr115_s50765%  GOTO %csr115_kh_250%
  IF ~~ THEN REPLY #%csr115_s50766%  GOTO %csr115_kh_256%
END

IF %csr115_weight_csr115_party_fallback_22% ~  !Dead("JAHEIRA")
Global("BD_SDD223","GLOBAL",4)
Global("BD_SDD223_MAY_I","LOCALS",1)
GlobalLT("chapter","global",%csr115_ch13%)
HasItem("MISC33",Myself)
~ THEN BEGIN %csr115_kh_250%
  SAY #%csr115_s50767%
  IF ~  Alignment(LastTalkedToBy,MASK_EVIL)
~ THEN REPLY #%csr115_s50768%  DO ~TakePartyItemNum("misc33",1)
DestroyItem("misc33")
~ GOTO %csr115_kh_255%
  IF ~  !Alignment(LastTalkedToBy,MASK_EVIL)
~ THEN REPLY #%csr115_s50757%  DO ~TakePartyItemNum("misc33",1)
DestroyItem("misc33")
~ GOTO %csr115_kh_255%
  IF ~~ THEN REPLY #%csr115_s50769%  DO ~SetGlobal("BD_SDD223","GLOBAL",4)
~ GOTO %csr115_kh_251%
  IF ~~ THEN REPLY #%csr115_s50770%  DO ~SetGlobal("BD_SDD223","GLOBAL",4)
~ GOTO %csr115_kh_254%
END

IF %csr115_weight_csr115_party_fallback_23% ~~ THEN BEGIN %csr115_kh_251%
  SAY #%csr115_s50771%
  IF ~~ THEN REPLY #%csr115_s50772%  DO ~TakePartyItemNum("misc33",1)
DestroyItem("misc33")
~ GOTO %csr115_kh_255%
  IF ~  !CheckStatGT(LastTalkedToBy,14,CHR)
~ THEN REPLY #%csr115_s50773%  GOTO %csr115_kh_252%
  IF ~  CheckStatGT(LastTalkedToBy,14,CHR)
~ THEN REPLY #%csr115_s50773%  GOTO %csr115_kh_253%
  IF ~  !CheckStatGT(LastTalkedToBy,11,CHR)
~ THEN REPLY #%csr115_s50774%  GOTO %csr115_kh_252%
  IF ~  CheckStatGT(LastTalkedToBy,11,CHR)
~ THEN REPLY #%csr115_s50774%  GOTO %csr115_kh_253%
END

IF %csr115_weight_csr115_party_fallback_24% ~~ THEN BEGIN %csr115_kh_252%
  SAY #%csr115_s50775%
  IF ~~ THEN DO ~SetGlobal("BD_SDD223","GLOBAL",5)
~ SOLVED_JOURNAL #%csr115_s50750%  EXIT
END

IF %csr115_weight_csr115_party_fallback_25% ~~ THEN BEGIN %csr115_kh_253%
  SAY #%csr115_s50751%
  IF ~~ THEN DO ~GiveGoldForce(200)
TakePartyItemNum("misc33",1)
DestroyItem("misc33")
~ GOTO %csr115_kh_255%
END

IF %csr115_weight_csr115_party_fallback_26% ~~ THEN BEGIN %csr115_kh_254%
  SAY #%csr115_s50776%
  IF ~~ THEN EXIT
END

IF %csr115_weight_csr115_party_fallback_27% ~~ THEN BEGIN %csr115_kh_255%
  SAY #%csr115_s50777%
  IF ~~ THEN DO ~SetGlobal("BD_SDD223","GLOBAL",6)
SetGlobalTimer("bd_sdd223_end_timer","global",SIX_HOURS)
~ SOLVED_JOURNAL #%csr115_s56840%  EXIT
END

IF %csr115_weight_csr115_party_fallback_28% ~~ THEN BEGIN %csr115_kh_256%
  SAY #%csr115_s50778%
  IF ~~ THEN UNSOLVED_JOURNAL #%csr115_s56839%  EXIT
END

IF %csr115_weight_csr115_party_fallback_29% ~  !Dead("JAHEIRA")
OR(2)
Global("BD_SDD223","GLOBAL",3)
Global("BD_SDD223","GLOBAL",4)
GlobalLT("chapter","global",%csr115_ch13%)
PartyHasItem("MISC33")
~ THEN BEGIN %csr115_kh_257%
  SAY #%csr115_s50779%
  IF ~~ THEN REPLY #%csr115_s51905%  GOTO %csr115_kh_250%
END

END
