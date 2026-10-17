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
  launches. Later up/down traversal uses `BDCUT55A/B`; the user's clarification
  below removes a return-trip feature from the interim design scope.
  No current remix implementation for this lift skip was found; the evidence
  is the repository's historical decompiled scripts, not the user's current run.

### Discussion update, 2026-09-28

**User direction:** present the bypass as a portal instead of an elevator. Keep
this a small interim overhaul of the existing Belhifet finale; the complete new
final battle belongs to the later rewrite. Make the encounter more challenging
overall while reducing abrupt party collapse and barriers to participation.
The user identifies the opening dispel, weapon-enchantment gate, large devil
groups, and rapid boss death against strong physical parties as the main issues.

**Ideas to discuss, not approved specifications:** remove the opening mass
dispel and provide more conventional protection removal during combat; lower
the weapon requirement to +1 or +2; use more HP or damage resistance for staying
power; give Hephernaan credible preparation and SCS-style cleric/mage casting;
consider ordinary Haste for Belhifet; replace hordes with a few replenishing
devils. Exact numbers, spell choices, difficulty tiers, and behavior remain OPEN.
Favor existing mechanics and bounded testing over a new encounter system.

**Read-only source refresh, 2026-09-28:** current live `BDELEV01`, `BDCUT55`,
`BD4601`, `BDCUT56`, `BDELEV02`, and `BD4700` still have the bypass seams described
above, including the return journey and the duplicate-confrontation risk.
`BDHEPHER.CRE` is already a level 14/14 cleric/mage; his finale transformation
must be accounted for when improving his combat role. Belhifet's current script
casts `WIZARD_TRUE_DISPEL_MAGIC` (`SPWI326`) once on Insane; his base level is 25.
The installed spell uses a normal caster-level dispel check, not unconditional
removal. SR Dispelling Screen supplies immunity to that dispel effect and is
intended to absorb one Dispel or Breach. The reported loss of both Screen and
buffs from one apparent cast remains unexplained without runtime evidence;
substituting another ordinary Dispel is not a demonstrated fix. His on-hit
`BDBELDIS` is disease, not another dispel.

Belhifet has 350 base HP, 3 base APR, 25% melee physical resistance and 50%
missile resistance. On engine NORMAL and above, equipment raises his base 80%
MR to 100% and imposes the +3 weapon gate; a separate armor effect imposes +2,
so lowering only one gate is insufficient. The area adds 2/4/6 devils on
NORMAL/HARD/HARDEST; later gates add one or two creatures using a broad
lawful-demonic hostile census rather than a precise reinforcement cap. Existing
offensive scripts already include fear, Symbol: Pain, Blazing Inferno, Fireball
and teleportation, competing with invisibility and summoning priorities.
Hephernaan's `BDFINHEP` transformation refers to a 90-HP, level-9 devil chassis
with `BDABISHA` combat AI. His original caster role needs explicit preservation
or replacement through that transformation. Full SCS cleric/mage generation
includes matching spellbooks and prebuff resources, not just one script swap.
These are static installed-resource findings, not runtime acceptance. No game
or save changes or live tests were performed for this discussion.

### User annotations and narrower scope, 2026-09-28

**DECIDED by the user:**

- The replacement portal leads one way into the finale. Do not spend effort on
  an elevator/portal return journey; preserve the existing victory/ending flow.
- Lower Belhifet's weapon requirement to **+1** and magic resistance to **60%**.
- Remove the opening mass dispel. Use normal targeted Breach during combat,
  eligible every **three rounds on Insane**, with brief initial pursuit of the
  selected character rather than excessive chasing.
- Use **four devils on Insane**, reducing the earlier six; tone down subsequent
  reinforcement pressure. Exact replacement cadence and whether four also
  acts as the living-add cap still need agreement.
- Keep Hephernaan's devil appearance and a competent cleric/mage combat role,
  with credible prebuffs and SCS/SR-compatible reuse where practical. He should
  be strong but below a standalone boss mage, not a second full boss.
- Keep investment small: remove frustrating mechanics and improve the average
  fight modestly. The later replacement finale still centers on **Caelar**.

**OPEN / revised assistant recommendations, not approvals:**

- Reduce the earlier HP proposal to **450 Core / 500 Insane**; other difficulty
  values remain to be settled. Keep 25% melee and 50% missile resistance.
- Prefer **+25% movement speed only**, preserving attack rate, over Haste.
  This follows the user's tentative suggestion, not a locked stat choice.
- Skip a separate Extra Challenge variant for this temporary encounter. The
  user considered the collection checkbox then questioned its value here.
  The existing bridge model was checked: optional component257 adds only the
  two Insane mage sequencers; regular Insane keeps the other improvements.
- First Breach around round three; four-round repeat eligibility below Insane,
  three on Insane. Prefer its target for at most one round, dropping the pursuit
  early if the target becomes inaccessible, then resume ordinary target choice.
- Proposed Insane reinforcement rule: four active supporting devils at most,
  replacing one casualty no faster than every four rounds. The living cap is
  an assistant proposal to prevent the opening reduction growing back into a
  horde, not an additional user decision.
- The prior suggestion to limit Belhifet to one defensive invisibility use
  remains a proposal; no exact offensive rotation or final spellbook is locked.

**Additional read-only checks:** the installed CRE still has 350 current/max
HP; no Insane-specific maximum-HP increase was found in the inspected creature,
equipment, nested proficiency payloads, combat or staging scripts. This is
source evidence, not a reading of the actor in the user's current playthrough.
The engine supports a percentage movement modifier without an APR increase.
An installed SCS 15/14 cleric/mage (`SHUPOL01`) is a plausible nearby-level
combat-script donor. Resolve its generated script from the installed creature,
then select a finite supported spellbook for Hephernaan; do not hardcode a
generated script name or assume arbitrary new spells gain AI support. The
transformation, prebuff delivery and chosen repertoire require a focused check.
This update records the discussion; no implementation or game changes were made.

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
