"""Public component 235 in disposable games: preserve Ymori and the XP once flag.

Fixtures carry foreign actor bytes and quest belongings. Success is compared
against exact expected ARE and separately compiled BCS bytes; failures must leave
all game resources unchanged. No native Activate()/quest completion is asserted.
"""

from pathlib import Path
import struct
import subprocess
import unittest

from test_bdscry_compat import WEIDU, SyntheticDialogGame, _dialog_source


TARGET = 0x11C + 0x110


def area(*, schedule=0, duplicate=False, missing=False, embedded_offset=0, embedded_size=0):
    rows = [("CONTROL1", 100, 200, 0x123456),
            ("BDYMORI" if not missing else "OTHER", 4089, 408, schedule),
            ("CONTROL2", 300, 400, 0xABCDEF)]
    if duplicate:
        rows.append(rows[1])
    data = bytearray(0x11C + len(rows) * 0x110)
    data[:8] = b"AREAV1.0"
    struct.pack_into("<IH", data, 0x54, 0x11C, len(rows))
    for index, (cre, x, y, appearance) in enumerate(rows):
        base = 0x11C + index * 0x110
        data[base:base + 0x110] = bytes([index + 17]) * 0x110
        struct.pack_into("<32sHH", data, base, f"actor {index}".encode(), x, y)
        struct.pack_into("<I", data, base + 0x40, appearance)
        struct.pack_into("<8sII", data, base + 0x80, cre.encode(),
                         embedded_offset if index == 1 else 0,
                         embedded_size if index == 1 else 0)
    return bytes(data) + b"Unrelated area sections and native Ymoribody metadata\x00\xff"


def creature(*, deactivated=True):
    data = bytearray(0x2D4)
    data[:8] = b"CRE V1.0"
    struct.pack_into("<I", data, 0x20, 0x80000 if deactivated else 0)
    struct.pack_into("<I", data, 0x14, 175)
    struct.pack_into("<32s", data, 0x280, b"BDYMORI")
    items = b"".join(struct.pack("<8s4HI", name, 0, 0, 0, 0, flags) for name, flags in
                     ((b"BDAMUL10", 2), (b"BDSW1H09", 2), (b"BDYMORI", 3)))
    struct.pack_into("<II", data, 0x2BC, len(data), 3)
    data.extend(items)
    return bytes(data)


def ledger(xp=23200, *, once=True):
    guard = '  Global("CSR_RN_CHUNK","GLOBAL",0)\n' if once else ""
    return f'''IF
  GlobalGT("bd_plot","global",292)
{guard}THEN
  RESPONSE #100
    SetGlobal("CSR_RN_CHUNK","GLOBAL",1)
    AddexperienceParty({xp})
    Continue()
END
'''


FOREIGN = '''IF
  Global("FOREIGN_QUEST","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_QUEST","GLOBAL",1)
    AddexperienceParty(175)
    Continue()
END
'''


class YmoriGame(SyntheticDialogGame):
    def __init__(self, data=None, *, xp=23200, deactivated=True, prerequisite=True,
                 script=None, expected_xp=23100):
        super().__init__(_dialog_source())
        override = self.root / "override"
        (override / "bd2000.are").write_bytes(area() if data is None else data)
        (override / "bdymori.cre").write_bytes(creature(deactivated=deactivated))
        for name in ("bd2000ym.bcs", "bdjunia.dlg", "bdkendra.dlg", "bdtharan.dlg",
                     "bdamul10.itm", "bdsw1h09.itm", "bdymori.itm"):
            (override / name).write_bytes(f"preserved quest resource {name}".encode())
        with (override / "action.ids").open("a") as handle:
            handle.write("36 Continue()\n64 AddexperienceParty(I:XP*)\n")
        with (override / "trigger.ids").open("a") as handle:
            handle.write("0x4034 GlobalGT(S:Name*,S:Area*,I:Value*)\n")
        (self.root / "fixture/bd2000.baf").write_text(
            FOREIGN + (ledger(xp) if script is None else script) + FOREIGN.replace("FOREIGN_QUEST", "FOREIGN_AFTER"))
        (self.root / "fixture/expected.baf").write_text(
            FOREIGN + ledger(expected_xp) + FOREIGN.replace("FOREIGN_QUEST", "FOREIGN_AFTER"))
        setup = self.root / "setup-ymori-bootstrap.tp2"
        setup.write_text('BACKUP ~weidu_external/backup/ymori-bootstrap~\nAUTHOR ~fixture~\n'
                         'BEGIN ~compile Ymori area fixture~\n'
                         'COMPILE ~fixture/bd2000.baf~\nCOMPILE ~fixture/expected.baf~\n')
        result = self._run(setup)
        if "SUCCESSFULLY INSTALLED" not in self.transcript(result):
            raise AssertionError(self.transcript(result))
        if prerequisite:
            # Synthetic history only; never edit a real installation's log.
            log = self._find_output(self.root, "weidu.log")
            log.write_text(log.read_text() +
                           "~CHRIZ-SOD-REMIX/SETUP-CHRIZ-SOD-REMIX.TP2~ #0 #230 // synthetic prior cut\n")
        self.before = self.resources()
        self.protected = {str(path.relative_to(self.root)): path.read_bytes() for path in
                          (self.root / "chitin.key", self.root / "data/bdsctest.bif", *self.tlks)}

    def resources(self):
        return {path.name.lower(): path.read_bytes() for path in (self.root / "override").iterdir()
                if path.is_file()}

    def install(self):
        return subprocess.run([
            str(WEIDU), "chriz-sod-remix/setup-chriz-sod-remix.tp2",
            "--force-install-list", "235", "--language", "0", "--use-lang", "en_us",
            "--no-exit-pause", "--noautoupdate", "--quick-log",
        ], cwd=self.root, capture_output=True, text=True, timeout=60)


@unittest.skipUnless(WEIDU.is_file(), f"WeiDU unavailable: {WEIDU}")
class YmoriInstallerTests(unittest.TestCase):
    def game(self, *args, **kwargs):
        result = YmoriGame(*args, **kwargs)
        self.addCleanup(result.cleanup)
        return result

    def assert_protected(self, game, allowed=()):
        after = game.resources()
        self.assertEqual(after.keys(), game.before.keys())
        for name, value in game.before.items():
            if name not in allowed:
                self.assertEqual(after[name], value, name)
        for name, value in game.protected.items():
            self.assertEqual((game.root / name).read_bytes(), value, name)

    def assert_success(self, game, *, schedule=0x00FFFFFF):
        result = game.install()
        output = game.transcript(result)
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("SUCCESSFULLY INSTALLED", output)
        self.assert_protected(game, ("bd2000.are", "bd2000.bcs"))
        expected = bytearray(game.before["bd2000.are"])
        struct.pack_into("<I", expected, TARGET + 0x40, schedule)
        after = game.resources()
        self.assertEqual(after["bd2000.are"], bytes(expected))
        self.assertEqual(after["bd2000.bcs"], after["expected.bcs"])

    def assert_rejected(self, game):
        result = game.install()
        output = game.transcript(result)
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn("NOT INSTALLED DUE TO ERRORS", output)
        self.assertIn("comp235", output)
        self.assert_protected(game)

    def test_old_cut_restores_only_schedule_and_old_award(self):
        self.assert_success(self.game())

    def test_fresh_230_native_actor_and_new_award_are_byte_exact_noop(self):
        game = self.game(area(schedule=0xFFFFFFFF), xp=23100)
        self.assert_success(game, schedule=0xFFFFFFFF)
        self.assert_protected(game)

    def test_already_repaired_actor_and_new_award_are_byte_exact_noop(self):
        game = self.game(area(schedule=0x00FFFFFF), xp=23100)
        self.assert_success(game)
        self.assert_protected(game)

    def test_foreign_nonzero_actor_schedule_is_preserved(self):
        self.assert_success(self.game(area(schedule=0x0000FFFF)), schedule=0x0000FFFF)

    def test_cut_actor_with_new_award_repairs_only_actor(self):
        game = self.game(xp=23100)
        self.assert_success(game)
        self.assertEqual(game.resources()["bd2000.bcs"], game.before["bd2000.bcs"])

    def test_missing_deactivated_state_rejects_and_preserves_quest_belongings(self):
        self.assert_rejected(self.game(deactivated=False))

    def test_duplicate_actor_rejects_and_rolls_back_schedule_and_xp(self):
        self.assert_rejected(self.game(area(duplicate=True)))

    def test_missing_actor_rejects(self):
        self.assert_rejected(self.game(area(missing=True)))

    def test_embedded_cre_size_rejects(self):
        self.assert_rejected(self.game(area(embedded_size=0x2D4)))

    def test_embedded_cre_offset_without_size_rejects(self):
        self.assert_rejected(self.game(area(embedded_offset=0x500)))

    def test_unrecognized_award_rejects_and_restores_area(self):
        self.assert_rejected(self.game(xp=23000))

    def test_duplicate_ledger_rejects_and_restores_area(self):
        self.assert_rejected(self.game(script=ledger() + ledger()))

    def test_ledger_without_once_guard_rejects_and_restores_area(self):
        self.assert_rejected(self.game(script=ledger(once=False)))

    def test_known_ledger_plus_reshaped_duplicate_action_pair_rejects(self):
        self.assert_rejected(self.game(script=ledger() + ledger(once=False)))

    def test_invalid_actor_table_rejects(self):
        data = bytearray(area())
        struct.pack_into("<I", data, 0x54, len(data) - 1)
        self.assert_rejected(self.game(bytes(data)))

    def test_public_component_requires_230(self):
        game = self.game(prerequisite=False)
        result = game.install()
        self.assertIn("SKIPPING", game.transcript(result))
        self.assertNotIn("SUCCESSFULLY INSTALLED", game.transcript(result))
        self.assert_protected(game)


if __name__ == "__main__":
    unittest.main()
