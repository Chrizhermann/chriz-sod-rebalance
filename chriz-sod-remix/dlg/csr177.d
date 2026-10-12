// Share the existing once-only payment global with the first-evening beat.
// Appending replies leaves the forced council and departure speech untouched.
EXTEND_BOTTOM ~BDLIIA~ 13
  IF ~Dead("BDKORLAS")
GlobalLT("CSR_KORL_RET","GLOBAL",2)
Global("bd_plot_003","BD0102",2)~ THEN REPLY @17701 GOTO csr177_report
END

EXTEND_BOTTOM ~BDLIIA~ 33
  IF ~Dead("BDKORLAS")
GlobalLT("CSR_KORL_RET","GLOBAL",2)
Global("bd_plot_003","BD0102",2)~ THEN REPLY @17701 GOTO csr177_report
END

ALTER_TRANS ~BDLIIA~ BEGIN 33 END BEGIN 0 END BEGIN
  ~REPLY~ ~@17703~
END

APPEND ~BDLIIA~
IF ~~ THEN BEGIN csr177_report
  SAY @17702
  IF ~~ THEN DO ~SetGlobal("CSR_KORL_RET","GLOBAL",2)
SetGlobal("CSR177_REPORT","GLOBAL",1)
EraseJournalEntry(%csr177_done%)
EraseJournalEntry(%csr177_pending%)
AddJournalEntry(%csr177_complete%,QUEST_DONE)
AddXPObject(Player1,22000)
AddXPObject(Player2,22000)
AddXPObject(Player3,22000)
AddXPObject(Player4,22000)
AddXPObject(Player5,22000)
AddXPObject(Player6,22000)~ EXIT
END
END

// The celebration's temporary Liia still disappears as before, after payment
// and journal completion. Normal hall Liia above is never destroyed.
ALTER_TRANS ~csrcele~ BEGIN 2 END BEGIN 0 END BEGIN
  ACTION ~SetGlobal("CSR_KORL_RET","GLOBAL",2)
SetGlobal("CSR177_REPORT","GLOBAL",1)
EraseJournalEntry(%csr177_done%)
EraseJournalEntry(%csr177_pending%)
AddJournalEntry(%csr177_complete%,QUEST_DONE)
AddXPObject(Player1,22000)
AddXPObject(Player2,22000)
AddXPObject(Player3,22000)
AddXPObject(Player4,22000)
AddXPObject(Player5,22000)
AddXPObject(Player6,22000)
DestroySelf()~
END
