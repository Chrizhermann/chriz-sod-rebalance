# Playthrough follow-ups after Ashatiel

Captured from the user on 2026-09-26. **Side notes for later**, not work to
implement during the Ashatiel encounter design. The user is enjoying the current
remix and wants targeted improvements. Ashatiel remains the immediate priority.

## Prologue XP presentation

- The replacement XP from the skipped first dungeon should not arrive as many
  separate awards/messages. Consolidate that presentation/delivery.
- Investigate the actual award sources before changing anything; the request is
  not to increase or reduce the agreed total (currently 22,000 per character).
- Check repeat/reload guards and companion eligibility when consolidating.
- **Source lead checked 2026-09-26:** `chriz-sod-remix/dlg/csr175.d` has one
  Liia reward with six `AddXPObject(Player1..6,22000)` actions. This is a likely
  source of repeated display lines, not six different compensation schemes.
  Component 140 does not separately award dungeon-skip compensation. Confirm
  the observed presentation before changing it; a single
  `AddExperienceParty(22000)` would divide the reward and change its value.

## Rewards moved out of a removed area

- Revisit the placement of the rewards moved into a chest after an area was
  removed. Find a fitting place for them.
- The user did not recall the area's or chest's name. Identify the existing
  relocation before treating any candidate as confirmed. Exact placement is OPEN.
- **Strong source-supported candidate, not yet user-confirmed:** Coast Way Forest
  (`BD7000`, component 210), whose notable loot component 900 moves to the camp
  chest `Container009` in Coast Way Crossing (`BD1000`, 509,3220), beside the
  Flaming Fist tents. Payload includes Gemblade, The Suncatcher, Boot and a Half
  of Speed, Wand of Paralyzation, Ring of Free Action and treasure. See
  `chriz-sod-remix/lib/comp900.tpa`.

## Relocated loot identification

- Backfilled/relocated loot is arriving already identified in multiple places,
  including the group the user referred to as “Corler's” (possibly Korlasz;
  identification of the exact source remains to be checked).
- Preserve the intended unidentified state for items that need identification;
  do not automatically identify rewards because the remix moves or grants them.
- Audit the affected grants and containers, keeping naturally identified mundane
  items and any intentionally identified originals distinct.
- **Confirmed code leads:** component 900 sets the identified flag on all eight
  relocated chest records. Component 170 explicitly uses `IDENTIFIED` on
  Korlasz's relocated gear and on equipment/consumables for Haskell, Vhasq and
  Sill. This supports Korlasz's group as the likely example. The later audit
  should cover other delivery paths too, not only these two components.

## Avernus lift and final battle, interim improvement

- Clicking the lift downstairs should jump directly to the upper arrival /
  confrontation cutscene for Belhifet, skipping the lift ride and its battles.
- No compensation is requested for the skipped lift-combat XP; the user accepts
  losing that XP. Preserve the final encounter's required setup and story state.
- This is an interim improvement before a fuller rewrite. The very last fight
  should become more engaging, but its exact changes still need discussion.
- Do not interpret this note as removal of the Belhifet fight or approval of a
  particular new final-boss design. Further ideas will follow.
- **Historical source pointers, refresh before implementation:** downstairs
  `BDELEV01` gathers the party and starts `BDCUT55`; `BD4601` owns the ride and
  three waves. Its completion sets `bd_plot=560` and `bd_hellevator=5`, then
  `BDCUT56` moves the party to `BD4700` and starts `BDCUT57`. That normal completion
  is the seam to investigate, rather than an isolated teleport. `BD4700` also
  starts the confrontation when `bd_plot<560`, so careless bypassing risks two
  launches. Later up/down traversal uses `BDCUT55A/B` and needs to keep working.
  No current remix implementation for this lift skip was found; the evidence
  is the repository's historical decompiled scripts, not the user's current run.

## Other retained content

- Keep the northern Dragonspear named party in place and separate from Ashatiel.
  A later light review is possible, but no current rework/removal is requested.
- The existing deferred broader Shadow Aspect redesign remains separate.

## Priority

Finish Ashatiel research and agree its design first, then develop and test a
community-playtest draft. Return to these minor fixes afterward. The user accepts
some necessary actor movement and a small number of additional focused arena
tests to produce a good encounter; this is not authorization for live game
actions now.
