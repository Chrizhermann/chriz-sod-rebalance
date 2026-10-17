# Ashatiel: one lane of the tent court

Focused static follow-up, 2026-09-26. The latest user direction is **one side
of the tent court**, not the whole previous A rectangle: a compact but usable
arena, both formations initially out of sight, enemies already present,
hostile and prebuffed. Approaching them starts combat early; otherwise they
advance after a few rounds (roughly 30 seconds remains the working baseline).
Only the player's party needs the reset. Any traps inside the chosen arena
must be removed, and every escape must be sealed visibly.

This note compares the two lanes. It does not select a lane, exact start
points, barricade endpoints, encounter size, or a guaranteed sight distance.

## Spatial comparison

The earlier A study rectangle was approximate. In particular, the right-hand
lane bends slightly beyond its x2200 edge; that box is not a proposed border.
The lane envelopes below also include impassable scenery around the actual path.

| | Left / western lane | Right / eastern lane |
|---|---|---|
| Rough envelope | x860–1450, y1500–2250 | x1650–2350, y1550–2250 |
| Useful north–south scale to investigate | About 650–750 world pixels | About 600–700 world pixels, bending southeast |
| Shape | Narrower winding strip between west-side tents/wall and the central tent island | Broader diagonal strip between the central tent island and eastern tents/palisade |
| Traps in current area | Hold Person, Flame Strike and several spear triggers | None of those ARE trap regions overlap the lane envelope |
| Principal concern | Tight spots and active traps; possible single-file combat | More existing training/guard actors and southeast traffic; enough width must still be retained when sealed |

The **right lane is the cleaner first static candidate** because it offers
more local passing space and avoids the known trap strip. The left lane is
still viable research territory if a tighter fight is preferred; its trap
removal is straightforward in scope, but available combat width needs checking.
This is a research assessment, not a user-approved site choice.

Approximate lane-centre traces for a study drawing, **not spawn points**:

- Left: `[1110,1550] → [1040,1750] → [1075,1950] → [1120,2110] → [1260,2240]`.
- Right: `[1780,1610] → [1900,1740] → [2040,1900] → [2190,2030] → [2070,2180]`.

## Width and connections actually observed

Sample horizontal runs of passable base-search cells illustrate the difference:

| World y | Left lane run | Right lane run |
|---:|---|---|
| 1668 | x944–1216, 272 pixels | x1552–2096, 544 pixels; includes northern widening |
| 1740 | x928–1136, 208 pixels | x1664–2160, 496 pixels |
| 1884 | x912–1248, 336 pixels | x1824–2320, 496 pixels |
| 2028 | x1040–1200, 160 pixels | x2064–2352, 288 pixels |
| 2172 | x1008–1360, 352 pixels | x1824–2256, 432 pixels |

These are selected horizontal cross-sections, **not the minimum navigable
width**, and they do not subtract creatures' collision footprints. In
particular, the left lane's 160-pixel section around y2028 deserves a movement
check. A six-person formation and an enemy front line may make a reasonable
walkway feel much narrower in actual combat.

A four-neighbour flood search between sample points in the two lanes finds:

- an upper cross-connection around the tent island, crossing x1504 at y1584;
- a lower cross-connection crossing x1504 at y2220;
- no such cross-lane path when restricted to the middle strip y1660–2150
  and x860–2370.

This supports using the **northern and southern junctions** as the first
barricade locations to study. Their exact geometry must connect into existing
impassable scenery and close every branch; simply drawing two short bars on
the centreline would not prove containment. No middle cross-lane shortcut was
found in that static strip, but corner gaps, larger/smaller creature footprints,
door masks and engine routing remain untested.

## Traps: exact regions to account for

These are trap-region bounding boxes, not the separate launch points. The
assault entry script activates them; their stored ARE deactivated flags are
not proof that they remain inactive when the player reaches Ashatiel.

| Region | Bounds [x1,y1]–[x2,y2] |
|---|---|
| Hold_persontrap1 | [923,1773]–[1159,1830] |
| Flamestriketrap1 | [962,1967]–[1213,2008] |
| Speartrap10 | [1128,2026]–[1160,2050] |
| Speartrap6 | [1121,2119]–[1153,2143] |
| Speartrap8 | [1031,2151]–[1063,2175] |
| Speartrap5 | [1215,2167]–[1247,2191] |
| Speartrap4 | [1094,2228]–[1126,2252] |
| Speartrap7 | [1287,2245]–[1319,2269] |
| Speartrap3 | [1203,2282]–[1235,2306] |
| Speartrap9 | [1010,2309]–[1042,2333] |
| Speartrap2 | [1117,2336]–[1149,2360] |
| Speartrap1 | [1252,2361]–[1284,2385] |

The first six are within the rough left-lane envelope; spear4/7 cross its
southern edge, and the remaining four are immediately beyond it. Final bounds
determine the precise removal set. A southern staging pocket must not quietly
include a trap just outside the drawn box. The right lane avoids all twelve
of these regions; that is not a claim about every possible script/spell hazard.

## Door07 and actors

Door07's 130 closed impeded cells form an outline around the central duel
pocket, spanning x1248–1808/y1656–2040. The actual cells, not that whole bounding
box, block movement. Its western boundary lies near x1248–1376 through much
of the middle, while its eastern boundary runs diagonally from roughly
x1456/y1680 to x1808/y1932. Both outer lanes are mostly outside that outline.
The mask can still affect the inner edge and any chosen staging pocket.
Preserve it for the existing duel; do not reuse an invisible wall as the new
lane's visible barricade. See [the full geometry audit](24d-ashatiel-arena-candidates.md)
for binary offsets and the distinction from the physical inner Door01.

Earlier-visit ARE placements in the left envelope include Leosis, Tristian,
sergeants/elites and mercenaries. The right envelope contains Famari and his
mercenaries, ordinary guards, the map-table guard, four training archers and
four target objects. The assault changes which actors survive or are created:
the right lane's southeast end approaches scripted assault formations, so
actual phase-specific actors need deliberate parking before a challenge.
Do not clear all actors in a rectangle indiscriminately. The northern champions
remain entirely separate and are not candidates for relocation here.

## What static work cannot settle

The lane bend and tent islands may provide initial separation, but the image
and search grid cannot prove that two hostile formations will start outside
each other's engine sight and detection range. Nor does an opaque-looking tent
prove that a thief can hide behind it. Reserve a focused native test for the
two actual starting formations, thief LOS break, full-party passage at the
pinch points, and all barricade corners.

Enemies being hostile from the outset also means their AI must use the agreed
start condition: engage when the player approaches or begin advancing at the
timer, without charging from staging merely because generic AI can detect a
party member through some broader search. That is an implementation constraint
for later, not approval for an invisible immunity or player-control lock.

No installation, area, script, save or live game was modified. This follow-up
used the same captured ARE/search map as the September 26 geometry check,
with in-memory grid probes only; no native pathfinding or LOS claim is made.
