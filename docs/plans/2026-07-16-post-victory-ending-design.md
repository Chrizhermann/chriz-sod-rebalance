# Post-victory ending: short celebration and direct campaign handoff

**Status:** approved by the user on 2026-07-16; not yet implemented.

## Purpose

End Siege of Dragonspear immediately after a short, playable victory celebration. Remove the
Skie murder, Irenicus framing, arrest, trial, jail, escape, reunion, and Shadow-Thief ambush
without disturbing the party, inventing a replacement explanation for BG2, or losing EET import
data. Standalone BG:EE+SoD receives the same narrative ending and then uses its native campaign
termination.

The later Caelar/Avernus rewrite remains a separate feature. This design begins after the
current final battle has already resolved and the party returns from Avernus.

## Player flow

1. Preserve `BDCUT59`, `BDCUT59A`, and `BDCUT59B`. They return and stage the party in the
   Dragonspear courtyard, `BD4300`, exactly where the victory already lands.
2. Keep the existing one-line party victory barks, but compress their pauses to roughly two
   seconds so the procession reads as a brief celebration rather than another cutscene.
3. Keep de Lancie's public victory acknowledgment (`BDDELANC` states 77–83).
4. Keep Bence Duncan's cheer and acknowledgment (`BDBENCE` states 64–65). After state 65 he
   restores the soldier ambience, leaves, and exits dialogue. He never asks the player to check
   on Skie.
5. Return control in `BD4300`. The player may speak to the assembled characters, loot, manage
   the party, save, and reload.
6. Sergeant Dazzo's existing rest conversation is available as the deliberate campaign endpoint
   only at `bd_plot=590`. Both accepted rest routes erase the celebration journal, fade out, and
   invoke the appropriate platform handoff exactly once.

There is no replacement kidnapping, unexplained defeat, forced companion farewell, romance
finale, or new narration. The short celebration is the coda.

## Clean removal surface

The implementation makes the following content unreachable while leaving retired resources on
disk for WeiDU reversibility and third-party compatibility:

- Bence state 66 ("check on Skie") and every murder/arrest branch downstream from it.
- de Lancie's private Waterdeep proposition (`BDDELANC` states 95–104). Her public victory
  acknowledgment remains.
- Corwin's and Neera's forced post-victory romance finales in `BD4300`, plus every other optional
  `bd_plot=590` coda. Ordinary earlier romance content is outside this component.
- `BDCUT60` onward: sleep, murder dream, Skie's corpse, Irenicus, arrest, companion stripping,
  trial, jail, escape, sewers, canon-party reunion, `BDCUT65`, and the `BD6100` ambush.
- Production and debug launchers into that retired band, including the Dazzo `BDCUT60` actions.
- The three Hooded-Man tavern rumors in `BDRUMOR3` states 7, 20, and 37.
- All remaining live SoD references to Entar. His retired CRE/DLG may remain inert; removing a
  resource file is not the goal.

Murder and arrest roots are false-gated at their entry points, not merely bypassed by the happy
path. CUTSKIP responses 51 and 67 become unreachable and may remain unchanged. Response 59 is
still live because `BDCUT59` is preserved. Responses 52 and 65/66 belong to the later
Caelar/Avernus rewrite, not this cleanup.

The earlier chapter-7/8 Coalition, refugee, and Tiax content in dual-use `BD0104` is unrelated
and must remain intact.

## Party and romance continuity

- The current party remains assembled through the celebration and until the platform handoff.
- Skie survives and stays in the party if present. No corpse, murder flag, arrest reaction, or
  companion horror bark is reachable.
- Imoen may be physically present in the party. No scene assumes that she is elsewhere.
- Mod NPCs, unusual party compositions, solo parties, dead-but-in-party companions, and
  multiplayer parties use the same endpoint.
- Removing Neera's SoD finale does not synthesize a completion state. Leave
  `bd_NeeraRomance6=0` and do not map or modify `bd_neera_romanceactive`.
- The SoD variables above are separate from BG2's `NeeraRomanceActive`, `NeeraLovetalks`, and
  EET/BG1 history variable `NEERA_ROMANCE`. The installed EET handoff contains no bridge between
  them, so the removed SoD coda does not block Neera's BG2 romance.

## EET handoff

The hard invariant is **not** that the party must enter `BD6100`. It is that the inventory bank
must reach `BD6100*K#ImportContainer`, because BG2's installed `AR0602.BCS` reads from that exact
area-qualified container.

The EET branch therefore:

1. Adds one invisible, empty container named `K#ImportContainer` to `BD4300` before that area is
   first visited.
2. At tail-install time, clones the **currently installed** `K#TELBGT.BCS` and `K#TELBGT.CRE`
   into private eight-character resources. This preserves every installed third-party capture,
   item-sweep, inventory, and campaign-transition addition.
3. Retargets only the cloned CRE to the cloned script.
4. Changes only the clone so that, after it banks the party into the local BD4300 container and
   before its normal movie/campaign move, it performs:

   `MoveContainerContents("BD4300*K#ImportContainer","BD6100*K#ImportContainer")`

5. Dazzo creates the cloned carrier in `BD4300`; the clone performs the installed EET handoff
   without ever loading the party into `BD6100`.

The original `K#TELBGT.BCS`, `K#TELBGT.CRE`, `AR0602.BCS`, `BD6100` resources,
`CAMPAIGN.2DA`, `STARTARE.2DA`, and `ENDOFBG1` remain byte-for-byte untouched. The ambush and
`sodcin05` are not played.

Installation must fail loudly if the EET resource set is partial, expected anchors drift, the
BD6100 destination container is absent or ambiguous, or BD4300 already contains a conflicting
container. At runtime, a missing local BD4300 container must abort visibly **before** any gear is
taken or campaign transition begins. This protects saves in which BD4300 was already baked before
installation. The component is intended to be installed before the next playthrough's first
BD4300 visit.

## Standalone handoff

On native BG:EE+SoD, Dazzo fades out and invokes the verified native terminal actions directly:

`EndCutSceneMode()`, `ContinueGame(FALSE)`, then `EndCredits()`.

No EET resource is required, `BD6100` is never loaded, and the removed ambush movie is not
replayed. A partial EET signature must be treated as an installation error rather than silently
falling back to this branch.

## Compatibility constraints

- Implement as a new tail component; never uninstall or rewrite an earlier WeiDU.log entry.
- Detect the complete EET handoff resource family by installed content, with loud rejection of a
  partial family. Do not rely on a game-name predicate alone.
- Patch narrow dialogue states, transitions, and launch blocks. Do not replace whole DLG/BCS
  resources or delete retired assets.
- Preserve third-party modifications by cloning installed resources, not a bundled vanilla copy.
- Count-guard every expected patch anchor and verify the live celebration path remains intact.
- Saves with an already visited BD4300 cannot acquire the new ARE container automatically; they
  are unsupported for the successful transition but explicitly covered by the safe runtime guard.

## Verification policy

First-party verification covers both supported platforms, asymmetrically:

- **EET:** static semantic verification plus a thorough runtime matrix: full party, solo,
  Imoen+Skie, a mod NPC, a dead in-party companion, empty/equipped/full/bagged inventories,
  save/reload during the playable celebration, repeat-use protection, and multiplayer smoke.
  Marker items must arrive in AR0602 with exact eligible-item multiset equality, and BD6100 must
  not be loaded as part of the new route.
- **Guard case:** a save with BD4300 already baked must stop visibly before banking, retain all
  gear, preserve control, and remain save/reload-safe.
- **Standalone:** one first-party staged `BD4300 -> Dazzo -> credits -> menu` runtime smoke on a
  disposable clone of a real merged SoD install.

Discord, stream-viewer, and broader community testing are welcome additional coverage, but they
do not replace the first-party standalone smoke or the EET matrix.
