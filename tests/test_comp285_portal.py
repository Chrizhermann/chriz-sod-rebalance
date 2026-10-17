"""Real WeiDU checks for the one-way portal; only disposable games are written."""
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'research/scripts'))
from test_comp291_installer import ROOT, WEIDU, compact, tree, write_fake_game

FOREIGN = '''IF
  Global("FOREIGN_PORTAL","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_PORTAL","GLOBAL",7)
    Continue()
END
'''
GATHER = '''IF
  Opened([PC])
  !Range(Player1,25)
THEN
  RESPONSE #100
    DisplayStringNoName(Player1,0)
END
'''
ACTIVATION = '''IF
  Global("bd_hellevator","global",0)
  OR(2)
    Opened([PC])
    Closed([PC])
THEN
  RESPONSE #100
    StartCutSceneMode()
    ClearAllActions()
    SetGlobal("bd_hellevator","global",1)
    StartCutSceneEx("bdcut55",FALSE)
END
'''
ARRIVAL = '''IF
  True()
THEN
  RESPONSE #100
''' + ''.join(f'    ActionOverride(Player{i},LeaveAreaLUA("bd4700","",[1200.900],0))\n'
              for i in range(2, 7)) + '''    LeaveAreaLUAPanic("bd4700","",[1285.870],0)
    LeaveAreaLUA("bd4700","",[1285.870],0)
    StartCutSceneEx("bdcut57",FALSE)
END
'''
AREA_ENTRY = '''IF
  GlobalLT("bd_plot","global",560)
THEN
  RESPONSE #100
    SetGlobal("bd_plot","global",560)
    StartCutSceneEx("bdcut57",FALSE)
END
'''


def area():
    doors = 0xf4
    notes = doors + 2 * 0xc8
    data = bytearray(notes + 2 * 0x34)
    data[:8] = b'AREAV1.0'
    struct.pack_into('<II', data, 0xa4, 2, doors)
    struct.pack_into('<II', data, 0xc4, notes, 2)
    for i, script in enumerate((b'FOREIGN', b'BDELEV01')):
        p = doors + i * 0xc8
        data[p:p+0xc8] = bytes([0x40+i]) * 0xc8
        data[p+0x80:p+0x88] = script.ljust(8, b'\0')
        struct.pack_into('<HH', data, p+0x74, 1354, 1114)
    struct.pack_into('<HHI', data, notes, 100, 200, 0)
    struct.pack_into('<HHI', data, notes+0x34, 1340, 1150, 0)
    return bytes(data)


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class PortalInstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='csr285-portal-')
        self.addCleanup(self.temp.cleanup)
        self.game = Path(self.temp.name)
        write_fake_game(self.game)
        self.override = self.game / 'override'
        additions = {
            'action': '''120 StartCutSceneEx(S:CutScene*,I:Evaluate*BOOLEAN)
133 ClearAllActions()
63 Wait(I:Time*)
272 CreateVisualEffect(S:Object*,P:Location*)
191 LeaveAreaLUA(S:Area*,S:Parchment*,P:Location*,I:Direction*)
267 LeaveAreaLUAPanic(S:Area*,S:Parchment*,P:Location*,I:Direction*)
''',
            'trigger': '''0x0052 Opened(O:Object*)
0x0053 Closed(O:Object*)
0x4018 Range(O:Object*,I:Range*)
0x4034 GlobalLT(S:Name*,S:Area*,I:Value*)
''',
            'object': ''.join(f'{20+i} Player{i}\n' for i in range(2, 7)),
            'ea': '2 PC\n',
        }
        for name, lines in additions.items():
            path = self.override / (name+'.ids')
            path.write_text(path.read_text()+lines)
        (self.override/'bd4600.are').write_bytes(area())
        (self.override/'ddoorh.vvc').write_bytes(b'PORTAL VFX SENTINEL')
        (self.override/'unrelated.itm').write_bytes(b'FOREIGN ITEM SENTINEL')
        (self.game/'fixture').mkdir()
        (self.game/'chriz-sod-remix/lib').mkdir(parents=True)
        shutil.copy2(ROOT/'chriz-sod-remix/lib/comp285_portal.tpa',
                     self.game/'chriz-sod-remix/lib/comp285_portal.tpa')
        (self.game/'fixture/setup-fixture.tp2').write_text('''BACKUP ~fixture/backup~
AUTHOR ~fixture~
BEGIN ~fixtures~
COMPILE ~fixture/bdelev01.baf~ ~fixture/bdcut56.baf~ ~fixture/bd4700.baf~
''')

    def run_weidu(self, *args):
        return subprocess.run([str(WEIDU), *args, '--game', str(self.game),
                               '--use-lang', 'en_US', '--no-exit-pause'],
                              cwd=self.game, capture_output=True, text=True, timeout=45)

    def assert_ok(self, result):
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertNotIn('FATAL ERROR', result.stdout+result.stderr)

    def fixture(self, activation=ACTIVATION, arrival=ARRIVAL):
        for name, text in [('bdelev01', FOREIGN+GATHER+activation),
                           ('bdcut56', arrival), ('bd4700', AREA_ENTRY+FOREIGN)]:
            (self.game/'fixture'/f'{name}.baf').write_text(text)
        self.assert_ok(self.run_weidu('fixture/setup-fixture.tp2', '--force-install-list', '0'))

    def install(self, name='portal'):
        (self.game/f'{name}.tp2').write_text(f'''BACKUP ~{name}-backup~
AUTHOR ~fixture~
BEGIN ~portal~
LOAD_TRA ~portal.tra~
INCLUDE ~chriz-sod-remix/lib/comp285_portal.tpa~
LAF csr285_portal_preflight END
LAF csr285_portal_install END
''')
        (self.game/'portal.tra').write_text('@28501 = ~Portal to the summit~\n')
        return self.run_weidu(f'{name}.tp2', '--force-install-list', '0')

    def decompile(self):
        out = self.game/'decompiled'
        out.mkdir()
        self.assert_ok(self.run_weidu(str(self.override/'bdelev01.bcs'), '--out', str(out)))
        return (out/'bdelev01.baf').read_text()

    def test_preserves_gathering_foreign_logic_and_exact_other_bytes(self):
        self.fixture()
        before = {p.name:p.read_bytes() for p in self.override.iterdir()}
        self.assert_ok(self.install())
        script = compact(self.decompile())
        self.assertTrue(script.startswith(compact(FOREIGN+GATHER)))
        self.assertNotIn('"BDCUT55"', script)
        self.assertEqual(script.count('STARTCUTSCENEEX("BDCUT56",FALSE)'), 1)
        self.assertIn(compact('''SetGlobal("bd_hellevator","global",5)
SetGlobal("bd_plot","global",560)
CreateVisualEffect("DDOORH",[1354.1114])
Wait(1)
StartCutSceneEx("bdcut56",FALSE)'''), script)
        permitted = set(range(0xf4+0xc8+0x58, 0xf4+0xc8+0x68))
        note = 0xf4+2*0xc8+0x34+4
        permitted.update(range(note,note+4))
        after = (self.override/'bd4600.are').read_bytes()
        self.assertEqual(len(after), len(before['bd4600.are']))
        self.assertTrue(all(a==b or i in permitted for i,(a,b) in enumerate(zip(before['bd4600.are'],after))))
        self.assertEqual(after[0xf4+0xc8+0x58:0xf4+0xc8+0x68], bytes(16))
        for name, data in before.items():
            if name not in {'bdelev01.bcs','bd4600.are'}:
                self.assertEqual((self.override/name).read_bytes(), data, name)
        patched = tree(self.override)
        self.assert_ok(self.install('second'))
        self.assertEqual(tree(self.override), patched)

    def test_changed_activation_fails_before_any_resource_write(self):
        self.fixture(activation=ACTIVATION.replace('"bdcut55"','"foreign"'))
        before = tree(self.override)
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unsupported downstairs activation', result.stdout+result.stderr)
        self.assertEqual(tree(self.override), before)

    def test_second_confrontation_handoff_fails_before_any_resource_write(self):
        self.fixture(arrival=ARRIVAL.replace('    StartCutSceneEx', '    StartCutSceneEx("bdcut57",FALSE)\n    StartCutSceneEx'))
        before = tree(self.override)
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('upper-arrival cutscene', result.stdout+result.stderr)
        self.assertEqual(tree(self.override), before)


if __name__ == '__main__':
    unittest.main()
