// chriz-sod-remix component 150 — crusade-only war council + assassination
// text gates. All state/transition indices verified against the DEV-install
// decompiles 2026-07-06 (docs/research/11a §2 mapped the council chain; 11b
// list (b) mapped the city references; research's flat transition numbers
// were converted to the per-state indices ALTER_TRANS/ADD_TRANS_TRIGGER use).
// ADD_TRANS_TRIGGER appends (ANDs) — mod-added transitions in the same
// states are untouched. ALTER_TRANS EPILOGUE only re-points the target;
// reply text and any triggers stay.

// ============================================================
// A. Council re-points (11a §2-3: crusade council, zero new text)
// ============================================================

// Entry stays BDLIIA 9 ("Let us begin..."); its "Assassins tried to kill
// me this night" reply dies. Replies 0/2/3 (greeting + the two Entar
// intros) all funnel into BDELTAN 4 and survive.
ADD_TRANS_TRIGGER BDLIIA 9 ~False()~ DO 1  // #257840

// BDELTAN 4 ("What do you know of ... Caelar Argent?"): all three replies
// went to BDELTAN 1 (the assassin sun-brand). Re-point them to BDBELT 35
// (refugee/trade report) — precedent: BDENTAR 7 transitions there already.
// Orphans BDELTAN 1 / BDLIIA 10 / BDBELT 34 / BDENTAR 7 naturally.
ALTER_TRANS BDELTAN BEGIN 4 END BEGIN 0 1 2 END BEGIN
  EPILOGUE ~EXTERN BDBELT 35~
END

// BDBELT 38 (accept: "Excellent...") went to BDELTAN 9 (the parchment
// likeness beat). Re-point straight to BDBELT 39 ("You need not go
// alone...") — Corwin assignment continues unchanged.
ALTER_TRANS BDBELT BEGIN 38 END BEGIN 0 END BEGIN
  EPILOGUE ~GOTO 39~
END

// BDLIIA 11 (the pitch): both refusal replies led into the parchment
// persuasion chain (BDELTAN 7/6). Re-point to BDELTAN 8 ("Whenever you
// are ready to join it") — the dukes don't take no for an answer.
ALTER_TRANS BDLIIA BEGIN 11 END BEGIN 1 2 END BEGIN
  EPILOGUE ~EXTERN BDELTAN 8~
END

// BDBELT 40 reply #257853 "As I've already had one attempt on my life
// this night, I will permit it." sits on the KEPT council path (research
// 11b filed it under dies-with-cut, but state 40 survives the redesign).
// Gating it also orphans BDSCHAEL 21 ("keep further assassination
// attempts to a minimum"), its only consumer.
ADD_TRANS_TRIGGER BDBELT 40 ~False()~ DO 2

// BDBELT 41 closes the council with journal 266701, whose QUEST_DONE text
// says the assassins were sent by Caelar. Swap for the crusade-only line
// @15010 (same "The Siege of Dragonspear" title, same quest 266700 — the
// tpa registers the new strref in bgee.lua). Rest of the action is the
// verbatim dev text: bd_plot_003=2, journals 256387/259617, bdcut04.
ALTER_TRANS BDBELT BEGIN 41 END BEGIN 0 END BEGIN
  ACTION ~SetGlobal("bd_plot_003","bd0102",2)
AddJournalEntry(256387,INFO)
AddJournalEntry(259617,QUEST)
AddJournalEntry(@15010,QUEST_DONE)
ClearAllActions()
StartCutSceneMode()
StartCutSceneEx("bdcut04",FALSE)~
END

// ============================================================
// B. Cheap-now assassination references in SURVIVING content
//    (11b list (b); design 01-prologue §4 "reference cleanup")
// ============================================================

// --- Eltan, palace small talk (states 10-23 web survives) ---
ADD_TRANS_TRIGGER BDELTAN 11 ~False()~ DO 1  // #256007 "assassins roam the Ducal Palace"
ADD_TRANS_TRIGGER BDELTAN 13 ~False()~ DO 2  // #256017 "Caelar tried to kill me. She will answer for it."

// --- Liia, palace small talk ---
// #256030 "As well as an assassin's target can be". Her reply #256031
// ("how fares Imoen?") -> state 14's poison line stays: 11a parks BDLIIA
// 14-15 as later-pass text-patch candidates.
ADD_TRANS_TRIGGER BDLIIA 13 ~False()~ DO 0

// --- Belt, BD0100 apology web (GlobalLT(BD_plot,55) + AreaCheck(bd0100)) ---
// "What happened to Imoen falls on my shoulders..." State 42 is the only
// scripted entry; 43-46/55-58 are gated too per the research list (inert
// for chained states, but future-proof against weight tricks).
ADD_STATE_TRIGGER BDBELT 42 ~False()~
ADD_STATE_TRIGGER BDBELT 43 ~False()~
ADD_STATE_TRIGGER BDBELT 44 ~False()~
ADD_STATE_TRIGGER BDBELT 45 ~False()~
ADD_STATE_TRIGGER BDBELT 46 ~False()~
ADD_STATE_TRIGGER BDBELT 55 ~False()~
ADD_STATE_TRIGGER BDBELT 56 ~False()~
ADD_STATE_TRIGGER BDBELT 57 ~False()~
ADD_STATE_TRIGGER BDBELT 58 ~False()~

// --- Corwin, city escort ---
ADD_TRANS_TRIGGER BDSCHAEL 46 ~False()~ DO 1   // #267279 "As assassins attacked me in the Ducal Palace..." (return-prompt)
ADD_TRANS_TRIGGER BDSCHAEL 162 ~False()~ DO 4  // #234704 "Someone tried to kill me tonight and I'm in a bar." (Elfsong)

// --- Garrick, Elfsong farewell (state 39 "She tried to slay the hero..."
//     is only entered by these two replies -> orphaned) ---
ADD_TRANS_TRIGGER BDGARRIC 38 ~False()~ DO 0 1  // #234516 #234517

// --- Safana, recruit ---
ADD_TRANS_TRIGGER BDSAFANA 22 ~False()~ DO 2  // #234909
ADD_TRANS_TRIGGER BDSAFANA 44 ~False()~ DO 1  // #235023

// --- Rasaad, recruit (Wayward Home) ---
// Research's entry-reply list plus the three closure gates (28.0, 32.1,
// 36.0) needed to actually orphan the "nearly killed" subgraph: state 39
// stays reachable through the clean-textual replies #234636/#234609/
// #234630 otherwise, and with all of 39's replies gated it would
// dead-end the dialog. With the closure, states 25/35/37/38/39/40/42/
// 44-47 (+ the SAFANJ 101 insert) are all unreachable; every gated state
// keeps at least one live reply.
ADD_TRANS_TRIGGER BDRASAAD 21 ~False()~ DO 3      // #234596
ADD_TRANS_TRIGGER BDRASAAD 22 ~False()~ DO 0 1    // #234598 #234599
ADD_TRANS_TRIGGER BDRASAAD 28 ~False()~ DO 0      // #234636 (closure: route into state 39)
ADD_TRANS_TRIGGER BDRASAAD 32 ~False()~ DO 1      // #234609 "I was nearly killed earlier this evening" (closure: route into 37/38)
ADD_TRANS_TRIGGER BDRASAAD 36 ~False()~ DO 0 1    // #234630 (closure: route into 44) + #234631 breakfast quip
ADD_TRANS_TRIGGER BDRASAAD 38 ~False()~ DO 1 2    // #234637 #234638 (state unreachable after closure; gated per list)
ADD_TRANS_TRIGGER BDRASAAD 39 ~False()~ DO 0 1 2  // #234640 #234641 #234642 (ditto)

// --- Dynaheir, recruit (Three Old Kegs) ---
// State 23 reply 1 (#234751 "She sent assassins to try and kill me this
// morning") was missed by the research list — gated as closure; reply 2
// (#234752) stays live so the state never dead-ends.
ADD_TRANS_TRIGGER BDDYNAHE 23 ~False()~ DO 0 1  // #234750 + #234751 (closure)
ADD_TRANS_TRIGGER BDDYNAHE 30 ~False()~ DO 1    // #234773
ADD_TRANS_TRIGGER BDDYNAHE 33 ~False()~ DO 0 2  // #238729 #238731

// --- Audamar (Rohma scene, BD0101 send-off plaza) ---
ADD_TRANS_TRIGGER BDAUDAM 10 ~False()~ DO 3  // #258137 "The Shining Lady has already tried to kill me once."
