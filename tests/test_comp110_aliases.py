"""Alias-aware palace retention, using real WeiDU in disposable games."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'research/scripts'))
from test_comp291_installer import ROOT, WEIDU, write_fake_game, tree
from test_comp197_xp import run_weidu


def strip_block(name, *, clean=False):
    actions = ('SmallWait(1)' if clean else
               f'ActionOverride("{name}",LeaveParty())\nSmallWait(1)\n'
               f'ActionOverride("{name}",DestroySelf())')
    return f'''IF
OR(2)
InMyArea("{name}")
InPartyAllowDead("{name}")
GlobalLT("BD_PLOT","GLOBAL",51)
THEN RESPONSE #100
{actions}
Continue()
END
'''


FOREIGN = '''IF Global("FOREIGN_NPC_QUEST","GLOBAL",1) THEN RESPONSE #100
ActionOverride("ForeignNPC",LeaveParty())
ActionOverride("ForeignNPC",DestroySelf())
ActionOverride("O#XAN",DestroySelf())
SetGlobal("FOREIGN_PRESERVED","GLOBAL",42)
Continue()
END
'''


def write_alias_fixture(game, source=None, expected=None):
    write_fake_game(game)
    for name, extra in {
        'action': '2 ActionOverride(O:Actor*,A:Action*)\n21 SmallWait(I:Wait*)\n'
                  '76 LeaveParty()\n',
        'trigger': '0x4035 GlobalLT(S:Name*,S:Area*,I:Value*)\n'
                   '0x40CB InMyArea(O:Object*)\n0x40D3 InPartyAllowDead(O:Object*)\n',
    }.items():
        path = game / 'override' / f'{name}.ids'
        path.write_text(path.read_text() + extra, encoding='ascii')
    shutil.copytree(ROOT / 'chriz-sod-remix', game / 'chriz-sod-remix')
    fixture = game / 'fixture'
    fixture.mkdir()
    if source is None:
        source = strip_block('O#XAN') + FOREIGN + strip_block('LK#YESLK')
    if expected is None:
        expected = strip_block('O#XAN', clean=True) + FOREIGN + strip_block('LK#YESLK', clean=True)
    (fixture / 'bd0103.baf').write_text(source, encoding='ascii')
    (fixture / 'expected.baf').write_text(expected, encoding='ascii')
    areas = ['bd0101', 'bd0108', 'bd0110', 'bd0111', 'bd1000', 'bd2000', 'bd2100', 'bd7000', 'bd7100']
    for area in areas:
        (fixture / f'{area}.baf').write_text('IF True() THEN RESPONSE #100 Continue() END\n')
    (fixture / 'setup-fixture.tp2').write_text('BACKUP ~fixture-backup~ AUTHOR ~test~ BEGIN ~fixture~\n' +
        '\n'.join(f'COMPILE ~fixture/{name}.baf~' for name in ['bd0103', 'expected', *areas]))
    (game / 'repair.tp2').write_text('''BACKUP ~repair-backup~ AUTHOR ~test~
BEGIN ~renamed companion retention~ DESIGNATED 110
INCLUDE ~chriz-sod-remix/lib/comp110_aliases.tpa~
LAF csr110_keep_renamed_companions END
''')
    # The repair must not edit saved/template build data or shared tables.
    for name in ['xan.cre', 'o#xan.cre', 'yeslick.cre', 'lk#yeslk.cre', 'bdintro.bcs',
                 'bddialog.2da', 'partyai.2da']:
        (game / 'override' / name).write_bytes(('protected ' + name).encode())


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class RenamedCompanionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='csr110-aliases-')
        self.addCleanup(temporary.cleanup)
        self.game = Path(temporary.name)

    def fixture(self, source=None, expected=None):
        write_alias_fixture(self.game, source, expected)
        result = run_weidu(self.game, 'fixture/setup-fixture.tp2', '--force-install-list', '0')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return tree(self.game / 'override')

    def repair(self, name='repair.tp2'):
        return run_weidu(self.game, name, '--force-install-list', '110')

    def assert_only_palace_changes(self, before):
        after = tree(self.game / 'override')
        self.assertEqual(after.keys(), before.keys())
        self.assertEqual({k for k in before if before[k] != after[k]}, {'BD0103.BCS'})
        self.assertEqual((self.game / 'override/bd0103.bcs').read_bytes(),
                         (self.game / 'override/expected.bcs').read_bytes())

    def test_tail_repair_preserves_foreign_actions_and_character_resources(self):
        before = self.fixture()
        result = self.repair()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assert_only_palace_changes(before)
        result = run_weidu(self.game, 'repair.tp2', '--force-uninstall-list', '110')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_one_alias_or_already_fixed_other_alias(self):
        for other in ('', strip_block('LK#YESLK', clean=True)):
            with self.subTest(other=bool(other)), tempfile.TemporaryDirectory() as temporary:
                game = Path(temporary)
                write_alias_fixture(game, strip_block('O#XAN') + FOREIGN + other,
                                    strip_block('O#XAN', clean=True) + FOREIGN + other)
                for tp2, component in [('fixture/setup-fixture.tp2', '0'), ('repair.tp2', '110')]:
                    result = run_weidu(game, tp2, '--force-install-list', component)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual((game / 'override/bd0103.bcs').read_bytes(),
                                 (game / 'override/expected.bcs').read_bytes())

    def test_absent_aliases_are_byte_exact_noop(self):
        before = self.fixture(FOREIGN, FOREIGN)
        self.assertEqual(self.repair().returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_second_execution_is_byte_exact_noop(self):
        self.fixture()
        self.assertEqual(self.repair().returncode, 0)
        before = tree(self.game / 'override')
        shutil.copy2(self.game / 'repair.tp2', self.game / 'second.tp2')
        self.assertEqual(self.repair('second.tp2').returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_duplicate_target_fails_before_any_write(self):
        before = self.fixture(strip_block('O#XAN') * 2 + strip_block('LK#YESLK'))
        self.assertNotEqual(self.repair().returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_late_unknown_action_fails_before_earlier_alias_write(self):
        changed = strip_block('LK#YESLK').replace('SmallWait(1)',
                  'SmallWait(1)\nSetGlobal("FOREIGN_INSIDE","GLOBAL",1)')
        before = self.fixture(strip_block('O#XAN') + changed)
        self.assertNotEqual(self.repair().returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_partial_strip_fails_without_removing_the_remaining_action(self):
        before = self.fixture(strip_block('O#XAN').replace('ActionOverride("O#XAN",LeaveParty())', ''))
        self.assertNotEqual(self.repair().returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_case_insensitive_aliases(self):
        source = strip_block('o#xan') + strip_block('lk#yeslk')
        expected = strip_block('o#xan', clean=True) + strip_block('lk#yeslk', clean=True)
        before = self.fixture(source, expected)
        result = self.repair()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assert_only_palace_changes(before)

    def test_fresh_public_110_retains_original_and_normalized_identities(self):
        source = strip_block('xan') + strip_block('yeslick') + strip_block('O#XAN') + strip_block('LK#YESLK')
        expected = ''.join(strip_block(n, clean=True) for n in ('xan', 'yeslick', 'O#XAN', 'LK#YESLK'))
        before = self.fixture(source, expected)
        result = self.repair('chriz-sod-remix/setup-chriz-sod-remix.tp2')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.game / 'override/bd0103.bcs').read_bytes(),
                         (self.game / 'override/expected.bcs').read_bytes())
        after = tree(self.game / 'override')
        changed = {k for k in before if before[k] != after[k]}
        self.assertEqual(changed, {'BD0103.BCS', 'BD0101.BCS', 'BD0108.BCS', 'BD0110.BCS',
                         'BD0111.BCS', 'BD1000.BCS', 'BD2000.BCS', 'BD2100.BCS', 'BD7000.BCS', 'BD7100.BCS'})
        self.assertEqual(before.keys(), after.keys())


if __name__ == '__main__':
    unittest.main()
