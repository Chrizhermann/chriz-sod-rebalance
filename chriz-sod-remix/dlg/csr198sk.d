// Early palace Skie. #198 assigns this to the one selected living actor,
// whether imported SKIE or palace BDSKIE; no new copy is created by dialogue.
// Council completion, not the clock or a normal preparation rest, selects
// the crusade wording. Keep the separate condolence acknowledgement from #197.
BEGIN ~CSR198SK~

IF ~!InParty(Myself)
OR(2)
  GlobalGT("bd_joined","LOCALS",0)
  Global("CSR198_JOINED","LOCALS",1)
~ THEN BEGIN rejoin
  SAY @8
  IF ~~ THEN REPLY @9 GOTO join
  IF ~~ THEN REPLY @10 EXIT
END

IF ~!InParty(Myself)
AreaCheck("BD0102")
Global("CSR_SKIE_PALACE","GLOBAL",0)
GlobalLT("bd_plot_003","BD0102",2)
~ THEN BEGIN meet_early
  SAY @0
  IF ~~ THEN REPLY @1 DO ~SetGlobal("CSR_SKIE_PALACE","GLOBAL",1)~ GOTO condolences_early
  IF ~~ THEN REPLY @12 DO ~SetGlobal("CSR_SKIE_PALACE","GLOBAL",1)~ GOTO ask_early
END

IF ~!InParty(Myself)
AreaCheck("BD0102")
Global("CSR_SKIE_PALACE","GLOBAL",0)
GlobalGT("bd_plot_003","BD0102",1)
~ THEN BEGIN meet_after_council
  SAY @0
  IF ~~ THEN REPLY @1 DO ~SetGlobal("CSR_SKIE_PALACE","GLOBAL",1)~ GOTO condolences_after_council
  IF ~~ THEN REPLY @2 DO ~SetGlobal("CSR_SKIE_PALACE","GLOBAL",1)~ GOTO ask_after_council
END

// Also covers a declined #197 meeting in an existing save. The original
// CSR_SKIE_PALACE marker remains authoritative; no repeated grief exchange.
IF ~!InParty(Myself)~ THEN BEGIN again
  SAY @8
  IF ~~ THEN REPLY @9 GOTO join
  IF ~~ THEN REPLY @10 EXIT
END

IF ~InParty(Myself)~ THEN BEGIN in_party
  SAY @17
  IF ~~ THEN EXIT
END

IF ~~ THEN BEGIN condolences_early
  SAY @14
  IF ~~ THEN REPLY @15 GOTO join
  IF ~~ THEN REPLY @16 GOTO stay
END

IF ~~ THEN BEGIN ask_early
  SAY @13
  IF ~~ THEN REPLY @15 GOTO join
  IF ~~ THEN REPLY @16 GOTO stay
END

IF ~~ THEN BEGIN condolences_after_council
  SAY @11
  IF ~~ THEN REPLY @4 GOTO join
  IF ~~ THEN REPLY @5 GOTO stay
END

IF ~~ THEN BEGIN ask_after_council
  SAY @3
  IF ~~ THEN REPLY @4 GOTO join
  IF ~~ THEN REPLY @5 GOTO stay
END

IF ~~ THEN BEGIN join
  SAY @6
  IF ~~ THEN DO ~SetGlobal("CSR_SKIE_PALACE","GLOBAL",2)
SetGlobal("bd_joined","LOCALS",1)
SetGlobal("CSR198_SKIE_JOINED","GLOBAL",1)
SetGlobal("CSR198_JOINED","LOCALS",1)
JoinParty()~ EXIT
END

IF ~~ THEN BEGIN stay
  SAY @7
  IF ~~ THEN EXIT
END
