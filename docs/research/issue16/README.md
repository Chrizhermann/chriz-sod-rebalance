# Effective dev census for issue #16

This is a read-only installed-resource audit, captured on **2026-09-07 KST**
(2026-09-06 UTC). The source is the dev EET installation named in
[`snapshot.json`](snapshot.json), with 446 WeiDU entries ending in component
291. Its installed remix entries and game-side TP2 still identify themselves
as **v0.6.4**. These findings describe those effective resources, not an
assumed installation of the repository's newest release.

## Snapshot results

| Measure | Count |
|---|---:|
| Historical area IDs, all found in the effective install | 76 |
| Additional effective `BD*.ARE` IDs outside that dataset | 0 |
| Placed actor records | 4,596 |
| Actors with at least one of the 24 hourly schedule bits set | 4,083 |
| Actors with no hourly schedule bits set | 513 |
| ARE spawn points | 37 |
| Spawn points initially enabled with a nonempty table, positive maximum and active schedule | 1 |
| Configured rest headers | 35 |
| Of those, headers containing the `BDNOREST` pseudo-creature | 5 |
| Freshly decompiled effective scripts | 1,371 |
| Production cut-list keys checked | 495 |
| Cut-list keys matching one actor with no active schedule bits | 495 |

The five cut-list files pass individually: component 220 **169/169**, 230
**98/98**, 240 **34/34**, 260 **183/183**, and 270 **11/11**. This checks their
current `CRE@X@Y` targets and schedules. It does not establish that all intended
filler removal is implemented or that removed creatures had no quest function.

All 4,596 placed records resolve to a CRE resource; none uses an embedded CRE
in this snapshot. The parser also supports bounded embedded records. Corpse
templates retain their raw XP and allegiance, so `ea255_scheduled` is not a
combatant count. The additional `ea_ge200_scheduled_not_dead` field excludes
the CRE dead-state bit; it is still only a static screening count.

## Files and interpretation

| File | Contents |
|---|---|
| [`areas.csv`](areas.csv) | One row per area: historical label, current script, actor/schedule/dead-state totals, spawn/rest counts and ARE hash. |
| [`historical-comparison.csv`](historical-comparison.csv) | All 76 historical encounter rows joined to current counts and dispositions, with an explicit warning that their counting scopes differ. |
| [`actors.csv`](actors.csv) | Placed actor identity, index, coordinates, flags, full schedule mask and active hours, external/embedded CRE identity, XP/EA/HP/dead state, actor and CRE script slots, death variable and dialogue. |
| [`creatures.csv`](creatures.csv) | Unique CRE metadata for placed actors, spawn/rest tables, and the first pass of literal script-created creatures. |
| [`cre_items.csv`](cre_items.csv) | CRE item instances with resref, flags, undroppable bit and charges. No inferred guarantee that an item drops or is obtainable. |
| [`spawn_points.csv`](spawn_points.csv) | Every ten-slot spawn table, selected table count, maximum, enabled field, method flags, hourly schedule, probabilities and EE timing fields. |
| [`rest.csv`](rest.csv) | Effective rest table, count, maximum, enabled and day/night chance fields, with `BDNOREST` distinguished. |
| [`regions.csv`](regions.csv) | Region types, names, destination/entrance, deactivation flags, trap flags and scripts. |
| [`cutlist_checks.csv`](cutlist_checks.csv) | Exact production cut key, match count, actor index and observed schedule. |
| [`early-cut-checks.csv`](early-cut-checks.csv) | Supplemental checks for component 200's eight spiders and component 187's nine night-set actors; all 17 pass, separately from the 495 generated-list checks. |
| [`scripts.csv`](scripts.csv) | Decompiled script inventory, line counts, literal creation-call counts and normalized-text hashes. |
| [`create_calls.csv`](create_calls.csv) | Literal creation action, selected creature/group argument and decompiled line reference. |
| [`resources.csv`](resources.csv) | Effective source category, byte length and SHA-256 of every resource read by this census. |
| [`snapshot.json`](snapshot.json) | Source paths, timestamp, installed component/version metadata, tool and source hashes, missing script references and aggregate checks. |

Actor-level script fields and CRE-level fields remain separate: a blank or
`NONE` override in the ARE must not hide a script supplied by its CRE template.
The historical area names are retained only as labels. A scheduled actor may
be in an unreachable map, disabled or moved by a script, part of a cutscene,
neutral now but hostile later, or a noncombat helper.

The script corpus includes all effective `BD*.BCS`, all present scripts named
by the census's areas, actors, regions and initial CRE templates, then one
additional pass of scripts attached to CREs named by literal creation calls.
This is a reproducible inspection corpus, not an exhaustive runtime call graph.
The missing assigned script names in the snapshot are resource references, not
proof of broken quests; some are unused slots or sentinel names. They are
reported rather than silently counted as decompiled.

Creation rows include every response branch and scripts whose campaign roots
are disabled. Counts do not mean simultaneous spawns, reachable spawns or
repeatable fights. `CreateCreatureAtLocation` reads the third argument as the
CRE; its first two arguments name the saved location. Group-based creation
retains `reference_kind=group` and is not resolved as a CRE. The effective
`ACTION.IDS` has no `CreateCreatureAtLocationAllowOverlap` signature, and none
occurs in this corpus. Unknown creation signatures fail the scan rather than
silently guessing an argument. This census does not resolve SPAWNGRP tables,
summoning spells/effects, every dialogue action or arbitrary script indirection.

## Format verification and limits

The parser follows the primary [ARE V1 specification](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/are_v1.htm)
and [CRE V1 specification](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/cre_v1.htm),
cross-checked against existing research tools and the local bg-modding
`ie-areas.md` / `ie-creatures.md` references. The local area's spawn-point
note incorrectly gives `+0xAC` / `+0xB4` for maximum/enabled. The primary ARE V1
fields are **`+0x84` maximum, `+0x86` enabled, `+0x88` hourly schedule** within
each `0xC8`-byte spawn point. The synthetic regression fixture deliberately
puts different values at the obsolete offsets. The current binary census
contains nonzero data at the primary fields, with all 37 schedule masks equal
to `0x00FFFFFF`.

BD7400's `Spawn 1` is initially enabled, with ten choices, maximum six and
20% day/night probability. The other 36 points initially have enabled=0;
their area scripts can activate them. An empty table cannot become populated
merely through `SpawnPtActivate`, but enabled=0 alone does not establish a
permanent removal. `configured_and_scheduled` deliberately does not claim
runtime reachability, difficulty outcome, successful placement or frequency.

All accessed resources, `WeiDU.log` and `chitin.key` were re-read after the
census and matched the captured hashes. This is evidence of snapshot stability,
not a historical before/after proof that a particular mod preserved them.
No game files, saves or running game state were changed. Fresh-install ARE
schedules do not establish the contents of already visited saved areas.

## Reproduction

From the repository root, choose a fresh ignored work directory:

```powershell
python -m unittest discover -s research/scripts -p test_audit_filler.py -v
python research/scripts/audit_filler.py `
  --game "C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install" `
  --work research/data/issue16-audit/census-new
```

Five focused tests cover hourly masks, spawn offsets, table/count bounds,
embedded CRE bounds, kill-XP selection and creation-action argument handling.
The tool refuses a reused work directory and writes all WeiDU diagnostics,
extracted resources and BAFs beneath that ignored directory. Every WeiDU
subprocess runs there with `--game` pointing to the source. Only the metadata
tables and this explanation are intended for version control. See the
snapshot's `decompile_work_directory` for the authoritative raw corpus of
this run.
