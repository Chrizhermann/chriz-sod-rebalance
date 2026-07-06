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

// States 25-27 polish (user 2026-07-07, BG2 villain register - "Sarevok and
// Irenicus are peak writing"; all new lines unvoiced, mismatched VO dropped).
//
// State 25 keeps the vanilla "punish/murder" vocabulary on purpose: Minsc's
// interjection (MINSCJ 909, "We will see who punish murders who for murder
// punishment-right now!") plays off exactly those words and replaces her state
// 26/27 entirely when he's in the party (it carries the same fight-start
// actions). State 27's SAY swap leaves its action block (journal 261626,
// BD_SPAWN_KORLASZ=2, Enemy()) untouched - REPLACE_SAY changes text only.
REPLACE_SAY ~BDKORLAS~ 25 @17021
REPLACE_SAY ~BDKORLAS~ 27 @17026

// State 26 needs its REPLIES rewritten too (the vanilla ones answer her cut
// "tortured in private" melodrama, which made no sense mid-jailbreak - she is
// standing free, armed, with her crew). Full state REPLACE, transition TARGETS
// identical to vanilla: r1 -> 27, r2 -> SAFANJ 108 with Safana (her "That makes
// two of us." tracks the kept I-never-thought-of-you sentiment) / -> 27 without,
// r3 -> 27.
REPLACE ~BDKORLAS~
IF ~~ THEN BEGIN 26
  SAY @17022
  IF ~~ THEN REPLY @17023 GOTO 27
  IF ~IsValidForPartyDialogue("Safana")~ THEN REPLY @17024 EXTERN ~SAFANJ~ 108
  IF ~!IsValidForPartyDialogue("Safana")~ THEN REPLY @17024 GOTO 27
  IF ~~ THEN REPLY @17025 GOTO 27
END
END
