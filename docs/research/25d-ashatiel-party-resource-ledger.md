# Ashatiel party: complete current resource ledger

Read-only capture, 2026-09-26. These are the effective Combined-install creatures,
including installed spell/item changes. This is the existing roster, not a new
approved loadout. Native/scripted prebuffs are analysed in the companion AI reports.

**Reading the numbers:** HP and header stats are stored values before runtime
equipment, ability, difficulty and buff calculations. Natural/stored AC and THAC0
are not a claim of final combat AC/THAC0. Spell counts are prepared copies; the
AI may not have a usable branch for every prepared spell. Item instance flags
describe drop eligibility, not guaranteed loot after scripted corpse cleanup.

The seven original members have **527 stored HP total** and **19,000 total kill XP**.
There are no balance changes in this capture.

| Character | Race / class levels | HP | Header THAC0 | Saves: death / wand / polymorph / breath / spell |
|---|---|---:|---:|---|
| Ashatiel | ELF / FIGHTER_MAGE_CLERIC 9/10/9 | 67 | 12 | 7 / 9 / 9 / 9 / 10 |
| Wormgums | GNOLL / FIGHTER 10 | 93 | 11 | 8 / 10 / 9 / 9 / 11 |
| Small Kimble | GNOME / MAGE 11 | 41 | 17 | 11 / 3 / 9 / 11 / 4 |
| Marius of Tethyr | HUMAN / PALADIN 10 | 93 | 11 | 6 / 8 / 7 / 7 / 9 |
| Zoe Kryn | HALFLING / FIGHTER_THIEF 8/10 | 70 | 13 | 6 / 6 / 10 / 12 / 7 |
| Sarginson | HUMAN / FIGHTER_MAGE 7/10 | 82 | 14 | 10 / 9 / 11 / 12 / 10 |
| Balvin Steadyhand | DWARF / FIGHTER_CLERIC 9/9 | 81 | 12 | 2 / 5 / 4 / 4 / 6 |

## Ashatiel (`BDASHATI`)

- Attributes: STR 17, STR_percent 0, DEX 18, CON 16, INT 16, WIS 16, CHA 15.
- Stored natural/effective AC: 10/10; APR encoding 1; kill XP 5000.
- Base resistances: all eleven fields zero.
- Base thief skills: Hide 0, Move silently 0, Detect illusions 0, Set traps 0, Open locks 0, Find traps 0, Pick pockets 0.
- Morale / break: 20 / 0. Stored kit bytes: `00000040`.
- Proficiency effects: PROFICIENCYMACE 2 (mode 0); PROFICIENCYDAGGER 2 (mode 0); PROFICIENCYSWORDANDSHIELD 2 (mode 0).
- Script slots: Override `BDASHATI`, Class `empty`, Race `BDSHOUT`, General `BDFMCL01`, Default `empty`.

### Equipment and complete inventory

| Item | Slot(s) | Stored quantity/charges 1,2,3 | Droppable instance | Identified instance |
|---|---|---|---|---|
| <strref 4294967295> (`BDERINYE`) | Helmet | 0, 0, 0 | Yes | No |
| Adventurer's Robe (`CLCK14`) | Armor | 0, 0, 0 | Yes | No |
| Small Shield +2 (`SHLD28A`) | Shield/offhand | 0, 0, 0 | Yes | No |
| Bracers of Defense AC 5 (`BDBRAC14`) | Gloves | 0, 0, 0 | Yes | No |
| Ring of Free Action (`BDRING09`) | Right ring | 0, 0, 0 | Yes | No |
| <strref 4294967295> (`MINHP1`) | Amulet | 0, 0, 0 | Yes | No |
| Golden Girdle (`BDBELT12`) | Belt | 0, 0, 0 | Yes | No |
| Throwing Dagger (`DAGG05`) | Weapon 1 | 20, 0, 0 | No | No |
| Mace +2 (`BLUN21`) | Weapon 2 | 0, 0, 0 | Yes | No |
| Cloak of Protection +1 (`CLCK01`) | Cloak | 0, 0, 0 | Yes | No |
| Potion of Extra Healing (`POTN52`) | Quick item 1 | 2, 0, 0 | Yes | No |
| Potion of Magic Shielding (`POTN35`) | Quick item 2 | 1, 0, 0 | Yes | No |
| Wand of Frost (`WAND06`) | Quick item 3 | 5, 0, 0 | Yes | No |
| Mirror (`DW#HASPT`) | Backpack 1 | 0, 0, 0 | Yes | No |
| <strref 9999999> (`DW#RND26`) | Backpack 2 | 0, 0, 0 | Yes | No |

Charges are raw instance fields, not three independent stacks. A value of 999
on ammunition is a large existing supply, not a proposed reward. For a
multi-ability item each charged ability must be matched to its field.
Item abilities and equip effects are retained in the scratch JSON.

### Prepared spells and abilities

- **Priest level 1**: Resist Fear (`SPPR108`) ×2; Sanctuary (`SPPR109`) ×2; Armor of Faith (`SPPR111`) ×1; Command (`SPPR102`) ×1.
- **Priest level 2**: Silence (`SPPR211`) ×2; Draw upon Divine Might (`SPPR214`) ×1; Aid (`SPPR201`) ×1; Chant (`SPPR203`) ×1; Slow Poison (`SPPR212`) ×1.
- **Priest level 3**: Invisibility Purge (`SPPR309`) ×1; Holy Smite (`SPPR313`) ×2.
- **Priest level 4**: Cure Critical Wounds (`SPPR401`) ×2.
- **Priest level 5**: Greater Command (`SPPR512`) ×1.
- **Wizard level 1**: Obscuring Mist (`SPWI106`) ×2; Magic Missile (`SPWI112`) ×2.
- **Wizard level 2**: Detect Invisibility (`SPWI203`) ×1; Mirror Image (`SPWI212`) ×2; Vocalize (`SPWI219`) ×1.
- **Wizard level 3**: Flame Arrow (`SPWI303`) ×2; Slow (`SPWI312`) ×1.
- **Wizard level 4**: Minor Globe of Invulnerability (`SPWI406`) ×1; Stoneskin (`SPWI408`) ×1; Secret Word (`SPWI419`) ×1.
- **Wizard level 5**: Breach (`SPWI513`) ×1; Spell Deflection (`SPWI522`) ×1.

Known entries with **no prepared copy**: none.

### Baked CRE effects

These rows expose existing proficiency/state/infrastructure records; they
are not a proposed prebuff list. Effects granted by equipped items are separate.

| Opcode | Parameter 1 | Parameter 2 | Timing | Duration | Resource | Parent |
|---:|---:|---:|---:|---:|---|---|
| 326 | 19 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 1 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 6 | 105 | 1 | 0 | `C0PR#MF1` | `` |
| 326 | 0 | 0 | 9 | 0 | `C0PR#CL` | `` |
| 293 | 0 | 1 | 9 | 0 | `` | `` |
| 233 | 2 | 101 | 9 | 0 | `` | `` |
| 233 | 2 | 96 | 9 | 0 | `` | `` |
| 233 | 2 | 112 | 9 | 0 | `` | `` |
| 176 | 3 | 0 | 9 | 0 | `` | `` |

## Wormgums (`BDASHA01`)

- Attributes: STR 18, STR_percent 95, DEX 17, CON 17, INT 10, WIS 10, CHA 10.
- Stored natural/effective AC: 5/5; APR encoding 1; kill XP 2000.
- Base resistances: all eleven fields zero.
- Base thief skills: Hide 0, Move silently 0, Detect illusions 0, Set traps 0, Open locks 0, Find traps 0, Pick pockets 0.
- Morale / break: 10 / 0. Stored kit bytes: `00400000`.
- Proficiency effects: PROFICIENCYHALBERD 2 (mode 0); PROFICIENCY2HANDED 2 (mode 0).
- Script slots: Override `BDDSC`, Class `BDCRUSDS`, Race `BDSHOUT`, General `BDFIGH01`, Default `empty`.

### Equipment and complete inventory

| Item | Slot(s) | Stored quantity/charges 1,2,3 | Droppable instance | Identified instance |
|---|---|---|---|---|
| Undroppable helmet with no animation (`HELMNOAN`) | Helmet | 0, 0, 0 | No | No |
| Halberd +2 (`HALB07`) | Weapon 1 | 0, 0, 0 | No | No |
| <strref 4294967295> (`UNICAEL2`) | Cloak | 0, 0, 0 | Yes | No |
| Potion of Extra Healing (`POTN52`) | Quick item 1 | 2, 0, 0 | Yes | No |
| Potion of Invulnerability (`POTN11`) | Quick item 2 | 1, 0, 0 | Yes | No |

Charges are raw instance fields, not three independent stacks. A value of 999
on ammunition is a large existing supply, not a proposed reward. For a
multi-ability item each charged ability must be matched to its field.
Item abilities and equip effects are retained in the scratch JSON.

### Prepared spells and abilities

- **Innate level 1**: Barbarian Rage (`SPCL152`) ×3.

Known entries with **no prepared copy**: none.

### Baked CRE effects

These rows expose existing proficiency/state/infrastructure records; they
are not a proposed prebuff list. Effects granted by equipped items are separate.

| Opcode | Parameter 1 | Parameter 2 | Timing | Duration | Resource | Parent |
|---:|---:|---:|---:|---:|---|---|
| 326 | 19 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 1 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 6 | 105 | 1 | 0 | `C0PR#MF1` | `` |
| 326 | 0 | 0 | 9 | 0 | `C0PR#CL` | `` |
| 233 | 2 | 99 | 9 | 0 | `` | `` |
| 233 | 2 | 111 | 9 | 0 | `` | `` |
| 176 | 2 | 0 | 9 | 0 | `` | `` |
| 293 | 0 | 1 | 1 | 0 | `` | `` |

## Small Kimble (`BDASHA02`)

- Attributes: STR 10, STR_percent 0, DEX 10, CON 15, INT 18, WIS 16, CHA 10.
- Stored natural/effective AC: 10/10; APR encoding 1; kill XP 3000.
- Base resistances: all eleven fields zero.
- Base thief skills: Hide 0, Move silently 0, Detect illusions 0, Set traps 0, Open locks 0, Find traps 0, Pick pockets 0.
- Morale / break: 10 / 0. Stored kit bytes: `00000004`.
- Proficiency effects: PROFICIENCYDAGGER 1 (mode 0); PROFICIENCYDART 1 (mode 0).
- Script slots: Override `BDDSC`, Class `BDCRUSDS`, Race `BDSHOUT`, General `BDMAGE01`, Default `empty`.

### Equipment and complete inventory

| Item | Slot(s) | Stored quantity/charges 1,2,3 | Droppable instance | Identified instance |
|---|---|---|---|---|
| Wand of Paralyzation (`WAND04`) | Quick item 2 | 4, 0, 0 | No | No |
| Potion of Extra Healing (`POTN52`) | Quick item 1 | 1, 0, 0 | Yes | No |
| <strref 4294967295> (`UNICAEL2`) | Cloak | 0, 0, 0 | Yes | No |
| Dart of Stunning (`DART03`) | Weapon 2 | 20, 0, 0 | Yes | No |
| Dagger (`DAGG01`) | Weapon 1 | 0, 0, 0 | No | No |
| Mirror (`DW#HASPT`) | Backpack 1 | 0, 0, 0 | Yes | No |

Charges are raw instance fields, not three independent stacks. A value of 999
on ammunition is a large existing supply, not a proposed reward. For a
multi-ability item each charged ability must be matched to its field.
Item abilities and equip effects are retained in the scratch JSON.

### Prepared spells and abilities

- **Wizard level 1**: Magic Missile (`SPWI112`) ×4; Shield (`SPWI114`) ×1.
- **Wizard level 2**: Blur (`SPWI201`) ×1; Detect Invisibility (`SPWI203`) ×1; Mirror Image (`SPWI212`) ×2; Vocalize (`SPWI219`) ×1.
- **Wizard level 3**: Flame Arrow (`SPWI303`) ×1; Haste (`SPWI305`) ×2; Protection from Missiles (`SPWI311`) ×1; Fireball (`SPWI304`) ×1.
- **Wizard level 4**: Confusion (`SPWI401`) ×1; Greater Malison (`SPWI412`) ×1; Improved Invisibility (`SPWI405`) ×1; Minor Globe of Invulnerability (`SPWI406`) ×1.
- **Wizard level 5**: Shadow Door (`SPWI505`) ×1; Waves of Fatigue (`SPWI508`) ×1; Spell Deflection (`SPWI522`) ×1; Hold Monster (`SPWI507`) ×1.

Known entries with **no prepared copy**: none.

### Baked CRE effects

These rows expose existing proficiency/state/infrastructure records; they
are not a proposed prebuff list. Effects granted by equipped items are separate.

| Opcode | Parameter 1 | Parameter 2 | Timing | Duration | Resource | Parent |
|---:|---:|---:|---:|---:|---|---|
| 326 | 19 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 1 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 6 | 105 | 1 | 0 | `C0PR#MF1` | `` |
| 326 | 19 | 105 | 1 | 0 | `C0PR#MO1` | `` |
| 326 | 1 | 105 | 1 | 0 | `C0PR#MO1` | `` |
| 326 | 19 | 105 | 1 | 0 | `C0PR#EK1` | `` |
| 326 | 1 | 105 | 1 | 0 | `C0PR#EK1` | `` |
| 326 | 0 | 0 | 9 | 0 | `C0PR#CL` | `` |
| 233 | 1 | 96 | 9 | 0 | `` | `` |
| 233 | 1 | 106 | 9 | 0 | `` | `` |
| 293 | 0 | 1 | 9 | 0 | `` | `` |

## Marius of Tethyr (`BDASHA03`)

- Attributes: STR 18, STR_percent 51, DEX 17, CON 15, INT 10, WIS 14, CHA 17.
- Stored natural/effective AC: 10/10; APR encoding 1; kill XP 2000.
- Base resistances: all eleven fields zero.
- Base thief skills: Hide 0, Move silently 0, Detect illusions 0, Set traps 0, Open locks 0, Find traps 0, Pick pockets 0.
- Morale / break: 10 / 0. Stored kit bytes: `00000440`.
- Proficiency effects: PROFICIENCYLONGSWORD 2 (mode 0); PROFICIENCYSWORDANDSHIELD 2 (mode 0).
- Script slots: Override `BDDSC`, Class `BDCRUSDS`, Race `BDSHOUT`, General `BDPAL01`, Default `empty`.

### Equipment and complete inventory

| Item | Slot(s) | Stored quantity/charges 1,2,3 | Droppable instance | Identified instance |
|---|---|---|---|---|
| Helmet (`HELM01`) | Helmet | 0, 0, 0 | No | No |
| Plate Mail +1 (`PLAT10`) | Armor | 0, 0, 0 | No | No |
| Large Shield +1 (`SHLD06A`) | Shield/offhand | 0, 0, 0 | Yes | No |
| Long Sword +1 (`SW1H05`) | Weapon 1 | 0, 0, 0 | No | No |
| <strref 4294967295> (`UNICAEL2`) | Cloak | 0, 0, 0 | Yes | No |
| Potion of Extra Healing (`POTN52`) | Quick item 1 | 2, 0, 0 | Yes | No |
| Potion of Stone Giant Strength (`POTN12`) | Quick item 2 | 1, 0, 0 | Yes | No |
| Mirror (`DW#HASPT`) | Backpack 1 | 0, 0, 0 | Yes | No |
| <strref 9999999> (`DW#RND12`) | Backpack 2 | 0, 0, 0 | Yes | No |
| <strref 9999999> (`DW#RND28`) | Backpack 3 | 0, 0, 0 | Yes | No |

Charges are raw instance fields, not three independent stacks. A value of 999
on ammunition is a large existing supply, not a proposed reward. For a
multi-ability item each charged ability must be matched to its field.
Item abilities and equip effects are retained in the scratch JSON.

### Prepared spells and abilities

- **Priest level 1**: Bless (`SPPR101`) ×1; Armor of Faith (`SPPR111`) ×1.
- **Innate level 1**: Lay On Hands (`SPCL211`) ×1; Detect Evil (`SPCL212`) ×6; Protection From Evil (`SPCL213`) ×6; Remove Fear (`SPCL222`) ×6.

Known entries with **no prepared copy**: none.

### Baked CRE effects

These rows expose existing proficiency/state/infrastructure records; they
are not a proposed prebuff list. Effects granted by equipped items are separate.

| Opcode | Parameter 1 | Parameter 2 | Timing | Duration | Resource | Parent |
|---:|---:|---:|---:|---:|---|---|
| 326 | 6 | 105 | 1 | 0 | `C0PR#GA1` | `` |
| 326 | 19 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 1 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 6 | 105 | 1 | 0 | `C0PR#MF1` | `` |
| 326 | 0 | 0 | 9 | 0 | `C0PR#CL` | `` |
| 233 | 2 | 90 | 9 | 0 | `` | `` |
| 233 | 2 | 112 | 9 | 0 | `` | `` |
| 293 | 0 | 1 | 9 | 0 | `` | `` |
| 267 | 14017 | 0 | 9 | 0 | `` | `` |
| 267 | 14662 | 0 | 9 | 0 | `` | `` |
| 267 | 8364 | 0 | 9 | 0 | `` | `` |
| 267 | 14672 | 0 | 9 | 0 | `` | `` |
| 267 | 14007 | 0 | 9 | 0 | `` | `` |
| 267 | 20568 | 0 | 9 | 0 | `` | `` |
| 267 | 17427 | 0 | 9 | 0 | `` | `` |
| 267 | 17392 | 0 | 9 | 0 | `` | `` |
| 267 | 14780 | 0 | 9 | 0 | `` | `` |
| 296 | 0 | 0 | 9 | 0 | `CDHORROR` | `` |
| 296 | 0 | 0 | 9 | 0 | `SPNWCHRM` | `` |
| 101 | 0 | 5 | 9 | 0 | `` | `` |
| 101 | 0 | 24 | 9 | 0 | `` | `` |
| 101 | 0 | 23 | 9 | 0 | `` | `` |
| 101 | 0 | 106 | 9 | 0 | `` | `` |
| 101 | 0 | 24 | 9 | 0 | `` | `` |
| 27 | 20 | 1 | 9 | 0 | `` | `` |
| 30 | 20 | 1 | 9 | 0 | `` | `` |
| 173 | 100 | 0 | 9 | 0 | `` | `` |
| 106 | 0 | 1 | 9 | 0 | `` | `` |

## Zoe Kryn (`BDASHA04`)

- Attributes: STR 17, STR_percent 0, DEX 19, CON 16, INT 10, WIS 10, CHA 10.
- Stored natural/effective AC: 10/10; APR encoding 1; kill XP 2000.
- Base resistances: all eleven fields zero.
- Base thief skills: Hide 0, Move silently 0, Detect illusions 0, Set traps 0, Open locks 0, Find traps 0, Pick pockets 0.
- Morale / break: 10 / 0. Stored kit bytes: `00000000`.
- Proficiency effects: PROFICIENCYSHORTSWORD 2 (mode 0); PROFICIENCYSINGLEWEAPON 2 (mode 0).
- Script slots: Override `BDDSC`, Class `BDCRUSDS`, Race `BDSHOUT`, General `BDFTHI01`, Default `empty`.

### Equipment and complete inventory

| Item | Slot(s) | Stored quantity/charges 1,2,3 | Droppable instance | Identified instance |
|---|---|---|---|---|
| Helmet (`HELM01`) | Helmet | 0, 0, 0 | No | No |
| Studded Leather Armor +1 (`LEAT05`) | Armor | 0, 0, 0 | No | No |
| Short Sword +1 (`SW1H08`) | Weapon 1 | 0, 0, 0 | Yes | No |
| <strref 4294967295> (`UNICAEL2`) | Cloak | 0, 0, 0 | Yes | No |
| Potion of Extra Healing (`POTN52`) | Quick item 1 | 1, 0, 0 | Yes | No |
| Potion of Invisibility (`POTN10`) | Quick item 2 | 4, 0, 0 | Yes | No |
| Mirror (`DW#HASPT`) | Backpack 1 | 0, 0, 0 | Yes | No |
| <strref 9999999> (`DW#RND12`) | Backpack 2 | 0, 0, 0 | Yes | No |
| <strref 9999999> (`DW#RND25`) | Backpack 3 | 0, 0, 0 | Yes | No |

Charges are raw instance fields, not three independent stacks. A value of 999
on ammunition is a large existing supply, not a proposed reward. For a
multi-ability item each charged ability must be matched to its field.
Item abilities and equip effects are retained in the scratch JSON.

### Prepared spells and abilities

- **Innate level 1**: Set Snare (`SPCL412`) ×2.

Known entries with **no prepared copy**: none.

### Baked CRE effects

These rows expose existing proficiency/state/infrastructure records; they
are not a proposed prebuff list. Effects granted by equipped items are separate.

| Opcode | Parameter 1 | Parameter 2 | Timing | Duration | Resource | Parent |
|---:|---:|---:|---:|---:|---|---|
| 326 | 19 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 1 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 6 | 105 | 1 | 0 | `C0PR#MF1` | `` |
| 326 | 0 | 0 | 9 | 0 | `C0PR#CL` | `` |
| 233 | 2 | 91 | 9 | 0 | `` | `` |
| 233 | 2 | 113 | 9 | 0 | `` | `` |
| 293 | 0 | 1 | 9 | 0 | `` | `` |

## Sarginson (`BDASHA05`)

- Attributes: STR 18, STR_percent 15, DEX 17, CON 10, INT 17, WIS 10, CHA 10.
- Stored natural/effective AC: 10/10; APR encoding 1; kill XP 3000.
- Base resistances: all eleven fields zero.
- Base thief skills: Hide 0, Move silently 0, Detect illusions 0, Set traps 0, Open locks 0, Find traps 0, Pick pockets 0.
- Morale / break: 10 / 0. Stored kit bytes: `00000000`.
- Proficiency effects: PROFICIENCYLONGBOW 4 (mode 0); PROFICIENCYSHORTSWORD 2 (mode 0).
- Script slots: Override `BDDSC`, Class `BDCRUSDS`, Race `BDSHOUT`, General `BDFMAG01`, Default `empty`.

### Equipment and complete inventory

| Item | Slot(s) | Stored quantity/charges 1,2,3 | Droppable instance | Identified instance |
|---|---|---|---|---|
| Wand of Frost (`WAND06`) | Quick item 2 | 4, 0, 0 | No | No |
| Potion of Extra Healing (`POTN52`) | Quick item 1 | 1, 0, 0 | Yes | No |
| <strref 4294967295> (`UNICAEL2`) | Cloak | 0, 0, 0 | Yes | No |
| Arrow of Fire +2 (`AROW08`) | Quiver 1 | 40, 0, 0 | Yes | No |
| Long Sword +1 (`SW1H05`) | Weapon 2 | 0, 0, 0 | No | No |
| Composite Longbow +1 (`BOW02`) | Weapon 1 | 0, 0, 0 | Yes | No |
| Mirror (`DW#HASPT`) | Backpack 1 | 0, 0, 0 | Yes | No |
| <strref 9999999> (`DW#RND26`) | Backpack 2 | 0, 0, 0 | Yes | No |
| <strref 9999999> (`DW#RND37`) | Backpack 3 | 0, 0, 0 | Yes | No |

Charges are raw instance fields, not three independent stacks. A value of 999
on ammunition is a large existing supply, not a proposed reward. For a
multi-ability item each charged ability must be matched to its field.
Item abilities and equip effects are retained in the scratch JSON.

### Prepared spells and abilities

- **Wizard level 1**: Shield (`SPWI114`) ×1; Magic Missile (`SPWI112`) ×2; Obscuring Mist (`SPWI106`) ×1.
- **Wizard level 2**: Horror (`SPWI205`) ×1; Mirror Image (`SPWI212`) ×2; Melf's Acid Arrow (`SPWI211`) ×1.
- **Wizard level 3**: Haste (`SPWI305`) ×1; Minor Spell Deflection (`SPWI318`) ×1; Spell Thrust (`SPWI321`) ×1.
- **Wizard level 4**: Improved Invisibility (`SPWI405`) ×1; Emotion, Hopelessness (`SPWI411`) ×1.
- **Wizard level 5**: Protection from Normal Weapons (`SPWI511`) ×1; Feeblemind (`SPWI509`) ×1.

Known entries with **no prepared copy**: none.

### Baked CRE effects

These rows expose existing proficiency/state/infrastructure records; they
are not a proposed prebuff list. Effects granted by equipped items are separate.

| Opcode | Parameter 1 | Parameter 2 | Timing | Duration | Resource | Parent |
|---:|---:|---:|---:|---:|---|---|
| 326 | 19 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 1 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 6 | 105 | 1 | 0 | `C0PR#MF1` | `` |
| 326 | 0 | 0 | 9 | 0 | `C0PR#CL` | `` |
| 233 | 4 | 104 | 9 | 0 | `` | `` |
| 233 | 2 | 91 | 9 | 0 | `` | `` |
| 0 | 0 | 0 | 1 | 0 | `` | `` |
| 293 | 0 | 1 | 9 | 0 | `` | `` |

## Balvin Steadyhand (`BDASHA06`)

- Attributes: STR 18, STR_percent 15, DEX 10, CON 19, INT 10, WIS 18, CHA 10.
- Stored natural/effective AC: 10/10; APR encoding 1; kill XP 2000.
- Base resistances: all eleven fields zero.
- Base thief skills: Hide 0, Move silently 0, Detect illusions 0, Set traps 0, Open locks 0, Find traps 0, Pick pockets 0.
- Morale / break: 10 / 0. Stored kit bytes: `00000000`.
- Proficiency effects: PROFICIENCYWARHAMMER 2 (mode 0); PROFICIENCYSWORDANDSHIELD 2 (mode 0); PROFICIENCYSLING 2 (mode 0).
- Script slots: Override `BDDSC`, Class `BDCRUSDS`, Race `BDSHOUT`, General `BDFCLE01`, Default `empty`.

### Equipment and complete inventory

| Item | Slot(s) | Stored quantity/charges 1,2,3 | Droppable instance | Identified instance |
|---|---|---|---|---|
| Helmet (`HELM01`) | Helmet | 0, 0, 0 | No | No |
| Plate Mail (`PLAT01`) | Armor | 0, 0, 0 | Yes | No |
| Medium Shield +1 (`SHLD04A`) | Shield/offhand | 0, 0, 0 | No | No |
| War Hammer +1 (`HAMM02`) | Weapon 1 | 0, 0, 0 | No | No |
| Sling +1 (`SLNG02`) | Weapon 2 | 0, 0, 0 | Yes | No |
| Bullet +2 (`BULL03`) | Quiver 1 | 40, 0, 0 | Yes | No |
| <strref 4294967295> (`UNICAEL2`) | Cloak | 0, 0, 0 | Yes | No |
| Potion of Extra Healing (`POTN52`) | Quick item 1 | 1, 0, 0 | Yes | No |
| Potion of Clarity (`POTN21`) | Quick item 2 | 1, 0, 0 | Yes | No |
| Wand of the Heavens (`WAND11`) | Quick item 3 | 2, 0, 0 | No | No |
| Mirror (`DW#HASPT`) | Backpack 1 | 0, 0, 0 | Yes | No |
| <strref 9999999> (`DW#RND26`) | Backpack 2 | 0, 0, 0 | Yes | No |

Charges are raw instance fields, not three independent stacks. A value of 999
on ammunition is a large existing supply, not a proposed reward. For a
multi-ability item each charged ability must be matched to its field.
Item abilities and equip effects are retained in the scratch JSON.

### Prepared spells and abilities

- **Priest level 1**: Sanctuary (`SPPR109`) ×1; Armor of Faith (`SPPR111`) ×1; Command (`SPPR102`) ×2; Doom (`SPPR113`) ×1; Cure Light Wounds (`SPPR103`) ×1.
- **Priest level 2**: Chant (`SPPR203`) ×1; Hold Person (`SPPR208`) ×2; Draw upon Divine Might (`SPPR214`) ×1; Silence (`SPPR211`) ×1; Slow Poison (`SPPR212`) ×1.
- **Priest level 3**: Remove Paralysis (`SPPR308`) ×1; Miscast Magic (`SPPR310`) ×1; Gust of Wind (`SPPR318`) ×1; Invisibility Purge (`SPPR309`) ×1.
- **Priest level 4**: Free Action (`SPPR403`) ×1; Defensive Harmony (`SPPR406`) ×1; Cure Critical Wounds (`SPPR401`) ×1.
- **Priest level 5**: Mass Cure (`SPPR514`) ×1.

Known entries with **no prepared copy**: none.

### Baked CRE effects

These rows expose existing proficiency/state/infrastructure records; they
are not a proposed prebuff list. Effects granted by equipped items are separate.

| Opcode | Parameter 1 | Parameter 2 | Timing | Duration | Resource | Parent |
|---:|---:|---:|---:|---:|---|---|
| 326 | 19 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 1 | 105 | 1 | 0 | `C0PR#AT1` | `` |
| 326 | 6 | 105 | 1 | 0 | `C0PR#MF1` | `` |
| 326 | 0 | 0 | 9 | 0 | `C0PR#CL` | `` |
| 233 | 2 | 97 | 9 | 0 | `` | `` |
| 233 | 2 | 112 | 9 | 0 | `` | `` |
| 233 | 2 | 107 | 9 | 0 | `` | `` |
| 293 | 0 | 1 | 9 | 0 | `` | `` |

## Equipped effects and kit interpretation

These are effective installed resources, not extra proposed prebuffs.

| Resource | Verified meaning relevant to this audit |
|---|---|
| `UNICAEL2` on the six escorts | Nineteen color-setting effects, no abilities. It supplies their uniform colors, not combat protection. |
| `BDERINYE` on Ashatiel | No equipped effects and no abilities. Do not count this presentation/story item as an extra defensive spell. |
| `BDBRAC14` | Base AC-setting effect at AC 5; final AC also depends on equipment, attributes and buffs. |
| `BDBELT12` | Three-point AC bonus versus slashing. |
| `CLCK01` | One-point AC and all-five-saves bonuses. |
| `BDRING09` | Permanent Free Action and related movement/hold protections, including several installed compatibility markers; not immunity to all control or magic. |
| `MINHP1` | Story item with minimum-HP protection and numerous death/control immunities. Existing `BDASHATI` introductory dialogue state 1 destroys it before the duel/refusal choices. It must not become part of the new combat loadout through bypassing that transition. |
| `DW#HASPT` / `DW#RND*` | SCS bookkeeping/random-allocation markers, not additional ready-to-drink potions. Their own ITM resources do not provide active abilities or equip buffs; initialization behavior is a separate matter. |

The Free Action ring includes immunity to opcode 16 (ordinary engine Haste),
but **the inspected SR Haste does not use that opcode**. It supplies movement
through opcode 176 and APR through opcode 1, which the ring does not block.
Its Haste icon can be hidden by the ring. Therefore do not infer loss of this
installed spell's movement/APR benefit from the item name or missing icon.
The [arcane audit](25a-ashatiel-arcane-ai.md#haste-support-kimble-and-sarginson)
records the spell's actual effects and the native AI's different state check.

The raw kit bytes above decode to **Barbarian for Wormgums, Illusionist for
Small Kimble, and Cavalier for Marius**. For a `KIT.IDS` lookup, swap the CRE
field's two 16-bit words; do not reverse all four individual bytes. Local SCS
`CRE_read_kit` calls `reverse_long` for this conversion. The
[reference audit follow-up](25c-scs-drasus-design-checklist.md)
records the source locations and the inspected kit identifiers. A kit identifier
is not proof that every mod-added passive has been initialized on that NPC.

Zoe's armor helper effects were also followed: the Invisible Blade-only helper
modifies backstab, the Eldritch Knight helper grants an exception to a casting
restriction, and the general helper disables wizard casting. None grants Hide
in Shadows or leads to a spell that does. Those effects do not establish that
her native ambush branch's Hide >=150 requirement is met. This does not affect
the separate, supported invisibility-potion behavior.

Sarginson's proficiency effects grant four longbow points and two **shortsword**
points; the carried backup is a **longsword**. This is a current equipment/build
mismatch, not an already-approved weapon change.

## Evidence and boundaries

Source: `%USERPROFILE%/CEBG-Tests/Combined-20260908/game`, read only.
Scratch: `%USERPROFILE%/CEBG-Tests/Ashatiel-20260926/party-facts/`.
`party-facts.json` contains full grouped known/prepared spells, readiness flags,
inventory, item abilities/equipping effects, script slots, attributes and baked
effects. `manifest.json` stores resource origins/hashes and the TLK hash.
Every memorized record was checked to belong to exactly one level/type group.
No source game, save, installer, creature or script was changed.

Binary decoding uses the IESDP [CRE](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/cre_v1.htm),
[ITM](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/itm_v1.htm), and
[EFF](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/eff_v2.htm)
references, cross-checked with the project CRE parsing conventions.
