// chriz-sod-remix component 120 — remove hooded-man dialogue hooks.
// BDSCRY states 0/4, transition 2: the opt-in "The Hooded Man..." scrying choice
// (launches BDSCRY05/06). BDIMOEN state 67, transition 1: Imoen's "What was that
// man in the hood doing here?" — dangling once he never appears at her bedside.
// ADD_TRANS_TRIGGER appends (ANDs) to any existing trigger, so False() disables
// the reply without touching mod-added transitions in the same states.

ADD_TRANS_TRIGGER BDSCRY 0 ~False()~ DO 2
ADD_TRANS_TRIGGER BDSCRY 4 ~False()~ DO 2
ADD_TRANS_TRIGGER BDIMOEN 67 ~False()~ DO 1
