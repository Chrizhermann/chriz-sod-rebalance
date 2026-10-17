# Imoen's handover into Shadows of Amn — lab verification

Components 292 / 293 / 294 (v0.6.14, unreleased), design
[12-imoen-soa-handover](../design/wave1/12-imoen-soa-handover.md). Tested on
2026-10-17/18 in a disposable copy of the CEBG install (`ImoenSoA-Lab-20261017`:
450 WeiDU entries with EET, EEex 1.2.0, Spell Revisions 4.21, the remix with 160,
290 and 910; engine 2.7.3.0). The game ran only through the quiet lab runner
(hidden desktop, muted, holding the shared install lock). The live installs and
Christopher's own game were not touched.

## Method

Every scenario loaded a profile save from one lab game and prepared its case
through the EEex remote console. It then ran component 290's ending by queueing
Dazzo's actual reply actions (or 910's bedroom skip), followed SoA's opening scene
until Imoen had joined in `AR0602` and the controls were back, and saved. A parser
then read the save: the party, Imoen's creature, `AR0602`'s import container and
EET's `K#IMPORT` store. A lab-only Lua trace logged every action Imoen started,
plus a once-a-second record of the creature "IMOEN2" resolved to.

The main save ("S1 setup") has the imported BG1 Imoen in the party: thief 9 with a
third-party thief kit (`C0TRICKS`), her own belt (`BELT02`), `RING25` (on EET's
import list), tome boosts DEX +1 / CON +2, and a temporary STR +3 effect. The
second save has Imoen never recruited (the BG1 Imoen in `BG2700`, 160's `csrimo`
in the palace bedroom).

## Engine behaviour that shaped the design

- **A destroyed Imoen comes back.** `DestroySelf()` takes a global NPC out of her
  area, but she stays in the game's list of global creatures, still marked as
  having been in the party. Any `MoveGlobal` into another area revives her, and
  EET's `AR0602` does exactly that for every Imoen who has been in the party and
  is not dead. So removing her never makes EET create `IMOEN10`.
- **Her queued actions come back with her.** The first version of choice 1
  queued its removal more than once; in SoA the trace showed the leftover
  `DestroySelf()` actions run again on arrival, and the opening scene then
  waited for her forever. Now every removal is queued once, and every timeout
  clears what is still queued.
- **A stand-in works.** A creature made from `IMOEN10.CRE` (script name `Imoen2`)
  in the same area, given `MakeGlobalOverride()` and then `DestroySelf()`,
  replaces her in the global list. It never joined the party, so `AR0602` then
  creates its own `IMOEN10`.
- **EET's SoD-party mark is needed.** Without `K#PartySoD`, `LeaveParty()` made
  the imported Imoen vanish at once, gear included (EET's `IMOEN_` script).
- **Her post-party dialog opens at once.** Rejoining through it in the middle
  of the handover left an empty party portrait in SoA, so the dialog stays
  closed while the preparation runs.
- **An area finds one creature per script name.** In a state that breaks 160's
  one-Imoen-per-area rule (the lab's own setup: its "S1" Imoen was added to a
  fresh-start game, whose `csrimo` still stood in the bedroom), "IMOEN2" in
  `BD0103` found `csrimo`. Once `csrimo` was removed, it found nobody until the
  party left and re-entered. A normal game never gets there, because 160 removes
  the bedroom's own Imoen before the imported one enters.
- **SoA's opening scene needs a living Imoen.** `NEWGAME` gives control back
  through `ActionOverride("Imoen2",UnhideGUI())`.

## Choice 1 (292)

| Case | Route | Result |
|---|---|---|
| Imported, in the party (S1) | ending | `IMOEN10` joined with DEX 19 / CON 18 (her +1/+2 tome boosts); she carries only `IMOENHP1`, in the belt slot. Her SoD gear is in `AR0602`'s import container, `RING25` in EET's import store. |
| Imported, dismissed and unmarked in `BD4400` (S2) | ending | Brought to `BD4300` first; same result. |
| Never recruited (S6) | ending | Preparation idle; EET's own `IMOEN10`, no boosts. |
| Fresh `csrimo` recruited, given a belt and `RING25` (S7) | ending | Swapped like the imported Imoen; `IMOEN10` without boosts (`csrimo` has the chassis scores); gear banked, ring imported. The never-recruited BG1 Imoen stays in `BG2700`. |
| Preparation could not reach her (S9: dismissed in `BD4500`, marked unreached) | ending | EET carried her BG1 build. The SoA fallback banked exactly her items (`BELT02`, `BOW05`, `WAND03`, `RING25`, arrows, potions) and gave her a fresh `IMOENHP1` in the belt slot; the report was shown. |
| Imported, in the party (S8) | 910 skip | Same as S1 (`IMOEN10` with boosts, only `IMOENHP1`, gear banked, `RING25` imported). |
| Imported, dismissed in the bedroom (S8b) | 910 skip | Same. |
| No preparation, as with 160 and 290 alone (S11) | ending | The carrier removed her like any companion; EET brought her BG1 build back with only `IMOENHP1`; the opening scene completed. |
| Imoen dead in the party (S10) | ending | **Soft lock.** `AR0602` neither brings her nor creates `IMOEN10`, and the opening scene never gives control back. 160 and 290 alone lead here too; open design question. |

SoA's join ladder gives the arriving Imoen 1,000,000 XP (1,250,000 after 910's
skip). The two 910 rows needed the lab state fixed first (the stray `csrimo`
removed and the bedroom re-entered, see above); with the stray `csrimo` still
there, the preparation left the BG1 Imoen to EET.

## Choices 2 and 3 (293, 294)

The first run of 293 (S1, before the fix): her own build arrived (thief 9 with
her kit and tome boosts) with only `IMOENHP1` in the belt slot, her gear banked
and `RING25` imported. But the preparation had left her alive and dismissed in
`BD4300`, and of the actions `AR0602` queued on her only those after its
`MoveGlobal` ran. Her SoA dialog and all five `ChangeAIScript` calls were lost:
she kept SoD's dialog (`CSRIMOEN`, offered in SoA's opening conversation) and
her BG1 script (`IMOEN_`), and SoA's XP ladder never ran (150,000 XP). In S9
(dismissed in another area) and S11 (removed by the carrier) every action ran.
Fix: after the bank, every choice has her remove herself like any companion,
and EET brings her back the same way.

With the fix (2026-10-18), choice 2 (293):

| Case | Route | Result |
|---|---|---|
| Imported, in the party (S1) | ending | Her own build: thief 9 with her kit, DEX 19 / CON 18 (her tome boosts), SoA's dialog (`IMOEN2J`) and script (`IMOEN`), 1,000,000 XP from SoA's join ladder. Only `IMOENHP1`, in the belt slot; her gear banked, `RING25` imported. |
| Imported, dismissed and unmarked in `BD4400` (S2) | ending | Brought to `BD4300` first; same result. |
| Fresh `csrimo` recruited, given a belt and `RING25` (S7) | ending | Her own build (thief 2, the chassis scores), handed over the same way. The never-recruited BG1 Imoen stays in `BG2700`. |
| Preparation could not reach her (S9) | ending | As in choice 1: the SoA fallback banked exactly her items and gave her a fresh `IMOENHP1` in the belt slot; the report was shown. |
| Imported, in the party (S8) | 910 skip | As S1, with 1,250,000 XP. |
| Imported, dismissed in the bedroom (S8b) | 910 skip | Same. |

Choice 3 (294), each SoA save also reloaded and run 30 more seconds:

| Case | Route | Result |
|---|---|---|
| Imported, in the party (S1) | ending | Dual-classed: mage/thief with thief as the original class, thief 9 and her kit kept, mage 1 with SoA's 1,000,000 XP to level up, `IMOEN10`'s 24 known wizard spells (the same list). Only `IMOENHP1`, in the belt slot; her gear banked, `RING25` imported; SoA's dialog and script. |
| The same Imoen without a kit (S5) | ending | Same conversion, no kit. |
| Never recruited (S6) | ending | EET's own `IMOEN10` (already mage/thief), left unchanged. |
| Fresh `csrimo` recruited, given a belt and `RING25` (S7) | ending | Same conversion at her thief level 2. |

After the reload nothing changed; she was not converted a second time.

## Coverage and limits

- Spell Revisions was installed in the lab; without it, only the synthetic
  installer tests ran (all 388 main and 41 research tests pass).
- One thief kit (`C0TRICKS`) in the lab; without a kit, see choice 3.
- Choice 3 ran on the ending route only; its preparation is choice 2's, which
  passed on both routes. Her new mage levels were not taken through the
  level-up screen.
- Not run: a BG1 Imoen dismissed in BG1 and never taken back, together with
  910's skip and an unrecruited `csrimo` (see the design doc's edge cases).
