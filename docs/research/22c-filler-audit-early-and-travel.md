# Issue 16 — early chapters, travel arenas, and recurring systems

Static audit of the effective dev EET copy, 2026-09-07. Decisions remain in the
chapter designs and wishlist. This report proposes no automatic blanket removal.
See [the campaign report](22-filler-audit.md) for snapshot provenance and coverage.

## Early chapters

| Area | Current treatment and evidence | Audit disposition |
|---|---|---|
| BD0010–BD0050 and city interiors | Social hubs, shops, recruit and departure staging; actor allegiance is not a reliable filler classifier. | Retain quest/recruit/city roles. No new city cut proposed. |
| BD0100/BD0103 | Assassination retired by components 150/187/190/195. Effective BD0100 retains the save-protection sweep; nine night-set actor schedules are handled by 187. | Already addressed. Remaining script text alone does not mean the scene is reachable. |
| BD0120/BD0130 | Component 140's effective BD0120 exit starts BDCUT00Z at plot 50. Original dungeon files and enemy schedules remain on disk. | Skipped content, not a live-route filler gap. Do not charge the XP ledger for these enemies again; component 175 already compensates the skipped dungeon. |
| BD0113/BD0114/BD0115 | Effective travel regions place BD0113 off BD5100, BD0114 off BD7200, and BD0115 off removed BD7000. The old research 02a assigned them to the prologue incorrectly. | BD0113/0114 remain reachable side areas, covered in the coalition/road fragments. BD0115 follows its removed parent, subject to the baked-worldmap limitation. |
| BD0116 | Designed Korlasz jailbreak and crew (170), with difficulty branches and rehomed dungeon items. | Intentional replacement encounter. Preserve the approved fight. |
| BD1000 | Eight west spiders removed by component 200. Spiders02 has an empty creature table; six other named ARE spawn points retain creature tables. Effective BD1000.BCS lines 887–923 still arms the points after the post-clear timer. | West cut and east keeper are intentional. The other recurring wilderness packs are OPEN for a separate cut/keep decision. |
| BD1010 | Mimic/spider cave unchanged by components 200/220. Nine living placed spiders plus a corpse template classified EA255. The mimic event has 5/6/8/9 script-created creatures on below-NORMAL/NORMAL/HARD/HARDEST branches respectively. | Unreviewed density candidate: retain the mimic and chest, consider cutting its extra ooze/spider reinforcement layers or selected placed spiders. No removal approved yet. |
| BD1100/BD1200 | Designed dig-site garrison, quest wight, Semahl's attackers, horde, honor guard and Coldhearth closure. Current BD1200.BCS still awards 22,000 + 106,700 party XP on the existing clean-kill path. | Preserve the signed-off layout. Further thinning is a new design decision, not a correction inferred from raw actor totals. |
| BD7000 | Component 210 hides the worldmap node, relocates Rasaad to BD1000, and components 215/900 account for XP and selected treasure. | Removed from new-worldmap progression. Its ARE/BCS contents are not missed cuts; already-baked worldmaps are a known separate limitation. |

### BD1010 dependency and loot check

The four `BD_Mimic_Trig=1` branches create BDMIMIC and support packs, then advance
the flag to 2. The chest remains disabled until `Dead("BDMIMIC")`, which advances
the flag to 3, enables and unlocks `Chest_mimic`. Removing the mimic alone would
break that closure. Removing support mobs can preserve the trigger, mimic death
condition, and reward chest unchanged.

Effective chest items include BDBOW04, BDAROW04×20 and BDAROW01×10, plus the other
rows in [the item screen](issue16/travel-and-mimic-items.csv). No recruit hook was
found in this area-script closure. This is a bounded script/CRE/container screen,
not a proof that every installed mod has no external reference.

XP consequence: no existing chapter ledger pays for a new BD1010 cut. Price the
selected placed actors and the selected **alternative** difficulty branch; do not
sum all four branches. Keep the chest reward separate from kill-XP compensation.

### Prologue ledger rationale needs correction

The historical calculation in `design/chapters/01-prologue.md` counts BD0113's 5,600
and BD0114's 47,515 party XP as guaranteed content removed by the dungeon skip.
The current region graph proves those areas remain reachable from the Underground
River and Forest of Wyrms. Thus **53,115 party XP in that rationale belongs to
retained side content**. The user's explicit 24,000-per-character Liia award is
still a locked decision; this audit does not silently resize it. Revisit the
justification before claiming exact XP neutrality or compensating future cuts
to those two side areas. This is a scope/accounting correction, not a failure of
`AddXPObject` delivery.

## Travel arena state: deferred work still present

The current eight parent scripts contain 18 `ForceRandomEncounterEntry` calls:

| Parent area | Direct arena destinations |
|---|---|
| BD7000 (removed worldmap node) | BD0060 |
| BD7100 | BD0060, BD0066, BD0064 |
| BD7200 | BD0064, BD0060, BD0066 |
| BD2000 | BD0064, BD0060, BD0066 |
| BD7300, BD7400 | BD0066, BD0063 each |
| BD3000, BD5000 | BD0066, BD0063 each |

All four direct destinations remain available through retained parent areas.
The user approved getting rid of huge groups, but deferred each arena's exact
removal/replacement and frequency in [wave1/04](../design/wave1/04-travel-ambush.md).
The July 10 lean toward cutting all arenas is recorded as a lean, not a final
instruction to erase every `BD_URE` scene.

**Timing correction to research 07:** parents set `BD_TIMER_URE` to EIGHT_HOURS on
both fire and skip branches, but BD0060/0063/0064/0066 initialization immediately
sets that same timer to **1** and clears BD_FRE. Therefore the code does **not**
guarantee eight hours between fired arenas. After an arena, another eligible
unused encounter can roll on returning to an eligible parent once that short
timer has expired. The per-encounter one-shot gates still limit the direct pool
to four. Frequency felt in a natural playthrough has not been tested here.

### Per-arena triage

Counts below describe current placed living combat templates where identifiable,
not the sum of every script branch. The full census retains raw allegiance and
schedule data so corpse props and neutral-to-hostile actors are visible.

| Area / path | Current content | Concrete options and consequences |
|---|---|---|
| BD0060 → BD0061 → BD0062 | Orc/troll entry: 8 hostiles; next cave: 8 living trolls (the ninth EA255 row is a dead-ogre prop); deep cave: 5 placed trolls plus 5 support creatures on NORMAL/HARD/HARDEST, with no below-NORMAL support branch. BDPOOL enables `Tranbd0062` through the infravision/race interaction. | Cut the complete optional chain at its URE1 parent hooks, or retain one compact troll encounter and shorten the annexes. Whole-chain removal must account for BD0062 `Corpse` items BDSLNG01 and AMUL12, other caches, and BD0061 BDBOOK11. Do not award removed-map XP repeatedly from each of its parent hooks. |
| BD0063, URE2 | Five placed mercenary/assassin templates; BDURE2A has an escape/outro path, so all five kill rewards are not guaranteed. | Keep as the already-small fight, simplify its gimmick, or remove URE2. Loot screen includes BDSW1H21, BDHELMJ3, BDHELM08 and SW1H43. BDURE2A's inventory is not a guaranteed drop. Aura has a conditional area comment; this is not a recruit site. |
| BD0064, URE4 | Juvenile dragon plus two giants begin neutral; `BD_MORE_GIANTS` can create a leader and two more giants. | Strongest candidate to retain as a small characterful encounter, or cut only reinforcements. The dragon dialogue and giant death conditions reveal `Hidden_cache`; preserve that path if keeping the cache. Full removal must handle BDIOUN02 in the cache and BDHALB03 on the optional leader. Dialogue has Jaheira/M'Khiin interjections and a reaction to worn dragon gear; it is not a companion recruitment gate. |
| BD0066 → BD0067, URE3 | Current BD0066 has **35 goblins + 3 ankhegs = 38**, not the historical prose's 41; the old CSV already records 38. The explosion/hole interaction BDURE3A enables `TransBD0067`. BD0067 has 13 placed enemies; its two BDSHRIE2 actors can each summon 2 BDMYCRD after THREE_ROUNDS, once per shrieker. | Highest-priority full-chain cut or radical consolidation candidate. Removing only goblins leaves ankhegs, the annex and its summons. Whole-chain removal must handle BDSW1H25 + CHAN12 on `Elite_elven_warrior`, BDURE3A on `Elven_wizard`, other container gear, and the explosion/exit linkage. |
| BD0065/0070/0071/0072 | No direct destination in the 18 current URE calls; no placed actors in the census. | No speculative cuts based on the unused direct-encounter slots. |

These are optional encounter chains; no main-plot gate was found in the reviewed
entry/exit/reward scripts. That is not a global assertion about all third-party
dialogue. [The item/dependency screen](issue16/travel-loot-screen.json) records the
effective resource hashes, reviewed CRE script/dialogue dependencies, and zero
missing references within that selected set. It deliberately includes corpse and equipment
templates: `instance_undroppable=False` alone does not prove an item can drop,
because ITM flags, randomiser tokens, scripted escapes and removals also matter.

**XP decision still OPEN:** travel arenas are optional and mutually conditioned by
one-shot gates; current components 215/230/240/260/270 do not compensate their removal.
BD0066's current placed hostile template sum is 4,775 party-total kill XP before
the annex, summons, rest spawns, or difficulty effects. Use that only as a bounded
baseline. Choose cut/retain scopes first, then recount the finite encounter paths
and pick a once-only award anchor. Do not treat repeatable rest/ambient spawns as
a finite guaranteed campaign reward.

## Ambient and rest systems

BD1000's script sets `BD_SPWN_ACTIVE` from 0 to 1 while disabling its points, then
from 1 to 2 once `!AreaCheckAllegiance(ENEMY)` passes and starts ONE_DAY, then from
2 to 3 and activates them.
This is a **one-time activation state machine**, not a proven script loop back
to 0. The engine spawn points themselves can be recurring; actual pack density
depends on their flags, schedule, caps and save state. Other outdoor maps use
the same pattern; see the road and coalition fragments and census rows.

Spiders02 in BD1000 is intentionally safe even when that script activates it:
its creature count is 0. The other six real points still have payloads. The
script additionally names `Boars`, which has no corresponding BD1000 spawn row;
counting activation calls alone would overstate the map's active systems.

The rest-header component 100 reduces frequency, not pack size. Retained payloads
and nonzero chances therefore are not failed removals. Zero-rest areas and pack
sizes remain per-area choices. In particular, removing a placed troll/spider
cluster does not remove that creature from the area's independent rest table.
The campaign census provides the effective day/night rates, table, cap and
difficulty so a future decision can address each layer explicitly.

## Verification boundary

Fresh WeiDU 24600 decompiles were written outside the game directory. The loot
screen uses the repository's existing bounds-checked CRE/item parser and resource
extractor. Reproduce the item screen from a clean scratch path:

```powershell
python research/scripts/audit_filler_loot.py --game "C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install" --scratch research/data/issue16-loot-rerun --output docs/research/issue16
python -m unittest discover -s research/scripts -p "test_audit_filler_loot.py"
```

The default screen covers the eight named travel/mimic areas, scheduled placed
CRE inventories, explicitly listed additional creature templates and all ARE
container item instances. Its 249 inventory rows are unchanged after the bounds
review; all 38 selected CRE script/dialogue dependencies resolved. The manifest
records the additional templates and exclusions. It does not automatically
discover every script-created creature or inspect every actor/area/container
script, ITM effect, merchant stock or randomiser outcome. For selected other
maps, supply `--areas BD0113 BD7310 ...` and a separate output directory; the
filenames remain `travel-and-mimic-items.csv` and `travel-loot-screen.json`.

No game installation, save, encounter or XP value was modified. No native
playthrough was run. Saved-area actors, engine respawn cadence, natural quest
closure and item delivery remain runtime checks for any resulting implementation.
