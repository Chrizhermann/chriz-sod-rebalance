// #120 owns the farewell state and removes its hooded-man reply.
REPLACE ~BDIMOEN~
IF %csr120_weight% ~  Global("BD_MDD007","BD0103",1)
~ THEN BEGIN 67
  SAY #%csr120_s35301%
  IF ~~ THEN REPLY #%csr120_s35302%  DO ~SetGlobal("BD_MDD007","BD0103",2)
~ GOTO 74
  IF ~  False()
~ THEN REPLY #%csr120_s55721%  DO ~SetGlobal("BD_MDD007","BD0103",2)
~ GOTO 68
  IF ~~ THEN REPLY #%csr120_s35304%  DO ~SetGlobal("BD_MDD007","BD0103",2)
~ GOTO 76
END
END
