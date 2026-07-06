// chriz-sod-remix component 160 — Imoen's SoD join dialog.
// Carried pre-join by the imported IMOEN2 instance (BD0120 strip
// patch, SetDialogue) or by csrimo.cre (install-time field); the
// patched BDDIALOG.2DA IMOEN2 row keeps it active through
// join/dismiss for the whole SoD campaign. Vanilla BDIMOEN.dlg is
// parked at bd_001_plot=10 by component 150 and never answers, so
// these states key ONLY on our own CSR_IMOEN_JOINED global —
// no vanilla state can hijack (design 01-prologue §5).

BEGIN csrimoen

// First meeting in the palace bedroom — not yet joined in SoD.
IF ~Global("CSR_IMOEN_JOINED","GLOBAL",0)~ THEN BEGIN greet
  SAY @16001
  // Join is NOT gated on NumInPartyLT(6): SoD recruiters keep the join option
  // visible even with a full party and let the engine pop the reform-party
  // screen on JoinParty() (matches every other companion; user, 2026-07-06).
  IF ~~ THEN REPLY @16002 DO ~SetGlobal("CSR_IMOEN_JOINED","GLOBAL",1) JoinParty()~ EXIT
  IF ~~ THEN REPLY @16003 GOTO stay
END

// Declined — she waits (reachable only via transition, no trigger).
IF ~~ THEN BEGIN stay
  SAY @16004
  IF ~~ THEN EXIT
END

// Dismissed after having joined — always re-recruitable.
IF ~Global("CSR_IMOEN_JOINED","GLOBAL",1) !InParty(Myself)~ THEN BEGIN rejoin
  SAY @16005
  IF ~~ THEN REPLY @16006 DO ~JoinParty()~ EXIT
  IF ~~ THEN REPLY @16007 EXIT
END

// In-party small talk (the patched BDDIALOG row keeps csrimoen as
// her joined dialog, so clicking her must never be a dead end).
IF ~Global("CSR_IMOEN_JOINED","GLOBAL",1) InParty(Myself)~ THEN BEGIN chat
  SAY @16008
  IF ~~ THEN EXIT
END
