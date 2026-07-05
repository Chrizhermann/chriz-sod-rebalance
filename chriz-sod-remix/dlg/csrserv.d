// chriz-sod-remix component 150 — csrserv, the palace servant.
// NEW dialog resref on a BDSERV.cre clone. Never reuse vanilla BDSERV.dlg:
// its state 2 triggers on bd_plot=54 alone and its exits set bd_plot=55,
// which would bypass the Skie enlistment scene (docs/research/11a §3D).
// State triggers are mutually exclusive on BD_PLOT, so start-state
// selection order never matters.

BEGIN ~csrserv~

// Role (b): wake-for-council. She is spawned by the patched BD0103 night
// block at bd_plot=51 and force-talks Player1 (her StartDialogNoSet is
// what ends the night block's cutscene mode). EscapeArea() on the exit so
// she walks off once her job is done.
IF ~Global("BD_PLOT","GLOBAL",51)~ THEN BEGIN wake
  SAY @15003
  IF ~~ THEN REPLY @15004 DO ~EscapeArea()~ EXIT
END

// Role (a): the bedtime offer. Saying yes sets CSR_BEDTIME, which is the
// AND-gate the patched night block waits for.
IF ~GlobalLT("BD_PLOT","GLOBAL",51)
Global("CSR_BEDTIME","GLOBAL",0)~ THEN BEGIN offer
  SAY @15001
  IF ~~ THEN REPLY @15002 DO ~SetGlobal("CSR_BEDTIME","GLOBAL",1)~ EXIT
  IF ~~ THEN REPLY @15005 EXIT
END

// Re-clicked in the moment between "yes" and the night block firing.
IF ~GlobalLT("BD_PLOT","GLOBAL",51)
Global("CSR_BEDTIME","GLOBAL",1)~ THEN BEGIN goodnight
  SAY @15006
  IF ~~ THEN EXIT
END

// Clicked after the council advanced bd_plot past 51 (she is normally
// already gone via EscapeArea by then) — generic fallback so the engine
// never reports "has nothing to say to you".
IF ~GlobalGT("BD_PLOT","GLOBAL",51)~ THEN BEGIN after
  SAY @15007
  IF ~~ THEN EXIT
END
