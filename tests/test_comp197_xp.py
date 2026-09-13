"""Native join-XP floors from real compiled Skie scripts; no engine timing claim.

All writes use disposable synthetic games. The small decision runner evaluates
the compiled/decompiled conditions and actions, rather than a second XP policy.
"""
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'research/scripts'))
from test_comp291_installer import ROOT, WEIDU, write_fake_game, tree, compact


ACTION_IDS = '''IDS V1.0
30 SetGlobal(S:Name*,S:Area*,I:Value*)
36 Continue()
86 SetInterrupt(I:State*BOOLEAN)
370 ChangeStat(O:Object*,I:Stat*STATS,I:Value*,I:Modifier*STATMOD)
'''
TRIGGER_IDS = '''IDS V1.0
0x400F Global(S:Name*,S:Area*,I:Value*)
0x4023 True()
0x4043 IsValidForPartyDialogue(O:Object*)
0x40C4 XPGT(O:Object*,I:XP*)
0x40C5 XPLT(O:Object*,I:XP*)
'''
FOREIGN = '''IF Global("FOREIGN_SKIE","LOCALS",0) THEN RESPONSE #100
SetGlobal("FOREIGN_SKIE","LOCALS",1) Continue() END
'''


def run_weidu(game, *args):
    return subprocess.run([str(WEIDU), *args, '--game', str(game), '--use-lang',
                           'en_US', '--language', '0', '--no-exit-pause'],
                          cwd=game, capture_output=True, text=True, encoding='utf-8',
                          errors='replace', timeout=60)


def write_skie_xp_fixture(game):
    """Reusable minimal game; callers may extend IDS and compile extra dialogs."""
    write_fake_game(game)
    for name, content in {
        'action': ACTION_IDS, 'trigger': TRIGGER_IDS,
        'stats': 'IDS V1.0\n44 XP\n', 'statmod': 'IDS V1.0\n1 ADD\n2 SET\n',
    }.items():
        (game / 'override' / f'{name}.ids').write_text(content, encoding='ascii')
    shutil.copytree(ROOT / 'chriz-sod-remix', game / 'chriz-sod-remix')
    (game / 'fixture').mkdir()
    for name in ('bdskie', 'skie'):
        (game / 'fixture' / f'{name}.baf').write_text(FOREIGN, encoding='ascii')
        cre = bytearray(0x2D4)
        cre[:8] = b'CRE V1.0'
        struct.pack_into('<I', cre, 0x18, 64000 if name == 'bdskie' else 400000)
        struct.pack_into('<I', cre, 0x244, 0x400c0000)
        cre[0x273] = 4
        cre[0x248:0x250] = name.encode().ljust(8, b'\0')
        (game / 'override' / f'{name}.cre').write_bytes(cre)
    (game / 'fixture/setup-fixture.tp2').write_text('''BACKUP ~fixture-backup~
AUTHOR ~test~ BEGIN ~fixture~
COMPILE ~fixture/bdskie.baf~ ~fixture/skie.baf~
''', encoding='ascii')
    (game / 'xp.tp2').write_text('''BACKUP ~xp-backup~ AUTHOR ~test~
BEGIN ~Skie native XP floors~ DESIGNATED 197
INCLUDE ~chriz-sod-remix/lib/comp197_xp.tpa~
LAF csr197_install_xp END
''', encoding='ascii')


def decompile(game, name):
    destination = game / 'decompiled'
    destination.mkdir(exist_ok=True)
    result = run_weidu(game, str(game / 'override' / name.lower()), '--out',
                       str(destination), '--log', str(destination / 'audit.log'))
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    suffix = '.d' if name.upper().endswith('.DLG') else '.baf'
    matches = [p for p in destination.iterdir()
               if p.name.lower() == Path(name).stem.lower() + suffix]
    return matches[0].read_text(encoding='utf-8', errors='replace')


def run_ladder(source, player_xp, xp, *, valid=True, safehouse=1, locals_=None,
               passes=12):
    """Limited BAF evaluator; unknown conditions/actions fail the test."""
    blocks = re.findall(r'\bIF\s+(.*?)\s+THEN\s+RESPONSE\s+#100\s+(.*?)\s+END',
                        source, flags=re.S | re.I)
    values = dict(locals_ or {})
    values[('BD_SAFEHOUSE_DONE', 'GLOBAL')] = safehouse
    awards = []
    for _ in range(passes):
        for conditions, actions in blocks:
            matches = []
            for line in conditions.splitlines():
                line = line.split('//', 1)[0].strip()
                if not line:
                    continue
                m = re.fullmatch(r'Global\("([^"]+)","([^"]+)",(\d+)\)', line, re.I)
                x = re.fullmatch(r'XP(GT|LT)\((Myself|Player1),(\d+)\)', line, re.I)
                if m:
                    name, scope, number = m.groups()
                    matches.append(values.get((name.upper(), scope.upper()), 0) == int(number))
                elif x:
                    comparison, who, number = x.groups()
                    value = xp if who.upper() == 'MYSELF' else player_xp
                    matches.append(value > int(number) if comparison.upper() == 'GT'
                                   else value < int(number))
                elif line.upper() == 'ISVALIDFORPARTYDIALOGUE(MYSELF)':
                    matches.append(valid)
                else:
                    raise AssertionError('unknown condition: ' + line)
            if not all(matches):
                continue
            for line in actions.splitlines():
                line = line.split('//', 1)[0].strip()
                if not line:
                    continue
                m = re.fullmatch(r'SetGlobal\("([^"]+)","([^"]+)",(\d+)\)', line, re.I)
                x = re.fullmatch(r'ChangeStat\(Myself,XP,(\d+),SET\)', line, re.I)
                if m:
                    name, scope, number = m.groups()
                    values[(name.upper(), scope.upper())] = int(number)
                elif x:
                    xp = int(x.group(1))
                    awards.append(xp)
                elif line.upper() not in ('SETINTERRUPT(FALSE)', 'SETINTERRUPT(TRUE)', 'CONTINUE()'):
                    raise AssertionError('unknown action: ' + line)
            break
    return xp, awards, values


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class SkieXPTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix='csr197-xp-')
        self.addCleanup(tmp.cleanup)
        self.game = Path(tmp.name)
        write_skie_xp_fixture(self.game)
        result = run_weidu(self.game, 'fixture/setup-fixture.tp2', '--force-install-list', '0')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.before = tree(self.game / 'override')
        result = run_weidu(self.game, 'xp.tp2', '--force-install-list', '197')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.script = decompile(self.game, 'bdskie.bcs')

    def test_reported_saved_join_and_repeat_ticks(self):
        xp, awards, state = run_ladder(self.script, 422163, 64000)
        self.assertEqual((xp, awards), (250000, [250000]))
        self.assertEqual(state[('BD_JOINXP', 'LOCALS')], 0)  # native safehouse re-arm
        self.assertEqual(state[('BDSODXP', 'LOCALS')], 1)
        self.assertEqual(run_ladder(self.script, 422163, xp, locals_=state)[1], [])

    def test_native_threshold_boundaries(self):
        for player, expected in ((89999, 64000), (90000, 90000), (109999, 90000),
                                 (110000, 110000), (134999, 110000), (135000, 135000),
                                 (160999, 135000), (161000, 161000), (199999, 161000),
                                 (200000, 200000), (249999, 200000), (250000, 250000),
                                 (500000, 250000)):
            with self.subTest(player=player):
                self.assertEqual(run_ladder(self.script, player, 64000)[0], expected)

    def test_existing_higher_xp_is_never_lowered(self):
        for player, xp in ((422163, 400000), (161000, 250000), (422163, 250000)):
            self.assertEqual(run_ladder(self.script, player, xp)[:2], (xp, []))

    def test_catchup_waits_for_valid_party_member(self):
        self.assertEqual(run_ladder(self.script, 422163, 64000, valid=False)[:2], (64000, []))

    def test_native_safehouse_second_opportunity(self):
        xp, awards, state = run_ladder(self.script, 161000, 64000, safehouse=0)
        self.assertEqual((xp, awards), (161000, [161000]))
        self.assertEqual(run_ladder(self.script, 422163, xp, safehouse=0, locals_=state)[:2],
                         (161000, []))
        self.assertEqual(run_ladder(self.script, 422163, xp, safehouse=1, locals_=state)[:2],
                         (250000, [250000]))

    def test_only_existing_bdskie_script_changes_and_uninstall_restores_it(self):
        after = tree(self.game / 'override')
        self.assertEqual(after.keys(), self.before.keys())
        self.assertEqual({name for name in after if after[name] != self.before[name]}, {'BDSKIE.BCS'})
        self.assertTrue(compact(self.script).endswith(compact(FOREIGN)))
        self.assertEqual(self.script.upper().count('GLOBAL("FOREIGN_SKIE"'), 2)
        result = run_weidu(self.game, 'xp.tp2', '--force-uninstall-list', '197')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree(self.game / 'override'), self.before)

    def test_component_197_wires_the_installer(self):
        source = (ROOT / 'chriz-sod-remix/lib/comp197.tpa').read_text()
        self.assertEqual(source.count('LAF csr197_install_xp END'), 1)


if __name__ == '__main__':
    unittest.main()
