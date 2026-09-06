# Filler coverage audit: coalition, river, and late maps

**Date:** 2026-09-07. **Issue:** [#16](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/16).
**Status:** static audit and triage evidence; no new removal decisions or game edits.

The current install contains every exact placed-actor cut listed by components
260 and 270. It does **not** establish complete filler coverage. The clearest
unfinished work is a reachable Unsleeping Guardian omitted from the cut list,
Mizhena's quest item still assigned to removed displacer beasts, and wilderness
spawn points that area scripts can enable after the initial clearance. The
larger Bloodbark, druid, drow, and Kanaglym choices remain OPEN.

## Evidence and counting boundaries

The source is the effective dev EET install at
`C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install`, ending at
component 291 in the recorded WeiDU log. See the reproducible
[snapshot](issue16/snapshot.json), [resource hashes](issue16/resources.csv),
[actors](issue16/actors.csv), [creatures](issue16/creatures.csv),
[carried items](issue16/cre_items.csv), [spawn points](issue16/spawn_points.csv),
[rest headers](issue16/rest.csv), [travel regions](issue16/regions.csv), and
[cut-list checks](issue16/cutlist_checks.csv).

Fresh script decompiles are local generated evidence under
`research/data/issue16-audit/census-v3/baf/`; additional current dialogue
decompiles are under `research/data/issue16-audit/coalition/` and
`research/data/issue16-audit/coalition-loot-final/`. The latter directory was
generated with `research/scripts/audit_filler_loot.py --areas BD0113 BD7310 BD7400
BD7410 BD5110 BD5000 BD5100 BD5300`. Its tracked
[inventory rows](issue16/coalition-loot/travel-and-mimic-items.csv) and
[dependency hashes](issue16/coalition-loot/travel-loot-screen.json) cover placed
CRE inventories and ARE containers, not all spell summons, store stock, or
dialogue rewards. The inherited output filenames say “travel”; this nested run
covers the eight coalition/river pockets named in its manifest.

The final loot run preserved the original seven-map 919 rows and added 24
BD7410 rows; all read source hashes, WeiDU log, and key stayed unchanged.
Eight assigned dependency references are absent from this effective install:
`BDCONCOC.BCS`, `BDENEMY1.BCS`, `BDJULANN.BCS`, `BDDM04.DLG`, `BDDM05.DLG`,
`BDDM06.DLG`, `BDDROWFM.DLG`, and `BDRCRUS.DLG`. The manifest records them;
no behavior is inferred from their names, and no repair is proposed here.

`research/data/sod_baf/` and research 02c are historical **pre-cut** evidence.
They cannot establish what survives now. Approved scope comes from
[the wishlist](../01-remix-wishlist.md) and
[the user-era chapter design](../design/chapters/04-coalition.md), not the old
agent-authored design proposals.

“Scheduled hostile” below means an ARE actor with a nonzero low-24-hour schedule,
an effective CRE with EA 255, and no CRE dead-state bit. This is a static inventory,
**not a guaranteed simultaneous fight count**. Actor-specific `BDLCORE`,
`BDLHARD`, and `BDLINSA` scripts destroy actors below NORMAL, HARD, and HARDEST
respectively; other scripts can change allegiance or remove an actor. Neutral
quest enemies are absent from that column. Kill XP is the sum of those templates,
before difficulty filtering, peaceful resolutions, and script-created actors.

## Installed cuts and current map classification

| Area | Exact listed cuts verified schedule-zero | Scheduled hostiles / raw kill XP | Classification |
|---|---:|---:|---|
| BD7300, Dead Man's Pass | 119/119 | 20 / 55,050 | Keep the parley route and approved distinctive encounters; wandering repopulation remains a candidate. |
| BD7310, shadow vault | 1/1 | 9 / 12,100 | Guardian cut applied. Remaining vault fight explicitly kept by the July design. |
| BD7400, Bloodbark Grove | 21/21 | 16 / 32,100 | Whole-map existence is OPEN; current quest and companion dependencies rule out a blind map cut. |
| BD7410, Bloodbark vampire annex | Not in either list | 14 / 18,005 | Optional vampire/wolf combat-and-loot pocket; further escort thinning or annex removal OPEN. |
| BD5000, river exterior | 32/32 | 7 / 12,500 | Main infiltration route and quest hub; displacer item regression needs repair. |
| BD5100, river caves | 10/10 | 25 / 46,440 | Duplicate grove cuts applied; druid reinforcement, myconid summons, and staged quest groups survive. |
| BD5110, ghost/shadow cave | Not in either list | 17 / 22,200 | Reachable, previously unreviewed pocket: one banned Guardian; further shadow thinning OPEN. |
| BD0113, wyrmling chamber | Not in either list | 4 / 5,600 | Reachable river side quest, not skipped prologue content. Further treatment OPEN. |
| BD5300, Kanaglym | 11/11 | 9 / 7,650 | Eight graveyard skeletons plus an excluded foreign 0-XP creature; neutral quest cluster is additional. |

The foreign `C0MNEV01` in BD5300 is not a removal candidate. Its presence explains
why an EA-only census gives nine while the approved retained graveyard has eight.
No assertion about that creature's narrative purpose is needed to leave it alone.

All 183 component-260 keys and all 11 component-270 keys match exactly once and
have schedule zero. Thus there is **no failed application among the 194 listed
cuts**. Coverage omissions and consequences of a successful cut are separate
findings. Schedule-zero is not a death event, which matters below. Existing saves
with baked actors also require a separate runtime/save review.

## Concrete follow-ups within the existing direction

### C1 — BD5110 still contains an Unsleeping Guardian

The wishlist's global not-fun creature list includes the Unsleeping Guardian.
Component 260 removes the BD7310 copy but has no BD5110 key. Current BD5110 actor
**12**, `UNSLEEPING_GUARDIAN`, uses `BDUNSLGU.CRE` at **[681,924]**, schedule
`0x00FFFFFF`, EA 255, and 4,000 kill XP. It has no dialogue and no difficulty
removal script. The effective CRE carries only `IMMUNE1`, `RING95`, and
`BDUNSLGU`; all three inventory instances are flagged undroppable.

The cave remains linked from BD5100's `TranBD5110`. Its area script gates the
Ettin container on `BD_ETTIN` and the five ghost-remains containers on `BD_GHOSTS`
or the deaths of the five named ghosts; it does not gate either on this guardian.
`BDUNSLGU.BCS` is combat logic, including its Chill Ray use, rather than a quest
completion script. This is a **missed global-ban coverage candidate**, not an
invitation to remove the whole ghost quest.

An implementation should target the exact actor, preserve the five ghosts and
their containers, and decide how to account for its 4,000 kill XP. The existing
260 ledger does not include this omitted actor. Do not silently add another
80% payment or count it in the old 129,495-XP cut total.

### C2 — The displacer cut strands Mizhena's amulet delivery

Current BD5000 actors **66–68** are `Displacer Beast 3/2/1`, at
**[4261,1133] / [4354,1063] / [4449,1082]**. Component 260 correctly zeroed their
schedules, together with the other three members of the pack. Nevertheless,
current `BD5000.BCS` lines 417–428 still select one of three responses:

```baf
SetGlobal("bd_add_mizhena_amulet","bd5000",1)
GiveItemCreate("bdmisc68","Displacer Beast 1",0,0,0)
```

The alternatives target Beast 2 or 3. All three intended recipients have been
removed. `BDMIZHEN.DLG` still checks `PartyHasItem("BDMISC68")`, takes the amulet,
and provides its gratitude outcomes. State 55 includes 500 gold and 1,000 XP to
each Player1–6; alternate responses differ, so those are not universal rewards.
No replacement item placement exists in the current remix libraries. The fresh
BCS census finds only these three SoD script grants.

This is a **static quest-item regression on the normal audited acquisition
path**, not evidence that every possible other-mod store or cheat source was
searched. Preserve the encounter cut and plan a reliable replacement acquisition
point with Mizhena's quest states intact. A fresh-area check should prove both
item acquisition and the chosen dialogue outcome.

Related stale dependencies require review in the same repair: BD5000's
`Hobgoblins01` rearm waits for all three `Dead("Displacer Beast n")` predicates;
schedule-zero does not supply those deaths. Companion barks below the block
also test the displacers' absence of death near the kill site. Do not retain a
new meaningless respawn merely to satisfy the old dead checks.

## Surviving density and map choices that remain OPEN

### C3 — Wilderness repopulation survived placed-actor thinning

These are ordinary ARE spawn points, separate from the random rest-interruption
header and from staged quest reinforcements. Their initial enabled values alone
do not establish absence of future spawns:

| Area | Current area-script activation path | Spawn tables retained |
|---|---|---|
| BD7300 | Init deactivates four points. Once no ENEMY allegiance is in the area and `BD_SPWN_CUTSCENE=0`, a ONE_DAY timer starts; expiry enables Boars, Wolves, and Spiders. Bears stays deactivated. | Boars, wolves, huge/giant spiders; max 6 at each enabled point. |
| BD5000 | Init deactivates four points; no ENEMY allegiance starts ONE_DAY; expiry enables all four. | Wolves, spiders, bears/ankheg, boars; max 6 except Bears01 max 1. The fifth hobgoblin point has the broken displacer-death dependency described above. |
| BD5100 | Init deactivates two points; no ENEMY allegiance starts ONE_DAY; expiry enables both. | Ankhegs and red myconids; max 2 each. |
| BD7400 | `Spawn 1` starts enabled in the ARE but init deactivates it. Lord Dushwick no longer being in the area starts ONE_DAY; expiry re-enables it. | Ten-entry mixed undead/wildlife table; max 6. |

Each reviewed activation block advances its guard from 2 to 3, so it is a
one-time **enabling step**. That does not turn the enabled spawn point into a
one-time encounter. Its own method, schedule, chance, and countdown fields are
recorded separately in the CSV. These are good candidates for a no-repopulation
decision because the July quickwin only selected placed actors. They are not
missed entries in that list, and this audit does not claim an observed respawn
frequency. Do not confuse the point name `Boars` with permission to remove all
neutral fauna.

Rest interruption is still configured at 1% per hour on BD7300/7400/5000/5100,
and 2% on BD5110/0113. BD7310 has a nonzero-looking 10% field but an **empty
creature table**, so it cannot spawn a rest encounter from that header. BD5300
has an empty rest table. Further zero-rest choices are separate from population
cuts. Travel-arena timing is covered by the main audit; an area's EIGHT_HOURS
assignment alone does not prove eight hours between actual arena encounters.

### C4 — Dead Man's Pass and the already-kept shadow vault

The 119 cuts remove the large repetitive blocks. Current retained hostile
templates include the nymph/hamadryad/treant/shambler pocket, hill giants and
their leader, two ettins, spider elites, and the named cave-bear encounter. The
nymph pocket and its dead-orog set dressing, both ettins, and the vault fight
were explicitly kept in July. The area also carries arrival/parley plot gates
and named neutral quests; its numerous neutral or corpse actors are not 75
remaining fights.

BD7310 retains five shadows, two greater shadows, and two wraiths before
difficulty filtering. Its current area script is empty and it has no spawn
points or configured rest encounter. Its containers hold `BDAMUL01` (Amulet of
Whispers), `SCRL6G`, `SCRL6X`, `BDSILK01` (Spider Silk), and `RNDTRE07`. Removing
the remaining vault is a new decision with item-access consequences; the
approved Guardian cut is already complete.

### C5 — Bloodbark Grove: a map question with real dependencies

Twenty-one actors were removed, but **16 scheduled hostile actors remain** before
difficulty filtering. The older design's “21 of ~30” is not a current nine-enemy
count. The remaining set comprises a greater basilisk, dark treants/shambler,
skeletons, wights, and ghasts. Four of the retained skeletal group and the wight
night pocket were expressly kept in the quickwin.

A whole-map cut would need explicit dispositions for:

- **Neera:** BD7400 marks belladonna bushes during her plot; the assigned
  `BDBELLAD` region script gives `BDBELLAD` to the triggering character. This is
  companion-quest material, not anonymous scenery.
- **An Uncommon Cold:** `BDONORO.DLG` provides the recluse/cure route. The retained
  basilisk carries `BDMISC33`, which Onoroth can exchange for `BDMISC31`. The
  blackthorn trigger `BDSDD302.BCS` has another cure path and starts an eight-wolf
  event: one vampiric wolf, three dread wolves, four wolves. BD7400 sets the
  encounter guard from 1 to 2, so this is a quest-triggered single pack, not an
  endless wave. Dialogue choices can avoid a mandatory basilisk kill.
- **Installed extra dialogue:** current Onoroth dialogue also has a
  `C02AuraTalk9`/`C02ASACK`-conditioned sunflower exchange. Removing the NPC would
  remove that installed path too; this audit makes no vanilla-origin claim for it.
- **Items and services:** Onoroth opens `BDONORO.STO`; the dead-mage container has
  `BDAMUL06` (Clasp of Helm), `WAND02`, and `SCRL7C`; the journal container has
  `BDBOOK12`; the gem cache has random treasure references. Lord Dushwick and
  Chalmers are a small dialogue encounter, not part of the main siege spine.

The decision is therefore keep with fewer fights, or remove with selected
quest/material/item relocations. Neither option is authorized by “maybe remove
Bloodbark” alone. The exact XP consequence depends on which hostile branches,
quest outcomes, store access, and material paths survive; 32,100 raw placed
kill XP is only one part of that ledger.

**BD7410 is a separate vampire annex**, reached by BD7400's region 0,
`TranBD7410`, and returning through `TranBD7400`. Its 20 scheduled actors include
one fledgling vampire, four dread wolves, five wolves, and four vampiric wolves:
14 living EA255 actors, 18,005 raw kill XP before difficulty filtering. The
remaining six actors are neutral critters or pre-dead skeletons. Its area script
is empty, with no spawn points or configured rest encounters. None of the
14 hostile CREs has dialogue; the inspected area does not itself provide the
belladonna or cure paths listed above. Its role is an optional combat-and-loot
pocket, rather than proof that every Bloodbark quest needs this interior.
Current containers hold `BDHAMM01`, `SHLD28A`, `SCRL1U`, potion/ordinary loot,
and random treasure references. Reducing the wolf escort or removing this annex
is OPEN and needs an item-access decision; it was not covered by the 21 exterior
cuts. The vampire's combat escape behavior also means its raw XP should not be
treated as proof of a completed kill reward.

### C6 — The river's druids, myconids, and drow

The ten BD5100 cuts reduced duplicate corrupted-grove pockets but deliberately
kept corrupted nymphs/hamadryads, one grove, the myconids/shriekers, and all
neutral quest actors. Retained mechanisms add volume beyond the 25 raw hostiles:

| Mechanism | Current source and branch behavior | Consequence for a cut |
|---|---|---|
| Druid retaliation, BD5000 | Jamven or Chorster hostile sets `bd_sdd307_hostile_extras` once. EASY / NORMAL / HARD / HARDEST creates 3 / 5 / 8 / 11 allies, with raw kill XP 1,950 / 4,750 / 9,400 / 25,650. | These are alternative branches, not 27 cumulative enemies. Decide whether retaliation remains with the druid story. |
| Ferrusk's grove allies, BD5100 | Hostile Ferrusk near his home sets `BD_Ferrusk_Allies=1`; area script consumes it. NORMAL: 2 treants; HARD: those plus 2 gargantuan spiders; HARDEST: those plus 2 shamblers. Raw kill XP 8,000 / 14,000 / 26,000. | A staged boss group distinct from the removed placed groves. No repeated area-script wave is established by these once-guarded blocks. |
| Ferrusk's other summons | Current dialogue can create 2 `BDANKHEG`; his combat script repeatedly attempts `UseItem("BDAMUL03",Myself)` on a timer. | Item-driven summons are additional scope; the area-script count is not a complete total. Exact summon lifetime/count/XP needs the item/spell chain before a ledger change. |
| Two BD5100 shriekers | `BDSHRIE2` starts THREE_ROUNDS on seeing the party; expiry consumes a local flag and creates 2 red myconids. | Up to 4 additional red myconids, 1,680 raw kill XP, from the two placed shriekers. Preserve or cut the caller and its additions together. |
| Crusader patrols and escape reinforcements | Patrol counters reset movement cycles. Later plot/alert and Turin blocks stage reinforcements; some difficulty blocks share a guard and the earlier branch consumes it. | A patrol-counter reset is not a spawn. Do not sum overlapping HARD/HARDEST branches or remove the main infiltration reaction as filler. |

Jamven/Chorster/Ferrusk are a cross-map quest chain, with blight-seed and cure
items, alternate allegiance outcomes, and 12,000-party-XP resolutions. Current
Jamven dialogue can award `BLUN10`; Ferrusk paths involve `BDAMUL03`, `BDPOTN06`,
and `BDMISC08`. Removing all three pockets' creatures is a smaller decision than
deleting the entire druid chain. Keeping the quest NPCs and reducing repeated
guard/summon bodies is a candidate for discussion, not an approved replacement.

The drow are likewise staged rather than ten always-hostile actors. Shapur's
party, Kaelet/Umar, and the nearby crusaders participate in the fugitive-children
quest. Its options include protection, return, disguise, confrontation, and
6,000-party-XP outcomes; current rewards include `BDHALB01` or `BRAC11` on
different paths. The teens can later reappear with Murs in BD5000. Deleting
Shapur or the teens requires dialogue, journal, death-predicate, relocation, and
reward treatment. Reducing generic escorts while retaining those roles is the
smaller OPEN density proposal. No recruitable party slot is supplied by these
drow actors, but that does not make their companion interjections disposable.

Keep Strunk/water-spirit, wounded-crusader, Murs/ogre-family, and Rigah/Julann
quest dependencies in scope before any broader river cut. Current rat creations
after looting the shield immediately receive move-and-destroy actions; those
three calls are a brief loot reaction, not a three-enemy encounter.

### C7 — BD5110's remaining shadows and the reachable wyrmling chamber

After separately removing the banned Guardian, BD5110 would retain ten shadows,
four wraiths, and two greater shadows before difficulty filters. This is a
strong further-thinning discussion candidate, but those sixteen were never in
the approved list. Preserve the five named ghosts and the remains-container
system unless the player explicitly chooses to remove their quest.

`BDWORIS.DLG` can enable the five remains containers for **The Lost** and later
resolve the journey to the Fugue Plane in BD5300 for 6,000 party XP. `BDSOTUK`
has M'Khiin-specific translation dialogue, including a 500-XP award to M'Khiin.
The separate Ettin container supplies `BDBONE02`; returning it through
`BDETTIN.DLG` permits a peaceful 3,000-party-XP resolution to the river ettin.
The remains containers also carry ordinary gear, random treasure, and
`BDDAGG04`. These are reasons to preserve the small quest pocket even if its
anonymous combat ring is reduced.

BD0113 is reached through BD5100's `TranBD0113` and returns directly there.
`BD0113.BCS` advances `BD_SDD317_WYRMS`, requires the special `BDWYRMLI` dead
plus three `BDWYRML1` deaths, and then routes through Jaheira or Corwin dialogue
or a no-companion journal fallback. Its four 1,400-XP wyrmlings therefore cannot
simply be schedule-zeroed while leaving the completion gate unchanged. The
special creature carries `BDSW1HDA` and `BDDAGG05`, and all four carry a random
treasure reference. A count cut needs that loot and quest/companion resolution
review. The historical prologue ledger rationale incorrectly includes this
still-reachable room among skipped content; this audit does not alter the
already-approved prologue award to compensate for that documentation overlap.

### C8 — Kanaglym's graveyard is thinned; its quest cluster is not

The eight retained graveyard skeletons match the July design. Kherriun, six
placed dark magicians, sacrifices, Zhadroth, the Endless Watcher, and servants
are staged actors, mostly initially neutral, and are additional to the hostile
table. `BDDMSH` changes the magicians' allegiance when the area's quest fight
starts. `BD5300.BCS` requires **all six BDDM01–06 and Kherriun dead** for the
12,000-party-XP completion award plus component 270's 5,200-party-XP ledger
payment. Its two switch responses are alternatives, not two awards.

The `Darkmagespawn` region is initially deactivated but has `BDDMSPWN` assigned.
No activation was found in the fresh BCS corpus or the inspected current actor
dialogues, so its runtime reachability is **unproven**. If activated in the
appropriate returning-quest state, that script creates
BDDM07–09 and either also `BDHALAT2` or only the three magicians, depending on
the dragon's death state. It changes the plot and deactivates itself. This is a
conditional staged extension to review, not three proven surviving enemies.
Kherriun's ghost jar and area response can also release/recreate the dragon.
No cumulative dragon count should be inferred by adding these alternatives.

A smaller dark-magician fight is a credible OPEN candidate, but a cut must
rewrite the exact death gate and preserve the chosen ghost-jar, dragon, captive,
Fugue Plane, and reward outcomes. The magicians carry wands and other equipment;
Kherriun carries the jar and `BDAMUL24`; the Endless Watcher carries `BDXBOW01`.
The map also gates the Kruntur container on M'Khiin's presence. Removing the
south quest cluster is not equivalent to removing spare graveyard skeletons.

## Locked late-story keeps

BD3000 is the **Coalition Camp**; BD4000 is **Dragonspear Castle**. The chapter
design's occasional “BD4000 camp” label should not be used to target resources.
The camp defense waves, castle assault, basement reveal, and Avernus/final
battle remain the user's locked war-setpiece keeps. Their area scripts have
large literal creation counts, but those include allies, corpses, plot carriers,
and alternative stages. The census is not a reason to convert those totals into
trash cuts. Neutral placed armies becoming enemies is expected encounter logic.

BD4400 and BD4700 also contain pre-dead actors; raw EA255 totals overstate their
living combatants. The requested Ashatiel encounter is a separate design issue
requiring back-and-forth triage, and the bridge's barrel/elemental overhaul is
[#14](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/14). Neither is
silently implemented as filler cleanup here.

## XP and acceptance boundaries for the next implementation

Component 260 replaces a recorded 129,495 cut kill XP with **103,600 party-total
XP** at the chapter-11 transition in BD4000. Component 270 replaces 6,550 with
**5,200 party-total XP** at the Kherriun/magician completion. Both are present;
their existing compensation must not be paid again. The chapter transition
payment still goes to players who skipped optional maps, as already recorded
in the OPEN ledger question.

The next concrete repair can address C1 and C2 separately from new creative
choices. For additional cuts, approve actor/quest roles first, then calculate
XP from the exact selected actors and reachable scripted alternatives, preserving
chosen quest rewards and item access. Verify fresh-area schedules, item grants,
dialogue completion, difficulty branches, and any already-visited save behavior
appropriate to the implementation. This audit proves current static resources
and their dependencies; it does not claim live completion of these side quests
or an exhaustive third-party loot audit.
