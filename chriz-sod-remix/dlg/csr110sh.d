// The remix owns both endpoints, so changed native actions cannot kill or
// refuse the returning companion. Existing localized wording is carried over.
BEGIN ~CSR110SH~
IF ~~ THEN BEGIN 0
  SAY #%csr110_join_say%
  IF ~~ THEN DO ~JoinParty()~ EXIT
END
IF ~~ THEN BEGIN 1
  SAY #%csr110_wait_say%
  IF ~~ THEN EXIT
END

%csr110_verb% ~BDSHARTE~
IF WEIGHT #-1 ~%csr110_field_condition%~ THEN BEGIN %csr110_label%
  SAY #%csr110_sharteel_say%
  IF ~~ THEN REPLY #%csr110_yes% EXTERN ~CSR110SH~ 0
  IF ~~ THEN REPLY #%csr110_no% EXTERN ~CSR110SH~ 1
END
END
