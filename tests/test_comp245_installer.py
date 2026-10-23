#!/usr/bin/env python3
"""Run production component 245 (CUTSKIP's BDCUT14 mirror) through real WeiDU.

The cutscene-skip rig repeats comp200's two decisions: no force wall, and a
30-second parley timer instead of THREE_ROUNDS. Synthetic sources only; the
patched script is compared with an independently compiled expected script.
"""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/scripts"))
from test_comp291_installer import WEIDU, tree, write_fake_game
from test_gtimes_compat import gtimes_variants

FOREIGN = '''IF
  Global("FOREIGN_SKIP","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_SKIP","GLOBAL",1)
    Continue()
END
'''
MIRROR = '''IF
  Global("bd_cutskip_bdcut14","GLOBAL",1)
THEN
  RESPONSE #100
    SetGlobal("bd_cutskip_bdcut14","GLOBAL",0)
    AmbientActivate("force_wall",TRUE)
    CloseDoor("force_wall_door")
    SetGlobalTimer("bd_caelar_timer","bd1000",THREE_ROUNDS)
    DisplayStringNoName(Player1,7)
END
'''
RESTORE = '''IF
  Global("bd_cutskip_restore","GLOBAL",1)
THEN
  RESPONSE #100
    AmbientActivate("force_wall",FALSE)
    OpenDoor("force_wall_door")
END
'''
EXPECTED_MIRROR = (MIRROR.replace('    AmbientActivate("force_wall",TRUE)\n', '')
                   .replace('    CloseDoor("force_wall_door")\n', '')
                   .replace('THREE_ROUNDS', 'FIVE_ROUNDS'))


@unittest.skipUnless(WEIDU.is_file(), "real WeiDU unavailable; set WEIDU_EXE")
class Component245InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.make_game()

    def make_game(self, gtimes: str | None = None) -> None:
        """A fresh synthetic game; gtimes replaces its whole GTIMES.IDS."""
        temp = tempfile.TemporaryDirectory(prefix="csr245-installer-")
        self.addCleanup(temp.cleanup)
        self.game = Path(temp.name)
        write_fake_game(self.game)
        self.override = self.game / "override"
        extra_ids = {
            "action": '''115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)
143 OpenDoor(O:Object*)
144 CloseDoor(O:Object*)
301 AmbientActivate(O:Object*,I:State*BOOLEAN)
''',
            "gtimes": "18 THREE_ROUNDS\n30 FIVE_ROUNDS\n",
        }
        for name, definitions in extra_ids.items():
            path = self.override / f"{name}.ids"
            previous = path.read_text(encoding="ascii") if path.exists() else "IDS V1.0\n"
            path.write_text(previous + definitions, encoding="ascii")
        if gtimes is not None:
            (self.override / "gtimes.ids").write_bytes(gtimes.encode("ascii"))
        (self.game / "chriz-sod-remix/lib").mkdir(parents=True)
        for library in ("comp245.tpa", "gtimes_compat.tpa"):
            shutil.copy2(ROOT / "chriz-sod-remix/lib" / library,
                         self.game / "chriz-sod-remix/lib" / library)
        (self.game / "fixture").mkdir()
        (self.game / "fixture/setup-fixture.tp2").write_text('''BACKUP ~fixture/backup~
AUTHOR ~fixture~
BEGIN ~compile synthetic skip rig~ DESIGNATED 0
COMPILE ~fixture/cutskip.baf~
COMPILE ~fixture/expected.baf~
''', encoding="ascii")
        (self.game / "patch.tp2").write_text('''BACKUP ~patch-backup~
AUTHOR ~fixture~
ALWAYS
  INCLUDE ~chriz-sod-remix/lib/gtimes_compat.tpa~
END
BEGIN ~production component 245 harness~ DESIGNATED 245
INCLUDE ~chriz-sod-remix/lib/comp245.tpa~
''', encoding="ascii")
        (self.override / "bdcut14.bcs").write_bytes(b"protected bridge cutscene")

    def run_weidu(self, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(WEIDU), *arguments, "--game", str(self.game),
                               "--language", "0", "--use-lang", "en_US", "--no-exit-pause"],
                              cwd=self.game, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=45)

    def fixture(self, mirror: str = MIRROR) -> None:
        (self.game / "fixture/cutskip.baf").write_text(FOREIGN + mirror + RESTORE, encoding="ascii")
        (self.game / "fixture/expected.baf").write_text(FOREIGN + EXPECTED_MIRROR + RESTORE,
                                                        encoding="ascii")
        result = self.run_weidu("fixture/setup-fixture.tp2", "--force-install-list", "0")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)

    def install(self) -> subprocess.CompletedProcess:
        return self.run_weidu("patch.tp2", "--force-install-list", "245")

    def test_mirror_loses_the_wall_and_gets_the_thirty_second_window(self):
        self.fixture()
        before = tree(self.override)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)
        after = tree(self.override)
        self.assertEqual({name for name in before if before[name] != after[name]}, {"CUTSKIP.BCS"})
        patched = (self.override / "cutskip.bcs").read_bytes()
        self.assertEqual(patched, (self.override / "expected.bcs").read_bytes())
        self.assertIn(b'30 0 0 0 0"bd1000bd_caelar_timer" "" AC', patched)

    def test_parley_timer_contract_follows_the_gtimes_name_for_eighteen_seconds(self):
        patched = set()
        for label, (gtimes, _) in gtimes_variants(18).items():
            with self.subTest(gtimes=label):
                self.make_game(gtimes)
                self.fixture()
                result = self.install()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual((self.override / "cutskip.bcs").read_bytes(),
                                 (self.override / "expected.bcs").read_bytes())
                patched.add((self.override / "cutskip.bcs").read_bytes())
        self.assertEqual(len(patched), 1)

    def test_changed_mirror_is_rejected_without_writes(self):
        for label, mirror in (("other timer", MIRROR.replace("THREE_ROUNDS", "FIVE_ROUNDS")),
                              ("no wall", MIRROR.replace('    CloseDoor("force_wall_door")\n', ''))):
            with self.subTest(change=label):
                self.make_game(gtimes_variants(18)["name from another mod"][0])
                self.fixture(mirror)
                before = tree(self.override)
                result = self.install()
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("CUTSKIP.bcs does not match the verified BDCUT14 mirror",
                              result.stdout + result.stderr)
                self.assertEqual(tree(self.override), before)


if __name__ == "__main__":
    unittest.main()
