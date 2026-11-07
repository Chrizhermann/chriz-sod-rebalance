"""Label-addressed table writes through real WeiDU in disposable fixtures."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'research/scripts'))
from test_comp291_installer import ROOT, WEIDU, write_fake_game


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class TableWriterTests(unittest.TestCase):
    def run_case(self, source, expected):
        with tempfile.TemporaryDirectory(prefix='csr-overwrite-2da-') as directory:
            game = Path(directory)
            write_fake_game(game)
            (game / 'weidu.log').write_text('')
            shutil.copy2(ROOT / 'chriz-sod-remix/lib/overwrite_2da.tpa', game / 'writer.tpa')
            target = game / 'override/bddialog.2da'
            target.write_text(source)
            for iteration in ('first', 'second'):
                (game / f'{iteration}.tp2').write_text(f'''BACKUP ~{iteration}-backup~
AUTHOR ~test~ BEGIN ~label-addressed table writer~
INCLUDE ~writer.tpa~
COPY_EXISTING ~bddialog.2da~ ~override~
  LPF csr_set_2da_cell STR_VAR row = ~SKIE~ column = ~POST_DIALOG_FILE~ value = ~CSR198SK~ END
  LPF csr_set_2da_cell STR_VAR row = ~SKIE~ column = ~JOIN_DIALOG_FILE~ value = ~CSR198SK~ END
BUT_ONLY
''')
                result = subprocess.run([str(WEIDU), f'{iteration}.tp2', '--force-install-list', '0',
                                         '--game', str(game), '--use-lang', 'en_US', '--no-exit-pause'],
                                        cwd=game, capture_output=True, text=True, timeout=45)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn('WARNING', (result.stdout + result.stderr).upper())
                lines = [line.split() for line in target.read_text().splitlines()]
                columns = lines[2]
                rows = {line[0]: dict(zip(columns, line[1:])) for line in lines[3:]}
                self.assertEqual(rows, expected)
                if iteration == 'first':
                    first = target.read_bytes()
                else:
                    self.assertEqual(target.read_bytes(), first)

    def test_reordered_columns_and_foreign_values(self):
        self.run_case('2DA V1.0\n***\nDREAM_SCRIPT_FILE JOIN_DIALOG_FILE POST_DIALOG_FILE\n'
                      'SKIE DREAM OTHER OLD\nFOREIGN F1 F2 F3\n', {
            'SKIE': {'DREAM_SCRIPT_FILE': 'DREAM', 'JOIN_DIALOG_FILE': 'CSR198SK', 'POST_DIALOG_FILE': 'CSR198SK'},
            'FOREIGN': {'DREAM_SCRIPT_FILE': 'F1', 'JOIN_DIALOG_FILE': 'F2', 'POST_DIALOG_FILE': 'F3'},
        })

    def test_missing_columns_and_row(self):
        self.run_case('2DA V1.0\n***\nDREAM_SCRIPT_FILE\nFOREIGN DREAM\n', {
            'SKIE': {'DREAM_SCRIPT_FILE': '***', 'JOIN_DIALOG_FILE': 'CSR198SK', 'POST_DIALOG_FILE': 'CSR198SK'},
            'FOREIGN': {'DREAM_SCRIPT_FILE': 'DREAM', 'JOIN_DIALOG_FILE': '***', 'POST_DIALOG_FILE': '***'},
        })

    def test_changed_text_and_extra_column(self):
        self.run_case('2DA V1.0\n0\nPOST_DIALOG_FILE JOIN_DIALOG_FILE EXTRA\n'
                      'SKIE HAND_EDITED ANOTHER_LANGUAGE PRESERVE\n', {
            'SKIE': {'POST_DIALOG_FILE': 'CSR198SK', 'JOIN_DIALOG_FILE': 'CSR198SK', 'EXTRA': 'PRESERVE'},
        })


if __name__ == '__main__':
    unittest.main()
