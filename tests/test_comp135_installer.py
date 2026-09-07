#!/usr/bin/env python3
"""Run production component 135 through real WeiDU in disposable synthetic games.

Only the KEY/BIF/TLK bootstrap is shared with the ending installer tests. These
fixtures compile independently written encounter blocks and compare the compiled
result with a separately compiled keeper script. No game installation is written.
"""

from __future__ import annotations

from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/scripts"))
from test_comp291_installer import WEIDU, tree, write_fake_game


def block(triggers: str, actions: str) -> str:
    return f"IF\n{triggers}\nTHEN\n  RESPONSE #100\n{actions}\nEND\n"


ANTIMAGIC = block(
    '  !GlobalTimerNotExpired("AntimagicTimer","MYAREA")',
    '    ApplySpell(Player1,DEAD_MAGIC_AREA)\n'
    '    SetGlobalTimer("AntimagicTimer","MYAREA",ONE_ROUND)')


def dead_magic_blocks(*, aura: bool = False, string_base: int = 0) -> list[str]:
    result = [ANTIMAGIC]
    for trigger in (
        '  OR(2)\n    Class(Player1,MAGE_ALL)\n    Kit(Player1,WIZARDSLAYER)',
        '  !Class(Player1,MAGE_ALL)\n  !Kit(Player1,WIZARDSLAYER)',
    ):
        result.append(block(
            '  Global("BD_String","MYAREA",0)\n' + trigger,
            f'    SetGlobal("BD_String","MYAREA",1)\n'
            f'    DisplayString(Myself,{string_base + len(result)})'))
    for roll, npc in enumerate(("Edwin", "Baeloth", "Dynaheir", "Neera"), 1):
        for random in (f"  RandomNum(4,{roll})\n", ""):
            result.append(block(
                f'  Global("BD_NPC01","MYAREA",0)\n'
                f'  IsValidForPartyDialogue("{npc}")\n{random}  Delay(3)',
                f'    SetGlobal("BD_NPC01","MYAREA",1)\n'
                f'    DisplayStringHead("{npc}",{string_base + len(result)})'))
    if aura:
        result.append(block(
            '  Global("BD_NPC01","MYAREA",0)\n'
            '  IsValidForPartyDialogue("C0Aura")\n  RandomNum(4,2)\n  Delay(3)',
            f'    SetGlobal("BD_NPC01","MYAREA",1)\n'
            f'    DisplayStringHead("C0Aura",{string_base + 12})'))
    return result


INIT = block('  Global("BD_Init","MYAREA",0)', '''    SetInterrupt(FALSE)
    SetGlobal("BD_Init","MYAREA",1)
    SetGlobal("BD_FRE","GLOBAL",0)
    SetGlobalTimer("BD_TIMER_URE","GLOBAL",1)
    SetGlobal("BD_URE2","GLOBAL",2)
    DayNight(MIDNIGHT)
    Weather(NOWEATHER)
    FadeFromColor([15.0],0)
    DisplayString(Myself,20)
    SetInterrupt(TRUE)''')
REST = block('''  Global("BD_CanRest","MYAREA",0)
  !AreaCheckAllegiance(ENEMY)
  CombatCounter(0)''', '''    SetInterrupt(FALSE)
    SetGlobal("BD_CanRest","MYAREA",1)
    RemoveAreaFlag(NOREST)
    SetInterrupt(TRUE)''')
WARNINGS = []
for random in (True, False):
    for roll, npc in enumerate(("Minsc", "Corwin"), 1):
        WARNINGS.append(block(
            f'  Global("BD_NPC02","MYAREA",0)\n'
            f'  IsValidForPartyDialogue("{npc}")'
            + (f'\n  RandomNum(2,{roll})' if random else ''),
            f'    SetGlobal("BD_NPC02","MYAREA",1)\n'
            f'    DisplayStringHead("{npc}",{20 + roll})'))
FOREIGN = [block(f'  Global("FOREIGN_{n}","MYAREA",0)',
                 f'    SetGlobal("FOREIGN_{n}","MYAREA",1)\n    Continue()')
           for n in ("BEFORE", "MIDDLE", "AFTER")]
KEEPERS = [FOREIGN[0], INIT, WARNINGS[0], WARNINGS[1], FOREIGN[1],
           WARNINGS[2], WARNINGS[3], REST, FOREIGN[2]]


@unittest.skipUnless(WEIDU.is_file(), "real WeiDU unavailable; set WEIDU_EXE")
class Component135InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="csr135-installer-")
        self.addCleanup(self.temp.cleanup)
        self.game = Path(self.temp.name)
        write_fake_game(self.game)
        self.override = self.game / "override"
        extra_ids = {
            "action": '''66 DayNight(I:TimeOfDay*TIME)
67 Weather(I:Weather*WEATHER)
86 SetInterrupt(I:State*BOOLEAN)
115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTIMES)
151 DisplayString(O:Object*,I:StrRef*)
160 ApplySpell(O:Target*,I:Spell*SPELL)
269 DisplayStringHead(O:Object*,I:StrRef*)
333 RemoveAreaFlag(I:Type*AREAFLAG)
''',
            "trigger": '''0x400C Class(O:Object*,I:Class*CLASS)
0x4027 Delay(I:Delay*)
0x4041 GlobalTimerNotExpired(S:Name*,S:Area*)
0x4043 IsValidForPartyDialogue(O:Object*)
0x4047 RandomNum(I:Range*,I:Value*)
0x4083 CombatCounter(I:Number*)
0x40BB Kit(O:Object*,I:Kit*KIT)
0x40DC AreaCheckAllegiance(I:Allegiance*EA)
''',
            "class": "202 MAGE_ALL\n", "ea": "255 ENEMY\n",
            "kit": "16384 WIZARDSLAYER\n", "time": "0 MIDNIGHT\n",
            "weather": "0 NOWEATHER\n", "areaflag": "32 NOREST\n",
            "gtimes": "6 ONE_ROUND\n", "spell": "3646 DEAD_MAGIC_AREA\n",
        }
        for name, definitions in extra_ids.items():
            path = self.override / f"{name}.ids"
            previous = path.read_text(encoding="ascii") if path.exists() else "IDS V1.0\n"
            path.write_text(previous + definitions, encoding="ascii")
        # Real TLK comments include punctuation resembling regex/code. The patch
        # must bind the action structure, not English text or EET strref offsets.
        text = b"Fixture text: (magic) [sound] <CHARNAME>, 100%!"
        count = 300
        records = b"".join(struct.pack("<H8siiII", 1, b"\0" * 8, 0, 0,
                                       index * len(text), len(text)) for index in range(count))
        tlk = struct.pack("<8sHII", b"TLK V1  ", 0, count, 18 + count * 26) + records + text * count
        for path in (self.game / "dialog.tlk", self.game / "lang/en_us/dialog.tlk"):
            path.write_bytes(tlk)
        (self.game / "chriz-sod-remix/lib").mkdir(parents=True)
        shutil.copy2(ROOT / "chriz-sod-remix/lib/comp135.tpa",
                     self.game / "chriz-sod-remix/lib/comp135.tpa")
        (self.game / "fixture").mkdir()
        (self.game / "fixture/setup-fixture.tp2").write_text('''BACKUP ~fixture/backup~
AUTHOR ~fixture~
BEGIN ~compile synthetic assassin fixture~ DESIGNATED 0
COMPILE ~fixture/bd0063.baf~
COMPILE ~fixture/expected.baf~
''', encoding="ascii")
        (self.game / "patch.tp2").write_text('''BACKUP ~patch-backup~
AUTHOR ~fixture~
BEGIN ~production component 135 harness~ DESIGNATED 135
INCLUDE ~chriz-sod-remix/lib/comp135.tpa~
''', encoding="ascii")
        for name in ("spin646.spl", "bd0063.are", "bdure2a.bcs", "bdure2a.cre",
                     "bd7300.bcs", "bd7400.bcs", "bd3000.bcs", "bd5000.bcs"):
            (self.override / name).write_bytes(f"protected encounter resource {name}".encode("ascii"))

    def run_weidu(self, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(WEIDU), *arguments, "--game", str(self.game),
                               "--language", "0", "--use-lang", "en_US", "--no-exit-pause"],
                              cwd=self.game, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=45)

    def fixture(self, targets: list[str] | None = None, keepers: list[str] | None = None,
                lowercase: bool = False) -> None:
        targets = dead_magic_blocks() if targets is None else targets
        keepers = KEEPERS if keepers is None else keepers
        # Mix foreign/preserved blocks among removal targets to catch range
        # deletions and retained-block reordering, not merely final marker counts.
        source = []
        for index in range(max(len(keepers), len(targets))):
            if index < len(keepers):
                source.append(keepers[index])
            if index < len(targets):
                source.append(targets[index])
        original = "\n".join(source)
        expected = "\n".join(keepers)
        if lowercase:
            original, expected = original.lower(), expected.lower()
        (self.game / "fixture/bd0063.baf").write_text(original, encoding="ascii")
        (self.game / "fixture/expected.baf").write_text(expected, encoding="ascii")
        result = self.run_weidu("fixture/setup-fixture.tp2", "--force-install-list", "0")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)

    def snapshot(self) -> dict:
        return {"override": tree(self.override), "immutable": {
            name: (self.game / name).read_bytes() for name in
            ("chitin.key", "data/csr291.bif", "dialog.tlk", "lang/en_us/dialog.tlk")}}

    def assert_preserved(self, before: dict, changed: bool) -> None:
        after = tree(self.override)
        self.assertEqual(after.keys(), before["override"].keys())
        for name, digest in before["override"].items():
            if changed and name == "BD0063.BCS":
                continue
            self.assertEqual(after[name], digest, name)
        for name, data in before["immutable"].items():
            self.assertEqual((self.game / name).read_bytes(), data, name)

    def install(self, name: str = "patch.tp2") -> subprocess.CompletedProcess:
        return self.run_weidu(name, "--force-install-list", "135")

    def assert_success(self, before: dict, *, changed: bool = True) -> None:
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)
        self.assert_preserved(before, changed)
        self.assertEqual((self.override / "bd0063.bcs").read_bytes(),
                         (self.override / "expected.bcs").read_bytes())

    def assert_rejected(self, before: dict) -> None:
        result = self.install()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NOT INSTALLED DUE TO ERRORS", result.stdout)
        self.assertIn("#135", result.stdout + result.stderr)
        self.assert_preserved(before, False)
        self.assertFalse(any(path.suffix.upper() == ".BCS"
                             for path in (self.game / "patch-backup/135").rglob("*")),
                         "preflight failure must precede resource backups")

    def test_vanilla_without_aura_preserves_compiled_keeper_script_exactly(self):
        self.fixture()
        self.assert_success(self.snapshot())

    def test_public_component_135_preserves_compiled_keeper_script_exactly(self):
        self.fixture(dead_magic_blocks(aura=True, string_base=200))
        shutil.copytree(ROOT / "chriz-sod-remix", self.game / "chriz-sod-remix", dirs_exist_ok=True)
        before = self.snapshot()
        result = self.install("chriz-sod-remix/setup-chriz-sod-remix.tp2")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)
        self.assert_preserved(before, True)
        self.assertEqual((self.override / "bd0063.bcs").read_bytes(),
                         (self.override / "expected.bcs").read_bytes())

    def test_eet_shaped_strings_and_optional_aura_preserve_foreign_blocks(self):
        self.fixture(dead_magic_blocks(aura=True, string_base=200))
        self.assert_success(self.snapshot())

    def test_case_insensitive_names_are_supported(self):
        self.fixture(dead_magic_blocks(aura=True), lowercase=True)
        self.assert_success(self.snapshot())

    def test_already_clean_is_byte_exact_noop(self):
        self.fixture([])
        self.assert_success(self.snapshot(), changed=False)

    def test_second_transform_is_byte_exact_noop_not_weidu_installed_skip(self):
        self.fixture(dead_magic_blocks(aura=True))
        self.assert_success(self.snapshot())
        before = self.snapshot()
        # New harness identity actually executes INCLUDE again, without uninstall.
        shutil.copy2(self.game / "patch.tp2", self.game / "second.tp2")
        result = self.install("second.tp2")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("already has no dead-magic", result.stdout)
        self.assert_preserved(before, False)

    def test_missing_original_remark_rejects_partial_change_before_write(self):
        self.fixture(dead_magic_blocks()[:-1])
        self.assert_rejected(self.snapshot())

    def test_duplicate_antimagic_block_is_rejected_before_write(self):
        self.fixture(dead_magic_blocks() + [ANTIMAGIC])
        self.assert_rejected(self.snapshot())

    def test_extra_action_inside_target_is_rejected_before_write(self):
        targets = dead_magic_blocks()
        targets[0] = targets[0].replace("    ApplySpell", "    Continue()\n    ApplySpell")
        self.fixture(targets)
        self.assert_rejected(self.snapshot())

    def test_changed_optional_aura_block_is_rejected_before_write(self):
        targets = dead_magic_blocks(aura=True)
        targets[-1] = targets[-1].replace("Delay(3)", "Delay(4)")
        self.fixture(targets)
        self.assert_rejected(self.snapshot())

    def test_missing_preserved_warning_rejects_before_write(self):
        self.fixture(keepers=[value for value in KEEPERS if value != WARNINGS[0]])
        self.assert_rejected(self.snapshot())


if __name__ == "__main__":
    unittest.main()
