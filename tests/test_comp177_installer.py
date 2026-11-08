"""Liia's report route survives changed and missing native dialogue/script data."""
import re
import unittest

from test_comp176_installer import PrologueGame, WEIDU


@unittest.skipUnless(WEIDU.is_file(), "real WeiDU unavailable; set WEIDU_EXE")
class LiiaReportTests(unittest.TestCase):
    def game(self, *, states=34, journal=True, farewell=True):
        game = PrologueGame()
        self.addCleanup(game.cleanup)
        override = game.root / "override"
        extras = {
            "action": '36 Continue()\n263 EraseJournalEntry(I:STRREF*)\n'
                      '152 AddJournalEntry(I:Entry*,I:Type*JOURTYPE)\n',
            "trigger": '0x4034 GlobalGT(S:Name*,S:Area*,I:Value*)\n'
                       '0x4035 GlobalLT(S:Name*,S:Area*,I:Value*)\n'
                       '0x4019 Dead(S:Name*)\n0x40D4 AreaCheck(S:ResRef*)\n',
        }
        for name, value in extras.items():
            path = override / f"{name}.ids"
            path.write_text(path.read_text() + value)
        (override / "jourtype.ids").write_text("IDS V1.0\n0 INFO\n1 QUEST\n2 QUEST_DONE\n")
        (override / "bgee.lua").write_text("function createQuest() end\nfunction createEntry() end\n")
        source = ['BEGIN ~bdliia~']
        for index in range(states):
            trigger = 'Global("BD_plot","GLOBAL",56)' if index == 33 else 'True()'
            transition = 'IF ~~ THEN EXIT' if farewell or index != 33 else ''
            source.append(f'IF ~{trigger}~ THEN BEGIN {index}\nSAY ~Changed greeting {index}~\n{transition}\nEND')
        (game.root / "fixture/bdliia.d").write_text("\n".join(source))
        journal_action = 'AddJournalEntry(0,QUEST_DONE)' if journal else ''
        (game.root / "fixture/bd0116.baf").write_text(
            'IF Dead("BDKORLAS") Global("bd_sdd011b_korlasz_journal_entry","BD0116",0) '
            'THEN RESPONSE #100 ' + journal_action +
            ' SetGlobal("bd_sdd011b_korlasz_journal_entry","BD0116",1) END\n'
            if journal else 'IF True() THEN RESPONSE #100 Continue() END\n')
        (game.root / "fixture/bd0102.baf").write_text('IF True() THEN RESPONSE #100 Continue() END\n')
        setup = game.root / "setup-report-fixture.tp2"
        setup.write_text('BACKUP ~report-fixture-backup~ AUTHOR ~test~ BEGIN ~report fixture~\n'
                         'COMPILE ~fixture/bdliia.d~ ~fixture/bd0116.baf~ ~fixture/bd0102.baf~\n')
        self.success(game, game._run(setup))
        return game

    def success(self, game, result):
        output = game.transcript(result)
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("SUCCESSFULLY INSTALLED", output)
        self.assertNotIn("WARNING", output.upper())

    def assert_report(self, game):
        self.success(game, game.install(177))
        source = game.decompile("bdliia")
        self.assertEqual(re.findall(r'AddXPObject\(Player([1-6]),(\d+)\)', source),
                         [(str(i), "22000") for i in range(1, 7)])
        self.assertIn('GlobalLT("CSR_KORL_RET","GLOBAL",2)', source)
        self.assertIn('SetGlobal("CSR177_REPORT","GLOBAL",1)', source)

    def test_changed_text_and_journal_registration(self):
        self.assert_report(self.game())

    def test_missing_native_states(self):
        self.assert_report(self.game(states=1))

    def test_missing_death_journal_block(self):
        self.assert_report(self.game(journal=False))

    def test_missing_departure_transition(self):
        self.assert_report(self.game(farewell=False))

    def test_absent_native_dialogue_and_scripts_are_created(self):
        game = self.game()
        for name in ('bdliia.dlg', 'bd0116.bcs', 'bd0102.bcs'):
            (game.root/'override'/name).unlink()
        self.assert_report(game)

    def test_damaged_dialogue_tables_are_rebuilt(self):
        game = self.game()
        (game.root/'override/bdliia.dlg').write_bytes(b'DLG V1.0')
        (game.root/'override/csrcele.dlg').write_bytes(b'DLG V1.0')
        self.assert_report(game)

    def test_second_tail_does_not_duplicate_report_states_or_replies(self):
        game = self.game()
        self.assert_report(game)
        first = (game.root/'override/bdliia.dlg').read_bytes()
        setup = game.root/'second-report.tp2'
        setup.write_text('BACKUP ~second-report-backup~ AUTHOR ~test~ BEGIN ~second report~\n'
                         'INCLUDE ~chriz-sod-remix/lib/comp177.tpa~\n')
        self.success(game, game._run(setup))
        self.assertEqual((game.root/'override/bdliia.dlg').read_bytes(), first)
        self.assertEqual(game.decompile('bdliia').count('AddXPObject(Player1,22000)'), 1)

    def test_second_install_has_same_dialogue(self):
        game = self.game()
        self.assert_report(game)
        first = (game.root / "override/bdliia.dlg").read_bytes()
        self.assert_report(game)
        self.assertEqual((game.root / "override/bdliia.dlg").read_bytes(), first)
