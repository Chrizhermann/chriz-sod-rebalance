// csr195.d — component 195: scrub the residue of the removed first-night Ducal
// Palace assassination attempt on CHARNAME (comp150 removed the event; NPCs
// still referenced it). ZERO new dialogue: reply/state False() gates plus two
// re-routes that drop residue-bearing states without replacing any text.
//
// All state/reply indices verified 2026-07-09 against fresh weidu 24600
// decompiles of the dev-install override (post comp150/160/180/185), the state
// AFTER which comp195 installs. In-scope = the assassination attempt only; the
// de Lancie supply-poison quest and generic poison mechanics are untouched
// (none present in these dialogs anyway). Lines comp150/comp120 already
// False()-gated (BDELTAN 11.1/13.2, BDLIIA 9.1/13.0, BDIMOEN 67.1) are NOT
// re-touched here.

// ============================================================
// A. LIVE player-reply residue (reachable in normal play)
// ============================================================
// Each gated reply leaves a clean generic-crusade fallback in its state; every
// gated state's siblings still route onward, so nothing dead-ends.

// -- BDCORWIN (Schael Corwin) — "you want to turn back?" at the first camp.
//    Reply 0 (Council of Four) survives; 2/3 left LIVE per user (Caelar still
//    is our antagonist), all four siblings GOTO 12 so nothing strands.
ADD_TRANS_TRIGGER BDCORWIN 11 ~False()~ DO 1   // #242095 "Caelar nearly killed me and my friend Imoen."

// -- BDELTAN (Grand Duke Eltan) — palace small-talk. The sibling of 11.1/13.2
//    that comp150 gated but skipped. Replies 0/2/3 stay; reply 2 also GOTO 11.
ADD_TRANS_TRIGGER BDELTAN 10 ~False()~ DO 1    // #256002 "people trying to kill me for no apparent reason"

// -- BDEDWIN (Edwin) — Coast Way recruitment. Eight "Caelar tried to kill me"
//    replies; reply 0 (the crusade line) is the fallback in every state.
//    Gating 21.1 orphans Edwin's own backstory state 39 — user OK'd the loss.
ADD_TRANS_TRIGGER BDEDWIN 21 ~False()~ DO 1    // #242137 "...Caelar Argent seeks my death."
ADD_TRANS_TRIGGER BDEDWIN 21 ~False()~ DO 2    // #242138 "Caelar Argent tried to kill me..."
ADD_TRANS_TRIGGER BDEDWIN 21 ~False()~ DO 3    // #242139 "...Caelar Argent tried to kill me. She failed."
ADD_TRANS_TRIGGER BDEDWIN 31 ~False()~ DO 1    // #242160 "Caelar Argent tried to kill me..."
ADD_TRANS_TRIGGER BDEDWIN 31 ~False()~ DO 2    // #242161 "...The Shining Lady tried to kill me."
ADD_TRANS_TRIGGER BDEDWIN 35 ~False()~ DO 2    // #242178 "The Shining Lady tried to kill me. Now it is my turn."
ADD_TRANS_TRIGGER BDEDWIN 36 ~False()~ DO 1    // #242181 "She tried to kill me, and now I'm trying to kill her back."
ADD_TRANS_TRIGGER BDEDWIN 36 ~False()~ DO 2    // #242182 "...the Shining Lady has targeted me for death."

// -- BDSCHAEL (Corwin) — city-escort banter. Gate the entry reply 167.0, which
//    orphans state 168 ("assassins Caelar sent after you"). 167 keeps replies
//    1 (->172) and 2 (->170).
ADD_TRANS_TRIGGER BDSCHAEL 167 ~False()~ DO 0  // #254918 "Is that really necessary?" -> 168

// -- BDDEBUG (dev console) — the now-broken "jump to the assassin scene".
ADD_TRANS_TRIGGER BDDEBUG 4 ~False()~ DO 1     // #265249 "Skip to assassin attack at Ducal Palace."

// ============================================================
// B. BDSCHAEL 227/228 — the goodnight "crusader poison" line (the one you
//    pointed at). State 228's SAY is load-bearing ONLY because its transition
//    sets BD_plot=54 (the retire-for-the-march commit). Move that DO up onto
//    the "I'm ready to march" reply and EXIT there, so state 228 is never
//    entered and Corwin speaks no line. State 227 already warns "there'll be no
//    coming back to the city," so nothing is lost. No new text.
// ============================================================
ALTER_TRANS BDSCHAEL BEGIN 227 END BEGIN 0 END BEGIN   // #266837 "Yes. I'm ready to begin the march..."
  ACTION ~SetGlobal("BD_plot","global",54) SetGlobal("BD_CORWIN_GOODNIGHT","BD0102",1) AddJournalEntry(266840,QUEST)~
  EPILOGUE ~EXIT~
END

// ============================================================
// C. BDLIIA 13 — re-route "how fares Imoen?" past the poison/palace residue.
//    13.1 -> 14 (SAY: weapons poisoned) -> 15 (SAY: palace penetrated) -> hub.
//    Gating 13.1 would kill the whole Liia palace conversation, so instead
//    re-point 13.1 straight to state 19 — Liia's existing Imoen-training-advice
//    line, which answers "how fares Imoen?" cleanly and keeps that tree.
//    States 14, 15, 16 (Caelar-flavor), 27, 28 (the assassination beat) fall
//    away as orphans. No new text; state 16's Caelar description is the only
//    (minor) content lost, which the user accepted.
// ============================================================
ALTER_TRANS BDLIIA BEGIN 13 END BEGIN 1 END BEGIN      // #256031 "...how fares Imoen?"
  EPILOGUE ~GOTO 19~
END

// ============================================================
// D. Dead-but-explicit assassination text — belt-and-suspenders gates matching
//    comp150's own defensive pattern (csrcncl.d BDBELT 42-58). All already
//    unreachable (empty inbound, or their sole entry re-pointed by comp150/185);
//    gated so the most explicit "assassins' bodies / High Hall" lines can never
//    resurface if a later rework re-enables a path.
// ============================================================
// -- BDELTAN council aftermath (entered only via now-severed EXTERNs)
ADD_STATE_TRIGGER BDELTAN 1 ~False()~          // #264712 "...the body of one of the assassins. A sun cresting..."
ADD_STATE_TRIGGER BDELTAN 9 ~False()~          // #264734 "...parchment from one of the assassins' bodies..."
// -- BDFIST05 palace door-guard ambient barks
ADD_STATE_TRIGGER BDFIST05 0 ~False()~         // #255915 "Whoever attacked the palace will pay..."
ADD_STATE_TRIGGER BDFIST05 1 ~False()~         // #255916 "Assassins in the High Hall..."
// -- BDLIIA bd0103 bedside-triage aftermath (csrarr.baf parks these) + dead council
ADD_STATE_TRIGGER BDLIIA 0 ~False()~           // #264618 "...dealing with the wounded downstairs..."
ADD_STATE_TRIGGER BDLIIA 3 ~False()~           // #264626 "...more of our attackers and who sent them."
ADD_STATE_TRIGGER BDLIIA 8 ~False()~           // #264631 "...speak with Duke Eltan... something of our attackers."
ADD_STATE_TRIGGER BDLIIA 12 ~False()~          // #264731 "...Caelar's zealots clearly mean to see you dead."
ADD_TRANS_TRIGGER BDLIIA 10 ~False()~ DO 1     // #264715 "The crusade's assassins paid for their arrogance."
