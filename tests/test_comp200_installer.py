#!/usr/bin/env python3
"""Run production component 200 (Coast Way Crossing field pass) through real WeiDU.

A synthetic BD1000.ARE carries the eight west-group spiders, both spawn points
and both web traps beside foreign entries; a synthetic BDCUT14 carries the
force-wall sequence and the THREE_ROUNDS parley timer. Patched resources are
compared with independently built expectations. No game installation is used.
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

WEST = [("SPIDGI", 530, 1562), ("SPIDGI", 644, 1594), ("SPIDHU", 548, 1459),
        ("SPIDPH", 616, 1502), ("SPIDPH", 468, 1468), ("SPIDPH", 467, 1532),
        ("BDSPIDGA", 563, 1523), ("BDSPIDGA", 498, 1496)]
KEPT_ACTORS = [("SPIDGI", 4500, 3300), ("SPIDPH", 530, 1563), ("FOREIGN", 1, 2)]
SPAWNS = [("Spiders01", 3), ("Spiders02", 4), ("Foreign_spawn", 2)]
REGIONS = [("Trap_web01", 4443), ("Trap_web02", 347), ("Foreign_region", 10)]
WALL = '''    ActionOverride("bdcrus13",ForceSpellPointRES("bdwforce",[3780.1110]))
    SmallWait(30)
    CreateVisualEffect("SPFLESHS",[3540.1135])
    CreateVisualEffect("SPFLESHS",[3625.1195])
    SmallWait(10)
    AmbientActivate("force_wall",TRUE)
    CloseDoor("force_wall_door")
'''
BRIDGE = '''IF
  Global("FOREIGN_BRIDGE","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_BRIDGE","GLOBAL",1)
    Continue()
END

IF
  True()
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_BEFORE","GLOBAL",1)
''' + WALL + '''    SetGlobal("FOREIGN_MIDDLE","GLOBAL",1)
    SetGlobalTimer("bd_caelar_timer","bd1000",THREE_ROUNDS)
    SetGlobal("FOREIGN_AFTER","GLOBAL",1)
END
'''
EXPECTED_BRIDGE = (BRIDGE.replace(WALL, '    SmallWait(1)\n')
                   .replace('THREE_ROUNDS', 'FIVE_ROUNDS'))


def area() -> bytes:
    actors = WEST[:4] + KEPT_ACTORS + WEST[4:]
    actor_offset = 0x11c
    region_offset = actor_offset + len(actors) * 0x110
    spawn_offset = region_offset + len(REGIONS) * 0xc4
    data = bytearray(b"\x5a" * (spawn_offset + len(SPAWNS) * 0xc8))
    data[:0x11c] = b"\0" * 0x11c
    data[:8] = b"AREAV1.0"
    struct.pack_into("<IHHI", data, 0x54, actor_offset, len(actors), len(REGIONS), region_offset)
    struct.pack_into("<II", data, 0x60, spawn_offset, len(SPAWNS))
    for index, (cre, x, y) in enumerate(actors):
        base = actor_offset + index * 0x110
        data[base:base + 32] = f"Actor {index}".encode().ljust(32, b"\0")
        struct.pack_into("<hh", data, base + 0x20, x, y)
        struct.pack_into("<I", data, base + 0x40, 0x000FFFC0)
        data[base + 0x80:base + 0x88] = cre.encode().ljust(8, b"\0")
    for index, (name, x1) in enumerate(REGIONS):
        base = region_offset + index * 0xc4
        data[base:base + 32] = name.encode().ljust(32, b"\0")
        struct.pack_into("<H", data, base + 0x22, x1)
        struct.pack_into("<H", data, base + 0x6c, 1)
    for index, (name, count) in enumerate(SPAWNS):
        base = spawn_offset + index * 0xc8
        data[base:base + 32] = name.encode().ljust(32, b"\0")
        struct.pack_into("<H", data, base + 0x74, count)
    return bytes(data) + b"UNRELATED AREA PAYLOAD"


def expected_area(before: bytes) -> bytes:
    data = bytearray(before)
    actor_offset, actor_count, region_count, region_offset = struct.unpack_from("<IHHI", data, 0x54)
    spawn_offset, spawn_count = struct.unpack_from("<II", data, 0x60)
    for index in range(actor_count):
        base = actor_offset + index * 0x110
        cre = data[base + 0x80:base + 0x88].rstrip(b"\0").decode()
        x, y = struct.unpack_from("<hh", data, base + 0x20)
        if (cre, x, y) in WEST:
            struct.pack_into("<I", data, base + 0x40, 0)
    for index in range(spawn_count):
        base = spawn_offset + index * 0xc8
        if data[base:base + 32].rstrip(b"\0") == b"Spiders02":
            struct.pack_into("<H", data, base + 0x74, 0)
    for index in range(region_count):
        base = region_offset + index * 0xc4
        if data[base:base + 32].rstrip(b"\0") == b"Trap_web02":
            struct.pack_into("<H", data, base + 0x6c, 0)
    return bytes(data)


@unittest.skipUnless(WEIDU.is_file(), "real WeiDU unavailable; set WEIDU_EXE")
class Component200InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.make_game()

    def make_game(self, gtimes: str | None = None) -> None:
        """A fresh synthetic game; gtimes replaces its whole GTIMES.IDS."""
        temp = tempfile.TemporaryDirectory(prefix="csr200-installer-")
        self.addCleanup(temp.cleanup)
        self.game = Path(temp.name)
        write_fake_game(self.game)
        self.override = self.game / "override"
        extra_ids = {
            "action": '''1 ActionOverride(O:Actor*,A:Action*)
83 SmallWait(I:Time*)
114 ForceSpellPointRES(S:RES*,P:Target)
115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)
144 CloseDoor(O:Object*)
272 CreateVisualEffect(S:Object*,P:Location*)
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
        for library in ("comp200.tpa", "gtimes_compat.tpa"):
            shutil.copy2(ROOT / "chriz-sod-remix/lib" / library,
                         self.game / "chriz-sod-remix/lib" / library)
        (self.game / "fixture").mkdir()
        (self.game / "fixture/setup-fixture.tp2").write_text('''BACKUP ~fixture/backup~
AUTHOR ~fixture~
BEGIN ~compile synthetic bridge cutscene~ DESIGNATED 0
COMPILE ~fixture/bdcut14.baf~
COMPILE ~fixture/expected.baf~
''', encoding="ascii")
        (self.game / "patch.tp2").write_text('''BACKUP ~patch-backup~
AUTHOR ~fixture~
ALWAYS
  INCLUDE ~chriz-sod-remix/lib/gtimes_compat.tpa~
END
BEGIN ~production component 200 harness~ DESIGNATED 200
INCLUDE ~chriz-sod-remix/lib/comp200.tpa~
''', encoding="ascii")
        (self.override / "bd1000.are").write_bytes(area())
        (self.override / "cutskip.bcs").write_bytes(b"protected skip rig")

    def run_weidu(self, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(WEIDU), *arguments, "--game", str(self.game),
                               "--language", "0", "--use-lang", "en_US", "--no-exit-pause"],
                              cwd=self.game, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=45)

    def fixture(self, bridge: str = BRIDGE) -> None:
        (self.game / "fixture/bdcut14.baf").write_text(bridge, encoding="ascii")
        (self.game / "fixture/expected.baf").write_text(EXPECTED_BRIDGE, encoding="ascii")
        result = self.run_weidu("fixture/setup-fixture.tp2", "--force-install-list", "0")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)

    def install(self) -> subprocess.CompletedProcess:
        return self.run_weidu("patch.tp2", "--force-install-list", "200")

    def assert_patched(self) -> bytes:
        before = tree(self.override)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)
        after = tree(self.override)
        self.assertEqual({name for name in before if before[name] != after[name]},
                         {"BD1000.ARE", "BDCUT14.BCS"})
        self.assertEqual((self.override / "bd1000.are").read_bytes(), expected_area(area()))
        patched = (self.override / "bdcut14.bcs").read_bytes()
        self.assertEqual(patched, (self.override / "expected.bcs").read_bytes())
        self.assertIn(b'30 0 0 0 0"bd1000bd_caelar_timer" "" AC', patched)
        return patched

    def test_field_pass_and_bridge_window(self):
        self.fixture()
        self.assert_patched()

    def test_parley_timer_contract_follows_the_gtimes_name_for_eighteen_seconds(self):
        patched = set()
        for label, (gtimes, _) in gtimes_variants(18).items():
            with self.subTest(gtimes=label):
                self.make_game(gtimes)
                self.fixture()
                patched.add(self.assert_patched())
        self.assertEqual(len(patched), 1)

    def test_changed_bridge_cutscene_is_rejected_and_rolled_back(self):
        for label, bridge in (("other timer", BRIDGE.replace("THREE_ROUNDS", "FIVE_ROUNDS")),
                              ("other wall", BRIDGE.replace("SmallWait(10)", "SmallWait(11)"))):
            with self.subTest(change=label):
                self.make_game(gtimes_variants(18)["name from another mod"][0])
                self.fixture(bridge)
                before = tree(self.override)
                result = self.install()
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("BDCUT14.bcs does not match the verified bridge-fight layout",
                              result.stdout + result.stderr)
                self.assertEqual(tree(self.override), before)


if __name__ == "__main__":
    unittest.main()
