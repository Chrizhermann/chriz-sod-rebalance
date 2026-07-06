// chriz-sod-remix component 180 -- click-dialogs for the celebration guests.
// BG1-register one-liners (user style rule): nobles simply congratulate, the
// Flaming Fist keep watch. Random pick per click; the last state of each dialog
// is trigger-less so state selection can never come up empty (vanilla commoner
// pattern - independent RandomNum rolls may all miss).

BEGIN ~csrnob~

IF ~RandomNum(4,1)~ THEN BEGIN n1
  SAY @18030
  IF ~~ THEN EXIT
END

IF ~RandomNum(4,2)~ THEN BEGIN n2
  SAY @18031
  IF ~~ THEN EXIT
END

IF ~RandomNum(4,3)~ THEN BEGIN n3
  SAY @18032
  IF ~~ THEN EXIT
END

IF ~~ THEN BEGIN n4
  SAY @18033
  IF ~~ THEN EXIT
END

BEGIN ~csrffgd~

IF ~RandomNum(2,1)~ THEN BEGIN g1
  SAY @18034
  IF ~~ THEN EXIT
END

IF ~~ THEN BEGIN g2
  SAY @18035
  IF ~~ THEN EXIT
END
