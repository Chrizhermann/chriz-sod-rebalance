"""The single pool omen and its reward survive changed or missing source data."""
from pathlib import Path
import struct
import unittest
from test_comp285_installer import InstallerFixture, WEIDU
from test_comp265_installer import area, item, containers

IDS = {'action': '30 SetGlobal(S:Name*,S:Area*,I:Value*)\n'
           '83 SmallWait(I:Time*)\n'
           '116 TakePartyItem(S:Item*)\n'
           '164 AddexperienceParty(I:XP*)\n'
           '198 StartDialogNoSet(O:Object*)\n'
           '204 TakePartyItemNum(S:ResRef*,I:Num*)\n'
           '259 AddXPObject(O:Object*,I:XP*)\n'
           '272 CreateVisualEffect(S:Object*,P:Location*)\n'
           '301 AmbientActivate(O:Object*,I:State*BOOLEAN)\n'
           '346 DisplayStringNoNameHead(O:Object*,I:StrRef*)\n',
 'object': '21 Player1\n'
           '22 Player2\n'
           '23 Player3\n'
           '24 Player4\n'
           '25 Player5\n'
           '26 Player6\n'
           '17 LastTrigger\n',
 'trigger': '0x0070 Clicked(O:Object*)\n'
            '0x400F Global(S:Name*,S:Area*,I:Value*)\n'
            '0x4018 Range(O:Object*,I:Range*)\n'
            '0x407B NumItemsPartyGT(S:ResRef*,I:Num*)\n'
            '0x407C NumItemsPartyLT(S:ResRef*,I:Num*)\n'}
FOREIGN = 'IF Global("FOREIGN","GLOBAL",0) THEN RESPONSE #100 SetGlobal("FOREIGN","GLOBAL",1) Continue() END\n'
PUZZLE = 'IF Global("BD_SDDD12_COUNTER","MYAREA",3) Global("PUZZLE_DONE","MYAREA",0) THEN RESPONSE #100 SetGlobal("PUZZLE_DONE","MYAREA",1) SetGlobal("BD_SDDD12_CLOUDY","MYAREA",1) AddexperienceParty(3000) END\n'
LEGACY = 'IF Global("BD_SDDD12_CLOUDY","MYAREA",1) THEN RESPONSE #100 TakePartyItem("BDMISC59") ActionOverride("BDSCRY",StartDialogNoSet(LastTrigger)) END\n'

@unittest.skipUnless(WEIDU.is_file(), 'set WEIDU_EXE')
class PoolTests(InstallerFixture):
    def setUp(self):
        super().setUp()
        for name, definitions in IDS.items():
            path = self.override/(name+'.ids')
            before = path.read_text() if path.is_file() else 'IDS V1.0\n'
            path.write_text(before+definitions)
        raw = bytearray(area(target_items=[item('BDMISC55')]))
        co = struct.unpack_from('<I', raw, 0x70)[0]
        target = co+0xc0
        raw[target:target+32] = b'Sarcophagus01'.ljust(32,b'\0')
        for offset, size in ((0x26,2),(0x28,4),(0x30,2),(0x48,8),(0x78,8)):
            raw[target+offset:target+offset+size]=bytes(size)
        ao=struct.unpack_from('<I',raw,0x54)[0]
        raw[ao:ao+32]=b'IMBUED_WIGHT_POTION'.ljust(32,b'\0')
        raw[ao+0x80:ao+0x88]=b'BDWIGHDD'
        (self.override/'bd1200.are').write_bytes(raw)
        (self.game/'fixture').mkdir()
        (self.game/'fixture/bdodscry.baf').write_text(FOREIGN+PUZZLE+LEGACY)
        (self.game/'seed.tp2').write_text('BACKUP ~seed-backup~ AUTHOR ~test~ BEGIN ~seed~ COMPILE ~fixture/bdodscry.baf~')
        self.assert_success(self.run_weidu('seed.tp2','--force-install-list','0'))
        (self.game/'pool.tp2').write_text('BACKUP ~pool-backup~ AUTHOR ~test~ BEGIN ~pool~ INCLUDE ~chriz-sod-remix/lib/bdscry_compat.tpa~ INCLUDE ~chriz-sod-remix/lib/comp225.tpa~')

    def apply(self):
        self.assert_success(self.run_weidu('pool.tp2','--force-install-list','0'))
        source=self.decompile('bdodscry.bcs')
        self.assertEqual(source.count('AddXPObject(Player1,1000)'),1)
        self.assertNotIn('TakePartyItem("BDMISC59")',source)
        target=containers((self.override/'bd1200.are').read_bytes())['Sarcophagus01']
        self.assertEqual(sum(x[:8].rstrip(b'\0')==b'BDMISC55' for x in target),1)
        self.assertEqual(sum(x[:8].rstrip(b'\0')==b'BDMISC59' for x in target),1)
        return source

    def test_normal_preserves_puzzle_reward_and_item_metadata(self):
        before=(self.override/'bd1200.are').read_bytes()
        source=self.apply()
        self.assertIn('AddexperienceParty(3000)',source)
        self.assertIn('"FOREIGN"',source)
        after=(self.override/'bd1200.are').read_bytes()
        target=containers(after)['Sarcophagus01']
        self.assertEqual(target,[item('BDMISC55'),b'BDMISC59'+bytes(12)])
        original=containers(before)
        self.assertEqual({k:v for k,v in containers(after).items() if k!='Sarcophagus01'},
                         {k:v for k,v in original.items() if k!='Sarcophagus01'})

    def test_other_contents_and_missing_scepter_get_owned_rewards(self):
        raw=bytearray((self.override/'bd1200.are').read_bytes())
        co=struct.unpack_from('<I',raw,0x70)[0];io=struct.unpack_from('<I',raw,0x78)[0]
        first=struct.unpack_from('<I',raw,co+0xc0+0x40)[0]
        raw[io+first*20:io+(first+1)*20]=item('FOREIGN',9)
        (self.override/'bd1200.are').write_bytes(raw)
        self.apply()
        self.assertIn(item('FOREIGN',9),containers((self.override/'bd1200.are').read_bytes())['Sarcophagus01'])

    def test_moved_locked_target_and_actor_build_are_overwritten(self):
        raw=bytearray((self.override/'bd1200.are').read_bytes())
        co=struct.unpack_from('<I',raw,0x70)[0];at=co+0xc0
        struct.pack_into('<HHHHI',raw,at+0x20,1,2,8,70,1)
        struct.pack_into('<H',raw,at+0x30,1)
        raw[at+0x48:at+0x50]=b'FOREIGN!'
        raw[at+0x78:at+0x80]=b'KEY12345'
        ao=struct.unpack_from('<I',raw,0x54)[0]
        raw[ao+0x80:ao+0x88]=b'OTHERCRE'
        struct.pack_into('<I',raw,ao+0x40,0xffffff)
        (self.override/'bd1200.are').write_bytes(raw)
        self.apply()
        after=(self.override/'bd1200.are').read_bytes()
        self.assertEqual(struct.unpack_from('<I',after,ao+0x40)[0],0)
        for off,size in ((0x26,2),(0x28,4),(0x30,2),(0x48,8),(0x78,8)):
            self.assertEqual(after[at+off:at+off+size],bytes(size))

    def test_missing_container_and_object_script_are_created(self):
        raw=bytearray((self.override/'bd1200.are').read_bytes())
        co=struct.unpack_from('<I',raw,0x70)[0]
        raw[co+0xc0:co+0xc0+32]=b'ForeignChest'.ljust(32,b'\0')
        (self.override/'bd1200.are').write_bytes(raw)
        (self.override/'bdodscry.bcs').unlink()
        self.apply()
        after=(self.override/'bd1200.are').read_bytes()
        self.assertIn('ForeignChest',containers(after))
        self.assertEqual(struct.unpack_from('<H',after,0x80)[0],20)

    def test_second_tail_is_byte_identical(self):
        self.apply()
        before={n:(self.override/n).read_bytes() for n in ('bd1200.are','bdodscry.bcs')}
        (self.game/'second.tp2').write_text((self.game/'pool.tp2').read_text().replace('pool-backup','second-backup'))
        self.assert_success(self.run_weidu('second.tp2','--force-install-list','0'))
        for name,data in before.items(): self.assertEqual((self.override/name).read_bytes(),data,name)

    def test_damaged_area_only_leaves_that_resource_unchanged(self):
        (self.override/'bd1200.are').write_bytes(b'AREAV1.0')
        self.assert_success(self.run_weidu('pool.tp2','--force-install-list','0'))
        self.assertEqual((self.override/'bd1200.are').read_bytes(),b'AREAV1.0')
        self.assertIn('AddXPObject(Player1,1000)',self.decompile('bdodscry.bcs'))
