// chriz-sod-remix component 170 — rewrite Korlasz's BD0116 breakout opener.
// Vanilla BDKORLAS state 24 (#245641, voiced [BD45641]) has her greet the PC
// as "the one who delivered me to this hell" — only coherent because vanilla
// makes you personally catch her in the Korlasz dungeon. The remix skips the
// dungeon (she surrendered to the Flaming Fist), so the line is rewritten to
// blame the PC as Sarevok's killer instead. Reproduced state keeps all four
// vanilla transitions verbatim (the replies already fit); only the SAY line
// changes, and to a fresh unvoiced strref (@17020) so the mismatched VO is
// dropped. Reply strrefs are this-install (EET) values — stable here; a
// distributable build would resolve them at install time.
REPLACE ~BDKORLAS~
IF ~AreaCheck("BD0116")~ THEN BEGIN 24
  SAY @17020
  IF ~~ THEN REPLY #245642 GOTO 25
  IF ~IsValidForPartyDialogue("Safana")~ THEN REPLY #245643 EXTERN ~SAFANJ~ 107
  IF ~!IsValidForPartyDialogue("Safana")~ THEN REPLY #245643 GOTO 26
  IF ~~ THEN REPLY #245644 GOTO 27
END
END
