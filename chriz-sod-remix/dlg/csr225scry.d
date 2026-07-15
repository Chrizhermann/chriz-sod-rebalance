// chriz-sod-remix component 225 — retire the remaining vanilla vision picker
// replies without replacing BDSCRY.DLG. Component 120 already False-gates
// transition 2 (the Hooded Man) in both states; these additions retire Imoen
// and Caelar while preserving the dialog's shape for third-party interjections.

ADD_TRANS_TRIGGER BDSCRY 0 ~False()~ DO 0 1
ADD_TRANS_TRIGGER BDSCRY 4 ~False()~ DO 0 1
