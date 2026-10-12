# Avernus: interim portal and final battle

Design accepted in the September 28 discussion, including the final constraint:
Hephernaan must remain manageable below Insane. This is a small temporary cleanup
before the later Caelar finale. No extra challenge checkbox or new boss phases.

## Agreed behavior

- The lower tower switch becomes a one-way portal into the existing confrontation.
  Skip the lift ride and its battles with no replacement XP. Keep the normal
  confrontation and victory/ending sequence.
- Belhifet requires +1 weapons, has 60% magic resistance and 25% extra movement
  without Haste or extra attacks. Keep his existing 25% melee physical and 50%
  missile resistance.
- HP targets on the audited 350-HP creature are 350 Easy, 400 Normal, 450 Core,
  475 Hard and 500 Insane. Apply the modest additions once; do not replace the
  engine's separate Legacy of Bhaal bonus or heal him repeatedly.
- Remove the mass dispel opener. First targeted Breach is eligible after three
  rounds; repeat no faster than four rounds below Insane or three on Insane.
  Easy receives no added Breach. Limit pursuit to one attack round after a
  nearby visible protected target is selected; suppress chasing teleport during
  that opening. Use the installed Breach spell and its protection interactions.
- Keep two opening devils on Core and four on Hard; reduce Insane from six to
  four. Reinforcements fill only vacancies under those living caps, one at a
  time. Core retains its below-half-health gate and five-round interval; Hard
  retains its below-75%-health gate and four-round interval; Insane has a
  four-round interval. Easy/Normal keep their absence of these reinforcements.
- Belhifet keeps the native offensive abilities and gets one defensive
  invisibility use, leaving more opportunities for his other actions.
- Hephernaan keeps his devil appearance and becomes a 14/14 cleric/mage with
  a finite supported spellbook. Core and lower have Stoneskin, Mirror Image
  and Armor of Faith, with no reserve Stoneskin/Mirror Image. Insane adds
  Minor Globe and Free Action, plus bounded reserves when supported by the AI.
  No contingencies, sequencers, HLAs, mass dispel or unlimited preparation.

## Implementation and acceptance

Component **285**, following 280 and preceding the ending components. It uses
owned item, reinforcement and final-form clones; original caster/transform
resources retain their other uses. The SCS combat donor is resolved from the
installed cleric/mage, with a native SoD script fallback. The selected spells
must have matching donor branches and stay within the level-14 slot budget;
installed SPELL.IDS resolves SR spell identities.

Install before first entering BD4700, preferably with a save before entering
BD4600. Existing saved actors and area data can retain their old resources.
Only disposable offline fixtures are used during implementation. Native
acceptance remains a focused portal/confrontation check and Core/Insane combat
check, including Hephernaan's casting, the add cap and Dispelling Screen against
Breach. Static installer success does not establish runtime balance.

### Offline verification, 2026-09-28

All **16 focused checks passed** using WeiDU246: component ordering, portal
preservation and rejection checks, full public component installation with the
installed SCS donor and the native caster fallback, generated statistics and
spellbooks, difficulty-dependent opening rosters, and failure/reapplication
guards. The effective resources were read from the existing EET installation
and copied into disposable fixtures; no game installation or save was modified.
The existing boss changes weapon slots, so its difficulty-dependent weapon
selection still uses the patched item clones. `git diff --check` was clean.

To repeat from the worktree, set `CSR285_SOURCE_GAME` to a read-only reference
game directory and run:

```text
python -m unittest tests.test_component_order tests.test_comp285_portal tests.test_comp285_installer -v
```

The native fallback check uses the same installed spell resources with the SCS
donor absent; it is not a clean BG:EE or unmodified-spell compatibility test.
