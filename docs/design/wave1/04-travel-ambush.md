# Wave 1 — Travel-Ambush (URE) Degut

**Status:** awaiting user sign-off. Supersedes the prior-agent proposal `design/05`.
**Scope:** the worldmap travel-ambush system (wishlist item 8): "kill the huge groups; fill
with nothing or something more interesting/fun."

## Mechanism recap (verified, `research/07`)
Script-driven, not engine-random: wilderness area scripts call
`ForceRandomEncounterEntry("BD00xx","Exit")` behind a weighted die (`RESPONSE #40` fire /
`#60` skip = ~40% per trigger), a shared 8-hour cooldown (`BD_TIMER_URE`), and per-encounter
one-shot globals (`BD_URE1–4`, never reset). **At most 4 random arenas per playthrough:**
- URE1 → BD0060 orc pack
- URE2 → BD0063 dead-magic-zone ambush
- URE3 → BD0066 goblin horde (38 goblins + 3 ankhegs — the worst pile-on)
- URE4 → BD0064 hill giants

Story vignettes URE6–10 (refugees, Myrleena, Ephrik, the Lebass chase) are separate,
fire-once-on-entry, and **stay untouched** (decided).

## Decided (user, 2026-07-03)
- The huge arena groups go. Arenas either become empty (encounter never fires / fires
  harmlessly) or get a small, fun roster instead.
- Story vignettes (URE6–10) and true set-pieces stay.

## Open questions
1. **Frequency:** with rosters gutted, does frequency still matter to you? Options:
   leave the 40%/8h trigger as-is (arenas become quick, small fights), lower the fire weight
   (~#15) and/or lengthen the cooldown to a day (≈1–2 arenas per run), or pre-set `BD_URE1–4`
   so random arenas never fire at all.
2. **Per-arena treatment:** which of the 4 get "nothing" vs. "something fun"? (Roster design
   is creative work — can be done here in Wave 1 or deferred to the chapter passes; the
   goblin horde BD0066 is the clear first candidate either way.)

## Implementation sketch (after sign-off)
Script-only, reversible, applies on next area load: `COPY_EXISTING` the wilderness `.bcs`
(BD7000/7100/7200/7300/7400/2000/3000/5000), `DECOMPILE_BCS_TO_BAF`, `REPLACE_TEXTUALLY` the
weights/cooldown, recompile. Arena rosters are `.are`/script edits per arena. Compat-first:
pattern-match the existing blocks rather than replacing whole scripts (other mods may have
appended blocks to the same `.bcs`).
