#!/usr/bin/env python3
"""Run production component 140 (skip the Korlasz dungeon) through real WeiDU.

Synthetic BDINTRO, BD0120 and BDSODTRN sources carry every seam the component
binds, beside foreign blocks; the patched scripts are compared with separately
compiled expectations. A standalone-numbered TLK supplies the three journal
strings. Only disposable synthetic games are written.
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
from test_gtimes_compat import gtimes_variants

JOURNAL = {56379: "I must find Korlasz.", 59573: "Korlasz has surrendered.",
           69028: "Korlasz is in custody; return to the Ducal Palace."}
FOREIGN = '''IF
  Global("FOREIGN_INTRO","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_INTRO","GLOBAL",1)
    Continue()
END

'''
STAGING_KEPT_HEAD = '''IF
  True()
THEN
  RESPONSE #100
    SetGlobal("chapter","global",7)
'''
STAGING_REMOVED = '''    ApplySpellRES("bdslow","intro_follower2")
    ActionOverride("intro_follower2",Polymorph(FIGHTER_FEMALE_HUMAN))
    SetGlobal("bd_plot","global",2)
'''
STAGING_STAGE = '''    JumpToPoint([905.1615])
    ActionOverride(Player2,JumpToPoint([728.1602]))
    ActionOverride(Player3,JumpToPoint([776.1602]))
    ActionOverride(Player4,JumpToPoint([776.1744]))
    ActionOverride(Player5,JumpToPoint([840.1746]))
    ActionOverride(Player6,JumpToPoint([824.1782]))
    ActionOverride(Player2,Face(E))
    ActionOverride(Player3,Face(E))
    ActionOverride(Player4,Face(NE))
    ActionOverride(Player5,Face(NE))
    ActionOverride(Player6,Face(NE))
    Face(NE)
    CreateCreature("bdshimoe",[881.1652],NE)
    SetGlobalTimer("BD_Ammon_stop","BD0120",TWO_MINUTES)
    SetAreaScript("cutskip",OVERRIDE)
    SetGlobal("BD_CUTSCENE_BREAKABLE","GLOBAL",1)
'''
STAGING = (STAGING_KEPT_HEAD + STAGING_REMOVED
           + '    SetGlobal("bd_npc_camp_chapter","global",0)\n'
           + STAGING_STAGE + '    SetCutSceneBreakable(TRUE)\nEND\n\n')
EXPECTED_STAGING = (STAGING_KEPT_HEAD
                    + '    SetGlobal("bd_npc_camp_chapter","global",1)\n'
                    + '''    SetGlobal("BD_KORLASZ_SURRENDER","GLOBAL",1)
    AddJournalEntry(56379,QUEST)
    AddJournalEntry(59573,QUEST_DONE)
    AddJournalEntry(69028,QUEST_DONE)
    SetGlobal("bd_plot","global",50)
    EndCutSceneMode()
END

''')


def walk_in(gate: str) -> str:
    """Both trigger-gated walk-in variants; gate is the line seam 2 adds."""
    return ''.join(f'''IF
{gate}  {trigger}
  Global("bd_walkin","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("bd_walkin","GLOBAL",{value})
END

''' for trigger, value in (('InMyArea("minsc")', 1), ('!InMyArea("minsc")', 2)))


INTRO = FOREIGN + STAGING + walk_in('')
EXPECTED_INTRO = FOREIGN + EXPECTED_STAGING + walk_in('  False()\n')
AREA_SCRIPT = '''IF
  Global("FOREIGN_0120","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_0120","GLOBAL",1)
END

'''
TRANSITION = '''IF
  True()
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_TRANSITION","GLOBAL",1)
    CopyGroundPilesTo("BD0120",[949.1686])
END
'''


def standalone_tlk() -> bytes:
    """Standalone BG:EE/SoD numbering: the journal strings at their native strrefs."""
    count = max(JOURNAL) + 1
    text = b"".join(value.encode("ascii") for value in JOURNAL.values())
    entries, offset = [], 0
    for strref in range(count):
        value = JOURNAL.get(strref, "").encode("ascii")
        entries.append(struct.pack("<H8siiII", 1 if value else 0, b"\0" * 8, 0, 0,
                                   offset if value else 0, len(value)))
        offset += len(value)
    return (struct.pack("<8sHII", b"TLK V1  ", 0, count, 18 + count * 26)
            + b"".join(entries) + text)


@unittest.skipUnless(WEIDU.is_file(), "real WeiDU unavailable; set WEIDU_EXE")
class Component140InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tlk = standalone_tlk()

    def setUp(self) -> None:
        self.make_game()

    def make_game(self, gtimes: str | None = None) -> None:
        """A fresh synthetic game; gtimes replaces its whole GTIMES.IDS."""
        temp = tempfile.TemporaryDirectory(prefix="csr140-installer-")
        self.addCleanup(temp.cleanup)
        self.game = Path(temp.name)
        write_fake_game(self.game)
        self.override = self.game / "override"
        extra_ids = {
            "action": '''1 ActionOverride(O:Actor*,A:Action*)
7 CreateCreature(S:NewObject*,P:Location*,I:Face*DIR)
48 JumpToPoint(P:Target*)
84 Face(I:Direction*DIR)
115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)
120 StartCutSceneEx(S:CutScene*,I:evaluateConditions*BOOLEAN)
146 Polymorph(I:AnimationType*Animate)
160 ApplySpellRES(S:RES*,O:Target)
173 AddJournalEntry(I:Entry*,I:Type*JourType)
264 CopyGroundPilesTo(S:ResRef*,P:Location*)
352 SetAreaScript(S:Script*,I:ScriptSlot*ASCRLEV)
387 SetCutSceneBreakable(I:Breakable*BOOLEAN)
''',
            "trigger": '''0x4030 False()
0x4035 GlobalLT(S:Name*,S:Area*,I:Value*)
0x40CB InMyArea(O:Object*)
''',
            "object": "22 Player2\n23 Player3\n24 Player4\n25 Player5\n26 Player6\n",
            "dir": "6 NW\n10 NE\n12 E\n", "animate": "0x6110 FIGHTER_FEMALE_HUMAN\n",
            "jourtype": "1 QUEST\n2 QUEST_DONE\n", "ascrlev": "4 OVERRIDE\n",
            "gtimes": "10 TWO_MINUTES\n",
        }
        for name, definitions in extra_ids.items():
            path = self.override / f"{name}.ids"
            previous = path.read_text(encoding="ascii") if path.exists() else "IDS V1.0\n"
            path.write_text(previous + definitions, encoding="ascii")
        if gtimes is not None:
            (self.override / "gtimes.ids").write_bytes(gtimes.encode("ascii"))
        for path in (self.game / "dialog.tlk", self.game / "lang/en_us/dialog.tlk"):
            path.write_bytes(self.tlk)
        mod = self.game / "chriz-sod-remix"
        (mod / "lib").mkdir(parents=True)
        (mod / "baf").mkdir()
        for library in ("comp140.tpa", "gtimes_compat.tpa"):
            shutil.copy2(ROOT / "chriz-sod-remix/lib" / library, mod / "lib" / library)
        for source in ("exit0120.baf", "blk0120.baf"):
            shutil.copy2(ROOT / "chriz-sod-remix/baf" / source, mod / "baf" / source)
        fixture = self.game / "fixture"
        fixture.mkdir()
        exit_source = (ROOT / "chriz-sod-remix/baf/exit0120.baf").read_text(encoding="utf-8")
        black_source = (ROOT / "chriz-sod-remix/baf/blk0120.baf").read_text(encoding="utf-8")
        sources = {
            "bd0120.baf": AREA_SCRIPT,
            "bdsodtrn.baf": TRANSITION,
            "exp0120.baf": black_source + "\n" + AREA_SCRIPT + exit_source,
            "exptrn.baf": TRANSITION.replace('CopyGroundPilesTo("BD0120",[949.1686])',
                                             'CopyGroundPilesTo("BD0103",[190.540])'),
            "expintro.baf": EXPECTED_INTRO,
        }
        for name, text in sources.items():
            # The production BAF comments are UTF-8, as in the mod itself.
            (fixture / name).write_text(text, encoding="utf-8")
        (fixture / "setup-fixture.tp2").write_text('BACKUP ~fixture/backup~\nAUTHOR ~fixture~\n'
            'BEGIN ~compile synthetic prologue scripts~ DESIGNATED 0\n'
            + "".join(f"COMPILE ~fixture/{name}~\n" for name in [*sources, "bdintro.baf"]),
            encoding="ascii")
        (self.game / "patch.tp2").write_text('''BACKUP ~patch-backup~
AUTHOR ~fixture~
ALWAYS
  INCLUDE ~chriz-sod-remix/lib/gtimes_compat.tpa~
END
BEGIN ~production component 140 harness~ DESIGNATED 140
INCLUDE ~chriz-sod-remix/lib/comp140.tpa~
''', encoding="ascii")

    def run_weidu(self, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(WEIDU), *arguments, "--game", str(self.game),
                               "--language", "0", "--use-lang", "en_US", "--no-exit-pause"],
                              cwd=self.game, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=60)

    def fixture(self, intro: str = INTRO) -> None:
        (self.game / "fixture/bdintro.baf").write_text(intro, encoding="ascii")
        result = self.run_weidu("fixture/setup-fixture.tp2", "--force-install-list", "0")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)

    def install(self) -> subprocess.CompletedProcess:
        return self.run_weidu("patch.tp2", "--force-install-list", "140")

    def assert_patched(self) -> tuple[bytes, ...]:
        before = tree(self.override)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)
        after = tree(self.override)
        self.assertEqual({name for name in before if before[name] != after[name]},
                         {"BDINTRO.BCS", "BD0120.BCS", "BDSODTRN.BCS"})
        patched = tuple((self.override / name).read_bytes()
                        for name in ("bdintro.bcs", "bd0120.bcs", "bdsodtrn.bcs"))
        expected = tuple((self.override / name).read_bytes()
                         for name in ("expintro.bcs", "exp0120.bcs", "exptrn.bcs"))
        for name, actual, wanted in zip(("BDINTRO", "BD0120", "BDSODTRN"), patched, expected):
            self.assertEqual(actual, wanted, name)
        self.assertNotIn(b"BD0120BD_Ammon_stop", patched[0])
        return patched

    def test_skip_seams_match_independently_compiled_scripts(self):
        self.fixture()
        self.assert_patched()

    def test_ammon_timer_contract_follows_the_gtimes_name_for_ten_seconds(self):
        patched = set()
        for label, (gtimes, _) in gtimes_variants(10).items():
            with self.subTest(gtimes=label):
                self.make_game(gtimes)
                self.fixture()
                patched.add(self.assert_patched())
        self.assertEqual(len(patched), 1)

    def test_changed_ammon_timer_is_rejected_without_writes(self):
        self.make_game(gtimes_variants(10)["name from another mod"][0])
        self.fixture(INTRO.replace('"BD0120",TWO_MINUTES)', '"BD0120",12)'))
        before = tree(self.override)
        result = self.install()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("chriz-sod-remix #140 [staging: Ammon timer]: expected exactly 1 match",
                      result.stdout + result.stderr)
        self.assertEqual(tree(self.override), before)


if __name__ == "__main__":
    unittest.main()
