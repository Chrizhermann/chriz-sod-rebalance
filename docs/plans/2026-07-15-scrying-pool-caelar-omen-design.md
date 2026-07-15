# Dig-site scrying pool: single Caelar omen

**Status:** approved by the user on 2026-07-15.

## Purpose

Replace the dig-site scrying pool's three oversized Beamdog vision cutscenes with one short,
text-only omen about Caelar. The item hunt remains, but every item is required for the single
payoff. The result must work whether Imoen is in the party, must not constrain the later Caelar
arc rewrite, and must leave no reachable path into the retired cinematics.

## User decisions

- The Imoen vision is removed. It is incoherent when component 160 allows Imoen to be standing
  in the party.
- The Hooded Man vision remains removed by component 120.
- The original Caelar cinematic is removed. No teleport, staged army, spawned actors, forced
  dialogue, or cutscene chain survives as reachable content.
- The pool gives one vague, text-only Caelar omen.
- The player must collect and expend **all three Silver Scepters (`BDMISC55`) and both Essences
  of Clarity (`BDMISC59`)**.
- The `BDWIGHDD` trash encounter remains cut. Its missing Essence is re-homed into an existing,
  sensible BD1200 container rather than restoring the creature.
- The pool becomes permanently exhausted after the omen.

## Player flow

1. The player finds the three Silver Scepters and both Essences of Clarity in BD1200.
2. The three scepters are inserted into the pedestal through the existing interaction.
3. The completed pool accepts the two Essences only when the party has both. Both are consumed
   as one final activation cost.
4. The pool presents one short narrative-text omen, with no choice menu and no cutscene:

   > The water clears. A woman in argent armor stands before a door beneath the world.
   > Something waits beyond it—something she knows, or believes she knows. She reaches out.
   > For an instant, you cannot tell whether she is opening the way or being drawn through.
   > Then the water clouds.

5. The pool records completion before awarding anything, pays the combined surviving vision
   reward once, settles into a dormant state, and cannot be activated again.

## XP policy

- Preserve the existing +3,000 party-total reward for completing the three-scepter pedestal.
- The post-component-120 pool has two intended surviving visions, each worth +500 to every
  player slot. The single omen therefore grants **+1,000 to each of Player1–6** once.
- This combines the removed Imoen and old Caelar vision rewards instead of creating an XP loss
  or an additional ledger entry.

## Clean removal surface

The implementation must make every old route unreachable:

- Imoen picker replies and `BDSCRY01`/`BDSCRY02` launch path.
- Original Caelar picker replies and `BDSCRY03`/`BDSCRY3A`/`BDSCRY04`/`BDSCRY4A` launch path.
- Hooded Man picker replies and `BDSCRY05`/`BDSCRY06`, already gated by component 120.
- The old repeatable picker/re-cloud loop and its per-vision Essence consumption.
- The old shared cinematic teardown/reward route through `BDSCRY07`.
- Any reachable area transition, cutscene-mode entry, actor creation, ambient-state loop,
  dialogue continuation, or retry path belonging only to those visions.

The retired game resources stay on disk as unreachable dead code. Deleting or wholesale-
replacing `BDSCRY.DLG` would be unnecessarily fragile and could break third-party dialogue
patches, including Aura's interjection from BDSCRY state 0.

## Compatibility and implementation constraints

- Patch narrow entry points and transitions; do not replace the full dialog resource.
- Preserve unrelated BD1200 object-script behavior and third-party dialog additions.
- Use a once-first completion flag so retries, interrupted dialogs, or repeated clicks cannot
  duplicate XP or consume items twice.
- Do not enter cutscene mode. CUTSKIP has no role in the replacement.
- Keep the solution valid for both EET and standalone BG:EE+SoD.
- Implement as a new tail component after the components whose behavior it supersedes, rather
  than rewriting their WeiDU history.

## Verification requirements

- Audit every reference to `BDSCRY*`, `BDODSCRY`, `BD_SDDD12_*`, `BDMISC55`, and `BDMISC59` in
  the source corpus and installed resources before finalizing the patch.
- Confirm exactly two reachable Essence sources after installation and zero restoration of
  `BDWIGHDD`.
- Decompile the installed dialog and scripts to prove that only the new omen can launch.
- Verify three-scepter completion, two-Essence gating/consumption, single +1,000-per-slot award,
  permanent exhaustion, save/reload persistence, and absence of cutscene mode or area travel.
- Confirm the existing hooded-man removal and Aura compatibility remain intact.
