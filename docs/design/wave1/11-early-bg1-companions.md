# Early BG1 companion recruitment in SoD

Captured from the user on **2026-10-04**, with same-day follow-up approval.
**Roster and broad placement groups APPROVED; exact locations, dialogue wording,
and implementation design remain OPEN.** This develops the
previously deferred step 2 of [keep all companions](02-keep-companions.md).
No implementation, installation, or runtime testing was performed for this note.
No release or priority change relative to Ashatiel was agreed.

**Validation direction, user follow-up 2026-10-04:** keep this work lightweight.
Do not build a large test/review suite or require a separate exhaustive playtest.
Use basic compile/parse checks and a focused code review; add a small targeted
test only where it materially helps catch a consequential error. The user will
check recruitment and behavior during the next overall installation/playthrough,
and fixes can follow observed problems. Do not install or run live game probes
as part of this planning discussion. Remaining runtime checks are deferred, not
already passed and not implementation blockers.

## DECIDED direction from the user

- Include most, preferably all, BG1 companions who survived BG1. Exclude someone
  only for a convincing lore/continuity reason, not because they lack SoD banter
  or overlap another companion's class.
- Make them available in the city and early SoD, as early as makes sense. A fresh
  SoD start needs useful recruitment choices before the replacement Korlasz fight.
- Keep the first version simple: standing NPCs, a very short conversation, join,
  decline, and ordinary re-recruitment. No new companion questlines required.
  **Follow-up approved:** inspect each existing cameo's dialogue when working on
  that companion, especially Coran and Garrick. Keep worthwhile lines that still
  fit, cut contradictory or excessive fluff, and aim for a short exchange like
  Skie's. This is not a requirement to preserve every existing line or create a
  larger writing project.
- Preserve the companion and equipment the player left behind in BG1 where that
  saved actor is available. Otherwise use modest, BG1-like starting equipment.
- **Dismissal decision, follow-up 2026-10-04:** previously recruited companions
  supported by this feature follow the army to the next camp when dismissed.
  They must remain available as the earlier city/road areas become inaccessible.
  Unrecruited companions stay at their original recruitment locations. Preserve
  the dismissed actor's build and possessions; do not create fresh replacement
  copies, resurrect dead companions, or relocate current party members.
- Move Skie's availability to **before the first palace rest**, on the same floor
  and at the same location as her current palace-hall appearance. Check her lines;
  use a small before/after-rest or before/after-council branch where necessary.
- The user's leading candidates were the male elf with Safana at the tavern
  (interpreted as **Coran**, rather than Corwin), Yeslick, and possibly Xan.
  The follow-up approved the full grouping below, including Xan. References to
  the male Elfsong companion as "Corwin" are understood as Coran; Corwin is the
  separate existing SoD companion.

## Current behavior checked against source

- The old wishlist and wave-1 companion plan already recorded optional non-party
  pickups as step 2; the September player-roadmap snapshot omitted them. Component
  110 keeps the imported party. It is not a general early-recruitment system.
- Fresh-start solo arrival is intentional (component 145). Imoen's component 160
  gives a bedside join option at initial palace arrival. **Correction after the
  user's follow-up:** with component 180, city exploration is NOT available on
  the opening evening. `baf/csrceleb.baf` locks both outside palace exits at plot
  50 and restores them after the first rest. The earlier statement relied on an
  older paragraph in the prologue design and missed the later door-lock change.
  Minsc, Dynaheir and Safana can be recruited on the subsequent city outing;
  earlier Skie would help with a first-evening Korlasz fight.
- Skie's component 197 currently retains the council spawns. Its palace meeting
  explicitly requires `bd_plot_003(BD0102)=2`, after the council. Existing lines
  refer to the council, going after Caelar, and marching north soon. These are not
  all suitable at first arrival.
- Coran and Garrick already have city cameos at the Elfsong. Coran recruitment
  must work independently of the Safana argument: `baf/skip0110.baf` correctly
  marks that scene resolved when Safana is already in the party.
- The inspected read-only reference installation log contains Xan for BGII v19,
  YeslickNPC v5.0, AjantisBG2 v21 and Branwen BG2 v8pre. This verifies that log's
  installed mods, not automatic cross-campaign identity/gear continuity or the
  stack used by a different game profile. Their existing behavior must be respected.
- Current source already protects the known `O#XAN` and `LK#YESLK` identities
  from the palace party strip (`lib/comp110_aliases.tpa`). This is useful prior
  work, not a general actor lookup or fresh recruitment implementation.

Sources: `docs/01-remix-wishlist.md` (July 3 step 2 and July 6/7 fresh-start
decision); `docs/design/chapters/01-prologue.md` sections 4, 5, 10 and 12;
`chriz-sod-remix/dlg/csr197skie.d`; `chriz-sod-remix/languages/english/csr197skie.tra`;
`chriz-sod-remix/lib/comp197.tpa`; `chriz-sod-remix/baf/skip0110.baf`;
historical decompiles `research/data/sod_baf/BD0109.baf` and `BD0110.baf`.
Historical decompiles are reference data, not proof of the current installed bytes.

## Opening order and delayed-Korlasz defect (source-verified)

- The player is not required to enter the prison or defeat Korlasz before the
  first rest. `dlg/csrserv.d` offers bedtime without a Korlasz-death condition;
  component 150's night block requires only that choice and the early plot state.
- With the full opening, the player can explore the palace and fight Korlasz
  that evening, or sleep, attend the council, explore/recruit in the city, then
  return to the prison. The stairs warning in `baf/jbhint.baf` is proximity-based
  and remains eligible at plot >49; it arms the breakout for the descent.
  Ordinary arrival in the palace does not itself force the prison fight.
- **Defect, not a verified equivalent later route:** `baf/csrceleb.baf` only
  creates Liia's post-Korlasz return/reward beat at plot 50. `baf/csrliiax.baf`
  additionally removes that Liia when the plot leaves 50. Component 175 pays
  the agreed 22,000 XP per character through this return dialogue; component
  176 only repairs the amount and does not add a later delivery route.
  Therefore a fight deferred until after the rest currently misses this custom
  reward path according to source. No alternative late path was found.
- **Follow-up to fix during implementation:** make the delayed city-phase fight
  receive the same single reward without duplicating or disrupting council Liia.
  Preserve the player's choice of when to enter the prison. This is a tracked
  source defect, not a repair already implemented or a runtime playtest result.

## Liia reward and bedroom rest: follow-up direction

**User direction, 2026-10-04:** the missed reward is important. Add reporting to
Liia's ordinary conversation when Korlasz has been defeated and the reward has
not yet been received. The journal should direct the player to report success
to Liia. The user also favors unlimited, convenient bedroom rests to prepare
newly recruited companions' spells before Korlasz, with a click or servant
conversation and no additional story advancement.

### Reward implementation shape

- Keep one completion/payment check shared by the existing first-evening beat
  and the later normal Liia conversation. The current `CSR_KORL_RET=2` records
  completed reporting; `<2` covers both a late kill with no return actor spawned
  and an early return actor that disappeared before the player collected XP.
- The new normal-talk offer needs Korlasz defeated, reporting unpaid, and the
  council completed. It must not take priority over the forced council opener.
  Use a short context-neutral acknowledgement for the later route; the existing
  "twice in one night" / "celebration" wording does not fit it.
  Cover departure-day Liia too; attaching only to her ordinary pre-departure
  greeting would leave another timing gap. Normal conversation remains available.
- Liia is not one persistent actor throughout the opening. Celebration and early
  return copies remove themselves; the council creates the regular hall Liia.
  Preserve the early route and add the later route to that ordinary dialogue;
  do not remove the normal Liia or spawn an extra copy just to award XP.
- Keep the existing 22,000 XP per present party member, paid once. Returning to
  Liia, changing party membership or save/reload must not allow another award.
  Existing completed-report saves must remain paid; the 0/1 unpaid cases need
  coverage on installation into a city-phase save.
- The current kill event already marks "Sarevok's Servant" completed. Update
  the journal progression coherently: defeat -> report to Liia pending -> report
  and receive reward -> completed. Do not leave a contradictory completed entry
  beside an unresolved reward objective. Exact dialogue/journal text remains open.
  For an existing unpaid city save whose death journal already fired, restore the
  report reminder once without replaying the kill event or awarding XP early.

### Bedroom resting: prefer the existing normal rest if it works

- Read-only inspection of `override/BD0103.ARE` in both the configured reference
  live copy and dev EET copy found area flags `0x10` (no rest-forbidden bit), type
  `0x180` (indoor rest enabled), and an empty random-rest creature table. Thus
  the room is already configured for ordinary resting without random ambushes.
  This is file evidence, not a test of the Rest button in the current save;
  active effects, enemies, UI rules or other mods can still affect a rest attempt.
- Use the existing normal Rest button as the simple default, based on the area
  and script evidence. The user can confirm it prepares changed spells during
  the next overall install; a separate dev playtest is not required before
  implementation. A servant/bed interaction is an optional convenience, not a
  demonstrated engine workaround. The current servant leaves after waking the
  player for the council, so a repeatable servant option would need a small
  lifecycle change.
- Never reuse/reset the first "retire for the night" story path for repeat
  rests. That path advances the plot to the council and retains the original
  fourteen-day time skip. The later "ready to march" choice separately arms
  the bedroom's departure-night scene. Normal preparation rests must not set
  either story commitment or replay those scenes.
- Prefer a normal party rest, retaining ordinary elapsed time and rest-related
  mod behavior, over a custom instant spell refresh. IESDP distinguishes
  `Rest()` (individual restoration with no time advance) from `RestParty()` /
  `RestPartyEx()` (party rest, uninterruptible even near enemies). A scripted
  servant rest therefore needs safe-party/no-combat conditions if used; do not
  inadvertently enable resting through a fight or bypass normal mod recharge.
- Ordinary rest still passes time: buffs and timed quests behave accordingly.
  It must not implicitly mean "attend the council" or "depart with the army."
  The user can check prepared spell changes and ordinary recovery on the next
  install. Preserve the story-state separation in code review; do not claim
  runtime compatibility from source inspection alone.

Sources: `dlg/csrserv.d`, `lib/comp150.tpa`, `baf/csrceleb.baf`,
`baf/csrliiax.baf`, `dlg/csr175.d`, `dlg/csrcele.d`, `dlg/csr195.d`,
`baf/csr190wake.baf`, and the two read-only area files above. Engine reference:
[IESDP area flags](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/are_v1.htm)
and [rest actions](https://gibberlings3.github.io/iesdp/scripting/actions/bgeeactions.htm).

## APPROVED: roster and broad placement groups

The user approved these groups in the follow-up. Exact tiles and dialogue are
still open. No companion is excluded on lore grounds at this stage.
The 17 BG1 companions without vanilla SoD recruitment are all accounted for.
Existing SoD recruits keep their ordinary availability unless separately agreed.

| Round / timing | Companions | Approved direction; precise staging open |
| --- | --- | --- |
| Round 1: immediate palace | Skie | Same hall/location, available before rest. |
| Round 1: near palace / first city outing | Yeslick, Branwen, Ajantis | Simple city recruits; divine support and frontline options. Exact sites open. |
| Round 1: Elfsong | Coran, Garrick | Existing tavern locations; short talk-to-join independent of Safana's scene. |
| Round 1: elsewhere in city | Kagain, Alora, Xan | Simple standing recruits. Inn/shop/palace-visit hooks are possible, not final dialogue. |
| Round 1: city or first road/camp areas | Kivan, Shar-Teel | Early recruitment with a brief reason to join; no prerequisite quest. |
| Round 1: city | Tiax | Include him; keep his jail release/recruitment as small as possible. Exact handling open. |
| Round 2: city or first road/camp areas | Faldorn, Quayle, Eldoth, Xzar, Montaron | Check continuity and motivation before additions. Deferred, not excluded. |

**Round 1 covers 12 companions:** earlier Skie plus 11 new recruitment options.
**Round 2 covers the remaining five.** Together with Imoen and the 11 BG1/EE
companions already recruitable in vanilla SoD, all 29 base/EE BG1 companions
are accounted for. Their inclusion still respects the survival policy above.

Later BG2 appearances alone do not establish that an NPC cannot travel in SoD.
Mod-added BG1 companions beyond the base/EE roster require separate scope and
ownership checks; this note does not take over their recruitment systems.

## OPEN: minimum implementation design

- Reuse a living saved NPC when possible, including their build, equipment and
  spellbook. Create a modestly equipped fallback only where no usable saved actor
  exists and no known death forbids it. Do not create extra copies of imported gear.
- Respect deaths for this new availability feature. Distinguish never-met,
  dismissed, dead and currently-in-party cases, including installed identity
  aliases. Do not silently extend the current Imoen exception (her original
  design deferred death detection) to every companion.
- Resolve the actual imported actor and suppress alternate cameos/recruitment
  spawns. Never move or neutralize a current party member just to stage a scene.
- For Skie, handle all five later council spawns and the council cutscene's
  direct movement/facing actions. Simply loosening her dialogue trigger would
  leave later duplication and party-control hazards.
- Keep Skie's grief about Entar and the existing condolence acknowledgement.
  Before the council, she can ask to accompany the player without assuming an
  agreed march against Caelar. Afterwards, the existing crusade-specific ask can
  remain. Trigger on the actual story milestone, not merely elapsed clock time.
  Exact lines need review; this note does not approve replacement wording.
- Coran's recruitment must be independent of Safana's presence and scene state.
  Review both Coran's and Garrick's cameo scripts/dialogue before making them
  controllable; an existing background creature is not necessarily a ready
  player-companion build.
- Recommended XP default: follow the existing SoD recruitment/catch-up rules
  already used for Imoen and palace Skie, preserving higher imported XP. No new
  custom XP scale is needed; resolve the exact hookup during implementation.
- Implement the approved camp follow-up for dismissed, previously recruited
  companions, reusing existing camp behavior where practical. The earlier
  wait-where-dismissed proposal is superseded. Check obsolete BG1 quest timers,
  partnership rules and BG2-mod hooks while implementing; do not introduce
  elaborate new companion stories.
- Use existing walkable placements or verify the searchmap, per the locked
  placement principle. Do not place a roster on arbitrary decorative tiles.

**Readiness:** no further player-facing design decision is required before
implementation. Exact placements, brief lines and technical integration can be
resolved under the approved scope. Use the existing SoD XP convention above as
the implementation recommendation. Begin with Liia's reward/journal correction,
then earlier Skie and round-1 recruitment; retain the simple native-rest default.
Round 2 remains deferred.

## Proportionate verification and later user check

- **During implementation:** compile/parse changed installer/dialogue/scripts and
  review the changed code. Focus on Liia's shared once-only reward guard, council
  safety, companion identity/death/gear preservation and duplicate suppression.
  Use existing relevant checks where useful; no new broad harness or repeated
  multi-stage review process. Investigate failures in checks that are run.
- **User's next overall install:** spot-check early Skie and the new recruitment
  locations, short join/rejoin conversations, normal bedroom rest after changing
  spells, dismissed recruits appearing at the next camp, and reporting a delayed
  Korlasz victory to Liia for the correct reward.
- Runtime edge cases, other party compositions and standalone coverage are not
  prerequisites for beginning or completing this implementation. State coverage
  honestly and fix actual problems when found; do not call untested paths passed.

This note records a design discussion, not live acceptance or a release promise.

## Existing mod references, not new dependencies

[Continuous NPCs](https://www.morpheus-mart.com/continuous-npcs) is an existing
lightweight precedent. Its author requires EET and prior BG1 recruitment, so its
documented scope does not solve fresh SoD starts. The [author discussion](https://forums.beamdog.com/discussion/89792/mod-continuous-npcs)
also distinguishes it from existing BG2 NPC mods; do not assume integration.
[Continuous End](https://github.com/11jo/Continuous_End) documents bridges for
Xan, Yeslick and Ajantis BG2 among others. These are research references, not a
recommendation to install another mod or a compatibility result for this stack.
Check existing continuity ownership before adding overlapping behavior.
