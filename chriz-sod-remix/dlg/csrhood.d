// chriz-sod-remix component 120 — remove hooded-man dialogue hooks.
// Disable every installed copy of the opt-in "The Hooded Man..." scrying
// choice by its semantic trigger. Aura copies the picker into an appended
// BDSCRY state on EET; native SoD has only the original state. Matching the
// trigger preserves either dialog shape and any interjections added beside it.
REPLACE_TRIGGER_TEXT BDSCRY
  ~Global("bd_sddd12_hood","LOCALS",0)~
  ~False()
Global("bd_sddd12_hood","LOCALS",0)~

// Imoen's "What was that man in the hood doing here?" is dangling once he
// never appears at her bedside. This transition is stable on both platforms.
ADD_TRANS_TRIGGER BDIMOEN 67 ~False()~ DO 1
