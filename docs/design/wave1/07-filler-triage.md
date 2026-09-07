# Filler audit triage — discussion started 2026-09-08

Source: [issue 16 audit](../../research/22-filler-audit.md) and the user's follow-up
discussion. **Only explicit user choices below are DECIDED.** Suggestions remain
OPEN; this document does not implement encounter or XP changes.

## Discussion queue

| Point | Current basis | Proposed treatment / remaining question |
|---|---|---|
| 1. Mizhena's amulet | All three scripted displacer carriers were cut. The quest remains. | **OPEN placement:** use BD5000's existing `Dead_fighter` container at (4295,1098), among the removed pack's positions. Her current dialogue says she dropped the amulet during a battle at the eastern edge of the forest. This would preserve exploration and the quest without restoring the pack. User choice pending. |
| 2. Ymori | A quest actor was cut as a stray wight; its activation, death and item dependencies remain. | **Recommendation:** preserve the original staged quest encounter and belongings. First test the `Activate()` path against the schedule-zero actor; repair suppression if confirmed. This need not restore unrelated bridge filler. No new quest-removal decision. |
| 3. Banned creatures | The global creature bans are already decided. Shadow Aspect still summons Shadowed Souls, and BD5110 retains an Unsleeping Guardian. | **Implementation recommendation:** remove those missed sources, keep the surrounding encounters/ghost quest, and account for the Guardian's omitted XP. A replacement monster would be a separate creative choice; none is assumed. |
| 4. Prologue XP | The old rationale counts 53,115 party XP from two still-reachable side caves. The 24,000-per-character Liia award was explicitly approved. | **OPEN:** recount actually skipped content and the replacement jailbreak, then agree a corrected future award. Do not subtract an arbitrary rounded amount or alter the approved reward during this discussion. |
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
- **Implied consistency work:** suppress the area descriptions and companion
  remarks specifically claiming magic does not work. Preserve ordinary ambush
  warnings, the encounter setup, enemies, equipment, escape/outro and rest unlock.
- **OPEN:** whether the installer also exposes full URE2 removal, an explicit
  unchanged-original flavor, or simply leaves original behavior available by
  not selecting this component. No alternative has been chosen for the user.
- **Not yet implemented:** no TP2, BAF, ARE, SPL or installed resource changed.

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
