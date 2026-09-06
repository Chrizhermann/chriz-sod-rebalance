# Issue 16 — campaign filler and trash coverage audit

**Static audit completed, 2026-09-07; findings ready for triage.** No new cuts,
quest changes, XP changes, or game installations were made. The existing
generated actor-cut lists are applied correctly; the important gaps are their
quest dependencies, omitted encounter sources, and historical map classification.

## Recommended order

| Priority | Finding | Evidence and next step |
|---|---|---|
| 1 | **Mizhena's amulet still goes to removed displacer beasts.** | Effective BD5000.BCS assigns BDMISC68 to Displacer Beast 1/2/3, all disabled by component 260. Preserve the retained quest with an obtainable item source; do not remove the quest as a side effect of a trash cut. Details: [coalition audit](22b-filler-audit-coalition.md). |
| 1 | **Ymori was cut as a stray wight despite quest staging.** | BDYMORI's schedule is 0, but BD2000YM activates him and creates zombies; Junia has death/item-dependent dialogue. This is a static dependency risk, not a proven total quest hardlock: another Junia route exists, and native Activate-versus-schedule behavior needs checking. Details: [road audit](22a-filler-audit-roadnorth.md). |
| 2 | **The creature bans missed two reachable paths.** | Shadow Aspect's BDASHIRU script summons two BDSHSOUL on HARDEST; BD5110 still has a scheduled BDUNSLGU. The latter is a different cave from the correctly cut guardian in BD7310. Complete the already-decided bans without redesigning surrounding quests. |
| 2 | **Prologue XP rationale includes retained side maps.** | The old calculation includes 53,115 party XP from BD0113/BD0114, but current travel regions connect them to BD5100/BD7200. Reconcile that rationale before claiming XP neutrality or pricing further cuts there. The user's 24,000-per-character Liia reward remains unchanged. Details: [early audit](22c-filler-audit-early-and-travel.md). |
| 3 | **Recurring packs remain outside the placed-actor pass.** | Thirty-seven spawn points remain across outdoor and underground maps; one is initially enabled and most others have script activation paths. BD1000's removed Spiders02 has an empty table, correctly surviving later activation. Choose which other points to disable or retain per map. |
| 3 | **Large travel arenas and Neera's spider cave remain.** | The URE3 goblin/ankheg/myconid chain and BD0114 are substantial unreviewed density candidates, with loot and quest consequences. Exact cut versus consolidation remains OPEN. |
| 4 | **Temple and later quest pockets need deliberate design.** | Ziatar/temple, Bloodbark, corrupted groves, drow, river shadows and Kanaglym south groups have actual quest or loot hooks. Use the per-map options below; none is a safe blanket deletion based solely on body count. |

The first implementation follow-up should preserve the two quests and complete
the existing creature bans. The wider encounter designs can then proceed from
accurate data. The bridge and Ashatiel remain their own design discussions in
[#14](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/14) and
[#15](https://github.com/Chrizhermann/chriz-sod-rebalance/issues/15).

## Coverage and reconciliation

The census covers **all 76 current SoD area resources**, matching all 76 rows of the
historical area dataset. [Map triage](issue16/map-triage.csv) assigns every area
one review disposition and a report reference. This is complete area coverage
for the static audit, not a claim that every dialogue branch or runtime state
has been exercised.

[The historical comparison](issue16/historical-comparison.csv) joins all 76 rows
of `sod_encounters_full.csv` to the current screens and dispositions. Its warning
about different scopes matters: old hostile totals and current scheduled,
non-dead allegiance screens are not interchangeable.

| Layer | Current evidence | Interpretation |
|---|---|---|
| Placed actors | 4,596 rows; 4,083 have at least one scheduled hour, 513 have none. | Counts include civilians, corpse props, skipped maps, staging actors and neutral-to-hostile encounters. They are not combat totals. |
| Generated cut lists | **495/495** exact CRE@X@Y keys matched once and have schedule 0. Counts by component: 220: 169; 230: 98; 240: 34; 260: 183; 270: 11. | No failure to apply these lists. A semantically wrong cut, such as a quest-item carrier, can still pass this check. |
| Other early cuts | BD1000's eight western spiders have schedule 0; BD0100's nine night-set actors all have schedule 0. [All 17 supplemental checks pass](issue16/early-cut-checks.csv). | Components 200/187's separate cuts are present. They are not included in the 495 generated-list total. |
| ARE spawn points | 37 parsed with CRE payloads, method flags, limits, schedule and default enable state. | 36 start disabled; BD7400's `Spawn 1` starts enabled. Initial disable alone is not removal. |
| Rest headers | All 76 parsed; 35 structurally configured, including five BDNOREST cancellers. | The other 30 configured tables still have encounter payloads. Component 100 targets frequency; pack-size and zero-area decisions are separate. |
| Scripts | 1,371 fresh effective BCS decompiles, including BD scripts and assigned/directly created CRE scripts. | Creation calls are a searchable dependency screen, not a sum of simultaneous hostiles. Conditions, alternative branches, allegiance and quest roles need interpretation. |
| Region graph | Every area travel/trigger region parsed. No current inbound region targets BD7220. | Confirms component 240's cave bypass and exposes the old BD0113/0114/0115 chapter misclassification. |
| Quest/loot | Targeted fresh dialogue/script checks for candidate groups, CRE item tables, plus travel/mimic container screen. | Unique-item presence is recorded before suggesting cuts. Randomiser tokens and item drop behavior are not assumed from a CRE table alone. |

Detailed reports:

- [Road north](22a-filler-audit-roadnorth.md): outdoor reactivation, warren/troll
  keepers, Neera's cave, temple/Ziatar, Shadow Aspect, Ymori and bridge boundaries.
- [Coalition and late maps](22b-filler-audit-coalition.md): Mizhena, Dead Man's
  Pass, Bloodbark, river/drow/druid pockets, BD0113/BD5110, Kanaglym and story keeps.
- [Early chapters and travel](22c-filler-audit-early-and-travel.md): prologue,
  Coast Way/dig-site reconciliation, mimic cave, all four travel chains, loot,
  timer correction and XP implications.

## What remains intentionally present

The coalition siege, bridge story progression, Dragonspear assault, castle and
hell set-pieces were deliberately kept by the chapter decisions. Their troop
counts do not authorize a new cut. Ashatiel's proposed replacement and the bridge
barrel/elemental redesign have their own creative scope.

Rasaad's original map, the bugbear cave, the original Korlasz dungeon and retired
ending maps still exist as resources. Reachability matters: deleting their raw
actors again would add no benefit on the intended route and could double-count
XP compensation. BD6100 additionally remains EET's required import-container
resource even though component 290 no longer sends the player through the old ambush story.

Banned-creature creation calls also survive in skipped prologue resources:
BD0120/BDSARC03 and BD0130/BDSHSARS→BDSPIRIT. These are recorded separately from
the two reachable ban misses; a keyword hit is insufficient to call a live gap.

## Historical data corrections

1. **Map IDs do not imply chapter membership.** BD0113 is off BD5100; BD0114 is
   Neera's cave off BD7200; BD0115 is off removed BD7000. Research 02a and the old
   prologue XP basis conflated these with the skipped Korlasz dungeon.
2. **Travel timing is not a guaranteed eight-hour gap.** The parent scripts set
   EIGHT_HOURS, but all four destination init scripts overwrite that shared timer
   with 1. Research 07's minimum-spacing claim is incorrect for the current code.
3. **BD0066 has 35 goblins and 3 ankhegs**, 38 current living hostile actor rows,
   rather than the historical prose's 41. BD5110 has a guardian in addition to
   the 16 shadow/wraith rows; Kanaglym is BD5300. The historical CSV already
   records the correct totals of 38 for BD0066, 17 for BD5110 and 14 for BD7410;
   the incorrect labels came from prose summaries. Raw EA255 counts can also
   include dead props.
4. **Spawn offsets needed correction.** The local skill reference's old
   max/enabled offsets +0xAC/+0xB4 were not used. The census uses the primary
   [IESDP ARE V1 specification](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/are_v1.htm):
   maximum +0x84, enabled +0x86, schedule +0x88. These fields are covered by parser tests.

Historical datasets remain intact as historical evidence, with prominent pointers
to this correction. Do not regenerate an XP ledger from their old totals alone.

## Snapshot and reproducibility

Source repo: `6c308f5facb6837b78f7e161613bb972c08b201b` (v0.6.8 source).
Game: `C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install`.
The dev game-folder TP2 and its installed row labels say **v0.6.4**, including
later appended components; the report therefore verifies actual resources rather
than equating that label with a clean v0.6.8 installation. There are 446 WeiDU rows,
32 for this mod, with component 291 last. The game source was not synchronized or changed.

[Snapshot](issue16/snapshot.json) records UTC time, source/tool versions, log/key
hashes, missing references and coverage counts. [Resource hashes](issue16/resources.csv)
record the exact effective ARE/CRE/BCS inputs. The log, key and every materialized
source resource were rechecked at the end and remained identical.

The prior-agent drift note was consulted only as historical context:
`C:\Users\chris\.claude\projects\C--src-private-chriz-sod-rebalance\memory\dev-install-mod-drift.md`
(mtime 2026-07-12T23:07:48Z). Current resource hashes and current chapter decisions,
not that note's obsolete install state or reinstall procedure, govern this audit.

```powershell
python research/scripts/audit_filler.py --game "C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install" --work research/data/issue16-audit-rerun --output docs/research/issue16
python -m unittest discover -s research/scripts -p "test_audit_filler.py"
```

Use a fresh `--work` directory. Raw game resources and WeiDU diagnostics are
ignored under `research/data/issue16*/`; only metadata, hashes, tools and reports
are tracked. The separate loot screen command is in the early/travel report.

## Acceptance boundary and next triage

This audit establishes current installed data and specific dependency risks.
It does not prove natural quest completion, existing-save behavior, exact engine
respawn cadence, difficulty feel, or loot arrival. Missing assigned scripts are
listed in the snapshot rather than silently treated as reviewed code. The script
screen follows direct resource references; it is not a full symbolic execution
of all dialogues, summoned spells, dynamically named resources and third-party AI.

For each agreed follow-up, record the keeper/cut scope, quest and item handling,
and XP delta before implementation. For the quest-preservation fixes, use focused
native acceptance at the amulet and Ymori scenes; for the creature bans, verify
the Shadow Aspect's HARDEST branch and a fresh BD5110 visit. Further density work
needs player-facing keep/cut/consolidate choices from the detailed tables.
