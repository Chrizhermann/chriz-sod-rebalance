// Share the existing once-only payment global with the first-evening beat.
// Appending replies leaves the forced council and departure speech untouched.
%csr177_routes%

ALTER_TRANS ~BDLIIA~ BEGIN 33 END BEGIN %csr177_farewell% END BEGIN
  ~REPLY~ ~@17703~
END

%csr177_report_verb% ~BDLIIA~
IF ~~ THEN BEGIN %csr177_report_label%
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
