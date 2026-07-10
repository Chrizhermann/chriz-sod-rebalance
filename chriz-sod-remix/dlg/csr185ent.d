// csr185ent.d — component 185: Entar Silvershield removed from the war council
// and the departure send-off. All state/reply indices verified against the
// installed (comp150/160/180-patched) BDLIIA/BDBELT/BDSERV decompiles
// 2026-07-08. ADD_TRANS_TRIGGER ANDs onto existing triggers; ALTER_TRANS
// EPILOGUE re-points a transition's target only (its trigger + action stay).

// ============================================================
// A. War council (BDLIIA 9)
// ============================================================
// The roll-call drops "and Entar Silvershield" (he no longer stands here). The
// resurrection reply (DO 2 — offered only on SOD_fromimport==1, which is TRUE
// on this EET install, so currently LIVE) and the Skie-introduction reply
// (DO 3 -> BDENTAR 5) are gated. The greeting reply (DO 0 -> BDELTAN 4) carries
// the council forward; comp150 already gated DO 1.
REPLACE_SAY ~BDLIIA~ 9 @18500
ADD_TRANS_TRIGGER BDLIIA 9 ~False()~ DO 2   // #257841 "Weren't you...killed?" -> BDENTAR 6
ADD_TRANS_TRIGGER BDLIIA 9 ~False()~ DO 3   // #257842 "Who is the young lady?" -> BDENTAR 5

// ============================================================
// B. Departure send-off, rebuilt Belt-side
// ============================================================
// The plot-56 send-off ping-ponged through Entar (BDENTAR 41 opener / 42 loop /
// 43-44 close), entered by clicking Entar (bd0102 stages him front-and-centre).
// comp185's script pass unspawns Entar and stands Belt on that spot instead, so
// Belt now presides: three new Belt states replicate opener/loop/close, and the
// surviving bridges re-point into them. bd_final_speech is still flipped to 1 in
// BDBELT 61 (first pass), so the hub runs once and a repeat click yields the
// existing short exits (BDBELT 64 / BDLIIA 33). Entar's entry (40) and repeat
// (45) orphan with no speaker; the Skie ring "family matter" branch (BDENTAR
// 8-23: ring07 + journal 256390) dies with them — consistent with the Skie
// SoD-plot removal (comp190).
APPEND ~BDBELT~
IF ~~ THEN BEGIN ~csr185_dep_open~
  SAY @18501
  IF ~~ THEN REPLY @18502 GOTO 62                 // route -> Belt's existing route line
  IF ~~ THEN REPLY @18503 EXTERN ~BDLIIA~ 31      // mission -> Liia's existing rendezvous line
  IF ~~ THEN REPLY @18504 GOTO ~csr185_dep_close~
END
IF ~~ THEN BEGIN ~csr185_dep_loop~
  SAY @18505
  IF ~~ THEN REPLY @18502 GOTO 62
  IF ~~ THEN REPLY @18503 EXTERN ~BDLIIA~ 31
  IF ~~ THEN REPLY @18504 GOTO ~csr185_dep_close~
END
IF ~~ THEN BEGIN ~csr185_dep_close~
  SAY @18506
  IF ~~ THEN EXIT
END
END

// Bridges re-point away from Entar. Belt 61 keeps its SetGlobal(bd_final_speech,1)
// action (EPILOGUE re-points target only). Belt 62 (route) and Liia 31 (mission)
// both looped back through Entar 42 -> now the Belt loop hub.
ALTER_TRANS BDBELT BEGIN 61 END BEGIN 0 END BEGIN
  EPILOGUE ~GOTO csr185_dep_open~
END
ALTER_TRANS BDBELT BEGIN 62 END BEGIN 0 END BEGIN
  EPILOGUE ~GOTO csr185_dep_loop~
END
ALTER_TRANS BDLIIA BEGIN 31 END BEGIN 0 END BEGIN
  EPILOGUE ~EXTERN BDBELT csr185_dep_loop~
END

// ============================================================
// C. Servant "fetch Duke Entar" night-before spawn (BDSERV 2)
// ============================================================
// Hygiene: the second-night servant offer to summon Entar (reply DO 0 -> state 3
// CreateCreature("bdentar")). No BDSERV creature spawns in the remixed prologue
// (comp150 substitutes csrserv, and comp190 owns the second-sleep beat), so this
// is belt-and-suspenders; gating DO 0 leaves the two wake-at-dawn replies
// (states 4/5) intact.
ADD_TRANS_TRIGGER BDSERV 2 ~False()~ DO 0   // #235244 "Fetch Duke Entar. I must speak to him about his daughter."
