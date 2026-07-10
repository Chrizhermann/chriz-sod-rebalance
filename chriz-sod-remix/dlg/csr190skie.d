// csr190skie.d — component 190: seal off Skie's night "don't tell Daddy"
// dialogue tree. State 16 ("Are you awake?") is the sole root of the 16-32
// night cluster (from: empty — it is only ever entered as a top-level state
// when Skie's dialog opens at night). csr190wake pre-empts the bd0103 block so
// Skie is never spawned or StartDialog'd there, but if Skie has been recruited
// her party dialog could otherwise select state 16 once BD_MDD005 flips to 1.
// False() removes state 16 from selection, which unreaches the whole 16-32
// subtree (journal 259627 included). Nothing GOTO/EXTERNs into 16, so no reply
// is stranded.
//
// The broader Skie SoD-plot lines (crypt state 3, council 12/13, dig-site
// 87-89) are entangled with her recruitment/camp/BDBENCE flow and are deferred
// to the dedicated Skie-companion pass — not touched here.
ADD_STATE_TRIGGER ~BDSKIE~ 16 ~False()~
