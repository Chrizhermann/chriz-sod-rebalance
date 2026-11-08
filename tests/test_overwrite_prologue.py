"""Copied-resource coverage for the prologue and authored chapter awards."""
import os
import re
from pathlib import Path
import shutil
import struct
import unittest
from test_comp285_installer import EffectiveResources, InstallerFixture, WEIDU

SOURCE=os.environ.get('CSR198_SOURCE_GAME')

@unittest.skipUnless(WEIDU.is_file() and SOURCE, 'set CSR198_SOURCE_GAME for copied-resource fixtures')
class AuthoredPrologueTests(InstallerFixture):
    def setUp(self):
        super().setUp()
        self.source=Path(SOURCE)
        self.resources=EffectiveResources(self.source)
        self.resources.copy_ids(self.override)
        shutil.copyfile(self.source/'lang/en_us/dialog.tlk',self.game/'lang/en_us/dialog.tlk')

    def seed(self,component,names):
        for name in names.split():
            backup=self.source/f'weidu_external/backup/chriz-sod-remix/{component}'/name
            raw=backup.read_bytes() if backup.is_file() else self.resources.read(name)
            (self.override/name).write_bytes(raw)

    def apply(self,component,body=None,second=False):
        name='second' if second else 'apply'
        if body is None: body=f'INCLUDE ~chriz-sod-remix/lib/comp{component}.tpa~'
        (self.game/(name+'.tp2')).write_text(f'BACKUP ~{name}-backup~ AUTHOR ~fixture~ BEGIN ~component {component}~\n'+body,encoding='utf-8')
        self.assert_success(self.run_weidu(name+'.tp2','--force-install-list','0'))

    def test_100_native_chances_and_changed_fields_have_identical_owned_output(self):
        import json
        chances=json.loads((self.game/'chriz-sod-remix/data/rest-chances.json').read_text(encoding='utf-8'))
        self.seed(100,' '.join(name+'.are' for name in chances))
        before={name:(self.override/(name+'.are')).read_bytes() for name in chances}
        self.apply(100)
        for name,fields in chances.items():
            expected=bytearray(before[name]);off=struct.unpack_from('<I',expected,0xc0)[0]
            struct.pack_into('<HH',expected,off+0xa8,fields['day'],fields['night'])
            self.assertEqual(expected,(self.override/(name+'.are')).read_bytes(),name)
        changed={}
        for name in chances:
            p=self.override/(name+'.are');raw=bytearray(p.read_bytes());off=struct.unpack_from('<I',raw,0xc0)[0]
            struct.pack_into('<H',raw,off+0x98,0)
            struct.pack_into('<HHHH',raw,off+0xa4,0,0,0,65535)
            p.write_bytes(raw);changed[name]=raw
        self.apply(100,second=True)
        for name,fields in chances.items():
            expected=changed[name];off=struct.unpack_from('<I',expected,0xc0)[0]
            struct.pack_into('<HH',expected,off+0xa8,fields['day'],fields['night'])
            self.assertEqual(expected,(self.override/(name+'.are')).read_bytes(),name)

    def test_100_missing_rest_record_is_created_once(self):
        self.seed(100,'bd0120.are')
        p=self.override/'bd0120.are';raw=bytearray(p.read_bytes());struct.pack_into('<I',raw,0xc0,0);p.write_bytes(raw)
        self.apply(100)
        first=p.read_bytes();off=struct.unpack_from('<I',first,0xc0)[0]
        self.assertEqual(struct.unpack_from('<HH',first,off+0xa8),(1,1))
        self.assertEqual(len(first),len(raw)+0xe4)
        self.apply(100,second=True)
        self.assertEqual(first,p.read_bytes())

    def test_110_missing_palace_and_recruitment_scripts_are_written(self):
        (self.override/'bd0120.are').write_bytes(b'AREAV1.0')
        self.assert_success(self.run_weidu('chriz-sod-remix/setup-chriz-sod-remix.tp2','--force-install-list','110'))
        self.assertIn('SetGlobal("BD_SPAWN_SAFANA","BD0110",2)',self.decompile('bd0110.bcs'))
        first={n:(self.override/n).read_bytes() for n in ('bd0110.bcs','bd2000.bcs','bd2100.bcs')}
        self.apply(110,body='INCLUDE ~chriz-sod-remix/lib/overwrite.tpa~\nINCLUDE ~chriz-sod-remix/lib/comp110_sites.tpa~',second=True)
        for n,data in first.items():self.assertEqual(data,(self.override/n).read_bytes(),n)

    def test_120_normal_exits_and_second_tail(self):
        from test_khalid_continuity_installer import dialog_states
        self.seed(120, 'bd0103.bcs bdcut10.bcs bdcut28.bcs bd5100.bcs bdimoen.dlg bdscry.dlg')
        body = ('INCLUDE ~chriz-sod-remix/lib/bdscry_compat.tpa~\n'
                'INCLUDE ~chriz-sod-remix/lib/comp120.tpa~')
        self.apply(120, body=body)
        scripts = {n:self.decompile(n) for n in ('bd0103.bcs','bdcut10.bcs','bdcut28.bcs')}
        self.assertNotIn('CreateCreature("bdireni"', scripts['bd0103.bcs'])
        self.assertNotIn('StartCutSceneEx("bdcut11"', scripts['bdcut10.bcs'])
        for n in ('bdcut10.bcs','bdcut28.bcs'):
            self.assertIn('EndCutSceneMode()', scripts[n])
            self.assertNotIn('"bdireni"', scripts[n])
        before = {n:(self.override/n).read_bytes() for n in (*scripts,'bd5100.bcs','bdimoen.dlg')}
        self.assertEqual('false()', dialog_states(before['bdimoen.dlg'])[67].transitions[1].trigger)
        self.apply(120, body=body, second=True)
        for n,raw in before.items(): self.assertEqual(raw,(self.override/n).read_bytes(),n)

    def test_120_missing_scenes_and_dialogue_are_written(self):
        from test_khalid_continuity_installer import dialog_states
        self.apply(120, body=('INCLUDE ~chriz-sod-remix/lib/bdscry_compat.tpa~\n'
                             'INCLUDE ~chriz-sod-remix/lib/comp120.tpa~'))
        self.assertIn('EndCutSceneMode()', self.decompile('bdcut10.bcs'))
        self.assertIn('StartMovie("sodcin02")', self.decompile('bdcut28.bcs'))
        self.assertEqual('false()',dialog_states((self.override/'bdimoen.dlg').read_bytes())[67].transitions[1].trigger)

    def test_130_absent_script_and_changed_flag_are_overwritten(self):
        (self.override/'bd0120.are').write_bytes(b'AREAV1.0')
        self.assert_success(self.run_weidu('chriz-sod-remix/setup-chriz-sod-remix.tp2','--force-install-list','130'))
        before=(self.override/'bdbaldur.bcs').read_bytes()
        # A second tail sees a changed owned setter, not a pristine base-game block.
        (self.override/'bdbaldur.bcs').write_bytes(before.replace(b'4 0 0 ',b'99 0 0 '))
        tp=(self.game/'chriz-sod-remix/setup-chriz-sod-remix.tp2').read_text(encoding='utf-8')
        body=tp[tp.index('BEGIN @130'):tp.index('// 135')]
        body='\n'.join(l for l in body.splitlines() if not l.startswith(('BEGIN @130','REQUIRE_PREDICATE')))
        self.apply(130,body=body,second=True)
        self.assertEqual(before,(self.override/'bdbaldur.bcs').read_bytes())
        self.assertEqual(self.decompile('bdbaldur.bcs').count('SetGlobal("bd_ddd","GLOBAL",4)'),1)

    def test_140_changed_walkin_guards_keep_native_intro_launcher(self):
        self.seed(140,'bdintro.bcs bd0120.bcs bdsodtrn.bcs')
        before=self.decompile('bdintro.bcs')
        src=before.replace('  InMyArea("minsc")','  True()\n  InMyArea("minsc")').replace('  !InMyArea("minsc")','  True()\n  !InMyArea("minsc")')
        source=self.game/'changed-intro.baf';source.write_text(src,encoding='utf-8')
        result=self.run_weidu(str(source),'--out',str(self.override))
        self.assertEqual(result.returncode,0,result.stdout)
        self.assertNotIn('WARNING',result.stdout.upper())
        (self.override/'bdintro.bcs').write_bytes((self.override/'changed-intro.bcs').read_bytes())
        self.apply(140)
        intro=self.decompile('bdintro.bcs');area=self.decompile('bd0120.bcs')
        self.assertNotIn('"intro_follower1"',intro)
        self.assertIn('ActionOverride("minsc",JoinPartyOverride())',intro)
        self.assertIn('StartCutSceneEx("bdintro",TRUE)',area)
        self.assertIn('StartCutSceneEx("bdcut00z",FALSE)',area)
        first={n:(self.override/n).read_bytes() for n in ('bdintro.bcs','bd0120.bcs','bdsodtrn.bcs')}
        self.apply(140,second=True)
        for n,raw in first.items():self.assertEqual(raw,(self.override/n).read_bytes(),n)

    def test_250_missing_script_and_changed_second_tail(self):
        self.apply(250)
        before=(self.override/'bd7210.bcs').read_bytes()
        self.assertIn('ApplySpellRES("csrmorh","bdmorent")',self.decompile('bd7210.bcs'))
        (self.override/'bd7210.bcs').write_bytes(before.replace(b'1 0 0 ',b'77 0 0 '))
        self.apply(250,second=True)
        self.assertEqual((self.override/'bd7210.bcs').read_bytes(),before)

    def test_150_normal_council_and_second_tail(self):
        from test_khalid_continuity_installer import dialog_states
        names = 'bd0103.bcs bd0100.bcs bd0102.bcs bdserv.cre bgee.lua bdliia.dlg bdeltan.dlg bdbelt.dlg bdschael.dlg bdgarric.dlg bdsafana.dlg bdrasaad.dlg bddynahe.dlg bdaudam.dlg'
        self.seed(150, names)
        self.apply(150)
        first={n:(self.override/n).read_bytes() for n in names.split() if not n.endswith('lua')}
        self.assertEqual(self.decompile('bd0102.bcs').count('Global("BD_plot","global",51)'),5)
        self.assertEqual(self.decompile('bd0103.bcs').count('SetGlobal("CSR_ARRIVE","GLOBAL",1)'),1)
        liia=dialog_states(first['bdliia.dlg'])
        self.assertEqual(liia[9].transitions[1].trigger,'false()')
        self.apply(150,second=True)
        for n,raw in first.items():self.assertEqual(raw,(self.override/n).read_bytes(),n)
        self.assertEqual((self.override/'bgee.lua').read_text().count('-- CSR150 journal registration'),1)

    def test_150_missing_scripts_dialogues_and_changed_journal(self):
        from test_khalid_continuity_installer import dialog_states
        (self.override/'bgee.lua').write_text('-- a different journal table\n',encoding='utf-8')
        (self.override/'bdserv.cre').write_bytes(b'CRE V1.0')
        self.apply(150)
        self.assertIn('AdvanceTime(FOURTEEN_DAYS)',self.decompile('bd0103.bcs'))
        self.assertEqual(self.decompile('bd0102.bcs').count('Global("BD_plot","global",51)'),5)
        self.assertIn('createEntry(', (self.override/'bgee.lua').read_text())
        states=dialog_states((self.override/'bdbelt.dlg').read_bytes())
        self.assertIn('startcutsceneex("bdcut04",false)',states[41].transitions[0].action)
        self.assertFalse((self.override/'csrserv.cre').exists())

    def test_160_normal_and_second_tail_keep_one_import_and_swap(self):
        self.seed(160,'imoen2.cre bddialog.2da bd0120.bcs bd0103.bcs')
        self.apply(160)
        data=(self.override/'csrimo.cre').read_bytes()
        self.assertGreaterEqual(struct.unpack_from('<I',data,0x18)[0],64000)
        self.assertEqual(data[0x280:0x286],b'IMOEN2')
        names=('csrimo.cre','bddialog.2da','bd0120.bcs','bd0103.bcs','csrimoen.dlg')
        before={n:(self.override/n).read_bytes() for n in names}
        self.apply(160,second=True)
        for n,raw in before.items(): self.assertEqual((self.override/n).read_bytes(),raw,n)
        self.assertEqual(self.decompile('bd0120.bcs').count('SetGlobal("CSR_IMOEN_IMPORT","GLOBAL",1)'),1)

    def test_160_missing_scripts_table_and_damaged_donor(self):
        (self.override/'imoen2.cre').write_bytes(b'CRE V1.0')
        self.apply(160)
        self.assertFalse((self.override/'csrimo.cre').exists())
        self.assertIn('CSRIMOEN',(self.override/'bddialog.2da').read_text())
        self.assertIn('"CSR_IMOEN_STAGE"',self.decompile('bd0103.bcs'))
        self.assertIn('SetDialogue("csrimoen")',self.decompile('bd0120.bcs'))

    def seed_170(self):
        names = 'bd0116.bcs bd0102.bcs bdkorlas.dlg bdkorlas.bcs bdcutkor.bcs bdkorlas.cre bdkorme9.cre bdkorme8.cre bdshis07.cre bdporios.cre bdshkfam.cre bdfist1b.cre bd0130.are bd0120.are'
        self.seed(170, names)

    def test_170_changed_classes_books_spawn_and_second_tail(self):
        from test_khalid_continuity_installer import dialog_states
        self.seed_170()
        for n in ('bdkorlas','bdkorme9','bdkorme8','bdshis07','bdporios'):
            p=self.override/(n+'.cre');raw=bytearray(p.read_bytes());raw[0x273]=99
            struct.pack_into('<II',raw,0x2a0,0,0)
            struct.pack_into('<II',raw,0x2a8,0,0)
            struct.pack_into('<II',raw,0x2b0,0,0)
            p.write_bytes(raw)
        (self.override/'bd0116.bcs').write_bytes(b'SC\nSC\n')
        self.apply(170)
        for n,k in (('csrkorl',1),('csrhass',3),('csrvhas',2),('csrsill',4),('csrpori',1)):
            raw=(self.override/(n+'.cre')).read_bytes();self.assertEqual(raw[0x273],k)
        self.assertIn('CreateCreature("csrkorl",[1003.298],SW)',self.decompile('bd0116.bcs'))
        first={n:(self.override/n).read_bytes() for n in ('bd0116.bcs','bd0102.bcs','csrkorl.cre','csrhass.cre','csrpori.cre','bdkorlas.dlg')}
        self.apply(170,second=True)
        for n,raw in first.items():self.assertEqual(raw,(self.override/n).read_bytes(),n)

    def test_170_missing_graph_and_donors_keep_other_writes(self):
        from test_khalid_continuity_installer import dialog_states
        (self.override/'bdkorlas.cre').write_bytes(b'CRE V1.0')
        self.apply(170)
        self.assertIn('CreateCreature("csrkorl"',self.decompile('bd0116.bcs'))
        states=dialog_states((self.override/'bdkorlas.dlg').read_bytes())
        self.assertIn('enemy()',states[27].transitions[0].action)
        self.assertIn('StartCutSceneEx("bdcutkor",FALSE)',self.decompile('bdkorlas.bcs'))
        self.assertFalse((self.override/'csrkorl.cre').exists())

    def test_180_normal_second_tail_and_changed_council_text(self):
        self.seed(180,'bd0102.bcs bd0102.are bdliia.cre bdbelt.cre bdliia.dlg bdbelt.dlg bdshpam1.itm bdnobm1.cre bdnobf1.cre bdffsol1.cre')
        p=self.override/'bdbelt.dlg';raw=bytearray(p.read_bytes());off=struct.unpack_from('<I',raw,12)[0];struct.pack_into('<I',raw,off+36*16,0);p.write_bytes(raw)
        self.apply(180)
        names=('bd0102.bcs','bd0102.are','csrcele.dlg','bdbelt.dlg','csrpam.itm')
        first={n:(self.override/n).read_bytes() for n in names}
        self.apply(180,second=True)
        for n,raw in first.items():self.assertEqual(raw,(self.override/n).read_bytes(),n)
        self.assertEqual(self.decompile('bd0102.bcs').count('SetGlobal("CSR_CELEB","GLOBAL",1)'),1)

    def test_180_missing_exits_and_dialogue_are_created(self):
        self.seed(180,'bd0102.are')
        p=self.override/'bd0102.are';raw=bytearray(p.read_bytes());struct.pack_into('<H',raw,0x5a,0);p.write_bytes(raw)
        self.apply(180)
        raw=p.read_bytes();off=struct.unpack_from('<I',raw,0x5c)[0];count=struct.unpack_from('<H',raw,0x5a)[0]
        self.assertEqual(count,2)
        self.assertEqual({raw[off+i*196:off+i*196+32].split(b'\0')[0] for i in range(count)},{b'TranBD0101',b'TranBD0010'})
        self.assertIn('SetDialogue("csrcele")',self.decompile('bd0102.bcs'))
        self.assertTrue((self.override/'csrcele.dlg').is_file())

    def test_185_changed_staging_and_second_tail(self):
        self.seed(185,'bd0102.bcs bdliia.dlg bdbelt.dlg bdserv.dlg')
        source=self.decompile('bd0102.bcs').replace('[728.366]','[1.2]').replace('[895.487]','[3.4]')
        (self.game/'altered.baf').write_text(source,encoding='utf-8')
        self.assertEqual(self.run_weidu('altered.baf','--out',str(self.override)).returncode,0)
        (self.override/'bd0102.bcs').write_bytes((self.override/'altered.bcs').read_bytes())
        self.apply(185)
        self.assertNotIn('CreateCreature("BDENTAR"',self.decompile('bd0102.bcs'))
        self.assertIn('ActionOverride("BDBELT",JumpToPoint([759.472]))',self.decompile('bd0102.bcs'))
        first={n:(self.override/n).read_bytes() for n in ('bd0102.bcs','bdliia.dlg','bdbelt.dlg','bdserv.dlg')}
        self.apply(185,second=True)
        for n,raw in first.items():self.assertEqual(raw,(self.override/n).read_bytes(),n)

    def test_185_missing_scripts_and_dialogues(self):
        from test_khalid_continuity_installer import dialog_states
        self.apply(185)
        self.assertIn('ActionOverride("BDBELT",JumpToPoint([759.472]))',self.decompile('bd0102.bcs'))
        states=dialog_states((self.override/'bdliia.dlg').read_bytes())
        self.assertEqual(states[9].transitions[2].trigger,'false()')
        self.assertEqual(states[9].transitions[3].trigger,'false()')

    def test_190_missing_night_block_and_dialogue(self):
        self.apply(190)
        self.assertIn('"BD_MDD005"',self.decompile('bd0103.bcs'))
        before={n:(self.override/n).read_bytes() for n in ('bd0103.bcs','bdskie.dlg')}
        self.apply(190,second=True)
        for n,raw in before.items(): self.assertEqual((self.override/n).read_bytes(),raw,n)

    def test_187_actor_build_and_position_do_not_gate_removal(self):
        self.seed(187,'bd0100.are')
        raw=bytearray((self.override/'bd0100.are').read_bytes())
        ao,ac=struct.unpack_from('<IH',raw,0x54)
        targets={'Corwin','Assassin1','Assassin2','Assassin3','FF Guard 1','FF Guard 2','FF Dead 1','FF Dead 2','FF Dead 3'}
        offsets=[]
        for i in range(ac):
            at=ao+i*0x110
            if raw[at:at+32].split(b'\0')[0].decode() in targets:
                offsets.append(at)
                raw[at+0x80:at+0x88]=b'OTHERCRE'
                struct.pack_into('<HH',raw,at+0x20,1,2)
                struct.pack_into('<I',raw,at+0x40,0x12345678)
        (self.override/'bd0100.are').write_bytes(raw)
        self.apply(187)
        expected=bytearray(raw)
        for at in offsets: struct.pack_into('<I',expected,at+0x40,0)
        self.assertEqual((self.override/'bd0100.are').read_bytes(),expected)

    def test_187_damaged_area_is_only_unavailable_resource(self):
        (self.override/'bd0100.are').write_bytes(b'AREAV1.0')
        self.apply(187)
        self.assertEqual((self.override/'bd0100.are').read_bytes(),b'AREAV1.0')

    def test_145_preserves_continuous_import_join_and_foreign_actions(self):
        self.seed(145,'bdintro.bcs')
        self.apply(145)
        source=self.decompile('bdintro.bcs')
        self.assertEqual(source.count('ActionOverride("safana",JoinPartyOverride())'),2)
        self.assertNotIn('ActionOverride("minsc",JoinPartyOverride())',source)
        first=(self.override/'bdintro.bcs').read_bytes()
        self.apply(145,second=True)
        self.assertEqual((self.override/'bdintro.bcs').read_bytes(),first)

    def test_195_missing_dialogue_routes_and_second_tail(self):
        from test_khalid_continuity_installer import dialog_states
        self.apply(195)
        names=('bdcorwin.dlg','bdeltan.dlg','bdedwin.dlg','bdschael.dlg','bddebug.dlg','bdliia.dlg','bdfist05.dlg')
        first={n:(self.override/n).read_bytes() for n in names}
        self.assertIn('setglobal("bd_plot","global",54)',dialog_states(first['bdschael.dlg'])[227].transitions[0].action)
        self.assertEqual(dialog_states(first['bdliia.dlg'])[13].transitions[1].state,19)
        self.apply(195,second=True)
        for n,raw in first.items():self.assertEqual(raw,(self.override/n).read_bytes(),n)

    def test_197_missing_plot_scripts_and_dialogues_repeat(self):
        from test_khalid_continuity_installer import dialog_states
        self.apply(197)
        names=('bd0102.bcs','bdskie.bcs','bd2000.bcs','bdbence.bcs','bd7100.bcs','bdskie.dlg','bdbence.dlg','bdnederl.dlg')
        first={n:(self.override/n).read_bytes() for n in names}
        self.assertRegex(self.decompile('bd7100.bcs'),r'!(?:InParty|IsValidForPartyDialogue)\("bdskie"\)')
        self.assertTrue(any('joinparty()' in t.action for state in dialog_states(first['bdskie.dlg']) for t in state.transitions))
        self.apply(197,second=True)
        for n,raw in first.items():self.assertEqual(raw,(self.override/n).read_bytes(),n)

    def test_197_changed_camp_actor_and_native_plot_removal(self):
        self.seed(197,'bd0102.bcs bdskie.bcs bd2000.bcs bdbence.bcs bd7100.bcs bd4000.are bdskie.dlg bdbence.dlg bdnederl.dlg bddialog.2da')
        p=self.override/'bd4000.are';raw=bytearray(p.read_bytes());off,n=struct.unpack_from('<IH',raw,0x54);target=[]
        for i in range(n):
            at=off+i*272
            if raw[at:at+32].split(b'\0')[0].lower()==b'skie':
                raw[at+128:at+136]=b'CHANGED!';struct.pack_into('<HH',raw,at+32,1,2);target.append(at)
        p.write_bytes(raw);self.apply(197)
        for at in target:struct.pack_into('<I',raw,at+64,0)
        self.assertEqual(raw,p.read_bytes())
        self.assertNotIn('"bd_skie_plot"',self.decompile('bdskie.bcs'))

    def test_210_changed_worldmap_flags_and_missing_recruitment_script(self):
        raw=bytearray(0x10+0xb8+2*0xf0)
        struct.pack_into('<II',raw,8,1,0x10)
        struct.pack_into('<II',raw,0x10+0x20,2,0xc8)
        raw[0xc8:0xd0]=b'BD7000\0\0';struct.pack_into('<I',raw,0xc8+0x30,0xffffffff)
        raw[0x1b8:0x1c0]=b'BD2000\0\0';struct.pack_into('<I',raw,0x1b8+0x30,9)
        (self.override/'worldmap.wmp').write_bytes(raw)
        self.apply(210)
        expected=bytearray(raw);struct.pack_into('<I',expected,0xc8+0x30,0)
        self.assertEqual((self.override/'worldmap.wmp').read_bytes(),expected)
        first=(self.override/'bd1000.bcs').read_bytes()
        self.apply(210,second=True)
        self.assertEqual((self.override/'bd1000.bcs').read_bytes(),first)

    def test_actor_fields_normal_changed_and_second_tail(self):
        import json
        manifest=json.loads((self.game/'chriz-sod-remix/data/area-actor-ownership.json').read_text())
        for component in (200,220,230,260,270):
            areas=manifest[str(component)]
            self.seed(component,' '.join(n+'.are' for n in areas))
            expected={}
            for area,rows in areas.items():
                p=self.override/(area+'.are');raw=bytearray(p.read_bytes());off,n=struct.unpack_from('<IH',raw,0x54)
                for row in rows:
                    at=off+row['index']*272
                    raw[at+128:at+136]=b'EDITED!!'
                    struct.pack_into('<HHI',raw,at+32,1,2,0x12345678)
                p.write_bytes(raw)
                for row in rows:
                    at=off+row['index']*272
                    if 'cut' in row:struct.pack_into('<I',raw,at+64,0)
                    else:
                        struct.pack_into('<HHHH',raw,at+32,row['mvx'],row['mvy'],row['mvx'],row['mvy'])
                        struct.pack_into('<H',raw,at+52,row['mvo'])
                expected[area]=raw
            body=f'INCLUDE ~chriz-sod-remix/lib/comp{component}_lists.tpa~'
            name=f'actors{component}'
            (self.game/(name+'.tp2')).write_text(f'BACKUP ~{name}-backup~ AUTHOR ~fixture~ BEGIN ~actor fields~\n'+body)
            self.assert_success(self.run_weidu(name+'.tp2','--force-install-list','0'))
            for area,raw in expected.items():self.assertEqual(raw,(self.override/(area+'.are')).read_bytes(),area)
            (self.game/(name+'b.tp2')).write_text(f'BACKUP ~{name}b-backup~ AUTHOR ~fixture~ BEGIN ~actor fields again~\n'+body)
            self.assert_success(self.run_weidu(name+'b.tp2','--force-install-list','0'))
            for area,raw in expected.items():self.assertEqual(raw,(self.override/(area+'.are')).read_bytes(),area)

    def test_220_missing_movers_are_created_once(self):
        self.seed(220,'bd1200.are')
        p=self.override/'bd1200.are';raw=bytearray(p.read_bytes());struct.pack_into('<H',raw,0x58,0);p.write_bytes(raw)
        self.apply(220)
        raw=p.read_bytes();off,n=struct.unpack_from('<IH',raw,0x54)
        self.assertEqual(n,11)
        self.assertTrue(all(raw[off+i*272:off+i*272+7]==b'CSR220M' for i in range(n)))
        first=raw
        self.apply(220,second=True)
        self.assertEqual(first,p.read_bytes())

    def test_290_native_missing_graph_and_second_tail(self):
        from test_khalid_continuity_installer import dialog_states
        self.apply(290)
        raw=(self.override/'bddazzo.dlg').read_bytes()
        self.assertIn('endcredits()',dialog_states(raw)[2].transitions[0].action)
        self.assertEqual(self.decompile('bd4300.bcs').count('SetGlobal("bd_plot","global",587)'),1)
        names=('bd4300.bcs','bddebug.bcs','bdpalace.bcs','bddazzo.dlg','bdbence.dlg')
        first={n:(self.override/n).read_bytes() for n in names}
        self.apply(290,second=True)
        for n,raw in first.items():self.assertEqual(raw,(self.override/n).read_bytes(),n)

    def test_290_eet_changed_carrier_and_existing_bank(self):
        from test_khalid_continuity_installer import dialog_states
        self.seed(290,'bd4300.bcs bddebug.bcs bdpalace.bcs bdbence.dlg bddelanc.dlg bddazzo.dlg bdrumor3.dlg bddebug.dlg bdcorwij.dlg bd4300.are k#telbgt.bcs k#telbgt.cre')
        (self.override/'eet.flag').write_bytes(b'')
        original=(self.override/'k#telbgt.bcs').read_bytes()
        self.apply(290)
        self.assertEqual(original,(self.override/'k#telbgt.bcs').read_bytes())
        self.assertIn('MoveContainerContents("BD4300*K#ImportContainer","BD6100*K#ImportContainer")',self.decompile('csretbgt.bcs'))
        self.assertIn('createcreatureobject("csretbgt"',dialog_states((self.override/'bddazzo.dlg').read_bytes())[2].transitions[0].action)
        names=('bd4300.are','bd4300.bcs','csretbgt.bcs','bddazzo.dlg')
        first={n:(self.override/n).read_bytes() for n in names}
        self.apply(290,second=True)
        for n,raw in first.items():self.assertEqual(raw,(self.override/n).read_bytes(),n)

    def test_290_missing_eet_script_has_complete_private_handoff(self):
        self.seed(290,'bd4300.are k#telbgt.cre')
        (self.override/'eet.flag').write_bytes(b'')
        self.apply(290)
        script=self.decompile('csretbgt.bcs')
        for frame in (1,2,3):self.assertIn(f'SetGlobal("K#FrameDelay","LOCALS",{frame})',script)
        self.assertLess(script.index('SetGlobal("K#FrameDelay","LOCALS",1)'),script.index('TakeCreatureItems(Player1,ALL)'))
        self.assertLess(script.index('TakeCreatureItems(Player1,ALL)'),script.index('MoveToCampaign("SoA")'))
        self.assertIn('MoveContainerContents("BD4300*K#ImportContainer","BD6100*K#ImportContainer")',script)
        self.assertFalse((self.override/'k#telbgt.bcs').exists())

    def test_award_sections_create_missing_blocks_and_repeat_once(self):
        cases=((215,'bd7100.bcs',16500),(220,'bd1200.bcs',106700),
               (260,'bd4000.bcs',103600),(270,'bd5300.bcs',5200))
        for component,name,amount in cases:
            with self.subTest(component=component):
                source=(self.game/f'chriz-sod-remix/lib/comp{component}.tpa').read_text(encoding='utf-8')
                source=source[source.index('INCLUDE ~chriz-sod-remix/lib/overwrite.tpa~'):]
                body=f'OUTER_SET csr_xp_chunk = {amount} OUTER_SET csr_xp_chunk_260 = {amount} OUTER_SET csr_xp_chunk_270 = {amount}\n'+source
                # Different setup paths append separate components without uninstalling.
                name1=f'award{component}'
                (self.game/(name1+'.tp2')).write_text(f'BACKUP ~{name1}-backup~ AUTHOR ~fixture~ BEGIN ~award~\n'+body,encoding='utf-8')
                self.assert_success(self.run_weidu(name1+'.tp2','--force-install-list','0'))
                raw=(self.override/name).read_bytes()
                actual=self.decompile(name)
                self.assertEqual(actual.count(f'AddexperienceParty({amount})'),2 if component==270 else 1)
                (self.game/(name1+'b.tp2')).write_text(f'BACKUP ~{name1}b-backup~ AUTHOR ~fixture~ BEGIN ~award~\n'+body,encoding='utf-8')
                self.assert_success(self.run_weidu(name1+'b.tp2','--force-install-list','0'))
                self.assertEqual((self.override/name).read_bytes(),raw)

    def test_native_awards_preserve_every_unowned_story_block(self):
        cases=((215,'bd7100.bcs',16500,'IncrementChapter("SODTXT9")'),
               (220,'bd1200.bcs',106700,'SetGlobal("BD_DOD_COLDH_DEFEATED"'),
               (260,'bd4000.bcs',103600,'IncrementChapter("chptxt11")'),
               (270,'bd5300.bcs',5200,'Switch("bd_sdd350_ihj","bd5300")'))
        for component,name,amount,owned in cases:
            with self.subTest(component=component):
                self.seed(component,name)
                original=self.decompile(name)
                source=(self.game/f'chriz-sod-remix/lib/comp{component}.tpa').read_text(encoding='utf-8')
                source=source[source.index('INCLUDE ~chriz-sod-remix/lib/overwrite.tpa~'):]
                body=f'OUTER_SET csr_xp_chunk = {amount} OUTER_SET csr_xp_chunk_260 = {amount} OUTER_SET csr_xp_chunk_270 = {amount}\n'+source
                setup=f'native{component}'
                (self.game/(setup+'.tp2')).write_text(f'BACKUP ~{setup}-backup~ AUTHOR ~fixture~ BEGIN ~award~\n'+body,encoding='utf-8')
                self.assert_success(self.run_weidu(setup+'.tp2','--force-install-list','0'))
                actual=self.decompile(name)
                for block in re.findall(r'^IF\n.*?^END',original,re.M|re.S):
                    if owned.lower() not in block.lower(): self.assertIn(block,actual)
                self.assertEqual(actual.count(f'AddexperienceParty({amount})'),2 if component==270 else 1)

    def test_280_public_install_with_missing_optional_scripts(self):
        (self.override/'bd0120.are').write_bytes(b'AREAV1.0')
        self.assert_success(self.run_weidu('chriz-sod-remix/setup-chriz-sod-remix.tp2','--force-install-list','280'))
        for name in ('bdcut45a','bdcut45b','cutskip'):
            self.assertFalse((self.override/(name+'.bcs')).exists())

    def test_280_duplicate_party_dispels_preserve_nonparty_actions_and_repeat(self):
        names=('bdcut45a','bdcut45b','cutskip')
        source='IF True() THEN RESPONSE #100 ReallyForceSpellRES("BDDISPEL",Player1) ReallyForceSpellRES("bddispel",Player1) ReallyForceSpellRES("bddispel",Player6) ReallyForceSpellRES("bddispel",Myself) SetGlobal("FOREIGN","GLOBAL",5) END'
        for name in names: (self.game/(name+'.baf')).write_text(source,encoding='utf-8')
        for name in names:
            result=self.run_weidu(name+'.baf','--out',str(self.override))
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.apply(280)
        before={}
        for name in names:
            actual=self.decompile(name+'.bcs')
            self.assertNotRegex(actual,r'ReallyForceSpellRES\("[Bb][Dd][Dd][Ii][Ss][Pp][Ee][Ll]",Player[1-6]\)')
            self.assertIn('ReallyForceSpellRES("bddispel",Myself)',actual)
            self.assertIn('SetGlobal("FOREIGN","GLOBAL",5)',actual)
            before[name]=(self.override/(name+'.bcs')).read_bytes()
        self.apply(280,second=True)
        for name,raw in before.items(): self.assertEqual((self.override/(name+'.bcs')).read_bytes(),raw)
