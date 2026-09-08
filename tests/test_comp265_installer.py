#!/usr/bin/env python3
"""Real WeiDU fixtures for component265; writes only disposable synthetic games.

The public TP2's dependency selection and separate XP library have their own
integration tests. This harness exercises the exact production corrective TPA.
"""
from __future__ import annotations

from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'research/scripts'))
from test_comp291_installer import WEIDU, ROOT, compact, tree, write_fake_game

ITEM_BLOCK = '''IF
  Global("bd_add_mizhena_amulet","bd5000",0)
THEN
''' + ''.join(f'''  RESPONSE #33
    SetGlobal("bd_add_mizhena_amulet","bd5000",1)
    GiveItemCreate("bdmisc68","Displacer Beast {n}",0,0,0)
''' for n in (1, 2, 3)) + 'END\n'
CURRENT_ITEM = re.sub(r'^    GiveItemCreate.*\n', '', ITEM_BLOCK, flags=re.M)
SOUL = '    CreateCreatureObject("bdshsoul",Myself,1,0,0)\n'
SHADOW = '    CreateCreatureObject("bdshad04",Myself,1,0,0)\n'


def summon_block(difficulty: str, souls: int) -> str:
    return f'''IF
  !StateCheck(Myself,STATE_INVISIBLE)
  Difficulty({difficulty})
  !GlobalTimerNotExpired("bd_summons","locals")
  See(NearestEnemyOf(Myself))
THEN
  RESPONSE #100
    SetGlobalTimer("bd_summons","locals",TEN_ROUNDS)
    ApplySpell(Myself,WIZARD_SHADOW_DOOR)
    ApplySpell(Myself,WIZARD_DARKNESS_15_FOOT)
''' + SHADOW * 2 + SOUL * souls + '    Continue()\nEND\n'


FOREIGN = '''IF
  Global("FOREIGN_TEST","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_TEST","GLOBAL",7)
    Continue()
END
'''
ASHIRUK = FOREIGN + summon_block('HARD', 0) + summon_block('HARDEST', 2) + FOREIGN
CURRENT_ASHIRUK = ASHIRUK.replace(SOUL, '')


def item(ref: str, seed: int = 1) -> bytes:
    # Deliberately nondefault expiration/charges/flags: preserving only resrefs
    # or rebuilding a vanilla-looking loadout cannot satisfy these fixtures.
    return struct.pack('<8sHHHHI', ref.encode(), seed, seed + 1, seed + 2,
                       seed + 3, 0x12340000 + seed)


def area(*, guardian: bool = False, target_items: list[bytes] | None = None,
         guardian_schedule: int = 0xffffff) -> bytes:
    actors = [('Other ghost', 'BDWORIS', 900, 650, 0xffffff),
              ('UNSLEEPING_GUARDIAN', 'BDUNSLGU', 681, 924, guardian_schedule),
              ('Unrelated Guardian', 'BDUNSLGU', 12, 34, 0xffffff)] if guardian else [
        (f'Displacer Beast {n}', 'BDDISPBE', 4200+n, 1100+n, 0) for n in (1, 2, 3)]
    if target_items is None:
        target_items = [item('FOREIGN', 5), item('RNDMAG05', 7), item('SCRL01', 9)]
    containers = [('Before', [item('BEFORE', 3)]), ('Dead_fighter', target_items),
                  ('Empty', []), ('After', [item('AFTER', 11)])]
    ao = 0xf4
    co = ao + len(actors) * 0x110
    io = co + len(containers) * 0xc0
    items = b''.join(raw for _, entries in containers for raw in entries)
    data = bytearray(io + len(items))
    data[:8] = b'AREAV1.0'
    struct.pack_into('<IH', data, 0x54, ao, len(actors))
    struct.pack_into('<IHHI', data, 0x70, co, len(containers), len(items)//20, io)
    for index, (name, cre, x, y, schedule) in enumerate(actors):
        b = ao + index * 0x110
        data[b:b+0x110] = bytes([0x40 + index]) * 0x110
        data[b:b+32] = name.encode().ljust(32, b'\0')
        struct.pack_into('<HH', data, b+0x20, x, y)
        struct.pack_into('<I', data, b+0x40, schedule)
        data[b+0x80:b+0x88] = cre.encode().ljust(8, b'\0')
    first = 0
    for index, (name, entries) in enumerate(containers):
        b = co + index * 0xc0
        data[b:b+0xc0] = bytes([0x70 + index]) * 0xc0
        data[b:b+32] = name.encode().ljust(32, b'\0')
        struct.pack_into('<HH', data, b+0x20, 4295, 1098)
        struct.pack_into('<II', data, b+0x40, first, len(entries))
        first += len(entries)
    data[io:io+len(items)] = items
    return bytes(data) + b'UNRELATED TRAILING PAYLOAD\0\xff'


def containers(data: bytes) -> dict[str, list[bytes]]:
    co, count, _, io = struct.unpack_from('<IHHI', data, 0x70)
    result = {}
    for i in range(count):
        b = co+i*0xc0
        name = data[b:b+32].split(b'\0')[0].decode()
        first, length = struct.unpack_from('<II', data, b+0x40)
        result[name] = [data[io+j*20:io+(j+1)*20] for j in range(first, first+length)]
    return result


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class Component265InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='csr265-installer-')
        self.addCleanup(self.temp.cleanup)
        self.game = Path(self.temp.name)
        write_fake_game(self.game)
        self.override = self.game / 'override'
        additions = {
            'action': '0 NoAction()\n115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)\n140 GiveItemCreate(S:ResRef*,O:Object*,I:Usage1*,I:Usage2*,I:Usage3*)\n160 ApplySpell(O:Target,I:Spell*Spell)\n',
            'trigger': '0x401C See(O:Object*)\n0x4037 StateCheck(O:Object*,I:State*State)\n0x4041 GlobalTimerNotExpired(S:Name*,S:Area*)\n0x40D0 Difficulty(I:Amount*DIFFLEV)\n',
            'object': '12 NearestEnemyOf\n',
            'state': '16 STATE_INVISIBLE\n',
            'difflev': '4 HARD\n5 HARDEST\n',
            'gtimes': '60 TEN_ROUNDS\n',
            'spell': '2505 WIZARD_SHADOW_DOOR\n2228 WIZARD_DARKNESS_15_FOOT\n',
        }
        for name, text in additions.items():
            path = self.override / f'{name}.ids'
            old = path.read_text() if path.exists() else 'IDS V1.0\n'
            path.write_text(old + text, encoding='ascii')
        (self.game / 'chriz-sod-remix/lib').mkdir(parents=True)
        shutil.copy2(ROOT / 'chriz-sod-remix/lib/comp265.tpa',
                     self.game / 'chriz-sod-remix/lib/comp265.tpa')
        (self.game / 'fixture').mkdir()
        (self.game / 'fixture/setup-fixture.tp2').write_text('''BACKUP ~fixture/backup~
AUTHOR ~fixture~
BEGIN ~compile fixture~ DESIGNATED 0
COMPILE ~fixture/bd5000.baf~
COMPILE ~fixture/bdashiru.baf~
''')
        self.write('bd5000.are', area())
        self.write('bd5110.are', area(guardian=True))
        self.write('unrelated.cre', b'IMMUTABLE THIRD PARTY CREATURE')
        self.write('bd4000.bcs', b'IMMUTABLE XP RESOURCE')

    def write(self, name, data):
        (self.override / name).write_bytes(data)

    def run_weidu(self, *args):
        return subprocess.run([str(WEIDU), *args, '--game', str(self.game),
                               '--language', '0', '--use-lang', 'en_US', '--no-exit-pause'],
                              cwd=self.game, capture_output=True, text=True, timeout=45)

    def fixture(self, item_script=ITEM_BLOCK, ash_script=ASHIRUK):
        (self.game / 'fixture/bd5000.baf').write_text(FOREIGN+item_script+FOREIGN)
        (self.game / 'fixture/bdashiru.baf').write_text(ash_script)
        result = self.run_weidu('fixture/setup-fixture.tp2', '--force-install-list', '0')
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('SUCCESSFULLY INSTALLED', result.stdout)

    def repair(self, repair260=1, repair240=1):
        (self.game / 'repair.tp2').write_text(f'''BACKUP ~repair-backup~
AUTHOR ~fixture~
BEGIN ~production265 harness~ DESIGNATED 265
OUTER_SET csr265_repair260 = {repair260}
OUTER_SET csr265_repair240 = {repair240}
INCLUDE ~chriz-sod-remix/lib/comp265.tpa~
''')
        return self.run_weidu('repair.tp2', '--force-install-list', '265')

    def decompile(self, name):
        out = self.game / 'decompiled'
        out.mkdir(exist_ok=True)
        result = self.run_weidu(str(self.override/name), '--out', str(out),
                                '--log', str(out/'audit.log'))
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        return next(p for p in out.iterdir() if p.name.lower()==name.replace('.bcs','.baf')).read_text()

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('SUCCESSFULLY INSTALLED', result.stdout)

    def assert_failure(self, expected):
        before = tree(self.override)
        result = self.repair()
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn(expected, result.stdout+result.stderr)
        self.assertEqual(tree(self.override), before)
        backups = self.game / 'repair-backup/265'
        self.assertFalse(backups.exists() and any(p.suffix.lower() in {'.are','.bcs'}
                         for p in backups.iterdir()), 'preflight failure began resource writes')

    def test_full_repair_preserves_raw_items_other_tables_quests_and_ai(self):
        self.fixture()
        original = {p.name:p.read_bytes() for p in self.override.iterdir()}
        self.assert_success(self.repair())
        before = original['bd5000.are']; after = (self.override/'bd5000.are').read_bytes()
        expected = containers(before)
        expected['Dead_fighter'].append(b'BDMISC68'+b'\0'*12)
        self.assertEqual(containers(after), expected)
        co = struct.unpack_from('<I',before,0x70)[0]
        permitted = set(range(0x76,0x7c)) | set(range(co+0xc0+0x44,co+0xc0+0x48))
        permitted |= set(range(co+2*0xc0+0x40,co+2*0xc0+0x44))
        permitted |= set(range(co+3*0xc0+0x40,co+3*0xc0+0x44))
        self.assertTrue(all(a==b or i in permitted for i,(a,b) in enumerate(zip(before,after))))
        expected_guardian = bytearray(original['bd5110.are'])
        struct.pack_into('<I',expected_guardian,0xf4+0x110+0x40,0)
        self.assertEqual((self.override/'bd5110.are').read_bytes(),expected_guardian)
        self.assertEqual(compact(self.decompile('bd5000.bcs')),compact(FOREIGN+CURRENT_ITEM+FOREIGN))
        self.assertEqual(compact(self.decompile('bdashiru.bcs')),compact(CURRENT_ASHIRUK))
        for name,data in original.items():
            if name not in {'bd5000.are','bd5110.are','bd5000.bcs','bdashiru.bcs'}:
                self.assertEqual((self.override/name).read_bytes(),data,name)

    def test_already_corrected_is_byte_exact_noop(self):
        self.fixture(CURRENT_ITEM,CURRENT_ASHIRUK)
        self.write('bd5000.are',area(target_items=[item('FOREIGN'),b'BDMISC68'+b'\0'*12]))
        self.write('bd5110.are',area(guardian=True,guardian_schedule=0))
        before=tree(self.override)
        self.assert_success(self.repair())
        self.assertEqual(tree(self.override),before)

    def test_existing_single_amulet_preserved_while_obsolete_grants_removed(self):
        self.fixture()
        raw=area(target_items=[item('BDMISC68',29),item('FOREIGN',17)])
        self.write('bd5000.are',raw)
        self.assert_success(self.repair())
        self.assertEqual((self.override/'bd5000.are').read_bytes(),raw)
        self.assertNotIn('GiveItemCreate',self.decompile('bd5000.bcs'))

    def test_empty_target_preserves_following_and_empty_container_runs(self):
        self.fixture()
        self.write('bd5000.are',area(target_items=[]))
        self.assert_success(self.repair())
        self.assertEqual(containers((self.override/'bd5000.are').read_bytes()),
            {'Before':[item('BEFORE',3)],'Dead_fighter':[b'BDMISC68'+b'\0'*12],
             'Empty':[],'After':[item('AFTER',11)]})

    def test_no240_does_not_require_or_write_ashiruk(self):
        self.fixture(); (self.override/'bdashiru.bcs').unlink()
        self.assert_success(self.repair(repair240=0))
        self.assertFalse((self.override/'bdashiru.bcs').exists())

    def test_240_only_does_not_require_260_resources(self):
        self.fixture()
        for name in ('bd5000.are','bd5110.are','bd5000.bcs'): (self.override/name).unlink()
        self.assert_success(self.repair(repair260=0))
        self.assertEqual(compact(self.decompile('bdashiru.bcs')),compact(CURRENT_ASHIRUK))

    def test_no_selected_scope_is_noop(self):
        before=tree(self.override)
        self.assert_success(self.repair(0,0))
        self.assertEqual(tree(self.override),before)

    def test_changed_native_grant_branch_fails_before_any_write(self):
        self.fixture(ITEM_BLOCK.replace('Displacer Beast 3','Other actor'))
        self.assert_failure('amulet grant branches differ')

    def test_changed_summon_block_fails_before_any_write(self):
        self.fixture(ash_script=ASHIRUK.replace(SOUL, '', 1))
        self.assert_failure('HARDEST summon block differs')

    def test_duplicate_amulet_fails_before_any_write(self):
        self.fixture(); self.write('bd5000.are',area(target_items=[item('BDMISC68'),item('BDMISC68',3)]))
        self.assert_failure('duplicate amulets already exist')

    def test_amulet_in_another_container_fails_before_any_write(self):
        self.fixture(); raw=area().replace(b'AFTER\0\0\0',b'BDMISC68')
        self.write('bd5000.are',raw)
        self.assert_failure('amulet is outside Dead_fighter')

    def test_active_displacer_fails_before_any_write(self):
        self.fixture(); raw=bytearray(area()); struct.pack_into('<I',raw,0xf4+0x40,0xffffff)
        self.write('bd5000.are',raw)
        self.assert_failure('not a suppressed displacer beast')

    def test_missing_or_moved_container_fails_before_any_write(self):
        self.fixture(); raw=bytearray(area()); co=struct.unpack_from('<I',raw,0x70)[0]
        struct.pack_into('<H',raw,co+0xc0+0x20,1234); self.write('bd5000.are',raw)
        self.assert_failure('Dead_fighter moved')

    def test_out_of_bounds_item_run_fails_before_any_write(self):
        self.fixture(); raw=bytearray(area()); co=struct.unpack_from('<I',raw,0x70)[0]
        struct.pack_into('<I',raw,co+0xc0+0x44,999); self.write('bd5000.are',raw)
        self.assert_failure('container item run is out of bounds')

    def test_overlapping_item_ownership_fails_before_any_write(self):
        self.fixture(); raw=bytearray(area()); co=struct.unpack_from('<I',raw,0x70)[0]
        struct.pack_into('<I',raw,co+3*0xc0+0x40,2); self.write('bd5000.are',raw)
        self.assert_failure('container item runs overlap')

    def test_missing_guardian_fails_before_any_write(self):
        self.fixture(); raw=bytearray(area(guardian=True))
        struct.pack_into('<H',raw,0xf4+0x110+0x20,680); self.write('bd5110.are',raw)
        self.assert_failure('expected one Guardian')


if __name__=='__main__':
    unittest.main(verbosity=2)
