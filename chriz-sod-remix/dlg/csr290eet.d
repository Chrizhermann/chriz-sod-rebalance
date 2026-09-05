// Component 290 EET endpoint: invoke the guarded clone of the currently
// installed EET transition carrier from the playable BD4300 celebration.
ALTER_TRANS ~BDDAZZO~ BEGIN 2 3 END BEGIN 0 END BEGIN
  ACTION ~SetGlobal("CSR_ENDING_USED","GLOBAL",1)
EraseJournalEntry(266908)
StartCutSceneMode()
FadeToColor([1.0],0)
EndCutSceneMode()
SetCutSceneLite(TRUE)
CreateCreatureObject("CSRETBGT",Player1,0,0,0)~
  EPILOGUE ~EXIT~
END
