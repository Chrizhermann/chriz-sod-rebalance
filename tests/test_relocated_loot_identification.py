"""Production #170 grant lines and ID helper, without its unrelated fight scripts."""
import re
import struct
import subprocess
import unittest
from pathlib import Path

from test_bdscry_compat import WEIDU
from test_treasure_container_installer import TreasureGame, area, item

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "chriz-sod-remix/lib/comp170.tpa"


def creature(records):
    raw = bytearray(0x324)
    raw[:8] = b"CRE V1.0"
    for offset in (0x2A0, 0x2A8, 0x2B0, 0x2C4):
        struct.pack_into("<I", raw, offset, 0x2D4)
    struct.pack_into("<III", raw, 0x2B8, 0x2D4, len(raw), len(records))
    for slot in range(40):
        struct.pack_into("<H", raw, 0x2D4 + slot * 2, 0xFFFF)
    for index in range(len(records)):
        struct.pack_into("<H", raw, 0x2D4 + (21 + index) * 2, index)
    return bytes(raw) + b"".join(records)


def records(raw):
    offset, count = struct.unpack_from("<II", raw, 0x2BC)
    return [raw[offset + i*20:offset + (i+1)*20] for i in range(count)]


@unittest.skipUnless(WEIDU.is_file(), f"WeiDU unavailable: {WEIDU}")
class RelocatedLootIdentificationTests(unittest.TestCase):
    def test_actual_jailbreak_grants_preserve_source_id_and_all_other_grant_fields(self):
        game = TreasureGame(area([]))
        self.addCleanup(game.cleanup)
        source = SOURCE.read_text(encoding="utf-8")
        prefix = source[:source.index("// 0. Loud preconditions:")]
        control = item("CONTROL", expiration=42, charges=(8, 7, 6), flags=0x82)
        template = creature([control])
        (game.root / "recipient.cre").write_bytes(template)
        # Multiple copies, changed order, unrelated flags/charges, one intentional ID.
        donor = creature([item("STAF02", flags=0x82), item("CLCK01", flags=0x83),
                          item("UNRELATED", flags=1), item("STAF02", flags=2)])
        (game.root / "override/bdshkorl.cre").write_bytes(donor)
        (game.root / "override/bd0130.are").write_bytes(area([
            item("BDHELM10", flags=0x85), item("BDSW2H03", flags=0x82)]))
        grant_lines = [line.strip() for line in source.splitlines()
                       if "ADD_CRE_ITEM" in line]
        harness = "BACKUP ~test-backup~\nAUTHOR ~test~\nBEGIN ~loot grants~\n" + prefix
        expected = {}
        for index, line in enumerate(grant_lines):
            match = re.match(r"ADD_CRE_ITEM ~([^~]+)~\s+#(\d+)\s+#(\d+)\s+#(\d+)\s+(.+?)\s+~(?:inv|QITEM|ARMOR|CLOAK|GLOVES|WEAPON\d|HELMET)~", line)
            self.assertIsNotNone(match, line)
            name, a, b, c, flags = match.groups()
            # Isolate each authored grant so occupied equipment/quick slots do not
            # obscure which item the public line produced.
            harness += f'COPY ~recipient.cre~ ~override/grant{index:02}.cre~\n  {line}\n'
            if "%csr170_id_" in flags:
                flag_bits = int(name.upper() in ("CLCK01", "BDHELM10"))
            elif "UNDROPPABLE" in flags:
                flag_bits = 9
            elif "IDENTIFIED" in flags:
                flag_bits = 1
            else:
                flag_bits = 0
            expected[f"grant{index:02}.cre"] = item(name.upper(), charges=(int(a), int(b), int(c)), flags=flag_bits)
        (game.root / "loot-test.tp2").write_text(harness, encoding="utf-8")
        result = subprocess.run([str(WEIDU), "loot-test.tp2", "--force-install-list", "0",
                                 "--language", "0", "--use-lang", "en_us",
                                 "--no-exit-pause", "--noautoupdate"],
                                cwd=game.root, capture_output=True, text=True, timeout=60)
        self.assertEqual(0, result.returncode, game.transcript(result))
        tree = game.tree()
        for name, wanted in expected.items():
            with self.subTest(grant=name):
                self.assertEqual([control, wanted], records(tree[name]))
        self.assertEqual(donor, tree["bdshkorl.cre"])
        # Normal WeiDU uninstall restores the fixture; no live installation involved.
        result = subprocess.run([str(WEIDU), "loot-test.tp2", "--force-uninstall-list", "0",
                                 "--language", "0", "--use-lang", "en_us",
                                 "--no-exit-pause", "--noautoupdate"],
                                cwd=game.root, capture_output=True, text=True, timeout=60)
        self.assertEqual(0, result.returncode, game.transcript(result))
        self.assertFalse(any(name in game.tree() for name in expected))
        self.assertEqual(donor, game.tree()["bdshkorl.cre"])


if __name__ == "__main__":
    unittest.main()
