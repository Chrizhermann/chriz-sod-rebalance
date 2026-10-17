# Ashatiel encounter: current sequence and reusable hooks

> Design update 2026-09-26: preserve the original duel and refusal routes and add
> a separate agreed brawl. Keep the northern party independent; reset the player
> party, stage enemies already hostile/prepared out of sight, then engage on early
> contact or the timed advance. No literal enemy reset is required. See
> [current decisions](../design/wave1/09-ashatiel-party-brawl.md).
> The original sequence findings below remain evidence, not proposed behavior.

Read-only research for issue #15, 2026-09-22. This is an implementation map,
not an approved encounter design. The approved process and open decisions remain
in [the wishlist](../01-remix-wishlist.md#ashatiel-chosen-of-cyric-style-party-fight--15).

## Evidence boundary

Current resources were copied from
`%USERPROFILE%\CEBG-Tests\Combined-20260908\game\override` into
`%USERPROFILE%\CEBG-Tests\Ashatiel-20260922\sequence\game\override`.
Effective IDS were copied from override or read directly from KEY/BIFF;
the English TLK was copied. WeiDU 249 decompiled only the scratch copy, against
a synthetic KEY/BIFF in that scratch game. No game was started, and no installer
or decompiler was run against an existing game directory.

The scratch `capture.json`, `decompiled/`, and `dialogue-readable.txt` record
the inspected resources and their decoded text. Source assets remain outside Git.
This is script/resource evidence, not a live pathfinding or encounter test.

The historical `research/data/sod_baf/` corpus was used for discovery, then checked
against current resources. Current `BDEXDUEL`, `BDASHATI`, `BDCUT44`, `BDASC`,
`BDCRUSDS`, and `BDDSGAT2` match that corpus after stripping comments/whitespace.
`BD4000`, `BDDSC`, and `CUTSKIP` differ; claims below use the current copies.
For example, the historical `BDDSC` has an Aura poison-supply prefix absent from
this Combined copy. That historical prefix must not become a required contract.

## Entry and existing formation

The location is **BD4000, Dragonspear Castle exterior during the assault**.
Ashatiel and her six escorts are created by a script, not placed as ARE actors.

Two type-0 regions in the current ARE run `BDEXDUEL.BCS`:

| Region | ARE index | Bounding box | Script condition |
|---|---:|---|---|
| Asha1 | 21 | [1084,1945]–[1121,1973] | `Name("asha1",Myself)` and `Range([PC],22)` |
| Asha2 | 22 | [1843,1634]–[1880,1662] | `Name("asha2",Myself)` and `Range([PC],22)` |

Both require `415 < bd_plot < 435`. They use proximity, so these boxes are not
the full trigger footprint. The outer-gate sequence in `BDDSGAT1` changes plot
415 to 416, opens doors 05/06, and performs the bombardment/breach scene. That
provides the existing lower progress boundary for the Ashatiel introduction.

Whichever Ashatiel region fires first sets `bd_plot=435` and
`bd_asha_duel=2`, excluding the other region. It enables lite cutscene mode,
clears actions, moves the camera, plays seven dimension-door effects, and spawns
the same seven creatures in one of two formations. All face south.

| Creature | Resource | Asha1 spawn [x,y] | Asha2 spawn [x,y] |
|---|---|---|---|
| Ashatiel | BDASHATI | [1140,1985] | [1920,1675] |
| Sarginson | BDASHA05 | [1110,1930] | [1945,1580] |
| Small Kimble | BDASHA02 | [1175,1940] | [1880,1590] |
| Zoe Kryn | BDASHA04 | [1075,1985] | [1995,1615] |
| Balvin Steadyhand | BDASHA06 | [1200,1995] | [1925,1625] |
| Wormgums | BDASHA01 | [1100,2035] | [1865,1640] |
| Marius of Tethyr | BDASHA03 | [1165,2030] | [1975,1665] |

This is already a named seven-person group; creating an entirely new roster is
not technically required. These escorts are distinct from the separate northern
`BDCHAL01`–`BDCHAL06` group identified in the map/roster audit. Reusing either
group, combining them, or reducing their number is still a design decision.

The introduction stores Ashatiel's default location as **[825,1280]**, sets her
locals `bd_no_combat=1`, `bd_no_retreat=1`, `bd_no_search=1`, turns all Player1–6
toward her, then sets `bd_mdd1230=1`, disables lite cutscene mode, and autosaves.
Her override script sees `duel=2` plus that local, applies `BDCUTSPY` to herself,
and starts dialogue with Player1. `BDCUTSPY.SPL` in this copy contains one effect,
opcode 268; neither this spell nor the two encounter scripts contains a dispel
opcode/action. The separate earlier BD4000 chapter-entry `BDREMOVE` cast is not
part of this introduction.

## Dialogue and current fight paths

`BDASHATI.DLG` has eight states. State 0 is an earlier parley continuation to
`BDDELANC` state 47; it is not part of the castle challenge and should stay intact.

| State(s) | Role | Important actions or destinations |
|---|---|---|
| 1 | Castle entry, requires duel=2 and BD4000 | Sets duel=1; destroys `MINHP1`; continues to 2 |
| 2–4 | Introduction and response branches | One branch reaches 6 through 3; the others reach 5 through 4 |
| 5 | Offers a one-on-one duel | Accept goes to 6; refuse goes to 7 |
| 6 | Explains no allies/no hiding; final confirmation | Accept sets duel=3 and launches `BDCUT44`; refuse goes to 7 |
| 7 | Group battle / accusation after cheating | Sets `bd_duel_cheat=2`, duel=1; opens door07; `Enemy()` |

State 7 can also start directly when `bd_duel_cheat=1` in BD4000. Its text is an
accusation of cowardice and an order for all soldiers to attack, so it is not
automatically suitable as the introduction to an agreed party challenge.

On the solo path, `BDCUT44` moves only Player1 to **[1400,1805]** and Ashatiel
to **[1485,1880]**, faces them at each other, makes Ashatiel hostile, changes
combat music, and ends cutscene mode. It does not reposition Player2–6.
The existing `Duel_spot` region (ARE index 4) has box
[1391,1774]–[1412,1793].

On refusal/cheating, her override script handles duel=1 by setting it to **-1**,
allowing retreat, assigning CRUSADERS specifics, playing a teleport effect,
and jumping to **[825,1280]**, the map's Crusader Commander marker. Thus the
group-fight commander location and the solo-duel location already differ.

The solo rules are enforced outside the dialogue:

- `BDASHATI.BCS` sets the cheat flag if Player2–6 attack/hit her during duel=3.
- It also tracks losing sight of Player1 and sets the cheat flag after its
  `FOUR_MINUTES` timer expires while Player1 remains unseen.
- `BDDSC.BCS` sets cheat when a friendly party-side actor attacks a crusader
  during duel=3.
- Ashatiel has an EASIEST-only solo adjustment that removes her Wand of Frost
  and listed Mirror Image/Spell Deflection memorization entries.

Do not merely label a new party battle as duel=3: these rules would still fire.

## What the surrounding armies do

`BDDSC` is shared siege behavior rather than a private Ashatiel AI script.
While `bd_asha_duel > 1`, it changes crusaders to neutral, faces them at
Ashatiel, and blocks later behavior with `NoAction()`. `BDASC` similarly makes
coalition troops neutral and idles them while plot<440 and duel>1.

The existing global pause is therefore useful evidence for how the introduction
isolates a conversation, but retaining it unchanged would also idle an enemy
party during the actual fight. Changing shared `BDDSC` indiscriminately could
alter every surrounding siege actor. A future implementation must distinguish
the selected encounter combatants from bystanders.

The separate northern `BDCHAL01`–`BDCHAL06` party does **not** use this stack.
The roster audit confirms its override is `BDCHALL`, which initializes
`bd_no_search=1`, assigns `HOSTILES3`, and turns hostile; it has no duel-global
ceasefire or retreat block. The original army-wide pause therefore does not
automatically hold that northern party. Reusing it needs its own preparation
and engagement handling, even if the existing siege pause is retained elsewhere.

Other relevant current `BDDSC` behavior:

- At plot>439, living crusaders become neutral, set no-combat/retreat flags,
  and escape toward `crusader_camp`.
- On death in BD4000 it updates crusader counters, clears script slots, and
  calls `DestroySelf()`. Reusing this stack needs a loot/corpse review.
- Prior supply sabotage (`bd_poison_dsc_supplies=1/2`) applies `BDWEAKDS`.
  Whether selected elite combatants inherit that consequence remains open.

`BDNEDERL` also uses the duel global: its initial siege conversation requires
`bd_nederlok_plot=1`, duel<1, plot<440, BD4000, and seeing a PC. Reusing -1 as a
custom preparation/fight state without reviewing this can expose that dialogue.

## Victory and later progression

**Current victory is Ashatiel's death alone, not defeat of her group.** The
following must be considered together if the new fight requires group victory:

1. `BD4000` detects `Dead("bdashati")` while plot<440. An uncheated solo duel
   uses `bd_asha_fadeout=1` and a fade/camera transition; other deaths use value 2.
2. Once fadeout>0, the area sets `bd_plot=440`, starts the Caelar delay timer,
   activates the inner-gate trigger, removes the Commander map note, opens
   door07, changes battle sound/trigger/journal state, and stages coalition
   leaders plus the fleeing crusader.
3. Shared `BDDSC` sees plot>439 and makes surviving crusaders retreat. Simply
   adding tougher living escorts does not stop that early conclusion.
4. A second BD4000 safeguard independently unlocks and opens door07 whenever
   Ashatiel is dead and the door remains closed.
5. `BDDSGAT2` starts Caelar's address when plot<450, her delay timer has expired,
   Ashatiel is dead, and a PC is within 23 of `gate_proxy`. It sets plot=450,
   stages Caelar at [2740,1553], faces the party/allied leaders, then starts her
   dialogue. This is the subsequent story handoff to preserve.

**Geometry correction, 2026-09-26:** `Door07` is an invisible obstruction in
the western duel space, not the physical inner gate. `Door01` is the physical
gate near [2793,1775]. Thus the death path opens the duel obstruction and
enables the later inner-gate sequence; those are different operations. See
[the ARE geometry audit](24d-ashatiel-arena-candidates.md#important-correction-door07-is-not-the-inner-gate).

Keeping her original death variable provides compatibility with these consumers,
but it is not sufficient if encounter completion is changed to require more than
her death. Completion and the independent door safeguard need an explicit design.

## Cutscene skipping and buff-window constraints

Neither `BDEXDUEL` nor `BDCUT44` arms `BD_CUTSCENE_BREAKABLE`, replaces the area
override with `CUTSKIP`, or calls `SetCutSceneBreakable`. Current `CUTSKIP` has
no Ashatiel-duel mirror; its Ashatiel destruction belongs to the earlier parley
response 30. Do not modify that unrelated response as a substitute.

The requested approximately 30-second preparation window does not exist today.
Its implementation must return player control during preparation, persist a
one-shot timer/stage across saves, and exclude both original approach triggers
from spawning another set. Existing scene setup uses `ClearAllActions()`;
uncritically repeating it at preparation expiry could interrupt an in-progress
player buff. No exact warning text, countdown, spawn location, or treatment of
an unfinished cast has been selected here.

## Prepared implementation/test boundaries; decisions still open

Reusable assets/hooks are the two approach regions, the introductory lines,
the dimension-door entrance, the existing named CRE templates, the commander
and duel positions, the surrounding-army pause, and the post-victory story
handoff. Reuse is available; this note does not choose among them.

The next design discussion still needs to choose: location/roster (including
the separate northern group), whether the solo/refusal paths remain, warning
and preparation trigger, victory condition, surrounding-army participation,
sabotage consequences, spells/prebuffs/potions/sequencers/difficulty, and rewards.

Once those choices are approved, focused acceptance checks can be prepared for:

- both original approaches and exactly one encounter spawn;
- full control and persistent timing through a preparation save/reload;
- existing party buffs and casting at the preparation boundary;
- party attacks/summons not triggering obsolete duel-cheat behavior;
- Ashatiel dying first and last, plus any selected enemy escape/surrender route;
- gate opening, army retreat, and Caelar's next scene occurring at the approved
  completion point, without breaking the earlier parley;
- loot preservation and unchanged unrelated BD4000 component edits.

## Selected current-resource fingerprints

| Resource | SHA-256 |
|---|---|
| BD4000.ARE | `197a55c076def0e6056db4dcb29dae8566ba5081cc710b3d57cadb711039e2b1` |
| BD4000.BCS | `71afcbf30850cbb36cc370c2de3ecd1984c2045f884eba29908392af1f60ba29` |
| BDEXDUEL.BCS | `c087c4ad961369ebb221090106e0c036f0a8e75b90f18d861de7ced3ea47bec1` |
| BDASHATI.BCS | `22c25f50a559b8d3765727208d7c0fea9261b086e0e42654f6718d602d37e4d9` |
| BDASHATI.DLG | `e37bc15520505d857bef2c72530a12691810e569f2529335a86a11a614639091` |
| BDCUT44.BCS | `51548d74193679fb8ff2a1abf452be9550a9292613500573141e261ef3d64719` |
| BDDSC.BCS | `f540ec1186b5989eb9b5fd19af334acea8e125d6a2e0bc73b9f47b729574a963` |
| BDDSGAT2.BCS | `ded95cd09a7223ffd809d70a1dd686f595a2017e8ba6c804ee14f4020ac930a4` |
