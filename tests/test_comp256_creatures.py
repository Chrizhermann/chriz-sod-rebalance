"""Real WeiDU validation of the owned bridge roster; synthetic game only."""
from pathlib import Path
import collections
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'research/scripts'))
from test_comp291_installer import WEIDU, write_fake_game

SPELLS = {
    'stoneskin': ('SPWI408', 4), 'mirrorimage': ('SPWI212', 2),
    'shield': ('SPWI114', 1), 'fireshield': ('SPWI418', 4),
    'protfire': ('SPWI319', 4), 'spiritarmor': ('SPWI414', 4),
    'minordeflect': ('SPWI318', 3), 'haste': ('SPWI305', 3),
    'fireball': ('SPWI304', 3), 'flamearrow': ('SPWI303', 3),
    'slow': ('SPWI312', 3), 'glitterdust': ('SPWI224', 2),
    'grease': ('SPWI101', 1), 'breach': ('SPWI513', 5),
    'malison': ('SPWI412', 4), 'magicmissile': ('SPWI112', 1),
}
ITEMS = ('STAF01 DART01 CLCK12 POTN52 HELM01 PLAT01 SW2H02 '
         'IMMUNE2 FIREELEL FIREELEM ELEARL ELEAR').split()


def u(b, o, f='I'):
    return struct.unpack_from('<' + f, b, o)[0]


def s(b, o, n=8):
    return b[o:o+n].split(b'\0', 1)[0].decode()


def creature(cls=1, hp=52, immunity=False, version=1):
    b = bytearray(0x2d4)
    b[:8] = b'CRE V1.0'
    struct.pack_into('<HH', b, 0x24, hp, hp)
    b[0x33] = version
    b[0x273] = cls
    b[0x234] = 13 if cls == 1 else 9
    for o in (0x248, 0x250, 0x258, 0x260, 0x268, 0x280, 0x2cc):
        b[o:o+8] = b'FOREIGN\0'
    # A complete existing spellbook must be removed, not left below new spells.
    struct.pack_into('<II', b, 0x2a0, len(b), 1)
    b += struct.pack('<8sHH', b'OLDMAGIC', 5, 1)
    struct.pack_into('<II', b, 0x2a8, len(b), 1)
    b += struct.pack('<HHHHII', 5, 9, 9, 1, 0, 1)
    struct.pack_into('<II', b, 0x2b0, len(b), 1)
    b += struct.pack('<8sI', b'OLDMAGIC', 1)
    struct.pack_into('<I', b, 0x2b8, len(b))
    slots = [-1] * 40
    slots[9] = 0
    slots[38] = 0
    slots[39] = 0
    if immunity:
        slots[4] = 1
    b += struct.pack('<40h', *slots)
    entries = [struct.pack('<8sHHHHI', b'UNIQUE!!', 0, 3, 4, 5, 0)]
    if immunity:
        entries.append(struct.pack('<8sHHHHI', b'IMMUNE2', 0, 0, 0, 0, 0))
    struct.pack_into('<II', b, 0x2bc, len(b), len(entries))
    b += b''.join(entries)
    struct.pack_into('<II', b, 0x2c4, len(b), 2)
    for opcode in (233, 187):
        effect = bytearray(264 if version else 48)
        if version:
            effect[:8] = b'EFF V2.0'
            struct.pack_into('<I', effect, 8, opcode)
            struct.pack_into('<I', effect, 28, 9)
            effect[40:48] = b'bd_no_co' if opcode == 187 else bytes(8)
        else:
            struct.pack_into('<H', effect, 0, opcode)
            effect[12] = 9
            effect[20:28] = b'bd_no_co' if opcode == 187 else bytes(8)
        b += effect
    return bytes(b)


def item(fire=False):
    b = bytearray(0x72 + 56 + (48 if fire else 0))
    b[:8] = b'ITM V1  '
    struct.pack_into('<I', b, 0x60, 3)
    struct.pack_into('<IHI', b, 0x64, 0x72, 1, 0x72 + 56)
    b[0x72] = 1
    struct.pack_into('<HHhHHH', b, 0x72 + 0x16, 8, 3 if fire else 4, 0, 2, int(fire), 0)
    if fire:
        p = 0x72 + 56
        struct.pack_into('<H', b, p, 12)
        b[p+2] = 2
        struct.pack_into('<I', b, p+8, 0x80000)
        struct.pack_into('<II', b, p+28, 1, 6)
    return bytes(b)


def monk_policy_creature(version=1, **changes):
    """Artisan's reviewed class-filtered equipment helpers in either CRE format."""
    b = bytearray(creature(version=version))
    fields = dict(target=0, power=0, param2=105, timing=1, duration=0,
                  prob1=100, prob2=0, special=0)
    fields.update(changes)
    layouts = ({'target': (2, 'B'), 'power': (3, 'B'), 'param1': (4, 'I'),
                'param2': (8, 'I'), 'timing': (12, 'B'), 'duration': (14, 'I'),
                'prob1': (18, 'B'), 'prob2': (19, 'B'), 'special': (44, 'I')},
               {'target': (12, 'I'), 'power': (16, 'I'), 'param1': (20, 'I'),
                'param2': (24, 'I'), 'timing': (28, 'I'), 'duration': (32, 'I'),
                'prob1': (36, 'H'), 'prob2': (38, 'H'), 'special': (64, 'I')})
    for cls in (19, 1):
        effect = bytearray(264 if version else 48)
        if version:
            effect[:8] = b'EFF V2.0'
        struct.pack_into('<I' if version else '<H', effect, 8 if version else 0, 326)
        for key, value in {'param1': cls, **fields}.items():
            off, fmt = layouts[version][key]
            struct.pack_into('<' + fmt, effect, off, value)
        off = 40 if version else 20
        effect[off:off+8] = b'C0PR#MO1'
        b += effect
    struct.pack_into('<I', b, 0x2c8, 4)
    return bytes(b)


def effects(b):
    off, count = u(b, 0x2c4), u(b, 0x2c8)
    size = 264 if b[0x33] else 48
    return [b[off+i*size:off+(i+1)*size] for i in range(count)]


def book(b):
    return collections.Counter(s(b, u(b, 0x2b0)+i*12) for i in range(u(b, 0x2b4)))


def inventory(b):
    return {s(b, u(b, 0x2bc)+i*20):
            (u(b, u(b, 0x2bc)+i*20+10, 'H'), u(b, u(b, 0x2bc)+i*20+16))
            for i in range(u(b, 0x2c0))}


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable')
class BridgeCreatureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='csr256-cre-')
        self.addCleanup(self.temp.cleanup)
        self.game = Path(self.temp.name)
        write_fake_game(self.game)
        self.ov = self.game/'override'
        self.donors = {}
        for ref in ('BDOLONEI BDCRUE45 BDELFIRL BDELFIRM BDELFIRG '
                    'ELEARL01 ELEAR01 ELEARG01').split():
            b = creature(cls=1 if ref == 'BDOLONEI' else 2,
                         hp=52 if ref == 'BDOLONEI' else 108,
                         immunity=ref.startswith('ELEAR') or ref in ('BDELFIRM', 'BDELFIRG'))
            self.donors[ref+'.CRE'] = b
            self.resource(ref+'.CRE').write_bytes(b)
        for ref in ITEMS:
            b = item(fire=ref.startswith('FIRE'))
            self.donors[ref+'.ITM'] = b
            self.resource(ref+'.ITM').write_bytes(b)
        self.mod = self.game/'fixture'
        self.mod.mkdir()
        shutil.copy2(ROOT/'chriz-sod-remix/lib/comp256_creatures.tpa', self.mod/'creatures.tpa')

    def run_install(self, *, protfire=4, preflight_only=False, levels=None):
        spells = dict(SPELLS)
        spells['protfire'] = ('SPWI319', protfire)
        for key, level in (levels or {}).items():
            spells[key] = (spells[key][0], level)
        variables = '\n'.join(f'OUTER_SPRINT csr256_{k}_res ~{ref}~\nOUTER_SET csr256_{k}_level = {lev}'
                              for k, (ref, lev) in spells.items())
        source = f'''BACKUP ~fixture/backup~
AUTHOR ~test~
BEGIN ~Bridge creature fixture~
OUTER_SET csr256_xp_mage = 1000
OUTER_SET csr256_xp_guard = 420
OUTER_SET csr256_xp_elemental = 420
{variables}
INCLUDE ~fixture/creatures.tpa~
LAF csr256_creatures_preflight END
''' + ('' if preflight_only else 'LAF csr256_creatures_install END\n')
        path = self.game/'fixture.tp2'
        path.write_text(source)
        p = subprocess.run([str(WEIDU), str(path), '--game', str(self.game),
                            '--language', '0', '--use-lang', 'en_US',
                            '--no-exit-pause', '--skip-at-view', '--force-install-list', '0'],
                           cwd=self.game, capture_output=True, text=True, errors='replace', timeout=90)
        self.output = p.stdout + p.stderr
        return p.returncode

    def resource(self, name):
        # WeiDU writes normalized resource names on Unix. Use lowercase files
        # while keeping logical resrefs/CRE contents uppercase.
        return self.ov/name.lower()

    def owned_resources(self):
        return sorted(p for p in self.ov.iterdir() if p.name.lower().startswith('csr2'))

    def read(self, ref):
        return self.resource(ref+'.CRE').read_bytes()

    def assert_success(self, **kwargs):
        self.assertEqual(self.run_install(**kwargs), 0, self.output)

    def test_approved_books_are_finite_and_old_spells_removed(self):
        self.assert_success()
        fire, control = self.read('CSR256FM'), self.read('CSR256CM')
        for b in (fire, control):
            self.assertEqual(book(b)['SPWI408'], 2)
            self.assertEqual(book(b)['SPWI212'], 3)
            self.assertEqual(book(b)['SPWI513'], 1)
            self.assertNotIn('OLDMAGIC', book(b))
            self.assertFalse(any(ref in book(b) for ref in ('SPWI620', 'SPWI622')))
            self.assertEqual((u(b, 0x24, 'H'), u(b, 0x26, 'H'), b[0x234]), (52, 52, 13))
            self.assertEqual(inventory(b)['POTN52'][0], 1)
            self.assertNotIn('UNIQUE!!', inventory(b))
            self.assertEqual(u(b, 0x1c), 0)
            info = u(b, 0x2a8)
            slots = [(u(b, info+i*16, 'H'), u(b, info+i*16+2, 'H'),
                      u(b, info+i*16+12)) for i in range(u(b, 0x2ac))]
            self.assertEqual([row[:2] for row in slots], list(enumerate((5, 5, 5, 4, 4, 2))))
            self.assertTrue(all(prepared <= capacity for _, capacity, prepared in slots))
        self.assertEqual({ref: book(fire)[ref] for ref in ('SPWI305', 'SPWI303', 'SPWI304')},
                         {'SPWI305': 1, 'SPWI303': 2, 'SPWI304': 2})
        self.assertEqual(book(control)['SPWI318'], 2)
        self.assertEqual(book(control)['SPWI312'], 3)
        self.assertEqual(book(control)['SPWI224'], 2)

    def test_vanilla_protection_level_preserves_haste_and_reserves(self):
        self.assert_success(protfire=3)
        b = self.read('CSR256FM')
        self.assertEqual(book(b)['SPWI304'], 1)
        self.assertEqual(book(b)['SPWI303'], 2)
        self.assertEqual(book(b)['SPWI305'], 1)
        self.assertEqual(book(b)['SPWI408'], 2)

    def test_standalone_earth_fallbacks_match_the_approved_tiers(self):
        for name in ('ELEARL01.CRE', 'ELEAR01.CRE', 'ELEARL.ITM'):
            self.resource(name).unlink()
        lesser = bytearray(creature(cls=188, hp=64, immunity=True))
        lesser[0x234] = 8
        lesser[0x237] = 6
        lesser[0x275] = 6
        self.resource('SUMELEAR.CRE').write_bytes(lesser)
        greater = bytearray(creature(cls=188, hp=128, immunity=True))
        greater[0x237] = 6
        greater[0x275] = 6
        self.resource('ELEARG01.CRE').write_bytes(greater)
        self.assert_success(protfire=3)
        for tier, hp, thac0, saves in [
            ('L', 80, 10, [8, 10, 9, 9, 11]),
            ('S', 96, 9, [7, 9, 8, 8, 10]),
        ]:
            b = self.read('CSR26E1'+tier)
            self.assertEqual((u(b, 0x24, 'H'), u(b, 0x26, 'H')), (hp, hp))
            self.assertEqual(b[0x52], thac0)
            self.assertEqual(list(b[0x54:0x59]), saves)
            self.assertEqual(b[0x234], 10)
            self.assertEqual((b[0x237], b[0x275]), (1, 4))
        self.assertEqual(u(self.read('CSR26E1G'), 0x26, 'H'), 128)
        fist = self.resource('CSR26ELW.ITM').read_bytes()
        self.assertEqual(u(fist, 0x60), 2)
        self.assertEqual(u(fist, u(fist, 0x64)+0x18, 'H'), 2)
        self.assertEqual(self.resource('ELEAR.ITM').read_bytes(), self.donors['ELEAR.ITM'])

    def test_missing_preferred_and_fallback_donor_fails_before_any_write(self):
        self.resource('ELEARL01.CRE').unlink()
        self.assertNotEqual(self.run_install(), 0)
        self.assertIn('SUMELEAR.CRE', self.output)
        self.assertFalse(self.owned_resources())

    def test_owned_scripts_identity_and_stale_locals(self):
        self.assert_success()
        for ref, ai in [('CSR256FM', 'CSR26FMA'), ('CSR256CM', 'CSR26CMA'), ('CSR256G1', 'CSR26MEL')]:
            b = self.read(ref)
            self.assertEqual(s(b, 0x248), ai)
            self.assertTrue(all(s(b, o) == '' for o in (0x250, 0x258, 0x260, 0x268, 0x2cc)))
            self.assertEqual(s(b, 0x280, 32), ref)
            self.assertEqual(b[0x270], 255)
            self.assertEqual(u(b, 0x2c8), 1)
            self.assertEqual(u(b, u(b, 0x2c4)+8), 233)

    def test_tier_variants_have_same_slot_identity_and_reward(self):
        self.assert_success()
        for element in ('E', 'F'):
            for slot, tiers in [('1', 'LSG'), ('2', 'LS')]:
                for tier in tiers:
                    b = self.read(f'CSR26{element}{slot}{tier}')
                    self.assertEqual(s(b, 0x280, 32), f'CSR256{element}{slot}')
                    self.assertEqual(u(b, 0x14), 420)
                    self.assertEqual(s(b, 0x248), 'CSR26MEL')
                    self.assertFalse(book(b))
                if slot == '2':
                    self.assertFalse(self.resource(f'CSR26{element}2G.CRE').exists())
        self.assertEqual(2*u(self.read('CSR256FM'), 0x14)+2*u(self.read('CSR256G1'), 0x14)+4*420, 4520)

    def test_lesser_weapons_softened_and_source_resources_untouched(self):
        self.assert_success()
        for ref, dice in [('CSR26ELW', 2), ('CSR26FLW', 1)]:
            b = self.resource(ref+'.ITM').read_bytes()
            o = u(b, 0x64)
            self.assertEqual((u(b, 0x60), u(b, o+0x16, 'H'), u(b, o+0x18, 'H')), (2, 6, dice))
        self.assertEqual(self.resource('CSR26FLW.ITM').read_bytes()[-48:], self.donors['FIREELEL.ITM'][-48:])
        for name, original in self.donors.items():
            self.assertEqual(self.resource(name).read_bytes(), original, name)

    def test_preflight_does_not_create_owned_resources(self):
        self.assert_success(preflight_only=True)
        self.assertFalse(self.owned_resources())

    def test_v1_effects_preserve_proficiency_and_remove_stale_local(self):
        self.resource('BDOLONEI.CRE').write_bytes(creature(version=0))
        self.assert_success()
        b = self.read('CSR256FM')
        self.assertEqual(u(b, 0x2c8), 1)
        off = u(b, 0x2c4)
        self.assertEqual(u(b, off+8) if b[0x33] else u(b, off, 'H'), 233)
        self.assertEqual(book(b)['SPWI408'], 2)

    def test_ordinary_loot_has_no_random_helpers_or_droppable_plate_sword(self):
        self.assert_success()
        gear = inventory(self.read('CSR256G1'))
        self.assertEqual(set(gear), {'HELM01', 'PLAT01', 'SW2H02', 'POTN52'})
        self.assertTrue(gear['PLAT01'][1] & 8)
        self.assertTrue(gear['SW2H02'][1] & 8)
        self.assertFalse(gear['POTN52'][1] & 8)

    def test_other_spell_level_drift_fails_before_any_owned_resource(self):
        self.assertNotEqual(self.run_install(levels={'mirrorimage': 3}), 0)
        self.assertIn('changed spell level', self.output)
        self.assertFalse(self.owned_resources())

    def test_namespace_collision_is_preserved_and_stops_install(self):
        collision = b'existing foreign resource'
        path = self.resource('CSR256CM.CRE')
        path.write_bytes(collision)
        self.assertNotEqual(self.run_install(), 0)
        self.assertIn('already exists', self.output)
        self.assertEqual(path.read_bytes(), collision)
        self.assertEqual(self.owned_resources(), [path])

    def test_overlapping_tables_fail_before_any_owned_resource(self):
        b = bytearray(self.donors['BDOLONEI.CRE'])
        struct.pack_into('<I', b, 0x2a0, u(b, 0x2b0))
        self.resource('BDOLONEI.CRE').write_bytes(b)
        self.assertNotEqual(self.run_install(), 0)
        self.assertIn('overlapping', self.output)
        self.assertFalse(self.owned_resources())

    def test_unknown_effect_fails_before_any_owned_resource(self):
        b = bytearray(self.donors['BDOLONEI.CRE'])
        struct.pack_into('<I', b, u(b, 0x2c4)+8, 171)
        self.resource('BDOLONEI.CRE').write_bytes(b)
        self.assertNotEqual(self.run_install(), 0)
        self.assertIn('unreviewed donor effect', self.output)
        self.assertFalse(self.owned_resources())

    def seed_monk_policy(self, row='0x10d -1 1', count=106):
        for ref in ('C0PR#MO1.SPL', 'C0PR#MO2.SPL'):
            self.resource(ref).write_bytes(b'unchanged external helper')
        table = '2DA V1.0\n0xffff\nSTAT VALUE RELATION\n'
        table += ''.join(f'{i} {row if i == 105 else "0 0 0"}\n' for i in range(count))
        self.resource('SPLPROT.2DA').write_text(table)

    def assert_monk_policy_preserved(self, version):
        self.seed_monk_policy()
        donor = monk_policy_creature(version)
        self.resource('BDOLONEI.CRE').write_bytes(donor)
        helpers = {ref: self.resource(ref).read_bytes() for ref in
                   ('C0PR#MO1.SPL', 'C0PR#MO2.SPL', 'SPLPROT.2DA')}
        self.assert_success()
        for ref in ('CSR256FM', 'CSR256CM'):
            b = self.read(ref)
            self.assertEqual(effects(b), [effects(donor)[i] for i in (0, 2, 3)])
            self.assertEqual(book(b)['SPWI408'], 2)
            self.assertEqual((u(b, 0x24, 'H'), b[0x234]), (52, 13))
        self.assertEqual(self.resource('BDOLONEI.CRE').read_bytes(), donor)
        for ref, payload in helpers.items():
            self.assertEqual(self.resource(ref).read_bytes(), payload, ref)

    def test_v1_monk_policy_is_preserved_byte_exact_in_both_mages(self):
        self.assert_monk_policy_preserved(0)

    def test_v2_monk_policy_is_preserved_byte_exact_in_both_mages(self):
        self.assert_monk_policy_preserved(1)

    def test_monk_policy_signature_drift_fails_before_owned_writes(self):
        self.seed_monk_policy()
        for version in (0, 1):
            for key, value in dict(target=1, power=1, param1=2, param2=104,
                                   timing=9, duration=1, prob1=99, prob2=1,
                                   special=1).items():
                with self.subTest(version=version, field=key):
                    b = monk_policy_creature(version, **{key: value})
                    self.resource('BDOLONEI.CRE').write_bytes(b)
                    self.assertNotEqual(self.run_install(), 0)
                    self.assertIn('unreviewed donor effect', self.output)
                    self.assertFalse(self.owned_resources())

    def test_monk_policy_rejects_non_caster_and_unknown_helper(self):
        self.seed_monk_policy()
        b = bytearray(monk_policy_creature())
        b[0x273] = 2
        self.resource('BDCRUE45.CRE').write_bytes(b)
        self.assertNotEqual(self.run_install(), 0)
        self.assertIn('unreviewed donor effect', self.output)
        self.assertFalse(self.owned_resources())
        self.resource('BDCRUE45.CRE').write_bytes(self.donors['BDCRUE45.CRE'])
        self.resource('BDOLONEI.CRE').write_bytes(monk_policy_creature().replace(b'C0PR#MO1', b'C0PR#MOX'))
        self.assertNotEqual(self.run_install(), 0)
        self.assertIn('unreviewed donor effect', self.output)
        self.assertFalse(self.owned_resources())

    def test_v2_monk_policy_checks_special_after_the_save_bonus(self):
        self.seed_monk_policy()
        b = bytearray(monk_policy_creature())
        # Independent mutation: embedded EFF V2 special is at +0x40,
        # after save type (+0x38) and save bonus (+0x3c).
        struct.pack_into('<I', b, u(b, 0x2c4) + 2*264 + 0x40, 1)
        self.resource('BDOLONEI.CRE').write_bytes(b)
        self.assertNotEqual(self.run_install(), 0)
        self.assertIn('unreviewed donor effect', self.output)
        self.assertFalse(self.owned_resources())

    def test_monk_policy_requires_its_helpers_and_class_filter(self):
        self.resource('BDOLONEI.CRE').write_bytes(monk_policy_creature())
        for missing in ('C0PR#MO1.SPL', 'C0PR#MO2.SPL', 'SPLPROT.2DA'):
            with self.subTest(missing=missing):
                self.seed_monk_policy()
                self.resource(missing).unlink()
                self.assertNotEqual(self.run_install(), 0)
                self.assertIn('monk equipment policy is missing', self.output)
                self.assertFalse(self.owned_resources())
        for row in ('0x10c -1 1', '0x10d 1 1', '0x10d -1 5'):
            with self.subTest(row=row):
                self.seed_monk_policy(row)
                self.assertNotEqual(self.run_install(), 0)
                self.assertIn('changed semantics', self.output)
                self.assertFalse(self.owned_resources())
        self.seed_monk_policy(count=105)
        self.assertNotEqual(self.run_install(), 0)
        self.assertIn('requires SPLPROT row 105', self.output)
        self.assertFalse(self.owned_resources())

    def test_malformed_tables_fail_before_any_owned_resource(self):
        b = bytearray(self.donors['BDOLONEI.CRE'])
        struct.pack_into('<I', b, 0x2c4, len(b)+1)
        self.resource('BDOLONEI.CRE').write_bytes(b)
        self.assertNotEqual(self.run_install(), 0)
        self.assertIn('out of bounds', self.output)
        self.assertFalse(self.owned_resources())


if __name__ == '__main__':
    unittest.main()
