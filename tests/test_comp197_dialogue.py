"""Palace Skie's campaign POST route: real WeiDU, disposable games only."""
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'research/scripts'))
from test_comp291_installer import ROOT, WEIDU, write_fake_game, tree
from test_comp197_xp import run_weidu


TABLE = (b'2DA V1.0\r\n0\r\n'
         b'              POST_DIALOG_FILE JOIN_DIALOG_FILE DREAM_SCRIPT_FILE\r\n'
         b'SKIE          BDSKIE           SKIEJ            SKIED\r\n'
         b'FOREIGN       FOREIGNP         FOREIGNJ         FOREIGND\r\n')


def write_skie_dialogue_fixture(game, table=TABLE):
    write_fake_game(game)
    shutil.copytree(ROOT / 'chriz-sod-remix', game / 'chriz-sod-remix')
    (game / 'override/bddialog.2da').write_bytes(table)
    # Existing dialogue/resources must stay untouched by this table-only hook.
    dlg = bytearray(0x34)
    dlg[:8] = b'DLG V1.0'
    struct.pack_into('<I', dlg, 12, 0x34)
    for name in ('bdskie', 'multig', 'skie'):
        (game / 'override' / f'{name}.dlg').write_bytes(dlg)
    for name in ('bdskie.cre', 'bdskie.bcs', 'pdialog.2da', 'campaign.2da'):
        (game / 'override' / name).write_bytes(('protected ' + name).encode())
    (game / 'route.tp2').write_text('''BACKUP ~route-backup~ AUTHOR ~test~
BEGIN ~Palace Skie POST route~ DESIGNATED 197
INCLUDE ~chriz-sod-remix/lib/comp197_dialogue.tpa~
LAF csr197_install_dialogue_route END
''')


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class SkieDialogueRouteTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='csr197-dialogue-')
        self.addCleanup(temporary.cleanup)
        self.game = Path(temporary.name)

    def fixture(self, table=TABLE):
        write_skie_dialogue_fixture(self.game, table)
        return tree(self.game / 'override')

    def install(self, tp2='route.tp2'):
        return run_weidu(self.game, tp2, '--force-install-list', '197')

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_only_appends_palace_row_and_uninstall_restores_exact_bytes(self):
        before = self.fixture()
        self.assert_success(self.install())
        after = tree(self.game / 'override')
        self.assertEqual(after.keys(), before.keys())
        self.assertEqual({n for n in after if after[n] != before[n]}, {'BDDIALOG.2DA'})
        self.assertEqual((self.game / 'override/bddialog.2da').read_bytes(),
                         TABLE + b'BDSKIE BDSKIE MULTIG ***\n')
        self.assert_success(run_weidu(self.game, 'route.tp2', '--force-uninstall-list', '197'))
        self.assertEqual(tree(self.game / 'override'), before)

    def test_already_correct_modded_row_is_byte_exact_noop(self):
        table = TABLE + b'bdskie  bdskie  multig  ***\r\n'
        before = self.fixture(table)
        self.assert_success(self.install())
        self.assertEqual(tree(self.game / 'override'), before)

    def test_second_independent_execution_is_byte_exact_noop(self):
        self.fixture()
        self.assert_success(self.install())
        before = tree(self.game / 'override')
        shutil.copyfile(self.game / 'route.tp2', self.game / 'second.tp2')
        self.assert_success(self.install('second.tp2'))
        self.assertEqual(tree(self.game / 'override'), before)

    def test_optional_columns_and_short_foreign_rows_are_preserved(self):
        table = TABLE.replace(b'DREAM_SCRIPT_FILE\r\n', b'DREAM_SCRIPT_FILE EXTRA SECOND\r\n')
        table += b'MODDED MP MJ MD KEEP_THIS KEEP_TOO\r\n'
        self.fixture(table)
        self.assert_success(self.install())
        self.assertEqual((self.game / 'override/bddialog.2da').read_bytes(),
                         table + b'BDSKIE BDSKIE MULTIG *** *** ***\n')

    def test_header_width_wins_when_all_existing_rows_are_short(self):
        table = TABLE.replace(b'DREAM_SCRIPT_FILE\r\n', b'DREAM_SCRIPT_FILE EXTRA SECOND\r\n')
        self.fixture(table)
        self.assert_success(self.install())
        self.assertEqual((self.game / 'override/bddialog.2da').read_bytes(),
                         table + b'BDSKIE BDSKIE MULTIG *** *** ***\n')

    def test_existing_correct_optional_values_are_preserved(self):
        table = TABLE.replace(b'DREAM_SCRIPT_FILE\r\n', b'DREAM_SCRIPT_FILE EXTRA\r\n')
        table += b'BDSKIE BDSKIE MULTIG *** RETAIN\r\n'
        before = self.fixture(table)
        self.assert_success(self.install())
        self.assertEqual(tree(self.game / 'override'), before)

    def test_missing_final_newline_does_not_join_two_rows(self):
        self.fixture(TABLE.rstrip(b'\r\n'))
        self.assert_success(self.install())
        self.assertEqual((self.game / 'override/bddialog.2da').read_bytes(),
                         TABLE.rstrip(b'\r\n') + b'\nBDSKIE BDSKIE MULTIG ***\n')

    def test_conflicting_short_row_is_not_hidden_by_optional_columns(self):
        table = TABLE.replace(b'DREAM_SCRIPT_FILE\r\n', b'DREAM_SCRIPT_FILE EXTRA SECOND\r\n')
        table += b'BDSKIE FOREIGNP FOREIGNJ FOREIGHD\r\n'
        before = self.fixture(table)
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('another BDSKIE dialogue route', result.stdout + result.stderr)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_duplicate_rows_fail_without_writes(self):
        before = self.fixture(TABLE + b'BDSKIE BDSKIE MULTIG ***\n' * 2)
        self.assertNotEqual(self.install().returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_unfamiliar_header_fails_without_writes(self):
        before = self.fixture(TABLE.replace(b'POST_DIALOG_FILE JOIN_DIALOG_FILE',
                                            b'JOIN_DIALOG_FILE POST_DIALOG_FILE'))
        self.assertNotEqual(self.install().returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_component_197_calls_route_after_its_dialogue_compile(self):
        source = (ROOT / 'chriz-sod-remix/lib/comp197.tpa').read_text()
        self.assertEqual(source.count('LAF csr197_install_dialogue_route END'), 1)
        self.assertLess(source.index('COMPILE ~chriz-sod-remix/dlg/csr197skie.d~'),
                        source.index('LAF csr197_install_dialogue_route END'))


if __name__ == '__main__':
    unittest.main()
