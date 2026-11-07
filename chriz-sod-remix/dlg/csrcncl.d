// chriz-sod-remix component 150 — crusade-only war council + assassination
// text gates. All state/transition indices verified against the DEV-install
// decompiles 2026-07-06 (docs/research/11a §2 mapped the council chain; 11b
// list (b) mapped the city references; research's flat transition numbers
// were converted to the per-state indices ALTER_TRANS/ADD_TRANS_TRIGGER use).
// Owned trigger fields are overwritten; mod-added transitions in the same
// states are untouched. ALTER_TRANS EPILOGUE only re-points the target;
// reply text and any triggers stay.

// ============================================================
// A. Council re-points (11a §2-3: crusade council, zero new text)
// ============================================================

// Entry stays BDLIIA 9 ("Let us begin..."); its "Assassins tried to kill
// me this night" reply dies. Replies 0/2/3 (greeting + the two Entar
// intros) all funnel into BDELTAN 4 and survive.
ALTER_TRANS BDLIIA BEGIN 9 END BEGIN 1 END BEGIN TRIGGER ~False()~ END// #257840

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
ALTER_TRANS BDBELT BEGIN 40 END BEGIN 2 END BEGIN TRIGGER ~False()~ END

// BDBELT 41 closes the council with the platform-specific QUEST_DONE whose
// text says the assassins were sent by Caelar. Swap for the crusade-only line
// @15010 (same "The Siege of Dragonspear" title; the tpa registers the new
// strref in bgee.lua). The two preserved journal IDs are injected for native
// SoD or EET while the rest of the action remains verbatim.
ALTER_TRANS BDBELT BEGIN 41 END BEGIN 0 END BEGIN
  ACTION ~SetGlobal("bd_plot_003","bd0102",2)
AddJournalEntry(%csr150_council_info%,INFO)
AddJournalEntry(%csr150_campaign_quest%,QUEST)
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
ALTER_TRANS BDELTAN BEGIN 11 END BEGIN 1 END BEGIN TRIGGER ~False()~ END// #256007 "assassins roam the Ducal Palace"
ALTER_TRANS BDELTAN BEGIN 13 END BEGIN 2 END BEGIN TRIGGER ~False()~ END// #256017 "Caelar tried to kill me. She will answer for it."

// --- Liia, palace small talk ---
// #256030 "As well as an assassin's target can be". Her reply #256031
// ("how fares Imoen?") -> state 14's poison line stays: 11a parks BDLIIA
// 14-15 as later-pass text-patch candidates.
ALTER_TRANS BDLIIA BEGIN 13 END BEGIN 0 END BEGIN TRIGGER ~False()~ END

// --- Belt, BD0100 apology web (GlobalLT(BD_plot,55) + AreaCheck(bd0100)) ---
// "What happened to Imoen falls on my shoulders..." State 42 is the only
// scripted entry; 43-46/55-58 are gated too per the research list (inert
// for chained states, but future-proof against weight tricks).
REPLACE_STATE_TRIGGER BDBELT 42 ~False()~
REPLACE_STATE_TRIGGER BDBELT 43 ~False()~
REPLACE_STATE_TRIGGER BDBELT 44 ~False()~
REPLACE_STATE_TRIGGER BDBELT 45 ~False()~
REPLACE_STATE_TRIGGER BDBELT 46 ~False()~
REPLACE_STATE_TRIGGER BDBELT 55 ~False()~
REPLACE_STATE_TRIGGER BDBELT 56 ~False()~
REPLACE_STATE_TRIGGER BDBELT 57 ~False()~
REPLACE_STATE_TRIGGER BDBELT 58 ~False()~

// --- Corwin, city escort ---
ALTER_TRANS BDSCHAEL BEGIN 46 END BEGIN 1 END BEGIN TRIGGER ~False()~ END// #267279 "As assassins attacked me in the Ducal Palace..." (return-prompt)
ALTER_TRANS BDSCHAEL BEGIN 162 END BEGIN 4 END BEGIN TRIGGER ~False()~ END// #234704 "Someone tried to kill me tonight and I'm in a bar." (Elfsong)

// --- Garrick, Elfsong farewell (state 39 "She tried to slay the hero..."
//     is only entered by these two replies -> orphaned) ---
ALTER_TRANS BDGARRIC BEGIN 38 END BEGIN 0 1 END BEGIN TRIGGER ~False()~ END// #234516 #234517

// --- Safana, recruit ---
ALTER_TRANS BDSAFANA BEGIN 22 END BEGIN 2 END BEGIN TRIGGER ~False()~ END// #234909
ALTER_TRANS BDSAFANA BEGIN 44 END BEGIN 1 END BEGIN TRIGGER ~False()~ END// #235023

// --- Rasaad, recruit (Wayward Home) ---
// Research's entry-reply list plus the three closure gates (28.0, 32.1,
// 36.0) needed to actually orphan the "nearly killed" subgraph: state 39
// stays reachable through the clean-textual replies #234636/#234609/
// #234630 otherwise, and with all of 39's replies gated it would
// dead-end the dialog. With the closure, states 25/35/37/38/39/40/42/
// 44-47 (+ the SAFANJ 101 insert) are all unreachable; every gated state
// keeps at least one live reply.
ALTER_TRANS BDRASAAD BEGIN 21 END BEGIN 3 END BEGIN TRIGGER ~False()~ END// #234596
ALTER_TRANS BDRASAAD BEGIN 22 END BEGIN 0 1 END BEGIN TRIGGER ~False()~ END// #234598 #234599
ALTER_TRANS BDRASAAD BEGIN 28 END BEGIN 0 END BEGIN TRIGGER ~False()~ END// #234636 (closure: route into state 39)
ALTER_TRANS BDRASAAD BEGIN 32 END BEGIN 1 END BEGIN TRIGGER ~False()~ END// #234609 "I was nearly killed earlier this evening" (closure: route into 37/38)
ALTER_TRANS BDRASAAD BEGIN 36 END BEGIN 0 1 END BEGIN TRIGGER ~False()~ END// #234630 (closure: route into 44) + #234631 breakfast quip
ALTER_TRANS BDRASAAD BEGIN 38 END BEGIN 1 2 END BEGIN TRIGGER ~False()~ END// #234637 #234638 (state unreachable after closure; gated per list)
ALTER_TRANS BDRASAAD BEGIN 39 END BEGIN 0 1 2 END BEGIN TRIGGER ~False()~ END// #234640 #234641 #234642 (ditto)

// --- Dynaheir, recruit (Three Old Kegs) ---
// State 23 reply 1 (#234751 "She sent assassins to try and kill me this
// morning") was missed by the research list — gated as closure; reply 2
// (#234752) stays live so the state never dead-ends.
ALTER_TRANS BDDYNAHE BEGIN 23 END BEGIN 0 1 END BEGIN TRIGGER ~False()~ END// #234750 + #234751 (closure)
ALTER_TRANS BDDYNAHE BEGIN 30 END BEGIN 1 END BEGIN TRIGGER ~False()~ END// #234773
ALTER_TRANS BDDYNAHE BEGIN 33 END BEGIN 0 2 END BEGIN TRIGGER ~False()~ END// #238729 #238731

// --- Audamar (Rohma scene, BD0101 send-off plaza) ---
ALTER_TRANS BDAUDAM BEGIN 10 END BEGIN 3 END BEGIN TRIGGER ~False()~ END// #258137 "The Shining Lady has already tried to kill me once."
