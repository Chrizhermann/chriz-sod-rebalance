"""Real WeiDU checks for the native-confirmed Shar-Teel field rejoin repair.

All mutations are confined to disposable synthetic games; no native timing or
other retained companion acceptance is inferred from these checks.
"""
from pathlib import Path
import re
import shutil
import struct
import tempfile
import unittest

from test_comp110_aliases import WEIDU, write_alias_fixture, tree
from test_comp197_xp import run_weidu


def compact(value):
    return re.sub(r'\s+', '', value).upper()


def dialogue(data):
    def number(offset):
        return struct.unpack_from('<I', data, offset)[0]

    def script(table, count, index):
        if index == 0xffffffff:
            return ''
        assert index < number(count)
        offset = number(table) + index * 8
        return data[number(offset):number(offset) + number(offset + 4)].decode('ascii')

    states = []
    for index in range(number(8)):
        offset = number(12) + index * 16
        say, first, count, trigger = struct.unpack_from('<IIII', data, offset)
        transitions = []
        for t in range(first, first + count):
            offset = number(20) + t * 32
            flags, reply, journal, tri, action = struct.unpack_from('<IIIII', data, offset)
            transitions.append((flags, reply, journal,
                script(32, 36, tri) if flags & 2 else '',
                script(40, 44, action) if flags & 4 else '',
                data[offset + 20:offset + 28].rstrip(b'\0').decode('ascii'),
                number(offset + 28)))
        states.append((say, script(24, 28, trigger), transitions))
    return states


def source(*, bad_root=False, bad_join=False, bad_wait=False, foreign=False):
    root = ('OR(2) AreaCheck("BD0120") AreaCheck("BD0130") '
            'Global("bd_joined","locals",0)')
    if bad_root:
        root = root.replace('BD0130', 'BD0102')
    parts = ['BEGIN ~BDSHARTE~']
    for state in range(7):
        trigger = root if state == 4 else ('True()' if state == 0 else '')
        if state == 4:
            transitions = ('IF ~~ THEN REPLY ~Travel with me again?~ GOTO 5\n'
                           'IF ~~ THEN REPLY ~Wait here.~ GOTO 6')
        elif state == 5:
            action = 'JoinParty()' + (' SetGlobal("FOREIGN","GLOBAL",1)' if bad_join else '')
            transitions = f'IF ~~ THEN DO ~{action}~ EXIT'
        elif state == 6 and bad_wait:
            transitions = 'IF ~~ THEN DO ~DestroySelf()~ EXIT'
        else:
            transitions = 'IF ~~ THEN EXIT'
        parts.append(f'IF ~{trigger}~ THEN BEGIN {state}\nSAY ~existing {state}~\n{transitions}\nEND')
    if foreign:
        parts.append('IF ~Global("FOREIGN","GLOBAL",1)~ THEN BEGIN foreign '
                     'SAY ~foreign text~ IF ~~ THEN DO ~SetGlobal("UNCHANGED","GLOBAL",1)~ EXIT END')
    return '\n'.join(parts)


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class SharTeelFieldTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='csr110-field-')
        self.addCleanup(temporary.cleanup)
        self.game = Path(temporary.name)
        write_alias_fixture(self.game)
        extras = {
            'action': '19 JoinParty()\n',
            'trigger': '0x4034 GlobalGT(S:Name*,S:Area*,I:Value*)\n'
                       '0x4043 InParty(O:Object*)\n0x40A5 Name(S:Name*,O:Object*)\n'
                       '0x40DF BeenInParty(S:Name*)\n',
        }
        for name, value in extras.items():
            path = self.game / 'override' / f'{name}.ids'
            path.write_text(path.read_text() + value)
        (self.game / 'field.tp2').write_text('''BACKUP ~field-backup~ AUTHOR ~test~
BEGIN ~Shar-Teel field rejoin~ DESIGNATED 110
INCLUDE ~chriz-sod-remix/lib/comp110_field.tpa~
LAF csr110_sharteel_field_rejoin END
''')

    def fixture(self, **kwargs):
        (self.game / 'fixture/bdsharte.d').write_text(source(**kwargs))
        installer = self.game / 'fixture/setup-fixture.tp2'
        installer.write_text(installer.read_text() + '\nCOMPILE ~fixture/bdsharte.d~\n')
        result = run_weidu(self.game, 'fixture/setup-fixture.tp2', '--force-install-list', '0')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.original = dialogue((self.game / 'override/bdsharte.dlg').read_bytes())
        return tree(self.game / 'override')

    def repair(self, filename='field.tp2'):
        return run_weidu(self.game, filename, '--force-install-list', '110')

    def assert_route(self):
        states = dialogue((self.game / 'override/bdsharte.dlg').read_bytes())
        self.assertEqual(states[:-1], self.original)
        say, trigger, transitions = states[-1]
        self.assertEqual(say, states[4][0])
        self.assertEqual(transitions, states[4][2])
        self.assertEqual(compact(states[5][2][0][4]), 'JOINPARTY()')
        self.assertEqual(compact(trigger), compact('''Name("sharteel",Myself)
BeenInParty("sharteel") !InPartyAllowDead(Myself) !AreaCheck("BD0120") !AreaCheck("BD0130")
GlobalGT("chapter","GLOBAL",6) GlobalLT("chapter","GLOBAL",14)'''))
        self.assertNotIn('BD_JOINED', trigger.upper())

    def test_append_preserves_every_original_state_and_localized_text(self):
        before = self.fixture(foreign=True)
        tlk = (self.game / 'lang/en_us/dialog.tlk').read_bytes()
        result = self.repair()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = tree(self.game / 'override')
        self.assertEqual(before.keys(), after.keys())
        self.assertEqual({p for p in before if before[p] != after[p]}, {'BDSHARTE.DLG'})
        self.assertEqual((self.game / 'lang/en_us/dialog.tlk').read_bytes(), tlk)
        self.assert_route()

    def test_second_execution_is_byte_exact_noop(self):
        self.fixture()
        self.assertEqual(self.repair().returncode, 0)
        before = tree(self.game / 'override')
        shutil.copy2(self.game / 'field.tp2', self.game / 'again.tp2')
        result = self.repair('again.tp2')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_external_dialogue_source_and_actual_inparty_aliases(self):
        path = self.game / 'override/trigger.ids'
        path.write_text(path.read_text() + '0x4043 IsValidForPartyDialogue(O:Object*)\n')
        self.fixture()
        shutil.copy2(self.game / 'chriz-sod-remix/dlg/csr110sh.d', self.game / 'owned.d')
        path = self.game / 'field.tp2'
        path.write_text(path.read_text().replace('LAF csr110_sharteel_field_rejoin END',
            'LAF csr110_sharteel_field_rejoin STR_VAR dialogue_source = ~owned.d~ END'))
        self.assertEqual(self.repair().returncode, 0)
        self.assert_route()
        before = tree(self.game / 'override')
        shutil.copy2(path, self.game / 'again.tp2')
        result = self.repair('again.tp2')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_changed_crypt_root_fails_without_writes(self):
        before = self.fixture(bad_root=True)
        self.assertNotEqual(self.repair().returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_changed_join_action_fails_without_writes(self):
        before = self.fixture(bad_join=True)
        self.assertNotEqual(self.repair().returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_changed_wait_action_fails_without_writes(self):
        before = self.fixture(bad_wait=True)
        self.assertNotEqual(self.repair().returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_missing_optional_dialogue_is_noop(self):
        before = tree(self.game / 'override')
        result = self.repair()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_fresh_public_component_110_calls_field_repair(self):
        self.fixture()
        result = self.repair('chriz-sod-remix/setup-chriz-sod-remix.tp2')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assert_route()

    def test_weidu_uninstall_restores_original_dialogue(self):
        before = self.fixture()
        self.assertEqual(self.repair().returncode, 0)
        result = run_weidu(self.game, 'field.tp2', '--force-uninstall-list', '110')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree(self.game / 'override'), before)


if __name__ == '__main__':
    unittest.main()
