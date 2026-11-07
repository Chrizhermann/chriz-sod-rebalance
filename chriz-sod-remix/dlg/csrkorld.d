// Own the two reply sets and all four new lines. Existing interjections in
// states 25 and 27 remain; missing states receive the native fallback.
REPLACE ~BDKORLAS~
IF %csr170_weight24% ~  AreaCheck("BD0116")
~ THEN BEGIN 24
  SAY @17020
  IF ~~ THEN REPLY #%csr170_reply1%  GOTO 25
  IF ~  IsValidForPartyDialogue("Safana")
~ THEN REPLY #%csr170_reply2%  EXTERN ~SAFANJ~ 107
  IF ~  !IsValidForPartyDialogue("Safana")
~ THEN REPLY #%csr170_reply2%  GOTO 26
  IF ~~ THEN REPLY #%csr170_reply3%  GOTO 27
END

IF %csr170_weight26% ~~ THEN BEGIN 26
  SAY @17022
  IF ~~ THEN REPLY @17023  GOTO 27
  IF ~  IsValidForPartyDialogue("Safana")
~ THEN REPLY @17024  EXTERN ~SAFANJ~ 108
  IF ~  !IsValidForPartyDialogue("Safana")
~ THEN REPLY @17024  GOTO 27
  IF ~~ THEN REPLY @17025  GOTO 27
END
END
REPLACE_SAY ~BDKORLAS~ 25 @17021
REPLACE_SAY ~BDKORLAS~ 27 @17026
