# Ashatiel's party: per-character reference sheets

Read-only extraction, 2026-09-26, from the Combined test install
(`%USERPROFILE%/CEBG-Tests/Combined-20260908/game`: SR, SCS, Artisan's Kitpack,
CDTweaks, EET and the rest of that stack). Facts only: what each of the seven
carries, what their spells actually do in this install, and what their current
AI does, in priority order. Nothing here is a proposal.

Sources: effective CRE/ITM/SPL/2DA files and the decompiled scripts in
`%USERPROFILE%/CEBG-Tests/Ashatiel-20260922/roster`. Companion docs:
[25](25-ashatiel-party-dossier.md), [25a](25a-ashatiel-arcane-ai.md),
[25b](25b-ashatiel-martial-divine-ai.md), [25d](25d-ashatiel-party-resource-ledger.md).

**Computed, not observed.** AC, THAC0 and damage below are worked out from the
installed tables (STRMOD/STRMODEX, DEXMOD, WSPECIAL, WSPATCK, STYLBONU, THAC0)
plus item and CRE effects. Nothing was checked in a running game. Melee attacks
per round come from WSPATCK. For bows, slings, darts and thrown daggers only the
item's own rate of fire is listed, because how proficiency adds to it was not
verified. Ranged damage marked † includes the proficiency damage bonus; whether
that bonus applies to ranged weapons in this install was not verified either.

Difficulty gates use the slider names: **Normal+** = Normal/Core/Hard/Insane,
**Core+** = Core/Hard/Insane, **Hard+** = Hard/Insane. (In script terms these
are `DifficultyGT(EASIEST)`, `DifficultyGT(EASY)` and `DifficultyGT(NORMAL)`.)

---

## At a glance

| | Ashatiel | Wormgums | Small Kimble | Marius | Zoe Kryn | Sarginson | Balvin |
|---|---|---|---|---|---|---|---|
| Race / class | Elf F9/M10/C9 | Gnoll Fighter 10 (Barbarian) | Gnome Illusionist 11 | Human Paladin 10 (Cavalier) | Halfling F8/T10 | Human F7/M10 | Dwarf F9/C9 |
| Alignment | LG | **CE** | NG | LG | NG | N | LN |
| HP | 67 | 93 | 41 | 93 | 70 | 82 | 81 |
| AC (general / vs missile) | −3 / −4 | 2 / 2 | 10 / 10 | −3 / −8 | 0 / −1 | 7 / 7 | 1 / −3 |
| Main weapon, THAC0, damage | Mace +2, 8, 1d6+6 | Halberd +2, 6, 1d10+10 | Darts of Stunning, 17, 1d3 + stun | Long Sword +1, 7, 1d8+6 | Short Sword +1, 10, 1d6+4 | Longbow +1 w/ Fire Arrows +2, 5, 1d6+7† +1d6 fire | War Hammer +1, 9, 1d4+7 |
| Melee attacks/round | 2 | 2 | 1 | 2 | 2 | 1½ (non-proficient long sword) | 2 |
| Saves D/W/P/B/S | 6/8/7/8/9 | 8/10/9/9/11 | 11/3/9/11/4 | 6/8/7/7/9 | 6/6/10/12/7 | 10/9/11/12/10 | 2/5/4/4/6 |
| Crit-immune (helmet) | **no** | yes | **no** | yes | yes | **no** | yes |
| Kill XP | 5000 | 2000 | 3000 | 2000 | 2000 | 3000 | 2000 |

Totals: 527 HP, 19,000 kill XP. All numbers above are before buffs. Each sheet
lists what the opening buffs change.

---

## How their AI works (all seven)

**Script stack.** Ashatiel: `BDASHATI` (story) → `BDSHOUT` → `BDFMCL01`.
The six escorts: `BDDSC` (story) → `BDCRUSDS` → `BDSHOUT` → their own general
script. These are native SoD scripts; SCS did not generate AI for them.

**Priority list.** Every tick the general script is read top to bottom and the
first block whose conditions pass runs. Most blocks have two weighted responses,
e.g. 100 "do it" / 50 "skip to the next block". So "100/50" means a 2-in-3
chance to act when that block is reached. Blocks that are not weighted always
act.

**One spell or item per round.** Every spell and item use sets a 6-second
`bd_cast` timer and every spell/item block requires it to be clear. While the
timer runs, the script falls through to the weapon blocks at the bottom. So a
caster casts, fights with a weapon for the rest of the round, then casts again.

**The opening.** Balvin and the three arcane casters have an instant opening
buff chain. It fires the first time they `Detect` an enemy, which includes
hearing. Each buff removes one prepared copy and is force-cast with no casting
time. Afterwards a flag stops the chain from repeating and the defensive-recast
timer is set to 4 seconds. Wormgums, Marius and Zoe have no opening chain.

**Defensive recasts.** These share a 15-second `bd_defence_timer`, so at most one
recast per 15 seconds. They can only use prepared copies that remain.

**Targeting.** Most offensive spells use a "scan" block that walks the nearest
enemies (usually 3–10) and remembers the first visible one that fits, for example
not already disabled or not already Malisoned. The cast block right after it
targets that creature. Damage spells and wands pick among the three nearest
visible enemies: 50% the nearest, then the 2nd, then the 3rd. There is no shared
focus-fire and no party-level coordination.

**Weapon fallback.** Nearest visible enemy. They use their best melee weapon if
that enemy is within script range 5; otherwise they switch to a ranged weapon if
they have one and keep attacking.

**Story-layer behaviour that is live in BD4000 today:**
- `BDDSC` (escorts only):
  - **Death:** a dead escort is removed with `DestroySelf()` after the kill
    counters update.
  - **Plot 439:** once `bd_plot` passes 439 they turn neutral and retreat.
  - **Duel:** while the duel is running they stand neutral, and attacking during
    it sets the cheating flag.
  - **Poisoned supplies:** if you poisoned the crusader supplies
    (`bd_poison_dsc_supplies` = 1 or 2) they get **`BDWEAKDS`, a permanent −2
    THAC0**.
  - **Approach:** they walk their approach lanes while no enemy is in sight.
- `BDCRUSDS`: picks one of two approach lanes at random, makes them hostile and
  sets `bd_no_retreat=1`.
- `BDSHOUT`: `Enemy()` plus `Shout(ASSIST)` when combat starts, answers ASSIST
  calls from the same group, and heals/rests out of combat after a retreat. That
  rest resets the opening flag, but it never runs during a fight.
- `BDASHATI`:
  - Dialogue, duel rules and cheating detection.
  - In the solo duel on Easy it destroys her Wand of Frost and removes both
    Mirror Images and her Spell Deflection. That is duel-only.

---

## 1. Ashatiel (`BDASHATI`)

Elf, Fighter 9 / Mage 10 / Cleric 9, Lawful Good, 67 HP.
STR 17 · DEX 18 · CON 16 · INT 16 · WIS 16 · CHA 15. Morale 20.
Stored CRE effect: **movement +3**. Proficiencies: Mace ★★, Dagger ★★,
Sword-and-Shield style ★★.

**Base numbers**
- AC −3. Vs missile −4 (the shield doesn't count against missiles, the style's +4
  does), vs crushing −4, vs slashing −6.
- Mace +2: THAC0 8, 1d6+6 crushing, 2 attacks.
- Throwing Daggers: THAC0 8, 1d4+3†, rate of fire 2.
- Saves 6/8/7/8/9.
- **Can be critically hit**: the item in her helmet slot has the flag that turns
  helmet crit protection off.

**After her Core+ opening**
- AC −4.
- Mace: THAC0 5, 1d6+13 (STR 20 from Draw upon Divine Might; Aid adds +1 to hit).
- +9 HP.
- 5 Stoneskins.
- Minor Globe.
- 10% resistance to physical and magic damage.

### Gear
| Slot | Item | Effect in this install |
|---|---|---|
| Helmet | `BDERINYE` (appearance item) | No stats; disables helmet crit protection |
| Armor | Adventurer's Robe | +1 AC vs crushing, +1 save vs polymorph |
| Shield | Small Shield +2 | +3 AC, **no protection against missiles** |
| Gloves | Bracers of Defense AC 5 | Base AC 5 |
| Right ring | Ring of Free Action | Immune to hold, paralysis, slow, haste (op16), web, entangle, grease and movement-rate changes (op126) |
| Amulet | `MINHP1` (story item) | Minimum 1 HP plus a long immunity list. **Destroyed by her intro dialogue** before the duel/refusal choice |
| Belt | Golden Girdle | +3 AC vs slashing |
| Cloak | Cloak of Protection +1 | +1 AC, +1 all saves |
| Weapons | Throwing Dagger ×20 (undroppable), Mace +2 (1d6+3, +2) | |

### Consumables
- Potion of Extra Healing ×2: heals 27.
- Potion of Magic Shielding ×1: +20 to all saves (effectively automatic
  success) and 50% resistance to fire, cold, electricity, acid and magic damage,
  3 turns.
- Wand of Frost, 5 charges: 8d6 cold cone, save vs wand for half.
- Random slot `DW#RND26`: 50% nothing; otherwise 12.5% each of Hill Giant
  Strength, Heroism, Oil of Speed or Defense. These spawn as SCS's undroppable
  `DW#PTN` copies, and **no script in her stack uses them**.
- `DW#HASPT` "Mirror": SCS marker item with no effect.

### Spellbook (priest level 9, wizard level 10)
| Spell | × | What it does here |
|---|---:|---|
| Command | 1 | Target sleeps 1 round, save vs spell −5 |
| Resist Fear | 2 | Allies in a 30' radius: fear removed, immune to fear for 5 turns |
| Sanctuary | 2 | 6 rounds |
| Armor of Faith | 1 | 10% resistance to slashing/crushing/piercing/missile/magic damage, 5 turns |
| Aid | 1 | +1 to hit and saves (SR's text also claims +1 damage); +9 HP; 9 turns |
| Chant | 1 | Allies +1 to hit, damage and saves; enemies −1; 1 turn (the caster moves at half speed meanwhile) |
| Silence | 2 | 15' radius, save vs spell −5, 1 turn |
| Slow Poison | 1 | Cures poison |
| Draw upon Divine Might | 1 | +3 STR/DEX/CON, 1 turn |
| Invisibility Purge | 1 | Strips invisibility around her once a round for 5 rounds |
| Holy Smite | 2 | 20' radius, 9d4 magic damage (4d4 unavoidable + 5d4 negated by save vs spell); blinded 1 round on a failed save |
| Cure Critical Wounds | 2 | Heals 4d8+36 |
| Greater Command | 1 | Target plus enemies within 20': sleep up to 1 turn, save vs spell −4, a new save every round |
| Obscuring Mist | 2 | 20' cloud for 6 rounds: −2 to hit inside, sight halved, ranged attacks into it at −4 |
| Magic Missile | 2 | 5 × 1d4+1 |
| Detect Invisibility | 1 | See-invisible for 5 rounds plus a reveal pulse every round |
| Mirror Image | 2 | 5 images, 5 turns |
| Vocalize | 1 | Removes silence; immune to silence for 1 turn |
| Flame Arrow | 2 | 5 arrows, each 1d6 missile + 1d6 fire. The first hits the target; the rest pick random enemies |
| Slow | 1 | Enemies in a 30' radius, save vs polymorph −3: slowed, −2 to hit/AC/saves vs breath, 1 turn |
| Minor Globe of Invulnerability | 1 | Immune to 1st–3rd level spells, 2 turns |
| Stoneskin | 1 | 5 skins |
| Secret Word | 1 | Strips the highest spell protection of 7th level or lower |
| Breach | 1 | Strips all combat and specific protections |
| Spell Deflection | 1 | Deflects 9 levels of 1st–7th level spells, 5 turns |

### Opening (first Detect)
- **Easy:** nothing.
- **Normal:** Stoneskin 50%, Minor Globe 50%.
- **Core+:** Armor of Faith, Aid, Draw upon Divine Might, Stoneskin and Minor
  Globe, all at once.

### AI, in priority order
1. Story stops: `bd_no_combat=2`, or retreat mode.
2. Opening chain (above).
3. **Sanctuary**:
   - Core+, below 65% HP, sees an enemy.
   - Not silenced, and a Cure Critical Wounds or Extra Healing is left.
4. **Slow Poison** when poisoned.
5. **Cure Critical Wounds** on herself: below 80% HP, while no enemy is in sight
   or she is under Sanctuary or untargetable.
6. **Extra Healing** potion: Normal+, below 75% HP (100/50).
7. **Vocalize** when silenced.
8. **Holds still** (Normal+) while under Sanctuary, below 80% HP, with an enemy in
   sight and a heal left. This keeps her from breaking Sanctuary.
9. **Magic Shielding** potion: Normal+, sees an enemy, defense timer clear (100/50).
   In practice this is about 4 seconds after her opening.
10. **Stoneskin** recast (100/35): no images and no skins left. Only possible on
    Easy/Normal, where the opening may not have used it.
11. **Mirror Image** (100/50): no images and no skins left. Two copies.
12. **Spell Deflection** (100/50): no spell protection up and an enemy
    mage/cleric/bard/druid in sight.
13. **Minor Globe**: same condition, only if still unused.
14. **Holy Smite** (100/50):
    - Only at a visible **evil** enemy.
    - Only if no evil creature on her own side is within range 22 of the target.
      That creature is Wormgums.
15. **Invisibility Purge**, else **Detect Invisibility** (100/50): she detects a
    player-side creature she cannot see.
16. **Breach** (100/100):
    - First pass: the first visible enemy with Stoneskin or weapon protection. It
      checks the three nearest enemy mages, then the five nearest enemies.
    - Second pass: an enemy with a damage-protection or effect-protection buff.
17. **Secret Word** (100/100): first of the 5 nearest enemies with a spell
    protection up.
18. **Slow** (100/35):
    - First choice: a visible enemy in the hasted state.
    - Otherwise: an enemy with another enemy within 15 who isn't slowed yet.
19. **Chant** (100/50): enemy within 30, at least 4 of her allies within 20, and
    not all of them chanted.
20. **Resist Fear** (100/25) on a panicking ally.
21. **Greater Command** (100/50): Core+, the nearest visible enemy that isn't
    already debuffed.
22. **Silence** (100/50):
    - Normal+.
    - An enemy mage or cleric who is not within 15 of any mage or cleric on her
      side, including herself.
    - Target still able to cast and without Spell Turning.
23. **Command** (100/50): a nearby enemy that isn't disabled. Random-weighted
    toward the nearest.
24. **Obscuring Mist** (100/50): at a visible enemy warrior type that isn't
    debuffed. Random-weighted.
25. **Flame Arrow**, then **Wand of Frost**, then **Magic Missile** (each 100/25),
    each at one of the 3 nearest enemies.
26. **Weapon**: mace within range 5, otherwise throwing daggers.

Not in her book, so these generic branches never fire: Haste, Shield, Blur,
Improved Invisibility, Remove Magic/Dispel, summons. Armor of Faith, Aid and
Draw upon Divine Might are only ever cast in the opening; there is no recast
branch for them.

---

## 2. Wormgums (`BDASHA01`)

Gnoll Fighter 10 with the Barbarian kit, **Chaotic Evil**, 93 HP. Natural AC 5.
STR 18/95 · DEX 17 · CON 17 · INT 10 · WIS 10 · CHA 10.
Stored CRE effect: **movement +2**. No other Barbarian passives are stored on the
creature; for example there is no backstab-immunity effect.
Proficiencies: Halberd ★★, Two-Handed style ★★.

**Base numbers**
- AC 2.
- Halberd +2: THAC0 6, 1d10+10 slashing/piercing, 2 attacks, crits on 19–20.
- Saves 8/10/9/9/11. Crit-immune (undroppable hidden helmet).

**During Rage** (30 seconds):
- STR 24: THAC0 2, 1d10+17 per hit.
- AC 4, +2 save vs spell.
- Immune to level drain.

**With the Invulnerability potion:** base AC 0, so AC −3; +5 all saves.

### Gear
- Hidden helmet (`HELMNOAN`, undroppable): crit protection only.
- Halberd +2 (1d10+2, speed 7, undroppable).
- `UNICAEL2` cloak: colors only.

### Consumables
- Extra Healing ×2: heals 27.
- Potion of Invulnerability ×1: base AC 0, +5 saves, 1 hour.
- No random potion slot.

### Innate abilities
- **Barbarian Rage** ×3 (Artisan's version, level 10):
  - For 30 seconds: +6 STR, +6 CON, +2 save vs spell, −2 AC, level drain restored
    and blocked.
  - Then 30 seconds of fatigue, during which Rage cannot be used again.

### AI, in priority order
1. Story stops.
2. **Extra Healing**: Normal+, below 75% HP (100/50).
3. **Barbarian Rage** (100/35): Core+, sees an enemy, and his "raging" marker
   stat (`OFFENSIVE_MODIFIER`) is 0.
4. **Potion of Invulnerability** (100/50): Normal+, sees an enemy, defense timer
   clear, and AC above 0 or save vs spell above 0. At AC 2 this is true right
   away.
5. **Weapon**: halberd at the nearest visible enemy. He has no ranged weapon, so
   outside range 5 he just walks in.

No opening chain. The template's branches for Berserker rage, Kai, Called Shot
and other potions have nothing to use.

---

## 3. Small Kimble (`BDASHA02`)

Gnome Illusionist 11, Neutral Good, **41 HP**.
STR 10 · DEX 10 · CON 15 · INT 18 · WIS 16 · CHA 10.
Proficiencies: Dagger ★, Dart ★.

**Base numbers**
- AC 10, no armor.
- Darts of Stunning: THAC0 17, 1d3, rate of fire 3. Each hit: save vs spell or
  **stunned 7 rounds**.
- Dagger: THAC0 17, 1d4.
- Saves 11/3/9/11/4. **Can be critically hit** (no helmet).

**After her Core+ opening**
- Blur + Shield: AC 5, vs missile 1.
- Protection from Missiles, 5 Mirror Images, Improved Invisibility, Minor Globe.

### Gear
- Dagger (undroppable).
- Darts of Stunning ×20.
- `UNICAEL2` cloak: colors only.

### Consumables
- Extra Healing ×1.
- Wand of Paralyzation, 4 charges (undroppable): stun 1 turn, save vs wand −4.
- No random potion slot. `DW#HASPT` marker only.

### Spellbook (wizard level 11)
| Spell | × | What it does here |
|---|---:|---|
| Magic Missile | 4 | 5 × 1d4+1 |
| Shield | 1 | +2 AC, +4 vs missiles, immune to Magic Missile, 5 turns |
| Blur | 1 | Attackers −3 (AC +3 vs all types), +3 save vs spell, 5 turns |
| Detect Invisibility | 1 | See-invisible plus a reveal pulse every round, 5 rounds |
| Mirror Image | 2 | 5 images, 5 turns |
| Vocalize | 1 | Removes silence |
| Flame Arrow | 1 | 5 × (1d6 missile + 1d6 fire) |
| Fireball | 1 | 10d6 fire, save vs breath −3 for half |
| Haste | 2 | Allies in an area: +6 movement, +½ attack, 90 seconds, then 3 rounds of −2 to hit/damage/AC |
| Protection from Missiles | 1 | Immune to normal missiles, 1 turn |
| Confusion | 1 | Area, 5 rounds, save vs spell −2 |
| Improved Invisibility | 1 | 84 seconds |
| Minor Globe of Invulnerability | 1 | Immune to 1st–3rd level spells, 2 turns |
| Greater Malison | 1 | Enemies in a 30' radius: −2 all saves, −1 luck, 2 turns, no save |
| Shadow Door | 1 | Invisible 66 seconds; enemies within 5' save vs spell or are trapped up to 4 rounds |
| Hold Monster | 1 | 1 turn, save vs spell −2 |
| Waves of Fatigue | 1 | Enemies in a 30' radius: +7 fatigue for 5 rounds, no save, stacks |
| Spell Deflection | 1 | 9 levels of 1st–7th level spells, 5 turns |

### Opening (first Detect)
- **Easy:** nothing.
- **Normal:** Protection from Missiles, Mirror Image, Improved Invisibility and
  Minor Globe, 50% each. The random rolls share a tick, so they are not
  independent.
- **Core+:** Blur, Shield, Protection from Missiles, Mirror Image, Improved
  Invisibility and Minor Globe.

### AI, in priority order
1. Story stops.
2. Opening chain.
3. **Extra Healing**: Normal+, below 75% HP (100/50).
4. **Vocalize** when silenced.
5. **Mirror Image** (100/50): no images and no skins. One copy left after a Core+
   opening.
6. **Protection from Missiles** (100/50): no weapon protection up. Only if still
   unused.
7. **Spell Deflection** (100/50): no spell protection up and an enemy caster in
   sight.
8. **Minor Globe**: same condition, only if still unused.
9. **Shadow Door** (100/50): not improved-invisible, able to turn invisible, sees
   an enemy.
10. **Improved Invisibility**: same condition, only if still unused.
11. **Fireball** (100/50):
    - Core+.
    - Target: the farthest visible enemy that has another enemy within 15 **and no
      member of her own side within 22**.
12. **Detect Invisibility** (100/50): detects an enemy she cannot see.
13. **Haste** (Core+; always on Hard+, 100/35 on Core):
    - First choice: a slowed ally.
    - Otherwise: the first of her 5 nearest allies who is in sight, has another
      ally within 15 and is not in the hasted state. Also needs an enemy within 30
      and her 24-second Haste timer clear.
14. **Waves of Fatigue** (100/50): Core+, the nearest visible enemy that isn't
    debuffed.
15. **Confusion** (100/50): Core+, same target rule.
16. **Greater Malison** (100/50): the first of the 3 nearest enemies not already
    Malisoned.
17. **Hold Monster**, then **Wand of Paralyzation** (each 100/50): a nearby enemy
    that isn't disabled. Random-weighted toward the nearest.
18. **Flame Arrow**, then **Magic Missile** (100/25), at one of the 3 nearest
    enemies.
19. **Weapon**: dagger within range 5; otherwise darts. If a ranged weapon is
    already equipped she keeps shooting.

No Stoneskin, Breach, Secret Word, Spell Thrust or dispel, so the generic
anti-magic and Stoneskin branches can never fire. Blur and Shield have no recast
branch.

---

## 4. Marius of Tethyr (`BDASHA03`)

Human Paladin 10 with the Cavalier kit, Lawful Good, 93 HP.
STR 18/51 · DEX 17 · CON 15 · INT 10 · WIS 14 · CHA 17.
Proficiencies: Long Sword ★★, Sword-and-Shield style ★★.

Stored Cavalier effects:
- Immune to charm, fear/horror/morale break and poison.
- **20% fire and acid resistance.**

**Base numbers**
- AC −3. Vs missile −8, vs slashing −6.
- Long Sword +1: THAC0 7, 1d8+6 slashing, 2 attacks.
- Saves 6/8/7/7/9. Crit-immune (helmet).

**With Stone Giant Strength (STR 20):** THAC0 6, 1d8+11.

### Gear
| Slot | Item | Effect |
|---|---|---|
| Helmet | Helmet (undroppable) | Crit protection |
| Armor | Plate Mail +1 (undroppable) | Base AC 2, +3 vs slashing |
| Shield | Large Shield +1 | +2 AC, +1 vs missiles |
| Weapon | Long Sword +1 (1d8+1, undroppable) | |
| Cloak | `UNICAEL2` | Colors only |

### Consumables
- Extra Healing ×2.
- Potion of Stone Giant Strength ×1: STR 20 for 2 hours.
- Random `DW#RND12`: 60% nothing, 20% Freedom, 20% Invulnerability.
- Random `DW#RND28`: 33% nothing, 22% Oil of Speed, 11% each Hill Giant
  Strength, Stone Giant Strength, Heroism, Power.
- Both random slots are **undroppable `DW#PTN` copies and unused by his
  scripts**.

### Prepared abilities (paladin casting level 2)
| Ability | × | What it does here | Used by AI? |
|---|---:|---|---|
| Bless | 1 | Area: +1 to hit and morale, 5 turns | **no** |
| Armor of Faith | 1 | 10% physical/magic damage resistance, 5 turns | **no** |
| Lay on Hands | 1 | Heals 20 | yes |
| Detect Evil | 6 | Highlights evil creatures | **no** |
| Protection from Evil | 6 | On himself, 5 turns, against evil creatures | yes |
| Remove Fear | 6 | Allies in a 30' radius: fear removed, immune to fear for 5 turns | yes |

### AI, in priority order
1. Story stops.
2. **Lay on Hands** on himself: Core+, below 80% HP.
3. **Extra Healing**: Normal+, below 75% HP (100/50).
4. **Protection from Evil** on himself (100/35), any difficulty. It needs:
   - no Protection from Evil up already, and
   - an evil enemy within 5, or a third evil enemy detected, or his last attacker
     was evil.
5. **Stone Giant Strength**: Core+, sees an enemy, STR below 19 (100/50). This is
   his first action on sight.
6. **Remove Fear** (100/25) on a panicking ally.
7. **Weapon**: long sword at the nearest visible enemy. He has no ranged weapon.

No opening chain.

---

## 5. Zoe Kryn (`BDASHA04`)

Halfling Fighter 8 / Thief 10, Neutral Good, 70 HP.
STR 17 · DEX 19 · CON 16 · INT 10 · WIS 10 · CHA 10.
Proficiencies: Short Sword ★★, Single-Weapon style ★★.
**All thief skills are 0 in the CRE**, including Hide in Shadows.

**Base numbers**
- AC 0. Vs piercing −1, vs slashing −2, vs missile −1.
- Short Sword +1: THAC0 10, 1d6+4 piercing, 2 attacks, crits on 19–20.
- Backstab ×4 (thief 10, standard table).
- Saves 6/6/10/12/7. Crit-immune (helmet).

### Gear
| Slot | Item | Effect |
|---|---|---|
| Helmet | Helmet (undroppable) | Crit protection |
| Armor | Studded Leather +1 (undroppable) | Base AC 6, +1 vs piercing, +2 vs slashing, +1 vs missile |
| Weapon | Short Sword +1 (1d6+1) | |
| Cloak | `UNICAEL2` | Colors only |

### Consumables
- Potion of Invisibility ×4.
- Extra Healing ×1.
- Random `DW#RND25`:
  - 50% nothing; otherwise 12.5% each of Hill Giant Strength, Heroism, Oil of
    Speed or Defense.
  - These are **real, droppable potions**, and her script has a branch for each.
- Random `DW#RND12`: 60% nothing, 20% Freedom, 20% Invulnerability. Undroppable
  `DW#PTN` copies, **unused**.

### Innate abilities
- Set Snare ×2: **never used**; there is no branch for it.

### AI, in priority order
1. Story stops.
2. **Ambush invisibility** (`BDINVIS`) before any enemy is detected. Requires Hide
   in Shadows ≥ 150; hers is 0, so **this never fires**.
3. **Invisibility potion**: whenever she is visible, able to turn invisible and not
   neutral.
   - No need to see an enemy, no difficulty gate, no skip weight.
   - She drinks one as soon as she is hostile, attacks out of invisibility, then
     drinks the next. Four potions means four re-approaches.
4. **Extra Healing**: Normal+, below 75% HP (100/50).
5. Random-roll potions, only if she rolled them:
   - **Defense**: Normal+, and only if her AC is above 0. At AC 0 it never fires.
   - **Oil of Speed**: Core+, not hasted.
   - **Hill Giant Strength**: Core+, STR below 19.
   - **Heroism**: Core+, no enhancement buff.
   - All four need an enemy in sight and use 100/50.
6. **Weapon**: short sword if the nearest enemy is within 5, or if she is
   invisible or can't turn invisible. Otherwise the script tries a ranged weapon,
   which she doesn't have, and attacks the nearest enemy.

There is no Hide action, trap-setting, poison use, flanking or target choice. A
backstab only happens if the engine allows it on her attack out of invisibility.

---

## 6. Sarginson (`BDASHA05`)

Human Fighter 7 / Mage 10, True Neutral, 82 HP.
STR 18/15 · DEX 17 · CON 10 · INT 17 · WIS 10 · CHA 10.
Proficiencies: **Longbow ★★★★**, Short Sword ★★. He carries a long sword, not a
short sword.

**Base numbers**
- AC 7, no armor.
- Composite Longbow +1 with Arrows of Fire +2: THAC0 5, 1d6+7† missile plus 1d6
  fire (save vs spell negates the fire). Rate of fire 2.
- Long Sword +1, **non-proficient**: THAC0 14, 1d8+4, 1½ attacks.
- Saves 10/9/11/12/10. **Can be critically hit** (no helmet).

**After his Core+ opening**
- Shield: AC 5, vs missile 1.
- Protection from Normal Weapons, 5 Mirror Images, Improved Invisibility, Minor
  Spell Deflection.

### Gear
- Composite Longbow +1 (+2 to hit, +1 damage; needs STR 18).
- Arrows of Fire +2 ×40.
- Long Sword +1 (undroppable).
- `UNICAEL2` cloak: colors only.

### Consumables
- Extra Healing ×1.
- Wand of Frost, 4 charges (undroppable): 8d6 cold cone, save vs wand for half.
- Random `DW#RND26`: 50% nothing, 12.5% each of Hill Giant Strength, Heroism,
  Oil of Speed or Defense. Undroppable `DW#PTN` copies, **unused**.
- Random `DW#RND37`: 50% one Potion of Invisibility, 25% two, 25% nothing.
  Real droppable potions, but **his script has no branch to drink them**.

### Spellbook (wizard level 10)
| Spell | × | What it does here |
|---|---:|---|
| Obscuring Mist | 1 | 20' cloud, 6 rounds |
| Magic Missile | 2 | 5 × 1d4+1 |
| Shield | 1 | +2 AC, +4 vs missiles, immune to Magic Missile, 5 turns |
| Horror | 1 | Area panic 5 rounds, save vs spell −1 |
| Melf's Acid Arrow | 1 | 1d6 missile + 2d4 acid, then 2d4 acid each round for 3 rounds |
| Mirror Image | 2 | 5 images, 5 turns |
| Haste | 1 | As Kimble's, 84 seconds |
| Minor Spell Deflection | 1 | 6 levels of 1st–4th level spells, 5 turns |
| Spell Thrust | 1 | 15' radius: strips one spell protection of 5th level or lower from each enemy |
| Improved Invisibility | 1 | 78 seconds |
| Emotion, Hopelessness | 1 | 7' radius, stun 1 turn, save vs spell |
| Feeblemind | 1 | Permanent, save vs spell −4 |
| Protection from Normal Weapons | 1 | Immune to non-magical weapons, 1 turn |

### Opening (first Detect)
- **Easy:** nothing.
- **Normal:** Protection from Normal Weapons, Mirror Image, Improved
  Invisibility and Minor Spell Deflection, 50% each.
- **Core+:** Shield, Protection from Normal Weapons, Mirror Image, Improved
  Invisibility and Minor Spell Deflection.

### AI, in priority order
1. Story stops.
2. Opening chain.
3. **Extra Healing**: Normal+, below 75% HP (100/50).
4. **Mirror Image** (100/50): no images and no skins. One copy left.
5. **Protection from Normal Weapons**, **Minor Spell Deflection** and **Improved
   Invisibility** recasts. Each needs its protection to be down, and each is only
   possible if the opening didn't already spend the copy.
6. **Spell Thrust** (100/100): the first of the 5 nearest enemies with a spell
   protection.
7. **Haste**: same rules as Kimble. One copy.
8. **Emotion, Hopelessness** (100/50): Core+, the nearest visible enemy that isn't
   debuffed.
9. **Horror** (100/50): the nearest enemy without fear protection that isn't
   disabled.
10. **Feeblemind** (100/50): a nearby enemy that isn't disabled. Random-weighted.
11. **Obscuring Mist** (100/50): an enemy warrior type that isn't debuffed.
    Random-weighted.
12. **Wand of Frost**, then **Melf's Acid Arrow**, then **Magic Missile** (each
    100/25), at one of the 3 nearest enemies.
13. **Weapon**: long sword within range 5, otherwise the bow. He doesn't move to
    keep distance.

---

## 7. Balvin Steadyhand (`BDASHA06`)

Dwarf Fighter 9 / Cleric 9, Lawful Neutral, 81 HP.
STR 18/15 · DEX 10 · CON 19 · INT 10 · WIS 18 · CHA 10.
Proficiencies: War Hammer ★★, Sling ★★, Sword-and-Shield style ★★.

**Base numbers**
- AC 1. Vs missile −3, vs slashing −2.
- War Hammer +1: THAC0 9, 1d4+7 crushing, 2 attacks.
- Sling +1 with Bullets +2: THAC0 8, 1d4+6†, rate of fire 1.
- Saves 2/5/4/4/6. Crit-immune (helmet).

**After his Core+ opening**
- Defensive Harmony: AC −3.
- Hammer: THAC0 6, 1d4+13 (STR 21 from Draw upon Divine Might).
- 10% damage resistance; Free Action.

### Gear
| Slot | Item | Effect |
|---|---|---|
| Helmet | Helmet (undroppable) | Crit protection |
| Armor | Plate Mail | Base AC 3, +3 vs slashing |
| Shield | Medium Shield +1 (undroppable) | +2 AC |
| Weapons | War Hammer +1 (1d4+2, undroppable), Sling +1, Bullets +2 ×40 | |
| Cloak | `UNICAEL2` | Colors only |

### Consumables
- Extra Healing ×1.
- Potion of Clarity ×1: immune to charm, confusion, fear and feeblemind; 1 hour.
- Wand of the Heavens, 2 charges (undroppable): 8d6 fire with 1s counted as 2s,
  one target, save vs wand for half.
- Random `DW#RND26`: undroppable `DW#PTN` copies, **unused**.

### Spellbook (priest level 9)
| Spell | × | What it does here |
|---|---:|---|
| Command | 2 | Sleep 1 round, save vs spell −5 |
| Cure Light Wounds | 1 | Heals 1d8+9 |
| Sanctuary | 1 | 6 rounds |
| Armor of Faith | 1 | 10% physical/magic damage resistance, 5 turns |
| Doom | 1 | −2 to hit, damage and saves, 1 turn, save vs spell −5 |
| Chant | 1 | Allies +1, enemies −1, 1 turn |
| Hold Person | 2 | Humanoids, 1 turn, save vs spell −1 |
| Silence | 1 | 15' radius, save vs spell −5, 1 turn |
| Slow Poison | 1 | Cures poison |
| Draw upon Divine Might | 1 | +3 STR/DEX/CON, 1 turn |
| Remove Paralysis | 1 | 30' radius: cures hold, stun and paralysis |
| Invisibility Purge | 1 | Strips invisibility around him each round for 5 rounds |
| Miscast Magic | 1 | Target's spells misfire; 5 rounds with repeat saves, save vs spell −2 |
| Gust of Wind | 1 | **Never cast** (no branch) |
| Cure Critical Wounds | 1 | Heals 4d8+36 |
| Free Action | 1 | 9 turns, immune to hold, slow, web, entangle and similar |
| Defensive Harmony | 1 | +4 AC to everyone within 10' of him, 1 turn |
| Mass Cure | 1 | Heals 2d8+18 to allies around him |

### Opening (first Detect)
- **Easy:** nothing.
- **Normal:** Free Action 50%.
- **Core+:** Armor of Faith, Defensive Harmony, Draw upon Divine Might and Free
  Action.

### AI, in priority order
1. Story stops.
2. Opening chain.
3. **Sanctuary**: Core+, below 65% HP, sees an enemy, not silenced, a heal left.
4. **Slow Poison** when poisoned.
5. **Mass Cure**:
   - An enemy is within 30 and one of his 4 nearest allies is below 65% HP.
   - Plus one of: he is below 80% HP, his 8th-nearest ally is within 20, or his
     5th or 6th nearest ally is below 65% HP.
   - No skip weight.
6. **Cure Critical Wounds**, then **Cure Light Wounds**, on himself: below 80% HP,
   while no enemy is in sight or he is under Sanctuary or untargetable.
7. **Extra Healing**: Normal+, below 75% HP (100/50).
8. **Holds still** under Sanctuary (Normal+) while below 80% HP with a heal left.
9. **Clarity** potion: Normal+, sees an enemy, defense timer clear (100/50). This
   is his first action after the opening.
10. **Invisibility Purge** (100/50): detects an enemy he cannot see.
11. **Defensive Harmony** recast (100/50): only if the opening didn't use it.
    Needs an enemy within 30, 4 allies within 20 and some of them without it.
12. **Chant** (100/50): same pattern.
13. **Remove Paralysis** (100/25) on an ally who is held or stunned.
14. **Silence** (100/50): Normal+, same rules as Ashatiel's.
15. **Miscast Magic** (100/50):
    - First an enemy mage below 50% spell failure, able to cast and without Spell
      Turning.
    - Then an enemy cleric or druid.
16. **Doom** (100/50): the first of the 3 nearest enemies without a Malison-type
    debuff.
17. **Hold Person**, else **Command** (100/50): a nearby enemy that isn't
    disabled. Hold Person only works on humanoids. Random-weighted.
18. **Wand of the Heavens** (100/25): one of the 3 nearest enemies.
19. **Weapon**: hammer within range 5, otherwise the sling.

---

## Verified quirks and mismatches

1. **Holy Smite only goes at evil PCs.** Ashatiel's script uses targeting written
   for vanilla Holy Smite, which only hurt evil creatures. It only targets an evil
   enemy, and holds off if Wormgums is near that target. The installed SR spell's
   description says it hits all opponents in the area. Against a party with no
   evil members she never casts either copy.
2. **Their scripts don't recognise SR Haste.** SR Haste doesn't put anyone in the
   hasted state that the scripts check.
   - Kimble and Sarginson can cast Haste again on an ally who already has it.
     After their 24-second timer this wastes a copy (the spell blocks itself from
     stacking).
   - Ashatiel's "Slow the hasted enemy" branch never sees SR-hasted PCs. Only her
     cluster branch fires.
3. **Rage can be wasted.** Wormgums's "not raging" check clears after 30 seconds,
   but Artisan's fatigue lock lasts another 30. He can spend a Rage while the
   lock blocks it. (Static finding, from [25b](25b-ashatiel-martial-divine-ai.md).)
4. **Prepared but never used:**
   - Marius: Bless, Armor of Faith, Detect Evil ×6.
   - Zoe: Set Snare ×2.
   - Balvin: Gust of Wind.
   - Zoe's Hide-150 ambush branch can't fire, and her Defense-potion branch can't
     fire at AC 0.
5. **Limited dispels.** No one has Dispel or Remove Magic. The only protection
   removal is Ashatiel's Breach and Secret Word and Sarginson's Spell Thrust.
6. **Stoneskin.** Kimble and Sarginson have none. Ashatiel has one, and it goes in
   her opening.
7. **Three members can be critically hit:** Ashatiel (her helmet-slot item),
   Kimble and Sarginson (no helmet). The other four are crit-immune.
8. **Wormgums is the only evil member.** This matters for player Protection from
   Evil and for item 1.
9. **SCS random potions.** Most of them are undroppable `DW#PTN` copies that no
   script in these stacks uses. The only exceptions:
   - Zoe's `DW#RND25` potions are real and her AI drinks three of the four types.
   - Sarginson's possible Invisibility potions are real but never drunk.
10. **Sarginson's melee weapon doesn't match his proficiency.** He has Short Sword
    ★★ but carries a Long Sword +1, so his melee is non-proficient.
11. **Small Shield +2 gives no AC against missiles** under this install's shield
    rules. Ashatiel's missile AC comes from her Sword-and-Shield style instead.
12. **Kimble's Fireball** only goes where none of her allies is within 22 of the
    target. In a tight melee it rarely has a legal target.
13. **Poisoned supplies:** escorts lose 2 THAC0 permanently. Ashatiel doesn't,
    because she has no `BDDSC`.

## Not verified yet (needs an in-game check)

- Attacks per round for the bow, sling, darts and thrown daggers once proficiency
  and level are added to the item's rate of fire, and whether proficiency damage
  (the † numbers) applies to them.
- Loot. Dead escorts are `DestroySelf()`ed in BD4000; whether their droppable
  items survive has not been checked.
- Which allies actually receive Haste, Defensive Harmony, Chant and Mass Cure,
  given the area sizes and where everyone stands.
- All computed AC/THAC0/damage figures against the character-record screen.
- Random-potion odds assume the engine skips the `*` padding cells in `RNDTRES`.
  SCS's use of `DW#BLANK` entries for "nothing" implies that it does.
