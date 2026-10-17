# Ashatiel roster audit: Wormgums, Marius, Zoe and Balvin

Research, 2026-09-26. This describes **current resources**, not the approved new
brawl's loadout. No game or mod implementation files were changed. The northern
named party is outside this audit and remains separate.

## Evidence and reading conventions

Read-only effective installation:
`%USERPROFILE%\CEBG-Tests\Combined-20260908\game`.

The four CREs, four general BCS scripts, shared `BDDSC` / `BDCRUSDS` / `BDSHOUT`,
and `SPELL`, `DIFFLEV`, `GTIMES`, `STATS`, `STATE` IDS files all still byte-match
the 2026-09-22 capture. Script line numbers below refer to the decompiles in
`%USERPROFILE%\CEBG-Tests\Ashatiel-20260922\roster\escorts-decompiled`.
Full CRE inventories and books are in that capture's `escorts.json`. The fresh
audit, ready-spell flags, selected executable blocks, effective SPL/ITM data and
SHA-256 manifests are under
`%USERPROFILE%\CEBG-Tests\Ashatiel-20260926\martial-audit`.

Spell names and descriptions were read from the **installed SPL/ITM plus TLK**,
not inferred from familiar vanilla numbers. All memorized entries reported here
have flag 1 (ready). This is static resource/AI verification; there was no live
fight, timing or ally-delivery test. Equipment effects and engine-derived combat
statistics belong in the companion roster/build appendix.

Difficulty words in these scripts are not the usual menu labels: installed
`DIFFLEV.IDS` maps `EASIEST=1`, `EASY=2`, `NORMAL=3`, `HARD=4`, `HARDEST=5`.
For the ordinary five-step difficulty slider, `DifficultyGT(EASY)` means Core
Rules and above; `DifficultyGT(EASIEST)` includes Normal and above. Story Mode
and Legacy of Bhaal add separate engine behavior and are not additional script
tiers examined here.

Most actions share `bd_cast=ONE_ROUND` (6 seconds). Response weights are relative:
`#100` cast versus `#50 Continue()` means a two-thirds choice to take that action
**when this eligible block is reached**, not a scheduled two-thirds chance every
round. Earlier shared scripts, earlier healing/buff priorities, sight, available
spells and state tests all affect which block is reached.

## At-a-glance current preparation

| Actor | What the current AI really prepares | What it does not currently promise |
|---|---|---|
| Wormgums | Sight-triggered Barbarian Rage on Core+; Potion of Invulnerability on Normal+ | No instant prebuff chain; no Haste of his own; three rage entries are finite, and Artisan's fatigue lock needs special attention |
| Marius | Conditional Protection from Evil; Stone Giant Strength potion on Core+ | His prepared Bless and Armor of Faith are not used by his assigned AI |
| Zoe | Invisibility potion as soon as non-neutral and able to turn invisible; four uses carried | No trap placement, Poison Weapon, Hide action or sophisticated backstab target selection |
| Balvin | First-detection instant Armor of Faith, Defensive Harmony and Draw upon Divine Might on Core+; Free Action on Core+ and a 50% opening chance on Normal | No automatic refresh of those four protections; only one copy of each is prepared |

None of these four scripts contains sequencer, contingency or trigger-release
logic. They are native SoD general AI scripts, despite this installation also
containing SCS. They are not per-creature generated SCS scripts.

## Wormgums — `BDASHA01`, `BDFIGH01`

Gnoll Fighter 10, 93 HP. Halberd +2; three ready Barbarian Rages, two Extra
Healing potions and one Potion of Invulnerability. The rage ability's presence
does not establish that all Barbarian kit passives have been applied to this
creature.

### Actual opening and upkeep

1. When he sees an enemy, on Core+ and with `bd_no_innates=0`, he may use Rage if
   `OFFENSIVE_MODIFIER=0`. The response is `#100` rage / `#35 Continue()`; it sets
   the 6-second timer, explicitly removes one prepared Rage, then force-casts it.
   There is no once-only flag: another ready use can be attempted when the marker
   clears. Source: `BDFIGH01.baf:83–100`.
2. On Normal+, after sight, he may drink Invulnerability if his Armor Class or
   save-vs-spell value is above zero, `bd_no_innates=0`, and the defense timer is
   clear. Response weights are 100/50. This consumes his single potion rather
   than granting a permanent innate defense. `BDFIGH01.baf:236–257`.
3. Below 75% HP on Normal+, he may drink Extra Healing, again 100/50 with a
   6-second timer. Two uses are present. `BDFIGH01.baf:49–64`.
4. Otherwise he attacks the nearest visible enemy, selecting melee inside range
   5 and requesting a ranged weapon outside it. He carries no ranged weapon,
   so the latter is generic template behavior, not a hidden ranged attack.
   `BDFIGH01.baf:580–595`.

There are branches for Berserker Rage, Kai, Called Shot, speed/strength/heroism
potions and antidotes, but the required resources are absent from this CRE.
Those branches must not be included in his actual loadout.

### Effective buffs and an Artisan's Kitpack boundary

- Invulnerability: base AC 0 and +5 saving throws; current item description says
  one in-game hour. Extra Healing restores 27 HP.
- Effective `SPCL152` is Artisan's Barbarian Rage. At level 10 its relevant ability
  supplies +6 STR/CON, a +2 save-vs-spell bonus, an AC penalty and level-drain
  recovery/protection for **30 seconds**. Its description also states a following
  five-round fatigue period. The exact passives/derived AC remain separate CRE
  questions; do not import the vanilla Rage immunity list from memory.
- Static recast concern: the Rage's `OFFENSIVE_MODIFIER` marker lasts 30 seconds.
  Its delayed `C0BAR#02` then applies another 30 seconds of immunity to `SPCL152`;
  that helper and its child `C0BAR#0A` do not extend the marker. The current AI only
  checks the marker before `RemoveSpell` plus `ForceSpell`. It can therefore
  attempt and spend another finite Rage while the fatigue lock still blocks the
  spell. This is a **source-backed compatibility risk, not a live-proven outcome**.
  Source: installed `SPCL152` level-10 ability, `SPCL152A`, `C0BAR#02`, `C0BAR#0A`;
  `ArtisansKitpack/lib/Barbarian.tpa:105–111` establishes the replacement family.

For the future design, a 30-second preparation window and a 30-second Rage cannot
be treated like long-duration prebuffs without considering when Rage begins.
This is a timing requirement to discuss, not an approved new spell package.

## Marius of Tethyr — `BDASHA03`, `BDPAL01`

Human Paladin (Cavalier) 10, 93 HP; plate +1, large shield +1, longsword +1, two Extra
Healing potions, one Stone Giant Strength potion. Prepared magic is Bless ×1,
Armor of Faith ×1, Lay on Hands ×1, Detect Evil ×6, Protection from Evil ×6 and
Remove Fear ×6.

| Actual action | Conditions and expenditure | Script |
|---|---|---|
| Lay on Hands on himself | Core+, below 80% HP, ready use, 6-second timer; ordinary `Spell`, one use. Current level-10 effect heals 20 HP | `BDPAL01:49–60` |
| Extra Healing | Normal+, below 75% HP; 100/50 choice; two potions, 27 HP each | `BDPAL01:62–77` |
| Protection from Evil on himself | Protection absent and an evil enemy within range 5, a third evil enemy detected, or last attacker evil; no difficulty gate. 100/35 choice, consumes one of six uses | `BDPAL01:96–110` |
| Stone Giant Strength | Core+, sees an enemy, STR below 19, innates allowed; 100/50 choice; one potion sets STR 20 | `BDPAL01:390–405` |
| Remove Fear on an ally | Visible living ally panicking, ready use; no difficulty gate. Candidate scan followed by 100/25 cast-or-continue choice; six uses | `BDPAL01:760–830` |
| Weapon attack | Nearest visible enemy, melee selection inside range 5; generic ranged selection outside it although no ranged weapon is carried | `BDPAL01:887–902` |

**Bless and Armor of Faith are prepared but have no cast/prebuff branches in
`BDPAL01`. Detect Evil is likewise unused.** This is why an inventory/spellbook
listing alone overstates his opening. He has no `bd_prebuff` chain at all.

The template's Inquisitor True Sight/Dispel Magic and priest Remove Paralysis
branches are unavailable for Marius because he has none of those prepared.
Remove Fear is reactive to an already panicking ally, not a planned group
prebuff. Protection from Evil is conditional on enemy alignment and will not
necessarily appear against every player party.

## Zoe Kryn — `BDASHA04`, `BDFTHI01`

Halfling Fighter 8 / Thief 10, 70 HP; studded leather +1, shortsword +1, four
Invisibility potions, one Extra Healing potion, and two ready Set Snare abilities.

- A first-ambush branch can apply `BDINVIS` when no enemy is detected, she belongs
  to the relevant hostile group, her ambush flag is clear, and Hide in Shadows is
  at least 150. It also excludes invisible/charmed/blind states via mask `0x42010`.
  This is a direct invisibility application, not a Hide skill action.
  `BDFTHI01.baf:19–33`.
- The CRE's base Hide in Shadows and other thief-skill bytes are zero. The first
  ambush branch must therefore not be called guaranteed without accounting for
  permanent/equipment effects and derived stats. Neither her direct CRE effects
  nor direct equipped-item effects provide that missing 150-point boost; no
  engine-derived skill was captured. Header offsets were checked
  against the [CRE format reference](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/cre_v1.htm).
- Her practical invisibility-potion branch is broader: not currently invisible,
  not barred from turning invisible, not neutral, timer ready and a potion
  present. It has **no enemy-sight or difficulty requirement**. Thus she can drink
  it before contact once made hostile, and use another after attacking/revealing
  herself. There are four finite uses, no replenishment loop.
  `BDFTHI01.baf:35–48`.
- On Normal+, below 75% HP, she may drink her single Extra Healing potion for
  27 HP. However the invisibility-potion branch precedes healing, so concealment
  can get the next action first. `BDFTHI01.baf:79–94`.
- If invisible, within range 5, or unable to become invisible, she equips melee
  and attacks the nearest visible enemy. Otherwise the final block requests a
  ranged weapon and attacks the nearest enemy; she has no ranged weapon in this
  snapshot. `BDFTHI01.baf:537–555`.

**There is no Set Snare, Hide, Detect Traps, Poison Weapon, flanking or explicit
backstab-victim selection action in this script.** Both prepared Set Snares are
unused. She can create a backstab opportunity using ordinary invisibility and
melee, but the script does not guarantee a successful backstab or seek a
particular vulnerable caster. Engine-facing and target-immunity conditions
still matter; this was not live tested.

## Balvin Steadyhand — `BDASHA06`, `BDFCLE01`

Dwarf Fighter 9 / Cleric 9, 81 HP; plate, medium shield +1, war hammer +1,
sling +1 and 40 bullets +2. One Extra Healing, one Clarity, and **two usable
Wand of the Heavens charges** are present. The wand's ability has a nonzero
maximum charge count and destroys the item at exhaustion; it is not a zero-use
decorative wand.

### Real opening chain

On first `Detect(NearestEnemyOf(Myself))`, while `bd_prebuff=0`, each matching
block removes one prepared copy, uses `ReallyForceSpell` on himself and continues
through the remaining opening blocks. The final block sets `bd_prebuff=1` and a
4-second defense timer. It does not wait for the new brawl's proposed preparation
clock; that clock does not exist in the native AI.

| Prepared opening spell | Difficulty for a hostile Balvin | Effective installed benefit | Source |
|---|---|---|---|
| Armor of Faith ×1 | Core+ | 10% physical/magic-damage reduction, 5 turns | `BDFCLE01:19–31` |
| Defensive Harmony ×1 | Core+ | +4 AC in a 10-foot area around caster, 1 turn; actual allies reached depend on position/delivery | `BDFCLE01:75–87` |
| Draw upon Divine Might ×1 | Core+ | +3 STR/DEX/CON at cleric 9, 1 turn | `BDFCLE01:89–101` |
| Free Action ×1 | Core+ guaranteed by this branch; Normal has a 50% random opening test | Movement-disabling-effect protection on himself, 1 turn/level | `BDFCLE01:201–217` |

The native template additionally lists Protection from Evil, Aid, Spiritual
Hammer, Righteous Magic, Blade Barrier, Resist Fire, a legacy Physical Mirror
entry, Shield of the Archons and Magic Resistance. **Balvin has none prepared**,
so these are not his existing prebuffs. The final opening flag is set even if
the difficulty rules skipped the buffs.

On Core+ the four available opening buffs spend their only copies. There is no
ordinary Armor of Faith, Draw upon Divine Might or Free Action refresh branch.
There is a later ordinary Defensive Harmony group-buff branch, but normally
the opening already consumed its sole copy. The template's two specialized
defense-recast blocks require spells Balvin does not have (`BDFCLE01:784–819`).
Consequently he should **not** be described as a cleric that repeatedly rebuilds
his full defenses.

### Prepared book and what he uses

| Effective prepared spell | Copies | Current use |
|---|---:|---|
| Sanctuary | 1 | Core+, below 65% HP, not already in Sanctuary, sees enemy, not silenced, healing remains: explicitly consume and force-cast |
| Armor of Faith | 1 | Opening as above |
| Command | 2 | Ordinary disabling casts against a living visible enemy not already disabled |
| Doom | 1 | Ordinary debuff, skips targets marked with Malison |
| Cure Light Wounds | 1 | Self-heal below 80% only if no enemy seen, untargetable or protected by Sanctuary |
| Chant | 1 | Ordinary group buff in combat, requires fourth-nearest ally within range 20 and unchanted allies in the checked pairs |
| Hold Person | 2 | Ordinary disabling cast; visible living humanoid not already disabled |
| Draw upon Divine Might | 1 | Opening only |
| Silence | 1 | Normal+; targets active enemy spellcasters with checks against silencing nearby allied mage/cleric units and Spell Turning |
| Slow Poison | 1 | Forced, explicitly consumed self-cure when poisoned |
| Remove Paralysis | 1 | Visible living ally stunned/helpless (`STATE` mask 40); ordinary cast |
| Miscast Magic | 1 | Enemy arcane/divine casters not already disabled and below 50% relevant spell failure; arcane branch checks Spell Turning |
| Gust of Wind (`SPPR318`) | 1 | **Unused**: no cast branch resolves to this resource |
| Invisibility Purge | 1 | Detects an opposing creature it cannot see and has no True Sight; ordinary self-centered cast |
| Free Action | 1 | Opening only |
| Defensive Harmony | 1 | Opening or later ordinary group cast if the copy remains |
| Cure Critical Wounds (`SPPR401`) | 1 | Self-heal under the same protected/no-sight conditions as Cure Light; current SR effect is 4d8+36 at cleric 9 |
| Mass Cure | 1 | Group heal when nearest enemy within range 30, a checked nearby ally below 65%, and either Balvin below 80%, another checked ally injured, or enough allies nearby; current effect is 2d8+18 at cleric 9 |

Current SR `SPPR401` is named **Cure Critical Wounds**, although the script
decompiles its numeric identity as `CLERIC_CURE_SERIOUS_WOUNDS`. The resource
still matches his prepared book; this is a misleading symbolic name, not a
missing cast. Conversely `SPPR318` is currently **Gust of Wind**, not whatever a
vanilla-number mnemonic suggests, and no template branch calls it.

Sources: `BDFCLE01.baf:228–428` healing/retreat protection; `1046–1088`
Invisibility Purge; `1106–1179` group buffs; `1201–1255` paralysis removal;
`1452–1787` Silence/Miscast/Doom/Hold/Command.

### Potions, offense and targeting priorities

- His Sanctuary-then-heal path has higher priority than offensive spells. While
  protected by Sanctuary, still below 80%, with a heal/potion remaining and an
  enemy visible, a `NoAction()` block keeps him from breaking Sanctuary with
  lower-priority offense on Normal+ (`BDFCLE01:413–428`). No flee movement is
  in that branch: he is pausing to heal, not pathing away.
- Extra Healing is considered below 75% on Normal+, 100/50 response weights,
  one 27-HP potion (`379–394`).
- Clarity is considered on Normal+ after seeing an enemy, with no Chaotic
  Commands stat, innates allowed and the defense timer clear. One potion;
  100/50 weights. Its effective description covers charm, fear, confusion and
  feeblemind protection for one hour (`470–488`).
- Wand of the Heavens comes late, after support and control options. It chooses
  from nearest enemy candidates, then uses a charge on a living visible target;
  100/25 response weights. Two charges are carried. Effective item describes
  8d6 fire damage, save-vs-wand for half (`1789–1853`).
- Final fallback is nearest-enemy weapon combat: hammer inside range 5, sling
  outside. He has both weapons, so this template fallback is meaningful
  (`1855–1870`).

The long `False()` candidate-scan blocks should not be classified as dead
abilities merely because their own responses never run. They update `LastSeenBy`
as predicates scan possible targets; the following cast blocks reuse that
object. There is no coordinated party-wide focus-fire controller here.

## Shared behavior and reset limits

All four use `BDDSC` override, `BDCRUSDS` class, `BDSHOUT` race and the individual
general scripts above. This ordering matters: native encounter behavior can
prevent the combat script from running.

- `BDDSC:25–39` turns them neutral and starts retreat once `bd_plot>439`.
  `BDDSC:91–116` makes them neutral/spectators during the duel and suppresses
  lower AI. These must not be accidentally reused as new brawl activation logic.
- `BDCRUSDS:1–22` assigns a random one of two arrival lanes, a courtyard
  destination, hostility and initially `bd_no_retreat=1`. `BDDSC:171–227` moves
  them along those lanes and eventually allows ordinary searching/retreat.
- `BDDSC:128–144` reads the existing poisoned-crusader-supplies global and can
  apply `BDWEAKDS`. Any new fresh-fight staging must deliberately account for
  inherited campaign effects instead of silently assuming a pristine stat line.
- `BDSHOUT:292–366` calls/answers assistance; it can draw these actors toward
  other same-group actors. A small arena alone is not a complete isolation rule.
- `BDSHOUT:447–493` eventually restores full health and rests an actor after
  retreat, the six-hour rest timer, no current combat and no detected enemy. It
  resets `bd_prebuff` and `bd_hide_in_ambush`; subsequent rests are spaced by a
  twelve-hour timer. This can recharge spell/innate books but does not recreate
  consumed potions or wand charges. **There is no in-fight infinite recharge.**

No new levels, spells, consumables, immunities or difficulty changes are selected
by this audit. The useful discussion inputs are the uneven current preparation,
finite copies, unused prepared abilities, support targeting, short-duration
timing, concealment counters, and explicit compatibility boundaries above.
