"""Real WeiDU installs for Liia's flat reward in disposable synthetic games."""

import re
import struct
import subprocess
import unittest

from test_bdscry_compat import WEIDU, SyntheticDialogGame, _dialog_source


def award(xp=24000):
    return ('SetGlobal("CSR_KORL_RET","GLOBAL",2)\n' +
            "\n".join(f"AddXPObject(Player{slot},{xp})" for slot in range(1, 7)) +
            "\nDestroySelf()")


def dialog(action, *, gate=1, terminal_gate="", reply_action=""):
    return f'''BEGIN ~csrcele~
IF ~Global("FOREIGN_QUEST","GLOBAL",0)~ THEN BEGIN 0
  SAY #0
  IF ~~ THEN DO ~SetGlobal("FOREIGN_QUEST","GLOBAL",1)~ EXIT
END
IF ~Global("CSR_KORL_RET","GLOBAL",{gate})~ THEN BEGIN 1
  SAY #0
  IF ~~ THEN REPLY #0 {reply_action} GOTO 2
  IF ~~ THEN REPLY #0 GOTO 2
END
IF ~{terminal_gate}~ THEN BEGIN 2
  SAY ~Then the Fist will see to what remains.~
  IF ~~ THEN DO ~{action}~ EXIT
END
IF ~~ THEN BEGIN 3
  SAY #0
  IF ~~ THEN DO ~AddexperienceParty(24000)~ EXIT
END
'''


class PrologueGame(SyntheticDialogGame):
    def __init__(self, action=None, *, prerequisite=True, **kwargs):
        super().__init__(_dialog_source())
        override = self.root / "override"
        with (override / "action.ids").open("a") as handle:
            handle.write("111 DestroySelf()\n259 AddXPObject(O:Object*,I:XP*)\n"
                         "64 AddexperienceParty(I:XP*)\n")
        (override / "object.ids").write_text(
            "IDS V1.0\n1 Myself\n" +
            "".join(f"{20 + slot} Player{slot}\n" for slot in range(1, 7)))
        (override / "bd0120.are").write_bytes(b"unmodified SoD presence marker")
        (self.root / "fixture/csrcele.d").write_text(dialog(
            award() if action is None else action, **kwargs))
        setup = self.root / "setup-prologue-bootstrap.tp2"
        setup.write_text('BACKUP ~weidu_external/backup/prologue-bootstrap~\n'
                         'AUTHOR ~fixture~\nBEGIN ~compile prologue fixture~\n'
                         'COMPILE ~fixture/csrcele.d~\n')
        result = self._run(setup)
        if "SUCCESSFULLY INSTALLED" not in self.transcript(result):
            raise AssertionError(self.transcript(result))
        # Synthetic history only: no real game log is edited.
        components = (170, 180, 175) if prerequisite else (170, 180)
        log = self._find_output(self.root, "weidu.log")
        log.write_text(log.read_text() + "".join(
            f"~CHRIZ-SOD-REMIX/SETUP-CHRIZ-SOD-REMIX.TP2~ #0 #{comp} // fixture\n"
            for comp in components))
        self.before = self.resources()
        self.protected = {str(path.relative_to(self.root)): path.read_bytes() for path in
                          (self.root / "chitin.key", self.root / "data/bdsctest.bif", *self.tlks)}

    def resources(self):
        return {path.name.lower(): path.read_bytes() for path in
                (self.root / "override").iterdir() if path.is_file()}

    def install(self, component=176):
        return subprocess.run([
            str(WEIDU), "chriz-sod-remix/setup-chriz-sod-remix.tp2",
            "--force-install-list", str(component), "--language", "0", "--use-lang", "en_us",
            "--no-exit-pause", "--noautoupdate", "--quick-log",
        ], cwd=self.root, capture_output=True, text=True, timeout=60)


@unittest.skipUnless(WEIDU.is_file(), f"WeiDU unavailable: {WEIDU}")
class PrologueXPInstallerTests(unittest.TestCase):
    def game(self, *args, **kwargs):
        game = PrologueGame(*args, **kwargs)
        self.addCleanup(game.cleanup)
        return game

    def assert_unrelated_preserved(self, game):
        after = game.resources()
        for name, data in game.before.items():
            if name != "csrcele.dlg":
                self.assertEqual(after[name], data, name)
        for path, data in game.protected.items():
            if not path.endswith("dialog.tlk"):
                self.assertEqual((game.root / path).read_bytes(), data, path)
        source = game.decompile("csrcele")
        self.assertIn('SetGlobal("FOREIGN_QUEST","GLOBAL",1)', source)
        self.assertIn('AddexperienceParty(24000)', source)

    def assert_success(self, result, game):
        output = game.transcript(result)
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("SUCCESSFULLY INSTALLED", output)
        self.assertNotIn("WARNING", output.upper())

    def assert_reward(self, game):
        self.assert_success(game.install(), game)
        source = game.decompile("csrcele")
        self.assertEqual(re.findall(r"AddXPObject\(Player([1-6]),(\d+)\)", source),
                         [(str(slot), "22000") for slot in range(1, 7)])
        self.assertIn('Global("CSR_KORL_RET","GLOBAL",1)', source)
        self.assertNotIn('Global("CSR_KORL_RET","GLOBAL",0)', source)
        self.assertLess(source.index('AddXPObject(Player6,22000)'), source.index('DestroySelf()'))
        self.assert_unrelated_preserved(game)

    def test_original_award_is_normalized(self):
        self.assert_reward(self.game())

    def test_current_award_is_written(self):
        self.assert_reward(self.game(award(22000)))

    def test_fresh_175_and_176_have_the_same_output(self):
        game = self.game('SetGlobal("CSR_KORL_RET","GLOBAL",2)\nDestroySelf()',
                         prerequisite=False)
        self.assert_success(game.install(175), game)
        first = game.resources()["csrcele.dlg"]
        self.assert_success(game.install(), game)
        self.assertEqual(game.resources()["csrcele.dlg"], first)

    def test_hand_edited_award_is_overwritten(self):
        self.assert_reward(self.game(award(21000)))

    def test_missing_award_is_restored(self):
        self.assert_reward(self.game(award().replace("AddXPObject(Player6,24000)", "")))

    def test_extra_recipient_is_normalized(self):
        self.assert_reward(self.game(award().replace("Player6", "Player5")))

    def test_changed_once_gate_is_restored(self):
        self.assert_reward(self.game(gate=0))

    def test_terminal_entry_trigger_is_removed(self):
        self.assert_reward(self.game(terminal_gate="True()"))

    def test_extra_reply_reward_is_removed(self):
        self.assert_reward(self.game(reply_action="DO ~AddXPObject(Player1,24000)~"))

    def test_action_order_is_written(self):
        self.assert_reward(self.game("DestroySelf()\n" + award().replace("\nDestroySelf()", "")))

    def test_missing_states_are_created(self):
        game = self.game()
        (game.root / "fixture/csrcele.d").write_text(
            'BEGIN ~csrcele~\nIF ~True()~ THEN BEGIN 0 SAY #0 IF ~~ THEN EXIT END\n')
        setup = game.root / "setup-missing-states.tp2"
        setup.write_text('BACKUP ~missing-states-backup~\nAUTHOR ~fixture~\n'
                         'BEGIN ~remove the return states~\nCOMPILE ~fixture/csrcele.d~\n')
        self.assert_success(game._run(setup), game)
        self.assert_success(game.install(), game)
        source = game.decompile("csrcele")
        self.assertEqual(re.findall(r"AddXPObject\(Player([1-6]),(\d+)\)", source),
                         [(str(slot), "22000") for slot in range(1, 7)])

    def test_second_install_is_byte_identical(self):
        game = self.game()
        self.assert_success(game.install(), game)
        first = game.resources()["csrcele.dlg"]
        self.assert_success(game.install(), game)
        self.assertEqual(game.resources()["csrcele.dlg"], first)

    def test_public_component_requires_175(self):
        game = self.game(prerequisite=False)
        result = game.install()
        self.assertIn("SKIPPING", game.transcript(result))
        self.assertNotIn("SUCCESSFULLY INSTALLED", game.transcript(result))
        self.assertEqual(game.resources(), game.before)


if __name__ == "__main__":
    unittest.main()
