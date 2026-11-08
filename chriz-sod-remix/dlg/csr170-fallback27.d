REPLACE ~BDKORLAS~
IF %csr170_weight27% ~~ THEN BEGIN 27
  SAY @17026
  IF ~~ THEN DO ~AddJournalEntry(%csr170_journal%,QUEST)
SetGlobal("BD_SPAWN_KORLASZ","BD0116",2)
Enemy()
~ EXIT
END
END
