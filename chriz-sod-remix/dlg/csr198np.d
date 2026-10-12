BEGIN ~%csr198_dialogue%~

IF ~!InParty(Myself) Global("CSR198_JOINED","LOCALS",0)~ THEN BEGIN first
  SAY @%csr198_greeting%
  IF ~~ THEN REPLY @1 GOTO join
  IF ~~ THEN REPLY @2 EXIT
END

IF ~!InParty(Myself)~ THEN BEGIN again
  SAY @%csr198_rejoin%
  IF ~~ THEN REPLY @1 GOTO join
  IF ~~ THEN REPLY @2 EXIT
END

IF ~InParty(Myself)~ THEN BEGIN in_party
  SAY @3
  IF ~~ THEN EXIT
END

IF ~~ THEN BEGIN join
  SAY @4
  %csr198_release_transition%
  IF ~%csr198_join_guard%~ THEN DO ~%csr198_join_actions%~ EXIT
END
