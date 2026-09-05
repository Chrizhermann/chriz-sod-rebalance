// chriz-sod-remix component 120 — remove the remaining BDIMOEN dialogue hook.
// The BDSCRY picker is patched semantically by lib/bdscry_compat.tpa against
// the current no-Aura four-state graph.
//
// BDIMOEN state 67, transition 1: Imoen's "What was that man in the hood doing
// here?" — dangling once he never appears at her bedside.
ADD_TRANS_TRIGGER BDIMOEN 67 ~False()~ DO 1
