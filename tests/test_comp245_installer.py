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
  CutSceneBroken()
  Switch("BD_CUTSCENE_BREAKABLE","GLOBAL")
THEN
  RESPONSE #14
    ActionOverride("bdwilhm",JumpToPoint([4360.690]))
    ActionOverride("bdcrus15",JumpToPoint([4345.735]))
    ActionOverride("bdwilhm",DestroyItem("minhp1"))
    SmallWait(5)
    ApplyDamagePercent("bdwilhm",150,FIRE)
    ApplyDamagePercent("bdcrus15",150,FIRE)
    OpenDoor("Bridge01")
    TriggerActivation("info_bridge",TRUE)
    AmbientActivate("Bridge_Damage_Day",FALSE)
    AmbientActivate("Bridge_Damage_Night",FALSE)
    Weather(FOG)
    ActionOverride("bdcrus10",JumpToPoint([3945.1040]))
    ActionOverride("bdcrus11",JumpToPoint([4025.955]))
    ActionOverride("bdcrus12",JumpToPoint([3995.905]))
    ActionOverride("bdcrus13",JumpToPoint([4090.915]))
    ActionOverride("bdcrus14",JumpToPoint([4135.965]))
    ActionOverride("bdivann",JumpToPoint([3965.975]))
    ActionOverride(Player1,JumpToPoint([3785.1095]))
    ActionOverride(Player2,JumpToPoint([3655.1135]))
    ActionOverride(Player3,JumpToPoint([3880.1185]))
    ActionOverride(Player4,JumpToPoint([3750.1170]))
    ActionOverride(Player5,JumpToPoint([3665.970]))
    ActionOverride(Player6,JumpToPoint([3745.1020]))
    ActionOverride("bdjayvis",DestroySelf())
    ActionOverride("JAYVIS_GUARD1",DestroySelf())
    ActionOverride("JAYVIS_GUARD2",DestroySelf())
    ActionOverride("cutspy",DestroySelf())
    ActionOverride("cutspy2",DestroySelf())
    ActionOverride("barrel1",DestroySelf())
    ActionOverride("barrel2",DestroySelf())
    ActionOverride("barrel3",DestroySelf())
    ActionOverride("barrel4",DestroySelf())
    ChangeEnemyAlly("bdivann",NEUTRAL)
    ChangeEnemyAlly("bdcrus10",NEUTRAL)
    ChangeEnemyAlly("bdcrus11",NEUTRAL)
    ChangeEnemyAlly("bdcrus12",NEUTRAL)
    ChangeEnemyAlly("bdcrus13",NEUTRAL)
    ChangeEnemyAlly("bdcrus14",NEUTRAL)
    AmbientActivate("explosion",FALSE)
    MoveViewPoint([3780.1110],INSTANT)
    ActionOverride(Player6,SetSequence(SEQ_AWAKE))
    ActionOverride(Player3,SetSequence(SEQ_AWAKE))
    ActionOverride(Player1,SetSequence(SEQ_AWAKE))
    ActionOverride(Player6,Face(NEE))
    ActionOverride(Player3,Face(NNE))
    ActionOverride(Player5,SetSequence(SEQ_AWAKE))
    ActionOverride(Player1,Face(NE))
    ActionOverride(Player2,SetSequence(SEQ_AWAKE))
    ActionOverride(Player5,Face(E))
    ActionOverride(Player4,SetSequence(SEQ_AWAKE))
    ActionOverride(Player2,Face(NE))
    ActionOverride("bdcrus10",SetSequence(SEQ_AWAKE))
    ActionOverride(Player4,Face(NE))
    ActionOverride("bdcrus11",SetSequence(SEQ_AWAKE))
    ActionOverride("bdivann",SetSequence(SEQ_AWAKE))
    ActionOverride("bdcrus13",SetSequence(SEQ_AWAKE))
    ActionOverride("bdcrus14",SetSequence(SEQ_AWAKE))
    ActionOverride("bdcrus12",SetSequence(SEQ_AWAKE))
    ActionOverride("bdivann",FaceObject(Player1))
    ActionOverride("bdcrus10",FaceObject(Player1))
    ActionOverride("bdcrus13",FaceObject(Player1))
    ActionOverride("bdcrus11",FaceObject(Player1))
    ActionOverride("bdcrus14",FaceObject(Player1))
    ActionOverride("bdcrus12",FaceObject(Player1))
    AmbientActivate("force_wall",TRUE)
    CloseDoor("force_wall_door")
    ActionOverride("bdivann",DestroyItem("minhp1"))
    ActionOverride("bdcrus13",DestroyItem("minhp1"))
    ActionOverride("bdivann",Enemy())
    ActionOverride("bdcrus10",Enemy())
    ActionOverride("bdcrus11",Enemy())
    ActionOverride("bdcrus12",Enemy())
    ActionOverride("bdcrus13",Enemy())
    ActionOverride("bdcrus14",Enemy())
    SmallWait(10)
    SetGlobalTimer("bd_caelar_timer","bd1000",THREE_ROUNDS)
    FadeFromColor([10.0],0)
    EndCutSceneMode()
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
        (self.game / "WeiDU.log").write_text("")
        extra_ids = {'action': '1 ActionOverride(O:Actor*,A:Action*)\n10 Enemy()\n48 JumpToPoint(P:Target*)\n49 MoveViewPoint(P:Target*,I:ScrollSpeed*Scroll)\n67 Weather(I:Weather*Weather)\n83 SmallWait(I:Time*)\n84 Face(I:Direction*DIR)\n111 DestroySelf()\n115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)\n122 EndCutSceneMode()\n143 OpenDoor(O:Object*)\n144 CloseDoor(O:Object*)\n153 ChangeEnemyAlly(O:Object*,I:Value*EA)\n169 DestroyItem(S:ResRef*)\n177 TriggerActivation(O:Object*,I:State*Boolean)\n203 FadeFromColor(P:Point*,I:Blue*)\n229 FaceObject(O:Object*)\n301 AmbientActivate(O:Object*,I:State*BOOLEAN)\n306 ApplyDamagePercent(O:Object*,I:Amount*,I:Type*DMGTYPE)\n345 SetSequence(I:Sequence*SEQ)\n', 'trigger': '0x00EB CutSceneBroken()\n0x40E5 Switch(S:Global*,S:Area*)\n', 'scroll': '0 INSTANT\n', 'weather': '3 FOG\n', 'ea': '128 NEUTRAL\n', 'dir': '9 NNE\n10 NE\n11 NEE\n12 E\n', 'dmgtype': '0x00080000 FIRE\n', 'seq': '1 SEQ_AWAKE\n', 'gtimes': '18 THREE_ROUNDS\n30 FIVE_ROUNDS\n'}
        extra_ids["object"] = "21 Player1\n22 Player2\n23 Player3\n24 Player4\n25 Player5\n26 Player6\n"
        for name, definitions in extra_ids.items():
            path = self.override / f"{name}.ids"
            previous = path.read_text(encoding="ascii") if path.exists() else "IDS V1.0\n"
            path.write_text(previous + definitions, encoding="ascii")
        if gtimes is not None:
            (self.override / "gtimes.ids").write_bytes(gtimes.encode("ascii"))
        (self.game / "chriz-sod-remix/lib").mkdir(parents=True)
        for library in ("comp245.tpa", "gtimes_compat.tpa", "overwrite.tpa"):
            shutil.copy2(ROOT / "chriz-sod-remix/lib" / library,
                         self.game / "chriz-sod-remix/lib" / library)
        (self.game / "chriz-sod-remix/baf").mkdir()
        shutil.copy2(ROOT / "chriz-sod-remix/baf/csr245skip.baf", self.game / "chriz-sod-remix/baf/csr245skip.baf")
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

    def test_changed_and_duplicate_mirrors_get_the_owned_response(self):
        for mirror in (MIRROR.replace("THREE_ROUNDS", "999"),
                       MIRROR.replace('    CloseDoor("force_wall_door")\n', ''),
                       MIRROR.replace("[4360.690]", "[5.6]"),
                       MIRROR.replace('  RESPONSE #14', '  RESPONSE #100'),
                       MIRROR.replace('END\n', '  RESPONSE #14\n    Continue()\nEND\n')):
            with self.subTest(mirror=mirror):
                self.make_game()
                self.fixture(mirror)
                result = self.install()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn('WARNING', (result.stdout + result.stderr).upper())
                raw = (self.override / 'cutskip.bcs').read_bytes()
                self.assertEqual(raw.count(b'30 0 0 0 0"bd1000bd_caelar_timer"'), 1)

    def test_absent_script_and_response_get_the_complete_skip(self):
        self.fixture('')
        (self.override / 'cutskip.bcs').unlink()
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('WARNING', (result.stdout + result.stderr).upper())
        self.assertIn(b'30 0 0 0 0"bd1000bd_caelar_timer"', (self.override/'cutskip.bcs').read_bytes())

    def test_second_tail_install_is_byte_identical(self):
        self.fixture()
        self.assertEqual(self.install().returncode, 0)
        first = (self.override/'cutskip.bcs').read_bytes()
        (self.game/'second.tp2').write_text((self.game/'patch.tp2').read_text().replace('patch-backup', 'second-backup'))
        result = self.run_weidu('second.tp2', '--force-install-list', '245')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.override/'cutskip.bcs').read_bytes(), first)


if __name__ == "__main__":
    unittest.main()
