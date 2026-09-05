# Optional SoD skip: isolated source prototype

This is **not an installable skip candidate**. The public remix installer and
v0.6.5 payload have not changed. Component 910's bedroom hook and EET equipment
adapter are not wired in. Do not pin this branch in CEBG or publish it.

**Native result, 2026-09-05: collection gate FAILED.** On the tested BG2:EE
2.7.3.0 / EEex 1.2.0 copy, imported tokens occupied a new source-named pile;
CSRBG1PILE remained empty, including after restart/reload. The banking step was
not run. See [the evidence report](engine-results-20260905.md). The instructions
below are retained as the reproducible probe, not a production recommendation.

Implemented here: the exact three-state question/confirmation dialogue and a
protagonist-only, once-guarded 250,000 XP action behind an unset item-readiness
gate. Tests compile those sources with WeiDU and replay their decompiled actions.
Replay across serialized test state is not an engine save/reload test.

## Native check required before handling imported ground loot

The proposed production approach adds one empty named ground-pile container at
BD0103 [190.540], the existing component-140 import point. Before relying on it,
prove that `CopyGroundPilesTo` merges all copied items into that named receptacle,
preserves its name on save/reload, and allows targeted `MoveContainerContents`.
If the engine creates a separate unnamed pile, this approach is rejected.

A separate **source-named** pile also rejects the approach; that is the result
actually observed. Do not assume its observed name identifies future imports.

The `csr-ground-probe` tail mod creates only **CSRGPA-D.ITM** and two new areas,
**CSRGP001/CSRGP002**, using the palace's existing background. It changes no
campaign script or area. All placed actors, triggers, scripted spawns, ambient
sounds, and area-script references are disabled in these two copies. Source
chest C and destination chest D are negative controls; A and B start on two
separate ground piles. Probe items are inert test tokens, not campaign rewards.

### Operator preparation (requires a coordinated game-test window)

1. Choose a **new disposable game copy and separate save profile**, not the live
   install, accepted v0.6.5 test copy/profile, or frozen collection build.
   Isolate Steam cloud integration too; a new engine_name/profile alone is
   insufficient on the tested 2.7 build. See the evidence report for the tested
   copy-local offline setup. Never change the user's global Steam settings.
2. Verify the resolved path and confirm its game and loader are closed. Copy
   only `csr-ground-probe/` into that disposable game. Create the intentional
   opt-in file `csr_ground_probe_disposable.ok` in that game root only after this
   path check. The installer refuses to proceed without it.
3. Tail-install `csr-ground-probe/setup-csr-ground-probe.tp2`, component 0. Do
   not uninstall existing WeiDU entries. Do not launch another game while Chris
   is playing; launch only after explicit coordination.
4. Use a throwaway save/character. Never overwrite a campaign save. Keep the
   original save as the reset point; this probe performs no campaign transition.

### Short engine sequence

Use the console in the disposable session:

```lua
C:Eval('LeaveAreaLUA("CSRGP001","",[190.540],S)')
```

After arrival has completed:

```lua
C:Eval('CopyGroundPilesTo("CSRGP002",[190.540])')
```

After a few engine ticks:

```lua
C:Eval('LeaveAreaLUA("CSRGP002","",[190.540],S)')
```

Save as **CSR ground copy**. Stop here and run the read-only verifier with
`--stage copy`. It must find exactly A+B in the **named CSRBG1PILE**, no C in the
destination, D unchanged, and no duplicate items. Reload that save and save a
second copy; the same verification must still pass. Only then try:

```lua
C:Eval('MoveContainerContents("CSRGP002*CSRBG1PILE","CSRGP002*CSRProbeBank")')
```

Allow ticks, save as **CSR ground bank**, and verify with `--stage bank`. Reload
and verify again. A+B must now be in CSRProbeBank, absent from the ground, with
both control chests untouched. These tests move items only between probe rooms.

Example verification, from this prototype directory:

```powershell
python verify_ground_probe.py 'D:\DISPOSABLE-PROFILE\save\NNN-CSR ground copy\BALDUR.SAV' --stage copy
python verify_ground_probe.py 'D:\DISPOSABLE-PROFILE\save\NNN-CSR ground bank\BALDUR.SAV' --stage bank
```

The paths above are placeholders, not instructions to choose a live profile.
The verifier reads two ARE entries in BALDUR.SAV entirely in memory and writes
only its JSON report to stdout. It does not operate or modify the game.

## Separate EET eligibility concern

The **effective** K#TELBGT.BCS on the inspected v0.6.5 test copy includes generated
`PartyHasItem -> TakePartyItem -> DestroyItem -> AddStoreItem("K#IMPORT",...)`
rules before the bulk BD6100 bank. The bare EET source template omits those
generated blocks. Therefore, transferring stored equipment directly into
BD6100*K#ImportContainer is **not sufficient proof** that it participates in the
normal import eligibility rules. An eventual adapter must preserve the effective
rules, duplication behavior and bag handling without patching K#TELBGT/AR0602 or
inventing destinations. That work remains open even after the ground probe.
