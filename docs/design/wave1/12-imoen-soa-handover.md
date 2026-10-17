# Imoen's handover from SoD into Shadows of Amn (EET)

Status: **DECIDED** by Christopher on 2026-10-17. Technical checks still open are
listed at the end; there are no open gameplay questions.

## The problem

Component 160 keeps the imported BG1 Imoen (and builds a recruitable fallback,
`csrimo`, for fresh SoD starts), so vanilla SoD's swap to the scene actor never
happens. EET's SoD-to-SoA handover then treats her like any other carried NPC:

- **In the party at the switch:** the transition carrier (`K#TELBGT`) banks her
  gear, destroys her, and `AR0602` creates EET's installed BG2 Imoen (`IMOEN10`).
- **Out of the party:** she survives. `AR0602` moves the existing actor into the
  dungeon with **all of her SoD gear**, and only adds `IMOENHP1` with
  `FillSlot(SLOT_BELT)`. When her own belt is equipped, `FillSlot` moves it into
  the magic-weapon slot: the UI shows "Magical weapon in use" and she fights
  bare-handed. She also stays a pure BG1 thief.

Optional component 910 already tried to bank an imported Imoen's gear at the
bedroom skip, but its adapter never fired in Christopher's run (his save shows
the skip completed with no Imoen item handled; she reached SoA with her gear).

## DECIDED (Christopher, 2026-10-17)

1. Three **install-time** choices; the CEBG default is choice 1. Each choice must
   work with any thief kit and without a kit, with and without Spell Revisions.
   1. **Vanilla BG2 dual-class.** She becomes EET's installed BG2 Imoen build
      (`IMOEN10`: thief 7 / mage 8 in vanilla, with that file's HP, skills, spells
      and proficiencies), **plus her BG1/SoD tome boosts** on top of that build's
      ability scores. Must work without EEex.
   2. **As taken along.** Her own BG1/SoD build continues.
   3. **Dual-class at her end-of-SoD thief level.** Her thief levels freeze, mage
      starts at level 1, and all of SoA's catch-up XP goes into mage. She starts
      with vanilla BG2 Imoen's spellbook. **Requires EEex.** No script action or
      opcode can set the CRE "original class" flag (IESDP-checked), so the
      conversion has to write that field directly.
2. **Gear, all choices:** "BG2 should always be a clean start." Her carried gear
   goes through EET's item-import rules exactly like the protagonist's. Items on
   EET's import lists are imported (at most one copy per item, and only when the
   party does not already carry one, as EET does for the party). Everything else
   is banked in EET's invisible import container. She keeps only her BG2 belt
   (`IMOENHP1`), now equipped correctly.
3. Christopher's own running game gets a separate, one-time repair proposal; it
   needs his explicit OK and is not part of this component.

## Mechanism

New EET-only subcomponents **292 / 293 / 294** ("Imoen in Shadows of Amn",
choices 1 / 2 / 3). They require 160 and 290 (the normal route hosts the
preparation), EET_end, and — 294 only — EEex. They integrate with 910 when it is
installed, in either install order.

### SoD-end preparation (all choices)

A short state machine runs **before** the transition logic on both routes:

| Route | Host | Bank container |
|---|---|---|
| Normal ending (290) | our carrier clone `CSRETBGT`, inserted after the 290 guard block | `BD4300*K#ImportContainer` (moved on to BD6100 by 290) |
| Bedroom skip (910) | the 910 helper `csrskask`, at the top of phase 1 | `BD0103*PlayerChest00` (moved on to BD6100 by 910) |

Steps (global `CSR_IMSOA_PREP`; each step gated, interrupt-protected, and with a
timeout that never blocks the transition). The host's script does not reach its
own transition blocks until the preparation reports finished: a final wait block
(`!Global("CSR_IMSOA_PREP","GLOBAL",9)` → `NoAction()`) holds it.

1. Only an Imoen who has been in the party and is alive is handled
   (`BeenInParty`, not `STATE_REALLY_DEAD`). A never-recruited `csrimo` is left
   alone: EET creates `IMOEN10` as usual.
2. **Mark her, then separate her from the party.** EET's `IMOEN_` (the BG1
   Imoen's override script) destroys her as soon as she is out of the party after
   BG1, unless she carries EET's SoD-party mark (`K#PartySoD` LOCALS 1). EET sets
   that mark on Imoen itself in SoD's epilogue (`BD6200`, chapter 13), which the
   remix's ending replaces. So the preparation sets the same mark first, verifies
   it on her (`NextTriggerObject`), and only then calls `LeaveParty()`
   (`InPartyAllowDead`, so a sleeping or silenced Imoen counts as a member).
   Lab, 2026-10-17: without the mark, `LeaveParty()` made an imported Imoen vanish
   at once, with her gear.
   If she is elsewhere (dismissed at a camp, parked in the palace, ...), the mark
   is queued on her ahead of `MoveGlobalObject`, so it is the first thing she does
   on arrival. This replaces 910's `InMyArea` assumption. If she turns out to be a
   corpse, nothing is done. If the step does not finish within 15 seconds, the
   preparation gives up and the transition goes ahead:
   - still in the party (`CSR_IMSOA_FAILED` 5): the host's transition hands her
     over like any companion and Shadows of Amn's own Imoen takes her place;
   - alive elsewhere (`CSR_IMSOA_FAILED` 1): SoA's fallback below banks her gear;
   - gone (`CSR_IMSOA_FAILED` 4, another script removed her): nothing of hers can
     be carried over.

   Cases 4 and 5 are reported once Shadows of Amn's Imoen is in the party.
   Neither one triggers the fallback, which would otherwise strip the fresh
   `IMOEN10`'s own gear.
3. **Import:** for every item rule in the *effective* installed carrier
   (EET_end-generated from `K#IMPORT.2DA`, `IMPORT01-03.2DA` and `BDSODIMP`, plus
   other mods' additions), if she has the item and the party does not, add one
   copy to EET's `K#IMPORT` bag store — the same operation EET's own rule performs.
   The rules are read from the installed script and verified at install time:
   when an import rule has an unexpected shape, installation stops instead of
   guessing.
4. **Bank:** `TakeCreatureItems("IMOEN2",0)` (0 = all items, including equipped
   ones) into the host's container.
5. **Choice 1 only:** strip ability-score effects (opcode 337 for opcodes 6, 10,
   15, 19, 44, 49, 97), read her base scores with `CheckStat`, store each positive
   difference to the installed BG1 chassis (`IMOEN2.CRE`) as a tome boost, and
   destroy her. The removal is confirmed with `!BeenInParty("IMOEN2")`, the same
   test EET's `AR0602` uses to create `IMOEN10`. If it cannot be confirmed within
   3 seconds (`CSR_IMSOA_FAILED` 2), her gear has still been handed over; she
   continues as taken along and SoA reports that the rebuild did not happen.

### In Shadows of Amn (`BALDUR.BCS`)

- **Choice 1:** once `IMOEN10` is in the party, add the stored boosts with
  `ChangeStat(..., ADD)`. Each boost is capped at installation against the
  installed `IMOEN10.CRE` score, so no score passes 25. One-shot
  (`CSR_IMSOA_BOOST` 1 → 2).
- **Choice 3:** after EET's carried-Imoen arrival (`K#ImoenImport` set in
  `AR0602`), one EEex Lua call converts a **pure single-class thief** in place:
  class `MAGE_THIEF`, original-class flag thief, mage level 1, thief level = her
  level, XP 0, and `BD_JOINXP` re-armed. Kit, HP, skills and proficiencies stay.
  SoA's normal join ladder (`BD_JOINXP` in `IMOEN.BCS`) then raises her XP, which
  for a dual-class is mage XP. Resetting XP and the ladder inside the conversion
  makes the result independent of whether `AR0602`'s own ladder reset ran first.
  Anyone who is not a pure thief (an `IMOEN10` from EET's fresh path, an Imoen
  the player already dual-classed, a multiclass) is left unchanged.
  She is then taught `IMOEN10`'s known wizard spells (read at install time;
  missing resources skipped) with the engine's learn-spell effect (opcode 147).
  That effect rolls against Intelligence, so the Lua first raises her
  Intelligence to 25 for 12 seconds, teaches on the next pass and verifies the
  spellbook, retrying up to 10 times. Spells that still fail are logged and
  reported once. A Lua error or a missing EEex leaves her unchanged and reports it.
- **Fallback (she could not be brought, `CSR_IMSOA_FAILED` 1):** when she is in
  the party in `AR0602`, drop EET's `IMOENHP1` from her (it may sit outside the
  belt slot), bank everything else she still carries in
  `AR0602*K#ImportContainer`, then create a fresh `IMOENHP1` in the belt slot.
  These are three separate passes, because different objects act and no second
  copy of the unique belt may reach EET's bank. Choice 1's rebuild is not
  attempted in this failure path (it would have to swap a party member after the
  dungeon intro); a message reports it.

## Edge cases

- **Dead Imoen** is left to EET: dead in the party → EET replaces her with
  `IMOEN10`; dead outside the party → EET brings no Imoen (pre-existing EET
  behaviour, unchanged here).
- **Kits:** no kit is stripped or validated against `DUALCLAS.2DA`; choice 3
  converts any thief kit (Christopher's requirement).
- **Tome boosts** are measured against the installed `IMOEN2.CRE` scores. Only
  increases count; exceptional strength is ignored. A mod that grants permanent
  ability effects instead of base-score changes is undercounted (effects are
  stripped before reading).
- **Two Imoen copies** cannot exist: choice 1 destroys the carried actor before
  EET creates `IMOEN10`; choices 2/3 keep the carried actor, so EET does not
  create one.

## Open technical checks (lab)

- `TakeCreatureItems(ALL)` on a non-party NPC also clears the magic-weapon slot.
- `MoveGlobalObject` brings an off-party Imoen from another SoD area.
- Global script blocks act during the dungeon intro (timing of choice 3).
- After choice 3: level-up, thief reactivation, spell slots, save/reload.
