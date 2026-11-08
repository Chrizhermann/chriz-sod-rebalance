"""Synthetic Forest of Wyrms records: changed input, the same owned result."""
from pathlib import Path
import struct
import unittest
from test_comp285_installer import InstallerFixture, WEIDU


def area(names=(), travel=True):
    data = bytearray(0x11c + len(names)*0x110)
    data[:8] = b'AREAV1.0'
    struct.pack_into('<IH', data, 0x54, 0x11c, len(names))
    for i, name in enumerate(names):
        at = 0x11c + i*0x110
        data[at:at+32] = name.encode().ljust(32, b'\0')
        struct.pack_into('<4H', data, at+0x20, 123, 456, 123, 456)
        struct.pack_into('<I', data, at+0x40, 0xffffffff)
        data[at+0x80:at+0x88] = b'FOREIGN\0'
    if travel:
        ro = len(data); data.extend(bytes(0xc4))
        struct.pack_into('<HI', data, 0x5a, 1, ro)
        data[ro:ro+32] = b'TranBD7220'.ljust(32, b'\0')
        struct.pack_into('<H', data, ro+0x20, 2)
        data[ro+0x38:ro+0x40] = b'BD7220\0\0'
        data[ro+0x40:ro+0x60] = b'ExitBD7220'.ljust(32, b'\0')
        struct.pack_into('<I', data, ro+0x60, 1540)
        eo = len(data); data.extend(bytes(0x68))
        struct.pack_into('<II', data, 0x68, eo, 1)
        data[eo:eo+32] = b'ExitBD7220'.ljust(32, b'\0')
        struct.pack_into('<HHH', data, eo+32, 111, 222, 3)
    return bytes(data)


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable')
class ForestInstallerTests(InstallerFixture):
    def setUp(self):
        super().setUp()
        for name, content in {
            'action': '30 SetGlobal(S:Name*,S:Area*,I:Value*)\n36 Continue()\n164 AddexperienceParty(I:XP*)\n',
            'trigger': '0x400F Global(S:Name*,S:Area*,I:Value*)\n0x4032 Dead(S:Name*)\n',
        }.items():
            (self.override/f'{name}.ids').write_text('IDS V1.0\n'+content)
        self.names = ('CULTIST_AMBUSH1', 'CULTIST_AMBUSH6', 'KEPT_FOREIGN')
        for name, data in {'bd7200': area(), 'bd7210': area(),
                           'bd7230': area(self.names)}.items():
            (self.override/f'{name}.are').write_bytes(data)
        (self.override/'bd7230.bcs').write_bytes(b'SC\nSC\n')
        self.tp2 = 'BACKUP ~forest-backup~ AUTHOR ~test~ BEGIN ~forest~\nINCLUDE ~chriz-sod-remix/lib/comp240.tpa~\n'
        (self.game/'forest.tp2').write_text(self.tp2)

    def apply(self):
        self.assert_success(self.run_weidu('forest.tp2', '--force-install-list', '0'))
        for name, destination in (('bd7210', b'BD7230'), ('bd7230', b'BD7210')):
            data = (self.override/f'{name}.are').read_bytes()
            ro = struct.unpack_from('<I', data, 0x5c)[0]
            self.assertEqual(data[ro+0x38:ro+0x40].rstrip(b'\0'), destination)
            self.assertEqual(struct.unpack_from('<H', data, ro+0x20)[0], 2)
            self.assertFalse(struct.unpack_from('<I', data, ro+0x60)[0] & 0x100)
            self.assertEqual(struct.unpack_from('<I', data, 0x6c)[0], 1)
        data = (self.override/'bd7230.are').read_bytes()
        ao = struct.unpack_from('<I', data, 0x54)[0]
        self.assertEqual([struct.unpack_from('<I', data, ao+i*0x110+0x40)[0]
                          for i in range(3)], [0, 0, 0xffffffff])
        script = self.decompile('bd7230.bcs')
        self.assertEqual(script.count('AddexperienceParty(22700)'), 1)

    def test_owned_fields_and_unrelated_actor_bytes(self):
        before = (self.override/'bd7230.are').read_bytes()
        self.apply()
        expected = bytearray(before)
        for i in (0, 1): struct.pack_into('<I', expected, 0x11c+i*0x110+0x40, 0)
        ro = struct.unpack_from('<I', expected, 0x5c)[0]
        expected[ro+0x38:ro+0x40] = b'BD7210\0\0'
        self.assertEqual((self.override/'bd7230.are').read_bytes(), expected)

    def test_changed_actor_values_and_old_route_are_overwritten(self):
        for name in ('bd7210', 'bd7230'):
            data = bytearray((self.override/f'{name}.are').read_bytes())
            ro = struct.unpack_from('<I', data, 0x5c)[0]
            struct.pack_into('<H', data, ro+0x20, 0)
            struct.pack_into('<I', data, ro+0x60, 0x100)
            data[ro+0x38:ro+0x40] = b'FOREIGN\0'
            (self.override/f'{name}.are').write_bytes(data)
        self.apply()

    def test_missing_travel_records_and_script_are_created(self):
        (self.override/'bd7210.are').write_bytes(area(travel=False))
        (self.override/'bd7230.are').write_bytes(area(self.names, travel=False))
        (self.override/'bd7230.bcs').unlink()
        self.apply()

    def test_second_tail_is_byte_identical(self):
        self.apply()
        before = {p.name:p.read_bytes() for p in self.override.iterdir()}
        (self.game/'second.tp2').write_text(self.tp2.replace('forest-backup','second-backup'))
        self.assert_success(self.run_weidu('second.tp2', '--force-install-list', '0'))
        self.assertEqual({p.name:p.read_bytes() for p in self.override.iterdir()}, before)


if __name__ == '__main__':
    unittest.main()
