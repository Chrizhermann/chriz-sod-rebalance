# Ashatiel: an agreed party brawl

Status: **design discussion**, updated 2026-09-26. This records user decisions;
it is not an approved final roster, arena or implementation plan. The scope
anchor remains [the wishlist](../../01-remix-wishlist.md#ashatiel-chosen-of-cyric-style-party-fight--15).

## DECIDED: three distinct choices

Keep the original one-on-one duel and the option to reject its terms and fight
normally. Add the agreed group-versus-group brawl as a **third route**. Selecting
one route must not accidentally impose another route's rules or preparation.

The northern named adventuring party stays in place as its own encounter.
Do not merge it into Ashatiel's party, cut it, duplicate its members or rewards,
or begin reworking it now. A later light review is optional future work.

The new fight should feel like a fair, deliberate match between two parties.
It should be challenging through good builds, preparation and cooperation.
Discuss Ashatiel and each participating ally individually before finalizing
their equipment, spells, prebuffs, sequencers, potions and combat AI.

Use SCS Drasus and Chosen of Cyric principally as **questions to consider**:
distinct roles, starting defenses, finite resources/recasts, conditional target
selection, ally assistance, counters and rewards. The user explicitly does not
want their packages copied broadly across the group. Establish each current
build and actual AI behavior, then choose changes and scaling together.

## DECIDED: reset and preparation

On the agreed brawl route, **the player party is reset: dispelled and fully
rested before preparation**. The user's clarification makes clear that this
does not require literally dispelling/resting the enemies: they can be staged
ready for the encounter, with the intended resources and strong appropriate
prebuffs. This supersedes both the earlier preserve-player-buffs preference and
the unnecessary requirement for a symmetric enemy reset. Explain the player
reset before agreement.

**Latest staging decision:** the enemy group is already present, prebuffed and
hostile/red when the player-controlled preparation starts. The parties begin
out of sight of one another. If the player approaches and makes contact early,
the enemies attack immediately; preparation is not an invulnerable/non-hostile
grace period. Otherwise the enemy group advances/engages after the first few
rounds. Roughly 30 seconds remains the working timer baseline, with the exact
duration to confirm during design/testing.

This replaces the original spawn-after-preparation proposal. Delay the enemy's
planned advance, not its ability to react to early contact. The timer should
start when player control returns after setup, and must not reset on reload.
How the group shares an early alert and responds to an attack from beyond sight
is an AI implementation detail to resolve alongside its character scripts.

The old `BDCRUSDS` script assigns escort walking points toward the arrival lanes
and courtyard. Reusing that movement unchanged would undermine the new timed
advance. The brawl route needs encounter-owned waiting/advance behavior while
retaining immediate reactions to contact; do not achieve the delay by making
the group neutral, invulnerable or unable to respond.

Implementation research must distinguish the intended clean combat start from
indiscriminately deleting effects. Permanent kit/class features, item effects,
mod bookkeeping and companions must survive. The exact treatment of effects
that resist ordinary Dispel Magic, summons, familiars, temporary transformations
and remaining temporary conditions needs explicit verification/discussion.
Do not claim a generic dispel or rest action already fulfills this contract.

Full health and restored daily combat resources are the proposed interpretation
of a full rest; exact engine semantics and mod-granted abilities need checking.
No replenishment of spent potions, ammunition or charged items has been requested.
Any change to time-of-day or unrelated quest timers is a technical concern, not
an approved gameplay feature of the reset.

## DECIDED: arena qualities

- **Agreed direction:** use the **right-hand lane within candidate A**, the
  western tent court, following the user's acceptance of the lane comparison.
  The exact perimeter and starting positions still need verification; do not
  expand to both lanes or the entire court. Keep the northern enclosure intact.
- Make the arena small but not tiny: just enough separation for the two initial
  formations to be out of sight, with useful movement/cover within the lane.
  Do not enlarge it substantially beyond that requirement.
- The combatants cannot run out of the agreed match. Use visible wooden
  barricades at the relevant exits, with actual movement blocking and clean
  removal/unlocking when the match ends.
- Provide enough space and sight breaks for tactical movement and Hide in
  Shadows, without making a large chase arena. Hiding is legitimate in this
  party route and must not trigger the original solo-duel cheating rules.
- Remove/disarm any existing traps within the selected arena for the brawl.
  The user suspects the right lane has none; check actual regions and scripted
  activation rather than assuming it. This is not a blanket castle trap removal.
- Moving some existing actors is acceptable if necessary, but their encounters
  and later progression must remain functional. Do not treat this as approval
  to remove surrounding content.
- The user accepts additional map research and a small number of focused tests
  to get the first community-playtest draft right. No live-game action is
  requested in this research turn.

## DECIDED: victory and return to the siege

Once the party wins the group encounter, **remove the barricades and give the
same story outcome as winning the original duel against Ashatiel**. The visible
wooden barriers and their blocking geometry must both disappear/release; do not
leave invisible obstacles behind.

Victory means the brawl has been resolved, not simply that Ashatiel died while
her allies are still fighting. Exact roster-specific defeat/cleanup rules for
charmed, disabled or otherwise unresolved opponents remain to be specified.
Do not add a new surrender or escape route without discussion.

After arena cleanup, reuse the original successful-duel aftermath: the siege's
victory state, normal crusader retreat, journal and scene changes, and onward
progression to Caelar. Preserve the separate northern encounter as the original
duel route does. Gate/scene timing should follow that existing progression;
the request does not require instantly playing every later scene at victory.

The group route must not be treated as duel cheating or refusal. Its native
death-trigger consumers need to wait for group completion; setting the solo-duel
state during active party combat is not a substitute because it enables the
old cheating rules. Camera positions may need to match the new lane, while the
story result remains the successful-duel result.

Cleanup and the victory handoff run once and survive save/reload. Include an
Ashatiel-dies-first case in the later checks, plus a post-victory save/reload
confirming open passage and the normal next scene.

## Current discussion checkpoint (2026-09-26 handover)

The latest reference is [the per-character mechanical sheets](../../research/26-ashatiel-party-sheets.md),
recovered unchanged from the `claude/azure-teal-rebalance-b1ee87` worktree.
It extends the earlier audit with installed equipment/spell effects, consumable
counts, difficulty conditions and AI priorities. Calculated combat statistics
and the explicitly listed runtime uncertainties are not live-test results.

The user rejected abstract role alternatives and agent-selected design directions.
Use the concrete sheets to discuss each member's equipment, spells, prebuffs and
AI with the user. Earlier proposed role labels and scaling suggestions remain
unapproved; no answer about Ashatiel's role, roster size or new loadout is implied.

The user asked to keep this handover small because the next steps require their
design input. Resume the per-character discussion when they are ready; no further
research, encounter implementation or game testing is part of this handover.
The later final-fight/lift and other playthrough requests remain in
[the deferred follow-up list](10-playthrough-followups.md).

## OPEN: choices for the next discussion

1. Exact right-lane boundaries; which nearby actors, if any, must temporarily
   move or be held out of the fight; safe assembly positions for both parties.
2. Enemy roster and headcount. Ashatiel's existing six escorts are available
   candidates, but retaining all six is not yet decided.
3. Precise player reset and setup, summons/familiars, save/reload and effects
   that ordinary dispel cannot remove safely. Early contact is already decided
   to trigger combat; exact shared-alert logic and advance timing remain open.
4. Roster-specific completion detection and recovery for charmed/disabled
   opponents or interrupted progression. Barrier removal and the successful-duel
   aftermath are decided; Ashatiel's death alone must not end an ongoing brawl.
5. Each character's build, resources and teamwork, followed by difficulty and
   rewards. Do not assume RR's BG2 levels, spell packages or forced-cast cheats.

## Prepared evidence and next validation

- [Latest per-character mechanical sheets](../../research/26-ashatiel-party-sheets.md)
- [Complete current party dossier and scaling discussion axes](../../research/25-ashatiel-party-dossier.md)
- [Exact current builds, inventory and spell counts](../../research/25d-ashatiel-party-resource-ledger.md)
- [SCS Drasus / Chosen of Cyric design checklist](../../research/25c-scs-drasus-design-checklist.md)
- [Map and resource triage](../../research/24-ashatiel-map-triage.md)
- [Current encounter sequence](../../research/24a-ashatiel-sequence.md)
- [Both existing rosters](../../research/24b-ashatiel-roster.md)
- [Chosen of Cyric reference](../../research/24c-chosen-of-cyric-reference.md)
- [Alternative arena geometry](../../research/24d-ashatiel-arena-candidates.md)
- [Reset and physical boundary feasibility](../../research/24e-ashatiel-reset-and-boundaries.md)
- [Left/right single-lane comparison](../../research/24f-ashatiel-single-lane.md)

The initial September 26 research compared the western tent
court (less displacement, potential hiding terrain) and central courtyard
(more continuous open floor, many existing named assault actors to stage).
The [study map](%USERPROFILE%/CEBG-Tests/Ashatiel-20260922/map/BD4000-arena-options.png)
shows their approximate inspection bounds, not approved barricade positions.
The southeast enclosure already contains Gnarg's group and returning ogres;
it is not an empty alternative. Neither shortlisted site has been tested live.
The user subsequently narrowed the brief to one side lane of the western
candidate A and accepted the right-lane recommendation. Central court B is now
only a fallback research reference, not an equally active design option.

The western candidate contains the original invisible duel obstruction,
`Door07`, plus assault traps. Those must be handled only for the new route and
kept correct for the old duel/refusal. The physical inner castle gate is
`Door01`, a different object. This corrects earlier loose references to Door07
as the inner gate. The map's wooden wall-breach sequence provides an existing
visual/collision reference for researching new barricades, not a ready-made
new arena boundary.

The reset research supports prototyping player-actor rest with explicit full-HP
restoration. An ordinary guaranteed dispel cannot remove undispellable buffs;
stronger cleanup needs a focused compatibility sample before it is selected.
Restoration and effect cleanup remain setup mechanics for the agreed route,
not changes to the player's normal rest or kit systems.

The original siege concludes on Ashatiel's death alone. The group route needs
its own completion condition integrated with gate opening, army retreat and
Caelar's next scene while preserving the two original routes. Its new barricades
must not recreate the bridge's temporary invisible-wall problem.

Before public testing, verify the player reset, both initial formations being
outside each other's actual sight, early-contact aggression, timed enemy advance,
movement around every boundary, hiding, trap removal, visible/collision barrier
removal, successful-duel aftermath, both original alternatives, and save/reload
at meaningful stages. Existing static research is not proof
of live pathfinding, balance or mod compatibility.

## Deferred notes

The user's other playthrough observations are captured in
[the follow-up queue](10-playthrough-followups.md). They remain behind Ashatiel.
