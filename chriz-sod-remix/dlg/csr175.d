// The two owned return states. Other celebration states remain untouched.
REPLACE ~csrcele~
IF ~Global("CSR_KORL_RET","GLOBAL",1)~ THEN BEGIN 1
  SAY @18012
  IF ~~ THEN REPLY @18013 GOTO 2
  IF ~~ THEN REPLY @18014 GOTO 2
END

IF ~~ THEN BEGIN 2
  SAY @18015
  IF ~~ THEN DO ~SetGlobal("CSR_KORL_RET","GLOBAL",2)
AddXPObject(Player1,22000)
AddXPObject(Player2,22000)
AddXPObject(Player3,22000)
AddXPObject(Player4,22000)
AddXPObject(Player5,22000)
AddXPObject(Player6,22000)
DestroySelf()~ EXIT
END
END
