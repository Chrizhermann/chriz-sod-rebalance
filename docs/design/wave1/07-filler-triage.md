# Filler audit triage — discussion started 2026-09-08

Source: [issue 16 audit](../../research/22-filler-audit.md) and the user's follow-up
discussion. **Only explicit user choices below are DECIDED.** Suggestions remain
OPEN. The user approved the targeted implementation below on 2026-09-08.

## Discussion queue

| Point | Current basis | Proposed treatment / remaining question |
|---|---|---|
| 1. Mizhena's amulet | All three scripted displacer carriers were cut. The quest remains. | **DECIDED:** use BD5000's existing `Dead_fighter` container at (4295,1098), among the removed pack's positions. Her current dialogue already fits. Component 265 preserves the corpse's existing contents and retires the three old scripted item grants. |
| 2. Ymori | A quest actor was cut as a stray wight; its activation, death and item dependencies remain. | **DECIDED:** preserve his staged quest and belongings, with proportionate verification; the user considers this side quest low priority. Fresh 230 excludes him. Repair 235 restores the original all-hours schedule while requiring the CRE's native deactivated state. Quest `Activate()` still controls his appearance. Native activation remains untested; this is a source-supported staging repair. |
| 3. Banned creatures | The global creature bans are already decided. Shadow Aspect still summons Shadowed Souls, and BD5110 retains an Unsleeping Guardian. | **DECIDED:** remove those missed sources without replacements. Component 265 preserves the surrounding encounters and ghost quest. The omitted Guardian adds 3,200 party XP under the existing 80% rule at the existing chapter-11 reward. Repeatable Shadowed Soul summons have no fixed-count compensation. |
| 4. Prologue XP | The old rationale counts retained caves and combines difficulty-exclusive actors. The [recount](../../research/23-prologue-xp-recount.md) separates difficulty and route. | **DECIDED (user, 2026-09-08): flat 22,000 XP per character on every difficulty**, paid once by Liia after the jailbreak. The user explicitly rejects difficulty-scaled quest rewards. Fresh 175 uses 22,000; append 176 to update an older 24,000 installation. Road-north 23,100 and coalition 106,800 remain party-total awards. |
| 5. Assassin ambush / dead magic | URE2, BD0063, remains in the current source and effective dev copy. No shipped remix component removes it. | **DECIDED default direction (user, 2026-09-08): keep the ambush, remove only its dead-magic treatment.** Exact alternative installer choices remain OPEN. |

After these, the broader density questions remain: ambient repopulation; treatment
of the other travel arenas; Neera's spider cave; temple/Ziatar; Bloodbark and the
river/druid/drow/ghost/Kanaglym pockets. The bridge and Ashatiel retain their separate
design discussions in issues 14/15.

## Assassin ambush: user decision and scope

The user wants keeping the scripted assassin fight **without the dead-magic
effect** to be the default option. The prior lean toward cutting all scripted
travel ambushes must not override this encounter-specific direction.

- **DECIDED:** default treatment keeps URE2's fight and removes its dead magic.
- **DECIDED consistency work (explicitly approved):** suppress the area descriptions and companion
  remarks specifically claiming magic does not work. Preserve ordinary ambush
  warnings, the encounter setup, enemies, equipment, escape/outro and rest unlock.
- **OPEN:** whether the installer also exposes full URE2 removal, an explicit
  unchanged-original flavor, or simply leaves original behavior available by
  not selecting this component. No alternative has been chosen for the user.
- **Implementation:** component 135 is selected by default by WeiDU and only
  patches BD0063.BCS. Explicit component selections can omit it to retain the
  original encounter. No full-removal alternative is being added without design.

## Installation and save boundaries

These changes are unreleased on the issue-16 branch. Append 135, 235 (after 230),
and 265 (after 260); do not reinstall the old components. Component 265 also
cleans Shadow Aspect's summons independently of optional 240. Fresh 230 already preserves
Ymori, and 235 tolerates that corrected schedule and reward.

ARE resources are cached in saves: use a save from before entering BD2000,
BD5000 and BD5110 for the area changes. The installer does not edit saves or
retroactively create quest items in an already visited area. Changed script
awards apply to future payouts only. Road-north compensation becomes 23,100
party XP (28,850 cut XP × 80%, rounded to 100); coalition compensation becomes
106,800 party XP (103,600 + 3,200). Existing once-only quest/chapter gates remain.

For an older component 175, append **176** to change Liia's future reward from
24,000 to 22,000 per character. Fresh 175 already pays the approved amount; 176
leaves it unchanged. No difficulty checks or retroactive XP deductions are added.

## What the current code does

Read-only verification on 2026-09-08 found the same effective resource hashes as
the audit snapshot. BD0063 has five scheduled actors. Current URE2 launchers remain
in BD7300, BD7400, BD3000 and BD5000, for example BD7300.BCS line 136:

```baf
ForceRandomEncounterEntry("BD0063","ExitW")
```

The dead-magic mechanism is a separate block in **BD0063.BCS**, decompiled lines 171–177:

```baf
IF
  !GlobalTimerNotExpired("AntimagicTimer","MYAREA")
THEN
  RESPONSE #100
    ApplySpell(Player1,DEAD_MAGIC_AREA)
    SetGlobalTimer("AntimagicTimer","MYAREA",ONE_ROUND)
END
```

The block runs when its local timer is absent or expired, applies the spell, and
waits one round before it becomes eligible again. Current `GTIMES.IDS` defines
ONE_ROUND as 6 seconds. `SPELL.IDS` maps DEAD_MAGIC_AREA to 3646, i.e. **SPIN646.SPL**.
Although the script names Player1, the installed spell's effects target
**Everyone**, so Player1 is not the sole affected character.

The current spell includes an unconditional dispel and 100% casting failure for
wizard spells, priest spells and innate abilities, lasting 14 seconds. Refreshing
that every 6 seconds maintains the restriction and repeatedly strips buffs. The
other effects supply the presentation. This is installed-resource evidence;
native gameplay acceptance remains part of the eventual implementation.

**The narrow patch is to remove this one application block from BD0063.BCS.**
Do not empty the encounter, remove its parent launchers, or change the shared
SPIN646 spell globally. The current ARE's flags are 0x30: its dead-magic bit 0x4 is
already clear, and it has no trigger regions. An ARE-flag-only change would not
stop this scripted spell refresh.

Text cleanup has a similarly narrow scope in BD0063.BCS: two area descriptions,
eight vanilla caster-remark blocks, and one installed Aura remark explicitly
describe missing magic. Minsc/Corwin's ordinary ambush warnings remain appropriate.
Compatibility work should match the existing blocks and tolerate the absence of
the optional Aura addition; it must not replace the whole installed area script.

### Code locations and primary references

The audit's readable decompiles are local ignored evidence:

- `research/data/issue16-audit/census-v3/baf/BD7300.baf`: URE2 entry block 125–139.
- `research/data/issue16-audit/census-v3/baf/BD0063.baf`: antimagic block 171–177;
  dead-magic descriptions/remarks above it; rest-unlock block 179–189.
- `research/data/issue16-audit/census-v3/baf/BDURE2A.baf`: assassin intro, HP/mercenary-
  death-dependent outro, and escape. These are separate from the area antimagic.

Format checks use the primary
[ARE flags specification](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/are_v1.htm),
[SPL effect targets](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/spl_v1.htm),
[casting failure opcode](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm#op60),
and [dispel opcode](https://gibberlings3.github.io/iesdp/opcodes/bgee.htm#op58).
The exact spell payload describes this heavily modded dev copy, not every install.
