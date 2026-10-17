# Ashatiel: alternative arena geometry

> **Subsequent user direction:** narrow candidate A to just its left OR right
> side path. The arena should be only large enough for initial out-of-sight
> separation, with traps removed and all escapes sealed. Other candidate
> comparisons below remain background research, not an open choice to use
> the whole courtyard. See [current design](../design/wave1/09-ashatiel-party-brawl.md).

Read-only research, 2026-09-26, following the user's decision to keep the northern
champions separate and preserve both the solo duel and refusal/all-out battle.
The new agreed party challenge needs visible wooden boundaries, enough space
for repositioning and hiding, and no interference from the surrounding siege.
**No site or barricade coordinates are selected by this note.**

## Evidence and limitations

Inspected the actual daytime BD4000 ground render, effective ARE records and
320-by-320 search map from the Combined test installation. World dimensions
are 5120 by 3840; search cells represent 16 by 12 world pixels. Re-read
`BD4000.ARE` on September 26: SHA-256 remains
`197a55c076def0e6056db4dcb29dae8566ba5081cc710b3d57cadb711039e2b1`, matching
the September 22 capture. Script claims below use the captured effective
`BDCUT41`, `BDCUT42`, `BD4000`, and `BDDSGAT1`, not an ARE-only census.

Evidence remains in `%USERPROFILE%/CEBG-Tests/Ashatiel-20260922/`, especially
`map/area.json`, `map/BD4000-ground.png`, `map/BD4000SR.BMP`,
`roster/decompiled/` and `sequence/decompiled/`. No original game file was
written and no game was launched.

Search-map floor classifications were checked against the primary
[IESDP search-map reference](https://gibberlings3.github.io/iesdp/appendices/search.html).
They distinguish passable terrain from walls, roofs and obstacles. The
[ARE door specification](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/are_v1.htm#arev1_0_Door)
explains how door state adds impeded search cells. This is a static geometry
check, not proof that a six-person party, summons or enemy formation fits,
that a route is wide enough, or that hiding works in the engine. Search-map
visibility and rendered scenery must not be treated as a complete live LOS test.

## Candidate comparison

Rectangles below are **inspection windows**, not exact arena perimeters or
approved teleport/spawn coordinates. Their rough sizes are comparable.

The [study-box map](%USERPROFILE%/CEBG-Tests/Ashatiel-20260922/map/BD4000-arena-options.png)
shows A (western court), B (central court), and the northern party to preserve.
Its boxes do not represent actual barricade placements.

| Candidate | Inspection window | Spatial advantage | Main cost |
|---|---|---|---|
| Western tent court around the current duel | x1000–2200, y1450–2250 | Closest to both Ashatiel introductions; tent islands offer potential cover; northern champions remain untouched | Existing invisible Door07 enclosure, narrow tent lanes, several active assault traps, and earlier-visit actors need explicit treatment |
| Central court and catapult approach | x1700–2700, y2100–2850 | More open continuous fighting floor; existing palisade edges on several sides; easier to see the combatants | Heavily occupied by the assault's named formations and troop lanes; substantial temporary relocation and reliable restoration |
| Southeastern pen / breach-side enclosure | x2850–3700, y2350–3000 | Existing walls and pen gates provide recognizable boundaries | Not empty: Gnarg's group and the ogres occupy it during the assault; narrow internal pen topology and breach progression make it a less attractive first draft |

The **western court and central court merit a visual choice together**. The
western one requires less displacement of scripted assault formations; the
central one offers a simpler-looking battle floor but much more staging work.
Neither requires removing the northern champions or merging their encounter.

The northern keep forecourt beyond the physical inner gate is a lower-priority
alternative: it overlaps the gate/Caelar progression and takes the agreed brawl
past an existing story boundary. It should not become the default merely
because its artwork looks spacious. A separate sequence audit is needed before
claiming that it can be entered and exited without firing Caelar's address.

### Static floor sample

Counting complete search cells wholly inside each inspection rectangle, before
dynamic doors and actor footprints:

| Window | Sampled cells | Passable base cells | Largest four-neighbour passable component |
|---|---:|---:|---:|
| Western | 4,884 | 3,220 | 3,220 |
| Central | 3,782 | 3,019 | 3,008 |
| Southeastern | 2,808 | 2,144 | 2,144 |

These figures show that the western window is not simply six tiny disconnected
tent pockets. They do **not** prove all connections are wide enough or survive
the assault's closed-door masks. The central court's open appearance also does
not mean it provides substantially more total floor within these bounds.

## Important correction: Door07 is not the inner gate

The previous sequence note used “inner gate” too loosely when describing
`OpenDoor("door07")`. Direct ARE geometry separates two objects:

- **Door01** is the physical inner gate near the `Dsc_gate_inner` / `Gate_proxy`
  regions. Its closed outline is `[2752,1671]–[2845,1848]`; 99 closed impeded
  cells span search x171–180/y138–153. This corresponds to the northern stone
  entrance and the existing Caelar scene trigger.
- **Door07** has no normal open/closed clickable polygon (all bounding values
  are 65535), no impeded cells while open, and **130 impeded cells when closed**.
  They span search x78–112/y138–169, equivalent to world x1248–1808/y1656–2040
  when the last cell's full extent is included. It is an invisible obstruction
  in the current western duel space, not at x2793/y1775.

`BDCUT42` closes Door01, Door03 and Door07 at lines 9, 12 and 15. Ashatiel's
refusal/cheat dialogue opens Door07, and `BD4000` opens it on her death with
an additional death safeguard. Therefore the new agreed group route cannot
assume that the western floor is all open simply because its ground art is.
It must account for Door07, then present any intended new boundary visibly.
Preserving the old solo path means not globally deleting that door or its rules.

Other relevant collision objects:

| Door | Closed impeded cell range | Spatial role / caution |
|---|---|---|
| Door02 | x202–215, y226–230 | Southeast pen, with `BDDSPENS` script; opens to a different set of 19 impeded cells rather than becoming entirely collision-free |
| Door03 | x163–168, y216–230 | Central-to-eastern pen passage; current open/closed outlines roughly x2606–2700, y2484–2779; assault scripting observes its state |
| Door04 | x191–208, y278–286 | Wall-breach barrier at the southern approach; no normal clickable outline |
| Door05 / Door06 | x52–66, y232–247 / x51–63, y237–250 | Southwestern outer-gate barriers; already opened by the assault entry/outer-gate sequence |

The listed ranges are bounding rectangles of impeded cells, not solid rectangular
walls. Openings or paths around their edges must be checked on the exact cell set.

## What actually occupies the candidates

### Western court

The ARE contains earlier-visit actors including Beno Famari and his mercenaries,
Commander Dreon, Zare, Leosis, several ordinary crusaders, training archers and
dummies, plus the map-table guard. Those placements cannot be assumed to remain
unchanged during the assault; their CRE/area scripts handle campaign phases.
Conversely, they cannot be indiscriminately removed just because the brawl needs
space. Current surviving actors must be staged on the new route only.

The current solo positions `[1400,1805]` and `[1485,1880]` are on passable base
grass cells. The broader tent court includes several roof/wall/obstacle islands
and narrow lanes. Tent art is **potential** cover, not a proven hiding spot.

Assault setup explicitly activates `Hold_persontrap1` at
`[923,1773]–[1159,1830]`, `Flamestriketrap1` at
`[962,1967]–[1213,2008]`, and the ten spear traps down the southwest lane. Several
spear traps fall inside or immediately beside this candidate (including one at
`[1128,2026]–[1160,2050]`). These would undermine a fair prepared brawl if left
live inside its bounds. Route-specific suspension/restoration, or a perimeter
that genuinely excludes them, must be decided and tested.

### Central court

`BDCUT41` creates substantial formations here, in addition to earlier ARE actors:
Ravoc `[1715,2300]`, Damarr `[1950,2595]`, Leopas `[1925,2370]`, Mald Colu
`[1885,2300]`, Valis `[2035,2350]`, Delton `[2100,2375]`, Corint `[2150,2360]`,
Sallo `[2165,2285]`, Famari `[2300,2235]`, and Commander Dreon `[2305,2135]`,
plus many ordinary soldiers and difficulty-dependent arcane/divine casters.
Presence can depend on earlier story state and survivors, so a fixed-count
“move everyone in the rectangle” assumption would be fragile.

The catapult occupies the northeast side. The gate sequence can also create
Heldmo at `[2495,2520]` and a cutscene observer at `[2535,2570]` when Door03's
branch fires. Coalition and crusader movement routes pass through this court.
This is usable only with a deliberate ceasefire and bystander staging; it is
not an unused patch of dirt.

### Southeastern enclosure

The ARE census reports zero placed actors inside the sampled rectangle, but
`BDCUT41` creates Gnarg Big-Bug at `[3095,2920]`, his orc squad across roughly
x3040–3365/y2730–2980, and Toliks `[3290,2555]`, Morruk `[3500,2645]`, and
Thrudd actors near `[3365,2630]` and `[3415,2560]`. Higher difficulties add
more squad members. This is a clear example of why an ARE-only clearance
check is insufficient. Repurposing it would require moving another existing
encounter, contrary to the goal of preserving the area's separate fights.

## Containment and movement implications

For the western court, containment must address its southwest assault lane,
northern continuation toward the champions, and eastern tent-camp route toward
the gate. Exact wooden sections depend on which tent pockets are included;
two guessed lines cannot yet be called a sealed arena. For the central court,
the broad southwest approach and northwest camp connection need closures,
while the eastern pen passage involves Door03 and the upper route leads toward
the gate. The southeastern pen similarly connects back to the central court
and onward to the southern breach.

BD4000's assault entry sets `NOTRAVEL` and `bd_cant_rest=1`. Neither is an arena
boundary: world-map travel prevention does not stop somebody walking around
the rest of this map. There is one actual travel region, `TransBD4100`, at
`[4261,346]–[4423,525]`, outside these three rectangles. Restore any flags to
their pre-brawl values rather than accidentally enabling travel/rest for the
entire siege.

Visible wooden scenery must have matching actual collision. Permanent search-map
painting would also block earlier visits and the preserved alternatives unless
made conditional through a suitable mechanism. A dynamic door/barricade design
needs authored visibility plus controlled open/closed collision; the exact
asset and implementation remain OPEN. A decorative animation alone is not
proof of containment. Avoid clearing bystanders through killing them: preserve
their death variables, rewards and the later siege progression.

## Small focused tests after a site is agreed

1. Walk all arena edges with both sides staged, then check tent/corner lanes
   with a full party and normal-sized summons; test a thief actually breaking
   enemy sight and hiding. This resolves geometry, not encounter balance.
2. Exercise each Ashatiel approach into the new challenge, plus unchanged solo
   acceptance and refusal. Confirm no traps/bystanders intrude, no unrelated
   northern fight is pulled in, and visible barriers match collision.
3. Save/reload during preparation and combat; on completion check reopening,
   bystander restoration, original door states, and the later Caelar scene.

These can be combined with the encounter's normal first-draft tests; they are
not a request for an additional full SoD playthrough.
