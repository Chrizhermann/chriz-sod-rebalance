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
    (game / "weidu.log").write_text("")
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
        result = run_weidu(self.game, tp2, '--force-install-list', '197')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('WARNING', (result.stdout + result.stderr).upper())
        return result

    def rows(self):
        lines = (self.game / 'override/bddialog.2da').read_text().splitlines()
        header = lines[2].upper().split()
        return [(row[0].upper(), dict(zip(header, row[1:]))) for row in map(str.split, lines[3:]) if row]

    def owned(self):
        rows = [values for label, values in self.rows() if label == 'BDSKIE']
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row['POST_DIALOG_FILE'].upper(), 'BDSKIE')
        return rows

    def test_new_row_and_uninstall_preserve_other_resources(self):
        before = self.fixture()
        self.install()
        after = tree(self.game / 'override')
        self.assertEqual({n for n in after if after[n] != before[n]}, {'BDDIALOG.2DA'})
        self.assertEqual(self.owned()[0], dict(POST_DIALOG_FILE='BDSKIE', JOIN_DIALOG_FILE='MULTIG', DREAM_SCRIPT_FILE='***'))
        result = run_weidu(self.game, 'route.tp2', '--force-uninstall-list', '197')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_existing_cells_outside_post_are_preserved(self):
        self.fixture(TABLE + b'BDSKIE FOREIGNP FOREIGNJ FOREIGHD\r\n')
        self.install()
        self.assertEqual(self.owned()[0]['JOIN_DIALOG_FILE'], 'FOREIGNJ')
        self.assertEqual(self.owned()[0]['DREAM_SCRIPT_FILE'], 'FOREIGHD')

    def test_second_tail_execution_is_byte_identical(self):
        self.fixture()
        self.install()
        before = tree(self.game / 'override')
        (self.game / 'second.tp2').write_text((self.game / 'route.tp2').read_text().replace('route-backup', 'second-backup'))
        self.install('second.tp2')
        self.assertEqual(tree(self.game / 'override'), before)

    def test_optional_columns_and_short_foreign_rows(self):
        table = TABLE.replace(b'DREAM_SCRIPT_FILE\r\n', b'DREAM_SCRIPT_FILE EXTRA SECOND\r\n')
        self.fixture(table + b'MODDED MP MJ MD KEEP_THIS KEEP_TOO\r\n')
        self.install()
        self.assertEqual(self.owned()[0]['EXTRA'], '***')
        self.assertEqual(dict(self.rows())['MODDED']['EXTRA'], 'KEEP_THIS')

    def test_existing_optional_values_survive(self):
        table = TABLE.replace(b'DREAM_SCRIPT_FILE\r\n', b'DREAM_SCRIPT_FILE EXTRA\r\n')
        self.fixture(table + b'BDSKIE old multig *** RETAIN\r\n')
        self.install()
        self.assertEqual(self.owned()[0]['EXTRA'], 'RETAIN')

    def test_missing_final_newline(self):
        self.fixture(TABLE.rstrip(b'\r\n'))
        self.install()
        self.assertIn('FOREIGN', dict(self.rows()))
        self.owned()

    def test_all_duplicate_rows_receive_the_owned_cell(self):
        self.fixture(TABLE + b'BDSKIE OLD JOIN DREAM\n' * 2)
        self.install()
        self.assertEqual(len(self.owned()), 2)

    def test_reordered_columns(self):
        self.fixture(TABLE.replace(b'POST_DIALOG_FILE JOIN_DIALOG_FILE', b'JOIN_DIALOG_FILE POST_DIALOG_FILE'))
        self.install()
        self.owned()

    def test_missing_post_column(self):
        self.fixture(b'2DA V1.0\n***\n JOIN_DIALOG_FILE\nBDSKIE EXISTING\n')
        self.install()
        self.assertEqual(self.owned()[0]['JOIN_DIALOG_FILE'], 'EXISTING')

    def test_missing_table_is_created(self):
        self.fixture()
        (self.game / 'override/bddialog.2da').unlink()
        self.install()
        self.assertEqual(self.owned()[0]['JOIN_DIALOG_FILE'], 'MULTIG')

    def test_component_calls_after_dialogue_compile(self):
        source = (ROOT / 'chriz-sod-remix/lib/comp197.tpa').read_text(encoding='utf-8')
        self.assertLess(source.index('INCLUDE ~chriz-sod-remix/lib/comp197_meeting.tpa~'), source.index('LAF csr197_install_dialogue_route END'))

if __name__ == '__main__':
    unittest.main()
