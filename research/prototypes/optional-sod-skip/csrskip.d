// Prototype only: not referenced by the released/public installer.
// Choice 0 = unresolved; 1 = confirmed skip; 2 = confirmed play SoD.
BEGIN ~csrskip~

IF ~Global("CSR_SKIP_CHOICE","GLOBAL",0)~ THEN BEGIN QUESTION
  SAY @0
  IF ~~ THEN REPLY @1 GOTO CONFIRM_SKIP
  IF ~~ THEN REPLY @2 GOTO CONFIRM_PLAY
END

// False entry triggers prevent these GOTO-only states becoming dialog starts.
IF ~False()~ THEN BEGIN CONFIRM_SKIP
  SAY @3
  IF ~~ THEN REPLY @1 DO ~SetGlobal("CSR_SKIP_CHOICE","GLOBAL",1)~ EXIT
  IF ~~ THEN REPLY @2 GOTO QUESTION
END

IF ~False()~ THEN BEGIN CONFIRM_PLAY
  SAY @4
  IF ~~ THEN REPLY @1 DO ~SetGlobal("CSR_SKIP_CHOICE","GLOBAL",2)~ EXIT
  IF ~~ THEN REPLY @2 GOTO QUESTION
END
