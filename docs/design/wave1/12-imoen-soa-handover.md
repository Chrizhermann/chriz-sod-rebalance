# Imoen's handover from SoD into Shadows of Amn (EET)

Status: **DECIDED** by Christopher on 2026-10-17, except a dead Imoen at the end
of SoD (OPEN, see Edge cases). Lab results are at the end.

## The problem

Component 160 keeps the imported BG1 Imoen (and builds a recruitable fallback,
`csrimo`, for fresh SoD starts), so vanilla SoD's swap to the scene actor never
happens. EET's SoD-to-SoA handover then carries her over as she is:
`AR0602` moves every Imoen who has been in the party and is not dead into the
dungeon (`MoveGlobal`), and creates its own BG2 Imoen (`IMOEN10`) only for an
Imoen who never joined.

- **Out of the party:** `AR0602` moves the existing actor into the dungeon with
  **all of her SoD gear**, and only adds `IMOENHP1` with `FillSlot(SLOT_BELT)`.
  When her own belt is equipped, `FillSlot` moves it into the magic-weapon slot:
  the UI shows "Magical weapon in use" and she fights bare-handed. She also stays
  a pure BG1 thief.
- **In the party at the switch:** the transition carrier (`K#TELBGT`) runs the
  party's import over her gear and destroys her. A destroyed Imoen is not gone,
  though (lab, 2026-10-17): `DestroySelf()` only takes her out of her area; she
  stays in EET's list of global creatures, still marked as having been in the
  party, and `AR0602`'s `MoveGlobal` brings her back. She arrives as her BG1
  build, never as `IMOEN10`.

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
   `LeaveParty()` also gives her the SoD campaign's post-party dialog
   (`BDDIALOG.2DA` `POST_DIALOG_FILE`, `csrimoen` with component 160), and she
   opens it within a second. `csrimoen` offers to rejoin the party; in the lab,
   rejoining mid-handover led to a removed party member (an empty portrait in
   SoA). So every state of that dialog that can open a conversation gets the
   condition `CSR_IMSOA_PREP` < 1 or > 8 at install time (the dialog is read
   from the installed table; a missing one needs no change). Before and after
   the preparation the dialog is unchanged. As a second line of defence, an
   Imoen who is back in the party before her gear is handed over sends the
   preparation back to this step, and her removal never targets a party
   member (if she is back in the party by then, the host's transition
   hands her over like any companion; see `CSR_IMSOA_FAILED` 5 below).
   If she is elsewhere (dismissed at a camp, parked in the palace, ...), the mark
   is queued on her ahead of `MoveGlobalObject`, so it is the first thing she does
   on arrival. This replaces 910's `InMyArea` assumption. If she turns out to be a
   corpse, nothing is done. If the step does not finish within 15 seconds, the
   preparation gives up and the transition goes ahead:
   - still in the party (`CSR_IMSOA_FAILED` 5): the actions the preparation
     queued on her are cleared, and the host's transition hands her over like any
     companion: her gear goes through the party's import, and EET carries her
     into SoA as she is (choice 1 is not applied);
   - alive elsewhere (`CSR_IMSOA_FAILED` 1): SoA's fallback below banks her gear;
   - "Imoen2" no longer refers to an Imoen who joined the party
     (`CSR_IMSOA_FAILED` 4, another script replaced her): EET creates
     `IMOEN10`, and nothing of hers can be carried over.

   Cases 4 and 5 are reported once Imoen is in the party in SoA. Neither one
   triggers the fallback: in case 5 her gear was already handled, in case 4 it
   would strip the fresh `IMOEN10`'s own gear.
3. **Import:** for every item rule in the *effective* installed carrier
   (EET_end-generated from `K#IMPORT.2DA`, `IMPORT01-03.2DA` and `BDSODIMP`, plus
   other mods' additions), if she has the item and the party does not, add one
   copy to EET's `K#IMPORT` bag store and destroy hers. That is what EET's own
   rule does for the party (take, destroy, add to the store), so an imported item
   is not also banked.
   The rules are read from the installed script and verified at install time:
   when an import rule has an unexpected shape, installation stops instead of
   guessing.
4. **Bank** (one second later, so her own `DestroyItem` actions come first):
   `TakeCreatureItems("IMOEN2",0)` (0 = all items, including equipped ones) into
   the host's container.
5. **Choice 1 only:** strip ability-score effects (opcode 337 for opcodes 6, 10,
   15, 19, 44, 49, 97), read her base scores with `CheckStat`, and store each
   positive difference to the installed BG1 chassis (`IMOEN2.CRE`) as a tome
   boost.
6. **Every choice: she leaves.** Two seconds after the bank she removes herself
   (`DestroySelf()`, never while in the party), as the carrier removes every
   companion, and EET's `AR0602` brings her back the same way. Lab, 2026-10-18:
   an Imoen left alive in the area the transition starts from lost the actions
   `AR0602` queues on her before its `MoveGlobal` (her SoA dialog and scripts).
   She then started SoA with SoD's dialog and her BG1 script, and SoA's XP
   ladder never ran. Choices 2/3 with this step are covered by the installer
   tests only; their lab run is still open.
7. **Choice 1 only: a stand-in.** She also has to stop being an Imoen who
   joined the party, because only then does EET's `AR0602` create `IMOEN10`
   (`!BeenInParty("Imoen2")`). Destroying her is not enough (see "The problem"),
   so a stand-in takes her place in EET's list of global creatures
   (lab-verified, 2026-10-17):
   1. Once she has left the area, a stand-in is created from the installed
      `IMOEN10.CRE`, whose script name is `Imoen2` as well. "IMOEN2" now finds
      the stand-in first, because it is in this area.
   2. Only once the stand-in is seen in the area, it is given two actions:
      `MakeGlobalOverride()`, which replaces her in EET's global list, then
      `DestroySelf()`. The screen is black throughout (both hosts fade out
      first).
   3. The stand-in never joined the party, so `!BeenInParty("IMOEN2")` now
      holds. In SoA, `AR0602` creates its own `IMOEN10` and makes it global,
      which replaces the stand-in in turn.

   Every step has a 3-second timeout. A timeout clears whatever is still queued
   on "IMOEN2" (an action left on her would run when EET carries her into SoA;
   in the lab, two leftover `DestroySelf()` actions removed her again there and
   SoA's opening scene waited for her forever) and ends the preparation with the
   boosts pending. SoA then decides by who arrives (see below). Installation
   checks that `IMOEN10.CRE`'s script name is `Imoen2` and that it is not marked
   as having been in the party.

### In Shadows of Amn (`BALDUR.BCS`)

- **Choice 1:** once Imoen is in the party, add the stored boosts with
  `ChangeStat(..., ADD)`, but only to an Imoen without the SoD party mark the
  preparation gave her own Imoen (`K#PartySoD`, read with `NextTriggerObject`),
  that is to Shadows of Amn's `IMOEN10`. Each boost is capped at installation
  against the installed `IMOEN10.CRE` score, so no score passes 25. One-shot
  (`CSR_IMSOA_BOOST` 1 → 2). If the arriving Imoen still carries the mark, the
  swap failed and EET carried her own Imoen over: her scores already include
  the boosts, so she gets a report instead (`CSR_IMSOA_BOOST` 1 → 3).
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

- **Dead Imoen (OPEN, lab 2026-10-17):** EET's `AR0602` has no case for a dead
  Imoen who has been in the party: it neither brings her nor creates `IMOEN10`.
  SoA's opening scene gives control back through her
  (`ActionOverride("Imoen2",UnhideGUI())` in `NEWGAME`), so the game never
  returns control. Components 160 and 290 alone already lead there; vanilla
  never does, because SoD's own Imoen is not in the party at the end. 292-294
  leave a dead Imoen untouched. Open for Christopher: raise her at the handover,
  or keep a living Imoen a requirement of the ending.
- **Bedroom skip with an Imoen dismissed in BG1 (not lab-tested):** names
  resolve in the host's own area first. On the 910 route the host stands in
  `BD0103`, where component 160 keeps exactly one Imoen: the imported one, or
  the fresh `csrimo`. If an Imoen who joined in BG1 was dismissed there and
  never taken back, and `csrimo` was not recruited before the skip, "IMOEN2"
  finds `csrimo`, and the preparation leaves everything to EET, which carries
  the BG1 Imoen over as she is. The normal route stands in `BD4300`, where no
  Imoen waits, and finds her.
- **Kits:** no kit is stripped or validated against `DUALCLAS.2DA`; choice 3
  converts any thief kit (Christopher's requirement).
- **Tome boosts** are measured against the installed `IMOEN2.CRE` scores. Only
  increases count; exceptional strength is ignored. A mod that grants permanent
  ability effects instead of base-score changes is undercounted (effects are
  stripped before reading).
- **Two Imoen copies** cannot exist: in choice 1 the carried actor is no
  longer global once the stand-in has taken her place, and EET's `IMOEN10`
  replaces the removed stand-in in turn; in choices 2/3 she still has been in
  the party, so EET brings her back and creates no `IMOEN10`.
- **Leftover actions:** an action still queued on a removed Imoen runs when EET
  carries her into SoA. Every removal is queued once, and every timeout clears
  what is still queued before the transition goes ahead.

## Lab verification (2026-10-17/18)

Details: [playtest note](../../playtest/2026-10-17-imoen-soa-handover.md). In a
disposable copy of the CEBG install (EET, EEex, Spell Revisions, engine 2.7.3.0):

- **Choice 1** passes on both routes: an imported Imoen in the party, dismissed
  in another area or in the bedroom, and a recruited `csrimo` all arrive as
  `IMOEN10` with only `IMOENHP1` in the belt slot. Her tome boosts are applied,
  her gear is banked, and `RING25` goes to EET's import store. A never-recruited
  Imoen leaves the preparation idle, and the SoA fallback banks exactly her
  items.
- `MoveGlobalObject` brings an off-party Imoen from another SoD area.
- **Choices 2/3:** the first run of 293 (before step 6 existed) brought her own
  build with only `IMOENHP1` and her gear handled, but with SoD's dialog, her
  BG1 script and her SoD XP. Step 6 is the fix; its lab run, and choice 3's
  conversion in the lab, are still open.
- Without the preparation (160 and 290 alone), the opening scene completes too.
  A dead Imoen stops it (see Edge cases).
