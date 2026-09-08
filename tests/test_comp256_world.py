"""Compile/install the real bridge seam patches in disposable synthetic games."""
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

ROSTER = '\n'.join(f'    CreateCreature("{ref}",[{x}.{y}],{face})' for ref, x, y, face in [
    ('bdcrubbm',1465,1910,'SE'), ('bdcrubb1',1605,1900,'S'),
    ('bdcrubb1',1540,1935,'SE'), ('bdcrubb1',1480,1985,'SE'),
    ('bdcrubb1',1430,2030,'E'), ('bdcrubb2',1530,1865,'S'),
    ('bdcrubb2',1400,1960,'E')])
BODY = '''THEN
  RESPONSE #100
    SetGlobal("bd_plot","global",293)
    CreateCreature("bdbence",[2425.2660],NW)
    ActionOverride("khalid",SaveLocation("LOCALS","bd_default_loc",[2425.2485]))
    ActionOverride("khalid",SetGlobal("bd_no_retreat","locals",0))
    ActionOverride("khalid",SetGlobal("bd_retreat","locals",1))
    AddJournalEntry(123,QUEST)
    SetGlobal("bd_cant_rest","myarea",0)
    SetGlobalTimer("BD_NPC_BANTER","GLOBAL",FIVE_ROUNDS)
END
'''
SCRIPT = ''.join(f'''IF
  Global("NATIVE_ROUTE","GLOBAL",{route})
THEN
  RESPONSE #100
    SetGlobal("NATIVE_PRESERVED_{route}","GLOBAL",1)
{ROSTER}
    SetGlobal("bd_bridge_plot","bd2000",2)
END
''' for route in (1,2)) + '''IF
  GlobalLT("bd_plot","global",293)
  OR(2)
    GlobalGT("bd_elemental","bd2000",0)
    Global("bdsumfir","global",3)
  OR(2)
    Dead("bdelefir")
    Global("bdsumfir","global",3)
''' + BODY + '''IF
  GlobalLT("bd_plot","global",293)
  Global("bd_elemental","bd2000",0)
  Global("bdsumfir","global",0)
  !NumDeadLT("bdcrubb",6)
  Dead("bdcrubbm")
''' + BODY + '''IF
  True()
THEN
  RESPONSE #100
    AddMapNoteColor([1384.1862],987,RED)
    SetGlobal("FOREIGN_TAIL","GLOBAL",7)
END
'''

ANIMATIONS = ['Barrel_ignited_1','Barrel_ignited_2','Barrel_ignited_3',
              'Fire_portal_1','Fire_portal_1a','Fire_portal_1b','Fire_portal_1c',
              'Big_explosion','Foreign_animation']

def area():
    data = bytearray(0xf4)
    data[:8] = b'AREAV1.0'
    tables = [(0x54,0x58,2,0x110,5), (0x5c,0x5a,2,0xc4,2),
              (0xb0,0xac,4,0x4c,9), (0x84,0x82,2,0xd4,2)]
    offsets=[]
    for off,count,width,stride,n in tables:
        offsets.append(len(data))
        struct.pack_into('<I',data,off,len(data))
        struct.pack_into('<H' if width==2 else '<I',data,count,n)
        data.extend(b'\x55'*(stride*n))
    def name(offset,text,length): data[offset:offset+length]=text.encode().ljust(length,b'\0')
    for i,(x,y) in enumerate([(1328,1947),(1329,1897),(1475,1836),(1540,1820),(1,2)]):
        b=offsets[0]+i*0x110
        name(b,'BD_BARREL_HE' if i<4 else 'Foreign_actor',32)
        name(b+0x80,'BDKEGX' if i<4 else 'FOREIGN',8)
        struct.pack_into('<HH',data,b+0x20,x,y)
        struct.pack_into('<I',data,b+0x28,1)
        struct.pack_into('<I',data,b+0x40,0xffffff)
    for i in range(2):
        b=offsets[1]+i*0xc4
        name(b,'Barrel_spot' if i==0 else 'Foreign_region',32)
        name(b+0x7c,'BDBOARB2' if i==0 else 'FOREIGN',8)
    for i,entry in enumerate(ANIMATIONS): name(offsets[2]+i*0x4c,entry,32)
    name(offsets[3],'Amb_fire_portal_1',32)
    name(offsets[3]+0xd4,'Foreign_ambient',32)
    return bytes(data)+b'UNRELATED AREA PAYLOAD'

@unittest.skipUnless(WEIDU.is_file(),'real WeiDU unavailable; set WEIDU_EXE')
class BridgeWorldTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(prefix='csr256-world-')
        self.addCleanup(tmp.cleanup)
        self.game=Path(tmp.name)
        write_fake_game(self.game)
        self.override=self.game/'override'
        ids={
          'action': '''0 NoAction()
7 CreateCreature(S:NewObject*,P:Location*,I:Face*DIR)
115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)
173 AddJournalEntry(I:Entry*,I:Type*JourType)
244 SaveLocation(S:Area*,S:Global*,P:Point*)
308 AddMapNoteColor(P:Position*,I:StringRef*,I:Color*Mapnotes)
''', 'trigger': '''0x4034 GlobalGT(S:Name*,S:Area*,I:Value*)
0x4035 GlobalLT(S:Name*,S:Area*,I:Value*)
0x4037 StateCheck(O:Object*,I:State*State)
0x4051 Dead(S:Name*)
0x4073 NumDeadLT(S:Name*,I:Num*)
0x40D0 Difficulty(I:Amount*DIFFLEV)
0x40D1 DifficultyGT(I:Amount*DIFFLEV)
0x40D2 DifficultyLT(I:Amount*DIFFLEV)
''', 'dir':'0 S\n14 SE\n12 E\n6 NW\n', 'jourtype':'1 QUEST\n',
          'gtimes':'30 FIVE_ROUNDS\n', 'mapnotes':'0 RED\n',
          'state':'128 STATE_STONE_DEATH\n',
          'difflev':'1 EASIEST\n2 EASY\n3 NORMAL\n4 HARD\n5 HARDEST\n'}
        for name,text in ids.items():
            p=self.override/(name+'.ids')
            p.write_text((p.read_text() if p.exists() else 'IDS V1.0\n')+text)
        lib=self.game/'chriz-sod-remix/lib'
        lib.mkdir(parents=True)
        shutil.copy2(ROOT/'chriz-sod-remix/lib/comp256_world.tpa',lib)
        (self.game/'fixture').mkdir()
        (self.game/'fixture/setup-fixture.tp2').write_text('BACKUP ~fixture/backup~\nAUTHOR ~test~\nBEGIN ~source~\nCOMPILE ~fixture/bd2000.baf~\n')
        (self.game/'world.tp2').write_text('''BACKUP ~world-backup~
AUTHOR ~test~
BEGIN ~production world patch~ DESIGNATED 256
OUTER_SET csr256_warning = 123
INCLUDE ~chriz-sod-remix/lib/comp256_world.tpa~
LAF csr256_world_preflight END
LAF csr256_world_install END
''')
        (self.override/'bd2000.are').write_bytes(area())

    def weidu(self,*args):
        return subprocess.run([str(WEIDU),*map(str,args),'--game',str(self.game),
            '--use-lang','en_US','--language','0','--no-exit-pause'],cwd=self.game,
            text=True,capture_output=True,encoding='utf-8',errors='replace',timeout=60)

    def fixture(self,script=SCRIPT):
        (self.game/'fixture/bd2000.baf').write_text(script)
        result=self.weidu('fixture/setup-fixture.tp2','--force-install-list','0')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def install(self): return self.weidu('world.tp2','--force-install-list','256')

    def decompile(self):
        result=self.weidu(self.override/'bd2000.bcs')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        return (self.game/'bd2000.baf').read_text()

    def test_both_routes_one_full_roster_and_preserved_aftermath(self):
        self.fixture()
        result=self.install()
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        script=compact(self.decompile())
        self.assertEqual(script.count('SETGLOBAL("CSR256_REQUEST","BD2000",1)'),2)
        self.assertEqual(script.count('CREATECREATURE("BDBENCE"'),1)
        for route in (1,2): self.assertIn(f'SETGLOBAL("NATIVE_PRESERVED_{route}","GLOBAL",1)',script)
        self.assertIn('SETGLOBAL("FOREIGN_TAIL","GLOBAL",7)',script)
        self.assertIn('ADDJOURNALENTRY(123,QUEST)',script)
        self.assertIn('SETGLOBAL("BD_CANT_REST","MYAREA",0)',script)
        for old in ('BDCRUBBM','BDSUMFIR','BD_ELEMENTAL','ADDMAPNOTECOLOR'):
            self.assertNotIn(old,script)
        for dv in ('FM','CM','G1','G2','E1','E2','F1','F2'):
            self.assertIn(f'!EXISTS("CSR256{dv}")',script)
        blocks=re.findall(r'IF\s+(.*?)\s+THEN\s+RESPONSE #100\s+(.*?)\s+END',self.decompile(),re.S)
        spawns=[(guard,actions) for guard,actions in blocks if 'CSR256_REQUEST' in guard]
        self.assertEqual(len(spawns),4)
        for guard,actions in spawns:
            self.assertIn('CSR256_STAGE',guard)
            self.assertEqual(actions.count('CreateCreature('),8)
        self.assertEqual(script.count('CREATECREATURE("CSR26E1G"'),2)
        self.assertEqual(script.count('CREATECREATURE("CSR26F1G"'),1)

    def test_area_preserves_every_other_byte_including_retreat_destination(self):
        self.fixture()
        before=area()
        result=self.install()
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        after=(self.override/'bd2000.are').read_bytes()
        expected=bytearray(before)
        ao=struct.unpack_from('<I',before,0x54)[0]
        for i in range(4): struct.pack_into('<I',expected,ao+i*0x110+0x40,0)
        ro=struct.unpack_from('<I',before,0x5c)[0]
        expected[ro+0x7c:ro+0x84]=b'\0'*8
        an=struct.unpack_from('<I',before,0xb0)[0]
        for i in range(8):
            struct.pack_into('<I',expected,an+i*0x4c+0x24,0)
            struct.pack_into('<I',expected,an+i*0x4c+0x34,0x55555554)
        am=struct.unpack_from('<I',before,0x84)[0]
        struct.pack_into('<I',expected,am+0x8c,0)
        struct.pack_into('<I',expected,am+0x90,0x55555554)
        self.assertEqual(after,bytes(expected))

    def test_native_skie_aftermath_survives_when_not_removed_by_another_component(self):
        self.fixture(SCRIPT.replace('    CreateCreature("bdbence",[2425.2660],NW)',
            '    CreateCreature("bdbence",[2425.2660],NW)\n    CreateCreature("bdskie",[2485.2655],NW)'))
        result=self.install()
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        text=compact(self.decompile())
        self.assertEqual(text.count('CREATECREATURE("BDSKIE",[2485.2655],NW)'),1)
        self.assertEqual(text.count('CREATECREATURE("BDBENCE"'),1)

    def test_changed_roster_fails_before_any_override_write(self):
        self.fixture(SCRIPT.replace('[1465.1910]','[1466.1910]',1))
        before=tree(self.override)
        self.assertNotEqual(self.install().returncode,0)
        self.assertEqual(tree(self.override),before)

    def test_changed_aftermath_fails_before_any_override_write(self):
        self.fixture(SCRIPT.replace('    AddJournalEntry(123,QUEST)','    NoAction()\n    AddJournalEntry(123,QUEST)',1))
        before=tree(self.override)
        self.assertNotEqual(self.install().returncode,0)
        self.assertEqual(tree(self.override),before)

    def test_late_area_mismatch_fails_before_script_write(self):
        self.fixture()
        (self.override/'bd2000.are').write_bytes(area().replace(b'BDBOARB2',b'FOREIGNX'))
        before=tree(self.override)
        self.assertNotEqual(self.install().returncode,0)
        self.assertEqual(tree(self.override),before)

if __name__=='__main__': unittest.main()
