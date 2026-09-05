// Component 290 standalone endpoint: use SoD's native campaign termination
// order directly from Dazzo, without any EET resource dependency.
ALTER_TRANS ~BDDAZZO~ BEGIN 2 3 END BEGIN 0 END BEGIN
  ACTION ~SetGlobal("CSR_ENDING_USED","GLOBAL",1)
EraseJournalEntry(66908)
StartCutSceneMode()
FadeToColor([1.0],0)
EndCutSceneMode()
ContinueGame(FALSE)
EndCredits()~
  EPILOGUE ~EXIT~
END
